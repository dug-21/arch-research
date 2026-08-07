# jurati-001 task freeze candidate

This executable candidate implements `SPEC-v0.1-dev.md` without changing its five verdicts, four clause
results, blocking/advisory criticality, or total verdict-to-action rule. The task, checker, evidence
digests, split, and reference commitments are represented by `corpus-generated/SHA256SUMS` and the POC
commit. They remain a **candidate**, not a launched holdout freeze, until the mandatory human
corpus-freeze gate approves the generated restricted mapping and attestations.

Checker launch: `python3 poc/test_jurati.py && python3 poc/verify_freeze.py`.

The checker self-test includes known-green, known-red, mechanically tampered evidence, missing transition,
undeclared evidence, illegal transition, judge response widening, prompt injection as evidence,
contradiction/insufficiency no-advance, counterfactual locality, and three fresh-process replays.

The B/C prompt, strict parser, retrieval/exclusion rules, model digest, decoding policy, repetition counts,
logging schema, and fail-closed launch wrapper are frozen under `task/` and `poc/run_semantic.py`.
No holdout semantic arm has been launched. Any language, prompt, contract, checker, or runner change after approval
requires a new version and untouched holdout.
