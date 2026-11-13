# mnstd-001 — Decompose: Metanorma ISO-style standards authoring & commenting/review prototype

**Status:** scoped
**Goal(s):** `mnstd` (new standalone goal, primary; no goal node exists yet, the curator creates it in the decompose phase)
**Capability target(s):** none yet. This decompose-scope *produces* the capability board; it advances no grade.
**Confidence-required:** decompose-scope is structure only. The follow-on `mnstd-002` is **validated** (owner, binding).
**Phase / area:** standards authoring · document review/commenting · docs-as-code
**Cycle topic / Issue:** `mnstd-001` · GitHub Issue dug-21/arch-research#73
**Owner intent (binding, verbatim):** `product/research/mnstd-001/OWNER-BRIEF.md`

---

## Goal sentence (for `context_cycle start` and the `goal` node; methodology §7)

> Demonstrate, with a reproducible prototype we build and run ourselves, that an ISO-flavored standard
> authored in Metanorma AsciiDoc (`metanorma-iso`) can go through a complete ISO-style commenting cycle:
> clause-anchored comment intake validated against the document, a disposition loop that regenerates a
> traced v2, Git/PR-based review of the AsciiDoc source, and rendered HTML/PDF review output that carries
> Metanorma's native review blocks plus a disposition report.

## The question

The owner wants to see how standards **authoring** and **commenting/review** work in Metanorma, shown by a
prototype. Before any technology is researched, the goal has to be split into the capabilities that must
exist for that prototype to be "delivered", each with a testable `done_when`, so `mnstd-002` has a
concrete board to research and prove against.

> What capabilities, NFRs and dependencies make up an ISO-style Metanorma authoring and commenting cycle,
> at a granularity where each one can be proven by a single integration-altitude demonstration?

## Why it matters

This is a new goal with nothing in the library (see prior art). Without a board, `mnstd-002` would
research "Metanorma" as one undifferentiated topic and could not give a clause-by-clause firewall ruling.
The board is also the place to settle one framing question early: whether the four owner demonstrations are
four capabilities, fewer, or more. Comment intake and PR review may be two channels into **one** comment
model. Or the anchor model may be a hidden prerequisite capability that all four depend on.

## Success criteria (for this decompose-scope)

1. A `goal` node (`mnstd`) carrying the goal sentence above, tagged `mnstd-001`.
2. A capability board where **each of the owner's four demonstrations** maps to at least one business
   capability with an integration-altitude `done_when`:
   (1) structured comment intake, (2) resolution loop with traced v2, (3) Git/PR review on AsciiDoc
   source, (4) rendered review output plus disposition report. Nothing the owner asked for is left
   unmapped.
3. Any prerequisite capability the four depend on (expected candidates: ISO-flavor authoring/compile
   baseline; a stable clause/element anchor model) is made explicit with `Prerequisite→` edges.
4. NFR nodes for the owner's environment and fidelity constraints (see D8), linked `About→` the
   capabilities they govern.
5. Every node is `grade:missing` or `grade:claimed`, tagged `mnstd-001`. **Nothing is `partial` or `proven`.**
6. The decomposition file names the `mnstd-002` target set. If the four are separate capabilities, the plan
   is **one validated research-scope covering them as workstreams** (owner-authorized; no fan-out into four
   runs).

## Known constraints & prior art  *(build on these, do not re-derive)*

**Unimatrix prior art: none found.** Queries run (agent_id `factory-researcher`, 2026-11-13):

| Query | Category | Result |
|---|---|---|
| "metanorma standards authoring AsciiDoc" | technology | no domain match (top hits #258, #270, #194, #282, #222 are all workflow-harness/jurati, relevance ≤0.19) |
| "document review commenting workflow, comment resolution, git pull request review docs-as-code" | technology | no domain match (#198 gh-aw, #278, #201 are agentic-workflow tooling, not document review) |
| "standards document authoring and review comment process" | (all) | no domain match (#300 "reviewer throughput", a process-plane position, not reusable here) |
| "metanorma ISO standard comment template review" | goal | no match (#242 shd, #92 platform vision) |
| "document authoring, comment intake, review annotation, rendered HTML PDF output" | capability | no match |
| "metanorma AsciiDoc docs-as-code git PR review of documents" | finding | no match (#319, #195 are unrelated) |

**Reuse candidates: none.** #198 (`github/gh-aw`) is the only GitHub-workflow-adjacent technology. It is not
a reuse candidate: it is agentic CI, not document review, and the owner restricts the prototype to a local
git simulation. The curator should create the `mnstd` nodes fresh.

**Constraints from the owner brief (binding):**
- ISO flavor only: `metanorma-iso`, with ISO's comment template model (MB/NC, line number, clause/subclause,
  paragraph/figure/table, comment type `ge`/`te`/`ed`, comment, proposed change, observations of the
  secretariat / disposition).
- Toolchain route: Docker `metanorma/metanorma` image. No local Ruby. Node 24 and Python 3.14 are available
  for glue.
- Git/PR review is a **local git-repo simulation**. No PRs against external repos and no publishing beyond
  Issues in dug-21/arch-research.
- Deliverable: one reproducible end-to-end script/Makefile, a sample ISO-flavor draft, a comment sheet from
  at least two simulated reviewers, dispositions, rendered v1/v2, and a disposition report. No large binaries
  committed unnecessarily.
- Prefer assembly over building. Check what Metanorma offers natively first.

**Light grounding (doc-claim only, not verified by running; deep evaluation is `mnstd-002`'s job):**
- Metanorma has native **reviewer comment blocks**: `[reviewer="…",date=…,from=anchorA,to=anchorB]` followed
  by a `****` sidebar block, anchored to `[[id]]` bookmarks. It also turns `TODO` admonitions into reviewer
  notes. By default, annotations render only for unpublished document stages. The
  `:presentation-metadata-render-document-annotations:` attribute overrides this. *(doc-claim)*
- A `metanorma/commenter` gem exists. It converts an ISO comment-sheet DOCX to YAML, fills a DOCX template
  from YAML, and has a `github-create` command that turns comments into GitHub issues. It was active in
  2026-09. This is a likely **assemble** candidate for intake (D3) and the disposition report (D7).
  *(doc-claim; whether it works and how well it fits is unverified)*
- ISO's guidance says the commenting template must not be structurally modified (no added or removed
  columns, one comment per row), and the national-body route accepts the Word form. This affects the
  CSV/YAML-vs-DOCX fidelity question (D3, D8). *(doc-claim)*

## Decomposition questions (the decompose-phase workstreams)

The decompose phase is one `factory-researcher` partition. These are the questions its decomposition file
must answer. Each yields candidate capabilities/NFRs plus dependency edges, not technology choices.

- **D1 — Authoring baseline.** Is "author and compile an ISO-flavor Metanorma document to HTML/PDF (+
  Metanorma XML) reproducibly via Docker" a capability in its own right and a prerequisite to the other
  four? What is its `done_when`, given that the semantic XML is the likely validation target for D3?
- **D2 — Anchor model.** How is a comment addressed? ISO uses line/clause/paragraph/figure/table, while
  Metanorma uses element ids, `[[anchor]]` bookmarks and clause numbering. Does draft output give line
  numbers at all? What must stay stable from v1 to v2 for tracing to work? Is this a separate prerequisite
  capability, or an NFR ("anchors are stable and resolvable") `About→` intake and resolution?
- **D3 — Comment intake (demo 1).** What does a validated, clause-anchored comment sheet look like
  (CSV/YAML schema mirroring the ISO template), and what does "validated against the document" mean
  (clause exists, anchor resolves, type is in `ge|te|ed`, required fields present)? What `done_when` would
  catch an invalid anchor? Native or assemble candidates: `commenter` YAML.
- **D4 — Comment → native review blocks.** Is projecting sheet comments into Metanorma `[reviewer=…]` blocks
  (for rendering, demo 4) part of intake, part of rendering, or a capability of its own?
- **D5 — Resolution loop (demo 2).** Disposition states (accept / reject / modify, plus ISO "observations of
  the secretariat"), how accepted edits are applied to the AsciiDoc source, v2 regeneration, and the
  **trace** comment → disposition → source change → v2 location. Is traceability an NFR or a capability?
  Who applies edits in the prototype (scripted patch, human-simulated, agent)? Name it, but do not choose
  the technology.
- **D6 — Git/PR review (demo 3).** In a local simulation, what is the unit (branch per reviewer? PR per
  comment batch? a commit that resolves a comment)? How do PR review comments relate to sheet comments:
  **one comment model with two intake channels, or two separate models?** This is the most important
  granularity call for the board. How does Metanorma's own GitHub practice (CI compile on PR) map to a local
  simulation?
- **D7 — Rendered review output + disposition report (demo 4).** v1 rendered with review annotations
  visible, v2 rendered with resolutions, and a disposition report (ISO compiled-comments table with
  observations) in a chosen format. Does the report have to match the ISO template's look (DOCX via
  `commenter`), or is HTML/Markdown/CSV acceptable? Flag this for the owner instead of assuming.
- **D8 — NFRs.** Candidates: reproducible one-command demo, Docker-only toolchain with a pinned image
  version, no external publishing, no unnecessary large binaries, ISO-template field fidelity, deterministic
  regeneration (same inputs give the same v2), and **original sample content** (ISO standard text is
  copyrighted, so the sample draft must be authored by us). Each needs an `About→` target.
- **D9 — Board shape and the `mnstd-002` target.** The final capability count and `Prerequisite→` edges.
  Confirm a single validated research-scope with one workstream per capability. Draft each capability's
  integration-altitude `done_when` clause, which `mnstd-002`'s firewall will be judged against clause by
  clause.

*Output (decompose phase):* `product/research/mnstd-001/decomposition.md`, containing candidate
capabilities (name, `done_when`, owner-demo mapping), NFRs (with `About→` targets), the `Prerequisite→`
graph, the `mnstd-002` target set, and open owner questions (expected: D7 report format, D6 channel model).

## Proof bar

**Structure only. No status change.** This scope produces a goal node, `missing`/`claimed` capability and
NFR nodes, and edges. All Metanorma behavior cited above is doc-claim. Proof (`partial`/`proven`) can only
come from `mnstd-002`'s feasibility phase: a factory-poc artifact demonstrated by us, at integration
altitude, that clears each capability's `done_when` clause by clause under an independent factory-validator
verdict.

## Explicitly out of scope

- **Technology selection and evaluation.** For example, `commenter` vs a custom schema, or which diff/trace
  mechanism to use. That is `mnstd-002`. D-questions may *name* candidates, not rank them.
- **Building or running anything.** No Docker pulls and no compiles in this run.
- **Other Metanorma flavors** (IEC, ITU, OGC, IETF, …) and non-ISO comment models.
- **Real ISO process integration.** No ISO OSD/eBalloting submission, no national-body voting/ballot
  mechanics, no real ISO standard text.
- **External GitHub interaction** beyond Issue #73: no PRs on external repos, no GitHub Actions on
  external repos, no use of `commenter github-create` against a live repo.
- **Production concerns:** multi-user web UI, access control, hosted review service, scale.
- **Word-document comment fidelity** beyond what D7/D8 surface as an owner question. It is not assumed to
  be in scope.

## Coverage / done call

A decompose-scope has no loop-until-dry tech coverage. Its done call is: every owner demonstration (1–4)
maps to a capability with a testable `done_when`, every D-question is answered or explicitly parked as an
owner question, and the board is approved at the advisory gate (pre-authorized by the owner to proceed). Per
§6, the board is **never assumed complete**: gaps found in `mnstd-002` are added as new `missing` nodes.

## Flags

- The ISO-template "line number" field may have no Metanorma equivalent in draft output (unverified). If
  so, the anchor model (D2) is the determining constraint for intake validation.
- The `metanorma/metanorma` image is large and its CPU-architecture support was not checked. This is an
  environment risk for `mnstd-002`, not this run.
- `commenter`'s maintenance status and correctness are doc-claim only. Treat it as a candidate, not a given.
