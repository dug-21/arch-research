<!--
Ready-to-post Issue body for wfh-005. NOT yet opened — the execution session opens it as INIT step 1,
paired with `context_cycle start`, so all three surfaces (Issue / cycle / git) open together (OBS-10).

  gh issue create --repo dug-21/arch-research \
    --label factory,scope:research,confidence:directional \
    --title "wfh-005 — theme-scan(challenge): attack the five positions theme:workflow-harness stands on" \
    --body-file product/research/wfh-005/ISSUE.md
-->

**Scope:** `product/research/wfh-005/SCOPE.md` (authoritative) · **Protocol:** `.claude/workflow/theme-scan.md`
· **Theme:** `theme:workflow-harness` → JURATI (`dug-21/jurati`) · **Mode:** challenge · **Confidence:** directional

## The question

> **Are the five things this theme is standing on actually true — and if they are not, what shape does the theme take instead?**

Three runs have added structure on top of premises nobody has attacked. This is a **challenge scan**: discovery finds what we lack and structurally cannot report that something we already believe is solved, superseded, or wrong. That is this run's entire job.

## The five positions under test

| | Position | Falsified by |
|---|---|---|
| **P1** | The ~30 owner-injected references are real and say what is claimed of them | a reference that doesn't exist, is misattributed, or doesn't support its claim |
| **P2** | Phase-indexed derivation and gate independence are **unpublished** | anyone doing it — especially under a different name |
| **P3** | Minimize inference; determinism is what makes a guarantee rather than a tendency | guarantees achieved *with* inference on the path — or evidence deterministic enforcement is insufficient in practice |
| **P4** | Build is necessary; nothing shipping or assemblable covers this | a product, or composition, whose scope covers the eight concerns |
| **P5** | The demand is real — this answers someone's problem, not only our incident log | absence of external evidence that others hit these failures |

P2 is the theme's moat, and it was asserted by a model as an absence claim — the hardest kind to establish and the easiest to assert. P4's falsification would be the **best** outcome available.

## Shape

Four scouts, one per reading surface — **research literature · established products · active development · adjacent prior art** — spawned in one message, each attacking all five positions from its own surface. Then a leader cross-surface merge (the same idea appears under four names), then goal-owner verdict synthesis.

**Coverage grid = 5 positions × 4 surfaces = 20 cells.** Complete when every cell is populated or declared a hole naming the surface that failed to see it.

**Cold leg is the emergent-position slot:** each scout reserves protected effort for *"what assumption is this theme holding that nobody put on the list?"* A sixth position surfaced there is the highest-value output available.

**Verdicts per position:** SURVIVES · WOUNDED (state the narrowing) · FALSIFIED (name the counter-evidence) · NEEDS-A-PROBE (name the one question). P4 additionally routes ADOPT / ASSEMBLE / BUILD with the required fields.

**Five protocol deviations** carried for sign-off at INIT (SCOPE §Deviations): surfaces as workstreams · grid is positions × surfaces · per-position verdict vocabulary · cold leg redefined · **no hypothesizer** (a challenge scan generates nothing; if it wants one it has drifted back into discovery).

## Proof bar

**None — structure only.** One distinction the run must not blur: **verifying that a citation exists does not make its claim `proven`** — it makes the citation real. A challenge scan may lower confidence, sharpen a node, or record a contradiction. It never raises status.

## Relationship to wfh-004

wfh-004 is **open and parked at its blocking owner gate** (#48). The wf-v0.17 governor — do not scan a theme carrying an untriaged shortlist without surfacing it — **fired, and this run is the owner's answer**: a bounded challenge scan run specifically to *inform* that gate, because the verification debt sits directly upstream of the build-versus-assemble decisions waiting there.

Binding: **wfh-005 must not touch wfh-004's shortlist.** It hands back verdicts. The gate stays unresolved and the owner's.

## Out of scope

Architecture and mechanism selection (Option C stays provisional) · any build or POC · board decomposition · premises H6/H7/H8 (parked to a second challenge scan) · the hooks-and-permissions probe (already queued from wfh-004) · **the wfh-004 gate decision itself**.

## Budget

**10–12 spawns** — 4 surface scouts, up to 4 grid-targeted round-two passes, 1 curator, 1 goal-owner. Under wfh-004's 18–22 (which overran to ~30): a challenge scan is bounded by its positions, not by generative range. Out-of-envelope is a blocking question, not an in-envelope steer.

## Gates

1. **INIT (advisory)** — the declared shape above plus the five deviations. The owner's kick is the approval.
2. **Triage (blocking)** — the owner reviews the five verdicts, the coverage call, P4's routing, and any theme-revision proposal. **Concluding that a premise is false is a successful run.**

## Notes for the execution session

- First run under the wide-mouth standard (wf-v0.17 / v0.18 / v0.19). Derive the stamp at INIT with `git describe --tags --match 'wf-*'` and pass it as the **set-once** `context_cycle` start tag — no append, no retro-fix.
- Open **all three surfaces at INIT** before any spawn: this Issue, `context_cycle start` (topic `wfh-005`), and the `research/wfh-005` branch (already pushed, carrying SCOPE.md and this file).
- **Auto-merge does not exist in this repo** (wf-v0.19) — the leader rebase-merges by hand after the gate.
- Specialists cannot write files in this harness (OBS-7): scouts return markdown inline, the leader persists.
- **No graph writes before triage** (lesson #172). The curator files post-gate only.
- Citations carry provenance now (D14): `type` · `ref` · `title` required, plus `author` / `org` / `year` and `surface` set to the scout's own assignment. **Omit an unknown key — never guess one.**
