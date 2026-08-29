#!/usr/bin/env python3
"""wfh-011 W2 — build artifacts/vnc-045-coverage.csv over the enumerated X alphabet.
Deterministic: re-enumerates X from the pinned M01, then joins an authored disposition table.
Every X row gets exactly one disposition. Failure/pressure rows carry the superseding fields.
"""
import csv, subprocess, sys, os

SCR = os.path.dirname(os.path.abspath(__file__))
X = [l.split('\t') for l in subprocess.run(
        [sys.executable, os.path.join(SCR, "vnc-045-coverage-enumerate-x.py")],
        capture_output=True, text=True, check=True).stdout.strip().split('\n')]

NA = "not-applicable"
COLS = ["x_class","model_path","disposition","instance_ref","value_or_witness","provenance","custody",
        "applicable_checks","enforcement_reality","open_pressure_disposition",
        "cause_classification","classification_evidence","current_project_fit","evolution_change",
        "independent_reason","semantic_proof_authority_custody_preservation","migration_cost",
        "affected_artifacts","current_form_representable","evolved_form_representable",
        "post_evolution_fit","unresolved_discriminator"]

def row(**kw):
    r = {c: NA for c in COLS}
    r.update(kw)
    return r

# ---------------------------------------------------------------- pressure builders
def P(cause, ev, fit="represented-with-gap", cf=NA, indep=NA, presv=NA, mig=NA, aff=NA,
      cur="true", evo=NA, post=NA, unres=NA):
    return dict(cause_classification=cause, classification_evidence=ev, current_project_fit=fit,
                evolution_change=cf, independent_reason=indep,
                semantic_proof_authority_custody_preservation=presv, migration_cost=mig,
                affected_artifacts=aff, current_form_representable=cur,
                evolved_form_representable=evo, post_evolution_fit=post,
                unresolved_discriminator=unres)

CF = {
 "CF-01": P("project-evolution-candidate",
   "RC-13/RC-20/RC-21/RC-23 describe the pre-reduction UN-01 and are committed unchanged in afaa8385 beside the reduced sources that contradict them; nothing distinguishes them.",
   "represented-with-gap",
   "[CF-01] Stamp agent/gate reports with the SCOPE digest they were written against; synthesizer stamps superseded_by when it regenerates after a scope change.",
   "The project already pays this cost by hand: RC-03 records that pattern #5607 cites a now-stale vnc-045 instance and hands the retro a manual reconciliation.",
   "Additive metadata only; no proof bar, gate outcome or authority moves; superseded reports stay on disk, as ADRs already do (RC-22).",
   "Low: two template lines plus one synthesizer step; no retro-stamping of history.",
   "uni-design-protocol Phase 2c; uni-delivery-protocol report conventions; agents/*.md and reports/gate-*.md templates",
   "true","true","retain",NA),
 "CF-02": P("project-evolution-candidate",
   "RC-09 flags as open a WARN already fixed by 843d0049 24 minutes earlier and pins no commit; AT-03's required baseline_ref does not survive (both GT-04 iterations collapse into 3afc2c49).",
   "represented-with-gap",
   "[CF-02] Add reviewed_commit: <sha> to the gate-report template, written by the validator from git rev-parse HEAD.",
   "T01 already declares 'Gates check committed HEAD' and makes the leader commit before the gate; a review that cannot name what it reviewed cannot be re-run.",
   "Purely additive provenance; bar, outcomes, consequences, assessor and independence predicate untouched.",
   "Low: one template line and one command per gate; does not recover AT-03's pre-commit baseline.",
   "uni-delivery-protocol Gate 3a/3b/3c spawn templates; gate-report templates",
   "partial","true","retain",NA),
 "CF-03": P("project-evolution-candidate|historical-evidence-gap",
   "EV-05 exists only as the dated phrase 'scope reduced by human 2026-07-07' inside seven documents written by the actors it governed; no forge object, no commit; occurred_at unavailable at the declared timestamp type.",
   "represented-with-gap",
   "[CF-03] Post one issue comment stating the scope decision, its rationale and its time, at the human gate, before regeneration.",
   "vnc-045's own thesis is that an append-only record is the primary control, applied to a single tag mutation at millisecond precision; the same organisation left its most consequential decision unrecorded.",
   "Custody strictly improves: the record moves from actor-authored paraphrase to forge-custodied primary source; no authority moves toward the governed activity.",
   "Very low: one comment per scope decision; does not retroactively supply EV-05.",
   "uni-design-protocol Phase 1 / Phase 2d human gates; uni-delivery-protocol merge gate",
   "partial","true","retain",NA),
 "CF-04": P("project-evolution-candidate|historical-evidence-gap",
   "RC-14 asserts 6961/0 and smoke 32/32 with no retained runner output; its own '12 -> 15 tools' claim is contradicted by the committed test_protocol.py diff (fourteen -> fifteen), as is the PR body's '13th tool'.",
   "represented-with-gap",
   "[CF-04] Retain the runner output (or its digest plus head/tail) beside RISK-COVERAGE-REPORT.md and cite it from the report's provenance line.",
   "The project treats a summary standing in for a record as a security defect for machine writes (R-03, the '{}' sentinel rule); the same standard on its own gate evidence would have caught a factual error that shipped.",
   "Nothing removed, no bar lowered; honest about what it buys - reproducibility, not attestation, since capture custody is still the reporting actor's shell.",
   "Low-moderate: repository growth per feature (mitigable by digest+truncation); one tester step; one template line.",
   "uni-delivery-protocol Stage 3c and Cargo Output Truncation; product/features/{id}/testing/",
   "true","true","retain",NA),
 "CF-05": P("enforcement-gap|project-evolution-candidate|historical-evidence-gap",
   "reports/gate-3c-report.md is absent at 37c7b09a while 153-of-226 sibling features at the same commit carry it; 'Gate 3c PASS' is claimed in the PR body and RC-10; the only Stage-3c record (RC-14) is authored by the tester under assessment.",
   "reject",
   "[CF-05] Require the gate-3c report as a forge-side branch-protection check on main (preferred), or a human pre-merge checklist item against the file.",
   "T01 already declares Gate 3c mandatory with an independent assessor and a fixed output path, and 153 of 226 feature directories produce it; the change makes an already-documented, already-normal behaviour non-bypassable.",
   "Authority moves AWAY from the governed actors to an externally custodied boundary; no bar, outcome or consequence changes; an absent report blocks rather than auto-passes. Recorded risk: a file-exists predicate raises the cost of an unrecorded gate, it does not attest the assessment happened.",
   "Moderate: repository-admin configuration plus a check script; changes the merge path for every feature; needs an exemption path for features with no Stage 3c.",
   "GitHub branch protection on dug-21/unimatrix:main; a CI check script; uni-delivery-protocol Gate 3c and Phase 4",
   "partial","true","retain",
   "Whether the Gate 3c assessment occurred and went uncommitted is unresolvable from the fixed alphabet; no project change settles it retrospectively."),
}

HG = lambda ev, cur="true": P("historical-evidence-gap", ev, "represented-with-gap", cur=cur)
EG = lambda ev: P("enforcement-gap", ev, "specified-not-enforced")
MD = lambda ev, unres=NA: P("model-defect", ev, "reject", unres=unres)

# ---------------------------------------------------------------- overrides
O = {}
def o(path, **kw): O[path] = kw

# ---- principles
o("principles.small_core", disposition="exercised", instance_ref="whole instance",
  value_or_witness="All seven core constructs carry at least one vnc-045 instance; no eighth common construct was needed to encode the case.",
  provenance="derived", applicable_checks="I13,I14", enforcement_reality="none - no checker")
o("principles.supporting_definitions", disposition="exercised", instance_ref="WF-01..GT-08,EB-01..03,AT-01..17,TE-01..03,SK-01..03,RO-01..13,DL-01..13",
  value_or_witness="All eight supporting definitions instantiated; none required redefining a core entity.", provenance="derived")
o("principles.extend_by_registration", disposition="construct-pressure", instance_ref="CP-02",
  value_or_witness="Held for unit_kind, record_category and effect_class (three empty registries populated as program extensions). FAILED for the grade vocabulary: the observed value 'asserted' has no registry and no extension_owner to enter through.",
  provenance="doc-claim", applicable_checks="I19",
  enforcement_reality="none", open_pressure_disposition="still-open",
  **MD("values.evidence_grade is RESOLVED and closed at [missing,claimed,partial,proven] with no registry, no extension_owner and no admission rule, while principles.program_ownership says programs own proof bars. The observed program's set is {proven,partial,missing,asserted} (SR-10) and it explicitly ruled 'claimed' a slip (S01 OQ-1)."))
o("principles.construct_admission_bar", disposition="exercised", instance_ref="advisory_reviews AR-01..03",
  value_or_witness="Applied as a negative test: the advisory product review was NOT admitted as a new construct; it fits communication Event + advisory-review Record.", provenance="derived")
o("principles.separation_is_the_product", disposition="exercised", instance_ref="EV-07..EV-30",
  value_or_witness="All six separations exercised. Sharpest: claim/observation (EV-26 reported vs EV-27 mechanical) and outcome/decision/consequence (AR-01..03 recommendations recorded, not adopted).", provenance="derived")
o("principles.authority_chain", disposition="construct-pressure", instance_ref="DL-01..DL-13",
  value_or_witness="Chain expressible (DL-06 -> DL-01 -> SC-01 in two hops) but wholly inferred; no artefact in the alphabet states a grant.",
  provenance="inference", custody="none", applicable_checks="I17",
  enforcement_reality="specified-not-enforced", **HG("No Delegation artefact exists; autonomy_tier, effect_grants and escalation_conditions are reconstructed from T01/T02 spawn templates and resource_ceiling has no source at all."))
o("principles.program_ownership", disposition="construct-pressure", instance_ref="registry_extensions",
  value_or_witness="Programs did own unit_kind/record_category/effect_class here. They do NOT own the grade vocabulary, which the case needs and V5 closes.",
  provenance="derived", **MD("Same evidence as principles.extend_by_registration."))
o("principles.method_custody", disposition="exercised", instance_ref="WF-01,WF-02",
  value_or_witness="DEMONSTRATED: PR #929 changed 57 files, none under .claude/. The governed activity did not edit its governing definition.",
  provenance="forge", custody="git/GitHub (EB-01)", applicable_checks="I18",
  enforcement_reality="none - conformance is observed, not enforced; no branch rule protects .claude/")
o("principles.inverse_relations", disposition="exercised", instance_ref="traversal_checks",
  value_or_witness="Both required one-way traversals resolved by index scan with no relation added.", provenance="derived")

# ---- notation
for k in ["status","identity","versioned","fields","relations","types"]:
    o(f"notation.{k}", disposition="exercised", instance_ref="whole instance",
      value_or_witness="Consumed while parsing M01 and encoding the case.", provenance="derived")
o("notation.types", disposition="construct-pressure", instance_ref="EB-01,CP-02,TE-01",
  value_or_witness="The declared type set is where three fields fail: bool (EffectBoundary.can_refuse), ref<value.evidence_grade> (CP-02, TE-01) and timestamp (EV-05.occurred_at) all have no admissible value from the alphabet.",
  provenance="derived", enforcement_reality="none",
  **P("model-defect|historical-evidence-gap",
      "M01 offers no 'unestablished' or 'unknown' member for a REQUIRED typed field, so an honest encoder must write a claim or leave the instance non-conforming. values.currentness has 'unknown' and effect_disposition has 'unknown'; the type system does not.",
      "represented-with-gap", cur="partial"))

# ---- Scope
o("core.Scope.fields.objective", disposition="exercised", instance_ref="SC-03",
  value_or_witness="'Ship the context_tag MECHANISM only; protected_tags deferred in full.'", provenance="repo-artifact")
o("core.Scope.fields.expires_at", disposition="exercised", instance_ref="SC-03",
  value_or_witness="2026-07-07T11:29:09Z (issue #928 closed, state_reason completed)", provenance="forge", custody="GitHub")
o("core.Scope.fields.effective_at", disposition="construct-pressure", instance_ref="SC-01,SC-02",
  value_or_witness="SC-03 = 2026-07-06T23:44:12Z (forge). SC-01 and SC-02 = missing-history: nothing in the alphabet dates the collective or the program.",
  provenance="forge/missing", **HG("The alphabet is vnc-045-scoped; no artefact dates the enclosing scopes."))
o("core.Scope.relations.contains", disposition="exercised", instance_ref="SC-01>SC-02>SC-03",
  value_or_witness="Three-level chain, acyclic within one baseline.", provenance="inference")
o("core.Scope.open[2]:authority-root succession", disposition="exercised", instance_ref="SC-01",
  value_or_witness="Exercised and unresolved: AC-01 is the sole authority root and the sole forge identity; no succession event, no second root.",
  open_pressure_disposition="still-open", provenance="forge")
o("core.Scope.open[3]:termination and transfer", disposition="exercised", instance_ref="SC-03",
  value_or_witness="SC-03 terminated at issue close with state_reason completed; no transfer observed. Termination is representable via expires_at.",
  open_pressure_disposition="still-open", provenance="forge")

# ---- Goal
o("core.Goal.fields.success_criteria", disposition="construct-pressure", instance_ref="GO-01,GO-02,GO-03",
  value_or_witness="missing-history on all three goals.", provenance="missing", custody="Unimatrix graph, outside the alphabet",
  applicable_checks="I13", enforcement_reality="none",
  **HG("Goal content lives in Unimatrix entries #5517/#5518/#5474 and product/PRODUCT-VISION.md; neither is in the fixed S alphabet. Not invented."))
o("core.Goal.fields.claim_floor", disposition="construct-pressure", instance_ref="GO-01,GO-02,GO-03",
  value_or_witness="missing-history. REQUIRED list<ref<Capability>>.", provenance="missing",
  **HG("Same as success_criteria. S01's uni-zero comments name capability ids (#5546, #5528) and quote two done_when clauses, but never the goals' claim floors."))
o("core.Goal.fields.north_star", disposition="exercised", instance_ref="GO-01",
  value_or_witness="Optional; absent. Recorded absent, not inferred.", provenance="missing")
o("core.Goal.relations.is_advanced_by", disposition="exercised", instance_ref="GO-01",
  value_or_witness="EMPTY BY OBSERVATION and this is the finding: both uni-zero reviews rule vnc-045 advances no capability toward completion.",
  provenance="doc-claim")
o("core.Goal.relations.directs", disposition="exercised", instance_ref="GO-01 -> UN-02",
  value_or_witness="Goal directs the Unit without becoming its Scope (SC-03 is).", provenance="derived")

# ---- Capability
o("core.Capability.fields.grade", disposition="construct-pressure", instance_ref="CP-02",
  value_or_witness="UNREPRESENTABLE. Observed value 'asserted'; M01's closed set is [missing,claimed,partial,proven].",
  provenance="doc-claim", applicable_checks="I9", enforcement_reality="none",
  open_pressure_disposition="model-pressure",
  **MD("SR-10 quotes uni-capability SKILL.md's set {proven,partial,missing,asserted}; S01 OQ-1 rules 'asserted' authoritative and 'claimed' a slip. Recording 'claimed' would be silent normalisation of the exact term the program rejected. See rejected counterfactual CF-R01 for why renaming the project is circular."))
o("core.Capability.fields.done_when", disposition="construct-pressure", instance_ref="CP-01,CP-02",
  value_or_witness="CP-01 partially recoverable from S01's quoted clauses; CP-02 missing-history.",
  provenance="doc-claim", **HG("done_when text lives in the Unimatrix nodes, outside the alphabet."))
o("core.Capability.fields.evidence_record_refs", disposition="construct-pressure", instance_ref="CP-01",
  value_or_witness="missing-history. uni-zero RECOMMENDS that KI-AUDIT's evidence set gain the context_tag row test; the recommendation is not an observed link and is not asserted here.",
  provenance="doc-claim", **HG("The Unimatrix node's proven_by set is outside the alphabet."))
o("core.Capability.relations.delivered_by", disposition="exercised", instance_ref="CP-01",
  value_or_witness="EMPTY, deliberately. 'delivery does not prove' is exactly the project's ruling: 'Do NOT mark any capability proven off vnc-045'.",
  provenance="doc-claim")
o("core.Capability.relations.composed_of", disposition=NA, instance_ref="",
  value_or_witness="no witness: the case exposes no capability composition; M01 open.capability_rollup is untouched by it.",
  open_pressure_disposition="not-exercised")
o("core.Capability.relations.prerequisite_of", disposition=NA, instance_ref="",
  value_or_witness="no witness in this case.", open_pressure_disposition="not-exercised")
o("core.Capability.open[0]:recursive evidence rollup", disposition=NA, instance_ref="",
  value_or_witness="no composed capability in the case.", open_pressure_disposition="not-exercised")
o("core.Capability.open[1]:parent-child done_when", disposition=NA, instance_ref="",
  value_or_witness="no capability hierarchy in the case.", open_pressure_disposition="not-exercised")
o("core.Capability.open[2]:Scope expiry", disposition="exercised", instance_ref="SC-03,CP-01",
  value_or_witness="SC-03 expired at issue close while CP-01 (scoped to SC-02) survives; the case shows mission expiry does not expire a program capability.",
  open_pressure_disposition="still-open", provenance="forge")

# ---- Actor
o("core.Actor.fields.declared_identity", disposition="exercised", instance_ref="AC-02..AC-16,AC-19",
  value_or_witness="STRONGEST FIELD-LEVEL WITNESS IN THE CASE. Every agent identity is a self-declared string in file content; the forge attests exactly one identity (dug-21/Doug) for author, committer, reviewer, merger and every comment. AC-19's Co-Authored-By trailer is the only agent identity inside a forge-held object and is still a self-declared trailer.",
  provenance="forge", custody="GitHub/git", applicable_checks="I12,I17",
  enforcement_reality="none - attribution is persisted self-assertion, exactly as the field's definition states")
o("core.Actor.fields.lifecycle_state", disposition="construct-pressure", instance_ref="AC-02..AC-16",
  value_or_witness="missing-history for every agent Actor. Agents are per-Attempt spawns; nothing records their existence outside the Attempt.",
  provenance="missing", **HG("No artefact records an agent's lifecycle; the agent-definition files under .claude/agents/uni/ describe roles, not actor instances."))
o("core.Actor.relations.has_skill", disposition="construct-pressure", instance_ref="SK-01,SK-02,SK-03",
  value_or_witness="Relation instantiable; ALL FOUR attributes (evidence_refs, grade, currentness, expires_at) are missing-history for every holder.",
  provenance="inference", applicable_checks="I10", enforcement_reality="none",
  **HG("Nothing in the alphabet records competence evidence, a competence grade, currentness or expiry for any actor."))
o("core.Actor.relations.receives", disposition="exercised", instance_ref="AC-02..AC-16",
  value_or_witness="Every agent Actor receives a dynamic Delegation; AC-01 receives none (authority root). Note S7: Actor.receives declares no inverse while Role.receives declares inverse: grantee.",
  provenance="inference", applicable_checks="I17,S7")
o("core.Actor.open[0]:identity attestation", disposition="exercised", instance_ref="AC-02..AC-19",
  value_or_witness="Exercised as a live, demonstrated gap, not a hypothetical.",
  open_pressure_disposition="still-open", provenance="forge",
  **EG("M01 I12 says only an EffectBoundary disposition demonstrates enforced authority; EB-01 authenticates one principal and enforces nothing about which agent produced a change. See rejected counterfactual CF-R02."))
o("core.Actor.open[1]:replacement and continuity", disposition=NA, instance_ref="",
  value_or_witness="no actor replacement observed.", open_pressure_disposition="not-exercised")
o("core.Actor.open[2]:composite Actors", disposition="construct-pressure", instance_ref="AC-19",
  value_or_witness="Every commit is authored by 'Doug' with a Co-Authored-By trailer for 'Claude Opus 4.8'. That is a composite actor in practice, and versioned:false Actor with a single declared_identity has no way to express it.",
  provenance="forge", open_pressure_disposition="still-open",
  **P("model-defect|historical-evidence-gap",
      "Commit 843d0049 (and every PR-head commit) carries a Co-Authored-By trailer; the instance must choose one Actor or invent a composite. Neither M01 Actor nor Attempt.actors distinguishes 'acted through' from 'acted as'.",
      "represented-with-gap", cur="partial"))

# ---- Unit
o("core.Unit.fields.intended_outcome", disposition="exercised", instance_ref="UN-01,UN-02",
  value_or_witness="The human scope reduction changes it, and M01's own definition ('changing it creates a new Unit') is what forces UN-01/UN-02 apart.",
  provenance="repo-artifact", applicable_checks="I16")
o("core.Unit.fields.current_state", disposition="exercised", instance_ref="UN-02..UN-08",
  value_or_witness="Workflow-owned; drawn from WF-02's state vocabulary (T01 context_cycle phases).", provenance="repo-artifact")
o("core.Unit.fields.baseline_ref", disposition="construct-pressure", instance_ref="UN-01",
  value_or_witness="UN-02..UN-08 carry commit shas. UN-01's is missing-history: the pre-reduction unit produced only untracked artefacts.",
  provenance="missing", **HG("T02: design artefacts stay untracked until the delivery session commits them, so the pre-reduction baseline was never written to git."))
o("core.Unit.relations.replaces", disposition="exercised", instance_ref="UN-02 replaces UN-01",
  value_or_witness="MODEL WIN. The relation and I16 represent the human scope reduction precisely; the project reused one identifier (vnc-045, #928, feature/vnc-045) and overwrote SCOPE/BRIEF/ACCEPTANCE-MAP in place.",
  provenance="repo-artifact", applicable_checks="I16", enforcement_reality="none")
o("core.Unit.relations.consumes", disposition="exercised", instance_ref="UN-02 consumes RC-01",
  value_or_witness="Admission and currentness stay explicit: RC-01's currentness is current, RC-13/RC-20/RC-21/RC-23 are superseded.", provenance="derived")
o("core.Unit.relations.produces", disposition="exercised", instance_ref="UN-02",
  value_or_witness="Production implies neither admission nor truth - RC-14 is produced and never admitted by any gate (see GT-06).", provenance="derived")
o("core.Unit.relations.gated_by", disposition="exercised", instance_ref="UN-03,UN-04,UN-05",
  value_or_witness="Qualified inverse of Gate.evaluates, applied only to the Unit subset. Exercised; see S2 on the dotted form.",
  provenance="derived", applicable_checks="S2")
o("core.Unit.relations.delivers", disposition="exercised", instance_ref="UN-02",
  value_or_witness="EMPTY BY OBSERVATION - the project explicitly rules that vnc-045 delivers no capability.", provenance="doc-claim")
o("core.Unit.relations.assigned_through", disposition="construct-pressure", instance_ref="UN-02..UN-08",
  value_or_witness="missing-history: no Delegation artefact exists to assign through.", provenance="missing",
  **HG("Same as principles.authority_chain."))
o("core.Unit.open[0]:interruption and resume", disposition="exercised", instance_ref="AT-03,AT-04",
  value_or_witness="GT-04 REWORKABLE FAIL -> rework -> re-check is an interruption and resume, expressible via Attempt.disposition=rework plus resume_requirements.",
  open_pressure_disposition="resolved-by-instance-at-document-altitude", provenance="doc-claim")
o("core.Unit.open[1]:concurrent Attempts", disposition="exercised", instance_ref="AT-06,AT-07,AT-08",
  value_or_witness="Waves are sequential by design (T01: 'components in later waves depend on earlier waves being committed'); AT-06/07/08 are consecutive, not concurrent. Within a wave, parallel component agents would be concurrent Attempts on DIFFERENT Units, so the OPEN is untouched.",
  open_pressure_disposition="not-exercised")
o("core.Unit.open[2]:partial-output admission", disposition="exercised", instance_ref="RC-14,GT-06",
  value_or_witness="RC-14 is a partial output (unit-seam-only R-03 proof, self-declared gap) that was never admitted by a gate and was nonetheless treated as a passed gate.",
  open_pressure_disposition="still-open", provenance="forge", **EG("No admission event exists for RC-14; see GT-06."))
o("core.Unit.fields.unit_kind", disposition="exercised", instance_ref="feature,stage,implementation-wave",
  value_or_witness="Three program-registered kinds; M01's own admission_rule anticipated 'software Feature belongs here'.", provenance="derived")

o("core.Unit.identity", disposition="construct-pressure", instance_ref="UN-01,UN-02",
  value_or_witness="Opaque unit_id works, but Unit has NO name and no external-reference field. The project's own work identifier (vnc-045), its tracking artefact (issue #928) and its branch (feature/vnc-045) have nowhere typed to live: Scope, Capability, Workflow, Skill, Role, Gate, EffectBoundary and Technology all carry `name`; Unit does not. The only homes are free-text intended_outcome or baseline_ref.",
  provenance="derived", applicable_checks="I1,I19", enforcement_reality="none",
  **P("model-defect",
      "Encoding UN-02 required putting 'vnc-045 / #928 / feature/vnc-045' into baseline_ref prose. M01 I19 forbids moving common semantics into free text, and 'which Unit is issue #928?' is the first question an auditor asks. Minor in severity, concrete in effect.",
      "represented-with-gap", cur="partial"))

# ---- Event
o("core.Event.identity", disposition="exercised", instance_ref="EV-05,EV-21",
  value_or_witness="Threshold exercised in both directions: EV-21 (merge disposition) is consequential and durably identified by the forge; EV-05 (the scope decision) is consequential and has NO durable identity anywhere.",
  provenance="forge", open_pressure_disposition="still-open")
o("core.Event.fields.occurred_at", disposition="construct-pressure", instance_ref="EV-05",
  value_or_witness="REQUIRED timestamp with no admissible value for the case's most consequential event; only a two-hour window is inferable, and that is an inference.",
  provenance="missing", custody="none", **CF["CF-03"])
o("core.Event.fields.recorded_at", disposition="exercised", instance_ref="EV-06",
  value_or_witness="occurred_at vs recorded_at genuinely diverge here: EV-06's adaptation was recorded at commit afaa8385 (02:50:37Z) long after it occurred.", provenance="forge")
o("core.Event.fields.authority_ref", disposition="exercised", instance_ref="EV-20,EV-29,EV-05",
  value_or_witness="ref<Delegation|Scope> is load-bearing: the merge and the scope reduction are the authority root acting, so authority_ref = SC-03 with no Delegation interposed. The M02 R4 correction is what makes these rows expressible without bypassing the root.",
  provenance="forge", applicable_checks="I17,R4")
o("core.Event.fields.epistemic_kind", disposition="exercised", instance_ref="EV-26,EV-27",
  value_or_witness="The case's sharpest pair: EV-26 (test results, reported-observation, no capture custody) against EV-27 (forge merge state, mechanical-observation, GitHub custody).",
  provenance="derived", applicable_checks="I4")
o("core.Event.fields.custody", disposition="exercised", instance_ref="EV-05,EV-21,EV-30",
  value_or_witness="Three custody values in one case: external forge (EV-21), git (EV-06), and none at all (EV-05, EV-30).", provenance="derived")
o("core.Event.fields.significance", disposition="exercised", instance_ref="EV-05,EV-10",
  value_or_witness="surprise used for EV-05 and EV-10 (the REWORKABLE FAIL); exception for gate assessments and effects; routine otherwise.", provenance="derived")
o("core.Event.fields.carrier", disposition="exercised", instance_ref="EV-05,EV-08,EV-21",
  value_or_witness="inline (EV-05, no record), record-ref (EV-08 -> RC-08), artifact-ref (EV-21 -> merge commit).", provenance="derived")
o("core.Event.fields.extension", disposition="exercised", instance_ref="EV-07..EV-30",
  value_or_witness="Every event type's required_extension attempted; assessment.independence_check and gate_outcome.missingness are missing-history throughout.",
  provenance="derived", **HG("No gate report in the case states an independence check or a missingness policy outcome."))
o("core.Event.relations.supersedes", disposition="exercised", instance_ref="EV-09/EV-10 -> EV-07/EV-08",
  value_or_witness="The GT-04 rework is a correction-by-new-event, not an edit: EV-09/EV-10 (iteration 0) are separate immutable events from EV-07/EV-08 (iteration 1).", provenance="doc-claim")
o("core.Event.relations.caused_by", disposition="exercised", instance_ref="EV-21 caused_by EV-20; EV-23 caused_by EV-21",
  value_or_witness="Demonstrated causal chain: request -> merge disposition -> issue-close disposition.", provenance="forge")
o("core.Event.relations.correlated_with", disposition=NA, instance_ref="",
  value_or_witness="no witness: the case supplies no pair that is correlated without being causally linked.", open_pressure_disposition="not-exercised")
o("core.Event.open[0]:durable identity threshold", disposition="exercised", instance_ref="EV-05",
  value_or_witness="Exercised adversely: a consequential decision with no durable identity is exactly the case M01's threshold is meant to catch, and M01 gives no rule that would have required one.",
  open_pressure_disposition="still-open", **EG("No mechanism assigns event identity in the observed project outside the forge."))
o("core.Event.open[1]:admission", disposition="exercised", instance_ref="RC-14",
  value_or_witness="Record.admitted_by is empty for RC-14 and for every agent-report Record.", open_pressure_disposition="still-open")
o("core.Event.open[2]:retention", disposition=NA, instance_ref="", value_or_witness="no retention policy or expiry observed.", open_pressure_disposition="not-exercised")
o("core.Event.open[3]:ordering and clock semantics", disposition="exercised", instance_ref="EV-21,EV-23,GT-05",
  value_or_witness="Exercised twice and it matters both times: the 2-second merge/issue-close lag establishes ordered-best-effort coupling, and the 843d0049-vs-RC-09 ordering is what makes GT-05's assessment unverifiable.",
  provenance="forge", open_pressure_disposition="still-open")

# ---- Record
o("core.Record.fields.category_schema_version", disposition="construct-pressure", instance_ref="RC-01..RC-24",
  value_or_witness="missing-history on every non-forge Record; only RC-25/RC-26 have one ('GitHub REST v3').",
  provenance="missing", **HG("The project has no schema-version concept for its document categories. No independently-justified bounded change was identified, so no evolution candidate is asserted here."))
o("core.Record.fields.currentness", disposition="exercised", instance_ref="RC-13,RC-20,RC-21,RC-23,RC-09",
  value_or_witness="MODEL WIN. Four superseded and one stale Record are expressible with cited evidence; the project marks supersession in-band only on ADRs (RC-22).",
  provenance="repo-artifact", enforcement_reality="none", **CF["CF-01"])
o("core.Record.fields.epistemic_kind", disposition="exercised", instance_ref="RC-14,RC-25,RC-11",
  value_or_witness="reported-observation (RC-14), mechanical-observation (RC-25/26), inference (RC-11/12/19), reviewed-finding (RC-08/09/10), claim (RC-01, agent reports). All five members witnessed.",
  provenance="derived", applicable_checks="I4")
o("core.Record.fields.evidence_altitude", disposition="exercised", instance_ref="RC-14,RC-26",
  value_or_witness="behavioral for forge records and the test-observation report; directional for every design and review record.", provenance="derived")
o("core.Record.fields.missing_or_unavailable_refs", disposition="exercised", instance_ref="RC-14,RC-01,RC-09",
  value_or_witness="Carries the three unretained runner outputs (RC-14), the two absent research FINDINGS (RC-01), and the unretained cargo output (RC-09). This optional field is what keeps I8 honest in the instance.",
  provenance="derived", applicable_checks="I8", **CF["CF-04"])
o("core.Record.fields.content_digest", disposition="exercised", instance_ref="RC-01..RC-27",
  value_or_witness="Every repo-artifact Record is digestible as a git blob at 37c7b09a; forge records digest to the pinned JSON dumps.", provenance="forge")
o("core.Record.fields.author_or_source_ref", disposition="construct-pressure", instance_ref="RC-11,RC-12,RC-19",
  value_or_witness="Two-valued for every advisory review: 'AC-16 (declared) / dug-21 (forge-attributed)'. The field is a single text, so one of the two must be dropped or the split hidden in prose.",
  provenance="forge", **P("model-defect",
     "GitHub attributes comments 4898695344 / 4899256125 / 4900099734 to dug-21 while their bodies declare uni-zero-reviewer. M01 offers one text field and no attested/declared distinction, though Actor.declared_identity draws exactly that line one construct away.",
     "represented-with-gap", cur="partial"))
o("core.Record.relations.admitted_by", disposition="exercised", instance_ref="RC-04,RC-14",
  value_or_witness="RC-04/RC-05 admitted by EV-08 (Gate 3a outcome). RC-14 admitted by NOTHING - and 'existence is not admission' is precisely the rule the 'Gate 3c PASS' claim breaks.",
  provenance="forge", applicable_checks="I2,I8", **CF["CF-05"])
o("core.Record.relations.supersedes", disposition="exercised", instance_ref="RC-03 supersedes RC-13",
  value_or_witness="Correction never overwrites history - except that the project DID overwrite SCOPE.md in place, so RC-01 has no predecessor to point at.",
  provenance="repo-artifact", **CF["CF-01"])
o("core.Record.open[0]:Category configuration", disposition="exercised", instance_ref="registry_extensions.record_category",
  value_or_witness="Seven categories registered by behaviour, not label; agent-report and test-observation-report each earn existence on distinct lifecycle/epistemic behaviour.",
  open_pressure_disposition="still-open")
o("core.Record.open[1]:admission rules", disposition="exercised", instance_ref="RC-14",
  value_or_witness="Two of seven categories have NO admission rule at all in the observed project (agent-report, advisory-review).",
  open_pressure_disposition="still-open", **EG("Nothing admits an agent report; it is written and committed."))
o("core.Record.open[2]:lesson-learned versus pattern boundary", disposition=NA, instance_ref="",
  value_or_witness="not-applicable to this case: the software case produces patterns (#5612, #5613) and no lesson-learned; the alphabet contains neither node's content, so no behavioural distinction is observable. This OPEN belongs to W1's research case.",
  open_pressure_disposition="not-exercised")

# ---- Workflow
o("supporting.Workflow.fields.state_vocabulary", disposition="exercised", instance_ref="WF-02",
  value_or_witness="[spec, spec-review, develop, test, pr-review] from T01's context_cycle phase-end calls.",
  provenance="repo-artifact (T01, transitive source)")
o("supporting.Workflow.fields.definition_custodian_ref", disposition="exercised", instance_ref="WF-01,WF-02",
  value_or_witness="AC-01. DEMONSTRATED by the 57-file PR touching nothing under .claude/.", provenance="forge", applicable_checks="I18")
o("supporting.Workflow.relations.applies_to", disposition="exercised", instance_ref="WF-01,WF-02 -> GO-01",
  value_or_witness="One-way by the M02 section-7 ruling; the Goal->Workflow traversal is an index scan and is demonstrated.", provenance="derived")
o("supporting.Workflow.relations.supersedes", disposition=NA, instance_ref="",
  value_or_witness="no workflow version change observed; T01/T02 carry no version identifier at all.", open_pressure_disposition="not-exercised")
o("supporting.Workflow.relations.requires", disposition="construct-pressure", instance_ref="WF-02",
  value_or_witness="missing-history: T01 selects dev agents by target language, never by a named Skill.", provenance="missing",
  **HG("No skill requirement is stated by either protocol."))
o("supporting.Workflow.open[0]:method admission and improvement evidence", disposition="exercised", instance_ref="WF-02",
  value_or_witness="Exercised adversely: T01/T02 are unversioned living files, so no assessment can pin a gate_version_ref and no method change is an adaptation Event.",
  open_pressure_disposition="still-open", **EG("The protocol has no version identifier and no admission record."))
o("supporting.Workflow.open[1]:cross-program reuse", disposition="exercised", instance_ref="WF-02",
  value_or_witness="Observable but outside the alphabet: .claude/protocols/ carries both uni-* and ndp-* protocol families, i.e. the same shape reused across programs. Not asserted from the fixed alphabet.",
  open_pressure_disposition="still-open")
o("supporting.Workflow.status", disposition="exercised", instance_ref="WF-01,WF-02",
  value_or_witness="M01 open.workflow_promotion is exercised affirmatively: the case is unencodable without Workflow. Stages, waves, gates, rework limits and state transitions all hang off it.",
  provenance="repo-artifact", open_pressure_disposition="resolved-by-instance")

# ---- Skill / Role
o("supporting.Skill.relations.held_by", disposition="construct-pressure", instance_ref="SK-01,SK-02,SK-03",
  value_or_witness="Relation instantiable; every one of the four attributes is missing-history.", provenance="missing",
  applicable_checks="I10,A1", **HG("No competence evidence, grade, currentness or expiry is recorded for any actor anywhere in the alphabet."))
o("supporting.Skill.fields.local_binding", disposition=NA, instance_ref="", value_or_witness="no repository-local skill binding observed.", open_pressure_disposition="not-exercised")
o("supporting.Skill.fields.definition_record_ref", disposition=NA, instance_ref="", value_or_witness="no skill definition record exists.", open_pressure_disposition="not-exercised")
o("supporting.Skill.open[0]:shared catalog", disposition=NA, instance_ref="",
  value_or_witness="no shared skill catalogue in the alphabet.", open_pressure_disposition="not-exercised")
o("supporting.Skill.open[1]:repository-local binding", disposition=NA, instance_ref="", value_or_witness="not observed.", open_pressure_disposition="not-exercised")
o("supporting.Skill.open[2]:admission and evidence", disposition="exercised", instance_ref="SK-02",
  value_or_witness="Exercised as a gap: an agent is assigned a Rust implementation Unit with no admission of competence and no evidence.",
  open_pressure_disposition="still-open", **EG("Dev-agent selection is by target language (T01), not by evidenced competence."))
o("supporting.Role.fields.independence_constraints", disposition="exercised", instance_ref="RO-09,RO-10,RO-13",
  value_or_witness="Populated from T01/T02 spawn rules ('fresh-context', 'the spawn prompt carries ONLY agent id, gate, ids and artifact paths'). DECLARED, never attested - the forge records one identity for assessor and assessee.",
  provenance="repo-artifact", applicable_checks="I7", enforcement_reality="specified-not-enforced",
  **P("enforcement-gap|historical-evidence-gap",
      "T01/T02 state the independence predicate; nothing verifies it, and the alphabet cannot establish whether a given review was independent. RO-09's Gate 3c instance is the case where it demonstrably was not recorded at all (GT-06).",
      "specified-not-enforced", cur="true"))
o("supporting.Role.relations.receives", disposition="exercised", instance_ref="RO-01,RO-13",
  value_or_witness="Standing delegations only: DL-01 to RO-01 and DL-13 to RO-13, both with unit absent. Satisfies S5's 'grantee = Role <=> unit absent' reading.",
  provenance="inference", applicable_checks="S5,S7")
o("supporting.Role.open[1]:incompatible-role enforcement", disposition="exercised", instance_ref="RO-08,RO-09",
  value_or_witness="Exercised adversely at GT-06: the tester's own report is the only Stage-3c record, so the tester and assessor roles were not separated in the record.",
  open_pressure_disposition="still-open", **CF["CF-05"])
o("supporting.Role.open[0]:composition", disposition=NA, instance_ref="", value_or_witness="no role composition observed.", open_pressure_disposition="not-exercised")
o("supporting.Role.open[2]:program-local versus collective", disposition=NA, instance_ref="",
  value_or_witness="every role in the case is program-local; no collective role observed.", open_pressure_disposition="not-exercised")

# ---- Delegation
for f in ["autonomy_tier","effect_grants","escalation_conditions","definition_custodian_ref","effective_at"]:
    o(f"supporting.Delegation.fields.{f}", disposition="construct-pressure", instance_ref="DL-01..DL-13",
      value_or_witness=f"Inferred from T01/T02 spawn templates; no artefact states a grant.", provenance="inference",
      applicable_checks="I17,I18", enforcement_reality="specified-not-enforced",
      **HG("The fixed alphabet contains no Delegation artefact. Values are reconstructions, marked as such on every row of the instance."))
o("supporting.Delegation.fields.resource_ceiling", disposition="construct-pressure", instance_ref="DL-01..DL-13",
  value_or_witness="unestablished on EVERY row. REQUIRED map with no source at all - not even an inferable one.",
  provenance="missing", enforcement_reality="specified-not-enforced",
  **HG("No budget, token, time or call ceiling is stated anywhere in the alphabet for any agent."))
o("supporting.Delegation.relations.derived_from", disposition="construct-pressure", instance_ref="DL-02..DL-13",
  value_or_witness="Chain expressible; attenuation holds on the initiative axis (A0/A1 < A5) and FAILS on the effect axis - every agent runs under the same OS/git/gh credentials as AC-01, so no derived grant is actually narrower.",
  provenance="inference", applicable_checks="I17", enforcement_reality="specified-not-enforced",
  **EG("M01 I17 says a derived Delegation may not exceed its parent. In this case it demonstrably does on the effect axis, and nothing detects it. This is an enforcement gap in the project, not a model defect: V5 names the property that is violated."))
o("supporting.Delegation.relations.enforced_by", disposition="exercised", instance_ref="DL-01..DL-13",
  value_or_witness="EMPTY on every dynamic Delegation. M01's own rule - 'without a boundary authority is declared only' - is the correct verdict for this case and V5 states it in typed structure.",
  provenance="derived", applicable_checks="I12", enforcement_reality="specified-not-enforced")
o("supporting.Delegation.open[0]:attenuation comparison", disposition="exercised", instance_ref="DL-02",
  value_or_witness="Exercised and unresolved: comparing A1 to A5 is orderable, comparing effect_grants across two agents holding identical credentials is not.",
  open_pressure_disposition="still-open")
o("supporting.Delegation.open[1]:revocation propagation", disposition=NA, instance_ref="", value_or_witness="no revocation observed.", open_pressure_disposition="not-exercised")
o("supporting.Delegation.open[2]:sub-delegation depth", disposition="exercised", instance_ref="DL-01>DL-04",
  value_or_witness="Depth 2 observed (root -> agent). No deeper chain in this case.", open_pressure_disposition="still-open")

# ---- Gate
o("supporting.Gate.fields.independence_predicate", disposition="construct-pressure", instance_ref="GT-04,GT-05,GT-06,GT-07",
  value_or_witness="Statable from T01/T02 for GT-04/05/06/07; missing-history for GT-08; and the assessment Events' independence_check is missing-history throughout.",
  provenance="repo-artifact", applicable_checks="I7", enforcement_reality="specified-not-enforced", **CF["CF-05"])
o("supporting.Gate.fields.baseline_rule", disposition="construct-pressure", instance_ref="GT-04,GT-05",
  value_or_witness="Statable ('committed HEAD') and unsatisfiable at GT-04 iteration 0 (nothing was committed) and unverifiable at GT-05 (no sha pinned; the WARN is already stale).",
  provenance="repo-artifact", **CF["CF-02"])
o("supporting.Gate.fields.missingness_policy", disposition="construct-pressure", instance_ref="GT-04..GT-08",
  value_or_witness="missing-history on every gate.", provenance="missing",
  **HG("Neither protocol states what a gate does when required evidence is absent; GT-06 is the case where it mattered."))
o("supporting.Gate.fields.procedure", disposition="exercised", instance_ref="GT-04..GT-08",
  value_or_witness="All five gates are judgment. NO deterministic gate exists in this case - notable for a software delivery with 6961 automated tests, because the test suite is an INPUT to a judgment gate, never a gate itself.",
  provenance="repo-artifact", open_pressure_disposition="still-open")
o("supporting.Gate.fields.allowed_outcomes", disposition="exercised", instance_ref="GT-04",
  value_or_witness="[PASS, REWORKABLE FAIL, SCOPE FAIL] verbatim from T01; GT-07 uses [READY, BLOCKED]; GT-08 uses [PASS, WARN, VARIANCE, FAIL]. Three distinct workflow-owned vocabularies in one case.",
  provenance="repo-artifact")
o("supporting.Gate.fields.outcome_consequences", disposition="exercised", instance_ref="GT-04",
  value_or_witness="Each outcome carries a real consequence in T01 (phase-end + commit + proceed / loop back max 2 / stop). Contrast advisory_reviews, which carry none and are therefore NOT modelled as Gates.",
  provenance="repo-artifact", applicable_checks="I6")
o("supporting.Gate.relations.evaluates", disposition="exercised", instance_ref="GT-04..GT-08",
  value_or_witness="Unit targets (GT-04/05/06) and Unit-as-whole-feature targets (GT-07/08). No Record, Capability or Event target in this case.",
  provenance="derived", applicable_checks="S2")
o("supporting.Gate.open[0]:deterministic versus judgment procedures", disposition="exercised", instance_ref="GT-04..GT-08",
  value_or_witness="Exercised: five gates, all judgment, all with deterministic evidence underneath. The OPEN is real and the case leans entirely to one side.",
  open_pressure_disposition="still-open")
o("supporting.Gate.open[1]:portability", disposition=NA, instance_ref="", value_or_witness="single-program case.", open_pressure_disposition="not-exercised")
o("supporting.Gate.open[2]:external enforcement", disposition="exercised", instance_ref="GT-06",
  value_or_witness="Exercised adversely and decisively: no external enforcement exists, and GT-06 is the gate that was claimed passed with no assessment record while 153 of 226 feature directories carry one.",
  open_pressure_disposition="blocking-hole", **CF["CF-05"])

# ---- EffectBoundary
o("supporting.EffectBoundary.fields.can_refuse", disposition="construct-pressure", instance_ref="EB-01",
  value_or_witness="unestablished. REQUIRED bool; no refusal receipt exists and branch-protection state is outside the alphabet. Its own definition ('a boundary that cannot refuse enforces nothing') makes it load-bearing.",
  provenance="missing", applicable_checks="I12", enforcement_reality="none",
  **P("historical-evidence-gap|model-defect",
      "Every requested effect in the case was performed; no refusal occurred and none is evidenced. M01 provides no unknown/unestablished member for a required bool, so an honest encoder must either assert a claim or leave the instance non-conforming. Compare values.effect_disposition, which DOES carry 'unknown'.",
      "represented-with-gap", cur="partial"))
o("supporting.EffectBoundary.fields.custody", disposition="exercised", instance_ref="EB-01,EB-02",
  value_or_witness="EB-01 is externally custodied (GitHub, Inc.). EB-02 fails the 'independently controlled' test: the Capability::Write gate is code AC-07/08/09 wrote during the same Attempts it would govern.",
  provenance="forge", applicable_checks="I12")
o("supporting.EffectBoundary.relations.enforces", disposition="exercised", instance_ref="EB-01",
  value_or_witness="EMPTY. The case's central custody result: no Delegation is enforced by any boundary. GitHub authenticates one principal and enforces nothing about which agent, under which grant, produced a change.",
  provenance="forge", applicable_checks="I12", enforcement_reality="specified-not-enforced")
o("supporting.EffectBoundary.open[0]:refusal evidence", disposition="exercised", instance_ref="EB-01,EB-03",
  value_or_witness="Exercised as an absence. The only refusal-shaped event described anywhere is a trigger-injected INSERT abort inside a test fixture, evidenced only by an authored report - NOT counted as a disposition witness.",
  open_pressure_disposition="still-open", provenance="doc-claim")
o("supporting.EffectBoundary.open[1]:attestation", disposition="exercised", instance_ref="EB-01",
  value_or_witness="Exercised as a live gap; the merge receipt attests the forge's action and one human principal, nothing about the agents.",
  open_pressure_disposition="still-open")
o("supporting.EffectBoundary.open[2]:common effect taxonomy", disposition="exercised", instance_ref="registry_extensions.effect_class",
  value_or_witness="Four effect classes registered from an empty seed. Nothing suggests they are common rather than program-local; the OPEN is untouched.",
  open_pressure_disposition="still-open")

# ---- Attempt
o("supporting.Attempt.fields.baseline_ref", disposition="construct-pressure", instance_ref="AT-03",
  value_or_witness="Supplied for AT-05..AT-09 and AT-12 (commit shas); missing-history for AT-03 (the failing Stage-3a attempt) and for every doc-claim-only attempt.",
  provenance="missing", **CF["CF-02"])
o("supporting.Attempt.fields.disposition", disposition="exercised", instance_ref="AT-01,AT-03,AT-02",
  value_or_witness="Three of five members witnessed: cancel (AT-01, terminated by the scope reduction), rework (AT-03, GT-04 iteration 0), complete (most). continue and hold have no witness.",
  provenance="doc-claim", applicable_checks="I15")
o("supporting.Attempt.fields.resume_requirements", disposition="exercised", instance_ref="AT-03",
  value_or_witness="MODEL WIN, and the field's full four-clause definition is what carries it: baseline, preconditions ('read reports/gate-3a-report.md first'), unresolved residue (Check 4 interface consistency) and next admissible transition (re-spawn, max 2 iterations) are all separately supplied by the history.",
  provenance="doc-claim")
o("supporting.Attempt.relations.governed_by", disposition="construct-pressure", instance_ref="AT-01..AT-17",
  value_or_witness="Instantiable; the rule 'pins immutable versions' is unsatisfiable - nothing in the alphabet pins a Delegation version to any Attempt.",
  provenance="inference", enforcement_reality="specified-not-enforced", **HG("No Delegation artefact and no version identifier exists."))
o("supporting.Attempt.relations.actors", disposition="construct-pressure", instance_ref="AT-05,AT-08",
  value_or_witness="Instantiable from report prose; the effect receipts name only 'Doug' plus a Co-Authored-By trailer, so the actor set is a doc-claim over a forge record that contradicts its granularity.",
  provenance="doc-claim", **HG("Per-commit custody attributes every commit to one human; agent participation is asserted in file content only."))
o("supporting.Attempt.status", disposition="exercised", instance_ref="AT-03,AT-04",
  value_or_witness="RESOLVED and it holds: Attempt is not a Unit subtype, and the baseline discriminator correctly places AC-08's self-corrected first-run test failure INSIDE AT-07 rather than creating a new Attempt.",
  provenance="doc-claim", applicable_checks="I15")

# ---- Technology
o("supporting.Technology.fields.grade", disposition="construct-pressure", instance_ref="TE-01,TE-02,TE-03",
  value_or_witness="unestablished on all three. REQUIRED. No grade is asserted for any mechanism in the alphabet, and the case's own reviews forbid inferring one from delivery.",
  provenance="missing", applicable_checks="I11", **HG("Not invented; inferring a grade from a merged delivery is exactly what I11 and the project's own ruling forbid."))
o("supporting.Technology.relations.enables", disposition="exercised", instance_ref="TE-01 -> CP-01",
  value_or_witness="'no grade transfer' is the project's own explicit, twice-stated, pre-registered ruling: 'Do NOT mark any capability proven off vnc-045'. STRONGEST CONFORMING WITNESS IN THE CASE.",
  provenance="doc-claim", applicable_checks="I11")
o("supporting.Technology.open[0]:adopted component versus conceptual mechanism", disposition="exercised", instance_ref="TE-01,TE-02",
  value_or_witness="Both kinds present: TE-01 is a built component, TE-02/TE-03 are conceptual techniques stored as knowledge. M01 gives no field distinguishing them.",
  open_pressure_disposition="still-open")
o("supporting.Technology.open[1]:expiry and reassessment", disposition=NA, instance_ref="", value_or_witness="no reassessment observed.", open_pressure_disposition="not-exercised")

# ---- registries
o("registries.record_category.seeded<EMPTY>", disposition="exercised", instance_ref="registry_extensions.record_category",
  value_or_witness="Seven categories registered by distinct behaviour; empty seed correctly NOT filled with invented canonical values.", provenance="derived")
o("registries.unit_kind.seeded<EMPTY>", disposition="exercised", instance_ref="registry_extensions.unit_kind",
  value_or_witness="Three kinds registered (feature, stage, implementation-wave), matching M01's own 'software Feature belongs here'.", provenance="derived")
o("registries.effect_class.seeded<EMPTY>", disposition="exercised", instance_ref="registry_extensions.effect_class",
  value_or_witness="Four classes registered; receipt_requirements satisfied only for forge-merge, forge-issue-state and repository-write.", provenance="forge")
o("registries.scope_type.seeded.team", disposition=NA, instance_ref="",
  value_or_witness="not-applicable: the delivery swarm has no durable membership, no boundary of its own and no authority root; nothing evidences a Scope whose lifecycle differs from SC-03.",
  open_pressure_disposition="not-exercised")
o("registries.event_type.seeded.effect_disposition", disposition="exercised", instance_ref="EV-21,EV-23",
  value_or_witness="Full intended scalar present in the pinned file ('EffectBoundary performs, refuses or cannot determine a request') - S1's split is closed at this digest. Two dispositions witnessed, both performed.",
  provenance="forge", applicable_checks="S1")
o("registries.event_type.seeded.adaptation", disposition="exercised", instance_ref="EV-06,EV-28",
  value_or_witness="Full intended scalar present ('authorized change to a definition, composition or method'). EV-06 supplies prior_baseline and new_baseline; its decision_ref points at the unrecorded EV-05.",
  provenance="forge", applicable_checks="S1")
o("registries.event_type.seeded.observation", disposition="construct-pressure", instance_ref="EV-26",
  value_or_witness="required_extension demands capture_custody and raw_evidence_ref; BOTH ABSENT for the case's entire test evidence.",
  provenance="doc-claim", applicable_checks="I4", **CF["CF-04"])
o("registries.event_type.seeded.assessment", disposition="construct-pressure", instance_ref="EV-07,EV-11,EV-13",
  value_or_witness="gate_version_ref cannot pin a version (unversioned protocol); independence_check missing-history throughout; EV-13 is NOT WRITABLE at all.",
  provenance="doc-claim", applicable_checks="I7", **CF["CF-05"])
o("registries.event_type.seeded.gate_outcome", disposition="exercised", instance_ref="EV-08,EV-10,EV-12,EV-16,EV-18",
  value_or_witness="MODEL WIN and a direct vindication of M02 R2: EV-09 (an abandoned iteration-0 assessment whose record does not survive) exists WITHOUT an outcome payload, which the v4 merged form would have made unwritable.",
  provenance="doc-claim", applicable_checks="R2")
o("registries.event_type.seeded.decision", disposition="construct-pressure", instance_ref="EV-05,EV-29",
  value_or_witness="EV-29 (merge) fully satisfiable from the forge; EV-05 (scope reduction) has no occurred_at, no recorded_at and no custody.",
  provenance="forge/missing", **CF["CF-03"])
o("registries.event_type.seeded.transition", disposition="construct-pressure", instance_ref="EV-19",
  value_or_witness="T01 mandates a context_cycle(phase-end) at every gate PASS, but those rows live in the Unimatrix cycle store, outside the alphabet. Every transition Event here is an inference from the protocol.",
  provenance="inference", **HG("The Unimatrix cycle store is not in the fixed S alphabet."))
o("registries.event_type.seeded.communication", disposition="exercised", instance_ref="EV-01..EV-04",
  value_or_witness="Four communications; acknowledgement_requirement is 'none' on all four, and the advisory reviews' non-adoption is the evidence that none was required.",
  provenance="forge")
o("registries.event_type.seeded.effect_request", disposition="exercised", instance_ref="EV-20,EV-22,EV-24,EV-30",
  value_or_witness="Four requests; EV-30 (knowledge-store write) is the one with no corresponding disposition anywhere.", provenance="forge/doc-claim")
o("registries.capability_classification.seeded.curve", disposition="exercised", instance_ref="CP-02",
  value_or_witness="SLN1 is explicitly 'curve/nfr' and 'a curve is never whole' (S01 4898695344).", provenance="doc-claim")
o("registries.capability_classification.seeded.threshold", disposition="exercised", instance_ref="CP-01",
  value_or_witness="KI-AUDIT is explicitly 'threshold (proven)'.", provenance="doc-claim")

# ---- catalogs
o("catalogs.skill.construct", disposition=NA, instance_ref="", value_or_witness="no shared skill catalogue exists in the alphabet.", open_pressure_disposition="not-exercised")
o("catalogs.skill.scope", disposition=NA, instance_ref="", value_or_witness="not exercised.", open_pressure_disposition="not-exercised")
o("catalogs.skill.status", disposition=NA, instance_ref="", value_or_witness="not exercised; M01 open.skill_catalog untouched by this case.", open_pressure_disposition="still-open")
o("catalogs.workflow.construct", disposition="exercised", instance_ref="WF-01,WF-02",
  value_or_witness=".claude/protocols/uni/ is a program-scoped workflow catalogue with five members; two are instantiated here.", provenance="repo-artifact")
o("catalogs.gate.construct", disposition="exercised", instance_ref="GT-04..GT-08",
  value_or_witness="Gates are catalogued inside the workflow protocol, at workflow scope, not independently.", provenance="repo-artifact")

# ---- values
o("values.evidence_grade.values", disposition="construct-pressure", instance_ref="CP-02",
  value_or_witness="See core.Capability.fields.grade.", **MD("Closed RESOLVED vocabulary vs the program's evidenced, explicitly-ruled 'asserted'."))
for m,w in [("missing","no witness in this case"),("claimed","NOT used: writing it for CP-02 would silently normalise 'asserted'"),
            ("partial","no witness"),("proven","CP-01, as a doc-claim only")]:
    o(f"values.evidence_grade.values.{m}", disposition=("exercised" if m=="proven" else NA),
      instance_ref=("CP-01" if m=="proven" else ""), value_or_witness=w,
      open_pressure_disposition=("still-open" if m=="claimed" else "not-exercised" if m!="proven" else NA))
o("values.epistemic_kind.rule", disposition="exercised", instance_ref="EV-05,EV-29",
  value_or_witness="Orthogonality holds: both are decision Events; EV-05 is a claim, EV-29 is a mechanical-observation. 'decision' never appears as an epistemic kind.",
  provenance="derived", applicable_checks="A8")
for m in ["mechanical-observation","reported-observation","claim","inference","reviewed-finding"]:
    o(f"values.epistemic_kind.values.{m}", disposition="exercised", instance_ref="RC-25/RC-14/RC-01/RC-11/RC-08",
      value_or_witness="all five members witnessed; see core.Record.fields.epistemic_kind", provenance="derived")
o("values.significance.values.surprise", disposition="exercised", instance_ref="EV-05,EV-10",
  value_or_witness="the scope reduction and the REWORKABLE FAIL", provenance="doc-claim")
o("values.significance.values.exception", disposition="exercised", instance_ref="EV-07,EV-20", value_or_witness="gate assessments and the merge", provenance="forge")
o("values.significance.values.routine", disposition="exercised", instance_ref="EV-24", value_or_witness="wave commits", provenance="forge")
for m,r,w in [("inline","EV-05","a decision with no record"),("record-ref","EV-08","a gate outcome carried by RC-08"),("artifact-ref","EV-21","the merge commit")]:
    o(f"values.carrier.values.{m}", disposition="exercised", instance_ref=r, value_or_witness=w, provenance="forge")
o("values.currentness.values.current", disposition="exercised", instance_ref="RC-01,RC-03", value_or_witness="the reduced sources", provenance="repo-artifact")
o("values.currentness.values.superseded", disposition="exercised", instance_ref="RC-13,RC-20,RC-21,RC-23,RC-11,RC-12",
  value_or_witness="six superseded Records, all committed unmarked", provenance="repo-artifact")
o("values.currentness.values.stale", disposition="exercised", instance_ref="RC-09,RC-15",
  value_or_witness="the gate-3b report whose WARN was already fixed by 843d0049", provenance="forge")
o("values.currentness.values.unknown", disposition="exercised", instance_ref="SK-01..SK-03 held_by",
  value_or_witness="every actor-skill currentness", provenance="missing")
o("values.coupling.values.atomic", disposition="exercised", instance_ref="EV-21,EV-25", value_or_witness="the merge itself; each commit", provenance="forge")
o("values.coupling.values.ordered-best-effort", disposition="exercised", instance_ref="EV-23",
  value_or_witness="DEMONSTRATED: merged_at 11:29:07Z vs issue closed_at 11:29:09Z - a two-second lag between two effects the forge performs for one request.",
  provenance="forge")
o("values.coupling.values.reported", disposition=NA, instance_ref="", value_or_witness="no witness distinct from the above.", open_pressure_disposition="not-exercised")
o("values.coupling.values.unknown", disposition="exercised", instance_ref="EV-30",
  value_or_witness="the claimed Unimatrix knowledge-store writes (#5599-#5613) have no disposition at all.", provenance="doc-claim")
o("values.effect_disposition.values.performed", disposition="exercised", instance_ref="EV-21,EV-23,EV-25", value_or_witness="merge, issue close, commits", provenance="forge")
o("values.effect_disposition.values.refused", disposition=NA, instance_ref="",
  value_or_witness="NO WITNESS. Every requested effect in the case was performed. The trigger-injected rollback is a test fixture inside the delivery, evidenced only by an authored report, and is NOT counted.",
  open_pressure_disposition="not-exercised")
o("values.effect_disposition.values.unknown", disposition=NA, instance_ref="",
  value_or_witness="no witness; EV-30's absence is modelled as no disposition Event rather than an unknown one, because nothing reported back at all.",
  open_pressure_disposition="not-exercised")
o("values.effect_disposition.rule", disposition="exercised", instance_ref="EV-21,EV-08",
  value_or_witness="Both vocabularies used side by side and kept apart: EV-21 uses effect_disposition (performed); EV-08 uses GT-04's allowed_outcomes (PASS).",
  provenance="derived", applicable_checks="I6")
o("values.autonomy_tier.values.A0", disposition="exercised", instance_ref="DL-08,DL-09,DL-10,DL-13",
  value_or_witness="Full intended scalar present at this digest ('analyze, evaluate or recommend without discretionary work initiation') - S1 closed. Fits the validators, the security reviewer and uni-zero exactly: they assess and recommend, and initiate no work.",
  provenance="forge", applicable_checks="S1")
o("values.autonomy_tier.values.A1", disposition="exercised", instance_ref="DL-02..DL-07,DL-12", value_or_witness="bounded judgment within an assigned Unit - the implementers and designers", provenance="inference")
o("values.autonomy_tier.values.A2", disposition=NA, instance_ref="",
  value_or_witness="no witness: the delivery leader plans waves and spawns agents, which is A2-shaped, but no artefact in the alphabet describes a leader Actor or its grant.",
  open_pressure_disposition="not-exercised")
o("values.autonomy_tier.values.A3", disposition=NA, instance_ref="",
  value_or_witness="no witness. Full intended scalar present ('adapt local tactics, composition or reversible method detail'); status insufficient-evidence is UNCHANGED by this case.",
  open_pressure_disposition="still-open")
o("values.autonomy_tier.values.A4", disposition=NA, instance_ref="",
  value_or_witness="no witness; SC-03 was launched by AC-01 directly. status insufficient-evidence UNCHANGED.",
  open_pressure_disposition="still-open")
o("values.autonomy_tier.values.A5", disposition="exercised", instance_ref="DL-01",
  value_or_witness="Full intended scalar present ('change Collective policy, authority structures or strategic objectives'), held_by: human - and AC-01 is the only actor who reduces scope and merges.",
  provenance="forge", applicable_checks="S1")

# ---- invariants
INV = {
 "I1": ("exercised","RC-01,UN-01","Identity opaque and distinct from name: UN-01 and UN-02 are distinct Units under one project name 'vnc-045'. History-never-overwritten FAILS in the project: SCOPE.md was overwritten in place and the pre-reduction text exists at no commit.", "forge", CF["CF-01"]),
 "I2": ("exercised","EV-30,RC-14","Cleanest witness in the case: for the claimed #5599-#5613 stores, the Record's existence, its admission and the effect's occurrence are three separate facts and only the first is evidenced.","doc-claim",None),
 "I3": ("exercised","registry_extensions.record_category","Seven categories own schema, admission, retrieval, lifecycle and correction; two of them (agent-report, advisory-review) own NO admission and NO lifecycle, which is itself the observed behaviour.","derived",None),
 "I4": ("exercised","EV-26,RC-14","DEMONSTRATED with a live error: RC-14 is an actor-authored account with no capture provenance, so it is a claim - and it contains a factually wrong tool count (12->15) that the committed diff (14->15) refutes.","forge",CF["CF-04"]),
 "I5": ("exercised","EV-09,EV-10","GT-04 iteration 0 is corrected by new Events (EV-07/EV-08), not by editing; and occurrence does not establish payload truth - EV-12's PASS payload contains a stale WARN.","doc-claim",None),
 "I6": ("exercised","AR-01..03,EV-08,EV-21","All six kept distinct AND observably separated: the advisory reviews produce assessments with recommendations that carry no consequence, while GT-04's outcome carries one.","forge",None),
 "I7": ("construct-pressure","GT-06","SPECIFIED-NOT-ENFORCED, adversely. Gate 3c's independence could not be established from any record and the project did not fail closed - it merged. 153 of 226 feature directories carry the gate-3c report vnc-045 lacks; vnc-045 is the ONLY feature with 3a and 3b but no 3c.","forge",CF["CF-05"]),
 "I8": ("construct-pressure","GT-06,RC-14","The merged record infers success from missing evidence: 'Gate 3c PASS' appears in the PR body with no assessment behind it. V5 surfaces this as a missing required Record rather than letting the claim stand.","forge",CF["CF-05"]),
 "I9": ("exercised","CP-01,TE-01","Held affirmatively: no capability was moved to proven off this delivery, by explicit pre-registered ruling. CP-01's own 'proven' is carried as a doc-claim, not demonstrated to this run.","doc-claim",None),
 "I10": ("exercised","SK-01..SK-03","Held: no Skill is treated as a Capability or as authority anywhere in the case. Weak-positive - nothing tested it.","inference",None),
 "I11": ("exercised","TE-01","STRONGEST CONFORMING WITNESS. 'Do NOT mark any capability proven off vnc-045' is the project's own pre-registered ruling, made twice by an independent reviewer and honoured at delivery.","doc-claim",None),
 "I12": ("construct-pressure","EB-01,DL-01..13","SPECIFIED-NOT-ENFORCED. Autonomy is not authority - and no EffectBoundary disposition in the case demonstrates ANY delegated authority, because EB-01 authenticates one principal and enforces nothing about agents. The invariant is right and the project has no point at which it bites.","forge",None),
 "I13": ("exercised","CP-01,CP-02","Both capabilities are required by GO-01.","doc-claim",None),
 "I14": ("exercised","CP-01","KI-AUDIT's meaning is unchanged when its governed surface expands to a new op; only the evidence set grows.","doc-claim",None),
 "I15": ("exercised","UN-03,AT-03,AT-04","Unit identity survives the GT-04 rework; each execution is an Attempt. Verifiable at the document altitude only - both attempts collapse into commit 3afc2c49.","doc-claim",CF["CF-02"]),
 "I16": ("exercised","UN-01,UN-02","MODEL WIN. The human scope reduction changed the intended outcome and V5 forces two Units with a replaces edge; the project reused one identifier and overwrote in place.","repo-artifact",None),
 "I17": ("construct-pressure","DL-02..DL-13","SPECIFIED-NOT-ENFORCED and demonstrably violated on the effect axis: derived grants run under the same credentials as the root, so no derived Delegation is actually narrower. Authority does reach every Actor through a chain from SC-01 - but only as an inference.","inference",None),
 "I18": ("exercised","WF-01,WF-02","DEMONSTRATED: PR #929 changed 57 files, none under .claude/. Adaptation-as-event holds for the ADR deferral (EV-06) and fails for SCOPE.md, which was edited in place with no adaptation record of its own.","forge",CF["CF-03"]),
 "I19": ("exercised","registry_extensions","No registered extension weakens a common invariant. The nearest strain is the grade vocabulary, which is a MODEL closure rather than a program extension - see values.evidence_grade. S6's binding question stands: I19 is cited only by Workflow.","derived",None),
}
for k,(disp,ref,wit,prov,cf) in INV.items():
    kw = dict(disposition=disp, instance_ref=ref, value_or_witness=wit, provenance=prov,
              enforcement_reality=("specified-not-enforced" if disp=="construct-pressure" else "none - no common checker implements this model"))
    if cf: kw.update(cf)
    elif disp=="construct-pressure": kw.update(EG(wit))
    o(f"invariants.{k}", **kw)

# ---- excluded (negative tests)
EXC = {
 0:("exercised","UN-02","NEGATIVE TEST PASSES: 'feature' is registered as a unit_kind, not as a construct. M01's admission_rule anticipated it verbatim."),
 1:("exercised","SK-01..03","NEGATIVE TEST PASSES vacuously: no qualification evidence exists in the case, so nothing needed a Qualification construct - but nothing tested the boundary either."),
 2:("exercised","DL-01..13","NEGATIVE TEST PASSES: limits travel with the Delegation (effect_grants, resource_ceiling, escalation_conditions); no Envelope construct was wanted."),
 3:("exercised","EV-20,EV-29","NEGATIVE TEST PASSES and it is load-bearing: the merge and the scope reduction are the authority ROOT acting, expressed as authority_ref -> SC-03. No AuthorityBasis was needed."),
 4:("exercised","RC-14,GT-06","NEGATIVE TEST PASSES: RC-14 is a Record playing an evidence role under a gate that never consumed it; no EvidenceItem construct was wanted."),
 5:("exercised","RC-01,RC-03","NEGATIVE TEST PASSES: versions belong to Record identity. Strained only because the project overwrote SCOPE.md, leaving no prior version to hold."),
 6:("exercised","EV-01..EV-30","NEGATIVE TEST PASSES across the board: signal, decision, transition, assessment, outcome, effect request and effect receipt are all Events here, and none wanted a noun."),
 7:("exercised","EV-20/EV-21,EV-22/EV-23","NEGATIVE TEST PASSES and PAYS OFF: the merge/issue-close pair is only expressible as separate request and disposition because the two-second lag makes them observably non-atomic."),
 8:("exercised","CP-01,UN-02,AT-03","NEGATIVE TEST PASSES: no organizational-level capability kind, Goal is never a Scope (SC-03 is), Attempt is never a Unit subtype, and no lesson event type was wanted."),
 9:("exercised","GT-04,GT-07,GT-08","NEGATIVE TEST PASSES decisively: three DIFFERENT outcome vocabularies coexist in one case ([PASS,REWORKABLE FAIL,SCOPE FAIL], [READY,BLOCKED], [PASS,WARN,VARIANCE,FAIL]). A universal outcome enum would have broken the instance."),
 10:("exercised","DL-08,EB-01","NEGATIVE TEST PASSES: A0 assessors hold no effect authority, and autonomy nowhere stands in for evidence strength."),
}
for i,(disp,ref,wit) in EXC.items():
    for cls,p in X:
        if p.startswith(f"excluded[{i}]:"):
            o(p, disposition=disp, instance_ref=ref, value_or_witness=wit, provenance="derived")

# ---- top-level open
TOPEN = {
 "delegation_attenuation": ("exercised","DL-02..13","still-open","Non-numeric grants are incomparable in this case precisely because every agent holds identical credentials; no revocation observed.",None),
 "workflow_promotion": ("exercised","WF-01,WF-02","resolved-by-instance","AFFIRMATIVE: the software case is unencodable without Workflow. Stages, waves, gates, rework limits, state transitions and method custody all hang off it. This case supports promotion.",None),
 "custody_enforcement": ("construct-pressure","EB-01,DL-01..13","blocking-hole","CONFIRMED with no common enforcement point anywhere: custody is asserted by protocol text and enforced by nothing; the one externally custodied boundary (GitHub) enforces nothing about agents or grants.",EG("No enforcement point exists.")),
 "event_identity_threshold": ("construct-pressure","EV-05","still-open","Exercised adversely: the case's most consequential Event has no durable identity and M01 supplies no rule that would have required one.",CF["CF-03"]),
 "gate_identity": ("construct-pressure","GT-04..GT-08","still-open","Exercised adversely: T01/T02 are unversioned living files, so gate_version_ref cannot pin anything and every assessment Event in the case carries an unversioned reference.",EG("The protocol carries no version identifier.")),
 "skill_catalog": (NA,"","not-exercised","No shared skill catalogue and no repository-local binding in the alphabet.",None),
 "lesson_vs_pattern": (NA,"","not-exercised","not-applicable to the software case: it produces patterns (#5612/#5613) and no lesson-learned, and neither node's content is in the alphabet, so no behavioural distinction is observable. Belongs to W1.",None),
 "collective_boundary": ("exercised","SC-01","still-open","AC-01 is sole root and sole forge identity; no succession, no membership record.",None),
 "autonomy_A3_A4": (NA,"","still-open","NEITHER TIER HAS A WITNESS in this case. A3 and A4 remain insufficient-evidence, unchanged.",None),
 "capability_rollup": (NA,"","not-exercised","No capability composition in the case.",None),
 "semantic_compression": ("exercised","whole instance","still-open","One case, one owner-operated program. Seven core entities sufficed with no eighth common construct - directional support only, and the grade-vocabulary defect is adverse to the values block rather than to the seven.",None),
}
for k,(disp,ref,od,wit,cf) in TOPEN.items():
    kw=dict(disposition=disp, instance_ref=ref, open_pressure_disposition=od, value_or_witness=wit, provenance="derived")
    if cf: kw.update(cf)
    o(f"open.{k}", **kw)

# ---- changelog
o("changelog.5.0.0", disposition="exercised", instance_ref="EV-08,EV-20,RO-13,GT-04",
  value_or_witness="Four V5 changes are load-bearing in this instance and would have broken it in v4: invariant binding (used throughout), the gate_outcome split (EV-09 without EV-10), Event authority as ref<Delegation|Scope> (EV-20/EV-29 = root acting), and Role.receives (DL-13 standing to RO-13). Scope seed conformance and the inverse rule are also consumed.",
  provenance="derived", applicable_checks="R1,R2,R3,R4,R5,A1,A2,A4,A5,A6")
o("changelog.4.0.0", disposition="exercised", instance_ref="DL-01..13,AT-01..17,GT-04..08",
  value_or_witness="Standing/dynamic Delegation, attenuation, rigorous Gate and Attempt semantics and registry extensibility are all consumed by this instance.",
  provenance="derived")

# ---- review concerns S1-S8 + traversals
o("M02.sanity.S1", disposition="exercised", instance_ref="values.autonomy_tier,event_type",
  value_or_witness="CLOSED AT THIS DIGEST, independently re-verified. sha256 of M01 re-computed as bf8e5536...9841060 (matches the pin), and a PyYAML parse returns the complete six formerly-split scalars. The file was parsed AS-IS; no quoting, normalising or in-memory patching was applied.",
  provenance="derived", applicable_checks="S1")
o("M02.sanity.S2", disposition="exercised", instance_ref="UN-03,UN-04,UN-05",
  value_or_witness="Exercised: Gate.evaluates targets Unit|Record|Capability|Event and the dotted inverse 'Unit.gated_by' resolved correctly in this instance only because a human read the subset rule. All five gates target Units, so the qualified form was never stressed against a Record or Event target.",
  provenance="derived", open_pressure_disposition="still-open")
o("M02.sanity.S3", disposition="exercised", instance_ref="whole instance",
  value_or_witness="Confirmed live: form, owner and extension_owner are undocumented in notation and were all three consumed while encoding. No instance error resulted, but the reader is relying on inference.",
  provenance="derived", open_pressure_disposition="still-open")
o("M02.sanity.S4", disposition="exercised", instance_ref="I1,I4,I15,I18",
  value_or_witness="CONFIRMED AND IT BITES. Four of the seven un-split invariants split under this case in opposite directions: I1's clauses disagree (identity holds, history-never-overwritten fails on SCOPE.md); I4's clauses both hold; I15's hold at document altitude and fail at forge altitude; I18's custody clause holds while its adaptation-as-event clause fails for SCOPE.md. A checker could not report which clause failed.",
  provenance="forge", open_pressure_disposition="blocking-hole",
  **P("model-defect","Four invariants in this case have clauses with different verdicts, exactly as M02 S4 predicted. Reporting 'I1 fails' would be wrong; reporting 'I1 passes' would be wrong.","reject",cur="partial"))
o("M02.sanity.S5", disposition="exercised", instance_ref="DL-01,DL-13,DL-02",
  value_or_witness="Exercised WITHOUT hitting the mixed case: DL-01 and DL-13 are standing (grantee Role, unit absent); DL-02..DL-12 are dynamic (grantee Actor, unit present). No Delegation naming a Role AND a Unit arose, so the undefined case is untested here.",
  provenance="inference", open_pressure_disposition="still-open")
o("M02.sanity.S6", disposition="exercised", instance_ref="registry_extensions",
  value_or_witness="Live: I19 is cited by Workflow alone, yet in this instance the constructs carrying extension points were Capability, Unit, Event, Record and Gate. I19 governed extensions on constructs that do not cite it.",
  provenance="derived", open_pressure_disposition="still-open")
o("M02.sanity.S7", disposition="exercised", instance_ref="AC-02..16,RO-01,RO-13",
  value_or_witness="Live and mildly confusing in practice: Role.receives declares inverse: grantee while Actor.receives declares none, though both invert Delegation.grantee. Both were traversable; the asymmetry cost nothing here.",
  provenance="derived", open_pressure_disposition="still-open")
o("M02.sanity.S8", disposition=NA, instance_ref="",
  value_or_witness="Out of W2's scope: superseded-marker hygiene across the M-alphabet model files is a repository question, not an instantiation question. W2 edited no model file.",
  open_pressure_disposition="not-exercised")
o("traversal.Goal->applicable_Workflows", disposition="exercised", instance_ref="GO-01 -> [WF-01, WF-02]",
  value_or_witness="DEMONSTRATED by index scan over Workflow.applies_to. No new relation added. This is exactly the disposition M02 section 7 adopted when A3 was withdrawn.",
  provenance="derived")
o("traversal.Actor->participated_Attempts", disposition="exercised", instance_ref="AC-09 -> [AT-08]",
  value_or_witness="DEMONSTRATED by index scan over Attempt.actors. No new relation added.",
  provenance="derived")

# ---------------------------------------------------------------- defaults
DEFAULTS = [
 ("core.Scope",       "SC-01,SC-02,SC-03"),
 ("core.Goal",        "GO-01,GO-02,GO-03"),
 ("core.Capability",  "CP-01,CP-02"),
 ("core.Actor",       "AC-01..AC-19"),
 ("core.Unit",        "UN-01..UN-08"),
 ("core.Event",       "EV-01..EV-30"),
 ("core.Record",      "RC-01..RC-27"),
 ("supporting.Workflow","WF-01,WF-02"),
 ("supporting.Skill", "SK-01..SK-03"),
 ("supporting.Role",  "RO-01..RO-13"),
 ("supporting.Delegation","DL-01..DL-13"),
 ("supporting.Gate",  "GT-04..GT-08"),
 ("supporting.EffectBoundary","EB-01..EB-03"),
 ("supporting.Attempt","AT-01..AT-17"),
 ("supporting.Technology","TE-01..TE-03"),
]
def default_for(cls, path):
    for pref, ref in DEFAULTS:
        if path.startswith(pref + "."):
            return dict(disposition="exercised", instance_ref=ref,
                        value_or_witness="instantiated in vnc-045-instance.yaml",
                        provenance="see instance", custody="see instance",
                        enforcement_reality="none - no common checker implements this model")
    if path.startswith("registries."):
        return dict(disposition="exercised", instance_ref="registry_extensions",
                    value_or_witness="consumed while registering or using this registry",
                    provenance="derived", enforcement_reality="none")
    if path.startswith("values."):
        return dict(disposition="exercised", instance_ref="see instance",
                    value_or_witness="vocabulary consumed by the instance",
                    provenance="derived", enforcement_reality="none")
    if path.startswith("catalogs."):
        return dict(disposition="exercised", instance_ref="WF-01,WF-02,GT-04..08",
                    value_or_witness="workflow and gate catalogues observed at program scope",
                    provenance="repo-artifact", enforcement_reality="none")
    return dict(disposition="exercised", instance_ref="whole instance",
                value_or_witness="consumed while encoding the case", provenance="derived",
                enforcement_reality="none")

# ---------------------------------------------------------------- emit
out = []
for cls, path in X:
    r = row(x_class=cls, model_path=path, **default_for(cls, path))
    if path in O:
        r.update(O[path])
    for c in COLS:
        if r[c] == "" or r[c] is None:
            r[c] = NA
    out.append(r)

OUT = "/workspaces/arch-research/product/research/wfh-011/artifacts/vnc-045-coverage.csv"
with open(OUT, "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS)
    w.writeheader()
    for r in out:
        w.writerow(r)

from collections import Counter
print("rows:", len(out))
print("dispositions:", dict(Counter(r["disposition"] for r in out)))
cc = Counter()
for r in out:
    if r["cause_classification"] != NA:
        for c in r["cause_classification"].split("|"):
            cc[c] += 1
print("cause classifications (rows may carry several):", dict(cc))
print("rows carrying >=1 cause classification:", sum(1 for r in out if r["cause_classification"] != NA))
print("project-evolution-candidate rows:", sum(1 for r in out if "project-evolution-candidate" in r["cause_classification"]))
print("open dispositions:", dict(Counter(r["open_pressure_disposition"] for r in out if r["open_pressure_disposition"] != NA)))
missing = [r["model_path"] for r in out if r["disposition"] not in ("exercised", NA, "blocked-by-OPEN", "construct-pressure")]
print("rows with invalid disposition:", len(missing))
blanks = [r["model_path"] for r in out for c in COLS if r[c] == ""]
print("rows with a silent blank field:", len(blanks))
