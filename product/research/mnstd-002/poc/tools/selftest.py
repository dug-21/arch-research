"""Self-tests of the pass-checks: every checker must PASS the real run (known-green, from checks/summary.json)
and must FAIL a tampered copy (known-red / tampered-tests). A checker that cannot be made to fail is not a
checker. Each case copies the run dir (and, where needed, the task dir) to a scratch area and tampers ONE thing.
Usage: selftest.py <run-dir> <out.json>
Authored by factory-poc (mnstd-002).
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import checks  # noqa: E402
import frozen  # noqa: E402
import trace as tracemod  # noqa: E402
from common import POC, dump_json, load_json  # noqa: E402
from gitx import Git  # noqa: E402
from resolver import Doc  # noqa: E402

TASK = POC.parent / "task"


def clause(results, name):
    for r in results if isinstance(results, list) else [results]:
        if isinstance(r, dict) and r.get("clause") == name:
            return r["result"]
    raise KeyError(name)


class Case:
    def __init__(self, base: Path, scratch: Path, name: str):
        self.dir = scratch / name
        if self.dir.exists():
            shutil.rmtree(self.dir)
        shutil.copytree(base, self.dir, symlinks=True, ignore=shutil.ignore_patterns("selftest*"))
        self.task = scratch / f"{name}.task"
        if self.task.exists():
            shutil.rmtree(self.task)
        shutil.copytree(TASK, self.task)

    def ctx(self):
        return checks.Ctx(self.dir, self.task)


def edit_json(p: Path, fn):
    d = json.loads(p.read_text())
    fn(d)
    p.write_text(json.dumps(d, indent=2) + "\n")


def main(argv):
    base, out = Path(argv[0]).resolve(), Path(argv[1])
    scratch = base / "selftest-scratch"
    scratch.mkdir(exist_ok=True)
    green = {r["clause"]: r["result"] for r in load_json(base / "checks" / "summary.json")}
    cases = []

    def case(name, target, fn, expect="FAIL"):
        try:
            got = fn(Case(base, scratch, name))
        except SystemExit as e:  # an abort is NOT detection: the tamper itself or the checker broke
            got = f"ERROR (aborted: {e.code})"
        except Exception as e:  # noqa: BLE001
            got = f"ERROR (raised {type(e).__name__}: {e})"
        detected = str(got).startswith(expect)
        cases.append({"case": name, "check": target, "green_result": green.get(target, "n/a"), "tampered_result": str(got),
                      "detected": detected})
        print(f"[selftest] {name:44} {target:6} green={green.get(target, 'n/a'):4} tampered={str(got)[:40]:40} {'DETECTED' if detected else 'MISSED'}")

    # C1.2 — an unexplained warning appears
    def t(c):
        p = c.dir / "v1" / "draft.err.html"
        s = p.read_text()
        s = s.replace("</tbody>", '<tr class="severity2">\n<td></td><th><code>X</code></th><td>ISO_999</td>\n<td>seeded unexplained warning</td><td><pre></pre></td><td>2</td></tr></tbody>', 1)
        p.write_text(s)
        return checks.c1_2(c.ctx())["result"]
    case("unexplained-warning", "C1.2", t)

    def t(c):
        p = c.task / "expected" / "locators.json"
        edit_json(p, lambda d: d["positive"][0].__setitem__("anchor", "cl-general"))
        return checks.c2_locators(c.ctx(), p)[0]["result"]
    case("locator-expectation-tampered", "C2.1", t)

    def t(c):
        p = c.task / "expected" / "lines.json"
        edit_json(p, lambda d: d["positive"][9].__setitem__("clause_no", "5.1"))
        return checks.c2_lines(c.ctx(), p)[0]["result"]
    case("line-expectation-tampered", "C2.2", t)

    def t(c):
        p = c.task / "expected" / "locators.json"
        edit_json(p, lambda d: d["negative"][0].__setitem__("code", "element_not_found"))
        r = checks.c2_locators(c.ctx(), p)[1]
        return "PASS" if r[1] else "FAIL"
    case("negative-locator-reason-tampered", "C2.3", t)

    def t(c):
        p = c.task / "expected" / "c24.json"
        edit_json(p, lambda d: d["renumbered"].pop("cl-report"))
        return checks.c2_4(c.ctx(), p)["result"]
    case("c24-renumber-expectation-tampered", "C2.4", t)

    def t(c):
        m = c.dir / "map" / "mapping.json"
        edit_json(m, lambda d: [e.__setitem__("status", "deleted") for e in d["elements"] if e["anchor"] == "note-general-1"])
        return checks.c2_4(c.ctx())["result"]
    case("c24-element-lost", "C2.4", t)

    def t(c):
        p = c.dir / "intake" / "B" / "register.json"
        edit_json(p, lambda d: d.append(dict(d[0], id="DE-01-001", source="sheets/de-mallory.csv:row1")))
        return clause(checks.c3(c.ctx()), "C3.3")
    case("seeded-row-leaks-into-register", "C3.3", t)

    def t(c):
        p = c.task / "expected" / "invalid-sheet.json"
        edit_json(p, lambda d: d.__setitem__("de-mallory.csv:row3", ["clause_not_found"]))
        return clause(checks.c3(c.ctx()), "C3.3")
    case("invalid-sheet-expectation-tampered", "C3.3", t)

    def t(c):
        p = c.dir / "intake" / "final" / "register.json"
        edit_json(p, lambda d: d[1].__setitem__("id", d[0]["id"]))
        return clause(checks.c3(c.ctx()), "C3.4")
    case("register-id-collision", "C3.4", t)

    def t(c):
        p = c.task / "expected" / "pr-rejects.json"
        edit_json(p, lambda d: d.pop("change-apparatus-wording/erin.json#3"))
        return clause(checks.c4(c.ctx()), "C4.2")
    case("pr-reject-expectation-tampered", "C4.2", t)

    def t(c):
        p = c.dir / "gate" / "gate.tsv"
        p.write_text(re.sub(r"(change/broken-table\t.*?)verdict=FAIL", r"\1verdict=PASS", p.read_text()))
        return clause(checks.c4(c.ctx()), "C4.3")
    case("broken-branch-gate-verdict-flipped", "C4.3", t)

    def t(c):
        g = Git(c.dir / "repo")
        g("checkout", "-q", "main")
        g.tick = 500
        g("merge", "-q", "--no-ff", "-m", "Merge change/broken-table\n\nResolves: GB-01-004\n", "change/broken-table")
        return clause(checks.c4(c.ctx()), "C4.3")
    case("broken-branch-merged-around-gate", "C4.3", t)

    def t(c):
        g = Git(c.dir / "repo")
        g("remote", "add", "origin", "https://example.invalid/repo.git")
        return clause(checks.c4(c.ctx()), "C4.5")
    case("network-remote-added", "C4.5", t)

    def t(c):
        p = c.task / "invalid" / "dispositions-bad.json"
        edit_json(p, lambda d: d.__setitem__("dispositions", load_json(TASK / "dispositions.json")["dispositions"]))
        import dispose
        rc = dispose.main(["--register", str(c.dir / "intake" / "final" / "register.json"), "--dispositions", str(p),
                           "--out", str(c.dir / "dispositions" / "validation-bad.json")])
        return "PASS" if rc == 0 else "FAIL"
    case("validator-accepts-good-record(control)", "C5.1", t, expect="PASS")

    def stray(c, cid, extra):
        g = Git(c.dir / "repo")
        g("checkout", "-q", "-f", "v2")
        g.tick = 900
        f = c.dir / "repo" / "draft.adoc"
        f.write_text(f.read_text().replace(*extra, 1))
        g.commit(f"Resolve {cid} (accept)\n\nComment-Id: {cid}")
        g("tag", "-f", "v2")
        return checks.attribution(g, c.ctx().register, c.ctx().disp)

    def t(c):
        probs = stray(c, "GB-01-001", ("The mallet has a felt head", "The mallet has a soft felt head"))
        return "FAIL" if probs else "PASS"
    case("stray-edit-commit", "C5.2", t)

    def t(c):
        g = Git(c.dir / "repo")
        sha = g("rev-parse", "v2").strip()
        # rewrite the LAST attributed commit so it carries one extra stray change under its own trailer
        g("checkout", "-q", "-f", f"{sha}^")
        g.tick = 950
        f = c.dir / "repo" / "draft.adoc"
        d = c.ctx().disp
        last = [x for x in g("log", "-1", "--format=%(trailers:key=Comment-Id,valueonly)", sha).split() if x][0]
        s = f.read_text()
        for e in d[last]["edits"]:
            s = s.replace(e["find"], e["replace"], 1)
        s = s.replace("The mallet has a felt head", "The mallet has a soft felt head", 1)
        f.write_text(s)
        new = g.commit(f"Resolve {last}\n\nComment-Id: {last}")
        p = checks.commit_scope(g, new, d[last])
        return "FAIL" if p else "PASS"
    case("stray-change-inside-attributed-commit", "C5.2", t)

    def t(c):
        probs = stray(c, "GB-01-004", ("Marks made with ink", "Marks made with pencil"))
        return "FAIL" if probs else "PASS"
    case("reject-changes-source", "C5.2", t)

    def t(c):
        p = c.task / "dispositions.json"

        def fn(d):
            for x in d["dispositions"]:
                if x["id"] == "FR-01-004":
                    x["modified_text"] = x["expect_in_v2"] = "for twenty days before the test"
        edit_json(p, fn)
        ctx = c.ctx()
        v2 = Doc(c.dir / "v2")
        tracemod.build(ctx.register, list(ctx.disp.values()), load_json(c.dir / "map" / "mapping.json"), v2,
                       Git(c.dir / "repo"), c.dir / "trace")
        return clause(checks.c5(ctx), "C5.3")
    case("containment-expectation-not-in-v2", "C5.3", t)

    # Rework 1 (gate-feasibility §4.1): v2 semantic XML loses an ACCEPTED change AFTER the run (GB-01-003,
    # 120 mm reverted to its v1 value 80 mm); trace/containment.json is left untouched. The checker must
    # recompute from v2/draft.xml and go red. Before rework 1 this case was MISSED (validator tamper).
    def t(c):
        p = c.dir / "v2" / "draft.xml"
        s = p.read_text(encoding="utf-8")
        if s.count("120 mm") != 1:
            return f"ERROR (tamper precondition: '120 mm' occurs {s.count('120 mm')}x in v2 XML)"
        p.write_text(s.replace("120 mm", "80 mm"), encoding="utf-8")
        return clause(checks.c5(c.ctx()), "C5.3")
    case("v2-xml-accepted-change-reverted", "C5.3", t)

    # the pipeline's recorded containment says FAIL for one accept while v2 is intact: record and recomputation
    # disagree, so the checker must not report green on either alone.
    def t(c):
        p = c.dir / "trace" / "containment.json"
        edit_json(p, lambda d: [x.__setitem__("pass", False) for x in d if x["id"] == "GB-01-001"])
        return clause(checks.c5(c.ctx()), "C5.3")
    case("containment-record-disagrees", "C5.3", t)

    def t(c):
        p = c.dir / "trace" / "trace.csv"
        lines = p.read_text().split("\n")
        cols = lines[1].split(",")
        cols[6] = ""
        lines[1] = ",".join(cols)
        p.write_text("\n".join(lines))
        return clause(checks.c5(c.ctx()), "C5.4")
    case("trace-blank-commit-cell", "C5.4", t)

    def t(c):
        p = c.dir / "review" / "annotations.json"
        edit_json(p, lambda d: d["pdf"].pop(3))
        return clause(checks.c6(c.ctx()), "C6.2")
    case("pdf-drops-one-annotation", "C6.2", t)

    def t(c):
        p = c.dir / "review" / "annotations.json"
        edit_json(p, lambda d: d["semantic"].append(dict(d["semantic"][0])))
        return clause(checks.c6(c.ctx()), "C6.2")
    case("duplicate-semantic-annotation", "C6.2", t)

    def t(c):
        p = c.dir / "review" / "input" / "draft.adoc"
        p.write_text(p.read_text().replace("The test stand holds", "The stand holds", 1))
        return clause(checks.c6(c.ctx()), "C6.3")
    case("derived-input-edits-v1-text", "C6.3", t)

    def t(c):
        p = c.dir / "review" / "clean-annotations.json"
        edit_json(p, lambda d: d["semantic"].append({"reviewer": "x", "text": "[GB-01-001] leaked"}))
        return clause(checks.c6(c.ctx()), "C6.3")
    case("clean-build-shows-annotation", "C6.3", t)

    def t(c):
        p = c.dir / "report" / "report.html"
        p.write_text(p.read_text().replace("Rejected.", "Rejected (edited by hand).", 1))
        return clause(checks.c7(c.ctx()), "C7.1")
    case("report-hand-edit", "C7.1", t)

    def t(c):
        p = c.dir / "report" / "report.csv"
        lines = p.read_text().split("\n")
        lines[1] = re.sub(r",(ge|te|ed),", lambda m: ",te," if m.group(1) != "te" else ",ed,", lines[1], count=1)
        p.write_text("\n".join(lines))
        return clause(checks.c7(c.ctx()), "C7.2")
    case("report-csv-count-drift", "C7.2", t)

    def t(c):
        p = c.dir / "report" / "report.html"
        p.write_text(re.sub(r'href="\.\./v2/draft\.html#[^"]+"', 'href="../v2/draft.html#does-not-exist"', p.read_text(), count=1))
        return clause(checks.c7(c.ctx()), "C7.3")
    case("report-link-to-missing-v2-location", "C7.3", t)

    def t(c):
        (c.dir / "trace" / "stray.txt").write_text("see comment GB-09-999\n")
        return checks.n5_2(c.dir, {r["id"] for r in c.ctx().register})["result"]
    case("artefact-with-unregistered-id", "N5.2", t)

    def t(c):
        p = c.dir / "command-trace.log"
        p.write_text(p.read_text() + "git -C repo push origin main\n")
        return clause(checks.nfr_local(c.ctx()), "N6.1")
    case("trace-contains-git-push", "N6.1", t)

    def t(c):
        p = c.dir / "command-trace.log"
        p.write_text(p.read_text() + "docker run --rm -v /x:/metanorma metanorma/metanorma:latest metanorma compile x.adoc\n")
        return clause(checks.nfr_local(c.ctx()), "N6.1")
    case("trace-networked-unpinned-docker-run", "N6.1", t)

    def t(c):
        p = c.dir / "command-trace.log"
        p.write_text(p.read_text() + "commenter github-create --repo dug-21/x sheet.yaml\n")
        return clause(checks.nfr_local(c.ctx()), "N6.2")
    case("trace-contains-commenter-github", "N6.2", t)

    def t(c):
        root = c.dir / "frozen-root"
        (root / "poc").mkdir(parents=True)
        shutil.copytree(c.task, root / "task")
        shutil.copytree(POC / "src", root / "poc" / "src")
        shutil.copy(POC / "warnings-explained.json", root / "poc" / "warnings-explained.json")
        ok_before = not frozen.verify(root)
        p = root / "task" / "expected" / "locators.json"
        p.write_text(p.read_text().replace("cl-scope", "cl-general", 1))
        return ("FAIL" if frozen.verify(root) else "PASS") if ok_before else "PASS (baseline not green)"
    case("fixture-file-tampered", "frozen", t)

    def t(c):
        env = dict(os.environ)
        bindir = c.dir / "fakebin"
        bindir.mkdir()
        for tool in ("python3", "git", "awk", "dirname", "basename"):
            real = shutil.which(tool)
            if real:
                os.symlink(real, bindir / tool)
        env["PATH"] = str(bindir)
        p = subprocess.run(["/bin/bash", str(POC / "tools" / "prereqs.sh")], capture_output=True, text=True, env=env)
        return "FAIL" if p.returncode == 2 and "docker" in p.stderr else f"PASS (exit {p.returncode}: {p.stderr.strip()})"
    case("prereq-docker-missing", "N1.3", t)

    def t(c):
        env = dict(os.environ, MNSTD_FONT_CACHE=str(c.dir / "no-such-font-cache"))
        p = subprocess.run(["/bin/bash", str(POC / "tools" / "prereqs.sh")], capture_output=True, text=True, env=env)
        return "FAIL" if p.returncode == 2 and "font cache" in p.stderr else f"PASS (exit {p.returncode})"
    case("prereq-font-cache-missing", "N1.3", t)

    # rework 1 (owner ruling 1): one byte of a pinned font changes -> fontpin verify must go red. Runs on a tiny
    # scratch cache (one real font file copied from the host cache when present, else synthetic bytes) with its
    # own scratch manifest, so it never touches the host cache or poc/fonts/MANIFEST.json.
    def t(c):
        import fontpin
        fc = c.dir / "fontcache"
        (fc / "metanorma" / "fonts").mkdir(parents=True)
        src = fontpin.FONT_CACHE / "metanorma" / "fonts" / "STIX2Math.otf"
        f = fc / "metanorma" / "fonts" / "STIX2Math.otf"
        f.write_bytes(src.read_bytes() if src.exists() else b"OTTO" + bytes(64))
        man = c.dir / "font-manifest.json"
        if fontpin.main(["write", "--cache", str(fc), "--manifest", str(man)]) != 0 or \
                fontpin.main(["verify", "--cache", str(fc), "--manifest", str(man)]) != 0:
            return "PASS (baseline not green)"
        b = bytearray(f.read_bytes())
        b[-1] ^= 0xFF
        f.write_bytes(bytes(b))
        return "FAIL" if fontpin.main(["verify", "--cache", str(fc), "--manifest", str(man)]) != 0 else "PASS"
    case("font-pin-byte-changed", "fonts", t)

    shutil.rmtree(scratch, ignore_errors=True)
    missed = [x for x in cases if not x["detected"]]
    dump_json({"cases": cases, "all_detected": not missed}, out)
    print(f"[selftest] {len(cases) - len(missed)}/{len(cases)} tampered cases detected")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
