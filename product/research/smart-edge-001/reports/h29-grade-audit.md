# H29 grade-chain audit — `smart-edge-001` (promoted probe)

**Run by:** `smart-edge-001-leader` · **Type:** structure-only directional probe (the cheapest look; goal-owner's sequencing decider) · **Firewall:** read-only; no graph write, no status moved.

## Purpose
goal-owner's decision rule (triage-v2 §Top recommendation): run this audit *before* promoting a build.
- **Illegal transition found** (or scale makes them near-certain) → the **write-path guard bundle** (H17+H29+H27) is the first build.
- **Clean** → **H11** (hotspot bank) is the first build.

The audit tests H29/D7's core: does any `grade:proven` node exist without a real `proven_by` artifact set via `context_correct` (never a bare `context_tag`)?

## Method
- `context_lookup(tags:["grade:proven"], status:active)` → all proven nodes.
- `context_lookup(tags:["grade:partial"], status:active)` → context on the graded set.
- `context_get(97, format:json)` → inspect the one proven node's `proven_by` + supersession provenance.

## Findings
- **Exactly one `grade:proven` node in the whole graph: #97** (Unimatrix — evidence-graded knowledge & governance engine).
- **#97 passes the D7 transition rule:**
  - Has a `proven_by` field: *"live — Unimatrix is the running knowledge engine of this research factory: context_* tools, the firewalled proven-vs-claimed graph, and cycle telemetry, in continuous use; built by us."*
  - Altitude-scoped explicitly: *"proven AS a knowledge/governance engine in production use. NOT proven as the integrated platform spine."*
  - `supersedes: 94`, `correction_count: 0` → reached `proven` via a **`context_correct`** chain, not a bare `context_tag`.
- `grade:partial` set (7 nodes: factory caps #25/26/27/29/30/31, enhancement #65) — all consistent, no proven-without-artifact.

## Verdict: **CLEAN**
No illegal grade transition exists. Per the decision rule → **promote H11 as the first proof-goal.**

## Caveats recorded (honest, not hidden)
1. **n = 1.** Only one proven node exists — "clean" is weak evidence. The factory is young and single-curator-disciplined; the write-path guards' value is **preventive at multi-goal / multi-agent scale**, not retroactive cleanup. This *confirms* goal-owner's read that the bundle's value skews to imminent scale, not today.
2. **#97's `proven_by` is prose narrative, not a pinned artifact ref.** H29-as-specified (has-proven_by + via-correct) passes it. A *stricter* variant (require a structured `{type, ref}` artifact) would flag it. This is a genuine design decision about the firewall's mechanical strictness — surfaced for the write-path-bundle scope when it is built, not treated as a violation here.

## Consequence for the shortlist
- **H11 → first build** (promoted now).
- **Write-path guard bundle (H17+H29+H27) → second build**, its value framed as *preventive at scale* (not retroactive), per caveat 1. When built, decide the H29 strictness question (caveat 2).
