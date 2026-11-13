"""C4 — local-only Git/PR review simulation (Q5 default: plain git + review-record files; findings-W3).

  setup            git init (no remote), v1 commit, tag v1
  branches         change-proposal branch(es) + seeded broken branches
  normalize        review records (JSON, GitHub review-comment fields) -> register candidates (channel pr)
  gate             pre-merge check: export branch head (git archive), compile through C1, verdict rule
  pr_merge         the ONLY merge path: gate, and on PASS `git merge --no-ff` with Resolves:/Gate: trailers

Gate verdict rule (stated, findings-W3 §3; finding #357 is settled empirically by the gate log):
  FAIL iff  exit != 0  OR  semantic XML missing/empty  OR  any `asciidoctor: ERROR|WARNING|FATAL` line
            OR  any err.html entry of severity 0 or 1 that is NOT in the base-branch baseline
            (entries keyed on (severity, code, message) with generated UUIDs normalised).
The log also records what W0's proposed rule (exit != 0 OR any severity-0 entry) and an exit-code-only rule
would have said, so the necessity of the stronger rule is demonstrated, not asserted.
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import io
import re
import shutil
import tarfile
from pathlib import Path

from common import ASCIIDOCTOR_DIAG, die, dump_json, load_json, mn_compile, parse_errhtml
from gitx import Git, apply_edits

SECRETARIAT = ("Secretariat", "secretariat@example.invalid")


def setup(repo: Path, srcdir: Path) -> Git:
    if repo.exists():
        shutil.rmtree(repo)
    g = Git(repo)
    g.init()
    for f in sorted(srcdir.iterdir()):
        shutil.copy(f, repo / f.name)
    g.commit("v1: committee draft for review\n\nInitial v1 source of ISO/CD 99999-1 (fictitious).", who=("Editor", "editor@example.invalid"))
    g("tag", "v1")
    return g


def create_branch(g: Git, name: str, commits: list[dict]) -> str:
    g("checkout", "-q", "-b", name, "v1")
    for c in commits:
        apply_edits(g.repo, c["edits"], c.get("id", name))
        msg = c["message"] + ("\n\nComment-Id: " + c["id"] if c.get("id") else "")
        g.commit(msg, who=tuple(c.get("who", SECRETARIAT)))
    head = g("rev-parse", "HEAD").strip()
    g("checkout", "-q", "main")
    return head


def add_commit_on(g: Git, branch: str, cid: str, disposition: str, edits: list[dict]) -> str:
    g("checkout", "-q", branch)
    apply_edits(g.repo, edits, cid)
    sha = g.commit(f"Resolve {cid} ({disposition})\n\nComment-Id: {cid}")
    g("checkout", "-q", "main")
    return sha


# ---------------- review-record normaliser (C4.2) ----------------
def _hunk_map(diff: str):
    """Parse a -U3 unified diff into per-side line maps: {('RIGHT'|'LEFT', n): base_line|None}."""
    m = {}
    old = new = 0
    block_minus: list[int] = []
    plus_idx = 0
    last_ctx_old = None
    for ln in diff.split("\n"):
        h = re.match(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@", ln)
        if h:
            old, new = int(h.group(1)), int(h.group(3))
            block_minus, plus_idx, last_ctx_old = [], 0, old - 1
            continue
        if not ln or ln.startswith(("diff ", "index ", "--- ", "+++ ", "\\")):
            continue
        if ln.startswith("-"):
            if plus_idx:
                block_minus, plus_idx = [], 0
            block_minus.append(old)
            m[("LEFT", old)] = ("removed", old)
            old += 1
        elif ln.startswith("+"):
            if block_minus:
                base = block_minus[min(plus_idx, len(block_minus) - 1)]
            else:
                base = last_ctx_old if last_ctx_old and last_ctx_old > 0 else None
            m[("RIGHT", new)] = ("added", base)
            plus_idx += 1
            new += 1
        elif ln.startswith(" "):
            m[("LEFT", old)] = ("context", old)
            m[("RIGHT", new)] = ("context", old)
            last_ctx_old = old
            block_minus, plus_idx = [], 0
            old += 1
            new += 1
    return m


def normalize(g: Git, reviews_dir: Path, out: Path) -> list[dict]:
    cands = []
    for rf in sorted(reviews_dir.glob("*/*.json")):
        rec = load_json(rf)["review"]
        branch = rec["branch"]
        head = g("rev-parse", branch).strip()
        base = g("merge-base", "v1", head).strip()
        for c in rec["comments"]:
            diff = g("diff", "-U3", "--no-color", f"{base}..{head}", "--", c["path"])
            hm = _hunk_map(diff)
            pre, v1_line, v1_end = [], None, None
            key = (c["side"], int(c["line"]))
            if c["side"] not in ("LEFT", "RIGHT"):
                pre.append(f"bad_side ('{c['side']}')")
            elif key not in hm:
                pre.append(f"line_not_in_diff ({c['side']} line {c['line']} of {c['path']} is outside every hunk of {branch})")
            else:
                v1_end = hm[key][1]
                if c.get("start_line"):
                    sk = (c.get("start_side", c["side"]), int(c["start_line"]))
                    if sk not in hm:
                        pre.append(f"line_not_in_diff (range start {sk} outside every hunk)")
                    else:
                        v1_line = hm[sk][1]
                else:
                    v1_line = v1_end
                if v1_line is None:
                    pre.append("line_not_in_diff (insertion with no base line)")
            cands.append({
                "review_file": f"{rf.parent.name}/{rf.name}", "local_id": c["local_id"],
                "reviewer": rec["reviewer"]["name"], "header_mb": rec["reviewer"]["mb"], "mb": c.get("mb", rec["reviewer"]["mb"]),
                "date": rec["date"], "type": c.get("type", ""), "comment": c.get("comment", ""),
                "proposed_change": c.get("proposed_change", ""), "observations": c.get("observations", ""),
                "source_branch": branch, "source_commit": head, "source_path": c["path"], "side": c["side"],
                "source_line": int(c["line"]), "start_line": c.get("start_line"),
                "v1_line": v1_line, "v1_end_line": v1_end if c.get("start_line") else None, "pre_reasons": pre,
            })
    dump_json(cands, out)
    return cands


# ---------------- pre-merge gate (C4.3) ----------------
def _export(g: Git, sha: str, dest: Path):
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    import subprocess
    p = subprocess.run(["git", "-C", str(g.repo), "archive", "--format=tar", sha], capture_output=True, env=g.env)
    if p.returncode != 0:
        die(f"git archive {sha} failed")
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as t:
        t.extractall(dest, filter="data")


def gate(g: Git, ref: str, gatedir: Path, baseline: dict | None) -> dict:
    sha = g("rev-parse", ref).strip()
    slug = ref.replace("/", "__")
    wd = gatedir / slug
    _export(g, sha, wd)
    log = gatedir / f"{slug}.compile.log"
    rc = mn_compile(wd, "draft.adoc", "xml,html,pdf", log)
    xml = wd / "draft.xml"
    xml_ok = xml.exists() and xml.stat().st_size > 0
    diags = ASCIIDOCTOR_DIAG.findall(log.read_text(encoding="utf-8"))
    diag_lines = [m.group(0) for m in ASCIIDOCTOR_DIAG.finditer(log.read_text(encoding="utf-8"))]
    entries = parse_errhtml(wd / "draft.err.html")
    keyset = sorted({(e["severity"], e["code"], e["message"]) for e in entries if e["severity"] <= 1})
    res = {"ref": ref, "sha": sha, "exit": rc, "xml": xml_ok, "asciidoctor_diag": diag_lines,
           "sev01": [list(k) for k in keyset], "sev0_count": sum(1 for e in entries if e["severity"] == 0),
           "severity_by_code": sorted({f"{e['code']}={e['severity']}" for e in entries})}
    if baseline is None:
        res["verdict"] = "BASELINE" if (rc == 0 and xml_ok and not diag_lines) else "BASELINE-BROKEN"
        res["new_sev01"] = []
    else:
        base = {tuple(x) for x in baseline["sev01"]}
        new = [list(k) for k in keyset if tuple(k) not in base]
        res["new_sev01"] = new
        fail = rc != 0 or not xml_ok or bool(diag_lines) or bool(new)
        res["verdict"] = "FAIL" if fail else "PASS"
    res["rule_w0_exit_or_sev0"] = "FAIL" if (rc != 0 or res["sev0_count"] > 0) else "PASS"
    res["rule_exit_only"] = "FAIL" if rc != 0 else "PASS"
    dump_json(res, gatedir / f"{slug}.gate.json")
    with open(gatedir / "gate.tsv", "a", encoding="utf-8") as f:
        f.write("\t".join([ref, sha, f"exit={rc}", f"xml={'yes' if xml_ok else 'no'}",
                           f"asciidoctor_diag={len(diag_lines)}", f"new_sev01={len(res['new_sev01'])}",
                           f"sev0={res['sev0_count']}", f"verdict={res['verdict']}",
                           f"w0_rule={res['rule_w0_exit_or_sev0']}", f"exit_only_rule={res['rule_exit_only']}"]) + "\n")
    shutil.rmtree(wd / "relaton", ignore_errors=True)
    return res


def pr_merge(g: Git, branch: str, resolves: list[str], gatedir: Path, baseline: dict) -> dict:
    res = gate(g, branch, gatedir, baseline)
    if res["verdict"] != "PASS":
        res["merged"] = False
        return res
    msg = f"Merge {branch}\n\n" + "".join(f"Resolves: {i}\n" for i in sorted(resolves)) + f"Gate: PASS {res['sha']}\n"
    res["merge_commit"] = g.merge(branch, msg)
    res["merged"] = True
    return res
