# shd-002 — FINDINGS (synthesis)

**Scope:** shd-002 · **Capability:** C2 — agentic harness drives research+coding to completion (#5)
**Confidence:** directional · **Status:** structure-only (no `proven`) · Date: 2026-06-23
Workstream files: `findings-W1.md` (inventory) · `findings-W2.md` (local compat) · `findings-W3.md`
(autonomy/tool-calls) · `findings-W4.md` (distribution).

---

## 1. The decision axis (what actually determines C2)

The load-bearing variable is **not** "does the harness claim local support" — every serious OSS
harness connects to a local OpenAI-compatible/Ollama/vLLM endpoint cleanly (W2: none foreclosed).
It is the **harness ↔ proxy ↔ model tool/edit contract**, which only fails *in motion* (W3). That
splits the field into two mechanism classes:

- **No-native-tool-call (degrades gracefully):** **aider** (text SEARCH/REPLACE / whole-file),
  **Continue** (XML system-message tools). They sidestep the entire envelope + capability-detection
  failure class.
- **Native-tool-call (inherits model + proxy weakness):** Claude Code (T3a), OpenHands, Goose,
  opencode, Cline, Roo — these break exactly where local models are weak (format drift > ~5 tools,
  litellm mis-detection, `finish_reason:stop` loop-exit).

## 2. Feasibility map (for "completes a multi-step task on a local backend")

| Tier | Harnesses | Read | Determining constraint |
|---|---|---|---|
| **Most promising (moderate)** | **aider**, **Continue** | best mechanism; no native tool-call dependency | aider autonomy narrower; Continue agent-mode metadata-gated (#6677) |
| **High ceiling / high risk (hard)** | **Claude Code (T3a)** | biggest autonomy ceiling, **most translation hops**, zero demonstrated local completion | the §12 L1 trap — must smoke-test |
| **Autonomous but plumbing-gated (hard)** | **OpenHands**, **Goose** | genuine agents; gated by litellm detection (#8424) / 41% toolshim ceiling | local tool-call reliability |
| **Broken/caveated today (dream-until-fixed)** | **opencode** (#20719), **Cline** (#4362) | concrete failure artifacts on local | unverified fixes |
| **Out / fading (W1)** | Cursor, Gemini CLI (retiring), Continue-the-product (Cursor-acquired), Plandex, Devika | fail local clause or unmaintained | — |

**Nothing is "easy/proven."** No harness has a demonstrated multi-step *completion* on local — only
connectivity and one-shot demos. Distribution (W4, N4) **forecloses no one** and stays a weak
tie-breaker; for owned-hardware it mildly favors opencode/Claude Code over OpenHands' vendor-sandbox.

## 3. Recommendation (position — directional)

Do **not** pick a single winner from literature. The directional call:

1. **The mechanism finding is the signal:** for local backends, **prefer no-native-tool-call
   harnesses**. This is corroborated across W2 (docs' own warnings) and W3 (concrete break artifacts).
2. **Smoke-test slate for `shd-003` (validated), in order:**
   - **aider** — baseline; lowest-risk mechanism, strongest recovery story.
   - **Claude Code + local `/v1/messages` shim (T3a)** — highest ceiling; the §12 candidate. Test, don't assume.
   - **Continue** — only if the agent-mode metadata gate (#6677) is overridable for a local model.
   - *(opencode/Cline excluded until their fix-PRs are confirmed working.)*
3. **POC bar (`shd-003` `done_when`):** drive **≥6–8 sequential tool calls** through the **real local
   proxy** (LiteLLM/Ollama/vLLM) and measure **task completion**, not single-call success (95%/call ≈
   66% over 8 steps). Confirms or kills the tier ordering — which is a hypothesis, not a result.

## 4. Coverage call (loop-until-dry)

One convergent round across four lenses; the candidate space is saturated (the major harnesses are
all surfaced and cross-assessed), and the lead finding is corroborated by ≥2 independent sources.
**Crucially, more searching cannot reduce the load-bearing uncertainty** — "does it complete
multi-step on local?" is answerable only by `shd-003`'s smoke test, not by literature. Directional
coverage is therefore **sufficient**; the residual is empirical, not searchable.

## 5. Follow-on

- **`shd-003`** (validated, `poc-required`): smoke-test the slate above against the §4 POC bar →
  first technology to move `partial`/`proven` on C2.
- Confirms methodology **L1** (live tool-call smoke is mandatory) — candidate `lesson-learned`.
