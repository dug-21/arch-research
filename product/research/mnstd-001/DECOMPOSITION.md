# mnstd-001: Decomposition (capability board proposal)

**Run:** `mnstd-001` (decompose-scope, phase `decompose`) · **Author:** `factory-researcher` (read-only; no graph writes)
**Inputs:** `SCOPE.md`, `OWNER-BRIEF.md`, methodology §4–§6, `.claude/rules/unimatrix-access.md`, `uni-capability` skill.
**For:** `factory-curator` (distils to the graph) and the decompose advisory gate (owner pre-authorized).
**Status of everything below:** structure only. Every Metanorma behaviour named here is a **doc-claim**: it
comes from public docs or READMEs and nothing was run. No node is `partial` or `proven`.

> Path note: SCOPE.md names the output `decomposition.md` (lowercase). The leader's tasking names
> `DECOMPOSITION.md`, and this file follows the leader. The curator should cite this path.

---

## 0. Board at a glance

| id | kind | name (outcome) | owner demo | grade | Prerequisite of (→) |
|---|---|---|---|---|---|
| **C1** | business | ISO-flavor draft compiles reproducibly to HTML, PDF and semantic XML | baseline | missing | C2 |
| **C2** | business | Any location in the draft is addressable and resolves to exactly one element | baseline (hidden prereq) | missing | C3 |
| **C3** | business | Validated, clause-anchored comment intake | **demo 1** | missing | C4, C5, C6 |
| **C4** | business | Git/PR review of the AsciiDoc source feeds the same comment register | **demo 3** | missing | — |
| **C5** | business | Disposition loop produces a traced v2 | **demo 2** | missing | C7 |
| **C6** | business | Rendered v1 review draft shows every comment as a native Metanorma annotation | **demo 4a** | missing | — |
| **C7** | business | Disposition report (compiled comments + observations) | **demo 4b** | missing | — |
| **N1** | nfr | One-command reproducible demo | — | missing | About→ C1–C7 |
| **N2** | nfr | Contained, pinned toolchain (Docker-only Metanorma) | — | missing | About→ C1–C7 |
| **N3** | nfr | Deterministic regeneration | — | missing | About→ C1, C5, C6, C7 |
| **N4** | nfr | ISO comment-template field fidelity | — | missing | About→ C3, C4, C7 |
| **N5** | nfr | End-to-end comment traceability | — | missing | About→ C3, C4, C5, C7 |
| **N6** | nfr | No external side effects | — | missing | About→ C4, C7 (and all) |
| **N7** | nfr | Lean repository footprint | — | missing | About→ C1, C5, C6, C7 |
| **N8** | nfr | Original sample content (no ISO copyrighted text) | — | missing | About→ C1 |

**Counts:** 7 business capabilities and 8 NFRs. There are 6 `Prerequisite` edges, 15 `Advances` edges and 32 `About`
edges (enumerated in §5). Every owner demonstration maps to at least one capability (§6).

**Archetype:** all 15 nodes are **threshold**. There are no curve capabilities and no keystone ruler. The goal's
**claim-floor is C1–C7 plus N1–N8**. A north-star is not set, because the owner asked for a prototype and not an
improving service (see owner question Q9).

---

## 1. Goal node (`mnstd`)

```
category: goal
name:     Prove an ISO-style Metanorma authoring and commenting cycle with a prototype we build and run.
intent:   The owner wants to see how standards authoring and commenting/review work in Metanorma,
          shown by a working prototype rather than described. Nothing in the library covers standards
          authoring or document review, so this goal opens a new demand map. Assembling Metanorma's
          native features is preferred over building new ones.
success:  Demonstrate, with a reproducible prototype we build and run ourselves, that an ISO-flavored
          standard authored in Metanorma AsciiDoc (metanorma-iso) can go through a complete ISO-style
          commenting cycle: clause-anchored comment intake validated against the document, a
          disposition loop that regenerates a traced v2, Git/PR-based review of the AsciiDoc source,
          and rendered HTML/PDF review output that carries Metanorma's native review blocks plus a
          disposition report.
          Claim-floor: C1–C7 and N1–N8 proven (all threshold).
          North-star: none set (prototype goal; see Q9).
          Strategic constraints: ISO flavor only; Docker metanorma/metanorma image, no local Ruby;
          Node 24 / Python 3.14 for glue; local git simulation only; no publishing beyond GitHub
          Issues in dug-21/arch-research; original sample content.
out-of-scope: other Metanorma flavors; real ISO OSD/eBalloting or national-body voting; real ISO
          standard text; PRs, Actions or `commenter github-create` against any external/live repo;
          multi-user UI, access control, hosted service, scale; Word-comment fidelity beyond Q1.
mode:     poc-required        (tag)
tags:     mnstd-001, grade n/a for goals
```

---

## 2. Answers to D1–D9

**D1: Authoring baseline. A capability, and the root prerequisite.** Every other demo compiles the draft
(v1 and v2), and intake validation needs the compiled **semantic XML** as its ground truth. Metanorma
assigns ids and clause numbers at compile time, so the source alone is not an adequate oracle. This
becomes **C1**. Its `done_when` requires the XML output explicitly, so C2 and C3 have a concrete artefact
to validate against.

**D2: Anchor model. A separate prerequisite capability (C2), plus a stability clause, and *not only* an NFR.**
Reasons:
1. Three consumers need it in different directions:
   - intake needs *ISO locator → element*;
   - PR review needs *source file:line → element*;
   - the trace needs *element v1 → element v2*.

   That is a function the prototype must perform. It is more than a property it must have.
2. It is the **determining constraint** flagged in SCOPE. If it fails, C3, C4 and C5 all fail, so it must be
   proven first and on its own.
3. Stability v1→v2 is folded into C2's `done_when` as clause C2.4. It is not a separate NFR, because it is
   testable only on the anchor function itself.

The **line number** question is unresolved. No doc evidence was found that metanorma-iso emits line numbers in
draft HTML/PDF output (searched; not found, which does not prove absence). The recommended default (Q3) is that
`line` is an optional, informational field and the clause plus element anchor is authoritative.

**D3: Comment intake (demo 1).** This is **C3**. It needs:
- **A comment register.** This is one canonical record set with ISO template fields: `id`, member body (MB/NC),
  `line` (optional), clause/subclause, paragraph/figure/table locator, type `ge|te|ed`, comment, proposed
  change, and observations/disposition (empty at intake).
- **A validator.** It checks that required fields are present, the type is in vocabulary, ids are unique, and
  the anchor resolves through C2.

The `done_when` uses **seeded invalid rows** so the validator is shown to *catch* errors. A run that only
passes valid input proves nothing. *Doc-claim:* `metanorma/commenter` offers `import` (DOCX/XLSX→YAML),
`validate` (unknown version, missing id or text, duplicate ids, unrecognized types; exits non-zero), and
`merge` (multi-body collation). Its `validate` as described checks **schema only, not anchors against the
document**, so anchor validation is likely a gap to assemble around. This is unverified.

**D4: Comment → native review blocks. This belongs to rendering (C6), not intake, and is not its own capability.**
- The projection has no observable outcome except the rendered annotation. A standalone capability would be
  mechanism-altitude and would fail the over-build guard.
- Intake must not mutate the source. The projection is a render-time transformation of v1, either into a
  derived copy or injected at build time.
- *Doc-claim:* reviewer notes are sidebars carrying `reviewer` (required), `from` (required), `to` and `date`
  (optional), anchored to `[[id]]` bookmarks. They render only for draft documents (`:draft:` or an unpublished
  stage), and they can be forced on with `:presentation-metadata-render-document-annotations:`.

**D5: Resolution loop (demo 2).** This is **C5**.
- **Disposition states:** `accept | modify | reject`, with ISO "observations of the secretariat" as a required
  free-text field for every disposition.
- **Traceability:** an **NFR (N5)** that runs across C3/C4/C5/C7. C5's `done_when` still carries its own local
  trace clause.
- **Who applies the edits:** this is named but not chosen (Q4). The options are a scripted patch derived from
  `proposed_change`, a human-simulated edit committed by a script, or an agent edit. The recommended default
  is scripted, because N3 determinism rules out an unconstrained agent edit as the *gated* path.

**D6: Git/PR review (demo 3). One comment model with two intake channels.** This is the key granularity call:
- **C4 does not define its own comment schema.** PR line comments are normalized into the **C3 register**.
  That is why C3 is a prerequisite of C4. Two models would make the disposition report (C7) a join of two
  schemas, and the trace (N5) would have two shapes.
- **Unit:** one branch per reviewer. That reviewer's review comments are recorded against commits and
  file:line on that branch. The change-proposal unit is a branch whose commits reference comment ids, merged
  with a merge commit.
- **CI on PR:** Metanorma's GitHub practice of compiling on every PR maps to a local hook or Makefile target.
  It compiles the PR head through C1 and records pass or fail before the merge is allowed.
- **Medium:** pure git plus a review-record file, or a local self-hosted forge container. That is a technology
  choice for mnstd-002 (Q5).
- **No hard edge between C4 and C5.** The recommended default is that C5's edits land through the C4 mechanism,
  but C5 is provable without it.

**D7: Rendered review output and disposition report (demo 4). Split into C6 and C7.** They have different
prerequisites:
- C6 needs only intake: v1 is annotated.
- C7 needs dispositions: the report is written after resolution.

Merging them would make the review render blocked on the resolution loop for no reason. v2 "rendered with
resolutions" is C5's output and C7's cross-reference, so it is not repeated in C6. **Report format is an owner
question (Q1).** The default is an HTML report plus a machine-readable register (YAML/CSV) in ISO template
column order. A DOCX in the ISO template's look (doc-claim: `commenter fill`) is a stretch, not a gate.

**D8: NFRs.** N1–N8 (§4), each with `About→` targets. There are two merge or split calls:
- The pinned image (N2) is kept separate from one-command reproducibility (N1). The owner named "no local Ruby"
  as a distinct constraint, and it fails independently: a demo can be one-command and still need host Ruby.
- "Original content" (N8) is kept as an NFR because it is a legal or stakeholder property of C1's sample. Flag:
  metanorma-iso injects **ISO copyright boilerplate** into output by design (doc-claim, from general flavor
  behaviour). N8 scopes *authored body text*, not tool-generated boilerplate (Q6).

**D9: Board shape and the mnstd-002 target.** This gives 7 capabilities and the DAG in §5. **mnstd-002 is ONE
validated research-scope that targets all seven business capabilities**, with N1–N8 re-verified across the
governed surface at the firewall. It has five workstreams: the two prerequisites form one foundations
workstream, and each of the four owner demonstrations gets one (§7). There is no fan-out into separate runs.

---

## 3. Business capabilities

Each `done_when` is clause-numbered for clause-by-clause validator rulings. "The demo" means the single
end-to-end entry point governed by N1. "Fixture" means artefacts committed under
`product/research/mnstd-002/` that the demo consumes.

### C1: ISO-flavor draft compiles reproducibly to HTML, PDF and semantic XML
- **why:** Every other demonstration consumes a compiled draft, and the semantic XML is the oracle for
  anchor and intake validation.
- **done_when:**
  - **C1.1** A sample draft authored in metanorma-iso AsciiDoc has at least: a foreword, scope, normative
    references, terms and definitions, ≥3 numbered clauses including ≥1 subclause level, ≥1 table, ≥1 figure,
    ≥1 note, and ≥1 annex. It compiles via the `metanorma/metanorma` container to **HTML, PDF and Metanorma
    semantic XML**, with exit status 0.
  - **C1.2** The compile log reports zero errors. Any warnings are listed in the run report, with none
    attributable to the authored source left unexplained.
  - **C1.3** The semantic XML shows ISO flavor (ISO root/flavor metadata) and a **draft** document stage, and
    contains every authored clause, table and figure with a machine-readable id and number.
- **Prerequisite of:** C2. **Governed by:** N1, N2, N3, N7, N8. **grade:** missing.

### C2: Any location in the draft is addressable and resolves to exactly one element
- **why:** ISO comments cite clause, paragraph, figure, table or line, PR comments cite source file:line,
  and the trace needs v1→v2 correspondence. Without one resolver, intake validation and tracing are
  unverifiable.
- **done_when:**
  - **C2.1** Given an ISO-style locator, either a clause/subclause number (e.g. `5.2`), or that number plus an
    element locator (`para 2`, `Table 1`, `Figure 2`, `Note 1`), the resolver returns **exactly one** element id
    in the v1 semantic XML for every locator in a fixture covering clauses, subclauses, paragraphs, tables,
    figures and an annex.
  - **C2.2** Given an AsciiDoc source `file:line`, the resolver returns the enclosing element id and its
    clause number, verified for ≥10 fixture lines spread across ≥3 clause levels.
  - **C2.3** Non-existent or ambiguous locators (e.g. `9.9`, `Table 7` when only 2 tables exist, a line in the
    document header) are **rejected with a stated reason**, never silently mapped.
  - **C2.4** **Stability.** After a v2 that edits ≥3 elements and inserts ≥1 new clause *before* existing ones,
    every unchanged v1 element resolves to its corresponding v2 element. If renumbering occurs, the resolver
    reports old→new number pairs instead of losing the element.
- **Prerequisite of:** C3. **Governed by:** N3. **grade:** missing.
- **Flag:** the ISO `line` field may have no Metanorma output equivalent (unverified). See Q3.

### C3: Validated, clause-anchored comment intake (demo 1)
- **why:** ISO review starts from a structured comment sheet, and a comment that points nowhere cannot be
  disposed or traced.
- **done_when:**
  - **C3.1** A comment sheet in CSV or YAML from **≥2 simulated reviewers (≥2 distinct MB/NC codes)** has
    ≥8 comments spanning all three types `ge`, `te` and `ed`. It is ingested into one register (the canonical
    record set that C4, C5 and C7 also read).
  - **C3.2** Every valid row is accepted with its anchor resolved through C2 to an element id. The register
    records the resolved id next to the reviewer's original locator.
  - **C3.3** A fixture of **seeded invalid rows** is rejected, each with a per-row reason. The validator exits
    non-zero and no seeded row enters the register. The fixture includes: a non-existent clause, an
    unresolvable element locator, type `xx`, a missing required field (comment text, or MB/NC), and a
    duplicate id.
  - **C3.4** Sheets from separate reviewers merge into one register without id collisions, with each comment's
    originating reviewer preserved.
- **Prerequisite of:** C4, C5, C6. **Governed by:** N4, N5. **grade:** missing.
- **Assemble candidate (doc-claim):** `metanorma/commenter` `import`, `validate` and `merge`. Anchor-vs-document
  validation appears to be outside its scope.

### C4: Git/PR review of the AsciiDoc source feeds the same comment register (demo 3)
- **why:** This is how Metanorma users actually work: the standard's AsciiDoc lives in git and changes are
  reviewed as PRs. That channel must land in the same disposition pipeline as the ISO sheet.
- **done_when:**
  - **C4.1** In a **local** git repository holding the v1 source, ≥2 simulated reviewers each produce a review:
    ≥1 per reviewer is line-anchored to a change branch's AsciiDoc diff, and ≥1 change-proposal branch exists.
  - **C4.2** Each PR review comment is normalized into the C3 register with the same fields, an ISO type, and an
    anchor resolved via C2.2 from its source `file:line`. It is marked with channel `pr` and with its source
    commit and line. A PR comment on an unresolvable line is rejected exactly like C3.3.
  - **C4.3** A pre-merge check compiles the change branch head through C1 and records pass or fail. A branch with
    a deliberately broken source (a seeded fixture) **fails the check and is not merged**.
  - **C4.4** A merged change carries the id(s) of the register comment(s) it resolves in its merge commit, and
    `git log` alone lists comment id → merge commit for every PR-resolved comment.
  - **C4.5** No remote is contacted: the repository has no network remote, and no external PR, issue or Action
    is created.
- **Prerequisites:** C3 (and C2, C1 transitively). **Governed by:** N1, N4, N5, N6. **grade:** missing.

### C5: Disposition loop produces a traced v2 (demo 2)
- **why:** Commenting only matters if each comment gets a recorded decision and accepted changes really land
  in the next draft.
- **done_when:**
  - **C5.1** Every register comment receives exactly one disposition from `accept | modify | reject`, with a
    non-empty observation. The fixture includes ≥1 of each disposition and comments from both channels if C4 is
    present.
  - **C5.2** For every `accept` and `modify`, the AsciiDoc source is changed by a commit that references the
    comment id. `reject` produces no source change. A diff of v1→v2 source contains **no** change that is not
    attributable to a comment id.
  - **C5.3** v2 compiles via C1 to HTML, PDF and XML. For each accepted or modified comment, the v2 element
    reached through C2.4 contains the change, checked mechanically against the comment's `proposed_change`
    (accept) or the recorded modified text (modify).
  - **C5.4** A trace table is emitted with one row per comment: comment id → disposition → commit → v1
    element/clause → v2 element/clause. It has no blank cell except the v2 column for `reject`.
- **Prerequisites:** C3 (C2, C1 transitively). **Prerequisite of:** C7. **Governed by:** N1, N3, N5, N7.
  **grade:** missing.
- **Open:** who or what applies edits (Q4).

### C6: Rendered v1 review draft shows every comment as a native Metanorma annotation (demo 4a)
- **why:** Reviewers and editors need to see the comments *in* the document, using Metanorma's own
  annotation feature rather than a bespoke overlay.
- **done_when:**
  - **C6.1** A rendered v1 review build in **HTML and PDF** shows every register comment as a Metanorma-native
    reviewer annotation (reviewer, date, comment text, and type/MB visible). It is attached at the element its
    anchor resolved to, with the span covering from→to where a range was given.
  - **C6.2** The count of rendered annotations equals the register's comment count, checked against the
    semantic XML annotation elements and not by eye.
  - **C6.3** The annotations are produced by projecting the register into the build input. The committed v1
    source contains no hand-written review blocks, and a "clean" v1 build from the same source shows none.
  - **C6.4** Native rendering rules are respected and stated. The run report records which mechanism made the
    annotations visible (draft stage, or the render-annotations override; doc-claim).
- **Prerequisites:** C3 (C2, C1 transitively). **Governed by:** N1, N3, N7. **grade:** missing.

### C7: Disposition report (demo 4b)
- **why:** ISO practice closes a comment round with a compiled-comments table carrying the secretariat's
  observations. The report is the artefact a committee actually reads.
- **done_when:**
  - **C7.1** The report lists **every** register comment exactly once, in ISO template column order: MB/NC,
    line, clause/subclause, paragraph/figure/table, type, comment, proposed change, observations of the
    secretariat. It adds the disposition, and the v2 location from C5.4, and it is generated from the register
    only, with no hand edits.
  - **C7.2** It is emitted in the owner-selected format (Q1; default HTML plus a machine-readable YAML/CSV), and
    its counts by type × disposition × member body match the register.
  - **C7.3** Every comment marked `accept` or `modify` links or refers to its v2 location, and that location
    exists in the v2 build.
- **Prerequisites:** C5 (C3 transitively). **Governed by:** N1, N3, N4, N5, N6, N7. **grade:** missing.
- **Assemble candidates (doc-claim):** `commenter fill` (DOCX template) and `commenter stats` (counts).

---

## 4. NFRs

An NFR is proven only by a test **across its governed surface**, and re-opens if a governed capability is
added.

| id | name (business property) | done_when | About→ |
|---|---|---|---|
| **N1** | One-command reproducible demo | **N1.1** From a fresh clone with only Docker, Node 24 and Python 3.14 on the host, **one command** regenerates every artefact of C1–C7 with no manual step. **N1.2** A second run from a clean state succeeds with the same artefact set. **N1.3** Any missing prerequisite causes a fail-fast error that names it. | C1–C7 |
| **N2** | Contained, pinned toolchain | **N2.1** All Metanorma compilation runs inside the `metanorma/metanorma` image, pinned by **digest** (or by an immutable version tag recorded with its digest). **N2.2** The demo succeeds on a host with no Ruby or gem installed, checked by `which ruby` failing. **N2.3** Host-side glue uses only Node 24 or Python 3.14 with declared, pinned dependencies. | C1–C7 |
| **N3** | Deterministic regeneration | **N3.1** Two runs with identical inputs give an identical register, trace table and report, and v2 semantic XML that is identical after normalizing a declared list of volatile fields (timestamps, generated ids if any). Each normalized field is listed and justified. **N3.2** The edit-application path (Q4) has no non-deterministic step in the gated run. | C1, C5, C6, C7 |
| **N4** | ISO comment-template field fidelity | **N4.1** The register, the PR-channel records and the report carry every ISO template field, with none dropped or renamed without a documented mapping. **N4.2** There is one comment per row or record, and the type vocabulary is exactly `ge`/`te`/`ed`. **N4.3** If a DOCX output is selected (Q1), it does not alter the template structure (no added or removed columns; doc-claim ISO guidance). | C3, C4, C7 |
| **N5** | End-to-end comment traceability | **N5.1** For a random ≥50% sample of comments, plus every PR-channel comment, a validator can follow original locator → resolved v1 element → disposition → commit → v2 element → report row using only emitted artefacts and git history. **N5.2** No artefact contains a comment id absent from the register. | C3, C4, C5, C7 |
| **N6** | No external side effects | **N6.1** The demo creates no PR, issue, Action, push or publication on any external service. The only network access is the container image pull. **N6.2** `commenter github-*` or any equivalent is not invoked against a live repository, checked by command trace and repo remote inspection. | C4, C7 (and all) |
| **N7** | Lean repository footprint | **N7.1** Generated outputs (HTML, PDF, XML, DOCX) are reproducible build products and are not committed. Any curated evidence snapshot committed for the validator is ≤ a stated size budget (proposed: 5 MB total) and listed. **N7.2** No container image or tarball is committed. | C1, C5, C6, C7 |
| **N8** | Original sample content | **N8.1** The sample draft's authored body text is written by us on a fictitious subject, and carries an authorship/provenance note. **N8.2** It reproduces no clause text from any real ISO standard. Boilerplate the metanorma-iso tool injects itself is excluded and declared (Q6). | C1 |

Grade for all: **missing**.

---

## 5. Edge list (for the curator)

**`Prerequisite` (source is the prerequisite), 6 direct edges, no transitive duplicates:**
```
C1 → C2      C2 → C3      C3 → C4      C3 → C5      C3 → C6      C5 → C7
```
Blocked-frontier reading: C1 → C2 is the critical path, and nothing downstream is startable until C2's
resolver exists.

**`Advances` → goal `mnstd`:** all 15 nodes (C1–C7, N1–N8).

**`About` (nfr → capability), 32 edges:**
```
N1 → C1..C7 (7)        N2 → C1..C7 (7)        N3 → C1, C5, C6, C7 (4)
N4 → C3, C4, C7 (3)    N5 → C3, C4, C5, C7 (4)
N6 → C4, C7 (2)        N7 → C1, C5, C6, C7 (4)    N8 → C1 (1)
```
N6 is attached only where an external side effect is plausible: C4 (git remotes, forge) and C7 (GitHub
export path). Whether to attach it to all seven is a curator call, and attaching it to all seven would add
5 edges.

**Tags on every node:** `mnstd-001`, `grade:missing`, `goal:mnstd` (if that convention is in use), `kind:business|nfr`.
No `curve` or `keystone` tags.

**Grade rationale.** `missing` is used everywhere, including C1 and C6, even though Metanorma docs *claim*
the underlying features. Those claims belong on **technology** nodes (`claimed`) created in mnstd-002, so
that the capability reads "Researched" (🔴 with claimed tech children) per §6. Putting a doc-claim onto the
capability itself would blur demand and supply.

---

## 6. Owner-demo coverage check

| Owner demonstration (OWNER-BRIEF) | Capability | Unmapped residue |
|---|---|---|
| (1) structured comment intake, a clause-anchored CSV/YAML sheet validated against the document | C3 (+ C2) | none |
| (2) resolution loop: accept/reject/modify, edits applied, v2 regenerated with resolutions traced | C5 (+ N5) | none |
| (3) Git/PR review on the AsciiDoc source, as a local simulation | C4 | none |
| (4) rendered HTML/PDF with native review blocks, plus a disposition report | C6 + C7 | none |
| Deliverable: script/Makefile, sample draft, ≥2 reviewers, dispositions, v1/v2, report, no big binaries | N1, C1/N8, C3.1, C5.1, C1/C5.3, C7, N7 | none |

---

## 7. D9: mnstd-002 target set

**One validated research-scope, `mnstd-002`, targeting C1–C7.** N1–N8 are verified across the governed
surface at its firewall. There is one feasibility POC, which is the single end-to-end demo (N1), with
clause-by-clause validator rulings against §3 and §4.

| Workstream | Capabilities | Owner demo | Notes |
|---|---|---|---|
| **W0 Foundations** | C1, C2 | (prereq) | **Determining constraint** is C2 (anchors and line numbers). Prove first; if C2 fails, rule W1–W4 blocked, not failed. Also the environment risk: image size and CPU architecture. |
| **W1 Intake** | C3 | 1 | assemble-vs-build: `commenter` validate/merge vs custom schema |
| **W2 Resolution** | C5 | 2 | edit-application mechanism (Q4); trace emission |
| **W3 Git/PR review** | C4 | 3 | local simulation medium (Q5) |
| **W4 Review output** | C6, C7 | 4 | native annotation projection; report format (Q1) |

An honest partial outcome is legitimate. For example, C1, C3 and C6 proven while C2.4, the renumbering
stability clause, is only partial. The firewall rules per clause.

---

## 8. Open owner questions (non-blocking; defaults apply if unanswered)

| # | Question | Recommended default |
|---|---|---|
| **Q1** | Disposition report format: must it match the ISO template's look (DOCX), or are HTML, Markdown or CSV acceptable? | **HTML report plus YAML/CSV register in ISO column order** as the gate. DOCX via `commenter fill` is an optional stretch and is not in C7's done_when. |
| **Q2** | One comment model with two channels (sheet + PR), or two models? | **One register, two channels** (as built into C3/C4). |
| **Q3** | The ISO `line` field: required, or optional? | **Optional and informational.** Clause plus element anchor is authoritative. If mnstd-002 finds draft line numbering in metanorma-iso output, promote it. |
| **Q4** | Who applies accepted edits in the prototype: a script, a human-simulated script, or an agent? | **Scripted, from the disposition record** (deterministic, satisfies N3). An agent-applied variant may be shown but is not gated. |
| **Q5** | PR simulation fidelity: plain git plus a review-record file, or a local forge container (still local, no external repo)? | **Plain git plus review records** (fewest moving parts). A local forge is acceptable if it is cheap, and the choice is for mnstd-002. |
| **Q6** | metanorma-iso injects ISO copyright and boilerplate text into output. Is that acceptable in a sample? | **Acceptable.** It is tool-generated, and the sample is marked fictitious/non-ISO. Authored body text stays original (N8). |
| **Q7** | Disposition vocabulary: exactly accept/modify/reject, or also "noted" (common for `ge` comments with no change)? | **Exactly the owner's three.** "Noted" is recorded as `reject` or `accept` with an explanatory observation. |
| **Q8** | Is Word (.doc/.docx) draft output required? ISO's own drafting deliverable is Word. | **No.** HTML, PDF and XML are enough for the prototype. |
| **Q9** | Should the goal carry a north-star, such as realism against actual ISO committee practice? | **No north-star now.** Revisit after mnstd-002. |

---

## 9. Flags and what I could not verify

- **Line numbering in metanorma-iso draft output: not found** in docs or search. Absence is not proven. This
  drives Q3 and C2.
- **Reviewer-note syntax and rendering rules** come from older metanorma-standoc gem docs on rubydoc.info,
  plus SCOPE's grounding. The current metanorma.org pages returned 404 at the URLs I tried. The syntax may
  have changed (doc-claim, possibly stale).
- **`commenter` feature list** comes from its README (doc-claim). Recency, correctness, and whether `validate`
  checks anchors against a document are all unverified. As read, it does not.
- The render-annotations override attribute name is taken from SCOPE. I could not re-confirm it at source.
- The 5 MB footprint budget (N7) and the ≥8 comments / ≥10 lines fixture sizes are **my proposals**. They are
  not owner numbers, and the owner or leader may tune them.

## 10. Citations (D14)

```
- type: repo
  ref: github.com/metanorma/commenter
  title: commenter
  org: Metanorma
  surface: active-dev
- type: docs
  ref: https://www.rubydoc.info/gems/metanorma-standoc/1.1.2
  title: metanorma-standoc (README, reviewer notes section)
  org: Metanorma
  surface: products
- type: docs
  ref: https://rubydoc.info/gems/metanorma-standoc/1.0.13/file/README.adoc
  title: metanorma-standoc README
  org: Metanorma
  surface: products
- type: docs
  ref: https://www.rubydoc.info/gems/metanorma-iso/1.0.7
  title: metanorma-iso
  org: Metanorma
  surface: products
```
The ISO commenting-template guidance (no structural modification, one comment per row) is carried from
SCOPE.md's light grounding. I did not re-fetch the ISO source in this run, so it is not cited here as
independently read.
