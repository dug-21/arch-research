# Checkability review — cross-program work contract v0 draft

> **This is NOT a firewall gate and NOT a proof ruling.**
>
> There is no capability node in play, no `done_when` sentence, and no artifact claiming `proven`.
> Nothing in this chain writes Unimatrix and nothing advances a grade. The subject document is
> `claimed` by construction and stays `claimed` regardless of what is written below.
>
> **The single question answered here is: is the specification checkable as written?** Whether the
> design is *correct*, whether the estate should *adopt* it, and whether the architecture is *good*
> are the goal-owner's and the owner's calls, and were explicitly out of scope for this review. A
> later reader must not read the verdict below as a ruling on the specification's merit.
>
> **No grade is recommended.** My role definition's grade-recommendation step (`missing` / `claimed` /
> `partial` / `proven`) **does not apply here** — there is no node to grade and no capability in play.
> I am not inventing something to grade in its place.

**Subject:** `product/research/wfh-007/specs/work-contract-v0-draft.md` (773 lines, 34 clauses)
**Author:** `factory-architect` (`wfh-007-architect`)
**Reviewer:** `factory-validator` (`wfh-007-arch-validator`)
**Date:** 2026-08-21

**Gate-input independence:** satisfied. I did not author this document, did not advise on it, have
never seen the author's reasoning, and have repaired nothing. Every defect below is named, not fixed.

---

## Verdict — on checkability only

# REWORKABLE FAIL

The document is **substantially checkable** — it is far more honest about its own enforcement ceiling
than the corpus's null hypothesis predicted, and roughly twenty of its thirty-four clauses carry a
real, mechanical, buildable predicate. It fails this gate on a narrower ground: **the apparatus the
document supplies for a reviewer to check it with is itself broken in four mechanically demonstrable
places.**

1. The **example pair discriminates, but three of its discriminating rules do not fire as written** —
   including the C2 rule, which does not match the value it is aimed at.
2. The conforming example **fails a clause it claims to satisfy** (C18), and its `prev` format
   contradicts the schema in §4.1.
3. **C10 requires a field that C11 — the document's own normative requiredness rule — forbids**, and
   C10's stated justification for that field is false on the corpus.
4. **Three clauses are tiered E1 on an enforcement point that is vacuous** (C11, C31, C32), which is
   precisely the "present, believed, inert" failure the document was written to expose, occurring
   inside the document's own accounting table.

All four are text or re-derivation fixes. None requires re-research, a new experiment, or a change of
design. This is why the verdict is REWORKABLE rather than SCOPE FAIL. **Iteration 1 of a maximum 2.**

---

## Method

Every clause C1–C34 was read against its own enforcement cell. Both examples were then executed
against the full clause set by hand, clause by clause, rather than against the clauses the document
nominates. Provenance marks were spot-checked against the named source for eight of the fifteen
`derived` clauses and three of the seven `adapted` ones. The D6 contradiction was checked against both
primary sources **and against the live graph**. Zero graph writes were made; three read-only
`context_*` calls were issued.

---

## 1. The example pair — does it discriminate?

**Yes, directionally. No, cleanly.** The non-conforming example does fail and the conforming example
does mostly pass, so the pair is not the degenerate both-pass / both-fail case. But three of the five
discriminating rules the document states are defective, and a reviewer using the document as written
would reach the wrong result on each.

### 1.1 C2's detection rule does not match the value it is aimed at — DEFECT

§8's table says the non-conforming record violates C2, detected by: *"`contract_id` matches a
transport-shaped pattern (`<owner>/<repo>#<n>`)."*

The example's value is `"arch-research#57"`. That is `<repo>#<n>`. It has **no owner segment**. A
linter implementing the stated rule literally — the only thing a stranger implementing this
specification could do — **passes** the non-conforming example on C2.

This is the exact failure the brief names: an example that fails on the wrong rule. The clause C2
itself is fine; the detection rule offered as its mechanization is wrong.

**Remedy:** state the rule as a property, not a pattern — *"`contract_id` is non-conforming if it
contains `#` followed by digits, or resolves as a URL, or is a bare integer"* — and re-test it against
the example's actual value. Or change the example's value to `dug-21/arch-research#57` so the stated
rule fires. Do one or the other; today neither holds.

### 1.2 The conforming example fails C18 — DEFECT

C18: *"`acceptance.evidence_floor` **and** the values in `results[].evidence[].kind` MUST use the
estate's existing vocabulary (`missing|claimed|partial|proven`; …)."*

All five entries in §7's conforming return carry `"kind": "verbatim tool output"`. That value is not in
`missing|claimed|partial|proven`.

Both available readings are defects:

- **Strict reading** (`kind` must draw from the four grades): the conforming example violates C18. An
  example that fails a clause it claims to satisfy destroys the pair's value as a discriminator.
- **Loose reading** (`kind` draws on "the estate's existing vocabulary" in some broader sense): **no
  enumerated vocabulary for `kind` exists anywhere in the document**, so the `kind` half of C18 has no
  closed set to check against and is **unfalsifiable** — you cannot construct a `kind` value that
  violates it.

The document supplies the reader no way to choose between the two readings. Under either, C18 is not
checkable as written.

**Remedy:** split C18. Bind `acceptance.evidence_floor` to the four grades (mechanical, E1). Either
enumerate a closed `kind` vocabulary or delete the `kind` half of the clause and let §4.3's free-text
definition stand — an unenumerated vocabulary constraint is prose wearing a MUST.

### 1.3 The `prev` format in §7 contradicts §4.1 — DEFECT

§4.1 defines `prev: <hex hash of the canonical form of record seq-1, or null when seq == 0>`. C6 says
*"All hashes are SHA-256 over the canonical form."*

§7's records 1 and 2 carry `"prev": "sha256:<hash of record 0 canonical form>"` — a `sha256:`-prefixed
string, not a hex hash. A linter written against §4.1 rejects the conforming example on C7. This is
small, and it is exactly the class of defect that makes a specification unreviewable: the normative
text and the reference example disagree about the wire format of a load-bearing field.

**Remedy:** pick one. If the prefix is intended, normalize §4.1 and C6/C7 to `sha256:<hex>`; if not,
strip it from §7. Separately, the placeholder `<hash of record 0 canonical form>` should be an actual
computed hex digest — a reference example whose chain field cannot be verified cannot demonstrate C7.

### 1.4 The count contradicts the table — DEFECT

§8 opens: *"Constructed to fail on **exactly four clauses**, each detectable by a stated rule."* The
table immediately below has **five rows** naming **six clauses** (C2, C8, C12, C13, C10, C17).

A reviewer told "exactly four" cannot reconcile that with the table, and cannot tell whether a fifth
detection is a bonus, an error, or a clause the author double-counted. In a document whose entire
purpose is to let a second stranger check the first stranger's work, the discriminator's own arity must
be exact.

**Remedy:** state the count from the table, note that C10 and C17 are one violation detected twice (the
missing `expires` fires both the presence check and the requiredness clause), and say so.

### 1.5 What actually fires — the mechanical result

I executed the non-conforming record against all 34 clauses. Firing cleanly, under the rules as
written:

| Clause | Fires? | Note |
|---|---|---|
| **C8** | **YES** | `identity_basis: "attested"` — reserved in v0. Clean enum check. |
| **C12** | **YES** | `deliverables[0]` has no `checked_by`. Clean presence check. |
| **C13** | **YES** | `authority.granted` non-empty. Clean emptiness check. |
| **C10 / C17** | **YES** | `expires` absent. One violation, two clauses. |
| **C2** | **NO** | The stated rule does not match the value — §1.1 above. |

So **four independent mechanical firings, not five**, and one broken rule. The conforming example
passes every clause except C18 (§1.2) and the §4.1/C7 format mismatch (§1.3).

**The pair does discriminate.** It is not the fatal case. But a stranger implementing the document's
own detection rules gets 4/5, and a stranger checking the conforming example against the full clause
set finds it non-conforming. Both halves of the apparatus need repair before the pair can be used to
review anything.

### 1.6 A composition defect visible in the author's own example, unnoticed — DEFECT

The non-conforming record carries `evidence_floor: "proven"` **and** `identity_basis: "attested"`.
§8's closing notes say the `proven` floor is *"syntactically valid and unsatisfiable under C9 … it
fails at acceptance."*

That is wrong, and the reason matters. **C9's precondition is `identity_basis: self-asserted`.** This
record does not carry `self-asserted` — it carries `attested`. C9 therefore never binds. The record
evades the estate's single most restrictive clause **by committing the C8 violation**, and C8's only
enforcement point is a linter that does not exist.

C9 is guarded by a field the bound party writes itself. Any party willing to violate C8 is
automatically outside C9. The two clauses the document calls its strongest compose into a control that
a one-word edit defeats, and the document's own non-conforming example demonstrates it without the
author noticing.

**Remedy:** state the composition explicitly in C9 — *"C9's guard is defeated by a false
`identity_basis`; C9 is therefore no stronger than C8's enforcement, which is E1-unbuilt."* Better:
invert C9 to bind on the absence of positive attestation rather than the presence of self-assertion —
*"a return MUST NOT be accepted above `claimed` unless every record in the chain carries an
`identity_basis` the acceptor can independently verify."* That phrasing fails closed. The current
phrasing fails open, which is the wrong direction for the file's most restrictive clause.

---

## 2. Self-inconsistency: C10 requires a field C11 forbids — DEFECT

This is the sharpest internal contradiction in the document, and it is mechanically demonstrable
against the corpus.

**C11 (normative):** *"a field is REQUIRED only if it was present in the one real exchange, **or** it is
in the 12/12 intra-corpus core, **or** its absence caused a measured failure."*

**C10** requires ten fields, including `disclosure`. Test `disclosure` against C11's three limbs:

| C11 limb | `disclosure` | Source |
|---|---|---|
| present in the one real exchange | **NO** | Corpus brief §2 delta list: *"no information classification or onward-disclosure rules (only a proto-handling rule: 'redact secrets/PII only')"* |
| in the 12/12 intra-corpus core | **NO** | The 12/12 core is status, goal target, confidence-required, question, why, proof bar, out-of-scope, coverage. Disclosure is not among them and appears in no row of the frequency table. |
| its absence caused a measured failure | **NO** | The one measured failure is that #40 never terminated. Nothing about disclosure was implicated. |

`disclosure` fails all three limbs. **C10 requires it anyway**, and C10's own Source cell asserts the
opposite: *"Two (`expires`, `disclosure`) are required on the **measured-failure** rule in C11."* No
measured failure involved disclosure. `expires` survives limb three on a defensible reading (with an
expiry, C24 fires and the exchange terminates); `disclosure` does not survive any limb.

This matters beyond the one field. C11 is the document's stated defence against its own strongest
self-criticism (§10.2, over-fitting on n=1). If C11 is violated by C10 — the very next clause, in the
same table — then C11 is not doing the work the document claims for it, and a reviewer cannot use C11
to check any future extension because the author's own application of it is unsound.

**Remedy, three options, one must be chosen:** (a) demote `disclosure` to OPTIONAL, which is what C11
as written compels; (b) add a fourth limb to C11 — *"or the field is required by a settled owner
constraint"* — and cite §6's "exposing private or sensitive information" priority failure class,
which would carry `disclosure` honestly; (c) keep `disclosure` REQUIRED and record it explicitly as a
**declared exception to C11**, with the reason. Option (b) is the strongest. Option (c) is the minimum.
What is not available is the present state, where the document silently violates its own rule and
misstates the reason.

---

## 3. Enforcement points — the census

**15 of 34 clauses carry a defective enforcement-point statement.** They fall into four kinds, and the
kinds are not equally serious.

### 3.1 Vacuous enforcement point, tiered above it — 3 clauses. THE SERIOUS ONES.

These are the misrepresentations. Each names an enforcement point that is a human or a judgment call
with no stated procedure, and each is tiered **E1** — a tier the document defines as *"a pure function
of the record."* None of the three is a pure function of anything.

| Clause | Named enforcement point | Why it is vacuous |
|---|---|---|
| **C11** | *"A reviewer with the frequency table."* | This is the textbook vacuous form. Worse, the clause's third limb — *"its absence caused a measured failure"* — names no measurement procedure, so even a diligent reviewer has no decision rule. **The author admits it in the same cell** (*"its real enforcement is that it is written down and citable"*) — which is the definition of E0 — and then tiers it E1 anyway. The cell contradicts the tier. |
| **C31** | *"A consumer written against the record alone. The real check is that a second implementation, reading only the record, reaches the same conclusions."* | A differential test requiring a second implementer and a human comparison of "conclusions" is not a pure function of the record. It is also not obviously runnable at all: nobody has specified what counts as the same conclusion. |
| **C32** | *"Only checkable when the two are compared. Nothing compares them."* | The cell states its own vacuity and the tier says E1 regardless. See §4 — C32 is additionally unfalsifiable. |

Honest tiering would move all three to E0, taking the E1 population from 23 to 20 and the E0
population from 7 whole clauses to 10. **This is the "controls present, believed, and inert" failure
mode occurring inside the very table built to expose it.**

**Remedy:** re-tier C11, C31, C32 to E0 and restate their enforcement cells as *"nothing checks this;
its value is that it is citable."* For C11 specifically, if an E1 tier is wanted, supply the missing
procedure: a table of the three limbs with the corpus evidence per limb, so applying C11 becomes a
lookup rather than a judgment.

### 3.2 No enforcement point, honestly declared — 7. NOT DEFECTS.

C14, C21, C26, C34 whole; C12, C15, C16 in one declared half. Each says plainly that nothing checks it.
C15 and C16 are split into a checkable half and an uncheckable half, which is the right discipline and
should be the model for §3.3 below. C21's cell — *"This is the executor marking its own homework, and
the specification should not pretend otherwise"* — is the best enforcement statement in the file.

### 3.3 Tiered E0 against a question the clause does not ask — 3 clauses. INCONSISTENT.

| Clause | What it says | What it is tiered against |
|---|---|---|
| **C20** | *"`provenance.method` and `provenance.attestation` are REQUIRED."* | *"Nothing checks that an attestation is true."* |
| **C22** | *"`disclosures_made` MUST classify everything crossing back."* | *"Nothing checks a classification."* |
| **C27** | *"`owner_acted` MUST distinguish `approved` from `did-not-object`."* | *"Nothing checks it."* |

In all three the clause asserts **presence or enum-membership**, which is an E1 pure function
identical in kind to C10's. The truth of the value is a different and unasserted claim. The author
split C15 and C16 into halves for exactly this reason and did not split these three.

The direction of this error is conservative — it understates the document's coverage — so it is not
dangerous. It is still a defect, because §6.3 step 1's linter list is the buildable set an implementer
would work from, and these three presence checks are trivially implementable and excluded from it for
no stated reason.

**Remedy:** split C20, C22, C27 the way C15 and C16 are split. Add their presence/enum halves to the
§6.3 step 1 linter list.

### 3.4 Routed to a weaker enforcement point than is available — 2 clauses. C9 AND C18.

Both are tiered **E2-nominal** at the curator's write path, and the author then argues in §6.3 that
E2-nominal is E0-actual because the curator is an LLM. That argument is correct (see §6 below).

What the author missed: **C9 has a record-level check that is a pure function of the record set.**
Given a `disposition` with `outcome: accepted` or `accepted-with-deviations`, plus the request's
`acceptance.evidence_floor`, plus every `issuer.identity_basis` in the chain, the predicate

> `floor > "claimed" AND any(identity_basis == "self-asserted") AND disposition.outcome ∈ {accepted, accepted-with-deviations}` → non-conforming

is three lines and evaluates entirely within the file set C33 defines. It belongs in the same linter as
C23 and C24. **C9 is absent from §6.3 step 1's linter list.** So is C8, on which C9's guard depends
(§1.6), and on which the non-conforming example's cleanest detection fires.

The document therefore routes its most load-bearing clause to the weakest enforcement point available
and omits the strongest, and then draws its central pessimistic conclusion (§10.1: *"my most
load-bearing clause is nominally enforced by exactly the kind of party the owner has already ruled
cannot be a final authority"*) from that routing. The pessimism is partly self-inflicted.

**Remedy:** add C8 and C9 to the §6.3 step 1 linter list and re-tier C9 as **E1 at the record layer,
E2-nominal at the graph layer** — two enforcement points, honestly described, the record-level one
strictly stronger than the curator. This does not create an E3 clause and does not change the
zero-E3 conclusion. It does mean the file's most restrictive clause becomes buildable in the same
300 lines the author already scoped.

---

## 4. Unfalsifiable clauses — named, by number

A clause where no document can be constructed that violates it is not a rule.

| Clause | Why no document can violate it |
|---|---|
| **C14** | *"the record MUST NOT be **read** as granting or withholding anything."* This constrains a **reading**, not a record. A reading is not a property of any artifact the specification governs. No record, however written, violates C14. |
| **C26** | *"v0 default: `acceptance.acceptor: owner`."* This is a default, not a MUST. §8's own closing note confirms it: *"C26 makes non-default but does not forbid."* A record with any acceptor conforms. |
| **C32** | *"Where rendering and record disagree, the record governs."* A precedence rule. It tells a consumer what to do in a conflict; it forbids nothing. Neither a record nor a rendering can violate it. |
| **C34** (first sentence) | *"Nothing in this specification is enforced at a chokepoint the bound party cannot reach."* A factual self-assessment, not a rule — and *"until it is false"* names no procedure for determining falsity, so the clause cannot detect its own expiry. (C34's **second** sentence — *"Any implementation MUST state this"* — is falsifiable by grep, and is the only enforceable part.) |
| **C18** (`kind` half) | Unfalsifiable under the loose reading — no enumerated `kind` vocabulary exists to check against. Under the strict reading it is falsifiable but the conforming example violates it. See §1.2. |

**Separately: falsifiable only by a judgment call no stated procedure resolves.** These are not prose,
but a reviewer cannot mechanically apply them, and only some are labelled as such:

**C11** (*"caused a measured failure"* — no measurement procedure) · **C31** (semantic dependence on
transport metadata is not decidable from the record) · **C12** non-vacuity half (labelled; P-2 unrun) ·
**C15** truth half (labelled) · **C16** completeness half (labelled) · **C20** truth half (labelled) ·
**C21** (requires an observer with logs the specification does not provide; labelled) · **C22**
correctness half (labelled).

The labelled six are honest. **C11 and C31 are not labelled and are tiered E1** — they are the same
defect as §3.1.

**Remedy for the five unfalsifiable clauses:** C14 → restate as a definition, not a MUST (*"`self_limit`
is defined as a declaration by the requester about its own ask; it confers no authority"*) and move it
out of the numbered clause set, or renumber it as a non-constraining note. C26 → either make it a MUST
with a stated exception path, or move it to §4.2 as a schema default and drop the clause number. C32 →
same, restate as a consumer rule in §4 rather than a clause. C34 → keep the second sentence as the
clause, demote the first to a §6.3 assertion. C18 → split as in §1.2.

**A numbered `C<n>` in a table headed "Clauses" reads as a rule. Four of these are not rules. That is a
checkability defect independent of their merit — every one of them may be worth saying.**

---

## 5. Tier self-consistency

Three inconsistencies beyond §3.

**5.1 §6.2 and §6.3 disagree about which clauses are mechanizable — DEFECT.**

- §6.2's E1 roster: C1–C8, C10–C13, C17, C19, C23, C24, C25, C28–C33.
- §6.3 step 1's linter scope: C1–C7, C10, C12, C13, C17, C19, C23–C25, C28–C31.

The delta is **C8, C11, C32, C33** — declared E1 in one section and excluded from the buildable set in
the next, with no reason given. C11 and C32 are correctly excluded but for reasons the document never
states (they are not E1 at all — §3.1). **C8's exclusion is a straightforward error**: it is a
four-value enum check, it is the clause the non-conforming example fires on most cleanly, and C9's
entire guard depends on it. C33 (path and immutability) is separately noted in its own cell as
CI-checkable and then dropped from the CI list.

**Remedy:** make §6.3 step 1 the single authoritative list of buildable checks and derive §6.2's E1
column from it, rather than maintaining two rosters that disagree.

**5.2 §6.2's `n` column counts halves as wholes.** E0 is listed as **n=9** against seven whole clauses
plus two halves; E1 as *"23 whole + 2 halves."* The arithmetic reconciles to 34 only if the reader
notices the two columns use different counting conventions. Minor, but this is the table a reader uses
to judge the document's ceiling.

**Remedy:** one convention. Count halves as halves in both rows, or promote every split half to its own
clause number.

**5.3 The E1 population is overstated by three.** With C11, C31 and C32 correctly tiered, the honest
figures are **E0 = 10 whole + 5 halves · E1 = 20 whole + 5 halves · E2-nominal = 2 · E3 = 0.** The
document's ceiling is slightly lower than it says.

---

## 6. Ruling on the author's zero-E3 self-assessment

**The self-assessment is ACCURATE in its conclusion, and I checked it in both directions.**

The document claims (§6.3): zero E3 clauses; and the two E2 clauses (C9, C18) are E2 in name only,
because the curator is an LLM following a markdown rule and §5.1 is a settled owner constraint that an
LLM is not a final authority over another LLM.

**Checked for over-harshness** — is any clause actually enforced at a chokepoint the bound party cannot
reach?

- **No.** I looked for one. C24 is the closest candidate: expiry as a pure function of the record and a
  clock cannot be evaded by inaction. But it can be evaded by editing the record, and under D15 —
  which I verified in `product/factory/decisions.md` §D15 and in three workflow files — research
  documents land on `main` continuously with **no branch and therefore no required check**. C33 puts
  contract records on exactly that path. The artifact-plane chokepoint the author names does not
  currently apply to the surface the records live on. The author states this; it is correct.
- The one platform-side fact the author did not consider is that **`created_by` is server-recorded and
  the writing agent cannot rewrite it after the fact** (see §7). That is a genuine tamper-evidence
  property at a place the bound party cannot reach. But **no clause in this specification binds to it**,
  so it creates no E3 clause. The conclusion stands.

**Checked for over-generosity — the more dangerous direction, and where I found error.** The
*conclusion* is not generous, but the *table supporting it* is, in three places: **C11, C31 and C32 are
tiered E1 on vacuous enforcement points** (§3.1). Each is an instance of the same class the author
correctly identifies for C9 and C18 — a tier above what the enforcement point delivers — and the author
caught it at the E2 boundary while missing it at the E1 boundary. The E1 tier is defined as *"a pure
function of the record could check it"*; a human reviewer with a frequency table, a second implementer
comparing conclusions, and a comparison nobody performs are none of them pure functions of anything.

**Ruling:** the zero-E3 claim and the E2-nominal/E0-actual analysis of C9 and C18 are **sustained**. The
enforcement table that supports them is **overstated by three clauses**. The author applied its own
discipline rigorously at the top of the tier stack and inconsistently one tier down. Correcting it
lowers the document's claimed ceiling, which strengthens rather than weakens §6.3 and §10.1.

**One correction in the opposite direction, for completeness:** the author is *unnecessarily* pessimistic
about C9, which has an unclaimed E1 record-level check (§3.4). Both errors should be fixed; the
generous one is the one that matters.

---

## 7. The D6 contradiction — verified, and worse for the corpus than the author states

**The contradiction is real. I read both sources and then checked the live graph, and the live graph
settles it.**

**Source 1 — `.claude/rules/unimatrix-access.md`, §"agent_id (D6 — open)", line 68:**

> *"Pass `agent_id` on every call (e.g. `{run-id}-{role}`). **Caveat:** attribution does not yet persist
> (writes record `created_by: anonymous`); treat audit attribution as not-yet-trustworthy until the
> platform agent registry lands."*

**Source 2 — GitHub Issue #40, the response comment.** The raw JSON contains
`"created_by":"opcost-001-curator"` and `"created_by":"opcost-002-curator"` on nodes 113, 118–120, 125,
127–129, and `"created_by":"platform-vision-curator"` on node 97. The author reported this accurately.

**What the author missed, in the same comment it was quoting from.** The Issue #40 responder did not
merely emit contradicting JSON — **it stated the contradiction explicitly and drew the conclusion**:

> *"**(a) `created_by`** → `"platform-vision-curator"`. **This one is populated, not `anonymous`** — so
> D6 is *partly* stale: attribution *does* persist for at least some writers now. (Our own access rules
> still carry the D6 caveat; treat "always anonymous" as no longer universally true — verify per-node.)"*

The draft's §12.7 says *"I did not resolve it because resolving it is re-research."* **It was already
resolved, in the primary corpus document, in prose, immediately above the JSON the author quoted.**
The author quoted the evidence and skipped the responder's stated finding. That is a corpus-reading
defect, not a research gap, and it is the sort that matters: the resolution was in hand and was
reported as absent.

**Live verification (read-only, three calls, zero writes).** Because the Issue #40 records are five
weeks old, I checked whether attribution persists *today*:

| Node | Created | `created_by` |
|---|---|---|
| 97 (`context_graph(mode:"current")`) | 2026-06 | `platform-vision-curator` |
| 260 (`context_search`) | 2026-08-04 | `jurati-001-curator` |
| 266 (`context_search`) | 2026-08-08 | `jurati-001-retro-curator` |

**D6's clause "writes record `created_by: anonymous`" is refuted, currently and at three independent
points, including a write from five days before this review.** Attribution persists. The rule file is
stale.

### What this does to C8 and C9

D6 as cited in C8 carries **three** assertions. They do not fail together, and the distinction is the
whole answer:

| D6 assertion | Status | Effect |
|---|---|---|
| *"writes record `created_by: anonymous`"* | **REFUTED** — verified live, three nodes | C8's stated grounds are wrong in one of three limbs |
| *"attribution does not yet persist"* | **REFUTED** — same evidence | C8's stated grounds are wrong in a second limb |
| *"`agent_id` is a self-reported string"* | **INTACT** — `created_by` is populated *from the caller's own `agent_id` parameter*; every value observed matches the `{run-id}-{role}` convention the caller supplies | **C8's and C9's conclusions survive** |

**The conclusions of C8 and C9 are sound; two-thirds of their stated grounds are false.**

What has actually changed is that the system moved from *no attribution* to *durably recorded
self-assertion*. That is a real improvement — it is tamper-evident, since the writing agent cannot
revise `created_by` after the fact without another write — and it is **still not attestation**. The
value is whatever string the caller passed. `identity_basis: self-asserted` remains the correct value
for every record. C8's prohibition on `registry-asserted` and `attested` remains correct. C9's ceiling
remains correct.

**Effect on checkability — this is the answer to the gate question:**

1. **Neither clause becomes uncheckable.** Both are enum/predicate checks over the record; their
   checkability never depended on D6 being true. D6 supplies the *justification*, not the *predicate*.
2. **C8's Source cell is factually wrong and must be corrected**, because it is the citation a future
   reader would use to decide whether C8 can be relaxed. A reader who resolves the contradiction the
   way the Issue #40 responder did — "D6 is stale, attribution persists" — and does not carry the
   caller-controlled distinction will conclude C8 is obsolete and permit `attested`. Given §1.6, that
   single edit defeats C9. **This is a live path from a stale rule file to the collapse of the file's
   most restrictive clause.**
3. **§6.3 step 4 must be rewritten.** It says C8 can move off `self-asserted` when *"D6 [is] resolved."*
   D6 is now partly resolved and C8 must **not** move. The unlock condition is not "attribution
   persists" — it is "a party other than the caller vouches for the identity." Those are different
   events and the document conflates them.
4. The author's own §12.7 flag — *"the single most restrictive clause in this document may be
   over-restrictive"* — is **wrong, and wrong in the generous direction.** C9 is not over-restrictive.
   Persisted self-assertion is still self-assertion. Anyone acting on §12.7 as written would relax C9
   on a false premise.

**Remedy:** (a) correct C8's Source cell to cite only the surviving limb — *"`agent_id` is a
self-reported string; `created_by` persists it verbatim, which records the assertion without verifying
it"*; (b) rewrite §6.3 step 4's unlock condition to *"a party other than the caller attests the
identity"*; (c) replace §12.7 with the resolution rather than the open question, and note that the
Issue #40 responder had already stated it; (d) **flag `.claude/rules/unimatrix-access.md` D6 to the
curator as stale** — that is a graph/rules correction, outside both my authority and the author's, and
it should be routed to the owner rather than fixed in this document. **This review makes no such
change and writes nothing.**

---

## 8. Provenance spot-checks

I sampled eight `derived` and three `adapted` clauses against their named sources. **Most hold.** Two do
not, and both are load-bearing.

**Verified accurate:** C27's triage B-1 quote (verbatim, including the "systematically, in the agent's
favour, forever" consequence) · C30's OWNER-DIRECTION §8 quote, line 266, verbatim · C31's *"zero labels
and zero assignees"* — I confirmed via `gh` that Issue #40 has 0 labels, 0 assignees, 1 comment ·
C23's *"still `OPEN`, five weeks"* — confirmed, `state: OPEN`, created 2026-07-16 · C17's H30
adaptation, including the *"a staller can stop attesting … quietly reintroducing a clock"* quote,
line 242, verbatim · C22's fracture #7 quote, line 256, verbatim.

**DEFECT — C20's central provenance claim is half wrong.** C20's Source cell reads: *"**The strongest
derived clause in the file: the responder volunteered exactly this and the request never asked for
it.**"* The corpus brief §2 lists, among **fields the request DID carry**:

> *"provenance obligation on the responder ('for each, tell us the `goal_id`/`run_id`/node id you
> targeted')"*

The request also specified the exact call to issue for each of five items. So `provenance.method` — the
calls actually issued — was **substantially prompted**. Only `provenance.attestation` (*"every call
above was read-only … nothing was written to the graph"*) was volunteered. C20 bundles both fields into
one clause and claims both were unprompted.

The clause is still correct and still well-grounded. But it is the clause the document nominates as its
strongest derivation, and its strength is overstated by half. A reviewer checking derivation quality
would find the flagship claim inflated.

**Remedy:** split the claim in the Source cell — `method` was requested (per-item targets and exact
calls); `attestation` was volunteered. The volunteered half is the interesting evidence and it survives
intact.

**DEFECT — §7's provenance claim about the conforming example is false.** §7 opens: *"It is real, and
**every value below is taken from the actual exchange rather than invented**."* Against the corpus
brief's measured delta list, at least four values were invented:

| Value in §7 | Corpus brief §2, "fields the request did NOT carry" |
|---|---|
| `expires: {by: "2026-07-30T00:00:00Z"}` | *"no deadline / expiry / by-when"* |
| `acceptance.evidence_floor: "claimed"` | *"no confidence-required / evidence grade / evidence floor"* |
| `disclosure` block with `classification` / `onward` | *"no information classification or onward-disclosure rules"* |
| `contract_id: "xp-2026-0716-uni-ground"` | *"no schema version of the request itself"*; #40 had no id of its own — C2's own Source cell says *"the exchange **was** the Issue"* |

This is a checkability defect, not a design one. A reader trusting that sentence treats the conforming
example as a **measurement** of Issue #40 rather than a **reconstruction with four invented fields** —
and the four invented fields are precisely the ones the specification adds beyond what the corpus
demonstrates. The example is where the over-fitting the author worries about in §10.2 would be visible,
and the sentence tells the reader not to look.

**Remedy:** replace with *"Values marked ● are verbatim from the exchange; values marked ○ are the
fields this specification adds, shown populated as they would have been."* Mark the four. That turns
§7 from a claim into a demonstration and makes the schema's delta over the corpus directly visible —
which is the thing §10.2 says it cannot show.

---

## 9. Two owner fields dropped without a record — DEFECT

The corpus brief's §1 instruction was explicit: *"Do not silently normalise this — if you split or
merge, say which and why."*

The draft accounts for §8's field 4 (authority, §3.3) and field 10 (model/runtime provenance, §9). Two
of the owner's fields appear **neither in the record nor in §9's "Deliberately left out" table**:

- **§8 field 3 — "workflow instance, phase, role, and task context."** Zero occurrences of "task
  context", "workflow instance", or "role" as a field anywhere in the 773 lines. Note that C11 would
  probably cut it (`Roles:` is 1/12 in the frequency table, and #40 addressed a role rather than a
  principal) — but the document never says so.
- **§8 field 9's second half — "escalation destination."** The word "escalat" appears **zero times** in
  the document. `return_to` carries `channel` and `address` and no escalation path. The corpus brief
  lists *"no escalation destination if refused or partial"* among #40's measured gaps, so this is a
  field with corpus support that vanished without comment.

A reviewer cannot check the record's coverage of the owner's brief, because the accounting is
incomplete. §9 is the coverage instrument and it has two holes.

**Remedy:** add both rows to §9 with the C11 reasoning that cuts them. Field 3 is a clean C11 cut and
should say so. Escalation is not — it has corpus support — so it needs either a row in §4.2
(`return_to.escalation`) or an explicit deferral with a reason.

---

## 10. Does anything imply proof, ratification, or graph movement it has not earned?

**The header block is exemplary** — the best I have seen on a factory draft. It names the status, the
absence of a `context_cycle`, the absence of graph writes, D7, and the three reviews not yet passed. It
should be the template. §10.1 volunteering the strongest objection against itself, and stating *"that
defence is unfalsifiable in the direction that matters, and it is precisely the defence every one of
the six inert instances would have offered"*, is the opposite of overclaiming.

**Four residual defects, all vocabulary, none substantive:**

1. **§2's "rulings."** *"Two rulings I was asked to make, **made**"* · *"**Ruling:** define the RETURN
   record once"* · *"Ruling B — … **rejected** as a v0 design commitment, and **accepted** as a target
   invariant."* An unratified draft cannot *reject* a hypothesis from the estate's ledger or *accept*
   an invariant. Rejected and accepted are disposition words in a document whose whole subject is that
   disposition requires a named acceptor. **Remedy:** "recommended ruling", "recommends rejecting for
   v0". One word each.
2. **§4: "Field names below are normative."** and **C11: "Requiredness rule (normative, for anyone
   extending this schema)."** A draft's field names are not normative until ratified, and C11 binding
   "anyone extending this schema" asserts standing over future authors that no gate has granted.
   **Remedy:** "normative **if ratified**". C11: "**proposed** requiredness rule."
3. **§2: "Re-open the collapse when both preconditions land."** An instruction to the estate. **Remedy:**
   "recommends re-opening."
4. **§7: "It is real, and every value below is taken from the actual exchange rather than invented."**
   The strongest overclaim in the document, and it is a claim about *evidence*, not vocabulary — see
   §8 above. This is the one that would actually mislead.

**No sentence implies graph movement.** No `proven` claim is made anywhere. No `context_*` write is
described as having occurred, and none did.

---

## 11. Defect register

| # | Defect | Where | Severity | Remedy |
|---|---|---|---|---|
| **D1** | C2's detection rule (`<owner>/<repo>#<n>`) does not match the example's value (`arch-research#57`); a literal linter passes it | §8 table | **Blocking** | Restate the rule as a property, or change the example's value |
| **D2** | Conforming example fails C18 (`kind: "verbatim tool output"` ∉ `missing\|claimed\|partial\|proven`); alternatively C18's `kind` half is unfalsifiable | §7 vs C18 | **Blocking** | Split C18; enumerate a `kind` vocabulary or delete that half |
| **D3** | C10 requires `disclosure`, which fails all three limbs of C11; C10's stated justification is false | C10 vs C11 | **Blocking** | Add a fourth C11 limb citing the owner's sensitive-information failure class, or demote to OPTIONAL, or record an explicit exception |
| **D4** | C11, C31, C32 tiered E1 on vacuous enforcement points | §5, §6.2 | **Blocking** | Re-tier to E0; restate the cells; supply C11 a lookup procedure if E1 is wanted |
| **D5** | §7's "every value is taken from the actual exchange rather than invented" is false for ≥4 values | §7 | **Blocking** | Mark verbatim vs added values |
| **D6** | C8's cited grounds are two-thirds refuted; §6.3 step 4 and §12.7 would license relaxing C9 on a false premise | C8, §6.3, §12.7 | **Blocking** | Cite only the surviving limb; rewrite the unlock condition as third-party attestation; replace §12.7 with the resolution |
| **D7** | "exactly four clauses" vs a five-row / six-clause table | §8 | Major | State the count from the table |
| **D8** | C9's guard is defeated by the C8 violation the author's own example commits | C8/C9 composition | Major | Invert C9 to fail closed; state the composition |
| **D9** | §6.2 and §6.3 disagree on the mechanizable set; C8 and C9 dropped from the linter | §6.2 vs §6.3 | Major | One authoritative list; add C8, C9 |
| **D10** | C14, C26, C32, C34-sentence-1 are unfalsifiable but numbered as clauses | §5 | Major | Restate as definitions/defaults/consumer rules outside the clause table |
| **D11** | C20's flagship provenance claim ("the request never asked for it") is half false — `method` was prompted | C20 | Major | Split the claim; keep the attestation half |
| **D12** | §8 field 3 and "escalation destination" dropped with no row in §9 | §9 | Major | Add both rows with the C11 reasoning |
| **D13** | C20, C22, C27 tiered E0 against a truth question the clause does not ask; presence halves unclaimed | §5.3, §5.4 | Minor | Split as C15/C16 are split; add to the linter list |
| **D14** | §7's `prev` uses `sha256:<...>` against §4.1's `<hex hash>`, and the digest is a placeholder | §4.1 vs §7 | Minor | Pick one format; compute a real digest |
| **D15** | Decision vocabulary in an unratified draft ("rulings", "normative", "re-open") | §2, §4, C11 | Minor | Recommendation vocabulary |
| **D16** | §6.2's `n` column counts halves as wholes | §6.2 | Minor | One counting convention |

**Six blocking, six major, four minor.** Every one is a text edit or a re-derivation against material
already on disk. None requires a new experiment, and none touches the design.

---

## 12. What I did not judge

Out of scope by the gate's terms and untouched here: whether the specification is **correct**; whether
the estate should **adopt** it; whether Ruling A or Ruling B is **right**; whether the record has the
right **shape**; whether §10.1's null-hypothesis objection should **park the line**; and whether the
three refusals in §3 were the right calls. Those are the goal-owner's and the owner's rulings.

The author's §10.1 recommendation — *"this draft should not be ratified until P-1 is answered"* — is a
recommendation I am not empowered to endorse or reject. I note only that it is checkable: P-1 has a
stated cost (one Edit in a throwaway repo) and a binary outcome, which is more than most of the
document's open questions carry.

**Also not done, deliberately:** I repaired nothing. I wrote nothing to Unimatrix. The three `context_*`
calls made during this review were `context_graph(mode:"current")` and `context_search`, both read-only.
The stale D6 caveat in `.claude/rules/unimatrix-access.md` is flagged in §7 for the owner and the
curator; **I did not edit it.**

---

## 13. What would clear this gate

A revision that fixes the six blocking defects. Concretely, and in the order a reviewer would check
them:

1. Make the non-conforming example fail on **rules as literally stated** — fix D1, reconcile the count
   (D7), and re-run all 34 clauses against both examples, publishing the full pass/fail matrix rather
   than the five nominated rows. **The matrix is the deliverable that makes this document reviewable**;
   its absence is why four of these defects survived to me.
2. Make the conforming example **actually conform** — D2, D14 — and mark its invented fields (D5).
3. Resolve **C10 against C11** (D3) and state the resolution.
4. Re-tier **C11, C31, C32** honestly and re-publish the §6.2 counts (D4).
5. Correct **C8's grounds, §6.3 step 4, and §12.7** against the live `created_by` evidence, keeping the
   caller-controlled distinction explicit (D6).

That revision would be checkable as written. It would still be `claimed`, still unratified, and still
have zero E3 clauses — none of which this gate can change.

---

*Checkability review only. Not a firewall gate. No grade recommended, because no node or capability is
in play. Iteration 1 of a maximum 2.*
