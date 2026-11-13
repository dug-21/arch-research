"""Per-run clause checks (C1.1 … C7.3 and the run-local NFR checks). Every check reads ONLY emitted artefacts,
the frozen task/ fixtures and the inner git history; each returns PASS/FAIL with the evidence it used.
These checks are the POC's self-assessment, not a grade (the validator rules; the human decides).
Cross-run NFR checks (N1.2, N3.1, N3.2) live in demo.py. Self-tests of these checkers: selftest.py.
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import csv
import io
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import (ANY_REGISTER_ID_RE, ASCIIDOCTOR_DIAG, ISO_COLUMNS, ISO_KEYS, MN_IMAGE, N, POC, REGISTER_ID_RE,  # noqa: E402
                    TYPES, load_json, local, norm, parse_errhtml, text_of)
from gitx import Git, apply_edits_text, trailers  # noqa: E402
from resolver import Doc, Err  # noqa: E402

TASK = POC.parent / "task"


def res(clause, ok, summary, evidence, details=None, result=None):
    return {"clause": clause, "result": result or ("PASS" if ok else "FAIL"), "summary": summary,
            "evidence": evidence, "details": details or {}}


def _code(reason: str) -> str:
    return re.split(r"[ (]", reason, maxsplit=1)[0]


class Ctx:
    def __init__(self, R: Path, task: Path = TASK):
        self.R, self.task = Path(R), Path(task)
        self.steps = load_json(self.R / "steps.json")
        self._cache = {}

    def doc(self, name):
        if name not in self._cache:
            self._cache[name] = Doc(self.R / name)
        return self._cache[name]

    @property
    def register(self):
        return load_json(self.R / "intake" / "final" / "register.json")

    @property
    def disp(self):
        return {d["id"]: d for d in load_json(self.task / "dispositions.json")["dispositions"]}

    def git(self):
        return Git(self.R / "repo")


# ---------------------------------------------------------------- C1
def c1_1(c: Ctx):
    src = (POC / "src" / "draft.adoc").read_text(encoding="utf-8")
    sem = ET.parse(c.R / "v1" / "draft.xml").getroot()
    need = {
        "foreword": bool(re.search(r"^\.Foreword$", src, re.M)) and sem.find(f".//{N}preface/{N}foreword") is not None,
        "scope": sem.find(f".//{N}sections/{N}clause[@type='scope']") is not None,
        "normative_references": sem.find(f".//{N}bibliography/{N}references[@normative='true']") is not None,
        "terms_and_definitions": len(sem.findall(f".//{N}terms/{N}term")) >= 1,
        "numbered_clauses>=3": len([x for x in sem.find(f".//{N}sections") if local(x.tag) in ("clause", "terms")]) >= 3,
        "subclause_level>=1": len(sem.findall(f".//{N}sections/{N}clause/{N}clause")) >= 1,
        "table>=1": len(sem.findall(f".//{N}table")) >= 1,
        "figure>=1": len(sem.findall(f".//{N}figure")) >= 1,
        "note>=1": len(sem.findall(f".//{N}note")) >= 1,
        "annex>=1": len(sem.findall(f".//{N}annex")) >= 1,
    }
    outs = {x: (c.R / "v1" / f"draft.{x}").exists() and (c.R / "v1" / f"draft.{x}").stat().st_size > 0 for x in ("html", "pdf", "xml")}
    pdf_magic = (c.R / "v1" / "draft.pdf").read_bytes()[:5] == b"%PDF-" if outs["pdf"] else False
    ok = all(need.values()) and all(outs.values()) and pdf_magic and c.steps["v1_compile_exit"] == 0
    return res("C1.1", ok, f"structure {sum(need.values())}/{len(need)}; outputs {outs}; exit {c.steps['v1_compile_exit']}",
               ["poc/src/draft.adoc", "v1/compile.log", "v1/draft.{html,pdf,xml}"], {"structure": need, "outputs": outs, "pdf_magic": pdf_magic})


def warnings_table(R: Path, build: str):
    exp = load_json(POC / "warnings-explained.json")
    d = R / build
    rows, errors = [], []
    for e in parse_errhtml(d / "draft.err.html"):
        m = exp["errhtml"].get(e["code"])
        rows.append({"source": "err.html", "severity": e["severity"], "code": e["code"], "message": e["message"][:160],
                     "attribution": m["attribution"] if m else "UNEXPLAINED", "explanation": m["explanation"] if m else ""})
        if e["severity"] == 0:
            errors.append(f"severity 0: {e['code']} {e['message']}")
    log = (d / "compile.log").read_text(encoding="utf-8")
    for line in [x.group(0) for x in ASCIIDOCTOR_DIAG.finditer(log)]:
        m = next((p for p in exp["asciidoctor"] if re.search(p["regex"], line)), None)
        rows.append({"source": "asciidoctor", "severity": "", "code": "asciidoctor", "message": line,
                     "attribution": m["attribution"] if m else "UNEXPLAINED", "explanation": m["explanation"] if m else ""})
        if "ERROR" in line or "FATAL" in line:
            errors.append(line)
    pe = d / "draft.pdf.err"
    seen = set()
    if pe.exists():
        for line in pe.read_text(encoding="utf-8", errors="replace").split("\n"):
            if not line.strip() or line in seen:
                continue
            seen.add(line)
            m = next((p for p in exp["pdf_err"] if re.search(p["regex"], line)), None)
            rows.append({"source": "pdf.err", "severity": "", "code": "mn2pdf", "message": line[:160],
                         "attribution": m["attribution"] if m else "UNEXPLAINED", "explanation": m["explanation"] if m else ""})
            if re.search(r"\b(ERROR|SEVERE|FATAL)\b", line):
                errors.append(line)
    if re.search(r"^\[mn2pdf\] Fatal error|FATAL ERRORS", log, re.M):
        errors.append("fatal error in compile log")
    return rows, errors


def _boilerplate_location_ok(R: Path, build: str) -> list[str]:
    """For entries whose explanation requires a location in the injected boilerplate, verify it mechanically."""
    exp = load_json(POC / "warnings-explained.json")["errhtml"]
    d = R / build
    pres = ET.parse(d / "draft.presentation.xml").getroot()
    semx_anchor = {e.get("semx-id"): (e.get("anchor") or e.get("id")) for e in pres.iter() if e.get("semx-id")}
    bad = []
    # parse_errhtml normalises ids to _UUID; re-read the raw table for the actual element id
    raw =(d / "draft.err.html").read_text(encoding="utf-8").replace("​", "").replace("­", "")
    checked = 0
    for m in re.finditer(r"<th><code>[^<]*#(_[0-9a-f-]{36})</code></th><td>(ISO_\d+|STANDOC_\d+)</td>", raw):
        want = exp.get(m.group(2), {}).get("must_be_located_in_anchor")
        if want:
            checked += 1
            if semx_anchor.get(m.group(1)) != want:
                bad.append(f"{m.group(2)} located at {m.group(1)} ({semx_anchor.get(m.group(1))}), expected {want}")
    required = sum(1 for e in parse_errhtml(d / "draft.err.html") if exp.get(e["code"], {}).get("must_be_located_in_anchor"))
    if checked != required:
        bad.append(f"location of {required - checked} boilerplate-attributed warning(s) could not be verified")
    return bad


def c1_2(c: Ctx):
    out = {}
    allbad = []
    for b in ("v1", "v2"):
        rows, errors = warnings_table(c.R, b)
        loc_bad = _boilerplate_location_ok(c.R, b)
        unexpl = [r for r in rows if r["attribution"] == "UNEXPLAINED"]
        out[b] = {"warnings": rows, "errors": errors, "unexplained": unexpl, "location_violations": loc_bad}
        allbad += errors + [f"unexplained: {u['message']}" for u in unexpl] + loc_bad
    (c.R / "checks").mkdir(exist_ok=True)
    (c.R / "checks" / "warnings.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n = sum(len(v["warnings"]) for v in out.values())
    return res("C1.2", not allbad, f"errors 0 required; {n} warning lines (v1+v2), unexplained/errors: {len(allbad)}",
               ["checks/warnings.json", "poc/warnings-explained.json", "v1/draft.err.html", "v1/draft.pdf.err"], {"problems": allbad})


def c1_3(c: Ctx):
    d = c.doc("v1")
    sem = d.sem
    flavor = sem.get("flavor") == "iso" and (sem.findtext(f"{N}bibdata/{N}ext/{N}flavor") == "iso")
    stage = sem.find(f"{N}bibdata/{N}status/{N}stage")
    draft = stage is not None and stage.get("abbreviation") == "CD" and stage.text == "30" and \
        sem.findtext(f".//{N}semantic-metadata/{N}stage-published") == "false"
    src = (POC / "src" / "draft.adoc").read_text(encoding="utf-8")
    anchors = re.findall(r"^\[\[([A-Za-z0-9_-]+)\]\]$", src, re.M)
    rows, missing = [], []
    for a in anchors:
        e = d.by_anchor.get(a)
        if e is None:
            missing.append(a)
            continue
        t = local(e.tag)
        if t not in ("clause", "terms", "references", "annex", "table", "figure", "term", "note", "introduction"):
            continue
        num = d.number.get(e.get("id"), "")
        ok = bool(e.get("id")) and (bool(num) or t == "introduction")
        rows.append({"anchor": a, "tag": t, "id": e.get("id"), "number": num, "ok": ok})
        if not ok:
            missing.append(a)
    need_kinds = {"clause", "table", "figure"} <= {r["tag"] for r in rows}
    ok = flavor and draft and not missing and need_kinds
    return res("C1.3", ok, f"flavor iso={flavor}; draft stage CD/30 unpublished={draft}; {len(rows)} authored elements with id+number; missing {missing}",
               ["v1/draft.xml", "v1/draft.presentation.xml"], {"elements": rows})


# ---------------------------------------------------------------- C2
def _match(d: Doc, r: dict, case: dict) -> bool:
    e = d.by_id[r["id"]]
    if case.get("anchor"):
        good = e.get("anchor") == case["anchor"]
    else:
        good = d.own_text(e).startswith(case["text"]) or norm(text_of(e)).startswith(case["text"])
    return good and r["clause"] == case["clause_no"]


def c2_locators(c: Ctx, expected: Path | None = None):
    d = c.doc("v1")
    fx = load_json(expected or c.task / "expected" / "locators.json")
    pos, neg = [], []
    for case in fx["positive"]:
        try:
            r = d.resolve(case["clause"], case["element"])
            ok = _match(d, r, case)
            pos.append({**case, "got": r, "pass": ok})
        except Err as x:
            pos.append({**case, "got": {"error": x.code, "message": x.message}, "pass": False})
    for case in fx["negative"]:
        try:
            r = d.resolve(case["clause"], case["element"])
            neg.append({**case, "got": r, "pass": False})
        except Err as x:
            neg.append({**case, "got": {"error": x.code, "message": x.message}, "pass": x.code == case["code"]})
    (c.R / "c2").mkdir(exist_ok=True)
    (c.R / "c2" / "locators.json").write_text(json.dumps({"positive": pos, "negative": neg}, indent=2) + "\n")
    kinds = {k for k in ("para", "Table", "Figure", "Note") if any(p["element"].startswith(k) for p in fx["positive"])}
    annex = any(p["clause"][:1].isalpha() for p in fx["positive"])
    p_ok, n_ok = all(x["pass"] for x in pos), all(x["pass"] for x in neg)
    return [res("C2.1", p_ok and len(kinds) == 4 and annex, f"{sum(x['pass'] for x in pos)}/{len(pos)} ISO locators -> exactly one expected element (kinds {sorted(kinds)}, annex {annex})",
                ["c2/locators.json", "task/expected/locators.json"]),
            ("C2.3-loc", n_ok, neg)]


def c2_lines(c: Ctx, expected: Path | None = None):
    d = c.doc("v1")
    fx = load_json(expected or c.task / "expected" / "lines.json")
    pos, neg = [], []
    for case in fx["positive"]:
        try:
            r = d.resolve_line(fx["file"], case["line"])
            pos.append({**case, "got": r, "pass": _match(d, r, case) and len(r["clause"].split(".")) == case["level"]})
        except Err as x:
            pos.append({**case, "got": {"error": x.code}, "pass": False})
    for case in fx["negative"]:
        try:
            r = d.resolve_line(fx["file"], case["line"])
            neg.append({**case, "got": r, "pass": False})
        except Err as x:
            neg.append({**case, "got": {"error": x.code, "message": x.message}, "pass": x.code == case["code"]})
    (c.R / "c2").mkdir(exist_ok=True)
    (c.R / "c2" / "lines.json").write_text(json.dumps({"positive": pos, "negative": neg}, indent=2) + "\n")
    levels = {p["level"] for p in pos if p["pass"]}
    ok = all(x["pass"] for x in pos) and len(pos) >= 10 and len(levels) >= 3
    return [res("C2.2", ok, f"{sum(x['pass'] for x in pos)}/{len(pos)} file:line -> element + clause; clause levels {sorted(levels)}",
                ["c2/lines.json", "task/expected/lines.json", "v1/srcmap.json"]),
            ("C2.3-line", all(x["pass"] for x in neg), neg)]


def c2_4(c: Ctx, expected: Path | None = None):
    v1 = c.doc("v1")
    m = load_json(c.R / "map" / "mapping.json")
    fx = load_json(expected or c.task / "expected" / "c24.json")
    mod_ids = {v1.resolve(*(loc.split(" ", 1) if " " in loc else (loc, "")))["id"] for loc in fx["modified"]}
    probs = []
    for e in m["elements"]:
        want = "modified" if e["v1_id"] in mod_ids else "unchanged"
        if e["status"] != want:
            probs.append(f"{e['tag']} {e['anchor'] or e['v1_id']} ({e['v1_clause']}): status {e['status']}, expected {want}")
        if e["status"] == "unchanged" and e["anchor"]:
            pass
    ins = [x for x in m["inserted"]]
    if sorted(x["anchor"] for x in ins if x["anchor"]) != sorted(fx["inserted_anchors"]) or len(ins) != fx["inserted_count"]:
        probs.append(f"inserted {[(x['tag'], x['anchor']) for x in ins]} != expected {fx['inserted_anchors']} (count {fx['inserted_count']})")
    got = {r["anchor"]: [r["old"], r["new"]] for r in m["renumbered"]}
    if got != fx["renumbered"]:
        probs.append(f"renumbered {got} != expected {fx['renumbered']}")
    # the insertion is BEFORE existing clauses (C2.4 wording)
    v2 = c.doc("v2")
    safety = v2.by_anchor.get("cl-safety")
    before = safety is not None and v2.number.get(safety.get("id")) == "5"
    if not before:
        probs.append("inserted clause is not numbered 5 (before the former clause 5)")
    edited = len(mod_ids)
    ok = not probs and edited >= fx["edited_element_count_min"]
    unchanged = sum(1 for e in m["elements"] if e["status"] == "unchanged")
    return res("C2.4", ok, f"{unchanged} unchanged + {edited} edited v1 elements mapped; {len(ins)} inserted; {len(got)} old->new pairs; problems {len(probs)}",
               ["map/mapping.json", "task/expected/c24.json"], {"problems": probs})


# ---------------------------------------------------------------- C3
def c3(c: Ctx, expected_invalid: Path | None = None, expected_ids: Path | None = None):
    out = []
    reg = c.register
    sheet = [r for r in reg if r["channel"] == "sheet"]
    reviewers = {r["reviewer"] for r in sheet}
    mbs = {r["mb"] for r in sheet}
    types = {r["type"] for r in sheet}
    fx_ids = load_json(expected_ids or c.task / "expected" / "register-ids.json")
    ids_ok = sorted(r["id"] for r in sheet) == sorted(fx_ids["sheet"]) and sorted(r["id"] for r in reg if r["channel"] == "pr") == sorted(fx_ids["pr"])
    one = (c.R / "intake" / "final" / "register.json").exists()
    ok = len(reviewers) >= 2 and len(mbs) >= 2 and len(sheet) >= 8 and types == set(TYPES) and ids_ok and one
    out.append(res("C3.1", ok, f"{len(sheet)} sheet comments, reviewers {sorted(reviewers)}, MB/NC {sorted(mbs)}, types {sorted(types)}; one register with {len(reg)} rows (sheet+pr); ids as frozen: {ids_ok}",
                   ["task/sheets/*.csv", "intake/final/register.{json,yaml,csv}"]))
    v1 = c.doc("v1")
    bad = [r["id"] for r in reg if not r["resolved_id"] or r["resolved_id"] not in v1.by_id or not r["locator"]]
    # re-resolve every sheet row independently from its original locator
    drift = []
    for r in sheet:
        try:
            if v1.resolve(r["clause"], r["element"])["id"] != r["resolved_id"]:
                drift.append(r["id"])
        except Err:
            drift.append(r["id"])
    out.append(res("C3.2", not bad and not drift and c.steps["intake_A_exit"] == 0,
                   f"{len(reg) - len(bad)}/{len(reg)} rows carry a resolved v1 element id beside the original locator; re-resolution drift {drift}",
                   ["intake/final/register.csv (locator, resolved_id)"]))
    A = (c.R / "intake" / "A" / "register.json").read_bytes()
    B = (c.R / "intake" / "B" / "register.json").read_bytes()
    rejB = load_json(c.R / "intake" / "B" / "rejects.json")
    fx = {k: v for k, v in load_json(expected_invalid or c.task / "expected" / "invalid-sheet.json").items() if not k.startswith("_")}
    got = {r["source"]: [_code(x) for x in r["reasons"]] for r in rejB}
    probs = []
    if set(got) != set(fx):
        probs.append(f"rejected rows {sorted(got)} != fixture rows {sorted(fx)}")
    for k, codes in fx.items():
        for code in codes:
            if code not in got.get(k, []):
                probs.append(f"{k}: expected reason {code}, got {got.get(k)}")
    no_seeded = not any("de-mallory" in r["source"] for r in load_json(c.R / "intake" / "B" / "register.json"))
    named = {"clause_not_found", "element_not_found", "bad_type", "missing_field:comment", "missing_field:mb", "duplicate_id"}
    covered = named <= {x for v in fx.values() for x in v}
    ok = c.steps["intake_B_exit"] != 0 and A == B and no_seeded and not probs and covered
    out.append(res("C3.3", ok, f"exit {c.steps['intake_B_exit']} (non-zero required); {len(rejB)} seeded rows rejected with per-row reasons; register A==B bytes: {A == B}; problems {len(probs)}",
                   ["intake/B/rejects.csv", "intake/A/register.json", "intake/B/register.json", "task/invalid/de-mallory.csv", "task/expected/invalid-sheet.json"], {"problems": probs}))
    ids = [r["id"] for r in reg]
    clash = [r for r in sheet if r["source_id"] == "GB-001"]
    hdr = {}
    for p in (c.task / "sheets").glob("*.csv"):
        meta = dict(l[1:].split(":", 1) for l in p.read_text().split("\n") if l.startswith("#"))
        hdr[p.name] = meta["reviewer"].strip()
    rev_ok = all(hdr[r["source"].split("/")[1].split(":")[0]] == r["reviewer"] for r in sheet)
    ok = len(ids) == len(set(ids)) and len({r["id"] for r in clash}) == len(clash) >= 2 and rev_ok and all(REGISTER_ID_RE.match(i) for i in ids)
    out.append(res("C3.4", ok, f"{len(ids)} ids, unique={len(ids) == len(set(ids))}; same-MB local-id clash GB-001 -> {sorted(r['id'] for r in clash)}; originating reviewer preserved={rev_ok}",
                   ["intake/final/register.csv (id, source_id, reviewer, source)"]))
    return out


# ---------------------------------------------------------------- C4
def c4(c: Ctx, expected_pr: Path | None = None):
    out = []
    g = c.git()
    reg = c.register
    pr = [r for r in reg if r["channel"] == "pr"]
    branches = load_json(c.task / "branches.json")["branches"]
    change = [b["name"] for b in branches if b.get("implements")]
    exist = all(g.ok("rev-parse", "--verify", f"refs/heads/{b['name']}") for b in branches)
    v1tag = g.ok("rev-parse", "--verify", "refs/tags/v1")
    by_rev = Counter(r["reviewer"] for r in pr)
    anchored = all(r["source_side"] in ("LEFT", "RIGHT") and r["source_line"] and r["source_branch"] in change for r in pr)
    ok = exist and v1tag and len(change) >= 1 and len(by_rev) >= 2 and anchored
    out.append(res("C4.1", ok, f"local repo with tag v1; change branch(es) {change}; PR reviewers {dict(by_rev)} each line-anchored to the branch diff",
                   ["repo/ (git)", "task/reviews/*/*.json", "pr/candidates.json"]))
    v1 = c.doc("v1")
    probs = []
    keys = set(reg[0].keys())
    for r in pr:
        if set(r.keys()) != keys:
            probs.append(f"{r['id']}: field set differs from sheet rows")
        if r["type"] not in TYPES or not r["comment"] or not r["mb"]:
            probs.append(f"{r['id']}: ISO fields incomplete")
        if not g.ok("cat-file", "-e", r["source_commit"] + "^{commit}"):
            probs.append(f"{r['id']}: source commit {r['source_commit']} not in repo")
        try:
            if v1.resolve_line(r["source_path"], int(r["v1_line"]))["id"] != r["resolved_id"]:
                probs.append(f"{r['id']}: re-resolution via C2.2 differs")
        except Err as x:
            probs.append(f"{r['id']}: {x.code}")
    rej = [x for x in load_json(c.R / "intake" / "final" / "rejects.json") if x["channel"] == "pr"]
    fx = {k: v for k, v in load_json(expected_pr or c.task / "expected" / "pr-rejects.json").items() if not k.startswith("_")}
    got = {x["source"]: [_code(y) for y in x["reasons"]] for x in rej}
    if set(got) != set(fx) or any(code not in got.get(k, []) for k, v in fx.items() for code in v):
        probs.append(f"PR rejects {got} != expected {fx}")
    in_reg = any(r["source_id"] in ("2",) and r["reviewer"] == "dave" for r in pr)
    if in_reg:
        probs.append("seeded PR negative entered the register")
    ok = not probs and c.steps["intake_final_exit"] != 0 and len(pr) >= 2
    out.append(res("C4.2", ok, f"{len(pr)} PR comments normalised into the register (channel pr, source commit+line, C2.2 anchor); {len(rej)} PR comments rejected like C3.3 (exit {c.steps['intake_final_exit']})",
                   ["intake/final/register.csv", "intake/final/rejects.csv", "task/expected/pr-rejects.json"], {"problems": probs}))
    # C4.3
    gates = [l.split("\t") for l in (c.R / "gate" / "gate.tsv").read_text().strip().split("\n")]
    gmap = {x[0]: dict(kv.split("=", 1) for kv in x[2:]) | {"sha": x[1]} for x in gates}
    probs = []
    for b in branches:
        gr = gmap.get(b["name"])
        anc = g.ok("merge-base", "--is-ancestor", b["name"], "main")
        if gr is None:
            probs.append(f"{b['name']}: no gate record")
            continue
        if b.get("seeded_broken"):
            if gr["verdict"] != "FAIL" or anc:
                probs.append(f"{b['name']}: seeded broken branch verdict={gr['verdict']} merged={anc}")
            if b.get("expect_exit") == "zero" and gr["exit"] != "0":
                probs.append(f"{b['name']}: designed to exit 0 but exited {gr['exit']}")
            if b.get("expect_exit") == "nonzero" and gr["exit"] == "0":
                probs.append(f"{b['name']}: designed to exit non-zero but exited 0")
        else:
            if gr["verdict"] != "PASS" or not anc:
                probs.append(f"{b['name']}: change branch verdict={gr['verdict']} merged={anc}")
    for mc in g("rev-list", "--merges", "v1..main").split():
        gt = trailers(g, mc, "Gate")
        p2 = g("rev-parse", f"{mc}^2").strip()
        if not gt or gt[0] != f"PASS {p2}" or gmap.get(next((k for k, v in gmap.items() if v["sha"] == p2), ""), {}).get("verdict") != "PASS":
            probs.append(f"merge {mc[:10]}: Gate trailer {gt} does not match a PASS gate record for its head {p2[:10]}")
    zero_exit_caught = [b["name"] for b in branches if b.get("seeded_broken") and gmap.get(b["name"], {}).get("exit") == "0" and gmap[b["name"]]["verdict"] == "FAIL"]
    weaker_rules_miss = {b["name"]: {"w0_rule": gmap[b["name"]]["w0_rule"], "exit_only_rule": gmap[b["name"]]["exit_only_rule"]}
                         for b in branches if b.get("seeded_broken") and b["name"] in gmap}
    ok = not probs and len(zero_exit_caught) >= 1
    out.append(res("C4.3", ok, f"gate verdicts {[(k, v['exit'], v['verdict']) for k, v in gmap.items()]}; broken branches that exit 0 yet FAIL: {zero_exit_caught}",
                   ["gate/gate.tsv", "gate/*.gate.json", "gate/*.compile.log", "git log"], {"problems": probs, "weaker_rules": weaker_rules_miss}))
    # C4.4 — git log alone
    log = g("log", "--merges", "--format=%H%x09%(trailers:key=Resolves,valueonly,separator=%x2C)", "main")
    pairs = {}
    for line in log.strip().split("\n"):
        if not line.strip():
            continue
        sha, _, ids = line.partition("\t")
        for i in [x for x in ids.split(",") if x]:
            pairs[i] = sha
    (c.R / "checks").mkdir(exist_ok=True)
    (c.R / "checks" / "c4.4-gitlog.tsv").write_text("".join(f"{k}\t{v}\n" for k, v in sorted(pairs.items())))
    disp = c.disp
    want = sorted(i for i, d in disp.items() if d.get("via_branch") and d["disposition"] != "reject")
    ok = sorted(pairs) == want and all(i in {r["id"] for r in reg} for i in pairs)
    out.append(res("C4.4", ok, f"git log --merges yields {len(pairs)} comment id -> merge commit pairs; expected PR-resolved ids {want}",
                   ["checks/c4.4-gitlog.tsv", "git log --merges --format=%(trailers:key=Resolves)"], {"pairs": pairs}))
    # C4.5
    remotes = g("remote", "-v").strip()
    rcfg = subprocess.run(["git", "-C", str(g.repo), "config", "--get-regexp", r"^remote\."], capture_output=True, text=True, env=g.env).stdout.strip()
    tr = trace_scan(c.R / "command-trace.log")
    ok = remotes == "" and rcfg == "" and g("config", "protocol.allow").strip() == "never" and not tr["forbidden"]
    out.append(res("C4.5", ok, f"git remote -v: {'(none)' if not remotes else remotes}; remote.* config: {'(none)' if not rcfg else rcfg}; forbidden commands in trace: {len(tr['forbidden'])}",
                   ["repo/.git/config", "command-trace.log"], tr))
    return out


NET_GIT = {"push", "fetch", "pull", "clone", "ls-remote", "submodule", "send-email", "request-pull"}
NET_TOOLS = {"curl", "wget", "gh", "commenter", "ssh", "scp", "rsync", "nc"}
NET_DOCKER = {"pull", "push", "login", "build", "buildx", "save", "export"}


def _git_subcommand(tokens):
    i = 1
    while i < len(tokens):
        t = tokens[i]
        if t in ("-C", "-c", "--git-dir", "--work-tree"):
            i += 2
            continue
        if t.startswith("-"):
            i += 1
            continue
        return t, tokens[i + 1:]
    return "", []


def trace_scan(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").split("\n") if path.exists() else []
    forbidden, docker_runs, bad_runs = [], 0, []
    for ln in lines:
        if not ln.strip():
            continue
        tok = ln.split()
        tool = tok[0]
        if tool in NET_TOOLS:
            forbidden.append(f"network/forge tool: {ln[:200]}")
        elif tool == "git":
            sub, rest = _git_subcommand(tok)
            if sub in NET_GIT or (sub == "remote" and rest[:1] and rest[0] in ("add", "set-url", "update")):
                forbidden.append(f"git network verb: {ln[:200]}")
        elif tool == "docker":
            sub = tok[1] if len(tok) > 1 else ""
            if sub in NET_DOCKER or (sub == "image" and len(tok) > 2 and tok[2] in ("pull", "push", "save")):
                forbidden.append(f"docker registry/build verb: {ln[:200]}")
            if sub == "run":
                docker_runs += 1
                if "--network none" not in ln:
                    bad_runs.append(f"docker run without --network none: {ln[:200]}")
                if MN_IMAGE not in tok:
                    bad_runs.append(f"docker run not using the pinned digest: {ln[:200]}")
    return {"trace_lines": len([l for l in lines if l.strip()]), "docker_runs": docker_runs, "forbidden": forbidden + bad_runs,
            "present": path.exists()}


# ---------------------------------------------------------------- C5
def attribution(g: Git, register: list[dict], disp: dict) -> list[str]:
    """C5.2 diff-attribution check, git history only (findings-W2 §4)."""
    probs = []
    reg = {r["id"]: r for r in register}
    seen = Counter()
    for sha in g("rev-list", "--reverse", "v1..v2").split():
        parents = g("rev-list", "--parents", "-n", "1", sha).split()[1:]
        if len(parents) > 1:
            cc = g("diff-tree", "--cc", "--no-commit-id", "-p", sha).strip()
            if cc:
                probs.append(f"merge {sha[:10]} introduces its own changes (evil merge)")
            continue
        ids = trailers(g, sha, "Comment-Id")
        if len(ids) != 1:
            probs.append(f"commit {sha[:10]} has {len(ids)} Comment-Id trailers (exactly 1 required)")
            continue
        cid = ids[0]
        seen[cid] += 1
        if cid not in reg:
            probs.append(f"commit {sha[:10]}: {cid} is not a register id")
            continue
        d = disp.get(cid)
        if d is None or d["disposition"] == "reject":
            probs.append(f"commit {sha[:10]}: {cid} is not an accept/modify")
            continue
        probs += commit_scope(g, sha, d)
    for i, d in disp.items():
        if d["disposition"] in ("accept", "modify") and seen[i] != 1:
            probs.append(f"{i}: appears in {seen[i]} commits (exactly 1 required)")
        if d["disposition"] == "reject" and seen[i]:
            probs.append(f"{i}: reject but changed the source")
    for line in g("log", "--format=%(trailers:key=Resolves,valueonly,separator=%x2C)", "v1..v2").split("\n"):
        for i in [x for x in line.split(",") if x]:
            if disp.get(i, {}).get("disposition") == "reject":
                probs.append(f"{i}: reject listed in a merge Resolves trailer")
    return probs


def commit_scope(g: Git, sha: str, d: dict) -> list[str]:
    """Re-apply the comment's recorded edits to the parent blob; the commit's blob must be exactly that, and no
    other file may change. Catches a stray edit smuggled into an attributed commit."""
    probs = []
    changed = [x for x in g("diff-tree", "--no-commit-id", "--name-only", "-r", sha).split("\n") if x]
    files = sorted({e["file"] for e in d["edits"]})
    if sorted(changed) != files:
        probs.append(f"commit {sha[:10]} ({d['id']}) changes {changed}, edits declare {files}")
    for f in files:
        before = g("show", f"{sha}^:{f}")
        after = g("show", f"{sha}:{f}")
        exp = apply_edits_text(before, d["edits"], f)
        if exp is None or exp != after:
            probs.append(f"commit {sha[:10]} ({d['id']}): {f} differs from parent + recorded edits (stray or missing change)")
    return probs


def c5(c: Ctx):
    out = []
    disp = c.disp
    reg = c.register
    v = load_json(c.R / "dispositions" / "validation.json")
    vb = load_json(c.R / "dispositions" / "validation-bad.json")
    want = load_json(c.task / "expected" / "invalid-dispositions.json")["codes"]
    got = {_code(e).rstrip(":") for e in vb["errors"]}
    kinds = Counter(d["disposition"] for d in disp.values())
    chans = Counter(r["channel"] for r in reg)
    ok = v["valid"] and c.steps["dispositions_exit"] == 0 and c.steps["dispositions_bad_exit"] != 0 and set(want) <= got \
        and all(kinds[k] >= 1 for k in ("accept", "modify", "reject")) and len(disp) == len(reg)
    out.append(res("C5.1", ok, f"{len(disp)} dispositions for {len(reg)} register comments; {dict(kinds)}; channels {dict(chans)}; seeded bad record rejected with {sorted(got & set(want))}",
                   ["task/dispositions.json", "dispositions/validation.json", "dispositions/validation-bad.json"]))
    g = c.git()
    probs = attribution(g, reg, disp)
    out.append(res("C5.2", not probs, f"every commit in v1..v2 carries exactly one accept/modify Comment-Id and equals parent + recorded edits; rejects change nothing; merges clean; problems {len(probs)}",
                   ["git log v1..v2", "task/dispositions.json"], {"problems": probs}))
    out.append(c5_3(c))
    tr = list(csv.DictReader(io.StringIO((c.R / "trace" / "trace.csv").read_text())))
    probs = []
    if sorted(r["id"] for r in tr) != sorted(r["id"] for r in reg):
        probs.append("trace ids != register ids")
    for r in tr:
        for k, v in r.items():
            if v == "" and not (r["disposition"] == "reject" and k.startswith("v2_") or (r["disposition"] == "reject" and k == "renumbered")):
                probs.append(f"{r['id']}: blank {k}")
            if "ERROR" in v:
                probs.append(f"{r['id']}: {k}={v}")
    out.append(res("C5.4", not probs, f"{len(tr)} trace rows (one per comment); blank cells outside reject v2 columns: {len(probs)}",
                   ["trace/trace.csv", "trace/trace.yaml"], {"problems": probs}))
    return out


def c5_3(c: Ctx):
    """C5.3, RECOMPUTED by the checker (rework 1, mnstd-002 gate §4.1). The checker does not trust
    trace/containment.json: it re-derives containment itself from
      - the expected text, taken from the register (accept: proposed_change) or the frozen task dispositions
        (modify: modified_text), and required to equal the frozen expect_in_v2;
      - the C2.4 mapping (map/mapping.json), whose v1->v2 pairs must agree in tag and anchor and whose v2 ids
        must exist in the v2 semantic XML;
      - the v2 SEMANTIC XML itself (v2/draft.xml), parsed here directly with ElementTree (not resolver.Doc and
        not trace.build, so a defect in the pipeline's containment code is not shared by the checker).
    It FAILS on any accept/modify whose expected text is absent from its mapped v2 element(s), and FAILS if the
    pipeline's recorded containment.json disagrees with the recomputation (a tampered record is also caught)."""
    disp = c.disp
    reg = {r["id"]: r for r in c.register}
    mp = load_json(c.R / "map" / "mapping.json")
    m1 = {e["v1_id"]: e for e in mp["elements"]}
    inserted = {x["v2_id"] for x in mp["inserted"]}
    root = ET.parse(c.R / "v2" / "draft.xml").getroot()
    by_id = {e.get("id"): e for e in root.iter() if e.get("id")}
    outs = {x: (c.R / "v2" / f"draft.{x}").exists() for x in ("html", "pdf", "xml")}
    rows, probs = [], []
    for i in sorted(disp):
        d = disp[i]
        k = d["disposition"]
        if k == "reject":
            continue
        r = reg.get(i)
        if r is None:
            probs.append(f"{i}: not in register")
            continue
        src = r["proposed_change"] if k == "accept" else d.get("modified_text", "")
        want = norm(src, strip_markup=True)
        if not want or want != norm(d.get("expect_in_v2", ""), strip_markup=True):
            probs.append(f"{i}: expected text ({k}) != frozen expect_in_v2")
        mode = d.get("containment", "element")
        if mode == "insert":
            els = [by_id[x] for x in inserted if x in by_id]
            if len(els) != len(inserted):
                probs.append(f"{i}: mapped inserted v2 id(s) absent from v2 XML")
            hit = any(want in norm(text_of(e)) for e in els)
            v2ids = sorted(x for x in inserted if x in by_id and want in norm(text_of(by_id[x])))
        else:
            v1ids = [r["resolved_id"]] + ([r["resolved_to_id"]] if mode == "range" and r.get("resolved_to_id") else [])
            v2ids, hit = [], False
            for v1 in v1ids:
                e = m1.get(v1)
                if e is None or not e.get("v2_id"):
                    probs.append(f"{i}: v1 element {v1} has no v2 counterpart in the C2.4 mapping")
                    continue
                v2e = by_id.get(e["v2_id"])
                if v2e is None:
                    probs.append(f"{i}: mapped v2 id {e['v2_id']} absent from v2 XML")
                    continue
                if local(v2e.tag) != e["tag"] or (e["anchor"] and v2e.get("anchor") != e["anchor"]):
                    probs.append(f"{i}: mapped v2 element {e['v2_id']} is <{local(v2e.tag)} anchor={v2e.get('anchor')}>, mapping says <{e['tag']} anchor={e['anchor']}>")
                v2ids.append(e["v2_id"])
            if len(v2ids) == len(v1ids):
                hit = want in " ".join(norm(text_of(by_id[x])) for x in v2ids)
        rows.append({"id": i, "mode": mode, "expect": want, "v2_ids": v2ids, "pass": bool(hit)})
        if not hit:
            probs.append(f"{i}: '{want[:60]}' not contained in v2 XML element(s) {v2ids}")
    rec = {x["id"]: x["pass"] for x in load_json(c.R / "trace" / "containment.json")}
    for x in rows:
        if rec.get(x["id"]) is not x["pass"]:
            probs.append(f"{x['id']}: recorded containment.json pass={rec.get(x['id'])} disagrees with recomputed {x['pass']}")
    for i, v in rec.items():
        if v is not None and i not in {x["id"] for x in rows}:
            probs.append(f"{i}: containment recorded for a non-accept/modify id")
    n_pass = sum(x["pass"] for x in rows)
    ok = c.steps["v2_compile_exit"] == 0 and all(outs.values()) and not probs and len(rows) >= 1
    return res("C5.3", ok, f"v2 exit {c.steps['v2_compile_exit']}, outputs {outs}; containment RECOMPUTED from v2/draft.xml via C2.4 mapping: {n_pass}/{len(rows)} pass; problems {len(probs)}",
               ["v2/compile.log", "v2/draft.xml", "map/mapping.json", "intake/final/register.json", "task/dispositions.json",
                "trace/containment.json (cross-checked, not trusted)"],
               {"problems": probs, "recomputed": rows})


# ---------------------------------------------------------------- C6
def c6(c: Ctx):
    out = []
    reg = sorted(c.register, key=lambda r: r["id"])
    A = load_json(c.R / "review" / "annotations.json")
    plan = load_json(c.R / "review" / "projection-plan.json")
    sem = [a for a in A["semantic"] if a["reviewer"] != "Metanorma"]
    pdf = A["pdf"]
    glue = (c.R / "review" / "build" / "draft.review-glue.html").read_text(encoding="utf-8")
    native_html = (c.R / "review" / "build" / "draft.html").read_text(encoding="utf-8")
    H = re.findall(r'<aside class="mn-review-glue"[^>]*data-comment-id="([^"]+)"', glue)
    rv = Doc(c.R / "review" / "build")
    v1 = c.doc("v1")
    probs = []
    pmap = {b["id"]: b for b in plan["blocks"]}
    for r in reg:
        s = [a for a in sem if a["text"].startswith(f"[{r['id']}]")]
        p = [a for a in pdf if a["Contents"].startswith(f"[{r['id']}]")]
        if len(s) != 1 or len(p) != 1 or H.count(r["id"]) != 1:
            probs.append(f"{r['id']}: semantic {len(s)} / pdf {len(p)} / html {H.count(r['id'])}")
            continue
        s, p = s[0], p[0]
        for what, ok in (("reviewer", s["reviewer"] == f"{r['reviewer']} ({r['mb']})" and p["T"] == s["reviewer"]),
                         ("date", (s["date"] or "").startswith(r["date"])),
                         ("comment text", r["comment"] in s["text"] and r["comment"] in p["Contents"]),
                         ("type/MB", f"type {r['type']}" in p["Contents"] and f"MB/NC {r['mb']}" in p["Contents"])):
            if not ok:
                probs.append(f"{r['id']}: {what} not visible")
        # attached at the resolved element
        frm = s["from"]
        tgt = rv.by_anchor.get(frm)
        v1e = v1.by_id[r["resolved_id"]]
        if tgt is None:
            probs.append(f"{r['id']}: from={frm} not found in review XML")
        else:
            x = tgt
            while x is not None and not rv._is_tracked(x) and local(x.tag) not in ("li",):
                x = rv.parent.get(x)
            same = (v1e.get("anchor") and (x.get("anchor") == v1e.get("anchor") or tgt.get("anchor") == v1e.get("anchor"))) or \
                   (x is not None and norm(text_of(x)) == norm(text_of(v1e)))
            if not same:
                probs.append(f"{r['id']}: from={frm} lands on {local(x.tag) if x is not None else None}, not the resolved element")
        if r.get("resolved_to_id"):
            if s["to"] == s["from"] or s["to"] != pmap[r["id"]]["to"]:
                probs.append(f"{r['id']}: range to={s['to']} not projected")
    ranged = [r["id"] for r in reg if r.get("resolved_to_id")]
    ok = not probs and c.steps["review_compile_exit"] == 0 and bool(ranged)
    native_n = len(re.findall(r"\[(?:GB|FR|PR)-[A-Z]{2}", native_html))
    out.append(res("C6.1", ok, f"PDF: {len(pdf)} native sticky-note annotations; HTML: {len(H)} glue asides from native semantic <annotation> (ruling R2; native ISO HTML shows {native_n}); ranged {ranged}; problems {len(probs)}",
                   ["review/build/draft.pdf", "review/build/draft.review-glue.html", "review/build/draft.xml", "review/annotations.json"], {"problems": probs}))
    Rn, X, P, Hn = len(reg), len(sem), len(pdf), len(H)
    each = all(sum(1 for a in sem if a["text"].startswith(f"[{r['id']}]")) == 1 for r in reg)
    out.append(res("C6.2", Rn == X == P == Hn and each, f"register R={Rn}, semantic XML annotation elements X={X}, PDF /Text annots P={P}, HTML H={Hn}; each id exactly once: {each}",
                   ["review/annotations.json (count script: checks.c6)"]))
    src = (POC / "src" / "draft.adoc").read_text(encoding="utf-8")
    hand = len(re.findall(r"^\[reviewer=", src, re.M)) + len(re.findall(r"^\*{4}$", src, re.M)) + len(re.findall(r"^TODO:|^\[TODO\]", src, re.M))
    clean = load_json(c.R / "review" / "clean-annotations.json")
    clean_html = len(re.findall(r'class="mn-review-glue"', (c.R / "v1" / "draft.html").read_text(encoding="utf-8")))
    derived = (c.R / "review" / "input" / "draft.adoc").read_text(encoding="utf-8")
    stripped = derived.replace(":presentation-metadata-render-document-annotations: true\n", "", 1)
    stripped = re.sub(r"\n\n\[reviewer=[^\n]*\]\n\*{4}\n.*?\n\*{4}", "", stripped, flags=re.S)
    stripped = re.sub(r"^\[\[rv-e\d+\]\]\n", "", stripped, flags=re.M)
    stripped = re.sub(r"\[\[rv-e\d+\]\]", "", stripped)
    only_projection = stripped == src
    ok = hand == 0 and len(clean["semantic"]) == 0 and len(clean["pdf"]) == 0 and clean_html == 0 and only_projection
    out.append(res("C6.3", ok, f"hand-written review blocks in committed v1 source: {hand}; clean v1 build X={len(clean['semantic'])} P={len(clean['pdf'])} H={clean_html}; derived input = v1 + projection only: {only_projection}",
                   ["poc/src/draft.adoc", "review/input/draft.adoc", "review/clean-annotations.json"]))
    rsem = rv.sem
    stage = rsem.findtext(f"{N}bibdata/{N}status/{N}stage")
    pres = ET.parse(c.R / "review" / "build" / "draft.presentation.xml").getroot()
    flag = [e.text for e in pres.iter(N + "render-document-annotations")]
    bodies = len(list(pres.iter(N + "fmt-annotation-body")))
    ok = stage == "30" and flag == ["true"] and P == Rn
    out.append(res("C6.4", ok, f"mechanism: stage {stage} (CD, unpublished) + :presentation-metadata-render-document-annotations: true in the DERIVED input only; presentation render flag {flag}; fmt-annotation-body {bodies}; native HTML renders none (glue per R2)",
                   ["review/build/draft.presentation.xml", "review/input/draft.adoc"], {"native_html_annotations": native_n}))
    return out


# ---------------------------------------------------------------- C7
class _Rows(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.cur, self.cell, self.tbl, self.heads = [], None, None, None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "table":
            self.tbl = a.get("id")
        if tag == "tr" and self.tbl == "comments" and "data-id" in a:
            self.cur = {"_attrs": a, "_cells": []}
        if tag == "td" and self.cur is not None:
            self.cell = []
        if tag == "th" and self.tbl == "comments":
            self.cell = []
        if tag == "a" and self.cur is not None and "href" in a:
            self.cur["_href"] = a["href"]

    def handle_endtag(self, tag):
        if tag == "td" and self.cur is not None and self.cell is not None:
            self.cur["_cells"].append("".join(self.cell))
            self.cell = None
        if tag == "th" and self.tbl == "comments" and self.cell is not None and self.cur is None:
            self.heads.append("".join(self.cell))
            self.cell = None
        if tag == "tr" and self.cur is not None:
            self.rows.append(self.cur)
            self.cur = None

    def handle_data(self, d):
        if self.cell is not None:
            self.cell.append(d)


def _report_yaml_rows(p: Path):
    rows, cur = [], None
    for line in p.read_text(encoding="utf-8").split("\n"):
        m = re.match(r"^  - id: (.*)$", line)
        if m:
            cur = {"id": json.loads(m.group(1))}
            rows.append(cur)
            continue
        m = re.match(r"^    ([a-z_]+): (.*)$", line)
        if m and cur is not None and not line.startswith("    - "):
            cur[m.group(1)] = json.loads(m.group(2))
        if line.startswith("counts_type_disposition_mb"):
            cur = None
    return rows


def c7(c: Ctx):
    out = []
    reg = {r["id"]: r for r in load_json(c.R / "trace" / "register.resolved.json")}
    base = {r["id"] for r in c.register}
    rows = list(csv.DictReader(io.StringIO((c.R / "report" / "report.csv").read_text(encoding="utf-8"))))
    hdr = (c.R / "report" / "report.csv").read_text(encoding="utf-8").split("\n")[0].split(",")
    want_hdr = ["Comment id"] + [h for _, h in ISO_COLUMNS] + ["Disposition", "v2 location"]
    ids = [r["Comment id"] for r in rows]
    probs = []
    if hdr != want_hdr:
        probs.append(f"column order {hdr} != {want_hdr}")
    if sorted(ids) != sorted(base) or len(ids) != len(set(ids)):
        probs.append("report ids != register ids exactly once")
    for r in rows:
        rr = reg[r["Comment id"]]
        for k, h in ISO_COLUMNS:
            if r[h] != rr[k]:
                probs.append(f"{rr['id']}: {h} differs from register")
    p = subprocess.run([sys.executable, str(POC / "tools" / "report.py"), str(c.R / "trace" / "register.resolved.json"),
                        str(c.R / "checks" / "report-regen"), "../v2/draft.html"], capture_output=True, text=True)
    regen = all((c.R / "checks" / "report-regen" / f).read_bytes() == (c.R / "report" / f).read_bytes()
                for f in ("report.html", "report.yaml", "report.csv")) if p.returncode == 0 else False
    if not regen:
        probs.append("report is not byte-identical to a regeneration from the register (hand edit?)")
    out.append(res("C7.1", not probs, f"{len(rows)} rows, each register comment once, ISO 2012-03 column order + Disposition + v2 location; regenerated-from-register identical: {regen}",
                   ["report/report.{html,csv,yaml}", "trace/register.resolved.json"], {"problems": probs}))
    key = lambda t, d, m: (t, d, m)  # noqa: E731
    c_reg = Counter(key(r["type"], r["disposition"], r["mb"]) for r in reg.values())
    c_csv = Counter(key(r["Type of comment"], r["Disposition"], r["MB/NC"]) for r in rows)
    yrows = _report_yaml_rows(c.R / "report" / "report.yaml")
    c_yaml = Counter(key(r["type"], r["disposition"], r["mb"]) for r in yrows)
    hp = _Rows()
    hp.feed((c.R / "report" / "report.html").read_text(encoding="utf-8"))
    c_html = Counter(key(x["_attrs"]["data-type"], x["_attrs"]["data-disposition"], x["_attrs"]["data-mb"]) for x in hp.rows)
    c_html_cells = Counter(key(x["_cells"][5], x["_cells"][9], x["_cells"][1]) for x in hp.rows)
    summ = {}
    for m in re.finditer(r'data-key="([^"]+)"><td>[^<]*</td><td>[^<]*</td><td>[^<]*</td><td>(\d+)</td>', (c.R / "report" / "report.html").read_text()):
        summ[tuple(m.group(1).split("|"))] = int(m.group(2))
    ok = c_reg == c_csv == c_yaml == c_html == c_html_cells == Counter(summ) and sum(c_reg.values()) == len(base)
    out.append(res("C7.2", ok, f"HTML + YAML + CSV emitted; type x disposition x MB counts equal across register/CSV/YAML/HTML rows/HTML summary: {ok} ({len(c_reg)} cells, total {sum(c_reg.values())})",
                   ["report/report.html", "report/report.yaml", "report/report.csv"], {"register_counts": {"|".join(k): v for k, v in sorted(c_reg.items())}}))
    v2 = c.doc("v2")
    v2html = (c.R / "v2" / "draft.html").read_text(encoding="utf-8")
    hids = set(re.findall(r'\bid="([^"]+)"', v2html))
    probs = []
    for x in hp.rows:
        cid = x["_attrs"]["data-id"]
        r = reg[cid]
        if r["disposition"] == "reject":
            continue
        href = x.get("_href", "")
        frag = href.split("#", 1)[1] if "#" in href else ""
        if not frag or frag != r["v2_location"]:
            probs.append(f"{cid}: no link to v2 location")
            continue
        if frag not in v2.by_anchor and frag not in v2.by_id:
            probs.append(f"{cid}: {frag} not in v2 semantic XML")
        if frag not in hids:
            probs.append(f"{cid}: #{frag} not an id in v2/draft.html")
    n = sum(1 for r in reg.values() if r["disposition"] != "reject")
    out.append(res("C7.3", not probs, f"{n - len(probs)}/{n} accept/modify rows link to a v2 location that exists in the v2 semantic XML and v2 HTML",
                   ["report/report.html", "v2/draft.xml", "v2/draft.html"], {"problems": probs}))
    return out


# ---------------------------------------------------------------- run-local NFRs
def nfr_local(c: Ctx):
    out = []
    tr = trace_scan(c.R / "command-trace.log")
    img = [l for l in (c.R / "command-trace.log").read_text().split("\n") if l.startswith("docker run")] if tr["present"] else []
    env = load_json(c.R / "envelope.json") if (c.R / "envelope.json").exists() else {}
    ok = tr["present"] and tr["docker_runs"] > 0 and all(MN_IMAGE in l for l in img) and env.get("image_digest_ok") is True
    out.append(res("N2.1", ok, f"{tr['docker_runs']} container runs, all on {MN_IMAGE.split('@')[1][:19]}… (digest verified in envelope: {env.get('image_digest_ok')})",
                   ["command-trace.log", "envelope.json"]))
    wr = env.get("which_ruby", {})
    out.append(res("N2.2", wr.get("exit") not in (0, None), f"`which ruby` exit {wr.get('exit')} output {wr.get('out')!r}", ["envelope.json"]))
    stdlib = set(sys.stdlib_module_names)
    own = {p.stem for p in (POC / "tools").glob("*.py")}
    bad = []
    for p in sorted((POC / "tools").glob("*.py")):
        for m in re.finditer(r"^\s*(?:from|import)\s+([A-Za-z_][\w]*)", p.read_text(), re.M):
            if m.group(1) not in stdlib and m.group(1) not in own and m.group(1) != "__future__":
                bad.append(f"{p.name}: {m.group(1)}")
    node = list(POC.rglob("package.json"))
    out.append(res("N2.3", not bad and not node, f"host glue: Python {env.get('python', '?')} stdlib only (third-party imports: {bad or 'none'}); Node not used; Ruby only in-container (srcmap.rb)",
                   ["poc/tools/*.py", "poc/REQUIREMENTS.txt"]))
    reg = c.register
    rows = list(csv.DictReader(io.StringIO((c.R / "report" / "report.csv").read_text(encoding="utf-8"))))
    pr = load_json(c.R / "pr" / "candidates.json")
    probs = []
    for r in reg:
        if not all(k in r for k in ISO_KEYS):
            probs.append(f"register {r['id']} lacks ISO fields")
    if not all(h in rows[0] for _, h in ISO_COLUMNS):
        probs.append("report lacks ISO columns")
    pr_iso = {"mb", "line(v1_line)", "clause(resolved)", "element(resolved)", "type", "comment", "proposed_change", "observations"}
    for x in pr:
        for k in ("mb", "type", "comment", "proposed_change", "observations", "v1_line"):
            if k not in x:
                probs.append(f"PR record {x['review_file']}#{x['local_id']} lacks {k}")
    out.append(res("N4.1", not probs, "register, PR records and report carry all 8 ISO 2012-03 fields (documented mapping in RESULT.md §N4)",
                   ["intake/final/register.csv", "pr/candidates.json", "report/report.csv"], {"problems": probs, "pr_mapping": sorted(pr_iso)}))
    types = {r["type"] for r in reg} | {r["Type of comment"] for r in rows}
    multi = [r["id"] for r in reg if "\n" in r["comment"]]
    out.append(res("N4.2", types <= set(TYPES) and not multi, f"type vocabulary {sorted(types)}; one comment per row (multi-line comments: {multi or 'none'})",
                   ["intake/final/register.csv", "report/report.csv"]))
    out.append(res("N4.3", True, "N/A: DOCX output not selected (Q1 default: HTML + YAML/CSV)", [], result="N/A"))
    out.append(n5_1(c))
    out.append(n5_2(c.R, {r["id"] for r in reg}))
    ok = not tr["forbidden"] and tr["present"]
    out.append(res("N6.1", ok, f"gated run: {tr['trace_lines']} external commands traced; forbidden/network verbs: {len(tr['forbidden'])}; every container run --network none. NOTE: font cache was provisioned by a separate networked `make fonts` (ruling R1) — the validator rules N6.1's literal text",
                   ["command-trace.log"], tr))
    hits = [l for l in (c.R / "command-trace.log").read_text().split("\n") if re.search(r"\bcommenter\b|github-", l)] if tr["present"] else ["no trace"]
    out.append(res("N6.2", not hits and c.git()("remote", "-v").strip() == "", f"commenter/github-* invocations in trace: {len(hits)}; inner repo remotes: none",
                   ["command-trace.log", "repo/.git/config"]))
    return out


def n5_1(c: Ctx):
    """Follow locator -> v1 element -> disposition -> commit -> v2 element -> report row for EVERY comment (100% >= 50%)."""
    g = c.git()
    reg = c.register
    v1, v2 = c.doc("v1"), c.doc("v2")
    disp = c.disp
    tr = {r["id"]: r for r in csv.DictReader(io.StringIO((c.R / "trace" / "trace.csv").read_text()))}
    rep = {r["Comment id"]: r for r in csv.DictReader(io.StringIO((c.R / "report" / "report.csv").read_text()))}
    mp = {e["v1_id"]: e for e in load_json(c.R / "map" / "mapping.json")["elements"]}
    log = {}
    for sha in g("rev-list", "v1..v2").split():
        for i in trailers(g, sha, "Comment-Id"):
            log.setdefault(i, []).append(sha)
    probs, walked = [], []
    for r in reg:
        try:
            e = v1.resolve_line(r["source_path"], int(r["v1_line"])) if r["channel"] == "pr" else v1.resolve(r["clause"], r["element"])
        except Err as x:
            probs.append(f"{r['id']}: locator no longer resolves ({x.code})")
            continue
        if e["id"] != r["resolved_id"] or tr[r["id"]]["v1_element_id"] != e["id"]:
            probs.append(f"{r['id']}: v1 element mismatch")
        d = disp[r["id"]]["disposition"]
        if tr[r["id"]]["disposition"] != d or rep[r["id"]]["Disposition"] != d:
            probs.append(f"{r['id']}: disposition mismatch")
        if d != "reject":
            cm = log.get(r["id"], [])
            if len(cm) != 1 or tr[r["id"]]["commit"] != cm[0]:
                probs.append(f"{r['id']}: commit not recoverable from git log")
            want_v2 = tr[r["id"]]["v2_element_id"]
            if disp[r["id"]].get("containment") != "insert" and mp.get(e["id"], {}).get("v2_id") != want_v2:
                probs.append(f"{r['id']}: v2 element not the C2.4 counterpart")
            if want_v2 not in v2.by_id:
                probs.append(f"{r['id']}: v2 element missing")
            if rep[r["id"]]["v2 location"].split("#")[-1] not in (tr[r["id"]]["v2_anchor"] or "", want_v2):
                probs.append(f"{r['id']}: report v2 location mismatch")
        walked.append(r["id"])
    pr_all = all(r["id"] in walked for r in reg if r["channel"] == "pr")
    return res("N5.1", not probs and pr_all and len(walked) * 2 >= len(reg),
               f"walked {len(walked)}/{len(reg)} comments (100%, incl. every PR comment) locator->v1->disposition->commit->v2->report using emitted files + git log; breaks {len(probs)}",
               ["intake/final/register.json", "trace/trace.csv", "map/mapping.json", "report/report.csv", "git log"], {"problems": probs})


# Outputs of DECLARED seeded-negative fixtures: they exist to name ids that are not in the register.
SEEDED_NEGATIVE_OUTPUTS = {"dispositions/validation-bad.json"}


def n5_2(R: Path, ids: set):
    stray = {}
    for p in sorted(R.rglob("*")):
        rel = str(p.relative_to(R))
        if p.is_dir() or ".git" in p.parts or p.suffix in (".pdf", ".png") or rel.startswith("selftest") \
                or rel in SEEDED_NEGATIVE_OUTPUTS:
            continue
        try:
            t = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in ANY_REGISTER_ID_RE.findall(t):
            if m not in ids:
                stray.setdefault(m, []).append(str(p.relative_to(R)))
    return res("N5.2", not stray, f"register-id-shaped tokens absent from the register, across all text artefacts: {len(stray)}",
               ["run dir (all text files)"], {"stray": {k: sorted(set(v))[:5] for k, v in stray.items()}})


def run_all(R: Path):
    c = Ctx(R)
    out = []
    out += [c1_1(c), c1_2(c), c1_3(c)]
    loc = c2_locators(c)
    lin = c2_lines(c)
    out += [loc[0], lin[0]]
    neg = loc[1][2] + lin[1][2]
    out.append(res("C2.3", loc[1][1] and lin[1][1], f"{sum(x['pass'] for x in neg)}/{len(neg)} non-existent/ambiguous locators and lines rejected with the expected reason (no nearest match)",
                   ["c2/locators.json", "c2/lines.json"]))
    out.append(c2_4(c))
    out += c3(c)
    out += c4(c)
    out += c5(c)
    out += c6(c)
    out += c7(c)
    out += nfr_local(c)
    order = ["C1.1", "C1.2", "C1.3", "C2.1", "C2.2", "C2.3", "C2.4"]
    out.sort(key=lambda x: (x["clause"][0], order.index(x["clause"]) if x["clause"] in order else 99, x["clause"]))
    return out
