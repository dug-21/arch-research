# mnstd — owner brief (verbatim, recorded 2026-11-13 by research-leader)

Source: owner instruction relayed to research-leader, session 2026-11-13. Recorded verbatim so specialists read the source, not a summary (D1).

## The owner's request (verbatim intent)
"A new research item related to developing a prototype model for the standards authoring/commenting process using metanorma.org. I'm interested in the standards authoring and how the commenting/reviews would work. The scope is to build a prototype that is able to show this, as a prototype task in the project."

## Owner's clarifying answers (binding)
- Confidence-required: **validated** (feasibility phase with factory-poc + independent factory-validator; firewall applies).
- Flavor: **ISO-style** — metanorma-iso, modelled on ISO's commenting model (ISO comment template: line/clause/paragraph, comment type ge/te/ed, comment, proposed change, observations/disposition).
- The prototype must demonstrate ALL FOUR: (1) structured comment intake — clause-anchored comment sheet (CSV/YAML) validated against the document; (2) comment resolution loop — dispositions accept/reject/modify, edits applied, v2 regenerated with resolutions traced; (3) Git/PR-based review on the AsciiDoc source (as Metanorma users actually work on GitHub — a local git-repo simulation is acceptable for the prototype; do NOT open PRs against external repos); (4) rendered review output — HTML/PDF carrying Metanorma's native review/annotation blocks plus a disposition report.
- Placement: **new standalone goal** → run `mnstd-001` = decompose-scope (`.claude/workflow/decompose-scope.md`) producing goal + capability board; then `mnstd-002` = validated research-scope (`.claude/workflow/research-scope.md`) targeting the capability(ies) for the prototype. If the board shows the four demonstrations are separate capabilities, one validated research-scope covering them as workstreams is acceptable (state it in SCOPE) — don't fan out into four runs.

## Autonomy / gates (owner delegation)
After clarifying questions, follow the process to completion autonomously. Human advisory gates (scope approval, coverage confirm, decompose board approval, synthesis review) are **pre-authorized by the owner to proceed**; gate artifacts are still produced and posted. Blocking gates stay blocking: coverage (loop-until-dry) and the FIREWALL (independent factory-validator verdict; no `proven` without a verified, demonstrated-by-us artifact clearing done_when clause by clause; REWORKABLE max 2, then SCOPE-FAIL). Honest `partial` beats an inflated `proven`.

## Environment facts (as given by owner)
- Docker works (daemon reachable); no Ruby locally. Metanorma's official image `metanorma/metanorma` is the expected route (`docker run -v $(pwd):/metanorma metanorma/metanorma metanorma compile ...`). Node 24 and Python 3.14 available.
- Artifacts under `product/research/mnstd-00N/`. POC self-contained and reproducible (a script/Makefile that runs the whole demo end to end), with a sample ISO-flavor standard draft, a sample comment sheet from >=2 simulated reviewers, dispositions, v1/v2 rendered outputs, and a disposition report. Don't commit huge binaries unnecessarily.
- Do NOT publish anything to claude.ai or any external service beyond GitHub Issues in dug-21/arch-research.
- Scouts/researchers should check what Metanorma natively offers for reviews (review/annotation blocks, `metanorma-cli` features, any existing comment-sheet tooling, Metanorma's GitHub-based workflows, ISO's comment template/ISO directive practice) — assembly over build.
