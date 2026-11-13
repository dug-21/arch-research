# mnstd-002 — FIREWALL gate (feasibility): independent validation report

- **Validator:** `factory-validator` (agent_id `factory-validator`). I did not build this artifact and did not advise on
  building it. Gate-input independence holds.
- **Date:** 2026-11-13. **Artifact:** branch `research/mnstd-002` @ `17a7fa4` (PR dug-21/arch-research#75); rig commit
  `7953833`. **Builder claim read as a claim:** `artifacts/RESULT.md`, `artifacts/ENVELOPE.md`.
- **Governing text:** fetched by me from Unimatrix (`context_graph` subgraph, `detail:"full"`): C1 #336, C2 #335,
  C3 #334, C4 #332, C5 #333, C6 #331, C7 #330, N1–N8 #337–#344, technologies #349–#354. All are `Active`, v1, and none is
  superseded. All capabilities are `grade:missing`; all technologies are `grade:claimed`. The `About` edges (governance)
  are listed in §5. Rulings follow SCOPE.md's proof bar and its 2026-11-13 Extension (R1–R3).

---

## 1. Verdict

**SCOPE FAIL. Return to the human. This is not an evidence failure, and no POC rework is recommended until the
owner rules.**

The artifact is real, reproducible and unusually well instrumented. I re-ran it from a clean detached checkout.
Exit 0, all 37 rig checks PASS, 33/33 rig self-tests PASS. The N3 identity set is byte-identical to both builder
invocations, including from a different checkout path. My own checks corroborate every clause the rig claims, with
one checker weakness noted in §4. The evidence is strong. Four clauses still fail on their literal text. In each
case the blocker is a mismatch between the bar's wording and the toolchain or environment. Better evidence would not
clear any of them:

| # | Failing clause | Why it fails (literal text) | Can a POC rework clear it? | What would clear it |
|---|---|---|---|---|
| F1 | **N1.1** (governs C1–C7) | "From a fresh clone with **only Docker, Node 24 and Python 3.14** on the host, **one command** … **no manual step**." The demo also needs a host-side, networked, **unpinned** 833 MiB font cache (`make fonts`) and a manual `docker pull`. Both are prerequisites outside `make demo`, and `make demo` fails fast without them. | **Partly.** `make demo` could self-provision (pull by digest, then fonts if absent) and be shown on an empty cache. That makes the demo networked, which deepens F2. | Owner amendment declaring one-time font provisioning to be environment, on a par with the image pull. With that amendment, N1.1 is **demonstrated**: my fresh checkout ran one command with no manual step (n=1, plus the builder's n=2). Otherwise the bounded rework described above. |
| F2 | **N6.1** (governs C4, C7; property applies to the whole demo) | "The only network access is the container image pull." PDF output needs a second networked step (the font fetch). | **No.** No rework clears it while C1 requires a PDF. Fonts are not in the pinned image. | Owner amendment of N6.1 (R1 explicitly left the text unamended and flagged this to the owner). Alternatively, a font-bearing image pinned by digest that is *pulled*, which is a new bar-relevant pin and out of the POC's hands. |
| F3 | **C1.3** | "The **semantic XML** … contains every authored clause, table and figure with a machine-readable id **and number**." I verified that the semantic XML (`draft.xml`) carries **no numbers**: zero `autonum`, and no number attribute on clause, table or figure. Numbers exist only in the presentation XML from the same compile (`@autonum`, caption labels), joined by `@semx-id`. | **No.** This is the tool's behavior (metanorma-iso 3.5.14). | Owner ruling that "semantic XML" in C1.3 admits the presentation XML of the same compile, joined by `@semx-id`. The substantive need (a machine-readable number per element, joinable to the semantic id) **is met and verified**. |
| F4 | **C6.1** (HTML leg) | "…in **HTML and PDF** shows every register comment as a **Metanorma-native** reviewer annotation". Native ISO HTML renders **0** (I measured 0 annotation markers in `review/build/draft.html`). The 13 HTML annotations are a glue `<aside>` overlay injected from native semantic data. The node's own `why` names the thing it rules out: "Metanorma's own annotation feature **rather than a bespoke overlay**." PDF leg: PASS. | **No.** Native HTML rendering does not exist in this metanorma-iso version (R2). | Owner ruling that glue HTML rendered from the native `<annotation>` data satisfies C6.1. Otherwise C6 stays `partial` until upstream renders annotations in HTML. |

Ruling R2 ("validator rules whether glue satisfies C6.1's wording"): **it does not.** The wording requires a native
annotation in HTML. The `why` excludes a bespoke overlay in so many words. The glue is honest, labelled and data-faithful,
but it is the excluded thing.

Ruling R1 (N6.1): **N6.1 on its literal text: FAIL** (second sentence; the first sentence, "no PR, issue, Action, push
or publication", PASSES). **Separately, the gated `make demo` is network-free: YES, verified independently.** All 24
container runs carry `--network none` (trace). My own `docker events` capture shows all 22 container attachments in
its window went to the `none` network, with 0 image pulls. Host glue imports no network module. Inner git has
`protocol.allow=never` and no remote.

One owner decision ("font provisioning is environment, like the image pull") clears F1 and F2 together. F3 and F4 each
need their own ruling. If the owner adopts all four readings, my recommendation becomes `proven` for C1–C7 within the
envelope in §6. If the owner adopts none, every capability is `partial` (see §5), because N1 governs all seven.

---

## 2. What I did (my own n, not the builder's)

| Step | Result |
|---|---|
| Detached checkout at `17a7fa4` in `/tmp/claude-1000/mnstd-002-validate` (outside the builder's worktree) | clean; `poc/build/` absent |
| `sha256sum -c task/FROZEN.sha256` | **19/19 OK** |
| Freeze precedes evidence | `task/`, `poc/` (including `tools/checks.py`, `tools/selftest.py`, shims) committed in `7953833`; `git diff 7953833 17a7fa4 -- poc task` is **empty**. The evidence commit adds only `artifacts/`. |
| `make -C product/research/mnstd-002/poc demo` | **exit 0**, wall time 9m55s; run-a 0, selftest 0, run-b 0; 37 checks PASS (N4.3 N/A); cross-run N1.2/N3.1/N3.2/N7.1 PASS; 33/33 self-tests detected |
| Determinism against committed evidence | Identity-set SHA-256 (register ×3, trace ×4, report ×3, v2 semantic XML) **identical** across builder demo-1, builder demo-2 and my demo-3. The v1/v2 inner-repo SHAs (`5410b5f…`/`f4e0d8b…`) are identical. `git diff` of the regenerated `artifacts/evidence/` against the commit shows changes only in volatile files (envelope timestamp, mn2pdf tmp filename in compile logs, absolute paths in command traces, snapshot size). Every register, trace, report, mapping, gate and C2 file is byte-identical. `normalised_hits: []`, so the declared-empty normalization list was never needed. |
| Totals | **n = 6 full pipeline runs** (builder 4, mine 2) across **3 invocations** and 2 checkout paths, all on one host, on 2026-11-13 |

**Environment recorded (part of the envelope; not repo content):** host x86_64, kernel 6.12.100+deb13-amd64, Docker
29.7.2. Image `metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da` present
locally (pulled by the leader). Python 3.14.7, git 2.55.0. `which ruby`/`which gem` exit 1. **Font cache** at
`$HOME/.cache/mnstd-002-fonts`: 873,405,539 bytes, 4,539 files. Content digest (sorted `sha256sum` of all files,
then hashed), taken by me after my run: **`03f4d031de6dd47952e9778aaa1dc1bdd097078d50bde95a891726ae78a0f968`**. Size
and file count match the builder's pre-run reading. Gated runs mount this cache **read-write**. Its contents came from
whatever fontist fetched on 2026-11-13: they are not pinned and their provenance and licensing were not inspected.
PDF output depends on them.

---

## 3. Independent spot-checks (not the rig's checkers)

| Check | My method | Result |
|---|---|---|
| Annotation count, semantic XML | ElementTree over `review/build/draft.xml`; `grep -c '<annotation '` | **13** (= register 13); v1 and v2 XML: 0 |
| PDF annotations | My own stream-decompressing scan of `review/build/draft.pdf` (rig code not used) | **13** `/Subtype /Text` (run-a and run-b). v1 and v2 PDFs: 0. Each note has `/T` = "reviewer (MB)" and `/M` = the comment date (for example `D:20261001000000` for alice). No highlight or range markup (see C6.1). PDF is 11 pages, `%PDF-1.7`, `%%EOF`. |
| Native HTML annotations | grep of reviewer names and ids in native `review/build/draft.html` | **0**. Glue file: 13 `mn-review-glue` asides, labelled "glue rendering of native data" |
| Annotation anchoring | every semantic `annotation/@from` resolves to an `@anchor`/`@id` in the review XML | 13/13 resolve. PR-US-01-001 carries from=`rv-e2`, to=`rv-e11` (two paragraphs) |
| C6.3 derived input | stripped the render attribute, `rv-e*` anchors and appended review blocks, then diffed against `poc/src/draft.adoc` | identical; committed source has 0 `[reviewer=`/`****`; clean build: 0/0/0 |
| Inner repo | `git remote -v`, local config, `merge-base --is-ancestor`, trailers | no remote; `protocol.allow=never`. The 3 broken branches are **not** ancestors of `main`; `change/apparatus-wording` is merged. Merge `4f70611` carries `Resolves: FR-01-002, PR-DE-01-001, PR-US-01-001` + `Gate: PASS b7dd8cf…` (its second parent) |
| C5.2 attribution | `git log --no-merges v1..v2` trailers; `git diff v1 v2` | 10 commits, one `Comment-Id` each, covering exactly the 10 accept/modify ids. The diff contains only those 10 edits plus the Safety clause heading and anchor that belong to GB-02-001 |
| C5.4 commit cells | for each non-reject trace row, the commit's `Comment-Id` trailer equals the row id | 10/10 match; 3 rejects hold the sentinel |
| C5.3 containment (re-derived) | my own check of the expected text (proposed_change for accept, `modified_text` for modify) against the v2 element in `trace.csv` | 9/10 inside the mapped v2 element; PR-US-01-001 (ranged) inside the range union in the document |
| v1→v2 renumbering | anchor → heading number in v1 and v2 HTML | Safety = 5 (new); Apparatus 5→6, Test stand 5.1→6.1, Clamp 5.1.1→6.1.1, Procedure 6→7, Measurement 6.2→7.2, Test report 7→8; annex unchanged |
| C2 resolver outputs | each positive `file:line` and locator result checked against the source line and the XML element text | 15/15 lines and 18/18 locators land on the right element (clause levels 1–3, term, note, table row, list item, figure caption, annex) |
| C7.2 YAML | parsed `report.yaml`, `register.yaml` and `trace.yaml` with **Ruby Psych** (independent library) inside the pinned image under `--network none`, then reconciled against CSV and the resolved register | parses; 13 rows, 13 unique ids; type×disposition×MB counts YAML == CSV == register (10 cells). **This retires the builder's caveat "YAML not validated by an independent library."** |
| C7.3 links | every `v2/draft.html#…` href in `report.html` checked for an `id=` in v2 HTML | 8 distinct targets (10 rows), all present |
| C1.2 warnings | parsed `draft.err.html`; grepped compile logs | v1/v2: severity 0 none; severity 1: ISO_42 (our fictitious normative reference, explained), ISO_66 and ISO_121 (the latter on "Blandonnet 8" in injected ISO copyright boilerplate; the authored source has no digit-8 prose); severity 3 STANDOC_68. 0 errors |
| N1.3 untested paths | ran `prereqs.sh` with git removed from PATH, with python3 replaced, with `docker image inspect` failing, and with `MNSTD_FONT_CACHE=/nonexistent` | all exit 2, naming the missing item. **This closes the builder's "not self-tested" caveat for image, python and git.** |

### Tamper tests I wrote myself (`checks.run_all` on scratch copies of run-a)

| Tamper | Expected | Got |
|---|---|---|
| Untouched copy (green control) | all PASS | all PASS/N/A |
| PDF note loses its "MB/NC" and "type" text for one comment | C6.1 FAIL | **FAIL** |
| Semantic annotation date altered | C6.1 FAIL | **FAIL** |
| `Resolves:` trailers stripped from the merge (via `git replace`) | C4.4 FAIL | **FAIL** |
| Register `resolved_id` swapped between two rows | C3.2 FAIL | **FAIL** |
| Trace commit cell points at another real commit | caught | C5.4 **PASS**, N5.1 **FAIL** (caught by the N5.1 walk, not by C5.4) |
| v2 semantic XML loses an accepted change (`120 mm`→`80 mm`) after the run | C5.3 FAIL | C5.3 **PASS**: **not detected** |

---

## 4. Defects and caveats found in the rig (none changes a clause ruling)

1. **C5.3 checker trusts the pipeline's own computation.** `checks.c5` reads `trace/containment.json` written by
   `trace.py` and does not re-derive containment from the v2 XML. Post-hoc corruption of v2 therefore goes undetected
   (tamper above). The builder's own self-test only alters the *expectation*. Because I re-derived containment
   independently (§3, 10/10), C5.3 still PASSES on this artifact. **Fix for reuse:** recompute containment inside the
   checker.
2. **C5.4 checker only tests for blank cells.** It does not test whether the commit cell is the right commit. N5.1
   covers the gap, and I verified the cells myself.
3. **N5.2 exclusion is broader than disclosed.** Besides `dispositions/validation-bad.json` (`ZZ-99-999`),
   `intake/B/rejects.{csv,json}` carry the seeded rows' reviewer-local ids `DE-001…DE-011`, which are absent from the
   register. The checker's register-shaped regex cannot see them. Ruling in §5.
4. **The range is not visually rendered.** The PDF sticky note is a point at `from`, and the HTML glue shows only
   `data-to`. The span exists in the native annotation (`from`/`to`) but not as a visible extent in either output.
5. **Unexplained warnings in the review build.** It emits 22 severity-1 style warnings (for example ISO_66 "pr"
   lowercase, ISO_121/ISO_105) from the injected review text. C1.2 does not govern the review build, but they are not
   listed.
6. **Envelope items not captured by the rig.** These are the font-cache content digest (supplied in §2) and the in-image
   Asciidoctor version (attested 2.0.26).

---

## 5. Clause-by-clause ruling

Legend: **PASS** · **FAIL** · **N/A**. "Indep." = I verified it myself beyond the rig's checker.

### C1 #336 — governed by N1, N2, N3, N7, N8
| Clause | Ruling | Basis |
|---|---|---|
| C1.1 | PASS | Source read in full: foreword, intro, scope, normative refs, terms (3.1, 3.2), clauses 4–7, subclauses to level 3, 3 tables, 1 figure, 2 notes, annex A. Container compile exit 0, outputs xml/html/pdf present. Indep. |
| C1.2 | PASS | 0 errors. 4 err.html entries + 8 font substitutions listed and explained; the only source-attributable one (ISO_42) is explained. Indep. |
| C1.3 | **FAIL (literal)** | `@flavor=iso` and stage 30 / `stage-published=false`: PASS. Every element has an `@id`: PASS. **A number in the semantic XML: absent** (F3). Substantively met via the presentation XML. |

### C2 #335 — governed by N1, N2 (node text also says N3; no `About` edge exists; N3 passes anyway)
| Clause | Ruling | Basis |
|---|---|---|
| C2.1 | PASS | 18/18 locators (clause, subclause, term, para N, Table N, Figure N, Note N, annex A, A.1 Table A.1). Indep. |
| C2.2 | PASS | 15/15 lines across levels 1, 2, 3. Asciidoctor sourcemap run in-image. Indep. |
| C2.3 | PASS | 14/14 rejected with a reason, including `9.9`, `Table 7`, a header line and a past-EOF line. The rig's resolver has no nearest-match path. |
| C2.4 | PASS (within envelope) | A v2 with 10 edits and an inserted clause *before* clause 5: 42 unchanged + 8 edited elements mapped, 9 old→new pairs. Indep. renumbering check. **Anchoring policy (builder caveat):** accepted as a stated envelope, not as a defect. Structural elements carry author `[[anchors]]` (normal Metanorma practice). Unanchored paragraphs and lists align by text (exact, else difflib ≥0.6 within the matched parent). **Untested:** a heavy paragraph rewrite (<0.6 similarity would show as delete+insert), `include::` multi-file sources, and a source without author anchors. |

### C3 #334 — governed by N1, N2, N4, N5
| Clause | Ruling | Basis |
|---|---|---|
| C3.1 | PASS | 3 CSV sheets (alice GB, bob GB, claire FR): 2 MB/NC, 10 comments, ge/te/ed; one register (13 rows including PR). |
| C3.2 | PASS | 13/13 rows have `resolved_id` beside `locator`. Tamper (swapped id) detected. Indep. |
| C3.3 | PASS | 11 seeded rows (all 5 named cases + 6 more) rejected per row with reason; exit 1; register A == register B byte for byte. |
| C3.4 | PASS | `GB-001` clash between alice and bob resolved to `GB-01-001`/`GB-02-001`; ids unique; reviewer preserved. |

### C4 #332 — governed by N1, N2, N4, N5, N6
| Clause | Ruling | Basis |
|---|---|---|
| C4.1 | PASS | Local repo, tag v1, `change/apparatus-wording`; dave (DE) and erin (US) each have ≥1 comment line-anchored on the branch diff (erin's is ranged). |
| C4.2 | PASS | 3 PR comments in the register with the same field set, channel `pr`, source commit and line, and a C2.2 anchor. 2 seeded PR negatives rejected by the same validator, exit non-zero. |
| C4.3 | PASS | Change branch PASS and merged. 3 broken branches FAIL and are not ancestors of main (indep.). Two of them exit 0 and are caught only by the stated verdict rule, which the rig shows the W0 rule would have missed. |
| C4.4 | PASS | `git log --merges` trailers alone yield FR-01-002, PR-DE-01-001, PR-US-01-001 → `4f70611`. Tamper detected (mine). |
| C4.5 | PASS | No remote, `protocol.allow=never`, no network verbs in the trace, refusing shims for curl/wget/gh/commenter. Indep. |

### C5 #333 — governed by N1, N2, N3, N5, N7
| Clause | Ruling | Basis |
|---|---|---|
| C5.1 | PASS | 13 dispositions (6 accept, 4 modify, 3 reject), each with an observation, from both channels; the seeded bad record is rejected. |
| C5.2 | PASS | One commit per accept/modify id, referencing the id; rejects change nothing; the v1→v2 diff is fully attributable. Indep. |
| C5.3 | PASS | v2 compiles (exit 0, xml/html/pdf); containment 10/10 **re-derived by me**. The checker weakness is in §4.1. |
| C5.4 | PASS | 13 rows, no blank cell except the v2 columns of rejects. **Reject commit cell (builder caveat):** the sentinel `none (reject: no source change)` is not blank and states the truth that C5.2 requires (a reject *has* no commit). This satisfies the clause. |

### C6 #331 — governed by N1, N2, N3, N7
| Clause | Ruling | Basis |
|---|---|---|
| C6.1 | **FAIL (HTML leg)** | PDF: 13 native sticky notes with reviewer (`/T`), date (`/M`) and text, type/MB in the note body, attached at the resolved anchors: PASS (indep.). **HTML: native = 0; glue overlay ≠ Metanorma-native** (F4). Range: carried natively in `from`/`to`, not visibly rendered (§4.4). |
| C6.2 | PASS | R = X = P = H = 13, each id exactly once. My own PDF and XML counts agree. |
| C6.3 | PASS | Projection only; 0 hand-written blocks; clean build 0/0/0. Indep. |
| C6.4 | PASS | Stated: stage 30 (CD) + `:presentation-metadata-render-document-annotations: true` in the derived input; flag `true` in presentation XML; 26 `fmt-annotation-body`. "PDF renders regardless of stage" is attested (W4), and the run report says so. |

### C7 #330 — governed by N1, N2, N3, N4, N5, N6, N7
| Clause | Ruling | Basis |
|---|---|---|
| C7.1 | PASS | 13 rows, once each, ISO 2012-03 column order + Disposition + v2 location; byte-identical when regenerated from the resolved register. |
| C7.2 | PASS | HTML + YAML + CSV; counts reconcile; **YAML independently parsed (Psych)**. |
| C7.3 | PASS | 10/10 accept/modify rows link to v2 targets that exist (indep., 8 distinct ids). |

### NFRs
| Clause | Ruling | Basis |
|---|---|---|
| N1.1 | **FAIL (literal)** | See F1. The demonstrated part: from a fresh detached checkout on a provisioned host, one command regenerates every C1–C7 artefact with no manual step (my run). |
| N1.2 | PASS | Run B from clean: same 145-file artefact set; the mn2pdf debris cleanup is declared. |
| N1.3 | PASS | All prerequisite paths now exercised (builder: docker, fonts; me: image, python, git, fonts). |
| N2.1 | PASS | 24/24 container runs on the digest; digest verified locally. |
| N2.2 | PASS | `which ruby` and `which gem` exit 1; Ruby only in-container. |
| N2.3 | PASS | Python stdlib only (mechanical import scan, and I confirmed no network module); Node not used. |
| N3.1 | PASS | Identity set byte-identical across 6 runs and 3 invocations; normalization list empty and justified; never triggered. HTML and PDF are not in the set (not required). |
| N3.2 | PASS | Every inner-repo SHA is identical across runs; edits are literal unique find/replace. |
| N4.1 | PASS | All 8 ISO fields in the register, PR records and report; mapping documented. |
| N4.2 | PASS | ge/te/ed only (full words rejected); one comment per row. |
| N4.3 | N/A | DOCX not selected (Q1 default); stated in RESULT.md. |
| N5.1 | PASS | 100% walk, including all PR comments; the walk caught my wrong-commit tamper. |
| N5.2 | PASS (interpretation stated) | The register separates `id` (comment id) from `source_id` (reviewer-local id). Under the register's own schema, `DE-0xx` in the reject logs are source ids of rows that never became comments, and `ZZ-99-999` is the echoed input of the seeded-negative disposition record. No traceability artefact (register, PR records, trace, commits, review build, report) contains an id absent from the register. If the owner wants the literal reading, the rework is trivial: reference rejected rows by `file:row` only. |
| N6.1 | **FAIL (literal)**; gated demo network-free: **YES** | See F2 and §1 (R1). |
| N6.2 | PASS | No `commenter`/`github-*` in the trace (refusing shim); no remote. |
| N7.1 | PASS | 53 committed files, 442,725 bytes ≤ 5 MB; no HTML/PDF/XML/DOCX/archive in the tree; listed in `SNAPSHOT.md`. |
| N7.2 | PASS | No image or tarball committed (one 513-byte authored PNG input). |
| N8.1 | PASS (attested boundary) | Fictitious subject (glimmerwood); provenance note in the source header and `PROVENANCE.md`; the file was created in commit `7953833` by `factory-poc`. "Written by us" rests on git attribution, which is self-asserted. |
| N8.2 | PASS (attested boundary) | I read all 161 source lines. No clause text of any real standard. The only stock phrasing is generic ISO drafting formulae ("This document specifies…", "The test report shall include the following information"). Injected boilerplate is declared. There was no mechanical similarity check against real standards (none is possible offline). |

**Builder's "untested" items.** Cross-day determinism: untested, and not required by N3.1. Second machine: untested; I
record this in the envelope. Heavy rewrite and `include::`: C2.4 envelope. Whole-table-anchor PDF failure: attested,
not re-measured; this bears on #351 below, not on any clause. YAML independence: closed by me. N1.3 paths: closed by
me. N8 attestation: ruled above.

---

## 6. Recommended grades (input to the human's firewall ruling; I set none)

Rule applied: `proven` only if every own clause PASSES **and** every governing NFR (by `About` edge) PASSES on that
surface; otherwise `partial`, naming the clauses.

| Node | (A) Bar as written: **my recommendation** | Failing clauses | (B) If owner accepts fonts-as-environment (F1+F2) | (C) If owner also accepts F3 and F4 |
|---|---|---|---|---|
| C1 #336 | **partial** | C1.3; N1.1 | partial (C1.3) | proven |
| C2 #335 | **partial** | N1.1 | proven | proven |
| C3 #334 | **partial** | N1.1 | proven | proven |
| C4 #332 | **partial** | N1.1, N6.1 | proven | proven |
| C5 #333 | **partial** | N1.1 | proven | proven |
| C6 #331 | **partial** | C6.1 (HTML); N1.1 | partial (C6.1-HTML) | proven |
| C7 #330 | **partial** | N1.1, N6.1 | proven | proven |
| N1 #337 | **partial** | N1.1 | proven | proven |
| N2 #338 | **proven** | — | proven | proven |
| N3 #339 | **proven** | — | proven | proven |
| N4 #340 | **proven** | — (N4.3 N/A) | proven | proven |
| N5 #341 | **proven** | — (N5.2 interpretation stated) | proven | proven |
| N6 #342 | **partial** | N6.1 (literal) | proven | proven |
| N7 #343 | **proven** | — | proven | proven |
| N8 #344 | **proven** | — (authorship attested) | proven | proven |

The blocker for every `partial` above is **not evidence quality**. It is bar wording against toolchain and
environment facts: fonts are not in the image, the semantic XML has no numbers, and ISO HTML does not render annotations.

### Technologies (the artifact demonstrates them on the gated path)
| Node | Recommend | Clauses carried | Envelope / limits |
|---|---|---|---|
| #349 image @ digest + metanorma-iso 3.5.14 | **proven** | C1.1, C1.2, C4.3 (compile step), C5.3 (compile), C6 (PDF) | digest above; x86_64; `metanorma compile -t iso --agree-to-terms --no-install-fonts -x xml,html,pdf,rxl`, root then chown, `--network none`, `SOURCE_DATE_EPOCH=1794528000`; font cache digest `03f4d031…f968` (unpinned upstream content). Its stated limits were observed in this run: no fonts, exit code misses broken sources, no commenter. |
| #350 resolver glue | **proven** | C2.1–C2.4, C3.2, C4.2, C5.3 | single-file source; author-anchored structural elements; difflib ≥0.6 for unanchored text; sourcemap via in-image Ruby (Asciidoctor 2.0.26 attested). Untested: heavy rewrite, `include::`. |
| #351 native annotations → PDF (+ HTML glue) | **partial** | C6.2, C6.3, C6.4, C6.1-PDF | Demonstrated: `[reviewer,date,from,to]`+`****` → semantic `<annotation>` → 13 PDF `/Text` notes with `/T`, `/M`, `/Contents`; HTML glue works *as glue*. **Not demonstrated by us** (attested from W4): the switch gating only Word/presentation, the PDF ignoring stage, whole-table and whole-list anchor failures, and the dangling-`from` crash. |
| #352 local git review & attribution | **proven** | C4.1–C4.5, C5.2, N3.2 | git 2.55.0 (≥2.32); fixed identity and synthetic clock. **The node should record the refined gate verdict rule:** FAIL iff exit≠0 OR no XML OR any `asciidoctor: ERROR/WARNING/FATAL` OR any severity 0/1 err.html entry not present in the main@v1 baseline. The W0 exit-or-sev0 rule passed 2 of 3 broken branches. |
| #353 ISO 2012-03 template schema + validator/register/report glue | **proven** | C3.1–C3.4, C5.1, C7.1–C7.3, N4.1, N4.2 | Python 3.14 stdlib; YAML output verified parseable by an independent parser (Psych). |
| #354 metanorma/commenter 0.7.0 | **claimed (no change)** | none | Not on the gated path (refusing shim); the artifact does not demonstrate it. |

---

## 7. What would clear this gate

1. **Owner rulings** (no compute): (a) whether one-time font provisioning counts as environment, like the image pull,
   for N1.1 and N6.1; (b) whether C1.3 "semantic XML" admits the presentation XML of the same compile; (c) whether glue
   HTML from native annotation data satisfies C6.1, given that the node's `why` excludes "a bespoke overlay". Record
   these as a dated Extension (D3) or a `context_correct` of the node text. Grades then follow column (B) or (C) above
   with **no re-run needed**: the evidence already covers them.
2. **If the owner holds N1.1 literal but amends N6.1:** one bounded POC rework (REWORK 1 of 2). `make demo`
   self-provisions the image (pull by digest) and fonts when they are absent. Show it on an empty `MNSTD_FONT_CACHE`
   from a fresh `git clone`. Ideally, pin or hash the font set.
3. **Recommended for reuse, but no clause depends on it:** recompute containment inside the C5.3 checker (§4.1).

*Gate reports are coordination artifacts (§14.3). This file is not graph knowledge, and it moves no grade.*
