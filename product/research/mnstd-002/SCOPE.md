# mnstd-002 — Validated: ISO-style Metanorma authoring and commenting cycle, proven by one integrated prototype

**Status:** synthesis (2026-11-13)
**Goal(s):** `mnstd` (primary, **#329**)
**Capability target(s):** all seven business capabilities on the mnstd board, as workstreams of this ONE scope:
C1 **#336** · C2 **#335** · C3 **#334** · C4 **#332** · C5 **#333** · C6 **#331** · C7 **#330**.
Governing NFRs, re-verified across their governed surface at the firewall: N1 **#337** · N2 **#338** · N3 **#339** ·
N4 **#340** · N5 **#341** · N6 **#342** · N7 **#343** · N8 **#344**. All 15 are `grade:missing` at scope open.
**Confidence-required:** **validated** (owner, binding: `product/research/mnstd-001/OWNER-BRIEF.md`)
**Phase / area:** standards authoring · document review/commenting · docs-as-code
**Cycle topic / Issue:** `mnstd-002` · GitHub Issue dug-21/arch-research#74
**Board source:** `product/research/mnstd-001/DECOMPOSITION.md` (§3 caps, §4 NFRs, §7 D9 plan, §8 Q1–Q9) ·
id map `product/research/mnstd-001/BOARD.md`. `done_when` text below is taken from the **stored Unimatrix
nodes** (read 2026-11-13 via `context_graph(mode:"subgraph", seed_ids:[329], max_depth:1,
edge_types:["Advances"], direction:"incoming", detail:"full")`); where node and DECOMPOSITION.md differ, the node governs.

**One scope, not seven (owner instruction).** The owner brief authorizes one validated research-scope covering
the separate capabilities as workstreams, with no fan-out into separate runs. This scope covers C1–C7 as
workstreams W0–W4 (the D9 plan). The feasibility phase builds **ONE integrated, reproducible prototype**: a
Makefile/script that runs the whole cycle end to end. It lives under `product/research/mnstd-002/poc/` on branch
`research/mnstd-002` (D15: executables on the branch, research documents on `main`).

---

## The question

The owner wants to *see* ISO-style standards authoring and commenting/review working in Metanorma, by a
prototype we build and run. mnstd-001 split that into a 7-capability chain (C1 compile → C2 anchor resolver →
C3 intake → {C4 PR channel, C5 disposition → C7 report, C6 annotated render}) with 8 NFRs. This scope finds,
for each link, the native Metanorma feature or thinnest glue that clears it, and then proves the whole chain
in one artifact.

> Can an ISO-flavor Metanorma draft, run through one reproducible Docker-plus-glue pipeline we build, clear
> every `done_when` clause of C1–C7 and N1–N8: intake validated against the document, a traced v2, PR-channel
> review, native review annotations, and a disposition report?

## Why it matters

This is the firewall step for the whole `mnstd` goal. Its claim-floor is C1–C7 plus N1–N8 proven, all
threshold, with no curve or keystone. mnstd-001 produced structure only, and every Metanorma behavior it names
is a doc-claim. Nothing in the library covers standards authoring or document review (prior art below), so the
technologies this scope grades are the first nodes of a new region of the library. The owner preference is
**assembly over build**: each workstream must first establish what Metanorma natively offers.

## Known constraints & prior art  *(build on these — do not re-derive)*

**Unimatrix library: no reusable technology.** mnstd-001 ran six searches across technology, goal, capability
and finding and found no domain match (DECOMPOSITION.md, prior-art table). Re-checked 2026-11-13
(`context_search` category `technology`, "metanorma ISO comment sheet review annotation AsciiDoc compile
docker"): top hits #198 gh-aw, #316 metaharness, #258, #189, all workflow-harness and relevance ≤0.28. **No
reuse.** #198 is agentic CI rather than document review, and the owner restricts PR work to local simulation.

**Board decisions to inherit (mnstd-001, do not reopen):**
- **One comment register, two intake channels** (D6/Q2). C4 defines no schema. PR comments normalize into the C3 register.
- **C2 is the determining constraint** (D2). If C2 fails, rule W1–W4 *blocked*, not failed (D9 §7).
- **Comment → native review block projection belongs to C6**, as a render-time transformation. Intake never mutates the v1 source (D4).
- **No hard edge C4↔C5.** C5 is provable without the PR channel. If C4 is present, C5.1 needs both channels in the fixture.

**Owner questions Q1–Q9: proceeding on the recorded defaults** (owner pre-authorized; DECOMPOSITION.md §8):
Q1 report = HTML plus YAML/CSV register in ISO column order (DOCX via `commenter fill` is an ungated stretch) ·
Q2 one register · Q3 `line` optional and informational, with clause plus element authoritative (promote if W0
finds draft line numbering) · Q4 edits applied by script from the disposition record · Q5 plain git plus
review-record files (a local forge is acceptable only if cheap) · Q6 tool-injected ISO boilerplate acceptable
and declared · Q7 dispositions exactly `accept|modify|reject` · Q8 no Word draft output · Q9 no north-star.

**Environment (measured by research-leader, 2026-11-13):**
- Host is `x86_64`. This retires mnstd-001's CPU-architecture flag.
- `metanorma/metanorma:latest` is already pulled: digest
  `sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da`, 2.52 GB. N2.1 requires the
  prototype to pin **by digest**, not by `latest`. The digest above is the candidate pin.
- No Ruby locally (the N2.2 precondition holds). Node 24 and Python 3.14 are available for glue.

**Doc-claim candidates to evaluate (unverified; from mnstd-001 light grounding):**
- Metanorma reviewer notes: `[reviewer=…,date=…,from=…,to=…]` plus a `****` sidebar anchored to `[[id]]`. `TODO`
  admonitions become reviewer notes. Notes render only at unpublished or draft stages. The override is
  `:presentation-metadata-render-document-annotations:`. Source is older metanorma-standoc docs, **possibly stale**.
- `metanorma/commenter`: `import` (DOCX/XLSX→YAML), `validate` (appears schema-only, with no anchor-vs-document
  check), `merge`, `fill` (DOCX template), `stats`, `github-create` (**forbidden against live repos**, N6.2).
- ISO commenting template: no structural modification and one comment per row (doc-claim; not independently re-read).
- **Unknown:** whether metanorma-iso draft output carries line numbers (searched, not found; absence not proven).

## Bounded investigation (workstreams)

Each workstream is one `factory-researcher` partition in tech-discovery. All are spawned in parallel.
Researchers are read-only, may consult docs, source and READMEs, and **run nothing**. Running is
feasibility's job, done by `factory-poc`. Every behavioral claim must be labeled doc-claim or
demonstrated (by others, with a link). Each workstream ends with an **assemble / build** call per capability and
a concrete **POC recipe** (inputs, commands, expected observable) for its clauses.

- **W0 — Foundations (C1 #336, C2 #335). Determining constraint.** What is the current metanorma-iso AsciiDoc
  document model? Cover the minimum header and attributes for a draft stage, section types (foreword, scope,
  normative references, terms, clauses, annex), table, figure and note syntax, and the `metanorma compile`
  invocation inside the container (flags for HTML, PDF and XML output, and where outputs land). What does the
  semantic XML look like? Cover the ISO flavor/root metadata, the document-stage element, element `id`
  generation (author `[[anchor]]` vs auto-generated, and whether auto ids are stable across compiles), and
  where clause, table and figure numbers appear (in the semantic XML or only in the presentation XML). How can a
  resolver map (a) an ISO locator (`5.2` + `para 2` / `Table 1` / `Figure 2` / `Note 1`, annex) → exactly one
  element id, (b) an AsciiDoc `file:line` → enclosing element (is there a sourcemap, or must the resolver parse
  the source itself?), and (c) v1 element → v2 element under renumbering (C2.4)? Do any line numbers exist in
  draft output (Q3)? Also cover image pinning by digest and known compile warnings for a minimal ISO doc.
  *Output:* `product/research/mnstd-002/findings-W0.md`: document-model and compile recipe, XML anchor/number
  map, resolver design options ranked (assemble vs build) with the stability strategy for C2.4, a Q3 verdict
  (doc-claim), and environment notes.
- **W1 — Intake (C3 #334).** Assemble or build? Assess `metanorma/commenter` (current state, maintenance,
  YAML schema, field names vs the ISO template, `validate` and `merge` behavior, whether it runs in the
  `metanorma/metanorma` image or needs its own Ruby, which would breach N2.2 if run on the host) against a
  custom CSV/YAML schema validated in Node or Python. How does validation call the C2 resolver? How are ids
  kept collision-free across reviewers (C3.4)? Cover the seeded-invalid-row fixture design (C3.3: non-existent
  clause, unresolvable element locator, type `xx`, missing comment text or MB/NC, duplicate id) and the N4
  field mapping. *Output:* `product/research/mnstd-002/findings-W1.md`: register schema (ISO template column
  order, documented mapping), a commenter assemble/build verdict with evidence class, validator design, and
  fixture spec.
- **W2 — Resolution (C5 #333).** How should dispositions be recorded (`accept|modify|reject` plus a
  mandatory observation)? How does a script apply `proposed_change` / modified text to AsciiDoc
  deterministically (Q4/N3), with one commit per comment id? How is "no unattributed change" verified on the
  v1→v2 diff (C5.2)? How does C5.3 check mechanically that the v2 element (reached via C2.4) contains the change?
  Cover the trace-table shape (C5.4) and the N3 volatile-field normalization list for v2 semantic XML.
  *Output:* `product/research/mnstd-002/findings-W2.md`: disposition record schema, edit-application
  mechanism (ranked), diff-attribution check, v2 containment check, trace-table spec, and N3 normalization candidates.
- **W3 — Git/PR review (C4 #332).** How does Metanorma's GitHub practice (compile-on-PR CI, review on AsciiDoc
  diffs) map to a **local-only** simulation? Choose a medium (Q5): plain git plus review-record files vs a local
  forge container, judged on cost and the N6 risk. Cover the review-record format that carries reviewer,
  commit, `file:line` and an ISO type, normalized into the C3 register with channel `pr`. Cover the pre-merge
  check (C4.3: compile the branch head via C1, record pass or fail, with a seeded broken-source branch that must
  fail and not merge), the merge-commit convention carrying comment ids so that `git log` alone yields comment
  id → merge commit (C4.4), and proof of no remote (C4.5/N6). *Output:*
  `product/research/mnstd-002/findings-W3.md`: medium verdict, review-record schema, branch/merge
  conventions, pre-merge gate recipe, and N6 check recipe.
- **W4 — Review output (C6 #331, C7 #330).** What is the **current** reviewer-note / annotation syntax and
  rendering rule in metanorma-iso? Re-verify the stale doc-claims: the attributes, the from/to range, the
  draft-stage rule, and the render override name. Which semantic XML element represents an annotation (for
  C6.2's count)? How is the register projected into a derived v1 build input without touching the committed
  source, and how does a clean build differ (C6.3)? Can type and MB be made visible? For C7: generate the report
  from the register only (ISO column order plus disposition plus v2 location), HTML plus YAML/CSV (Q1), with
  count reconciliation by type × disposition × MB (C7.2) and v2-location existence checks (C7.3). Is
  `commenter stats`/`fill` usable as an assemble candidate (DOCX stays an ungated stretch)? *Output:*
  `product/research/mnstd-002/findings-W4.md`: annotation syntax and rendering verdict (doc-claim vs
  demonstrated-by-others), projection mechanism, annotation-count oracle, report generator design, and C7.2/C7.3 check recipes.

## Expected output

1. Five findings files (`findings-W0.md` … `findings-W4.md`). The curator distills them into `technology` nodes
   (`grade:claimed`, `Prerequisite→` the capability) and `finding` nodes (`Motivates`, with structured `cites:`), tagged `mnstd-002`.
2. **One integrated prototype**, `product/research/mnstd-002/poc/`, on branch `research/mnstd-002`. One command
   (`make demo` or an equivalent script) runs, from a clean state: the v1 compile → the resolver fixture → intake
   plus the seeded-invalid fixture → the PR-channel simulation in a local git repo → dispositions → scripted
   edits → the v2 compile → the trace table → the annotated v1 review build plus the clean v1 build → the
   disposition report → the NFR checks (second run, determinism diff, no-remote and command trace, footprint,
   `which ruby`). It contains a sample fictitious ISO-flavor draft (N8 provenance note) and a comment sheet from
   ≥2 simulated reviewers. Generated HTML, PDF and XML are **not committed** (N7). Only a listed evidence
   snapshot within budget is committed.
3. A run report (`poc/RUN-REPORT.md` or equivalent) with a per-clause evidence pointer for every clause in the
   proof bar below. It also records the image digest, the warnings list (C1.2), the annotation mechanism used
   (C6.4), the N3 normalized-field list with justification, and the N7 snapshot listing.
4. An independent `factory-validator` gate report, ruling clause by clause.
5. Synthesis: the `position` finding, `REPORT.md`, capability grades moved by the curator per the firewall, and
   the goal-owner relevance review.

## Proof bar  *(validated: what would move status)*

**Altitude: integration**, so the smoke test is the end-to-end run of the one prototype, **demonstrated by
us**. Literature and citations never prove anything. They stay `claimed`. Grade rules:
- A **capability** goes to `proven` only when **every** `done_when` clause below is ruled PASS by the
  independent `factory-validator` on the artifact, and every NFR that governs it (its `About→` edges) passes on
  that surface. If some clauses pass and others do not, the capability is `partial`, and the failing clause ids
  are named. An honest `partial` beats an inflated `proven`.
- A **technology** (e.g. the pinned image, metanorma-iso, reviewer notes, `commenter`, the resolver glue) goes
  to `proven` / `partial` with `proven_by` carrying the envelope: image digest, host arch, command, and the
  clauses it carried.
- `proven` is set by `factory-curator` via `context_correct` with `proven_by` attached, in the same step as
  `grade:proven`. It is never set by a bare `context_tag`. FIREWALL is blocking: REWORK ≤2, then SCOPE-FAIL.
- **Dependency rule:** a clause that cannot be evaluated because an upstream capability failed is ruled
  BLOCKED, not FAIL. This applies above all when C2 fails and W1–W4 are blocked.

Clause register. Each clause is ruled against the stored node's `done_when`, quoted in short form here; the node text governs.

### C1 #336 — ISO-flavor draft compiles reproducibly to HTML, PDF and semantic XML
| Clause | Requirement (node) | Evidence the validator checks |
|---|---|---|
| C1.1 | metanorma-iso AsciiDoc sample with foreword, scope, normative refs, terms and definitions, ≥3 numbered clauses incl. ≥1 subclause level, ≥1 table, ≥1 figure, ≥1 note, ≥1 annex; compiles via the `metanorma/metanorma` container to HTML, PDF and semantic XML with exit 0 | source inspection + compile log + exit code + the three outputs exist |
| C1.2 | compile log reports zero errors; any warnings listed in the run report, with none attributable to authored source left unexplained | log + run-report warnings list |
| C1.3 | semantic XML shows ISO flavor (root/flavor metadata) and a draft stage; contains every authored clause, table and figure with a machine-readable id and number | XPath checks on the XML |

### C2 #335 — Any location resolves to exactly one element *(determining constraint; prove first)*
| Clause | Requirement (node) | Evidence |
|---|---|---|
| C2.1 | ISO locator (clause/subclause number, or number + `para N` / `Table N` / `Figure N` / `Note N`) → exactly one element id in v1 semantic XML, for every locator in a fixture covering clauses, subclauses, paragraphs, tables, figures and an annex | resolver fixture run, results table |
| C2.2 | AsciiDoc `file:line` → enclosing element id + clause number, verified for ≥10 fixture lines across ≥3 clause levels | fixture run, results table |
| C2.3 | non-existent or ambiguous locators (e.g. `9.9`, `Table 7` when only 2 exist, a document-header line) rejected with a stated reason, never silently mapped | negative-fixture run |
| C2.4 | after a v2 that edits ≥3 elements and inserts ≥1 new clause *before* existing ones, every unchanged v1 element resolves to its v2 counterpart; renumbering reported as old→new pairs | v1/v2 mapping output vs fixture |

### C3 #334 — Validated, clause-anchored comment intake
| Clause | Requirement (node) | Evidence |
|---|---|---|
| C3.1 | CSV or YAML sheet from ≥2 simulated reviewers (≥2 distinct MB/NC), ≥8 comments spanning `ge`, `te`, `ed`, ingested into one register (the record set C4, C5 and C7 also read) | sheets + register |
| C3.2 | every valid row accepted with its anchor resolved via C2 to an element id; register records resolved id next to the original locator | register fields |
| C3.3 | seeded-invalid fixture rejected per row with reason; validator exits non-zero; no seeded row enters the register. Fixture includes non-existent clause, unresolvable element locator, type `xx`, missing required field (comment text or MB/NC), duplicate id | validator output + exit code + register diff |
| C3.4 | separate reviewer sheets merge into one register with no id collisions, originating reviewer preserved | register inspection |

### C4 #332 — Git/PR review feeds the same register
| Clause | Requirement (node) | Evidence |
|---|---|---|
| C4.1 | local git repo with v1 source; ≥2 simulated reviewers each produce a review, ≥1 per reviewer line-anchored to a change branch's AsciiDoc diff; ≥1 change-proposal branch exists | repo state + review records |
| C4.2 | each PR comment normalized into the C3 register with the same fields, an ISO type, an anchor resolved via C2.2 from `file:line`; marked channel `pr` with source commit and line; a comment on an unresolvable line rejected exactly like C3.3 | register rows + negative case |
| C4.3 | pre-merge check compiles the branch head via C1 and records pass or fail; a seeded broken-source branch fails and is not merged | check log + `git log` |
| C4.4 | merged change carries the resolved comment id(s) in its merge commit; `git log` alone lists comment id → merge commit for every PR-resolved comment | `git log` extraction |
| C4.5 | no remote contacted: repo has no network remote; no external PR, issue or Action created | `git remote -v` + command trace |

### C5 #333 — Disposition loop produces a traced v2
| Clause | Requirement (node) | Evidence |
|---|---|---|
| C5.1 | every register comment gets exactly one disposition from `accept|modify|reject` with a non-empty observation; fixture has ≥1 of each, and comments from both channels if C4 is present | disposition record |
| C5.2 | each `accept`/`modify` changes the AsciiDoc source by a commit referencing the comment id; `reject` produces no source change; v1→v2 source diff contains no change not attributable to a comment id | git history + diff-attribution check |
| C5.3 | v2 compiles via C1 to HTML, PDF and XML; for each accept/modify, the v2 element reached via C2.4 contains the change, checked mechanically against `proposed_change` (accept) or recorded modified text (modify) | v2 outputs + containment check |
| C5.4 | trace table, one row per comment: id → disposition → commit → v1 element/clause → v2 element/clause; no blank cell except v2 for `reject` | trace table |

### C6 #331 — Rendered v1 review draft with native annotations
| Clause | Requirement (node) | Evidence |
|---|---|---|
| C6.1 | v1 review build in HTML and PDF shows every register comment as a Metanorma-native reviewer annotation (reviewer, date, comment text, type/MB visible), attached at the resolved element, spanning from→to where a range was given | rendered outputs + XML |
| C6.2 | rendered annotation count = register comment count, checked against the semantic XML annotation elements, not by eye | count script |
| C6.3 | annotations produced by projecting the register into the build input; committed v1 source has no hand-written review blocks; a "clean" v1 build from the same source shows none | source grep + clean-build count = 0 |
| C6.4 | native rendering rules respected and stated; run report records the mechanism that made annotations visible (draft stage, or the render-annotations override) | run report |

### C7 #330 — Disposition report
| Clause | Requirement (node) | Evidence |
|---|---|---|
| C7.1 | every register comment listed exactly once, in ISO template column order (MB/NC, line, clause/subclause, paragraph/figure/table, type, comment, proposed change, observations of the secretariat), plus disposition and the v2 location from C5.4; generated from the register only, no hand edits | report + generator trace |
| C7.2 | emitted in the Q1 format (default HTML plus machine-readable YAML/CSV); counts by type × disposition × member body match the register | reconciliation check |
| C7.3 | every `accept`/`modify` links or refers to its v2 location, and that location exists in the v2 build | link/existence check |

### NFRs (ruled across their governed surface — `About→` targets in brackets)
| Clause | Requirement (node) |
|---|---|
| N1.1 [C1–C7] | fresh clone with only Docker, Node 24, Python 3.14: one command regenerates every C1–C7 artefact, no manual step |
| N1.2 | second run from a clean state succeeds with the same artefact set |
| N1.3 | any missing prerequisite → fail-fast error naming it |
| N2.1 [C1–C7] | all Metanorma compilation inside `metanorma/metanorma` pinned by digest (or an immutable tag recorded with its digest) |
| N2.2 | succeeds with no Ruby or gem on host, checked by `which ruby` failing |
| N2.3 | host glue only Node 24 or Python 3.14 with declared, pinned dependencies |
| N3.1 [C1, C5, C6, C7] | two runs with identical inputs → identical register, trace table and report; v2 semantic XML identical after normalizing a declared, justified volatile-field list |
| N3.2 | the edit-application path (Q4) has no non-deterministic step in the gated run |
| N4.1 [C3, C4, C7] | register, PR records and report carry every ISO template field; none dropped or renamed without a documented mapping |
| N4.2 | one comment per row or record; type vocabulary exactly `ge`/`te`/`ed` |
| N4.3 | if DOCX output is selected (Q1), the template structure is unaltered. **N/A under the Q1 default** (DOCX not selected); the run report must state this |
| N5.1 [C3, C4, C5, C7] | for a random ≥50% sample plus every PR-channel comment, the validator follows locator → v1 element → disposition → commit → v2 element → report row using only emitted artefacts and git history |
| N5.2 | no artefact contains a comment id absent from the register |
| N6.1 [C4, C7; property applies to whole demo] | no PR, issue, Action, push or publication on any external service; only network access is the image pull |
| N6.2 | `commenter github-*` or any equivalent not invoked against a live repo, checked by command trace and remote inspection |
| N7.1 [C1, C5, C6, C7] | generated HTML/PDF/XML/DOCX not committed; any committed evidence snapshot ≤ stated budget (proposed 5 MB total) and listed |
| N7.2 | no container image or tarball committed |
| N8.1 [C1] | authored body text written by us on a fictitious subject, with an authorship/provenance note |
| N8.2 | no clause text reproduced from a real ISO standard; tool-injected metanorma-iso boilerplate excluded and declared (Q6) |

## Explicitly out of scope

- Other Metanorma flavors (IEC, ITU, OGC, IETF, …) and non-ISO comment models.
- Real ISO process integration: OSD/eBalloting, national-body voting, and real ISO standard text.
- Any external side effect: PRs, issues or Actions on any external or live repo; `commenter github-create`
  against a live repo; pushing the prototype's inner git repo anywhere; publishing beyond Issue #74 in
  dug-21/arch-research.
- Production concerns: multi-user UI, access control, a hosted review service, scale.
- Word fidelity beyond Q1/Q8 defaults: DOCX report (`commenter fill`) and Word draft output are ungated stretches at most.
- An agent-applied edit path as the *gated* path (Q4). It may be shown, but it is not ruled.
- Re-deciding the board (granularity, channel model, edges). A discovered gap is a frontier change (D3):
  either a dated Extension here (in-envelope) or a new `missing` capability node plus a new scope.
- Benchmarking performance or compile time. Nothing on the board asks for it.

## Coverage / done call

**Tech-discovery (blocking, loop-until-dry): K = 3, N = 2, per workstream.** A workstream is dry when **3
consecutive targeted searches** surface no new candidate technology or mechanism for its capabilities, **and ≥2
independent findings** (distinct sources: e.g. official docs plus source code or a maintained example repo)
corroborate the leading candidate for each of its clauses' mechanisms. A workstream with no assemble candidate
may close on a **build** verdict once K is met. That counts as dry, not as a gap. The scope is covered when W0–W4
are all dry. The agent proposes "sufficient". The owner pre-authorized the human confirm, but the gate remains
blocking and its artifact is still produced. REWORK ≤2 → SCOPE-FAIL.

**Validated done call:** the scope is done when the firewall gate has ruled every clause above (PASS, FAIL,
BLOCKED or N/A with reason) on the one prototype, the curator has moved grades accordingly (`proven` only on
all-clause PASS plus governing NFRs), and synthesis is reviewed. **Order of proof:** W0/C2 first. If C2
cannot be made to pass, feasibility stops at an honest `partial` / `blocked` record rather than building W1–W4
on an unproven resolver.

## Flags

- **`latest` vs digest:** the pulled image is `:latest`. N2.1 is satisfied only if the prototype references the
  digest above (or an immutable tag recorded with that digest). A later `docker pull` silently changes `latest`.
- **Line numbers (Q3)** remain unknown. If W0 finds draft line numbering, Q3's default is promoted and C2/C3 fixtures gain a `line` resolver case.
- **Reviewer-note syntax may be stale** (older standoc docs; current metanorma.org URLs returned 404 in mnstd-001). C6 rests on W4 re-verifying it.
- **`commenter` needs Ruby.** If it is not in the image, using it on the host would breach N2.2. Running it inside the container is the only N2-clean assembly.
- **N6 About edges** are written only to C4 and C7 (BOARD.md). The property is still ruled across the whole demo, per node #342's own text.
- **Fixture sizes** (≥8 comments, ≥10 lines, 5 MB) are researcher proposals carried in the nodes, not owner numbers.

## Extension — 2026-11-13 (tech-discovery leader rulings; append-only, D3, in-envelope)

Recorded by factory-curator for research-leader. No proof bar, clause or NFR text above is changed.

- **R1 — N6.1 vs PDF fonts.** The pinned image ships no fonts; a PDF compile needs a one-time networked font
  fetch (findings-W0 §5, findings-W4 §4). **Ruling:** the POC provides a separate one-time `make fonts`
  provisioning step (font cache gitignored, never committed). The gated `make demo` must run every compile with
  `--network none` and make no other network access. **The N6.1 text is NOT amended:** the validator rules N6.1
  on its literal text AND states separately whether the gated demo is network-free. The discrepancy is flagged
  to the owner.
- **R2 — C6.1 HTML.** Native metanorma-iso 3.5.14 HTML renders no reviewer notes (findings-W4 §0.3); the PDF
  renders native annotations. **Ruling:** the POC may inject HTML annotations from the native semantic
  `<annotation>` data, labelled as glue. The validator rules whether that satisfies C6.1's wording. No bar change.
- **R3 — Defaults and git.** Proceed on the Q1–Q9 defaults as recorded. Host `git` is added as a declared
  prerequisite with a fail-fast check (findings-W3 §6). This is a prerequisite declaration, not a bar change.

## Extension (2026-11-13): owner firewall rulings (verbatim)

**Owner firewall rulings for mnstd-002** (genuine human input, 2026-11-13; relayed verbatim by the coordinator to research-leader):

1. **N1.1 / N6.1 — YES.** The one-time font download (`make fonts`) is environment setup, equivalent to the image pull. Condition: pin the fonts (version + checksum manifest, verified by `make fonts`) as a follow-up. Do it in this run if it's cheap; otherwise log it as a tracked follow-up on the Issue.
2. **C1.3 — YES.** Clause numbers in Metanorma's presentation XML, joined by element id, satisfy C1.3. That's Metanorma's native layering, not our addition.
3. **C6.1 (HTML half) — NO.** HTML notes added by our script are the excluded bespoke overlay. C6 stays `partial`. Record the finding honestly: Metanorma ISO HTML does not render native review notes; PDF does.

Required before merging PR #75: fix the C5.3 checker so it actually recomputes its result (it must fail when an accepted change is removed from v2), add that case as a tamper test, and have the factory-validator (independent, not the builder) confirm the fix. A spot-check of the changed clause is enough; no full re-gate needed.

These rulings supersede the leader rulings R1/R2 above where they differ (R1: N6.1 now ruled satisfied by owner; R2: glue HTML ruled NOT to satisfy C6.1). Recorded on Issue #74 before any grade moved.
