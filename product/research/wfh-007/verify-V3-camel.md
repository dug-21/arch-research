# verify-V3-camel.md — targeted verification: the CaMeL primary (H-B H16; S5's declared hole)

**Run:** `wfh-007` · Issue #64 · `wf-v0.24` · **agent_id:** `wfh-007-v3-scout` · targeted verification
**Status moves: 0.** Everything `claimed` at best. Authors' measured results and design claims are marked separately.
**Dedup:** `context_search` returns **no CaMeL node**. Nearest neighbours #202 (AgentCore+Cedar, ASSEMBLE) and #198 (gh-aw, ADOPT). **NEW to the graph.**

**S5's declared hole is closed.** Sources read: `arxiv.org/abs/2503.18813` (metadata) · `ar5iv.labs.arxiv.org/html/2503.18813` (full text) · `arxiv.org/pdf/2503.18813v2` (5.3MB, extracted locally, 125pp, 358,492 chars — source of the appendix tables) · `github.com/google-research/camel-prompt-injection` (README, tree, five source files via `gh api`). Failed: arXiv-native HTML (404 for v1 and v2).

---

## 1. The mechanism, precisely

**Three components plus an interpreter** [demonstrated — the released code implements all four].

**The P-LLM / Q-LLM split.** The Privileged LLM sees *only the user query and tool signatures*, and its output is not a tool call — it is **Python source code** expressing the task's control and data flow. The Quarantined LLM is the only component touching untrusted content; it has **no tool access**, is called through one in-language function `query_ai_assistant(prompt, output_schema)`, and returns structured data against a schema. The isolation is deliberately one-way and lossy: *"the Q-LLM cannot communicate to the P-LLM which data is missing, as this could introduce a prompt injection vector."* And: *"the P-LLM only interacts with the user query and not the data returned by tools or with the Q-LLM output."*

This is Willison's Dual-LLM pattern, and the paper says so; CaMeL's contribution over it is the capability layer.

**What capabilities attach to: values.** From `src/camel/capabilities/capabilities.py`:

```python
@dataclasses.dataclass(frozen=True)
class Capabilities:
    sources_set: frozenset[sources.Source]
    readers_set: readers.Readers          # frozenset[user] | Public
    other_metadata: dict[str, Any] = ...
```

Every runtime value is a `CaMeLValue` carrying `_metadata: Capabilities` **and** `_dependencies: tuple[CaMeLValue, ...]`. Not variables — values. `readers` is the `Public` singleton or a frozenset of principals (email addresses in the evaluation). `sources` ∈ `{CaMeL, User, Assistant, TrustedToolSource}` plus `Tool(tool_name, inner_sources)`.

**What the policy is checked on, and when.** Immediately before each tool invocation, on the tool's *keyword arguments* and, separately, on accumulated **control-flow dependencies**. From `src/camel/security_policy.py`:

```python
def check_policy(self, tool_name, kwargs, dependencies):
    if tool_name in self.no_side_effect_tools: return Allowed()
    non_public_variables = [d.raw for d in dependencies if not is_public(d)]
    if len(non_public_variables) > 0:
        return Denied(f"{tool_name} is state-changing and depends on private values {non_public_variables}.")
    for policy_name, policy in self.policies:
        if fnmatch.fnmatch(tool_name, policy_name): return policy(tool_name, kwargs)
    return Denied("No security policy matched for tool. Defaulting to denial.")
```

**Default-deny** on unmatched tools. And a blunt global rule: *any state-changing tool whose control-flow dependency set contains a single non-public value is denied outright*, before any per-tool policy is consulted.

**The effective label is computed lazily, at check time, over the transitive dependency closure** — the detail no summary carries. Labels are not eagerly stamped and propagated; the closure is re-walked on every check.

**Two interpreter modes, load-bearing.** **STRICT** adds the conditional test or loop iterable as a dependency of every variable assigned inside the block, *and* makes every statement following a `query_ai_assistant` call depend on that call's arguments. **NORMAL** does neither. STRICT is what closes the §7 side channels; NORMAL leaks. **STRICT is the security-sound configuration.**

**Error handling is a loop, not an exception:** *"The interpreter prompts the P-LLM up to 10 times to get code that fully runs."* Exception text with untrusted dependencies is redacted before being shown back.

---

## 2. What it defeats, and what it explicitly does not

**Threat model (§3).** *"The primary goal of CaMeL is to stop prompt injection attacks coming from untrusted data sources."* Trust assumptions: *"We assume that the user prompt is trusted, that the user is not pasting a prompt from an untrusted source, and, if there is a memory in place, the memory has not been compromised."* Formalized as the `PI-SEC` game.

**Explicit non-goals (§3.1), quoted because they bound the claim tightly:**
- *"CaMeL doesn't aim to defend against attacks that do not affect the control nor the data flow… it cannot defend against text-to-text attacks which have no consequences on the data flow, e.g., an attack prompting the assistant to summarize an email to something different than the actual content."*
- Injection-induced phishing is out of scope.
- *"CaMeL does not aim to make a fully autonomous system without any need for human intervention."*

**A CaMeL-specific attack the authors found themselves (§6.4).** If the query is *"monitor emails, find an action in the email, and execute it,"* the P-LLM legitimately writes a dispatch loop over all tools selecting one based on email content. *"This effectively turns data into control flow."* They weaponized it and observed Claude 3.5 Sonnet, o3-mini and o1 all generating exploitable plans. §9.3 draws the CFI/ROP analogy: *"an attacker might be able to create a malicious control flow by approximating it with the smaller control flow blocks that are allowed by the security policy."* **The "provable security" is conditional on the shape of the plan the P-LLM writes.** [demonstrated — authors' own construction]

### On runtime betrayal / rug-pull — correcting S5's steelman

**S5 wrote:** *"CaMeL's data-flow capabilities catch it; nothing in the cheap stack does."* **The primary supports a narrower claim.**

The malicious-tool case is **§8 "Secondary attack scenarios that CaMeL can help with" — Scenario 2, External Spy Tool.** The answer: *"security policy can be configured in a way that external tools cannot access internal information."* Three qualifications, all from the paper:

1. **Outside the primary threat model** — §8 is explicitly *secondary*, "even stronger than the well-known prompt injection threat model."
2. **Not measured.** *"…is not explicitly addressed in AgentDojo."* No experiment. Design claim, not result `[asserted]`.
3. **Exfiltration only.** CaMeL governs *what data reaches a tool*, never *what a tool does with data it was legitimately entitled to receive.* A postmark-mcp-shaped defection misusing data the policy correctly allowed is **not** in scope; nor is a tool taking a destructive action rather than leaking.

**Honest reading: CaMeL converts rug-pull-by-exfiltration from an approval-time problem into a runtime data-flow check — genuinely, and structurally stronger than any allowlist. It does nothing for rug-pull-by-misuse or rug-pull-by-destructive-action. S5's fourth-failure-class instinct survives; the claim that CaMeL closes it does not.**

**Side channels (§7), acknowledged and partly mitigated.** Loop-count inference via repeated external fetches; one-bit leakage via adversary-triggered exceptions; timing via a clock (blocked only because `time` is absent from the interpreter). STRICT mitigates the first two. Authors: *"we believe that other types of side channels might be possible… data can still be (inefficiently) mishandled."*

---

## 3. The label-explosion question — the one that decides H16

**The combination rule, read from the artifact.** `src/camel/capabilities/utils.py`:

```python
def get_all_readers(value, visited_objects=frozenset()):
    value_readers = value.metadata.readers_set
    for dependency in value.get_dependencies()[0]:
        new_value_readers, visited_objects = get_all_readers(dependency, ...)
        value_readers &= new_value_readers          # INTERSECTION
    return value_readers, ...

def get_all_sources(value, ...):
    value_sources = value.metadata.sources_set
    for dependency in value.get_dependencies()[0]:
        new_value_sources, visited_objects = get_all_sources(dependency, ...)
        value_sources |= new_value_sources          # UNION
    return value_sources, ...
```

**Readers intersect. Sources union. Both over the full transitive closure.** `Public.__and__` returns the other operand — `Public` is the lattice top. **Nothing anywhere in the released code moves a value *up* the readers lattice.**

**So, the summarization question answered exactly.** An agent reading three labeled values and writing one summary produces a value whose effective readers set is the **intersection** of all three, and whose sources set is the **union** of all three provenances. `is_trusted` requires *every* source in the union to be trusted, so a single untrusted contributor poisons trust for the whole aggregate. **This is monotone narrowing by construction — the classic IFC lattice collapse. CaMeL does not mitigate it; it implements it.** STRICT makes it strictly worse: every statement after a Q-LLM call inherits that call's arguments as dependencies, so the closure grows and the intersection shrinks monotonically as the run proceeds.

**Does the paper report the collapse?** The prose never says "over-tainting" or "label creep". **Appendix D quantifies it exactly, and this is the number H16 needs.**

**Table 8 — policy triggering rates when NOT under attack (benign runs), over successfully solved tasks:**

| Mode | Overall | Banking | Slack | Travel | Workspace |
|---|---|---|---|---|---|
| NORMAL | 33.87% | 58.33% | 60.00% | 0.00% | 16.67% |
| **STRICT** | **53.23%** | 58.33% | 80.00% | 80.00% | 33.33% |

**Table 9 — same, under attack:** NORMAL 26.54%; STRICT 45.34%.

**In the security-sound configuration, on benign runs with no adversary present, 53.23% of successfully solved tasks trip a security policy.** In deployment this is not a block — *"executions that violate security policies will not be blocked, but they will require user confirmation"* — it is **a human confirmation prompt on more than half of all benign tasks.** [demonstrated — authors' measurement]

One mitigating datum: **Workspace**, where principals are email addresses and labels come from real per-object ACLs, is the best suite at 33.33% STRICT. Fig. 10's caption: *"the workspace suite, where users are identified by their email address, has more granular security policies which get triggered less often."* **Granular, environment-sourced identity halves the false-fire rate. It does not remove it.**

**Declassification: named as the problem, no mechanism shipped.** §9.2 is titled *"De-classification and user fatigue"*:

> *"Access control problems often manifest in the process of de-classification process or 'downgrading'. This can lead to user fatigue, where users become desensitized to security prompts and may inadvertently approve malicious actions."*

That is the entire treatment. **There is no declassification primitive in the paper and none in the code.** The one place it could hide — `new_with_metadata()` on a tool's output — replaces `_metadata` but leaves `_dependencies` intact, and `get_all_readers` still walks the closure, so a tool-boundary relabel can only narrow further, never widen. **The sole declassifier in the system is the human, via the confirmation prompt, at the Table 8 rate.** §9.3: *"CaMeL suffers from users needing to codify and specify security policies and maintain them. CaMeL also comes with a user burden."*

**Where the labels come from — and this part *supports* H16.** Readers are **not hand-authored per run**. They are minted mechanically from the environment's existing authorization state by per-return-type adapters (`src/camel/pipeline_elements/agentdojo_function.py`):

```python
def _get_cloud_drive_file_metadata(file, editors, tool) -> Capabilities:
    return Capabilities(frozenset({sources.Tool(tool, _transform_user_email_to_user(editors))}),
                        frozenset(file.shared_with))

def _get_email_metadata(email, tool) -> Capabilities:
    email_readers = frozenset({email.sender} | set(email.recipients) | set(email.cc) | set(email.bcc))
    return Capabilities(frozenset({sources.Tool(tool, ...)}), email_readers)
```

Drive file readers = the file's actual `shared_with`. Email readers = sender ∪ recipients ∪ cc ∪ bcc. **Structurally the same move H16 proposes** — minting labels from an actor-independent declaration rather than an actor's assertion. Minting them from a contract's disclosure list is the same operation with a different source of truth. (Note also `Capabilities.other_metadata: dict[str, Any]` — a free-form extension slot already in the dataclass.) Caveat: adapters are **hand-written per return type**, and the Slack one carries an acknowledged approximation.

---

## 4. Cost

**Token overhead [demonstrated]:** *"CaMeL requires 2.82× input tokens and 2.73× more output tokens for the median task in AgentDojo."* Measured against native tool-calling (Claude 3.5 Sonnet backbone, under attack), tokenized with `tiktoken` (Claude's tokenizer is closed) and **excluding tool-documentation tokens** — a floor, not a ceiling. **Worst of every defense measured**; Spotlighting is 1.06×/0.98×.

**Latency [asserted, not measured].** *"The main latency overhead in code execution comes from maintaining the data flow graph… This requires minimal processing and storage."* **No latency numbers anywhere in the paper.** The real serialized cost is the up-to-10 P-LLM repair round-trips, never priced as latency.

**Task quality [demonstrated].** The abstract's *"77% of tasks… compared to 84% with an undefended system"* is **o3 High: 77.3% ± 8.3 vs 84.5% ± 7.2** [inferred — Table 2's o3 High row matches to the decimal]. The spread is much wider:

| Model (Table 2, overall) | Native | CaMeL | Δ |
|---|---|---|---|
| o4 Mini High | 79.4% | 76.3% | **−3.1** |
| o3 High | 84.5% | 77.3% | **−7.2** |
| Claude 4 Sonnet | 86.6% | 74.2% | **−12.4** |
| Claude 4 Sonnet (reasoning) | 83.5% | 70.1% | **−13.4** |
| Gemini 2.5 Flash | 55.7% | 35.1% | **−20.6** |
| Gemini 2.5 Pro | 73.2% | 41.2% | **−32.0** |

Per-suite the damage concentrates: Slack loses 23–43 points across every model; Travel goes to **0.0%** for both Gemini models. Table 5 (Claude 3.5 Sonnet, defense comparison) is worse: CaMeL **63.92%** vs undefended **90.72%** — the *lowest-utility* defense measured (Spotlighting 92.78%, Prompt Sandwiching 89.69%, Tool Filter 73.20%).

**Security result [demonstrated]:** successful attacks out of 949 drop to **0** for Gemini 2.5 Pro and o3 High (from 163 and 11), and to 1–11 for the others — every residual "success" being the same non-injection Travel task the authors classify as outside their threat model.

**Which tasks became unsolvable — Table 1.** Two failure modes are **inherent to the architecture**:
- **"Data requires action"** (5): *"the P-LLM would need to take action based on some data that only the Q-LLM sees."* — *"no existing model manages to solve this task."* Unsolvable by construction under the Dual-LLM split.
- **"Not enough context for Q-LLM"** (5): the Q-LLM can raise `NotEnoughInformationError` but cannot say *what* is missing, because that channel would itself be an injection vector.

The largest bucket — **Underdocumented API, 13, all Travel** — is not inherent, and shrinks with newer models (Claude Travel utility 25%→55%→75% across 3.5→3.7→4 with no CaMeL changes): the paper's strongest evidence that part of the utility gap is a model-capability artifact rather than a hard architectural cost.

**One cheap win:** the Q-LLM can be small. Claude 3.5 Haiku as Q-LLM under a Claude 4 Sonnet P-LLM costs *"about 1%"* utility for *"an estimated 12% reduction in cost for the median task."*

---

## 5. Adoptability

**Code:** `github.com/google-research/camel-prompt-injection` — **Apache-2.0**, 372★, 57 forks, ~1MB, primarily Jupyter Notebook, created 2025-05-13, **last push 2025-06-20 (≈14 months dormant)**, 1 open issue, not archived.

**It is a research artifact and the authors say so in a README warning block** [demonstrated — verbatim]:

> *"This is a research artifact released to reproduce the results in our paper. The interpreter implementation likely contains bugs (e.g., it might throw uncaught exceptions and crash) and the implementation might not be fully secure.*
> *This is **not** a Google product, and we are not planning to provide support for and/or maintain this codebase."*

Plus *"we are not planning to fix bugs"* and *"not eligible for the Google Open Source Software Vulnerability Rewards Program."* **A security control with no vulnerability-disclosure path and a self-declared possibility of being insecure.**

**Library or framework?** Neither — **an agent runtime, and it replaces yours.** The tree is a full custom Python AST interpreter (`interpreter/{interpreter,library,namespace,op_protocols,result,value}.py`) plus the capability system plus an AgentDojo-specific pipeline. `main.py` is a benchmark harness, not a general entry point.

**Does it require the agent to emit code rather than call tools? Yes — unavoidably.** Architecture, not implementation choice. Native tool-calling APIs are the *baseline it is measured against*, not a supported mode.

**Compatibility with an MCP tool-calling estate — honest answer.** MCP tools could in principle be wrapped as interpreter-namespace callables the way `AgentDojoFunction` wraps AgentDojo functions, and MCP's schema'd I/O is a reasonable fit for that adapter shape. Two things do not survive:
1. **The agent loop must be replaced.** Any harness whose model emits `tool_use` blocks cannot be retrofitted. **No incremental adoption path.**
2. **Every tool needs a hand-written label adapter.** MCP carries no capability metadata whatsoever. Someone must write, per tool and per return type, the function that reads the underlying system's authorization state and constructs `Capabilities(...)`. **Where no such authorization state exists, there is nothing to mint from and the label must be invented — reintroducing the trusted-assertion problem the design exists to remove.**

**The authors' own adoption verdict (§9.1)**, blunter than anything I would write:
> *"Building a capability-based system requires significant effort and resources, as it requires a fundamental shift in how security is managed and enforced."* — with **CHERI** cited as the case study, requiring *"a redesign of the full software-hardware stack."*
> *"Capability-based systems ideally require full participation from the entire ecosystem… all external tools and services within the environment must be designed to understand and utilize capabilities, otherwise utility degrades."*

**Lock-in and exit.** Adoption means owning a custom Python interpreter as the trust boundary of the estate, unmaintained upstream, whose authors decline to assert it is secure. Exit is cheap in one direction only: the *labels* and *policy functions* are small, portable and independently valuable (`capabilities/` is ~150 lines); the interpreter is not. §10: *"Programming languages that handle errors and I/O more explicitly, such as Haskell, might be a more secure choice for deploying CaMeL to real-world applications."*

---

## Decision line

**Contract-minted taint labels: VIABLE-WITH-NAMED-LIMITS as a mechanism, NOT VIABLE as an estate-wide control at our scale — and the binding limit is not the labels, it is the missing declassifier.**

1. **The minting move H16 conjectures is confirmed possible, and is not novel.** CaMeL already mints readers sets from an actor-independent, machine-readable authorization source. Minting from a contract's disclosure field is the same operation with a different source of truth. **H16's core structural claim survives contact with the primary.**
2. **The lattice behaves exactly as the classic failure mode predicts, and the paper measures the cost.** Readers intersect over the transitive closure; nothing widens either set. **53.23% of benign, adversary-free, successfully-solved tasks trigger a policy in STRICT.** H16's cheapest test proposes to *"count label-lattice blowup and needed declassifications"* — the primary already supplies a strong prior, and it is roughly **one interruption per two benign tasks**, in a closed environment with hand-tuned per-suite policies and real ACLs to mint from. A cross-program contract corpus has neither.
3. **The declassifier is the hole, and it is unsolved upstream.** The paper names it as the central tension (§9.2), cites the user-fatigue literature against itself, and **ships no mechanism**. Any adoption inherits an unsolved problem whose failure mode — desensitized approval — is the same approval-fatigue path H-B H5 already flags as escalation-laundering in this run's own hypothesis set.

**What that leaves.** The mechanism is real and the strongest published thing of its kind; S5 was right to call it the steelman's best exhibit. But "enforceable rather than trusted" costs, at the measured rate: **2.8× tokens, 3–32 utility points depending on model, a replaced agent loop, a hand-written label adapter per tool return type, an unmaintained interpreter as the trust boundary, and a human in the loop on half of benign work.** A plausible price for **one narrow, closed, high-value flow with a real ACL to mint from and a small tool surface** — implausible for a general estate.

**Two corrections to positions already on file:**
- **S5's steelman overstates the rug-pull claim** (see §2). The instinct survives; the claim that CaMeL closes it does not.
- **"Provable security" is conditional on plan shape.** §6.4's dispatch-loop attack — authors' own construction, reproduced by three frontier models — turns data flow back into control flow inside a valid CaMeL program, and §9.3 concedes ROP-style gadget-chaining against the policy set is likely to work.

**H-B H17's bound is unaffected but its exposure leg now has a price.** The IFC mapping's conclusion that exposure is *"enforceable only if something like this works"* is answerable: it works, it is measured, and it costs a human confirmation on half of benign traffic absent a declassifier nobody has built.

---

## What I could not establish

- **Latency.** Not measured anywhere. Interpreter overhead *asserted* negligible; the up-to-10 repair round-trips never priced.
- **Absolute dollar/token cost.** Only ratios, against an unstated baseline, with the wrong tokenizer and excluding tool-doc tokens.
- **Whether NORMAL or STRICT is the shipped default.** The paper presents both and demonstrates NORMAL leaks (§7). It never states the default. **Changes the Table 8 number by 20 points** — flagged rather than guessed.
- **Whether the code implements the paper's claimed guarantees.** Capability and policy layers read; the ~6-file interpreter not audited, and the authors decline to assert it is secure.
- **Any post-June-2025 development.** Repo dormant 14 months; no successor search (targeted verification, not discovery). The related-work section names five concurrent efforts (Zhong et al. 2025; Abdelnabi et al. 2025; Kim/Choi/Lee 2025; Li et al. 2025; Costa et al. 2025) — **none fetched, and at least one (Zhong) is described as using coarser private/public + trusted/untrusted labels, closer to the granularity H16/H17 actually propose than CaMeL's per-principal readers sets.** Declared hole, and arguably the more relevant literature for our label granularity.

---

## Citations (D14)

```yaml
- type: paper
  ref: arXiv:2503.18813v2
  title: Defeating Prompt Injections by Design
  author: Debenedetti; Shumailov; Fan; Hayes; Carlini; Fabian; Kern; Shi; Terzis; Tramèr
  org: Google; Google DeepMind; ETH Zurich
  year: 2025
  surface: literature

- type: repo
  ref: github.com/google-research/camel-prompt-injection
  title: "CaMeL: Defeating Prompt Injections by Design (research artifact, Apache-2.0)"
  org: Google Research
  year: 2025
  surface: active-dev
```

**Named in related work, NOT fetched** — for the derived watchlist, not cited as evidence: Zhong et al. 2025 (coarse integrity/confidentiality labels via classifier); Abdelnabi et al. 2025; Kim, Choi & Lee 2025; Li et al. 2025; Costa et al. 2025; Wu et al. 2025; **Bagdasaryan et al. 2024 / Ghalebikesabi et al. 2024 (AirGap** — named by the authors as the contextual-integrity route to *automating* policy authorship; **the most directly relevant unread item for the declassification hole)**.
