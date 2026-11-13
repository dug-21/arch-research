"""One end-to-end run of the mnstd-002 prototype into a run directory (called twice by `make demo`).

Stage order (SCOPE "Expected output" 2): v1 compile -> resolver fixture -> intake + seeded-invalid fixture ->
PR-channel simulation in a local git repo -> dispositions -> scripted edits -> v2 compile -> C2.4 map -> trace ->
annotated v1 review build (+ the clean v1 build) -> disposition report -> clause checks.
Usage: pipeline.py <run-dir>
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
from common import POC, die, dump_json, load_json, mn_compile, srcmap  # noqa: E402
import intake  # noqa: E402
import dispose  # noqa: E402
import prsim  # noqa: E402
import review  # noqa: E402
import trace as tracemod  # noqa: E402
from gitx import Git, apply_edits  # noqa: E402
from resolver import Doc, map_versions  # noqa: E402

TASK = POC.parent / "task"


def log(msg):
    print(f"[pipeline] {msg}", flush=True)


def compile_dir(src_files_dir: Path, dest: Path, exts="xml,html,pdf,rxl") -> int:
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True)
    for f in sorted(src_files_dir.iterdir()):
        if f.is_file() and f.suffix in (".adoc", ".png"):
            shutil.copy(f, dest / f.name)
    rc = mn_compile(dest, "draft.adoc", exts, dest / "compile.log")
    shutil.rmtree(dest / "relaton", ignore_errors=True)
    return rc


def main(argv):
    R = Path(argv[0]).resolve()
    R.mkdir(parents=True, exist_ok=True)
    leftovers = [x.name for x in R.iterdir() if x.name not in ("command-trace.log",)]
    if leftovers:
        die(f"run dir {R} is not clean ({leftovers[:5]}); `make clean` first (N1.2: runs start from a clean state)")
    steps = {}
    import envelope
    log("envelope: capturing the effective configuration in force")
    dump_json(envelope.capture(), R / "envelope.json")

    # ---- C1: v1 compile (this is also the CLEAN v1 build for C6.3) ----
    log("C1 compile v1 (xml,html,pdf,rxl; --network none)")
    steps["v1_compile_exit"] = compile_dir(POC / "src", R / "v1")
    srcmap(R / "v1", "draft.adoc", R / "v1" / "srcmap.json")
    v1 = Doc(R / "v1")

    # ---- intake: A (valid sheets only) and B (valid + seeded invalid) ----
    sheets = [str(p) for p in sorted((TASK / "sheets").glob("*.csv"))]
    invalid = [str(p) for p in sorted((TASK / "invalid").glob("*.csv"))]
    log("C3 intake A (valid sheets)")
    steps["intake_A_exit"] = intake.main(["--v1", str(R / "v1"), "--sheets", *sheets, "--out", str(R / "intake" / "A")])
    log("C3 intake B (valid + seeded-invalid sheet; must exit non-zero)")
    steps["intake_B_exit"] = intake.main(["--v1", str(R / "v1"), "--sheets", *sheets, *invalid, "--out", str(R / "intake" / "B")])

    # ---- C4: local repo, branches ----
    disp = load_json(TASK / "dispositions.json")["dispositions"]
    dmap = {d["id"]: d for d in disp}
    log("C4 local git repo (no remote), v1 tag, change branches")
    g = prsim.setup(R / "repo", POC / "src")
    branches = load_json(TASK / "branches.json")["branches"]
    for b in branches:
        if b.get("implements"):
            commits = [{"id": i, "message": f"Resolve {i} ({dmap[i]['disposition']}): proposal", "edits": dmap[i]["edits"],
                        "who": b.get("author", prsim.SECRETARIAT)} for i in sorted(b["implements"])]
        else:
            commits = [{"message": f"Seeded broken source (fixture): {b['seeded_broken']}", "edits": b["edits"],
                        "who": ["Fixture", "fixture@example.invalid"]}]
        prsim.create_branch(g, b["name"], commits)
    log("C4 normalise PR review records")
    prsim.normalize(g, TASK / "reviews", R / "pr" / "candidates.json")
    log("C3/C4 final intake: sheets + PR candidates -> ONE register")
    steps["intake_final_exit"] = intake.main(["--v1", str(R / "v1"), "--sheets", *sheets,
                                              "--pr-candidates", str(R / "pr" / "candidates.json"),
                                              "--out", str(R / "intake" / "final")])
    register = load_json(R / "intake" / "final" / "register.json")

    # ---- C5.1 dispositions ----
    log("C5.1 validate dispositions (+ seeded bad record)")
    steps["dispositions_exit"] = dispose.main(["--register", str(R / "intake" / "final" / "register.json"),
                                               "--dispositions", str(TASK / "dispositions.json"),
                                               "--out", str(R / "dispositions" / "validation.json")])
    steps["dispositions_bad_exit"] = dispose.main(["--register", str(R / "intake" / "final" / "register.json"),
                                                   "--dispositions", str(TASK / "invalid" / "dispositions-bad.json"),
                                                   "--out", str(R / "dispositions" / "validation-bad.json")])
    if steps["dispositions_exit"] != 0:
        die("dispositions invalid; stopping before any edit is applied", 1)

    # ---- C4.3/C4.4 gate + merge; C5.2 scripted edits ----
    gd = R / "gate"
    gd.mkdir()
    log("C4.3 gate baseline on main@v1")
    baseline = prsim.gate(g, "main", gd, None)
    reg_ids = {r["id"]: r for r in register}
    merges = {}
    for b in branches:
        if b.get("implements"):
            pr_ids = sorted(i for i, r in reg_ids.items() if r["channel"] == "pr" and r["source_branch"] == b["name"]
                            and dmap[i]["disposition"] != "reject")
            for i in pr_ids:
                log(f"C5.2 apply {i} on {b['name']}")
                prsim.add_commit_on(g, b["name"], i, dmap[i]["disposition"], dmap[i]["edits"])
            resolves = sorted(set(b["implements"]) | set(pr_ids))
            log(f"C4.3 gate + merge {b['name']} resolving {resolves}")
            merges[b["name"]] = prsim.pr_merge(g, b["name"], resolves, gd, baseline)
        else:
            log(f"C4.3 gate seeded broken branch {b['name']} (must FAIL, must not merge)")
            merges[b["name"]] = prsim.pr_merge(g, b["name"], [], gd, baseline)
    dump_json(merges, gd / "merges.json")
    main_ids = sorted(i for i, d in dmap.items() if d["disposition"] != "reject" and not d.get("via_branch"))
    for i in main_ids:
        log(f"C5.2 apply {i} on main")
        apply_edits(g.repo, dmap[i]["edits"], i)
        g.commit(f"Resolve {i} ({dmap[i]['disposition']})\n\nComment-Id: {i}")
    g("tag", "v2")

    # ---- v2 compile from the v2 tag ----
    log("C5.3 compile v2 from tag v2")
    exp = R / "v2src"
    prsim._export(g, "v2", exp)
    steps["v2_compile_exit"] = compile_dir(exp, R / "v2")
    shutil.rmtree(exp)
    srcmap(R / "v2", "draft.adoc", R / "v2" / "srcmap.json")
    v2 = Doc(R / "v2")
    log("C2.4 map v1 -> v2")
    mapping = map_versions(v1, v2)
    dump_json(mapping, R / "map" / "mapping.json")
    log("C5.3/C5.4 containment + trace")
    tracemod.build(register, disp, mapping, v2, g, R / "trace")

    # ---- C6 review build ----
    log("C6 project register into derived v1 review input; compile")
    review.project(v1, POC / "src", register, R / "review" / "input")
    steps["review_compile_exit"] = compile_dir(R / "review" / "input", R / "review" / "build")
    srcmap(R / "review" / "build", "draft.adoc", R / "review" / "build" / "srcmap.json")
    anns = review.sem_annotations(R / "review" / "build" / "draft.xml")
    for a in anns:
        a["cid"] = a["text"].split("]")[0].lstrip("[") if a["text"].startswith("[") else ""
    nglue = review.inject_html(R / "review" / "build" / "draft.html", anns, R / "review" / "build" / "draft.review-glue.html")
    dump_json({"semantic": anns, "pdf": review.pdf_annotations(R / "review" / "build" / "draft.pdf"),
               "html_glue_injected": nglue}, R / "review" / "annotations.json")
    dump_json({"semantic": review.sem_annotations(R / "v1" / "draft.xml"),
               "pdf": review.pdf_annotations(R / "v1" / "draft.pdf")}, R / "review" / "clean-annotations.json")

    # ---- C7 report ----
    log("C7 disposition report from the resolved register only")
    subprocess.run([sys.executable, str(POC / "tools" / "report.py"), str(R / "trace" / "register.resolved.json"),
                    str(R / "report"), "../v2/draft.html"], check=True)
    dump_json(steps, R / "steps.json")
    log("checks")
    import checks
    summary = checks.run_all(R)
    dump_json(summary, R / "checks" / "summary.json")
    bad = [c for c in summary if c["result"] == "FAIL"]
    for c in summary:
        log(f"  {c['clause']:6} {c['result']:4}  {c['summary']}")
    log(f"done: {len(summary)} clause checks, {len(bad)} FAIL")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
