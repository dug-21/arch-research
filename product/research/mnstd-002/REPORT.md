<!-- Persisted verbatim by research-leader from the factory-curator's inline return (subagent file write was blocked; OBS-2: leader persists). Extracted mechanically from the agent's final message. -->
# mnstd-002 — REPORT: ISO-style Metanorma authoring and commenting, proven by one prototype

**Run:** `mnstd-002` · **Goal:** `mnstd` **#329** · **Issue:** [#74](https://github.com/dug-21/arch-research/issues/74) · **PR:** [#75](https://github.com/dug-21/arch-research/pull/75) (rebase-merged, head `417b83a`)
**Confidence-required:** validated (owner, binding: `product/research/mnstd-001/OWNER-BRIEF.md`) · research-scope with a feasibility phase
**Predecessor:** `mnstd-001` (decompose-scope; board in `product/research/mnstd-001/BOARD.md`)
**Method stamps:** mnstd-001 `wf-v0.26-46-gc4b39f5` · mnstd-002 `wf-v0.26-50-gecac38f`
**Synthesized at:** `main` @ `6632457` · **Author:** `factory-curator` · 2026-11-13
**Position finding:** **#384** (tag `position`)

---

## 1. The question

The owner wanted to *see* ISO-style standards authoring and commenting/review working in Metanorma, in a prototype
we build and run (OWNER-BRIEF). mnstd-001 split this into a 7-capability chain with 8 NFRs:

- C1 compile → C2 anchor resolver → C3 intake;
- C3 then feeds C4 (PR channel), C5 (disposition, then C7 report) and C6 (annotated render).

The SCOPE question:

> Can an ISO-flavor Metanorma draft, run through one reproducible Docker-plus-glue pipeline we build, clear every
> `done_when` clause of C1–C7 and N1–N8: intake validated against the document, a traced v2, PR-channel review, native
> review annotations, and a disposition report?

## 2. Verdict

**Yes, with one exception: native HTML review notes.** 14 of the 15 board nodes are `grade:proven`. **C6 is
`partial`**, because metanorma-iso 3.5.14 ISO HTML renders no native reviewer notes. The PDF renders them as native
sticky notes, and the owner ruled that HTML notes injected by our script do not count.

The working recipe (position #384) is **assemble the compiler, build thin glue, use plain git**:

| Layer | Call | What |
|---|---|---|
| Compiler | **Assemble** | `metanorma/metanorma@sha256:836b7ab2…dff3da` (Metanorma 2.5.24, metanorma-iso 3.5.14, mn2pdf 2.74), every run `--network none` |
| Resolver, intake, dispositions, edits, trace, report | **Build** (thin) | Python 3.14 stdlib glue. Metanorma has no locator resolver, no comment intake and no disposition loop. `commenter` is reference-only. |
| PR review | **Assemble git + build the gate** | Plain local git: review-record files, fixed-identity commits, `Comment-Id` / `Resolves:` trailers, `--no-ff` merges, and a pre-merge compile gate whose verdict is *not* the exit code |
| Rendered review | **Assemble (PDF)**, **no native HTML route** | `[reviewer,date,from,to]` + `****` projected into a derived input → semantic `<annotation>` → native PDF notes |

## 3. Final board (live; verified via `context_graph(subgraph, seed 329, Advances, incoming)` on 2026-11-13)

| Node | Name | Old id | Current id | Grade |
|---|---|---|---|---|
| C1 | ISO draft compiles to HTML, PDF, semantic XML | 336 | **#365** | proven |
| C2 | Any location resolves to exactly one element | 335 | **#366** | proven |
| C3 | Validated, clause-anchored comment intake | 334 | **#367** | proven |
| C4 | Git/PR review feeds the same register | 332 | **#368** | proven |
| C5 | Disposition loop produces a traced v2 | 333 | **#369** | proven |
| C6 | v1 review draft with native annotations | 331 | **#371** | **partial** (C6.1-HTML) |
| C7 | Disposition report | 330 | **#370** | proven |
| N1 | One-command reproducible demo | 337 | **#372** | proven |
| N2 | Contained, pinned toolchain | 338 | **#364** | proven |
| N3 | Deterministic regeneration | 339 | **#373** | proven |
| N4 | ISO comment-template field fidelity | 340 | **#374** | proven |
| N5 | End-to-end comment traceability | 341 | **#375** | proven |
| N6 | No external side effects | 342 | **#376** | proven |
| N7 | Lean repository footprint | 343 | **#377** | proven |
| N8 | Original sample content | 344 | **#378** | proven |

Every `proven` was set by `context_correct` with `proven_by` attached in the same step (GRADES.md). C6 was set by
`context_correct` (evidence + ruling 3) and then `context_tag replace grade:partial`. All 74 authored edges were
verified present between active nodes after the moves.

## 4. Technologies (the first nodes in a new region of the library)

| Tech | Old id | Current id | Grade | Role |
|---|---|---|---|---|
| metanorma/metanorma image @ digest + metanorma-iso 3.5.14 — ADOPT | 349 | **#379** | proven | C1 compile; compile step of the C4.3 gate and C5.3 |
| Locator resolver: presentation-XML numbers + Asciidoctor sourcemap + anchor-keyed v1→v2 alignment — ASSEMBLE + BUILD | 350 | **#380** | proven | C2.1–C2.4, C3.2, C4.2, C5.3 |
| Local git review & attribution — ASSEMBLE + BUILD | 352 | **#381** | proven | C4.1–C4.5, C5.2, N3.2; records the refined gate verdict rule |
| ISO 2012-03 template schema + validator/register/report glue | 353 | **#382** | proven | C3, C5.1, C7, N4 |
| Native reviewer annotations → PDF (+ HTML glue) | 351 | **#383** | **partial** | C6 PDF leg native; HTML glue excluded (ruling 3) |
| metanorma/commenter 0.7.0 — reference only | 354 | **#354** | claimed | Vocabulary source; not on the gated path, not in the image |

Key findings carried by the position (all `mnstd-002`, `Supports` edges from #384):

- #355: auto-ids are content+position hashes, stable on recompile, unstable across edits.
- #356: the compile exit code misses most broken sources, and `--strict` is inert.
- #358: ISO HTML renders no native reviewer annotations, contrary to the docs.
- #359: ISO PDF renders them as native sticky notes and ignores stage/override gating.
- #360: PDF needs a font set the image does not ship.
- #361: `commenter validate` is structural only.
- #362: annotation anchor failure modes.
- #363: fixed-identity commits give reproducible hashes, and trailers are readable from `git log`.

#357 (duplicate-anchor severity, `unresolved`) was settled empirically in RESULT.md. The duplicate yields **both**
STANDOC_36 at severity 0 and ISO_122 at severity 1, and the full compile exits 1. The node has not yet been corrected
(follow-on F6).

## 5. What the prototype demonstrates: the four owner demonstrations

| Owner demonstration (OWNER-BRIEF) | Capabilities | What the gated run shows |
|---|---|---|
| (baseline) authoring | C1 #365, C2 #366 | A fictitious ISO CD draft (foreword, scope, normative refs, terms, clauses to level 3, 3 tables, figure, notes, annex A) compiles to XML/HTML/PDF with exit 0. Warnings are explained. 18/18 locators and 15/15 `file:line` resolve, 14/14 bad ones are rejected with a reason, and v1→v2 maps under an insert-before renumbering (9 old→new pairs). |
| (1) structured comment intake | C3 #367 | 3 reviewers, 2 MB/NC, 10 sheet comments (ge/te/ed) go into one register with resolved element ids. 11 seeded-invalid rows are each rejected with a reason and exit 1, and the register is byte-identical with and without them. Colliding local ids are disambiguated (`GB-01-001` / `GB-02-001`). |
| (2) comment resolution loop | C5 #369 | 13 dispositions (6 accept, 4 modify, 3 reject) cover both channels. Scripted edits make one commit per comment id, and every non-merge commit is attributable. v2 compiles. Containment is recomputed from v2 XML via the C2.4 mapping (10/10). The trace table has 13 rows. |
| (3) Git/PR review | C4 #368 | Local repo with tag v1 and a change branch. 2 reviewers line-anchor on the diff, and their comments normalise into the same register (channel `pr`). The gate passes the change branch and fails 3 seeded broken branches, 2 of which **exit 0**. The merge carries `Resolves:` + `Gate: PASS <sha>`. No remote, `protocol.allow=never`. |
| (4) rendered review output | C6 #371 (partial), C7 #370 | Review build: 13 semantic `<annotation>` elements give 13 native PDF notes (reviewer, date, text). The clean build has 0, and the committed source has no review blocks. **Native ISO HTML: 0.** The disposition report (HTML + YAML + CSV) is in ISO column order with disposition and v2 links, and its counts reconcile by type × disposition × MB. |

## 6. How to run it

From the repo root, on an x86_64 host with Docker, Python 3.14 and git (no Ruby needed):

    docker pull metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da  # once, networked
    make -C product/research/mnstd-002/poc fonts   # once, NETWORKED: ~833 MiB cache at ~/.cache/mnstd-002-fonts; verified against poc/fonts/MANIFEST.json
    make -C product/research/mnstd-002/poc demo    # gated, network-free: 2 full runs from clean + self-tests + cross-run checks (~10 min)

- Outputs: `poc/build/run-{a,b}/` (gitignored).
- Committed evidence snapshot: `artifacts/evidence/` (~0.4 MB).
- Clause-by-clause pointers: `artifacts/RESULT.md`.
- Configuration in force: `artifacts/ENVELOPE.md`.

## 7. Firewall history

1. **Tech-discovery:** W0–W4 findings were distilled to techs #349–#354 (`claimed`) and findings #355–#363. Leader
   rulings R1–R3 (SCOPE Extension) covered fonts, HTML glue and git as a prerequisite.
2. **Feasibility:** factory-poc built the rig (`c99d0bd`, frozen task) and the evidence (`323a13f`): n=2 demos, 4 runs,
   37/37 checks, 33/33 self-tests.
3. **Firewall gate:** the independent validator returned **SCOPE FAIL** (`reports/gate-feasibility.md`). The evidence
   was strong (n=6 runs including its own, byte-identical identity set). Four clauses failed on their **literal
   wording** against toolchain and environment facts:
   - N1.1 and N6.1: a networked font fetch outside `make demo`.
   - C1.3: the semantic XML carries no numbers.
   - C6.1-HTML: native ISO HTML renders 0 notes, and the glue is the "bespoke overlay" the node's `why` excludes.

   The validator also found that the C5.3 checker trusted the pipeline's `containment.json`.
4. **Owner rulings (verbatim in SCOPE.md, last Extension, recorded on #74 before any grade moved):**
   1. N1.1/N6.1 YES: fonts are environment, like the image pull, on condition that they are pinned.
   2. C1.3 YES: presentation-XML numbers joined by element id are Metanorma's native layering.
   3. C6.1-HTML NO: C6 stays `partial`.

   Before merge: fix the C5.3 checker to recompute containment, add a tamper test, and get an independent
   validator spot-check.
5. **Rework 1:**
   - `4ac942e`: the C5.3 checker recomputes containment from v2 XML.
   - `922d004`: font pin manifest of 45 files.
   - `bbce28b`: re-freeze, so checker code is now frozen.
   - `417b83a`: demo-3 evidence (n=1, 37/37 self-tests).
6. **Spot-check PASS** (`reports/gate-feasibility-rework1.md`). The validator wrote its own 7 tamper cases across all
   three containment modes, and all went red.
7. **PR #75 rebase-merged at `417b83a`.** The diff of poc/, task/ and artifacts/ is empty between each pre-rebase SHA
   and its rebased SHA. Grades were then moved per GRADES.md.

## 8. Limits and caveats (do not strip)

- **Envelope:** one host (x86_64, Docker 29.7.2), one day (2026-11-13), within about 25 minutes for the gated runs.
  n = 6 full pipeline runs before rework, plus n=1 after rework. **No fresh-clone, second-host or cross-day run.**
- **Fonts:** the pin fixes *this* set (fontist formulas `75a1adb7`). It does not show that upstream still serves it.
  The pin is enforced by `make fonts`, not by `make demo`. Font licensing and provenance were not inspected.
- **C6:** native HTML notes do not exist in metanorma-iso 3.5.14. The PDF range is a point note at `from`, not a
  visible extent. Whole-table and whole-list anchor failures are attested from W4 and were not re-measured.
- **Residual checker gap:** a coordinated forgery of `mapping.json` + v2 XML passes the C5.3 and C2.4 checkers, and
  only N5.1 catches it. The C2.4 checker does not re-derive the mapping. Containment is substring-based.
- **Untested:** `include::` multi-file sources, heavy paragraph rewrites (difflib < 0.6), the missing-image, Python and
  git prerequisite paths (code exists, not self-tested), and DOCX (N4.3 N/A).
- **Non-deterministic:** HTML and PDF bytes differ run to run, and the cause was not analysed. The N3 identity set
  excludes them.
- **Attested, not measured:** N8 authorship and originality; host-side network isolation (command trace, not syscalls).
- **Scope:** ISO flavor only. No real ISO process (OSD, balloting), no real standard text, no forge.

## 9. Staged follow-ons (proposals, not commitments)

| # | Follow-on | Moves |
|---|---|---|
| F1 | **C6 HTML route:** file an upstream metanorma-iso issue for native HTML reviewer-note rendering, or test another output or flavor that renders notes natively. A native route demonstrated by us is the only way C6 reaches `proven`. | C6 #371, tech #383 |
| F2 | **C2.4 checker recomputes the v1→v2 mapping**, or C5.3 asserts the counterpart the way N5.1 does. Add the two-file forgery as a self-test. | Rig robustness (no grade) |
| F3 | **Fresh-clone, cross-day, second-host run**, including `make fonts` on an empty cache against upstream. This widens the N1/N3 envelope and tests whether the font pin still resolves. | N1 #372, N3 #373 envelope |
| F4 | **Stretch: DOCX disposition report via `commenter fill`** in a derived image (a new pin, so N2 stays clean). Rules N4.3. | #354, N4 #374 |
| F5 | Wire the font-pin check into `make demo`/prereqs, so an unverified cache fails fast. | Rig hardening |
| F6 | Correct #357 with the empirical result (both severities; full compile exits 1). | Graph hygiene |

## 10. Provenance

- Sources read directly:
  - `SCOPE.md`, `findings-W0.md`–`findings-W4.md`
  - `reports/gate-feasibility.md`, `reports/gate-feasibility-rework1.md`
  - `GRADES.md`, `artifacts/RESULT.md`, `artifacts/ENVELOPE.md`, `poc/README.md`
  - `product/research/mnstd-001/OWNER-BRIEF.md`, `BOARD.md`
- Board, tech ids and grades were verified live by subgraph query on #329 (Advances, incoming) and on C1–C7
  (Prerequisite, incoming).
- This report moves no grade. Proof lives in the attached rig artifacts and the gate reports.
