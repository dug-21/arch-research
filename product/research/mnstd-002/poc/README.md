# mnstd-002 POC — ISO-style Metanorma authoring and commenting cycle

One rig, one command. Authored by `factory-poc`. Evidence, not a grade.

```sh
docker pull metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da  # once (network)
make fonts   # once, NETWORKED: ~840 MB font cache in ~/.cache/mnstd-002-fonts (override MNSTD_FONT_CACHE); ruling R1
make demo    # gated, network-free: two full runs from clean + self-tests + cross-run checks (~10 min)
```

`make demo` runs, twice from a clean state (`build/run-a`, `build/run-b`):
v1 compile (C1) → resolver fixtures (C2.1–C2.3) → intake of 3 reviewer sheets + a seeded-invalid sheet (C3) →
local git repo with a change branch, PR review records from 2 reviewers, 3 seeded broken branches (C4) →
dispositions + seeded bad record (C5.1) → scripted edits, one commit per comment id, gated `--no-ff` merges
(C4.3/C4.4/C5.2) → v2 compile + v1→v2 map (C5.3/C2.4) → trace (C5.4) → annotated v1 review build + clean build
(C6) → disposition report (C7) → clause checks. Between the runs it self-tests every checker against tampered
copies; after them it compares the runs (N1.2, N3.1, N3.2) and snapshots small evidence to `../artifacts/`.

Layout: `src/` v1 source (frozen) · `tools/` glue (Python 3.14 stdlib; `srcmap.rb` runs in-container) ·
`bin/` command-trace shims (docker/git traced; curl/wget/gh/commenter refused) · `../task/` frozen fixtures,
expectations and `FROZEN.sha256` · `build/` generated, gitignored.
See `../artifacts/RESULT.md` for the clause-by-clause self-assessment and `../artifacts/ENVELOPE.md` for the
configuration in force.
