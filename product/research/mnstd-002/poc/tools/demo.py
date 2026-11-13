"""`make demo` driver: frozen-task verify -> run A -> self-tests on A -> run B (from clean) -> cross-run NFR checks
(N1.2 artefact set, N3.1 determinism, N3.2 edit-path SHAs) -> evidence snapshot into ../artifacts (N7 budget).
Usage: demo.py <build-dir> <artifacts-dir>
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frozen  # noqa: E402
from common import N, POC, dump_json, load_json, sha256  # noqa: E402

# N3.1 identity set (byte comparison with cmp semantics). Declared normalisation list for v2 semantic XML: EMPTY
# by construction (revdate, copyright-year, secretariat, committee pinned in the source; image pinned by digest;
# annotation dates always explicit). The defensive list below is applied ONLY if cmp fails, and every hit is reported.
IDENTITY = ["intake/final/register.json", "intake/final/register.yaml", "intake/final/register.csv",
            "trace/trace.csv", "trace/trace.yaml", "trace/trace.json", "trace/register.resolved.json",
            "report/report.html", "report/report.yaml", "report/report.csv", "v2/draft.xml"]
INFO_ONLY = ["v1/draft.xml", "v1/draft.presentation.xml", "v2/draft.presentation.xml", "review/build/draft.xml",
             "map/mapping.json", "gate/gate.tsv", "v1/draft.html", "v2/draft.html", "v1/draft.pdf", "v2/draft.pdf",
             "review/build/draft.pdf", "checks/summary.json"]
DEFENSIVE = [("bibdata/copyright/from", "copyright year from the clock if :copyright-year: unset"),
             ("bibdata/docidentifier (year suffix)", "falls back to Date.today.year"),
             ("bibdata/date/on, bibdata/version", "from :revdate:"),
             ("annotation/@date", "Date.today when the date attribute is absent"),
             ("@schema-version", "bound to gem versions (image-pinned)")]


def sh(*cmd, env=None):
    print(f"[demo] $ {' '.join(cmd)}", flush=True)
    return subprocess.run(list(cmd), env=env).returncode


def normalise_xml(p: Path) -> bytes:
    root = ET.parse(p).getroot()
    for e in root.iter():
        if "schema-version" in e.attrib:
            e.attrib["schema-version"] = "*"
        if e.tag == N + "annotation" and "date" in e.attrib:
            e.attrib["date"] = "*"
    for path in ("bibdata/copyright/from", "bibdata/date/on", "bibdata/version/revision-date"):
        for e in root.findall("/".join(N + x for x in path.split("/"))):
            e.text = "*"
    for e in root.findall(f"{N}bibdata/{N}docidentifier"):
        e.text = re.sub(r":\d{4}", ":*", e.text or "")
    return ET.tostring(root)


def files(R: Path):
    return sorted(str(p.relative_to(R)) for p in R.rglob("*") if p.is_file() and ".git" not in p.relative_to(R).parts
                  and not str(p.relative_to(R)).startswith("selftest"))


def git_shas(R: Path):
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_CEILING_DIRECTORIES=str(R))
    out = subprocess.run(["git", "-C", str(R / "repo"), "log", "--all", "--format=%H %s"], capture_output=True, text=True, env=env).stdout
    tags = {t: subprocess.run(["git", "-C", str(R / "repo"), "rev-parse", t], capture_output=True, text=True, env=env).stdout.strip()
            for t in ("v1", "v2", "main")}
    return out, tags


def compare(A: Path, B: Path) -> dict:
    fa, fb = files(A), files(B)
    set_eq = fa == fb
    ident = []
    for f in IDENTITY:
        same = (A / f).read_bytes() == (B / f).read_bytes()
        row = {"file": f, "identical": same, "normalised_identical": None, "sha256_a": sha256(A / f), "sha256_b": sha256(B / f)}
        if not same and f.endswith(".xml"):
            row["normalised_identical"] = normalise_xml(A / f) == normalise_xml(B / f)
        ident.append(row)
    info = []
    for f in INFO_ONLY:
        if (A / f).exists() and (B / f).exists():
            info.append({"file": f, "identical": (A / f).read_bytes() == (B / f).read_bytes()})
    la, ta = git_shas(A)
    lb, tb = git_shas(B)
    n31 = all(r["identical"] or r["normalised_identical"] for r in ident)
    return {
        "N1.2": {"result": "PASS" if set_eq and load_json(B / "checks" / "summary.json") else "FAIL",
                 "artefact_set_equal": set_eq, "files_a": len(fa), "files_b": len(fb),
                 "only_a": sorted(set(fa) - set(fb))[:20], "only_b": sorted(set(fb) - set(fa))[:20]},
        "N3.1": {"result": "PASS" if n31 else "FAIL", "identity_set": ident,
                 "declared_normalisation": "none needed (empty list) unless an identity file differs; defensive list applied only then",
                 "defensive_list": DEFENSIVE, "normalised_hits": [r["file"] for r in ident if not r["identical"]],
                 "info_only": info},
        "N3.2": {"result": "PASS" if (la == lb and ta == tb) else "FAIL", "tags_a": ta, "tags_b": tb,
                 "all_commit_shas_identical": la == lb},
    }


def snapshot(A: Path, art: Path, extra: dict):
    ev = art / "evidence"
    if ev.exists():
        shutil.rmtree(ev)
    keep = ["steps.json", "envelope.json", "command-trace.log", "checks/summary.json", "checks/warnings.json",
            "checks/c4.4-gitlog.tsv", "c2/locators.json", "c2/lines.json", "v1/srcmap.json",
            "intake/A/register.json", "intake/B/register.json", "intake/B/rejects.csv", "intake/B/rejects.json",
            "intake/final/register.json", "intake/final/register.yaml", "intake/final/register.csv",
            "intake/final/rejects.csv", "pr/candidates.json", "dispositions/validation.json",
            "dispositions/validation-bad.json", "gate/gate.tsv", "gate/merges.json", "map/mapping.json",
            "trace/trace.csv", "trace/trace.yaml", "trace/containment.json", "trace/register.resolved.json",
            "review/projection-plan.json", "review/annotations.json", "review/clean-annotations.json",
            "review/input/draft.adoc", "report/report.yaml", "report/report.csv", "selftest.json",
            "v1/compile.log", "v2/compile.log", "review/build/compile.log", "selftest-command-trace.log"]
    keep += sorted(str(p.relative_to(A)) for p in (A / "gate").glob("*.gate.json"))
    for f in keep:
        if (A / f).exists():
            (ev / f).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(A / f, ev / f)
    out, tags = git_shas(A)
    env = dict(os.environ, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", GIT_CEILING_DIRECTORIES=str(A))
    glog = subprocess.run(["git", "-C", str(A / "repo"), "log", "--all", "--graph", "--decorate",
                           "--format=%H %d%n    author: %an <%ae> %aI%n    %s%n%(trailers:only,unfold)"],
                          capture_output=True, text=True, env=env).stdout
    (ev / "repo-git-log.txt").write_text(glog)
    (ev / "repo-remote-v.txt").write_text(subprocess.run(["git", "-C", str(A / "repo"), "remote", "-v"], capture_output=True, text=True, env=env).stdout or "(no remotes)\n")
    dump_json(extra, ev / "cross-run.json")
    # N7: budget and listing (generated HTML/PDF/XML/DOCX and archives are never snapshotted)
    listing, total, banned = [], 0, []
    for p in sorted(art.rglob("*")):
        if p.is_file():
            sz = p.stat().st_size
            total += sz
            listing.append((str(p.relative_to(art)), sz))
            if p.suffix.lower() in (".html", ".htm", ".pdf", ".xml", ".docx", ".doc", ".tar", ".tgz", ".gz", ".zip"):
                banned.append(str(p.relative_to(art)))
    budget = 5 * 1024 * 1024
    lines = ["# Evidence snapshot listing (N7.1)", "", f"Budget: {budget} bytes (5 MB, researcher-proposed). Total: {total} bytes. "
             f"Within budget: {total <= budget}. Generated HTML/PDF/XML/DOCX/archives present: {banned or 'none'}.", "",
             "| file | bytes |", "|---|---:|"] + [f"| `{f}` | {s} |" for f, s in listing]
    (art / "SNAPSHOT.md").write_text("\n".join(lines) + "\n")
    return {"total_bytes": total, "budget_bytes": budget, "within_budget": total <= budget, "banned_types": banned,
            "files": len(listing)}


def main(argv):
    build, art = Path(argv[0]).resolve(), Path(argv[1]).resolve()
    probs = frozen.verify()
    if probs:
        print("[demo] FROZEN TASK TAMPERED:", probs, file=sys.stderr)
        return 3
    print("[demo] frozen task verified (task/FROZEN.sha256)")
    rc = {}
    for run in ("run-a", "run-b"):
        R = build / run
        if R.exists():
            shutil.rmtree(R)
        R.mkdir(parents=True)
        env = dict(os.environ, MNSTD_TRACE=str(R / "command-trace.log"))
        (R / "command-trace.log").write_text("")
        rc[run] = sh(sys.executable, str(POC / "tools" / "pipeline.py"), str(R), env=env)
        if run == "run-a":
            st_env = dict(env, MNSTD_TRACE=str(R / "selftest-command-trace.log"))
            rc["selftest"] = sh(sys.executable, str(POC / "tools" / "selftest.py"), str(R), str(R / "selftest.json"), env=st_env)
    A, B = build / "run-a", build / "run-b"
    cross = compare(A, B)
    snap = snapshot(A, art, cross)
    cross["N7.1"] = {"result": "PASS" if snap["within_budget"] and not snap["banned_types"] else "FAIL", **snap}
    dump_json(cross, art / "evidence" / "cross-run.json")
    inv = art / "invocations"
    inv.mkdir(parents=True, exist_ok=True)
    k = len(list(inv.glob("demo-*.json"))) + 1
    env_a = load_json(A / "envelope.json")
    dump_json({"invocation": k, "captured_at_utc": env_a["captured_at_utc"],
               "identity_sha256": {r["file"]: r["sha256_a"] for r in cross["N3.1"]["identity_set"]},
               "tags": cross["N3.2"]["tags_a"],
               "results": {c["clause"]: c["result"] for c in load_json(A / "checks" / "summary.json")} |
                          {x: cross[x]["result"] for x in ("N1.2", "N3.1", "N3.2", "N7.1")},
               "selftest_detected": f"{sum(x['detected'] for x in load_json(A / 'selftest.json')['cases'])}/{len(load_json(A / 'selftest.json')['cases'])}",
               "exit_codes": rc}, inv / f"demo-{k}.json")
    summary = load_json(A / "checks" / "summary.json")
    fails = [c["clause"] for c in summary if c["result"] == "FAIL"]
    print("\n[demo] ================= SUMMARY =================")
    for c in summary:
        print(f"[demo] {c['clause']:6} {c['result']:4}  {c['summary'][:150]}")
    for k in ("N1.2", "N3.1", "N3.2", "N7.1"):
        print(f"[demo] {k:6} {cross[k]['result']:4}  (cross-run)")
    st = load_json(A / "selftest.json")
    print(f"[demo] selftest: {sum(x['detected'] for x in st['cases'])}/{len(st['cases'])} tampered cases detected")
    print(f"[demo] exit codes: {rc}")
    bad = fails or any(v != 0 for v in rc.values()) or any(cross[k]["result"] != "PASS" for k in ("N1.2", "N3.1", "N3.2", "N7.1"))
    print(f"[demo] {'FAILED' if bad else 'OK'}: per-run FAILs {fails}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
