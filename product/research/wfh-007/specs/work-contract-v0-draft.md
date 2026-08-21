# DRAFT — Cross-program work contract, v0

> **Status: DRAFT. `claimed`, not `proven`, and not ratified.**
>
> This document is the output of one bounded authoring job assigned to `factory-architect`
> (`agent_id: wfh-007-architect`). It is **not** a chartered research scope, it did not run under a
> `context_cycle`, it moved nothing in the graph, and no agent wrote to Unimatrix on its behalf.
>
> A specification is a *claim about what would work*. Nothing here is proven by the fact that it is
> written down, and nothing here becomes proven by being well argued. Under D7 only an artifact
> demonstrated by us moves a grade, and this document is not one.
>
> It has not passed goal-owner review, validator check, or the owner's ratification. Treat every
> clause as a proposal.

**Author:** `factory-architect` · **Run:** `wfh-007` · **Date:** 2026-08-21
**Corpus:** `OWNER-DIRECTION.md` §5/§7/§8/§10/§12 · GitHub Issue #40 (`dug-21/arch-research`) ·
12 `SCOPE.md` files · `reports/triage.md` §2.2/§3/§6 · `hypotheses-HA-contract-phase.md` (H14–H16,
H22–H30, consolidated ledger) · `hypotheses-HD-federation.md` (H3, H4, H8–H11, H18–H19) ·
`verify-V2-cedar.md`, `verify-V4-dogwood.md` · `.claude/rules/unimatrix-access.md` (D6, D7, D8) ·
`.claude/workflow/research-scope.md`

---

## 1. The objective, restated

The owner is currently the wire between two programs. When the software-delivery program needs
something from the research garage, a human carries the request across, decides what may be disclosed,
translates the vocabulary, judges whether the answer is good enough, and routes what happens next.
§8 asks for a record that mechanises the carriage while leaving the judgement gates where the owner
put them.

Exactly one machine-to-machine exchange has ever occurred (Issue #40). It is the entire empirical
corpus. It succeeded at the work and **failed at the exchange**: five weeks later it is still `OPEN`,
with no completion signal of any kind. Nobody ever said "accepted."

So the thing to define is: **the record one program sends another when it needs work done, plus the
records that close the loop** — precise enough that a stranger could implement it, and precise enough
that a second stranger could check whether they did.

Three constraints frame it, and they come from the owner rather than from me:

1. **GitHub Issues may be a transport and a human surface. They must not be the semantic protocol.**
   The record must survive Issues, Unimatrix, local queues, hosted runtimes, and channels that do not
   exist yet.
2. **Free-form conversation obscures delegation, authority, acceptance, and provenance** (§8). The
   record exists to make those four legible, not to make agents chatty in YAML.
3. **An LLM is not the final authority over another LLM** (§5.1), and **agents cannot change active
   policy** (§5.2). Anything this record claims to enforce must be enforced somewhere an agent cannot
   reach — or the claim must be withdrawn.

The third one is the whole difficulty, and §6 below is where I confront it rather than decorate it.

---

## 2. Two rulings I was asked to make, made

The leader asked me to rule explicitly on two "do not author this" candidates rather than leave them
hanging. Both are ruled. Neither ruling is "do not author," but one of them substantially shrinks
what gets authored and the other refuses a collapse the run was hoping for.

### Ruling A — §8's work contract and §10's elevation pipeline are **not one object**. They share exactly one of the three records.

Triage S-3 carried the sub-claim that if the work contract and the second-brain elevation pipeline
are the same object, "it halves the architecture scope." They are not, and it does not. But the claim
is not wrong either — it is *aimed at the wrong grain*.

Compare the two directly:

| | §8 work contract | §10 elevation |
|---|---|---|
| Who initiates | the party that **wants** something | the party that **has** something |
| Direction of authority | requester grants (or withholds) authority to act | destination authorises ingestion |
| Is there work? | yes — a bounded deliverable is performed | no — nothing is executed; material is republished |
| Budget / expiry / retry | meaningful | meaningless (nothing runs) |
| Classification decision | at export time, by the source | at export time, by the source |
| Evidence check | against a declared floor | against a declared floor |
| Origin retention | needed on the return | the entire point |

The **request** half of §8 has no counterpart in §10 at all. Delegated authority, budget, expiry,
retry, cancellation and a bounded deliverable are request-shaped and elevation has none of them.

But the **return** half is the same record. An evidence-graded, classified, origin-retaining artifact
crossing an ownership boundary with a named acceptor and a recorded disposition is what §8's response
is and what §10's elevation is. §10 is a §8 exchange with the work part null and the source as
initiator.

**Ruling: define the RETURN record once and let §10 reuse it.** The architecture scope falls by the
size of the disclosure/classification/provenance leg — real, useful, and considerably less than half.
Anyone who reports this as "the collapse survived" is overstating it; anyone who reports it as
"they are unrelated" is missing the reuse. `§4.3` below is the shared record, and it is marked as such.

*(This ruling is derivable in an afternoon, as triage predicted, and I derived it from the two
documents rather than from a test. It is a reading, not a measurement. A falsifier: attempt to express
one real elevation using §4.3 alone and see whether a field is missing that only elevation needs —
"which categories may elevate automatically" is the likely candidate, and it is a policy input, not a
record field.)*

### Ruling B — the HA net structural read (phase and contract as one parameterized record) is **rejected as a v0 design commitment, and accepted as a target invariant**.

The HA ledger's net read is that the collapse survives as *one record type with three parameterized
differences* — signer/issuance-time, verification profile, disclosure discipline. If that held today,
this specification would be a parameterization of the phase record the estate already runs
(`context_cycle` phase-end plus the capability node's `done_when` / `proven_by` / `grade:` triple),
not a new type.

I am rejecting it for v0 on the ledger's own terms. Fracture #1 says the collapse holds only where
**every transition is a signed, checkable record** — it "costs the full Cluster D apparatus as a
precondition." We do not have that apparatus. D6 says attribution does not persist and `agent_id` is
a self-reported string; Issue #40's own executor identity (`jurati-req-researcher`) is unattested.
Declaring the two records one type today would assert a unification whose precondition is absent, and
the assertion would be believed. Fracture #5 says the same thing more mildly: phase and contract
"remain distinct roles of the one type — issuance-time is a parameter with teeth."

Accepting it as a target invariant has teeth of its own, and I have paid them here:

- **I define no new acceptance vocabulary.** §4.2's `acceptance` block reuses `done_when`,
  `proven_by` and `grade:` **by name**, with the estate's existing meanings (H15). The contract's
  acceptance check *is* the D7 firewall check, at a boundary.
- **I define no new evidence grades.** `missing | claimed | partial | proven` as they already exist.
- **I define no new disposition lifecycle for the intra-domain case.** Phases keep `phase-end`.

So the contract is a **superset of the acceptance triple plus an issuer across a trust boundary**, not
a parallel system beside it. **Re-open the collapse when both preconditions land: (a) D6 resolved so
identity is attested, and (b) phase transitions emit signed records.** Until then, one type is a claim
we cannot check, and the specification says so instead.

---

## 3. What I refused to author, and why

Three things the corpus or the triage pointed at, which I decided not to put in v0.

**3.1 — A signature envelope (DSSE / PAE).** H9 and triage Q4 both want classification bound to the
payload so a label cannot be stripped in transit. The mechanism is right. But **its falsifier is
unrun**: nobody has posted a signed contract through a real Issue round trip including a human edit
to see whether quoting, reformatting and GitHub's whitespace normalisation break signatures. Writing
a signature requirement I cannot know is satisfiable on the estate's only working transport would put
a clause in the specification whose first real use fails. Instead I **adapted the move and dropped
the cryptography**: canonicalise, then bind by content hash (C6, C7). A hash gives tamper-evidence
within the chain, survives reformatting because it is computed over the canonical form rather than the
rendered text, and can be recomputed by a human. It does **not** give non-repudiation. That is a
stated downgrade, not an oversight. Upgrade path in §11 Q5.

**3.2 — A partition claim as a contract field.** Triage §6 Q6 lists a partition claim among the
in-scope additions, and H16 proposes it as the thirteenth field. The HA ledger's own fracture #7
contradicts them: *"the fan-out partition lives naturally in the layout, not the contract — evidence
the workflow-as-whole retains at least one irreducible job."* I side with the ledger. Across a trust
boundary the issuer cannot see the executor's concurrent contracts, so a partition claim can only
describe the issuer's own fan-out — which the issuer's layout already knows and nobody at the other
end can check. An optional field one party fills and no party checks is fat, and fat gets implemented
forever. **Cut. Recorded as open question Q6.**

**3.3 — A rich grammar for delegated authority.** §8 field 4 asks for "authority delegated with the
request," and H4 wants it to be a token chain (Biscuit-style, monotone attenuation, cryptographically
verified). That is the right end state. It is unimplementable here because **nothing in this estate
mints authority**. Issue #40 is the evidence: the requester granted nothing; it *constrained itself*
("read-only queries only"), and the executor's compliance was voluntary and self-attested. A field
called `authority.granted` populated by an unattested requester, verified by nobody, would be the
single most dangerous thing in this document — it would read like a grant and behave like a wish.
So C13 defines the field **and forbids it from being non-empty** until a minting authority exists,
while C14 records what actually happened in the one real exchange: a *self-limit*, declared by the
requester, binding by convention. Naming the convention as a convention is worth more than dressing
it as a grant.

---

## 4. The record

**Shape: one envelope, four body types.** This is where the HA parameterization idea belongs — at the
grain of the exchange, not at the grain of phase-vs-contract. Everything that crosses is the same
envelope; only the body varies.

```
ENVELOPE
  ├── body: REQUEST      — issued by the requesting program
  ├── body: RETURN       — issued by the executing program   ← shared with §10 elevation
  ├── body: DISPOSITION  — issued by the acceptor
  └── body: AMENDMENT    — issued by the request's issuer only
```

Serialisation is a mapping (JSON or YAML). Field names below are normative. `MUST` / `MUST NOT` /
`MAY` carry their usual force. Every constraining clause is numbered `C<n>` and carries a provenance
mark and an enforcement tier — see §5 and §6.

### 4.1 The envelope

```yaml
schema:         work-contract/v0        # C1
contract_id:    <string, stable for the life of the exchange>
record_type:    request | return | disposition | amendment
seq:            <integer, 0-based, monotonic within contract_id>
prev:           <hex hash of the canonical form of record seq-1, or null when seq == 0>
issued_at:      <RFC3339 UTC>
issuer:
  program:      <string — the program/repository, e.g. dug-21/jurati>
  principal:    <string — the acting role or agent id>
  identity_basis: self-asserted | registry-asserted | attested
body:           <one of §4.2 – §4.5>
```

### 4.2 REQUEST body

```yaml
objective:      <one sentence — what is wanted>
grounds:        <what upstream claim or blockage this serves>

deliverables:                       # one or more
  - id:         <string, unique within the contract>
    statement:  <what is to be produced>
    done_when:  <the condition under which this item is complete>
    checked_by: mechanical:<named check> | judgement:<principal>
    priority:   required | droppable

effects_permitted: read-only | writes-local | external-send

authority:
  granted:      []                  # see C13 — MUST be empty in v0
  self_limit:   [<string>, ...]     # bounds the requester declares on its own ask

disclosure:
  complete:     true | false        # true asserts nothing beyond `items` was handed over
  items:
    - ref:            <pointer to the material disclosed>
      classification: public | internal | sensitive
      onward:         none | cite-only | redistribute

acceptance:
  evidence_floor: missing | claimed | partial | proven
  acceptor:       owner | program:<id> | principal:<id>

out_of_scope:   [<string>, ...]

return_to:
  channel:      <transport, e.g. github-issue-comment>
  address:      <where, e.g. dug-21/arch-research#40>

expires:
  by:           <RFC3339 UTC>       # required — C17
  after:        <optional resource bound, e.g. "3 owner gates" or "$X">
```

### 4.3 RETURN body — *this is the record §10 elevation reuses (Ruling A)*

```yaml
fulfils:        <contract_id>

results:
  - id:         <deliverable id from the request>
    outcome:    delivered | partial | refused | not-attempted
    evidence:                       # zero or more
      - kind:   <what sort of evidence this is>
        ref:    <pointer to it>

provenance:
  executor:        <who ran it>
  identity_basis:  self-asserted | registry-asserted | attested
  method:          [<the calls or steps actually issued>, ...]
  attestation:     <the executor's own statement about how it worked>

substitutions:                      # required if any deviation occurred
  - deliverable_id: <id>
    requested:      <what was asked>
    performed:      <what was done instead>
    reason:         <why>

disclosures_made:                   # what crossed back, and under what rules
  - ref:            <pointer>
    classification: public | internal | sensitive
    onward:         none | cite-only | redistribute
```

### 4.4 DISPOSITION body

```yaml
fulfils:        <contract_id>
outcome:        accepted | accepted-with-deviations | rejected | superseded | expired | abandoned
acceptor:       <principal — MUST match the request's acceptance.acceptor>
basis:                              # one entry per deliverable
  - id:         <deliverable id>
    cleared:    true | false
    note:       <why>
owner_acted:    approved | did-not-object | n/a
```

### 4.5 AMENDMENT body

```yaml
fulfils:        <contract_id>
amends:         <dotted path into the request body, e.g. deliverables[3].done_when>
change:         <the new value>
reason:         <why>
```

---

## 5. Clauses, with provenance and enforcement

Provenance marks: **D** = derived (the evidence supports it directly) · **A** = adapted (a shipped
pattern, changed to fit) · **X** = authored (my call).

Enforcement tiers (defined in §6): **E0** nothing checks it · **E1** a pure function of the record
could check it, and no such checker exists · **E2** an existing chokepoint checks it · **E3** a
chokepoint the bound party cannot reach checks it.

### 5.1 Envelope clauses

| # | Clause | Prov | Source / change | Enf | Enforcement point |
|---|---|---|---|---|---|
| **C1** | Every record MUST carry `schema: work-contract/v0`. A consumer that does not recognise the value MUST refuse the record rather than best-effort parse it. | **D** | Issue #40 carried no schema version of itself, and the two sides *did* disagree about schema (`wf:<version>` vs `wf-v<semver>`; string vs integer ids). The response had to open with two unsolicited corrections. | **E1** | A parser. None exists. The refusal behaviour is what makes the version load-bearing rather than decorative. |
| **C2** | `contract_id` MUST be stable across all records of one exchange and MUST NOT be a transport identifier (an Issue number, a URL, a queue key). | **D** | §8: Issues "must not become the semantic protocol." #40 had no id of its own; the exchange *was* the Issue. | **E1** | A linter matching `contract_id` against transport-shaped patterns. None exists. |
| **C3** | `record_type` MUST be one of the four. No fifth type may be introduced without a schema version bump. | **X** | Rests on: four is what the observed exchange plus its measured failure require (request, return, the disposition that never came, the deviation that did). | **E1** | Enum validation. None exists. |
| **C4** | `seq` MUST be 0 for the request, and MUST increase by exactly 1 per subsequent record. | **X** | Rests on: gaps are the only cheap way to detect a record that was dropped in transport. | **E1** | Arithmetic over the record set. None exists. |
| **C5** | `seq: 0` MUST be `record_type: request`. | **X** | Rests on: the exchange begins with an ask; a return with no request is a volunteered artifact, which is a §10 elevation, not a contract (Ruling A). | **E1** | As C4. |
| **C6** | The **canonical form** of a record is: the mapping serialised as JSON, keys sorted lexicographically at every level, no insignificant whitespace, UTF-8, `\n` line endings, null-valued keys omitted. All hashes are SHA-256 over the canonical form. | **A** | Adapted from DSSE's PAE. **What I changed:** dropped the signature, kept the canonicalise-then-bind move. **Why:** the PAE-over-GitHub falsifier is unrun (triage Q4); a signature that breaks on a human reformat is worse than a hash a human can recompute. **Cost of the change: no non-repudiation.** | **E1** | A canonicaliser plus `sha256`. Twenty lines. None exists. |
| **C7** | `prev` MUST equal the hash of the canonical form of the record at `seq-1`, and MUST be `null` at `seq: 0`. | **A** | Same adaptation as C6. Gives tamper-evidence within the chain without a key. | **E1** | As C6. Note: an executor that can write the whole file can rewrite the whole chain. This detects *transport* tampering and *transcription* error, **not a malicious party at either end**. Stated plainly because the difference is the entire value of the clause. |
| **C8** | `issuer.identity_basis` MUST be `self-asserted` in v0 for every record. `registry-asserted` and `attested` are reserved and MUST NOT be used. | **D** | D6: attribution does not persist; writes record `created_by: anonymous`; `agent_id` is a self-reported string. HD H3: identity-by-assertion "does not fail loudly; it fails by recording nothing." #40's `jurati-req-researcher` is a live instance. | **E1** | Enum validation. **The point of the clause is not the check** — it is that the record states its own ceiling instead of implying an identity it does not have. |
| **C9** | **A return MUST NOT be accepted at an evidence grade above `claimed` while any record in the chain carries `identity_basis: self-asserted`.** | **D** | D7 (`proven` only on an artifact demonstrated **by us**) composed with D6 (identity unattested). Across a boundary the artifact was demonstrated by *them*, under an unverifiable identity. | **E2** | The curator's write path — the estate's one graph-plane chokepoint. **But see §6.3 and §10: the curator is an LLM following a markdown rule, and §5.1 says an LLM is not a final authority. Treat this as E2-nominal, E0-actual.** |

### 5.2 Request clauses

| # | Clause | Prov | Source / change | Enf | Enforcement point |
|---|---|---|---|---|---|
| **C10** | A request MUST carry `objective`, `grounds`, at least one `deliverable`, `out_of_scope`, `return_to`, `acceptance`, `disclosure`, `effects_permitted`, `authority`, and `expires`. | **D** | Ten of these map onto fields present in either the 12/12 `SCOPE.md` core (question, why, proof bar, out-of-scope, coverage) or Issue #40's actual body (issuer, objective, enumerated items, per-item acceptance, scope limit, return channel). Two (`expires`, `disclosure`) are required on the **measured-failure** rule in C11. | **E1** | Presence check. None exists. |
| **C11** | **Requiredness rule (normative, for anyone extending this schema):** a field is REQUIRED only if it was present in the one real exchange, **or** it is in the 12/12 intra-corpus core, **or** its absence caused a measured failure. Everything else is OPTIONAL or absent. | **X** | Rests on: the triage's non-negotiable "derive before authoring," made operational. It is the rule that kept budget (2/12, no observed failure), roles (1/12), model/runtime provenance on the request side (absent, no observed failure), and the partition claim out of v0. | **E1** | A reviewer with the frequency table. **This clause binds future authors, not agents** — its real enforcement is that it is written down and citable. |
| **C12** | Each deliverable MUST carry `done_when` **and** `checked_by`. `checked_by` MUST be either `mechanical:<named check>` or `judgement:<principal>`. A `done_when` with no named checker is not a valid deliverable. | **X** | Rests on: the architect's own enforcement-point discipline, made structural — the record forces its users to name who checks each item. It also **prevents the fake-precision failure** that P-2 (unrun) would otherwise expose: if the checkable-`done_when` denominator is low, `judgement:` absorbs it honestly instead of prose being laundered through a field labelled machine-checkable. | **E1** | Syntactic: the value matches one of two prefixes. **Non-vacuity is not checkable syntactically** — P-2's disjointness test (the checker's input set disjoint from the executor's write-set) is the real check and it is unrun. |
| **C13** | `authority.granted` MUST be `[]` in v0. A non-empty `granted` MUST cause the record to be refused. | **X** | Rests on: nothing in this estate mints authority. Issue #40 granted nothing. §5.1 and §5.2 say deterministic policy outside the model authorises effects and agents cannot change active policy. A grant field populated by an unattested party and verified by nobody reads as a grant and behaves as a wish. **See §3.3.** | **E1** | Emptiness check. **This is the clause most likely to be quietly relaxed under growth pressure and it should be the loudest one in the file.** |
| **C14** | `authority.self_limit` records bounds the requester declares on its own ask. It is **binding by convention only** and the record MUST NOT be read as granting or withholding anything. | **D** | Issue #40 verbatim: *"Scope note: read-only queries only."* The requester constrained itself; authority was ambient; compliance was voluntary and self-reported in the response's method attestation. | **E0** | **Nothing checks this today.** A convention named as a convention. |
| **C15** | `effects_permitted` MUST be declared in the **executor's** action space, not the issuer's, using the three-value enum. `external-send` MUST additionally carry `acceptance.acceptor: owner`. | **A** | Adapted from HD H8 ("consequence class does not survive the crossing; the contract must re-derive it") and triage S-4 / Q3 ("external representation: there is no mechanism to build; there is a policy for the owner to write"). **What I changed:** H8 puts re-derivation on the executor at execution time; I put a coarse, cross-domain-meaningful three-value class on the request because #40 already carried one (`read-only`) and a richer taxonomy is a taxonomy-authoring project. | **E1** for the enum and the owner-acceptor pairing. **E0** for whether the declared class is *true*. | An external send touches only the OS egress allowlist, which is resource-shaped. **An irreversible send to an allowed domain is invisible to all three consequence-aware planes** (triage S-4). This is a known, unclosed hole and the clause does not close it. |
| **C16** | `disclosure.items` MUST enumerate every material made available to the executor. `disclosure` MUST NOT be attenuated by any later record; an amendment MAY add items and MUST NOT remove them. | **A** | Adapted from HA H25 (information does not attenuate; enumerated materials, in-toto style) and HD H10 (export-time classification is the source curator's job). **What I changed:** H25 wants staged disclosure; v0 has one stage, because staging is unexercised and C11 would cut it. | **E1** for append-only-ness across the chain. **E0** for completeness. | A diff of `disclosure.items` across records is mechanical. **Whether the list is complete is not checkable by any mechanism here** — H25's real test (diff deliverable content against the disclosure list) needs a content checker nobody has built. The `complete: true` flag is an assertion by the party with the incentive to assert it. |
| **C17** | `expires.by` (wall-clock) is REQUIRED. `expires.after` (resource-denominated) is OPTIONAL. | **A** | Adapted from HA H30, which argues expiry should be denominated in attention and budget rather than wall-clock. **What I changed: I inverted the priority, and this is a deliberate departure from the hypothesis.** **Why:** H23 — across a trust boundary the issuer cannot observe the executor's consumption, and H30 itself concedes "a staller can stop attesting, so expiry must fire on attestation silence, quietly reintroducing a clock." A wall-clock bound is the only expiry the issuer can evaluate with **zero cooperation from the executor**. Resource denomination stays available for the intra-domain case where an observer exists. | **E1** | A clock and a comparison. See C22 — this is the clause that fixes the one *measured* failure in the corpus. |
| **C18** | `acceptance.evidence_floor` and the values in `results[].evidence[].kind` MUST use the estate's existing vocabulary (`missing|claimed|partial|proven`; `done_when`/`proven_by` semantics per D7). This specification defines **no new evidence vocabulary**. | **D** | HA H15 (`done_when` + `proven_by` + grade is half a contract already) and Ruling B. Triage S-2 already routes the evidence-kind floor as an assemble over C15/D7. | **E2-nominal** | The D7 firewall at the curator. Same caveat as C9. |

### 5.3 Return clauses

| # | Clause | Prov | Source / change | Enf | Enforcement point |
|---|---|---|---|---|---|
| **C19** | A return MUST carry one `results` entry per deliverable in the request, including for deliverables not attempted (`outcome: not-attempted`). | **D** | #40's response answered per item with per-item headers (`Targeted: goal_id = 113`, `Canonical call issued: …`). Item #5 was droppable; the response's handling of it is exactly what `not-attempted` names. | **E1** | Set comparison between request ids and return ids. None exists. |
| **C20** | `provenance.method` and `provenance.attestation` are REQUIRED. | **D** | **The strongest derived clause in the file: the responder volunteered exactly this and the request never asked for it.** #40's response carried the calls issued, per-item targets, and an unprompted method attestation — *"every call above was read-only. `agent_id` was passed on all calls. Nothing was written to the graph."* Usage wrote this field, not me. | **E0** | **Nothing checks that an attestation is true.** It is an executor's statement about its own behaviour. Its value is that it is *specific enough to be falsified later* by someone with log access — which is a different and lesser property than being checked. |
| **C21** | If the executor deviated from any `deliverables[].statement`, `substitutions` MUST record it. A deviation not recorded is a non-conforming return. | **D** | #40's request pre-authorised deviation — *"if any no longer match your schema, run the nearest equivalent and note the substitution"* — and the response used it (integer `seed_ids`, not strings; noted up front). Both halves of the pattern are in the real exchange. | **E0** | **Nothing checks that a deviation was declared.** A diff of `performed` against `statement` catches a *declared* deviation, never an undeclared one. This is the executor marking its own homework, and the specification should not pretend otherwise. |
| **C22** | `disclosures_made` MUST classify everything crossing back. This block, with `provenance` and `results`, is the record §10 elevation reuses (Ruling A). | **A** | Adapted from HD H9 (classification must be authenticated *with* the payload) and §10's "second-brain entry retaining its origin." **What I changed:** dropped authentication (see §3.1); the classification travels as a field, tamper-*evident* via C7, not tamper-*proof*. | **E0** | **Nothing checks a classification.** HD H10's falsifier — hand a curator ten mixed entries and score misclassification — is unrun, and its result determines whether classification can be delegated at all or routes to the owner. |

### 5.4 Disposition and lifecycle clauses

| # | Clause | Prov | Source / change | Enf | Enforcement point |
|---|---|---|---|---|---|
| **C23** | An exchange is **not complete** without a disposition record. A return is not an acceptance. | **D** | The one measured failure in the corpus. Issue #40: request → response → nothing, five weeks, still `OPEN`, no completion signal. This clause exists because that happened. | **E1** | Presence of a `record_type: disposition` in the chain. None exists. |
| **C24** | **Expiry is self-executing.** A contract whose `expires.by` has passed with no disposition record **is** `expired`. No party need act for this to be true, and any party MAY write the disposition recording it. | **X** | Rests on: requiring someone to *declare* expiry recreates exactly the failure it fixes — #40 stayed open because closing it was somebody's discretionary act and nobody's obligation. Making the terminal state a **pure function of the record and a clock** removes the dependency on anyone's diligence. | **E1** | `now() > expires.by AND no disposition`. Three lines. **This is the highest value-per-line clause in the document and it exists because of an n=1 observation.** |
| **C25** | `disposition.acceptor` MUST match `request.acceptance.acceptor`. A disposition from any other principal is non-conforming. | **X** | Rests on: owner open question #3 ("who accepts returned work") is the owner's to answer, but the record must not be *unusable* while it is open. The requester names the acceptor at issuance; the answer becomes a per-contract value rather than a global architecture decision. | **E1** | String comparison. Note C8: both sides are self-asserted strings, so this checks *declaration consistency*, not identity. |
| **C26** | v0 default: `acceptance.acceptor: owner`. | **D** | §5.1 — an LLM cannot police itself or another LLM as the final authority. Any other default would put a model at the end of the acceptance chain. | **E0** | Nothing checks it; it is a default, and defaults drift. |
| **C27** | `owner_acted` MUST distinguish `approved` from `did-not-object`. | **D** | Triage B-1, verbatim: *"a record that distinguishes an owner's approval from an owner's silence."* And its consequence — a naive reconstruction "counts every action the owner never saw as a success, systematically, in the agent's favour, forever — directly corrupting the twenty-run counter §5.7 specifies." **Unbackfillable**: a record tagged coarse can be re-binned; an untagged record can never be binned at all. | **E0** | Nothing checks it. **But its absence is unrecoverable**, which is why it is required despite being unenforceable — the rare case where an E0 field earns its place. |
| **C28** | An `amendment` MUST be issued by the request's issuer. An executor MUST NOT amend the request it is executing. | **A** | Adapted from HA H27 / aviation MEL: typed, time-boxed, pre-enumerated permitted non-compliance, **granted by an authority distinct from the operator**. **What I changed:** dropped the pre-enumerated deviation taxonomy — H27's own cheapest test (retro-enumerate deviations across wfh-005/006/007 and check whether a small typology covers ≥80%) is unrun, and authoring a taxonomy on an unrun test is exactly the taxonomy-authoring project the run was told to avoid. | **E1** | `amendment.issuer.program == request.issuer.program`. Self-asserted on both sides (C8). **H27's own risk applies verbatim: "if the leader both operates and amends, this is Cluster H with extra steps."** |
| **C29** | The request's `objective` and `acceptance.evidence_floor` MUST NOT be amended. Amendments may narrow or clarify deliverables; a changed objective is a new contract. | **X** | Rests on: an amendable objective makes the disposition meaningless — anything can be `accepted` if the ask can be moved to meet the answer. This is the monotone-narrowing invariant (H4) applied to scope instead of to authority, which is where we can actually enforce something. | **E1** | Path check on `amends`. None exists. |

### 5.5 Transport clauses

| # | Clause | Prov | Source / change | Enf | Enforcement point |
|---|---|---|---|---|---|
| **C30** | The contract record is the mapping. Any transport rendering (an Issue body, a comment, a queue message) MUST embed the record verbatim and MUST be able to reproduce it. **Round-trip test: extract the record from the rendering, canonicalise per C6, compare to the original canonical form. They MUST be byte-identical.** | **D** | §8: *"GitHub Issues can remain an early adapter and human-visible surface. They must not become the semantic protocol."* This clause is what makes that sentence mechanical instead of aspirational. | **E1** | Extract, canonicalise, `diff`. **This is the specification's cheapest and most valuable unrun test**, and it is a strictly weaker version of the DSSE-PAE falsifier triage Q4 asked for — same experiment, hash instead of signature, so it can be run today. |
| **C31** | A record MUST NOT depend on any transport-supplied field for its meaning — not Issue labels, not assignees, not state, not comment ordering, not timestamps. | **D** | #40 had **zero labels and zero assignees**, and its only ordering signal was comment order. Everything semantic was in the prose body. Also HD H9: Issue bodies are silently mutable by anyone with triage access, so transport metadata has no integrity. | **E1** | A consumer written against the record alone. **The real check is that a second implementation, reading only the record, reaches the same conclusions.** None exists. |
| **C32** | The transport is free to render the record however it likes for humans, and the human rendering has no normative force. Where rendering and record disagree, **the record governs**. | **X** | Rests on: #40's response asserted precisely this shape about a different pair of artifacts — *"if any field here contradicts a claim in our `decisions.md`/`observations.md`, treat this live output as authoritative over the committed docs."* The executor invented a precedence rule because none existed. This clause is that rule, generalised. | **E1** | Only checkable when the two are compared. Nothing compares them. |

### 5.6 Where records live

| # | Clause | Prov | Source / change | Enf | Enforcement point |
|---|---|---|---|---|---|
| **C33** | Contract records are files, committed under `product/contracts/<contract_id>/<seq>-<record_type>.json`, one record per file, never edited after commit. | **X** | Rests on: git's immutable objects are the only append-only surface the estate actually has (triage A-3), and the artifact plane's chokepoint is owner-merged `main` (H28). One record per file makes an edit a visible diff rather than an in-place mutation. | **E1** | Path and immutability are checkable by a CI job over the diff. **None exists, and see C34.** |
| **C34** | **Nothing in this specification is enforced at a chokepoint the bound party cannot reach.** Any implementation MUST state this until it is false. | **X** | Rests on: HA fracture #8 — *"a type is not a boundary … the likeliest outcome of this whole line is a schema nothing enforces."* Triage A-3's own falsifier is unrun (*"can the executing agent reach the remote's protection settings through any credential it holds?"*), P-1 is unrun, and **this very session runs under bypass-permissions.** | **E0, necessarily** | This is the clause that admits the specification's ceiling. See §6.3. |

---

### 5.7 Provenance tally

34 clauses. **Derived 15** (C1, C2, C8, C9, C10, C14, C18, C19, C20, C21, C23, C26, C27, C30, C31) ·
**Adapted 7** (C6, C7, C15, C16, C17, C22, C28) · **Authored 12** (C3, C4, C5, C11, C12, C13, C24, C25,
C29, C32, C33, C34).

The authored twelve cluster in two places, and the clustering is not accidental: the chain mechanics
(C3–C5) and the lifecycle-and-placement clauses (C24, C25, C29, C32–C34). The corpus had nothing to say
about either, because the one real exchange had no chain and never terminated. **Aim scepticism there
first.**

---

## 6. Enforcement — the honest accounting

### 6.1 The tiers

- **E0 — nothing checks this today.** The clause is documentation. It may still be worth having (C20,
  C27), but it purchases no assurance.
- **E1 — a pure function of the record could check it, and no such checker exists.** The check is
  specified and buildable; it has not been built. E1 is a promise, not a control.
- **E2 — an existing chokepoint checks it.** The estate has exactly two: the single-writer curator on
  the graph plane, and owner-merged git `main` on the artifact plane.
- **E3 — a chokepoint the bound party cannot reach checks it.** The only tier that is enforcement in
  the sense §5.1 and §5.2 mean.

### 6.2 The count

| Tier | Clauses | n |
|---|---|---|
| **E0** | C14, C20, C21, C22, C26, C27, C34, plus the "is it true" half of C15 and the completeness half of C16 | **9** |
| **E1** | C1–C8, C10–C13, C17, C19, C23, C24, C25, C28–C33, plus the enum/append-only halves of C15 and C16 | **23 whole + 2 halves** |
| **E2 (nominal)** | C9, C18 | **2** |
| **E3** | — | **0** |

### 6.3 The ceiling, stated plainly

**This specification has zero E3 clauses. As of today there is no enforcement point for any clause in
it that the party it binds cannot reach.**

Worse, the two E2 clauses are E2 in name only. C9 and C18 are enforced at the curator's write path —
but the curator is an LLM agent following a rule written in a markdown file, and **§5.1 is a settled
owner constraint that an LLM cannot police itself or another LLM as the final authority.** By the
owner's own rule, my two strongest clauses are E0.

The artifact-plane chokepoint does not save them either. D15 puts research documents straight onto
`main` with no branch, no PR and therefore no required check. Triage A-3 found the failure mode is
*configuration, not technology* — the ruvnet precedent ran with `"protected": false` and zero rulesets
on all three repos while advertising the invariant *"the machine never merges."* Whether this repo is
in that state is **unverified**, and A-3's falsifier — *can the executing agent reach the remote's
protection settings through any credential it holds?* — is unrun.

**What would create the first E3 clause**, in order:

1. A `contract-lint` executable implementing the E1 checks (C1–C7, C10, C12, C13, C17, C19, C23–C25,
   C28–C31). Perhaps 300 lines. This is a POC's job, under its own gate — not mine.
2. That linter wired as a **required status check** on `main`, so CI evaluates the commit rather than
   the agent's report of it (triage S-4).
3. **P-1 answered:** can an agent widen its own boundary by editing configuration mid-session — the
   workflow file, `.claude/settings.json`, the repo ruleset? If yes, step 2 produces an E1 check
   wearing an E3 costume, which triage names as *worse than documentation* because it purchases
   misplaced trust.
4. **D6 resolved**, at which point C8 can move off `self-asserted` and C9's ceiling can lift.

Steps 1–2 are cheap. **Step 3 is the one that decides whether any of this is architecture or
documentation, it costs one Edit in a throwaway repo, and it has not been done.**

---

## 7. A conforming example

This is Issue #40, re-expressed. It is real, and every value below is taken from the actual exchange
rather than invented — including the `substitutions` entry, which really happened.

**`product/contracts/xp-2026-0716-uni-ground/0-request.json`**

```json
{
  "schema": "work-contract/v0",
  "contract_id": "xp-2026-0716-uni-ground",
  "record_type": "request",
  "seq": 0,
  "prev": null,
  "issued_at": "2026-07-16T19:24:34Z",
  "issuer": {
    "program": "dug-21/jurati",
    "principal": "jurati-ass002-researcher",
    "identity_basis": "self-asserted"
  },
  "body": {
    "objective": "Obtain raw, verbatim Unimatrix output from the live arch-research instance to ground five load-bearing claims in Jurati ASS-002 / Q3.",
    "grounds": "Q3 is currently sourced entirely from arch-research's committed decisions.md and observations.md. Unimatrix is project-scoped, so our context_* calls resolved against Jurati's empty instance. We have never seen real output.",
    "deliverables": [
      { "id": "d1", "statement": "The hydrated board query for one real goal: context_graph(mode:'subgraph', seed_ids:[<goal>], max_depth:1, edge_types:['Advances'], direction:'incoming', detail:'full').",
        "done_when": "Full returned subgraph pasted verbatim: nodes with content, the grade:<...> tag on each, and edges.",
        "checked_by": "judgement:jurati-ass002-researcher", "priority": "required" },
      { "id": "d2", "statement": "context_cycle_review for a recent wf-stamped run, entire object.",
        "done_when": "Object pasted verbatim, and it literally shows whether total_tool_calls, knowledge_curated and feature_knowledge_reuse.total_served are populated or 0/null, and whether the wf tag round-trips.",
        "checked_by": "mechanical:those four keys appear in the pasted object with their returned values",
        "priority": "required" },
      { "id": "d3", "statement": "The lookup used to compute findings-per-run by run-id tag, plus its raw result for one run-id.",
        "done_when": "Query and raw result pasted, confirming or refuting that yield is reconstructable only via a curator-maintained tag rather than engine-native.",
        "checked_by": "judgement:jurati-ass002-researcher", "priority": "required" },
      { "id": "d4", "statement": "One real proven node fetched by id via context_get, full record including metadata.",
        "done_when": "Record shows (a) created_by, (b) whether grade rides a grade:proven tag distinct from the DB status field, (c) whether cites:/proven_by: are fields rather than nodes or edges.",
        "checked_by": "mechanical:created_by, tags and status are all present in the pasted record",
        "priority": "required" },
      { "id": "d5", "statement": "Resolve-forward vs pinned read for one versioned node: context_graph(mode:'current') alongside context_get of the pinned id.",
        "done_when": "Both outputs pasted, showing whether current resolves forward while get holds the pin.",
        "checked_by": "judgement:jurati-ass002-researcher", "priority": "droppable" }
    ],
    "effects_permitted": "read-only",
    "authority": {
      "granted": [],
      "self_limit": [
        "read-only queries only",
        "redact secrets and PII only; keep field names, nulls and zeros exactly as returned",
        "if a query no longer matches the schema, run the nearest equivalent and record the substitution"
      ]
    },
    "disclosure": {
      "complete": true,
      "items": [
        { "ref": "jurati ASS-002 Q3 claim text, quoted inline in this request", "classification": "internal", "onward": "cite-only" }
      ]
    },
    "acceptance": { "evidence_floor": "claimed", "acceptor": "owner" },
    "out_of_scope": ["any write to the arch-research graph", "any query requiring credentials Jurati does not already hold"],
    "return_to": { "channel": "github-issue-comment", "address": "dug-21/arch-research#40" },
    "expires": { "by": "2026-07-30T00:00:00Z" }
  }
}
```

**`1-return.json`** (abridged — `results` d1–d5, `provenance`, `substitutions`, `disclosures_made`):

```json
{
  "schema": "work-contract/v0",
  "contract_id": "xp-2026-0716-uni-ground",
  "record_type": "return",
  "seq": 1,
  "prev": "sha256:<hash of record 0 canonical form>",
  "issued_at": "2026-07-16T22:10:00Z",
  "issuer": { "program": "dug-21/arch-research", "principal": "jurati-req-researcher", "identity_basis": "self-asserted" },
  "body": {
    "fulfils": "xp-2026-0716-uni-ground",
    "results": [
      { "id": "d1", "outcome": "delivered", "evidence": [ { "kind": "verbatim tool output", "ref": "#40 comment 1, section 1; targeted goal_id 113" } ] },
      { "id": "d2", "outcome": "delivered", "evidence": [ { "kind": "verbatim tool output", "ref": "#40 comment 1, section 2; feature_cycle opcost-001" } ] },
      { "id": "d3", "outcome": "delivered", "evidence": [ { "kind": "verbatim tool output", "ref": "#40 comment 1, section 3" } ] },
      { "id": "d4", "outcome": "delivered", "evidence": [ { "kind": "verbatim tool output", "ref": "#40 comment 1, section 4" } ] },
      { "id": "d5", "outcome": "delivered", "evidence": [ { "kind": "verbatim tool output", "ref": "#40 comment 1, section 5" } ] }
    ],
    "provenance": {
      "executor": "a factory agent on the live arch-research Unimatrix",
      "identity_basis": "self-asserted",
      "method": [
        "context_graph(mode:'subgraph', seed_ids:[113], max_depth:1, edge_types:['Advances'], direction:'incoming', detail:'full')",
        "context_cycle_review(feature_cycle:'opcost-001', format:'json')"
      ],
      "attestation": "Every call was read-only. agent_id was passed on all calls. Nothing was written to the graph. No secrets or PII were present to redact."
    },
    "substitutions": [
      { "deliverable_id": "d1", "requested": "seed_ids:[\"<goal id>\"] (string)", "performed": "seed_ids:[113] (integer)", "reason": "arch-research node ids are integers, not strings; ran the nearest equivalent per the request's self_limit." }
    ],
    "disclosures_made": [
      { "ref": "#40 comment 1, full body", "classification": "internal", "onward": "cite-only" }
    ]
  }
}
```

**`2-disposition.json`** — **this record does not exist in reality.** Its absence is the failure the
specification is built to detect. Under C24 the real exchange is `expired` as of 2026-07-30. What
should have been written:

```json
{
  "schema": "work-contract/v0", "contract_id": "xp-2026-0716-uni-ground",
  "record_type": "disposition", "seq": 2, "prev": "sha256:<hash of record 1>",
  "issued_at": "2026-07-17T09:00:00Z",
  "issuer": { "program": "dug-21/jurati", "principal": "owner", "identity_basis": "self-asserted" },
  "body": {
    "fulfils": "xp-2026-0716-uni-ground",
    "outcome": "accepted-with-deviations",
    "acceptor": "owner",
    "basis": [
      { "id": "d1", "cleared": true, "note": "Subgraph returned with grades and edges. One declared substitution (integer ids), accepted." },
      { "id": "d2", "cleared": true, "note": "All four flagged keys answered as literally returned. OBS-6 confirmed; two accounting paths disagree — recorded." },
      { "id": "d3", "cleared": true, "note": "Confirmed: run grouping is not engine-native; feature_cycle is empty on every node." },
      { "id": "d4", "cleared": true, "note": "created_by returns the curator string here, not anonymous — D6's caveat needs re-checking, filed separately." },
      { "id": "d5", "cleared": true, "note": "Droppable item delivered anyway." }
    ],
    "owner_acted": "approved"
  }
}
```

---

## 8. A non-conforming example

Constructed to fail on **exactly four clauses**, each detectable by a stated rule, so that a validator
can confirm the examples discriminate rather than merely differ.

```json
{
  "schema": "work-contract/v0",
  "contract_id": "arch-research#57",
  "record_type": "request",
  "seq": 0,
  "prev": null,
  "issued_at": "2026-08-21T10:00:00Z",
  "issuer": { "program": "dug-21/arch-research", "principal": "wfh-007-leader", "identity_basis": "attested" },
  "body": {
    "objective": "Summarise the uni software-delivery protocols.",
    "grounds": "wfh-007 routed recommendations against a corpus it could not read.",
    "deliverables": [
      { "id": "d1", "statement": "A described summary of the uni protocols.",
        "done_when": "The summary is comprehensive and useful.",
        "priority": "required" }
    ],
    "effects_permitted": "read-only",
    "authority": { "granted": ["read:dug-21/unimatrix/**"], "self_limit": [] },
    "disclosure": { "complete": true, "items": [] },
    "acceptance": { "evidence_floor": "proven", "acceptor": "principal:wfh-007-leader" },
    "out_of_scope": ["anything else"],
    "return_to": { "channel": "github-issue-comment", "address": "dug-21/arch-research#57" }
  }
}
```

| Violates | Rule that detects it | Detection |
|---|---|---|
| **C2** | `contract_id` matches a transport-shaped pattern (`<owner>/<repo>#<n>`). | The exchange has no identity of its own; move the Issue to a queue and the contract loses its name. |
| **C8** | `issuer.identity_basis != "self-asserted"`. | `attested` is reserved in v0. The record claims an identity property the platform cannot supply (D6). |
| **C12** | `deliverables[0].checked_by` is absent. | A `done_when` of *"comprehensive and useful"* names no checker, which is the exact failure C12 exists to prevent. |
| **C13** | `authority.granted != []`. | The issuer purports to grant read access to a repository it does not control and cannot mint a credential for. **This is the dangerous one** — it reads as a grant and is a wish. |
| **C10 / C17** | `expires` is absent. | Without it C24 cannot fire, and the record reproduces Issue #40's measured failure exactly. |

Two further points a validator should note, because they are *not* violations and the examples must
discriminate on real rules rather than on vibes:

- `acceptance.evidence_floor: "proven"` is **syntactically valid** and **unsatisfiable** under C9
  while `identity_basis` is `self-asserted`. v0 does **not** reject it at issuance; it fails at
  acceptance. Whether that should be an issuance-time check is **open question Q4**.
- `acceptor: principal:wfh-007-leader` is syntactically valid but puts an LLM at the end of the
  acceptance chain, which C26 makes non-default but does not forbid. Whether it should be forbidden
  is **open question Q1**.

---

## 9. Deliberately left out

| Left out | Why |
|---|---|
| **Signatures / DSSE envelope** | Falsifier unrun (§3.1). Replaced by canonicalisation + content hash, at the cost of non-repudiation. |
| **A partition claim** | HA fracture #7: the partition lives in the layout, not the contract. An optional field nobody can check is fat (§3.2). Triage §6 Q6 asked for it; I declined. → Q6. |
| **A rich authority grammar** | Nothing mints authority here (§3.3). C13 defines the field and forbids its use. |
| **Budget / cost bounds** | 2/12 in the intra-corpus, absent from the one real exchange, no observed failure. C11 cuts it. Re-enter when an exchange fails on cost. |
| **Retry and cancellation semantics** | §8 asks for them; nothing in the corpus exercises them. A cancellation with no revocation mechanism is a request to please stop (HA fracture #6: contracts never get free stopping). Omitted rather than faked. |
| **Model / provider / runtime provenance on the request** | §8 field 10. No observed use, and the *return* side already carries what the responder actually volunteered (C20). Re-enter when a decision turns on which model produced something. |
| **A deviation taxonomy** | H27's ≥80%-coverage test is unrun (C28). Authoring a taxonomy on an unrun test is a taxonomy-authoring project. |
| **A consequence-class taxonomy beyond three values** | The four-way idempotent/reversible/compensable/irreversible taxonomy does not survive the crossing (HD H8) and re-deriving it per action space is a design project of its own. |
| **Rate/velocity bounds on issuance** | HA H26 is a genuine whitespace hypothesis and I believe it is right. It is also untested, and its own risk note says legitimate bursty work must fit under the bound. Not v0. |
| **Aggregation controls** | Forty years unsolved; V4 narrows one subclass to configuration and leaves the hard core untouched. **Carried as an explicitly accepted residual risk**, per the ledger's fracture #3. |
| **Multi-hop delegation** | Every observed exchange is one hop. Depth limits without a token chain are unenforceable anyway. |
| **Any implementation** | Not my role. The linter in §6.3 step 1 is a POC's job under its own gate. |

---

## 10. The strongest objection I can find against this draft

There are two. I can answer the second. I cannot answer the first.

### 10.1 The one I cannot answer

**By the corpus's own null hypothesis, this document is instance #7.**

HA fracture #8 predicts the outcome of this whole line: *"the likeliest outcome is a schema nothing
enforces."* Six independent built-believed-inert instances stand behind that prediction. §6.2 shows
this draft has **zero E3 clauses**, and the two clauses I called E2 are enforced by an LLM curator
reading a markdown rule — which §5.1, a settled owner constraint, says is not enforcement at all.

So a fair reading is: I have produced a well-argued schema that nothing checks, whose most load-bearing
clause (C9) is nominally enforced by exactly the kind of party the owner has already ruled cannot be a
final authority.

My defence is that the record still makes failures **detectable after the fact**, and that C24 in
particular converts an ambient smell into a computable state. **That defence is unfalsifiable in the
direction that matters, and it is precisely the defence every one of the six inert instances would
have offered.** HA's own words are that placement at an unbypassable chokepoint "is not an
implementation detail; it is the difference between architecture and documentation." Today this is
documentation. I have labelled it as such in C34 and §6.3 rather than obscuring it, but labelling is
not curing.

The honest disposition: **this draft should not be ratified until P-1 is answered.** If an agent can
widen its own boundary by editing configuration, then step 2 of §6.3 produces an E1 check wearing an
E3 costume, and the correct verdict on this whole line is *park it* — not *implement the linter*. P-1
costs one Edit in a throwaway repo. It should be run before anyone builds against this.

### 10.2 The one I can answer, partially

**A twenty-clause schema derived from n=1 is over-fitting.**

Issue #40's *measured* failure was not a missing field. It was that nobody closed the issue. Of my
required fields, exactly two (C23 disposition, C17/C24 expiry) address the observed failure. The rest
address hypothetical failures, and the frequency evidence I leaned on — twelve `SCOPE.md` files — is
**intra-program**, authored by the same estate under one owner, so a field at 12/12 inside one trust
domain may be irrelevant at a boundary and a field at 2/12 may be mandatory across one. The brief
flagged this caveat and told me to test it rather than trust it. **I could not test it. There is one
exchange.**

My partial answer is C11: I wrote the requiredness rule down as a normative clause so the over-fitting
is visible and reversible, and it did real work — it cut budget, roles, request-side model provenance
and the partition claim out of v0. And H14's cheapest test is the direct falsifier and it is cheap:
run one exchange with this record and **record which fields either side actually consulted.
Unconsulted = schema fat; consulted-but-absent = schema holes.** I expect v0 to lose fields on that
test, and losing fields would be the test working.

What I cannot answer is the sharper form: with n=1, **the same evidence supports a three-field record**
(objective, done_when, disposition) as well as it supports this one. I chose twenty because the
missing-field delta list was the thing the triage identified as the adapter spec. That is a reading of
the evidence, not a measurement of it.

---

## 11. Open questions — the owner's to answer

Stated as questions, not buried as caveats. Q1–Q3 are the owner's §8 open delegation questions that
this draft could not answer without a decision; Q4–Q8 are ones the drafting surfaced.

**Q1. Who accepts returned work — deterministic contract checks, an independent verifier, the
requesting agent, or you?** C25/C26 make it a per-contract field defaulting to `owner`, which keeps the
record usable while you decide. But an `owner` default on every exchange makes you the acceptance hot
path — the exact labour §8 is trying to reduce. **Is there a class of exchange where a deterministic
check alone may accept?** If yes, naming that class is the single largest attention saving available.

**Q2. Is a program a stable principal, or is every team assembled per objective?** C8 records
`issuer.program`, which presumes the former. If teams are per-objective, `program` is the wrong grain
and the twenty-run trust counter of §5.7 has no stable denominator to accumulate in (HA H24).

**Q3. Does a called program inherit, receive an attenuated grant, or receive only explicitly packaged
material?** C13 forces the third answer by default, because it is the only one implementable without a
minting authority. **Is that acceptable as the standing answer, or is it a temporary consequence of
D6?**

**Q4. Should an unsatisfiable `evidence_floor` be rejected at issuance or at acceptance?** §8's example
is `evidence_floor: proven` under C9, which is unsatisfiable today. Rejecting at issuance is friendlier
and encodes today's ceiling into the schema; rejecting at acceptance keeps the schema honest about a
ceiling that should lift when D6 lands. I chose acceptance. **You may prefer the friendlier failure.**

**Q5. Is non-repudiation required for v0?** §3.1 dropped signatures for a content hash on an unrun
falsifier. If cross-program exchange will ever carry a decision you would need to *prove* someone made,
the hash is insufficient and the DSSE-PAE round-trip test must be run before this record is used in
anger.

**Q6. Does the partition belong in the contract or in the layout?** I cut it on HA fracture #7's
authority, against triage §6 Q6's request. **You are the tiebreaker.**

**Q7. May the classification decision be delegated to a curator, or must it come to you?** HD H10's
falsifier — hand a curator ten mixed entries and score misclassification — is unrun, and its result
decides whether C22 is workable or whether every crossing becomes an owner gate. Given §6 lists
"exposing private or sensitive information" as a priority failure class, **you may want to run that
test before delegating anything.**

**Q8. Should the first use of this record be P-3 (the `uni` corpus request)?** It is real work that is
blocked today, it exercises every field, and its three outcomes are all informative — including
*"just clone the repo,"* which would mean the ownership boundary is conventional rather than
platform-enforced and would change what this record is for.

---

## 12. What I needed and did not have

Named as gaps, per my role's instruction that a named gap may be worth more than the clause it was
going to support.

1. **A corpus of more than one.** H29 asked for *N* real exchanges before authoring. There is one.
   Every frequency claim in this draft rests on twelve intra-program documents plus a single
   cross-program instance. **What would close it:** run P-3, then two or three more real exchanges,
   recording consulted-vs-unconsulted fields per H14. Three exchanges would probably halve the schema.
2. **The `uni` corpus is not on this disk.** I could not see the sibling program's protocol documents,
   so this record's fit to the *other* side of the boundary is entirely unverified. I designed the
   requester's view of an exchange whose executor I cannot read. **What would close it:** P-3, or read
   access to `.claude/protocols/uni`.
3. **P-1, unrun.** Whether an agent can widen its own boundary decides whether any clause here can ever
   reach E3. Without it §6.3 is a plan, not a path. **This is the blocking gap and it costs one Edit.**
4. **P-2, unrun.** The checkable-`done_when` denominator. C12 forces the choice into the open with
   `checked_by`, but I do not know whether the mechanical branch will be used 5% of the time or 80%,
   and that number decides whether the acceptance stack is an attention reducer or an attention
   re-router.
5. **The DSSE-PAE round trip, unrun.** Cost me the signature envelope (§3.1). C30 is the weaker version
   that can be run today and should be.
6. **HD H10's classification error-rate test, unrun.** Cost me any confidence in C22.
7. **Whether `created_by` actually returns `anonymous`.** D6 says it does; Issue #40's own returned
   records show `"created_by":"opcost-001-curator"` and `"created_by":"opcost-002-curator"`. **These
   contradict.** C8 and C9 are both built on D6, so if D6's caveat is stale or narrower than stated,
   the single most restrictive clause in this document may be over-restrictive. I did not resolve it
   because resolving it is re-research. **This is a live contradiction in the corpus and someone should
   settle it before C9 is implemented.**
