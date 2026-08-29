#!/usr/bin/env python3
"""
Generate artifacts/wfh-008-coverage.csv.

Every X-alphabet item is ENUMERATED MECHANICALLY from the pinned model so that no item can be
silently omitted. Dispositions for construct fields, relations, registry seeds and value members
are DERIVED FROM THE INSTANCE (a field is `exercised` iff an instance object carries it), so the
witness column cannot drift from the artifact. Invariants, principles, notation, exclusions, OPEN
items, S1-S8 and the required traversals carry authored rulings from the tables below.

Usage: python3 wfh-008-coverage-gen.py <model.yaml> <instance.yaml> <counterfactual.yaml> <out.csv>
"""
import sys, csv, yaml, collections

model_p, inst_p, cf_p, out_p = sys.argv[1:5]
M = yaml.safe_load(open(model_p).read())
I = yaml.safe_load(open(inst_p).read())
CF = yaml.safe_load(open(cf_p).read())
MODEL_PATH = "product/factory/proposals/organizational-data-model-v5.yaml"

OBJS = [(c, r) for c, rows in I['instances'].items() for r in rows or []]
BY_C = collections.defaultdict(list)
for c, r in OBJS: BY_C[c].append(r)

SUPER = ['cause_classification','classification_evidence','current_project_fit','evolution_change',
         'independent_reason','semantic_proof_authority_custody_preservation','migration_cost',
         'affected_artifacts','current_form_representable','evolved_form_representable',
         'post_evolution_fit','unresolved_discriminator']
NA = {k: 'not-applicable' for k in SUPER}

# --------------------------------------------------------------------------- pressures
def P(cause, ev, cur, chg='not-applicable', why='not-applicable', pres='not-applicable',
      cost='not-applicable', art='not-applicable', cur_rep='yes', evo_rep='not-applicable',
      post='not-applicable', unres='not-applicable'):
    return dict(cause_classification=cause, classification_evidence=ev, current_project_fit=cur,
                evolution_change=chg, independent_reason=why,
                semantic_proof_authority_custody_preservation=pres, migration_cost=cost,
                affected_artifacts=art, current_form_representable=cur_rep,
                evolved_form_representable=evo_rep, post_evolution_fit=post,
                unresolved_discriminator=unres)

PRESSURE = {
"PR-SCOPE-AUTHORITY-ROOT": P("model-defect",
  "SC-TEAM and SC-MIS are nested Scopes holding no undelegated authority, yet Scope.authority_root_ref is required and defined as 'holder of undelegated authority for this Scope'. Naming the owner makes the field non-informative on every nested Scope; naming the leader asserts undelegated authority the leader did not hold (authority laundering).",
  "strained-representable: encoded as AC-OWNER on all four Scopes, so the field carries no information below the collective"),
"PR-SCOPE-EFFECTIVE-AT": P("historical-evidence-gap",
  "Scope.effective_at is required; the fixed alphabet establishes no founding date for the collective. Encoded as a lower bound from the earliest method commit 1a9b3d3 (2026-06-24) and marked _approx.",
  "representable with an approximated value"),
"PR-CAPABILITY-ABSENT": P("historical-evidence-gap; model-defect",
  "R01 states the capability target is 'proposed jurati-arch-002 - no Unimatrix capability id'. V5's Capability requires name, observable_behavior, scope_ref, done_when and grade. The alphabet supplies none of observable_behavior or done_when, and inventing them is forbidden. Capability also has no lifecycle_state field (Goal, Actor and Record all do) and no admissible 'proposed / not yet specified' state, so a Goal may name a capability target that the model cannot represent at all.",
  "NOT REPRESENTABLE: zero Capability instances. I9, I13, I14, capability_classification, Capability.composed_of/prerequisite_of/delivered_by/enabled_by, Unit.delivers, Technology.enables and Goal.claim_floor are all VACUOUS in this case.",
  chg="not-proposed", why="the only reason to invent an observable_behavior and a done_when here is to make V5 pass - the circular candidate the amendment forbids; see CF-REJECTED",
  cur_rep="no", evo_rep="not-applicable", post="not-applicable",
  unres="whether V5 needs a proposed/unspecified Capability state, or whether the project is right that a capability id is created only when a behavior is identified, is not decidable from one case"),
"PR-LIST-REQUIRED": P("model-defect",
  "Goal.claim_floor is 'list<ref<Capability>>, required: true'. notation does not say whether `required` on a list type means 'key present' or 'non-empty'. The instance writes [] and a checker cannot decide whether that conforms.",
  "ambiguous: encoded as an empty list; a rejecting counterexample cannot be constructed until the notation resolves"),
"PR-ACTOR-IDENTITY-SINGULAR": P("model-defect; unresolved",
  "Actor.declared_identity is a single text field. AC-OWNER carries three identity strings across two custody stores (GitHub login dug-21; git author 'Doug Faist'; git committer 'dug-21 <angryweed@gmail.com>'). Separately, seven researchers, two auditors, four rework researchers and one corrections researcher share the single value 'factory-researcher', so declared_identity does not individuate an Actor at all - the only individuator in the instance is the Delegation's unit.",
  "representable but non-discriminating",
  chg="not-proposed", why="a per-instance agent_id would individuate, but .claude/rules/unimatrix-access.md D6 rules the opposite explicitly; relitigating a ratified decision from outside its evidence is out of scope",
  cur_rep="yes",
  unres="whether the model should carry multiple declared identities per Actor, or the project should individuate, cannot be settled from one case and one standing decision"),
"PR-ACTOR-CONTINUITY": P("model-defect; historical-evidence-gap",
  "AC-LEAD-1 and AC-LEAD-2 share declared_identity 'research-leader' and operate the same Unit under two Delegations. Actor is versioned:false and its own open list names 'replacement and continuity'. The model cannot say whether these are one Actor or two, and the case cannot decide it either.",
  "encoded as two Actors; the choice is unforced by the model", unres="one Actor with a lifecycle, or two Actors with a handover relation - the alphabet does not discriminate"),
"PR-SKILL-EVIDENCE-ABSENT": P("historical-evidence-gap",
  "Actor.has_skill declares attributes [evidence_refs, grade, currentness, expires_at]. Not one of the four is populated for any of the 22 Actor-Skill pairs in the instance: agents are assigned by type, never by evidenced competence. SK-BUDGET-CONTROL is the sharpest case - the run failed on credit exhaustion while the Skill carried no grade and no expiry.",
  "structurally representable, evidentially empty"),
"PR-SKILL-NAME-COLLISION": P("project-evolution-candidate; unresolved",
  "The Skill instances are lifted from the `capabilities:` frontmatter key in .claude/agents/factory/*.md. The project's word 'capabilities' denotes V5 Skill (competence), not V5 Capability (an observable behavior required by a Goal). I10 exists to keep these apart and the project's vocabulary runs them together.",
  "representable; the collision is lexical, not structural",
  chg="rename the agent frontmatter key from `capabilities:` to `skills:`",
  why="the garage already maintains a separate Unimatrix `capability` category with a different meaning, and wfh-010 spent a workstream on exactly this conflation; the rename removes a real reader ambiguity in the repo regardless of V5",
  pres="pure rename; no semantics, proof, authority or custody move",
  cost="ten agent definition files, any tooling that reads the key, and the onboard skill; low but touches the method surface, so it is itself an adaptation Event",
  art=".claude/agents/factory/*.md; .claude/skills/factory-onboard/SKILL.md",
  cur_rep="yes", evo_rep="yes", post="identical V5 shape; the model gains nothing and the repository loses an ambiguity",
  unres="whether the collision has ever caused a concrete error is not evidenced by this case"),
"PR-ROLE-UNDEFINED-ASSESSOR": P("historical-evidence-gap; project-evolution-candidate",
  "Gate.requires_assessor is cardinality 1 to a Role. GT-COVERAGE's assessor is RO-COVERAGE-AUDITOR, which has NO definition file under .claude/agents/ - it is a duty handed to a factory-researcher. The protocol's factory-validator is reserved for validated runs, so a directional run has no defined gate-assessor Role.",
  "representable only by authoring a Role the project never defined",
  chg="declare the coverage-auditor duty explicitly, either as its own role contract or as a named independence clause on factory-validator covering directional runs",
  why="wfh-010's equivalent gate was ruled by a factory-validator and wfh-008's by a factory-researcher; the same blocking gate was assessed by two different role identities in consecutive runs, which is a real inconsistency independent of any model",
  pres="preserves; the independence constraints are already written in the audit headers and would simply move into the contract",
  cost="one new or amended agent definition plus one protocol line",
  art=".claude/agents/factory/factory-validator.md; .claude/workflow/research-scope.md",
  cur_rep="yes", evo_rep="yes", post="Gate.requires_assessor then resolves to a defined Role rather than an inferred one"),
"PR-METHOD-CUSTODY": P("enforcement-gap; project-evolution-candidate",
  "I18 requires Workflow/Gate/Delegation custody to sit outside the governed activity. All method definitions live in .claude/ inside the repository the governed agents write to; there is NO CODEOWNERS file and no branch-protection artifact in the tree. The most recent revision of research-scope.md (9d7806a, 2026-08-27) was authored by the agent identity 'Claude Opus 4.8' - the governed actor class edited its own governing definition. Separately, an npx install silently overwrote twelve method files on 2026-08-27 with no decision Event.",
  "representable, and the instance records the custody as prose because there is nothing else to record; definition_custodian_ref is marked _approx on WF-RESEARCH-SCOPE",
  chg="see CF-02 - a sha256 manifest over the method surface plus a drift check",
  why="an evidenced integrity incident that nothing detected mechanically; the argument is about that incident, not about a data model",
  pres="detects drift; explicitly does NOT establish custody, because the manifest is itself editable by the governed party (the #320 predicate applies to it)",
  cost="one manifest, one hook, one protocol line; recurring regeneration on legitimate method change",
  art=".claude/settings.json; a new .claude/METHOD-MANIFEST.sha256; .claude/workflow/research-scope.md",
  cur_rep="yes", evo_rep="yes",
  post="detection improves; I18 remains UNSATISFIED in both forms - the evolution does not repair it",
  unres="open.custody_enforcement says no common enforcement point exists; whether I18 is satisfiable inside a single repository at all is not decidable here"),
"PR-DELEGATION-UNIT-CARDINALITY": P("model-defect",
  "Delegation.unit is cardinality 0..1. Three historical rework directives each covered several Units (pass 1: W1+W2+W4; pass 2a: W1+W2; pass 2d: W5+W7). Each had to be split into separate Delegations, so one organizational grant becomes N model objects and the fact that they were one directive is lost from the typed structure.",
  "representable only by splitting; DL-RWK-P1 became DL-RWK-P1-W1/W2/W4, DL-RWK-P2A gained DL-RWK-P2A2, DL-RWK-P2D gained DL-RWK-P2D2"),
"PR-DELEGATION-ATTENUATION-COMPARISON": P("model-defect",
  "I17 says a derived Delegation may not exceed its parent 'on any axis'. The checker decides two axes (autonomy_tier is ordinal; effect_grants is a set) and reports 20 derived Delegations UNDECIDABLE on escalation_conditions and resource_ceiling, because the model supplies no ordering for a text list or a heterogeneous map. open.delegation_attenuation names this.",
  "PARTIALLY CHECKABLE - and the checkable half worked: it rejected a first-pass encoding that gave the leader's close grant graph-write its parent lacked, which was a genuine modelling error"),
"PR-DELEGATION-SELF-GRANT": P("model-defect",
  "DL-SCOPE has grantor AC-LEAD-1 and grantee AC-LEAD-1. V5 has no rule forbidding self-delegation and no check detects it; the scope-authoring Unit was self-assigned by the actor that then requested its own gate.",
  "representable and undetected"),
"PR-GATE-PROCEDURE": P("model-defect",
  "Gate.procedure is enum[deterministic,judgment]. GT-COVERAGE ran deterministic enumerations (git ls-files, sorted-set diffs, a 42/42 lock bijection) AND independent semantic judgment, and the final PASS turned on the judgment half - the auditor's own third sweep. Neither enum value is true. Encoded as `judgment` and marked _approx. open.deterministic-versus-judgment on Gate names the same hole.",
  "strained-representable with an approximated value"),
"PR-GATE-IDENTITY-VERSION": P("historical-evidence-gap; model-defect",
  "The assessment event type requires gate_version_ref. The historical gate has no independent identity or version - it is a paragraph in a protocol file. The instance pins 'GT-COVERAGE@v1 (git:.claude/workflow/research-scope.md)', which the checker cannot resolve to a versioned Gate object, so the gate_outcome vocabulary resolution degrades to a WARN. open.gate_identity names this.",
  "representable only by inventing a version label for a rule that has none"),
"PR-BOUNDARY-CAN-REFUSE": P("model-defect; historical-evidence-gap",
  "EffectBoundary.can_refuse is a required bool, defined as 'a boundary that cannot refuse enforces nothing'. There is no unknown value, while the sibling effect_disposition vocabulary does carry `unknown`. Git and the forge performed effects throughout wfh-008 and never refused one, so neither true nor false is evidenced. The instance therefore declines to instantiate them as EffectBoundaries at all rather than assert an unevidenced bool.",
  "NOT REPRESENTABLE without asserting an unevidenced value; two candidate boundaries are omitted and EV-005 carries a target_boundary_ref that names no instance"),
"PR-ENFORCED-AUTHORITY-ABSENT": P("enforcement-gap",
  "I12's second clause says only an EffectBoundary disposition demonstrates enforced authority. The checker reports Delegation.enforced_by empty on 31 of 31 Delegations. The single refusal receipt in the case (EV-018/EV-019, five refused context_cycle calls) is a PAYLOAD-SHAPE refusal - the run's own disclosure confirms agent_id was present on all five - so it demonstrates schema enforcement, not authority. The garage's strongest custody claim, the single-writer curator rule, has no enforcement point: any actor may call context_store, and the server checks only that an identity string is present, not who sent it.",
  "REPRESENTABLE AND EMPTY: the case demonstrates ZERO enforced authority. This is a correct and important negative, not a model failure.",
  chg="not-proposed", why="making the curator rule enforced needs a credential boundary that does not exist and cannot be costed from the fixed alphabet; proposing it would be the build recommendation this scope forbids"),
"PR-ATTEMPT-DISPOSITION": P("model-defect; project-evolution-candidate; historical-evidence-gap",
  "AT-RUN-1 terminated on platform credit exhaustion. No actor recorded a disposition. Attempt.disposition is required with enum[continue,hold,cancel,rework,complete] - no abandoned/interrupted/unknown value exists. `hold` is written and marked _approx; it is a reconstruction by AC-COORD, not the attempt's own record. This is the same argument the review's R2 finding made for splitting gate_outcome from assessment (an abandoned assessment must leave a trace), applied to Attempt, where V5 did not apply it.",
  "NOT FAITHFULLY REPRESENTABLE",
  chg="see CF-03 - the reconstructing coordinator writes a typed interruption record against the interrupted Attempt",
  why="wfh-008 lost every phase boundary for two phases and the replacement leader reconstructed state by hand across three surfaces; the run itself carried this into factory-retro as a lesson",
  pres="preserves only if the record stays explicitly authored by the RESUMING actor at reconstruction time and never claims to be the interrupted actor's own disposition",
  cost="theme-coordination protocol, the leader and coordinator contracts, and a record category; low-moderate. Real risk: a typed handover is easier to write than to write honestly, and the historical comment's best property - naming what is permanently missing and refusing to backfill - is a discipline no schema enforces",
  art=".claude/workflow/theme-coordination.md; .claude/agents/factory/theme-coordinator.md; .claude/agents/factory/research-leader.md",
  cur_rep="no", evo_rep="partially",
  post="STILL NOT FULLY REPRESENTABLE - CF-03 supplies the resume side, which V5 already carries well, and leaves the termination side exactly as it was. The model defect survives the project evolution, per the amendment's rule."),
"PR-ATTEMPT-RESUME-OWNER": P("model-defect",
  "resume_requirements sits on Attempt, but the model does not say which Attempt owns it. Historically the payload was authored by the RESUMING actor (AC-LEAD-2) about the INTERRUPTED attempt. The instance places it on AT-RUN-2.",
  "representable; the placement is unforced and two readings are equally conforming"),
"PR-OBSERVATION-RAW-EVIDENCE": P("historical-evidence-gap; project-evolution-candidate",
  "event_type observation requires raw_evidence_ref. wfh-008 retained NO raw command output for any enumeration against the target repository - only authored summaries. Under I4 those are claims, not observations. Exactly ONE Event in the instance (EV-015) carries a real raw_evidence_ref, and only because git objects are content-addressed and independently re-derivable.",
  "REPRESENTABLE, AND V5 CLASSIFIES IT CORRECTLY - the model refused to let a summary pass as a measurement without anyone arguing about it. This is a positive result for I4.",
  chg="see CF-04 - an audit writes its deciding command outputs to a sibling transcript and cites it",
  why="the round-1 audit reported 38 example manifests, round 2 found 37 and could not attribute the phantom path; a retained transcript settles it in one line, and part of a rework allowance was spent on the question",
  pres="raises the altitude from claim to reported-observation only; it does NOT move capture custody outside the reporting actor, and claiming otherwise would be laundering",
  cost="one convention line plus repository size; risk that a transcript invites the belief a rule was enforced when it was only observed",
  art=".claude/workflow/research-scope.md; .claude/agents/factory/factory-validator.md; reports/ layout",
  cur_rep="yes", evo_rep="yes", post="raw_evidence_ref becomes real; V5 needs no change either way"),
"PR-RECORD-DIGEST": P("model-defect; project-evolution-candidate",
  "Record.content_digest is a required digest. Eleven of the 22 Record instances cannot supply one: Unimatrix exposes no content digest through its read API, the forge exposes none for an Issue, and the cycle service exposes none. The overwritten skill state was never captured at all. Sentinels are written and every one is reported by the checker as MODEL-FORCED-APPROXIMATION.",
  "HALF REPRESENTABLE: file-backed Records carry real sha256 values; every service-backed Record cannot.",
  chg="expose a content digest on knowledge-node reads",
  why="a digest is what lets a later reader prove a cited node is the node that was cited; the run's own goal-owner re-read #316-#319 and could verify ids, status and edges but not content - it says so explicitly",
  pres="preserves; a digest adds verifiability and moves no authority",
  cost="a change to a service outside this repository, which this scope cannot cost and must not recommend building",
  art="the Unimatrix read API; out of this repository",
  cur_rep="partially", evo_rep="yes",
  post="Record.content_digest becomes satisfiable for knowledge nodes",
  unres="whether the model should relax content_digest to optional for externally-custodied Records, or the stores should expose one, is not decidable from one case"),
"PR-RECORD-INPLACE-OVERWRITE": P("enforcement-gap",
  "I1 says history is superseded, never overwritten, and Record.supersedes says correction never overwrites history. RC-COV-R2 was AMENDED IN PLACE twice after publication (commit 2929599 modified reports/coverage-r2.md), and the findings Records were edited in place across three rework passes and one correction pass. No Record identity was reissued; the prior versions survive only in the git object store - whose own identities were later rewritten (PR-BASELINE-REWRITE). The run's honest practice of retaining the superseded verdict verbatim INSIDE the amended file is a convention, not a model or tool guarantee.",
  "representable as a version increment; the model's supersession semantics are satisfied by narrative, not by the store"),
"PR-BASELINE-REWRITE": P("enforcement-gap; project-evolution-candidate",
  "MEASURED: a rebase reissued every wfh-008 commit id after the run closed - twelve spread author timestamps against ONE uniform committer timestamp (2026-08-28 14:20:37 -0400), author identity preserved, committer dug-21 <angryweed@gmail.com> applied uniformly, matching a reflog `rebase (finish)`; trees identical across every pair tested. wfh-010 W1 records the mismatch as differing 'displayed abbreviations'; that reading is wrong - they are different objects. No adaptation Event exists for the rewrite and git holds no supersession link from the new id to the old, whereas Unimatrix's context_correct reissues an id AND leaves a queryable chain. CORRECTION 2026-08-29: an earlier version of this row asserted that the recorded baselines no longer resolve. RETRACTED - wfh-010's R08 ledger pins the post-rebase oids and all twelve are ancestors of main; the ten pre-rebase short ids quoted in Issue #66 prose are not ancestors but all still resolve via the published branch workflow/agentic-organization-reframe. The pressure survives at reduced weight.",
  "REPRESENTABLE. baseline_ref is `text`, so any commit id conforms and no V5 rule was violated by the rewrite. The residue is narrow: `text` carries no integrity binding, and V5 cannot say whether a baseline's custody store preserves a supersession link.",
  chg="see CF-01 - record baselines as git-tree oids alongside commit ids, and do not rebase a branch after a gate has ruled against it",
  why="ten gate citations in the run's governance record depend for resolvability on a side branch that no policy protects; delete it and they become unresolvable. A modest reproducibility exposure, true with or without V5. The stronger original rationale - that a reader cannot reproduce the audited tree - is WITHDRAWN as false.",
  pres="preserves everything; adds an identifier stable under the operation that reissued the existing one, and retains the original ids",
  cost="one method commit plus, optionally, a dated errata note on the ten prose citations; no existing record is rewritten",
  art=".claude/skills/factory-git/SKILL.md; .claude/workflow/research-scope.md; product/factory/templates/scope.md",
  cur_rep="yes", evo_rep="yes",
  post="identical V5 shape; the pin survives a future rewrite"),
"PR-EVENT-IDENTITY-THRESHOLD": P("historical-evidence-gap; enforcement-gap",
  "Event identity is required 'when consequential or acknowledgement/replay/audit matters'. EV-004 (scope -> tech-discovery) is a durable:always transition whose cycle event NEVER REACHED Unimatrix; it is attested only by an Issue comment. All phase boundaries for the scope phase and the first tech-discovery pass are permanently missing and were deliberately not backfilled. open.event_identity_threshold is exercised as a live hole.",
  "representable; the Events exist in the instance because the Issue attests them, and the model cannot mark an Event as 'occurred but unrecorded by its designated carrier'"),
"PR-INDEPENDENCE-UNVERIFIABLE": P("enforcement-gap",
  "Gate.independence_predicate and the assessment extension's independence_check are required text. Both are populated from the auditors' own headers. At the custody layer nothing distinguishes them: every wfh-008 commit carries the git author 'Claude Opus 4.8 <noreply@anthropic.com>', and all nine Issue comments - including the owner's decisions - are posted by the single GitHub account dug-21. I7 (gates fail closed when independence cannot be established) is therefore never mechanically evaluable in this case.",
  "representable as an assertion; not verifiable by any evidence in the alphabet"),
"PR-LESSON-VS-PATTERN": P("historical-evidence-gap",
  "open.lesson_vs_pattern asks for a behavioral distinction. wfh-008's most reusable method rule - the custody predicate - was filed as a `finding` (#320), not as a lesson-learned, with no separate admission or retrieval behavior. That is one data point AGAINST a behaviorally distinct lesson category and it is weak: nobody tried the alternative.",
  "representable; the case exercises the question and does not settle it"),
"PR-I19-BINDING-ALTITUDE": P("model-defect",
  "I19 (program extensions may not weaken common invariants) is cited by Workflow ALONE, yet this instance registers program-owned extensions on unit_kind, record_category, effect_class and event_type - owned by Workflow, Scope, Scope and the registry respectively. Three of the four owners are not Workflow, so nothing binds I19 to them. Review finding S6 raised exactly this and it is unresolved in the pinned file.",
  "representable; the extensions conform, and no per-construct binding required them to"),
"PR-CAPABILITY-CLASSIFICATION-UNUSED": P("historical-evidence-gap",
  "registry.capability_classification carries four seeds (functional, nonfunctional, threshold, curve). None is exercised, because the case instantiates zero Capability objects. The registry cannot be tested by this case at all.",
  "not exercised"),
}

# --------------------------------------------------------------------------- authored rulings
# (disposition, witness/value, enforcement_reality, open/pressure disposition, pressure_key|'')
R = {}
def rule(xid, disp, val, enf, opendisp, pk=''):
    R[xid] = (disp, val, enf, opendisp, pk)

INV = {
 'I1': ('construct-pressure','RC-UNI-316 supersedes RC-UNI-312 with the deprecated version retained and the chain queryable (verified live 2026-08-29); RC-COV-R2 supersedes RC-COV-R1. BUT the git custody store rewrote ten commit identities, and RC-COV-R2 was amended in place twice.','specified-not-enforced: Unimatrix enforces the chain; git does not, and a rebase reissued every id with no supersession record','I1 HOLDS in one custody store and FAILS in the other; V5 cannot express which store an identity lives in','PR-BASELINE-REWRITE'),
 'I2': ('exercised','RC-RELEVANCE exists, is not admitted by any Event, and produced no consequence - the leader relayed it verbatim and did not act on it. RC-COV-R1 exists and is superseded. #316 exists, is admitted, and its grade never moved.','specified-not-enforced','n/a',''),
 'I3': ('exercised','nine program-owned record_category entries each declare their own schema_extension, admission_rule, retrieval, lifecycle and correction; the knowledge-node and research-finding categories differ on every one of the five','specified-not-enforced: the categories are authored here, not configured anywhere','n/a',''),
 'I4': ('construct-pressure','EV-015 is the ONLY Event with a real raw_evidence_ref (a content-addressed git tree). EV-016 is an observation with epistemic_kind reported-observation. Every target-repository enumeration is encoded as a claim.','specified-not-enforced, but the required_extension makes the gap mechanically visible','I4 correctly refused to let authored summaries pass as measurements','PR-OBSERVATION-RAW-EVIDENCE'),
 'I5': ('exercised','EV-018/EV-019 (refusals) are separate immutable Events from EV-020 (the later success); no Event is edited. The four asserted-but-untrue defects were corrected by a new Unit (UN-CORRECTIONS), not by rewriting the audit Event.','specified-not-enforced','n/a',''),
 'I6': ('exercised','EV-013 (assessment) / EV-014 (gate_outcome) / EV-024 (the coordinator decision confirming it) / EV-023 (transition) / EV-017 (effect_request) / EV-018 (effect_disposition) / RC-COV-R2 (Record) are seven distinct objects with different actors and authorities over one gate','specified-not-enforced','the strongest single positive result in the case',''),
 'I7': ('construct-pressure','GT-COVERAGE.independence_predicate is populated and the round-2 auditor DID fail closed on the leader\'s reading of predicate 6, running its own third sweep instead. But independence is asserted in prose only.','specified-not-enforced: no evidence in the alphabet can establish independence - one git author, one forge account','n/a','PR-INDEPENDENCE-UNVERIFIABLE'),
 'I8': ('exercised','RC-CYCLE.missing_or_unavailable_refs carries four permanent telemetry holes; RC-COV-R2 carries a ten-item gap register; RC-W6 records that its own gate enumeration is not closed. Nothing was backfilled.','specified-not-enforced','the field missing_or_unavailable_refs is what makes this checkable rather than rhetorical',''),
 'I9': ('not-applicable','no Capability instance and no proven grade anywhere; TE-METAHARNESS stayed grade:claimed and GT-FIREWALL was never evaluated','not-applicable','vacuous in this case','PR-CAPABILITY-ABSENT'),
 'I10': ('exercised','16 Skills held by 22 Actors; no Skill grants authority (every grant is a Delegation) and none is a Capability (there are none). SK-FIREWALL-ENFORCEMENT is named a competence and enforced by nothing.','specified-not-enforced','satisfied but weakly tested - the project has no Skill construct, so the Skills are lifted from role frontmatter','PR-SKILL-NAME-COLLISION'),
 'I11': ('exercised','TE-METAHARNESS.enables is empty and its grade stayed claimed across a correction that added substantial evidence; TE-RUFLO and TE-RETORT carry grade missing','specified-not-enforced','satisfied vacuously on the Capability side',''),
 'I12': ('construct-pressure','clause 1 WITNESSED: AC-GOALOWNER holds A0 with high evaluative influence while AC-GIT holds A0 with powerful repository effects - autonomy and effect authority are visibly independent. Clause 2 NOT WITNESSED: enforced_by is empty on 31/31 Delegations.','specified-not-enforced','zero enforced authority in the case; the only refusal receipt is a schema refusal','PR-ENFORCED-AUTHORITY-ABSENT'),
 'I13': ('not-applicable','zero Capability instances; the checker reports PASS vacuously','not-applicable','vacuous','PR-CAPABILITY-ABSENT'),
 'I14': ('not-applicable','zero Capability instances','not-applicable','vacuous','PR-CAPABILITY-ABSENT'),
 'I15': ('exercised','checker witnesses UN-RUN, UN-SCOPE, UN-W1, UN-W2, UN-W4, UN-W5, UN-W6, UN-W7 and UN-AUDIT-R2 with multiple Attempts each; UN-AUDIT-R2 has two Attempts against DIFFERENT baselines under one intended outcome','mechanically checkable on instance data and checked','clean positive',''),
 'I16': ('exercised','UN-CORRECTIONS is modelled as its own Unit rather than further Attempts of UN-W1/W2/W4/W6 precisely because its intended outcome differs; the checker confirms no two Units share an intended_outcome','mechanically checkable and checked','clean positive',''),
 'I17': ('construct-pressure','clause 1 CHECKED on two axes and it caught a real error - a first-pass encoding gave the leader\'s close grant graph-write its parent lacked, and the checker rejected it. Clause 2 (chain to a Scope root) PASSES for all 31 Delegations.','partially mechanically checkable; UNDECIDABLE on escalation_conditions and resource_ceiling for 20 derived Delegations','open.delegation_attenuation exercised, still-open','PR-DELEGATION-ATTENUATION-COMPARISON'),
 'I18': ('construct-pressure','the method surface was NOT edited during the run (no .claude commit on 2026-08-28) - a positive behavioral observation. But an npx install overwrote twelve method files the day before with no decision Event, and research-scope.md was last revised by an agent identity.','specified-not-enforced: no CODEOWNERS, no branch protection, no manifest','open.custody_enforcement exercised, still-open','PR-METHOD-CUSTODY'),
 'I19': ('construct-pressure','four program-owned registry extensions authored (unit_kind, record_category, effect_class, event_type); none weakens a common invariant and none moves semantics into free text - the unrecorded_change type exists precisely BECAUSE adaptation presupposes authorization','specified-not-enforced','S6 unresolved: I19 is bound to Workflow alone while three of the four extension owners are not Workflow','PR-I19-BINDING-ALTITUDE'),
}
for k,(d,v,e,o,pk) in INV.items():
    rule(f"invariant:{k}", d, v, e, o, pk)

PRIN = {
 'small_core':('exercised','all seven core entities present except Capability, which is absent for evidence reasons, not modelling reasons','n/a','the hypothesis survives this case on six of seven core entities','PR-CAPABILITY-ABSENT'),
 'supporting_definitions':('exercised','all eight supporting definitions instantiated; EffectBoundary has exactly one instance and Technology three','n/a','n/a',''),
 'extend_by_registration':('exercised','four registries extended, zero new entities needed - including the unauthorized-change case, which the registry absorbed','n/a','strong positive',''),
 'construct_admission_bar':('exercised','no case behavior required a new construct; the closest call (unauthorized definition change) fitted a registered event type','n/a','n/a',''),
 'separation_is_the_product':('construct-pressure','competence/capability, claim/observation, outcome/decision/consequence and record/effect all held. delivery/proof is UNTESTED (no Capability) and intent/enforcement FAILED on the evidence side - intent is everywhere, enforcement nowhere.','specified-not-enforced','n/a','PR-ENFORCED-AUTHORITY-ABSENT'),
 'authority_chain':('exercised','every Delegation traces to SC-COL\'s authority_root_ref AC-OWNER; checker PASS','partially checkable','n/a',''),
 'program_ownership':('exercised','the program owns nine record categories, eight unit kinds, five effect classes and the proof bar; the common model owns identity and invariants','n/a','n/a',''),
 'method_custody':('construct-pressure','the principle is stated and the project does not implement it','specified-not-enforced','n/a','PR-METHOD-CUSTODY'),
 'inverse_relations':('exercised','24 declared inverses required mechanical closure in this instance - they are real constraints, not decoration. The withdrawn A3 back-pointers (Goal->Workflow, Actor->Attempt) were served by index instead, and both traversals ran.','mechanically checkable and checked','the A3 withdrawal is vindicated by this case',''),
}
for k,(d,v,e,o,pk) in PRIN.items(): rule(f"principle:{k}", d, v, e, o, pk)

NOT = {
 'status':('exercised','OPEN/RESOLVED read on every construct and consumed as test input, not as permission','n/a','n/a',''),
 'identity':('construct-pressure','ids are opaque in the instance. In the project they are NOT: a commit id is content-derived and was reissued, and Unimatrix reissues on correction.','n/a','n/a','PR-BASELINE-REWRITE'),
 'versioned':('exercised','versioned:true constructs carry a version in the instance and versioned:false ones do not; the checker enforces both directions','mechanically checkable and checked','n/a',''),
 'fields':('exercised','all 15 constructs parsed under this notation with no ambiguity except the list<> case','n/a','n/a','PR-LIST-REQUIRED'),
 'relations':('exercised','name/target/cardinality/inverse/rule consumed mechanically','n/a','n/a',''),
 'types':('construct-pressure','text, timestamp, digest, bool, ref<X>, list<ref<X>>, enum[...] and map all exercised. `list` (bare) and `list<text>` appear in the model but are NOT in the declared type vocabulary.','n/a','S3 also notes form/owner/extension_owner are undocumented in notation','PR-RECORD-DIGEST'),
}
for k,(d,v,e,o,pk) in NOT.items(): rule(f"notation:{k}", d, v, e, o, pk)

EXC = {
 0:('exercised','no Feature; the research domain has none. Negative test passes trivially and the software case (W2) is the real test.'),
 1:('exercised','no Qualification object; competence evidence would live on Actor.has_skill attributes, which are empty - the exclusion is not what makes them empty.'),
 2:('exercised','STRONGEST NEGATIVE TEST IN THE CASE. themes.md literally calls the coordinator block an "authority envelope", and wfh-010 W1 carried Envelope as candidate noun N7. It maps field-for-field onto DL-COORD-STANDING (autonomy_tier, effect_grants, resource_ceiling, escalation_conditions, definition_custodian_ref) with nothing left over. Envelope is NOT needed.'),
 3:('exercised','authority reaches every Actor through SC-COL\'s root or a Delegation chain; no AuthorityBasis object was wanted.'),
 4:('exercised','evidence is Records under GT-COVERAGE (assessment.evidence_set); no EvidenceItem needed.'),
 5:('construct-pressure','no RecordVersion object, and Record versions are carried as a version integer. But the historical versions exist only in git, whose ids were rewritten - so the exclusion is fine and the custody is not.'),
 6:('exercised','all seven appear only as Event types; the instance has no Signal/Decision/Transition/Assessment/Outcome/EffectRequest/EffectReceipt section and the checker confirms it.'),
 7:('exercised','EV-017 (request) and EV-018/019/020 (dispositions) are separate; one request produced five dispositions, which a merged event could not represent.'),
 8:('exercised','no organizational-level Capability kinds (no Capability at all); GO-WFH is a Goal and SC-PROG is its Scope, never conflated; Attempt is not a Unit subtype; lesson is not an Event type - #320 is a finding Record.'),
 9:('exercised','no universal lifecycle imposed: Unit states are Workflow-owned, Record lifecycle is Category-owned, and the registries stay open.'),
 10:('exercised','A0 goal-owner has evaluative weight and no effect authority; A0 git has powerful effects and no judgment. Autonomy is neither authority nor evidence strength.'),
}
for i,(d,v) in EXC.items(): rule(f"excluded:{i}", d, v, 'specified-not-enforced', 'negative test', 'PR-RECORD-INPLACE-OVERWRITE' if i==5 else '')

OPEN_TOP = {
 'delegation_attenuation':('construct-pressure','20 derived Delegations undecidable on non-numeric axes','still-open','PR-DELEGATION-ATTENUATION-COMPARISON'),
 'workflow_promotion':('exercised','WF-RESEARCH-SCOPE was needed and instantiated in full from a real protocol file; every Unit follows it','still-open (one case is not adjudication)',''),
 'custody_enforcement':('construct-pressure','no enforcement point exists in this project; measured, not assumed','still-open','PR-METHOD-CUSTODY'),
 'event_identity_threshold':('construct-pressure','EV-004 is durable:always and its designated carrier never recorded it','still-open','PR-EVENT-IDENTITY-THRESHOLD'),
 'gate_identity':('construct-pressure','GT-COVERAGE has no independent identity or version in the project; gate_version_ref is unresolvable','still-open','PR-GATE-IDENTITY-VERSION'),
 'skill_catalog':('construct-pressure','a 16-member collective catalog is authored here from role frontmatter; the project has no Skill construct and no repository-local binding was needed','still-open','PR-SKILL-EVIDENCE-ABSENT'),
 'lesson_vs_pattern':('construct-pressure','#320 filed as a finding, not a lesson-learned; one weak data point against a distinct category','still-open','PR-LESSON-VS-PATTERN'),
 'collective_boundary':('blocked-by-OPEN','SC-COL has an authority root and no membership; succession never arose','not-exercised',''),
 'autonomy_A3_A4':('construct-pressure','A4 is USED (DL-COORD-STANDING) despite carrying status insufficient-evidence; A3 is NOT used - no actor in the case held general local-adaptation latitude, since every adaptation was gate-driven or owner-driven','still-open: A4 gains one instance, A3 gains none','PR-DELEGATION-ATTENUATION-COMPARISON'),
 'capability_rollup':('not-applicable','zero Capability instances','not-exercised','PR-CAPABILITY-ABSENT'),
 'semantic_compression':('construct-pressure','one research case encoded with 191 objects, six of seven core entities and zero new common constructs; that is directional evidence for compression on ONE domain and proves nothing general','still-open',''),
}
for k,(d,v,o,pk) in OPEN_TOP.items(): rule(f"open:{k}", d, v, 'not-applicable', o, pk)

S = {
 'S1':('exercised','independently re-verified: sha256 matches the pin; PyYAML returns all six formerly split scalars complete; a stray-key scan finds none. A0 parses with its non-initiating clause and A5 with its reserved-authority clause.','n/a','CLOSED for this digest',''),
 'S2':('construct-pressure','Gate.evaluates declares the dotted inverse `Unit.gated_by`. The checker had to special-case it and reports four NOTEs. It works, but only because a bespoke resolver understands the qualified form.','specified-not-enforced','still-open',''),
 'S3':('construct-pressure','form, owner and extension_owner were consumed by the checker despite being absent from notation; so were the bare `list` and `list<text>` types','n/a','still-open','PR-RECORD-DIGEST'),
 'S4':('construct-pressure','I1, I4, I5, I12, I15, I17 and I18 each split into independently-failing clauses in this case: I1 holds in one store and fails in another; I12 clause 1 is witnessed and clause 2 is not; I17 clause 2 passes while clause 1 is only half-decidable; I18 has a positive behavioral observation and a negative enforcement result. A single per-invariant verdict is not expressible.','partially checkable','still-open, and the case supplies concrete evidence FOR the split',''),
 'S5':('not-applicable','no historical mixed Delegation exists: standing grants name a Role and no Unit (DL-COORD-STANDING, DL-CUR-STANDING, DL-RESEARCHER-STANDING, DL-RESEARCH-LEADER-STANDING, DL-GOALOWNER-STANDING) and dynamic grants name an Actor and a Unit. The ambiguity is latent, not exercised.','n/a','still-open, not exercised',''),
 'S6':('construct-pressure','three of the four program-owned registry extensions authored here have owners that are not Workflow, and I19 is cited by Workflow alone','n/a','still-open','PR-I19-BINDING-ALTITUDE'),
 'S7':('exercised','Role.receives declares inverse grantee while Actor.receives declares none. The instance populates both; the checker closes only the declared side, so AC-* receives lists were authored by hand and RO-* were closed mechanically. Asymmetric handling is visible in the artifact.','n/a','still-open',''),
 'S8':('not-applicable','superseded-marker hygiene across the five model files is a repository question about M01\'s siblings, not an instance question','n/a','not exercised by this case',''),
}
for k,(d,v,e,o,pk) in S.items(): rule(f"review-concern:{k}", d, v, e, o, pk)

rule('traversal:Goal->Workflow','exercised','checker output: GO-WFH -> [WF-RESEARCH-SCOPE]; GO-JURATI-SUBSTRATE -> [WF-RESEARCH-SCOPE]. Served by filtering Workflow.applies_to; no inverse relation added.','mechanically checkable and checked','the A3 withdrawal holds','')
rule('traversal:Actor->Attempt','exercised','checker output: 19 Actors resolve to their Attempts by filtering Attempt.actors; AC-RWK-P2A -> [AT-W1-3, AT-W2-3]; AC-CUR -> [AT-SYNTH-1, AT-CLOSE-1]. No inverse relation added and no global scan beyond the Attempt collection.','mechanically checkable and checked','the A3 withdrawal holds','')
rule('changelog:5.0.0','exercised','every 5.0.0 claim was consumed by the instance: invariants bound per construct (19/19 cited), extension_owner on exactly six constructs, form restored, assessment split from gate_outcome (EV-013/EV-014), Event.authority_ref pointing at SC-COL, Role.receives navigable, effect_disposition vocabulary used, scope_type seeds conforming, and the inverse rule in principles','n/a','n/a','')
rule('changelog:4.0.0','inspected-no-material-instance','the v4 convergence claims are lineage; the instance tests 5.0.0 as pinned','n/a','n/a','')

CUSTODY = {'Scope':'git (themes.md, SCOPE.md) + forge','Goal':'git (themes.md, SCOPE.md)','Capability':'none - no instance',
 'Actor':'self-asserted; git author/committer and one forge account','Unit':'git working tree + commits','Event':'forge comments, git commits, Unimatrix cycle',
 'Record':'git for file-backed, Unimatrix/forge for service-backed','Workflow':'git .claude/ - inside the governed repository','Skill':'git .claude/agents frontmatter',
 'Role':'git .claude/agents','Delegation':'git themes.md and .claude/agents; no runtime carrier','Gate':'git .claude/workflow - prose',
 'EffectBoundary':'MCP server outside the agent process','Attempt':'reconstructed from git and forge; no runtime record','Technology':'Unimatrix'}

# Explicit overrides: X items whose auto-derived disposition would hide an authored pressure.
OVERRIDE = {
 'core.Scope.fields.authority_root_ref': ('construct-pressure','set on 4/4 Scopes and identical on all four (AC-OWNER) because a nested Scope holds no undelegated authority','SC-COL,SC-PROG,SC-MIS,SC-TEAM','specified-not-enforced','pressure','PR-SCOPE-AUTHORITY-ROOT'),
 'core.Actor.fields.declared_identity': ('construct-pressure','set on 22/22 Actors and NON-DISCRIMINATING: 15 Actors share the value "factory-researcher" and 2 share "research-leader"; AC-OWNER has three identity strings across two stores and one field','AC-OWNER,AC-LEAD-1,AC-LEAD-2,AC-RES-W1,AC-AUD-R1,AC-RWK-P1','specified-not-enforced','pressure','PR-ACTOR-IDENTITY-SINGULAR'),
 'core.Actor.versioned': ('construct-pressure','Actor is versioned:false, so the original and replacement leaders cannot be one identity with two revisions; encoded as AC-LEAD-1 and AC-LEAD-2, a choice the model does not force either way','AC-LEAD-1,AC-LEAD-2','not-applicable','still-open','PR-ACTOR-CONTINUITY'),
 'supporting.Attempt.fields.resume_requirements': ('construct-pressure','populated in full on AT-RUN-2 - the strongest positive witness for the field - but authored by the RESUMING actor about the INTERRUPTED attempt, and the model does not say which Attempt owns it','AT-RUN-2','specified-not-enforced','pressure','PR-ATTEMPT-RESUME-OWNER'),
 'supporting.EffectBoundary.fields.can_refuse': ('construct-pressure','true on EB-UNIMATRIX with a real receipt (five refused context_cycle calls). Git and the forge are NOT instantiated as boundaries at all, because the required bool has no unknown value and neither true nor false is evidenced for them','EB-UNIMATRIX','specified-not-enforced','pressure','PR-BOUNDARY-CAN-REFUSE'),
 'supporting.Delegation.relations.grantor': ('construct-pressure','set on 31/31. DL-SCOPE has grantor == grantee (AC-LEAD-1 self-assigned the scope-authoring Unit and then requested its own gate); V5 neither forbids nor detects this','DL-SCOPE,DL-RUN-1,DL-W1','specified-not-enforced','pressure','PR-DELEGATION-SELF-GRANT'),
 'supporting.Delegation.relations.unit': ('construct-pressure','cardinality 0..1 forced three historical multi-Unit rework directives to be split into six Delegations; the fact that they were one directive is not expressible','DL-RWK-P1-W1,DL-RWK-P1-W2,DL-RWK-P1-W4,DL-RWK-P2A2,DL-RWK-P2D2','mechanically checkable and checked','pressure','PR-DELEGATION-UNIT-CARDINALITY'),
 'supporting.Gate.relations.requires_assessor': ('construct-pressure','set on 4/4 Gates, but GT-COVERAGE points at RO-COVERAGE-AUDITOR, a Role the project never defined - a duty handed to a factory-researcher, while the protocol reserves factory-validator for validated runs','GT-COVERAGE','specified-not-enforced','pressure','PR-ROLE-UNDEFINED-ASSESSOR'),
 'supporting.Gate.fields.procedure': ('blocked-by-OPEN','judgment on all four Gates; GT-COVERAGE is APPROXIMATED because it was both deterministic and judgment and the enum admits no mixed value','GT-COVERAGE','specified-not-enforced','blocked by Gate.open[deterministic versus judgment procedures]','PR-GATE-PROCEDURE'),
 'values.autonomy_tier.A4': ('construct-pressure','USED by DL-COORD-STANDING despite the value carrying status insufficient-evidence in the model; the case adds one instance and no evidence about the tier boundary','DL-COORD-STANDING','specified-not-enforced','open.autonomy_A3_A4 still-open','PR-DELEGATION-ATTENUATION-COMPARISON'),
 'values.autonomy_tier.A3': ('blocked-by-OPEN','NOT USED. No actor in wfh-008 held general local-adaptation latitude - every adaptation was gate-driven or owner-driven. status insufficient-evidence is unchanged by this case.','','not-applicable','open.autonomy_A3_A4 still-open, gains nothing','PR-DELEGATION-ATTENUATION-COMPARISON'),
 'core.Record.fields.content_digest': ('construct-pressure','real sha256 on 11 file-backed Records; SENTINEL on 11 service-backed Records because Unimatrix, the forge and the cycle service expose no content digest','RC-SCOPE,RC-W1,RC-UNI-316,RC-ISSUE-66,RC-CYCLE','specified-not-enforced','pressure','PR-RECORD-DIGEST'),
}

rows = []
def emit(xid, kind, disp, val, inst_ids, enf, opend, pk=''):
    if xid in OVERRIDE:
        disp, val, inst_ids, enf, opend, pk = OVERRIDE[xid]
    pr = PRESSURE.get(pk, NA) if pk else NA
    r = dict(x_id=xid, x_kind=kind, source_id='R01,R02,R03,R04,R05,R06,M01,M02,M06,T01,T02',
             model_path=xid, instance_id=inst_ids or 'none',
             instance_version=('1' if inst_ids else 'not-applicable'), value=val,
             provenance='wfh-008 alphabet R + M01 as parsed + T01/T02 (ledgered transitive)',
             custody=CUSTODY.get(kind.split(':')[0], 'not-applicable'),
             invariant_check_ids='see instance + wfh-008-validate.py output',
             enforcement_reality=enf, open_pressure_disposition=opend, disposition=disp,
             pressure_id=pk or 'not-applicable')
    r.update(pr); rows.append(r)

# --- construct fields and relations, derived from the instance ---
for sec in ('core','supporting'):
    for cname, spec in M[sec].items():
        insts = BY_C.get(cname, [])
        emit(f"{sec}.{cname}.versioned", cname, 'exercised',
             f"versioned={spec.get('versioned')}; the checker enforces presence/absence of a version on every instance",
             ','.join(r['id'] for r in insts[:3]), 'mechanically checkable and checked', 'n/a')
        emit(f"{sec}.{cname}.identity", cname, 'exercised' if insts else 'not-applicable',
             f"identity={spec.get('identity')}; opaque ids in the instance",
             ','.join(r['id'] for r in insts[:3]), 'specified-not-enforced', 'n/a')
        emit(f"{sec}.{cname}.form", cname, 'exercised' if insts else 'not-applicable',
             f"form={spec.get('form')}", ','.join(r['id'] for r in insts[:3]), 'not-applicable', 'S3: form is undocumented in notation')
        emit(f"{sec}.{cname}.status", cname, 'exercised' if insts else 'not-applicable',
             f"model status={spec.get('status')}; consumed as test input, not as permission to fill holes",
             '', 'not-applicable', 'n/a')
        if 'owner' in spec:
            emit(f"{sec}.{cname}.owner", cname, 'exercised' if insts else 'not-applicable',
                 f"owner={spec.get('owner')}", '', 'specified-not-enforced', 'S3: owner is undocumented in notation')
        emit(f"{sec}.{cname}.invariants", cname, 'exercised' if insts else 'not-applicable',
             f"cites {spec.get('invariants')}", '', 'see the invariant rows', 'n/a')
        for fname, fspec in (spec.get('fields') or {}).items():
            xid = f"{sec}.{cname}.fields.{fname}"
            if not insts:
                emit(xid, cname, 'not-applicable', f"no {cname} instance in this case", '', 'not-applicable',
                     'missing-history', 'PR-CAPABILITY-ABSENT' if cname == 'Capability' else '')
                continue
            hits = [r['id'] for r in insts if fname in (r.get('fields') or {})]
            appr = [r['id'] for r in insts if fname in (r.get('_approx') or {})]
            pk = ''
            for r in insts:
                if fname in (r.get('_approx') or {}): pk = r['_approx'][fname]; break
            if not hits:
                emit(xid, cname, 'not-applicable', 'optional field; the alphabet supplies no value', '', 'not-applicable', 'missing-history')
            elif appr:
                emit(xid, cname, 'construct-pressure', f"set on {len(hits)}/{len(insts)}; APPROXIMATED on {appr}",
                     ','.join(hits[:6]), 'specified-not-enforced', 'pressure', pk)
            else:
                emit(xid, cname, 'exercised', f"set on {len(hits)}/{len(insts)} instances",
                     ','.join(hits[:6]), 'specified-not-enforced', 'n/a')
        for rname, rspec in (spec.get('relations') or {}).items():
            xid = f"{sec}.{cname}.relations.{rname}"
            if not insts:
                emit(xid, cname, 'not-applicable', f"no {cname} instance", '', 'not-applicable', 'missing-history',
                     'PR-CAPABILITY-ABSENT' if cname == 'Capability' else '')
                continue
            hits = [r['id'] for r in insts if (r.get('relations') or {}).get(rname)]
            if hits:
                inv = 'declared inverse, closed mechanically' if isinstance(rspec, dict) and 'inverse' in rspec else 'one-way, served by index'
                emit(xid, cname, 'exercised', f"non-empty on {len(hits)}/{len(insts)}; {inv}", ','.join(hits[:6]),
                     'mechanically checkable and checked', 'n/a')
            else:
                pk = ''
                if cname == 'Delegation' and rname == 'enforced_by': pk = 'PR-ENFORCED-AUTHORITY-ABSENT'
                if cname == 'EffectBoundary' and rname == 'enforces': pk = 'PR-ENFORCED-AUTHORITY-ABSENT'
                if rname == 'replaces': pk = ''
                emit(xid, cname, 'construct-pressure' if pk else 'not-applicable',
                     'empty on every instance - no historical occurrence' if not pk else 'EMPTY ON EVERY INSTANCE - the case demonstrates no enforced authority',
                     '', 'specified-not-enforced', 'pressure' if pk else 'missing-history', pk)
        for eo, owner in (spec.get('extension_owner') or {}).items():
            emit(f"{sec}.{cname}.extension_owner.{eo}", cname, 'exercised',
                 f"owner={owner}; exercised by the program-owned registry extensions in this instance",
                 'registry_extensions', 'specified-not-enforced',
                 'S6: I19 binds from Workflow only', 'PR-I19-BINDING-ALTITUDE')
        for oi, o in enumerate(spec.get('open') or []):
            emit(f"{sec}.{cname}.open[{oi}]", cname, 'construct-pressure' if insts else 'not-applicable',
                 str(o), '', 'not-applicable', 'still-open' if insts else 'not-exercised',
                 'PR-CAPABILITY-ABSENT' if cname == 'Capability' else '')

# --- registries, seeds, catalogs, values ---
used_vals = set()
for c, r in OBJS:
    for v in (r.get('fields') or {}).values():
        if isinstance(v, str): used_vals.add(v)
        elif isinstance(v, list):
            used_vals |= {x for x in v if isinstance(x, str)}
ext = I.get('registry_extensions') or {}
for rn, rs in M['registries'].items():
    n_ext = len((ext.get(rn) or {}).get('entries') or {})
    emit(f"registries.{rn}", 'Registry', 'exercised',
         f"{len(rs.get('seeded') or {})} model seeds + {n_ext} program-owned extensions authored here",
         'registry_extensions', 'specified-not-enforced',
         'admission_rule applied and recorded' if n_ext else 'seeds only')
    emit(f"registries.{rn}.shape", 'Registry', 'exercised',
         'every authored extension conforms to the declared shape; the checker verifies it key by key',
         'registry_extensions', 'mechanically checkable and checked', 'n/a')
    emit(f"registries.{rn}.admission_rule", 'Registry',
         'exercised' if n_ext else 'not-applicable',
         'applied to each authored entry with a stated behavioral justification' if n_ext else 'no extension authored',
         'registry_extensions' if n_ext else '', 'specified-not-enforced', 'n/a')
    for sk in (rs.get('seeded') or {}):
        u = sk in used_vals
        pk = 'PR-CAPABILITY-CLASSIFICATION-UNUSED' if rn == 'capability_classification' else ''
        emit(f"registries.{rn}.seeded.{sk}", 'Registry', 'exercised' if u else 'not-applicable',
             'used by at least one instance' if u else 'no historical occurrence in this case',
             '', 'specified-not-enforced', 'n/a' if u else 'missing-history', pk)
    for ek in ((ext.get(rn) or {}).get('entries') or {}):
        emit(f"registries.{rn}.extension.{ek}", 'Registry', 'exercised',
             'program-owned extension authored and used by this instance', '', 'specified-not-enforced', 'n/a')
for cn, cs in M['catalogs'].items():
    emit(f"catalogs.{cn}", 'Catalog', 'exercised',
         f"construct={cs['construct']} scope={cs['scope']} status={cs['status']}; populated in the instance's catalogs block",
         'catalogs', 'specified-not-enforced', 'still-open',
         'PR-SKILL-EVIDENCE-ABSENT' if cn == 'skill' else ('PR-GATE-IDENTITY-VERSION' if cn == 'gate' else ''))
for vn, vs in M['values'].items():
    members = vs['values'] if isinstance(vs.get('values'), (list, dict)) else []
    emit(f"values.{vn}", 'Value', 'exercised', f"{len(members)} members; status={vs['status']}", '', 'specified-not-enforced', 'n/a')
    if 'rule' in vs:
        emit(f"values.{vn}.rule", 'Value', 'exercised', str(vs['rule']), '', 'specified-not-enforced', 'n/a',
             'PR-ENFORCED-AUTHORITY-ABSENT' if vn == 'effect_disposition' else '')
    for m in members:
        u = m in used_vals
        pk = ''
        if vn == 'autonomy_tier' and m in ('A3', 'A4'): pk = 'PR-DELEGATION-ATTENUATION-COMPARISON'
        if vn == 'evidence_grade' and m in ('partial', 'proven'): pk = 'PR-CAPABILITY-ABSENT'
        emit(f"values.{vn}.{m}", 'Value', 'exercised' if u else 'not-applicable',
             'used by at least one instance' if u else 'no historical occurrence in this directional case',
             '', 'specified-not-enforced', 'n/a' if u else 'missing-history', pk)

for xid, (d, v, e, o, pk) in R.items():
    kind = xid.split(':')[0].capitalize()
    emit(xid, kind, d, v, '', e, o, pk)

FIELDS = ['x_id','x_kind','disposition','pressure_id','source_id','model_path','instance_id','instance_version',
          'value','provenance','custody','invariant_check_ids','enforcement_reality','open_pressure_disposition'] + SUPER
with open(out_p, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction='ignore')
    w.writeheader()
    for r in rows: w.writerow(r)

c = collections.Counter(r['disposition'] for r in rows)
print(f"rows: {len(rows)}")
for k, v in c.most_common(): print(f"  {k}: {v}")
pc = collections.Counter()
for r in rows:
    if r['cause_classification'] != 'not-applicable':
        for t in r['cause_classification'].split(';'): pc[t.strip()] += 1
print("cause classifications (row-weighted):")
for k, v in pc.most_common(): print(f"  {k}: {v}")
print("distinct pressures used:", len({r['pressure_id'] for r in rows if r['pressure_id'] != 'not-applicable'}))
print("pressures declared but unused:",
      sorted(set(PRESSURE) - {r['pressure_id'] for r in rows}))
