# Evidence packet specification and index

Each episode packet is a deterministic projection of the pinned source tree, not a new interpretation.
The executable extraction and generated packet bodies belong on `research/jurati-001` under D15. This
document freezes what must be extracted before that branch is created.

## Packet schema

1. `episode_id`, domain, cycle, decision point, partition.
2. Pinned repository SHA and ordered source paths with SHA-256 per file.
3. Historical question and clause obligations quoted from scope/specification/acceptance artifacts.
4. Evidence available at the decision time, excluding later rework and later verdict summaries.
5. Admissibility notes: direct artifact, report claim, owner ruling, or inferred chronology.
6. Reference-only envelope: historical verdict, exact next action, owner intervention, adjudicator notes.
7. Judge-facing envelope: identical evidence with the reference-only envelope removed.

All semantic claims retain source line spans. A packet must fail generation if a source path or digest does
not match, a selected report has no antecedent evidence artifact, or a holdout reference field enters the
judge-facing envelope.

## Source bundle rules

- SDLC design gate: `SCOPE.md`, `ACCEPTANCE-MAP.md`, `ARCHITECTURE.md` or its nested equivalent,
  `SPECIFICATION.md`, `RISK-TEST-STRATEGY.md`, and the selected gate 3a report.
- SDLC code gate: prior design artifacts, implementation brief, selected gate 3b report, and only the code
  state identified by the report's commit when available.
- SDLC risk gate: risk strategy, acceptance map, risk-coverage report, selected gate 3c report.
- Bug-fix gate: bug scope/investigation/fix/verification artifacts present in that cycle plus the selected
  bug-fix gate report. Do not invent missing lifecycle documents.
- Garage: approved scope, named findings/artifacts referenced by the decision, report or triage record, and
  owner ruling where present. Unimatrix summaries are context, not substitutes for repository evidence.

## Special packets

- `vnc-047`: preserve a whole-chain bundle while emitting three episode views. Later gates may see prior
  gate outcomes as chronology, but may not expose their own verdict summary.
- `shd-007`: split C1 and C2. Quote each `done_when` verbatim and preserve the owner's explicit `partial`
  rulings. The initially proposed C1 `proven` grade is evidence of a corrected judgment, not the label.
- `wfh-002`: preserve the unenforced boundary and the later out-of-scope decision as separate fields. A
  packet that silently rewrites the boundary has erased the failure under test.
- Rework pairs (`col-023`, `bugfix-381`): the initial failure and later pass are separate chronological
  decisions. The later packet may see the earlier result; the earlier packet may not see the fix.

## Integrity outputs required on the executable branch

- `corpus/manifest.jsonl`
- `corpus/packets/<episode-id>.json`
- `corpus/reference-labels.jsonl` (not judge-facing)
- `corpus/splits.json`
- `corpus/SHA256SUMS`

These generated files are intentionally not created on `main`; D15 classifies datasets and extraction code
as research executables.
