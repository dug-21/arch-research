# Annex to S4 (adjacent prior art) — clinical EDC and the evidence-graded commit

**Provenance:** returned by a sub-agent spawned by scout S4 under job (b). Persisted by the leader
ahead of S4's own return so it is not lost; it is **S4's material, not a sixth scout**, and is merged
into the cross-surface reconciliation as part of S4's adjacent-prior-art surface. `surface: adjacent`.

**Verdict up front: yes, this primitive is shipped, named, and mandatory here — but it is split across three artifacts that no one has unified.** The append-only part is `audit trail` (regulation + software). The declared-kind-evidence part is `def:Origin` in **Define-XML** (schema, FDA-required). The authority part is the **delegation log** + Form FDA 1572 (paper/PDF, not machine-readable). Nothing in the stack *joins* them at commit time.

---

## 1. What makes a commit VALID here?

Two different "commits," different validity conditions.

### Commit A — a data point entered into the eCRF

| Condition | Source |
|---|---|
| Entered by an **authorized data originator** on a maintained list | FDA eSource guidance §III.A.1: "Each data element is associated with an authorized data originator… A list of all authorized data originators (i.e., persons, systems, devices, and instruments) should be developed and maintained by the sponsor and made available at each clinical site." ([FDA 2013, p.3](https://www.fda.gov/media/85183/download)) |
| Carries a **data element identifier** recording who/when | Same guidance §III.A.3: "The eCRF should include the capability to record who entered or generated the data and when it was entered or generated." |
| Any change records **who, when, and why**, and does not obscure the original | 21 CFR 11.10(e); ICH E6(R3) §2.12.6 |
| Consistent with source records, or the discrepancy explained | E6(R3) §2.12.6: "Data reported to the sponsor should be consistent with the source records or the discrepancies explained." |
| Corrections must be **justified and supported by source records** | E6(R3) §4.2.4: "Corrections should be attributed to the person or computerised system making the correction, justified and supported by source records around the time of original entry" |

Note the exact shape: **a correction is only valid if it cites source-record evidence.** That is the primitive, stated in a guideline, in 2025.

### Commit B — the study data package submitted to FDA

Validity is *machine-checked and mechanically rejectable*. FDA runs **Technical Rejection Criteria (TRC)** — "automated validations by the Center (CDER or CBER) inbound processing system." A submission missing a valid Trial Summary dataset or Study Tagging File fails eCTD validation (errors 1734, 1789) and is **rejected at the door** ([sdTCG v6.2.1, June 2026, §8.1.2](https://www.fda.gov/media/153632/download)). Every dataset must be accompanied by a `define.xml` — "arguably the most important part of the electronic dataset submission for regulatory review… the sponsor needs to provide complete detail in this file, especially for the specifications pertaining to derived variables."

---

## 2. WHO may make one?

Enumerated at four altitudes, with decreasing formality as you go down:

**Statutory / signed:** the investigator signs **Form FDA 1572**, and 21 CFR 312.62(b) makes them personally responsible for "adequate and accurate case histories that record all observations and other data pertinent to the investigation."

**The delegation log** — the named artifact for authority:
- ICH E6(R2) §4.1.5: "The investigator should maintain a list of appropriately qualified persons to whom the investigator has delegated significant trial-related duties."
- ICH E6(R2) §5.5.3(e): the sponsor must "Maintain a list of the individuals who are authorized to make data changes."
- E6(R3) §2.3.2–2.3.3 **weakened** it to proportionate: delegation documentation "should be proportionate to the significance of the trial-related activities," and where activities are ordinary clinical practice, "delegation documentation may not be required."

**Machine-readable (the interesting part):**
- **ODM v2.0** `UserType`: `Sponsor | Investigator | Lab | Other | Subject | Monitor | Data analyst | Care provider | Assessor` ([ODM-enumerations.xsd](https://raw.githubusercontent.com/cdisc-org/DataExchange-ODM/main/schema/ODM-enumerations.xsd))
- **Define-XML** `def:Origin/@Source` (NCIt C170450): `Clinical Study Sponsor | Investigator | Study Subject | Vendor`

**Enforcement:** FY2025's #1 BIMO 483 observation was 21 CFR 312.60 — "An investigation was not conducted in accordance with the signed statement of investigator" — cited **80 times**.

---

## 3. What EVIDENCE KINDS are declared?

**Strongest match to the primitive, and it is a real controlled vocabulary in a real required schema.**

Define-XML v2.1's `def:Origin` has two enumerated attributes plus an evidence pointer.

`@Type` — NCIt codelist **C170449 "CDISC Define-XML Origin Type Terminology"** ([NCI EVS API](https://api-evsrest.nci.nih.gov/api/v1/subset/ncit/C170449/members?include=minimal&pageSize=50)):

| Value | CDISC definition |
|---|---|
| **Collected Value** | "A value that is actually observed and recorded by a person or obtained by an instrument." |
| **Derived Value** | "A value that is calculated by an algorithm or reproducible rule, and which is dependent upon other data values." |
| **Assigned Value** | "A value that is derived through designation, such as values from a look up table or a label on a CRF." |
| **Copied Value** | "A value that is copied from another variable." |
| **Protocol Value** | "A value that is included as part of the study protocol." |
| Not Available / Other | — |

`@Source` — codelist C170450: `Investigator | Clinical Study Sponsor | Study Subject | Vendor`.

The child element **points at the evidence artifact**. From CDISC's own published Define-XML v2.1 SDTM example ([defineV21-SDTM.xml](https://raw.githubusercontent.com/cdisc-org/define-xml-2.1-stylesheets/master/cdisc-2019/examples/DefineXML-2-1-SDTM/defineV21-SDTM.xml), line 839):

```xml
<ItemDef OID="IT.DM.ETHNIC" Name="ETHNIC" DataType="text" ...>
  <def:Origin Type="Collected" Source="Investigator">
    <def:DocumentRef leafID="LF.acrf">
      <def:PDFPageRef PageRefs="6" Type="PhysicalRef"/>
    </def:DocumentRef>
  </def:Origin>
</ItemDef>
```

Read that as the primitive: **kind = Collected, authority = Investigator, evidence = annotated CRF page 6.** Schema-validated. Required in every FDA and PMDA submission.

For `Type="Derived"`, the evidence is a `MethodDef` carrying `Description`, `FormalExpression` (with `Context` naming language/version), and optionally a `def:DocumentRef` to the algorithm document.

**Other declared vocabularies:**
- **SDTM/SDTMIG** (current SDTMIGv3.4, support began 2023-12-13) — the domain model constraining *what can be said at all*.
- **ODM v2.0 `AuditRecord`** — `UserRef, LocationRef, DateTimeStamp, ReasonForChange?, SourceID?`. `ReasonForChange` is **free text, no codelist**.
- **ODM v2.0 `Annotation → Flag → FlagValue/FlagType`** — the query/discrepancy carrier. Both require a `CodeListOID` that is **sponsor-defined per study**. No industry query-reason codelist exists.
- **ODM v2.0 `SignatureDef`** — requires *both* `Meaning` and `LegalReason` as mandatory children. That is 21 CFR 11.50(a)(3)'s "meaning associated with the signature" rendered machine-readable.
- **CDASH (CDASHIG v2.3, 2023-09-28)** — **not in the FDA Data Standards Catalog** (checked all sheets: zero CDASH rows). sdTCG only says traceability "can be enhanced when studies are prospectively designed to collect data using a standardized CRF, e.g., CDASH." Recommended, never required.

---

## 4. How is APPEND-ONLY enforced?

All four mechanisms, layered:

**Regulation:** 21 CFR 11.10(e) requires "secure, computer-generated, time-stamped audit trails to independently record the date and time of operator entries and actions that create, modify, or delete electronic records," and that "record changes shall not obscure previously recorded information."

**Explicit no-delete mandate:** E6(R2) §5.5.3(c) — sponsors must "Ensure that the systems are designed to permit data changes in such a way that the data changes are documented and that there is **no deletion of entered data** (i.e., maintain an audit trail, data trail, edit trail)."

**Anti-tamper on the trail itself** — E6(R3) §4.2.2(b), the tightest text: "Ensuring that audit trails, reports and logs are **not disabled**. Audit trails should **not be modified except in rare circumstances** (e.g., when a participant's personal information is inadvertently included in the data) and only if a log of such action and justification is maintained."

**Software constraint, but validating it is the sponsor's burden:** 21 CFR 11.10(a) requires "validation of systems to ensure accuracy, reliability, consistent intended performance, and **the ability to discern invalid or altered records**." Append-only is a *validated property you must demonstrate*, not one you inherit from a database.

**Inspection:** FY2025 produced **160 Bioresearch Monitoring Form FDA 483s** ([FDA FY2025 observations](https://www.fda.gov/media/190190/download?attachment)); #2 citation was 21 CFR 312.62(b) "Failure to prepare or maintain adequate/accurate case histories" — **52 times** (#3 was 12, so records failures dominate).

**Administrative death penalty:** 21 CFR 312.70 disqualification, for an investigator who "repeatedly or deliberately failed to comply" or "repeatedly or deliberately submitted false information in any required report." Disqualified investigators may not conduct *any* investigation supporting an FDA marketing permit, and prior data is re-examined for reliability. FDA's public register lists **232 records** ([Disqualification Proceedings](https://www.accessdata.fda.gov/scripts/sda/sdNavigation.cfm?sd=clinicalinvestigatorsdisqualificationproceedings)).

**Criminal liability:** exists (false statements on a signed 1572; 18 U.S.C. §1001) — **[could not verify]** a specific named prosecution; DOJ press-release search returned 403 this session.

**Retention:** 21 CFR 312.62(c) — 2 years post-approval/post-discontinuation; E6(R2) §4.9.5 — at least 2 years after last ICH-region marketing approval.

---

## 5. What does it COST?

### Evidence-checking is the dominant line item, and it is nearly worthless

- **Sheetz et al. 2014 (TransCelerate), 1,168 Phase I–IV studies, 53 sponsors** ([Ther Innov Regul Sci 48(6)](https://journals.sagepub.com/doi/full/10.1177/2168479014554400)): 3.7% of eCRF data corrected at all; **SDV corrected 1.1% of the total eCRF dataset**; SDV drove **32.0%** of corrections (two-thirds came from elsewhere). Conclusion: "SDV has a negligible impact on data quality" and should "no longer be the foremost quality management method employed in clinical trials."
- **Andersen et al. 2015, 2,566 subjects, >3M data fields** ([PMID 25327707](https://pubmed.ncbi.nlm.nih.gov/25327707/)): overall error 0.45%; 100% SDV 0.27% vs partial 0.53%. Killer number: **complete SDV of ~370 data points to avoid one unspecified error.**
- **Klatte et al. 2021, Cochrane review** ([PMID 34878168](https://pubmed.ncbi.nlm.nih.gov/34878168/)): RBM "not inferior to extensive on-site monitoring," RR 1.03 (95% CI 0.81–1.33) for major/critical findings; extensive monitoring cost **up to 3.4×**.
- **Andersen et al. 2023, >1.7M data points** ([PMID 36478289](https://pubmed.ncbi.nlm.nih.gov/36478289/)): RBM *beat* classic monitoring on what matters — major efficacy errors 0.15% vs 0.28%; major safety 0.49% vs 0.67%.

### Dollars

| Figure | Value | Source |
|---|---|---|
| Avg per-study cost, Phase 3 | **$19.9M** (Ph1 $3.8M, Ph2 $13.4M) | Sertkaya et al., ERG for HHS/ASPE, 2014 |
| Site monitoring, Phase 3 | **$1.6M/study — 9–14% of total** | same |
| Data management, Phase 3 | **$39K/study — <1% of total** | same |
| Monitoring visits avoided by remote RBM | **$13,500–$61,500 per trial site** | Yamada et al., Clin Trials 2021 ([PMID 33258688](https://pubmed.ncbi.nlm.nih.gov/33258688/)) |
| Query-driven SDV savings | **3–14% small studies; 25–35%+ large** | Tantsyura et al., TIRS 2016 ([PMID 30236013](https://pubmed.ncbi.nlm.nih.gov/30236013/)) |
| RBQM ROI (2026) | monitoring cost **−18%** at 10% SDV; phase duration **−8 to −19%**; trial ROI **$3.2M (Ph1) to $18.9M (Ph3)**, 6×–23× | Dirks et al., TIRS 2026 ([PMID 42348072](https://pubmed.ncbi.nlm.nih.gov/42348072/)) |

**The asymmetry that matters:** site monitoring costs ~40× what data management costs. Nearly all money is in *verifying* evidence, almost none in *recording* it. The record-keeping layer is cheap; the human attestation-checking layer eats the budget — and the evidence says it barely works.

**EDC cost per study/site: [could not verify].** No vendor publishes prices (Castor's pricing page: "We tailor pricing to your needs"). ASPE's Data Management line ($39K–$60K/study) is the closest sourced proxy but almost certainly excludes platform licensing.

### Failure modes

- FY2025 BIMO 483s = **160**. Top two: 21 CFR 312.60 protocol/1572 non-compliance (**80**), 21 CFR 312.62(b) inadequate or inaccurate case histories (**52**).
- **232 clinical investigators** in FDA's disqualification register.
- sdTCG's own confessions: "An **insufficiently documented data definition file is a common deficiency** that reviewers have noted"; "establishing traceability is one of the most problematic issues associated with any data conversion."

---

## Regulatory dates verified

- **ICH E6(R3)** — "Final version **Adopted on 06 January 2025**"; document history: "Endorsement by the Regulatory Members of the ICH Assembly under Step 4 — 06 January 2025." ✅ verified from the guideline PDF itself.
- **FDA adoption of E6(R3)** — final guidance, Federal Register **90 FR 43460, 9 September 2025**, Docket **FDA-2023-D-1955**. Annex 2 still draft.
- **Define-XML FDA-required?** ✅ with dates. Catalog **v11.0**: Define.xml-v2.0 requirement begins 12/17/2016 [1] / 12/17/2017 [2]; Define.xml-v2.1 support 2020-07-07, **requirement begins 03/15/2022 [1] / 03/15/2023 [2]**. Footnote [1] = "For NDAs, ANDAs, and certain BLAs"; [2] = "For certain INDs."
- **PMDA requirement** — [inferred] from CDISC's own claim; no PMDA primary source reached.
- **Current Define-XML** — v2.1.11, 2026-04-06 (schema/CT-package refresh of v2.1, not a new model version).

---

## Verdict

| The primitive | Name here | Maturity |
|---|---|---|
| append-only | **audit trail** (21 CFR 11.10(e); E6(R2) 5.5.3(c) "no deletion of entered data") | Shipped, mandatory, inspected |
| declared-kind evidence | **`def:Origin` Type + Source + DocumentRef** (Define-XML) | Shipped, schema-enforced, **FDA-required since 2016/2022**, machine-readable |
| defined set of who | **delegation log** (E6 4.1.5) + authorized-originator list + `UserType`/`Origin@Source` enums | Split: enumerated in schema, authoritative in PDFs |
| "on what evidence, by whom, when" | audit trail + Define-XML traceability + `Signature`(Meaning, LegalReason) | Shipped, but answered by joining three systems by hand |

**ADOPT:** **Define-XML v2.1** (CDISC standard, FDA/PMDA-required) as the declaration format, with **NCIt C170449/C170450** as ready-made evidence-kind and authority vocabularies. Plus **ODM v2.0** (free XSDs at github.com/cdisc-org/DataExchange-ODM) for `AuditRecord` and `SignatureDef`. Open schemas, validate today, zero licensing.

**Where the off-the-shelf answer STOPS — five places:**

1. **Retrospective, not enforcing.** Define-XML is authored at *submission* time, months or years after the commit. Nothing checks at write time that a value tagged `Type="Collected" Source="Investigator"` actually was. It's a promise about the past, not a precondition on the commit — the reverse of what is wanted.
2. **No validity gate.** No rule says a record lacking declared-kind evidence is *invalid*. Missing `Origin` is a review *deficiency*, not a rejection. The only mechanically-enforced gate (TRC) checks that ts.xpt and a Study Tagging File exist — it never opens the define.xml.
3. **Variable-level, not record-level.** `def:Origin` declares the ETHNIC *column* is investigator-collected. It says nothing about *this subject's ETHNIC value on 2026-03-04*. The primitive wanted is per-commit; Define-XML is per-column.
4. **`ReasonForChange` and query reasons are free text.** ODM `AuditRecord/ReasonForChange` has no codelist; `FlagValue`/`FlagType` require a sponsor-defined per-study `CodeListOID`. The one place the industry actually asks "why did this change?" is exactly where declared-kind discipline evaporates. Clearest unfilled gap.
5. **Authority lives in a PDF.** The delegation log is a scanned signature sheet, and E6(R3) §2.3.3 just made it weaker. ODM's `UserType` is a transport artifact, not the authoritative roster. Nothing joins "the account that wrote this row" to "the person on the delegation log for that task" — that join is done by a human monitor at $1.6M per Phase 3 trial to find errors at one per 370 verified data points.

**Contrarian read:** the industry spent 30 years and enormous money building the *checking* half of this primitive (SDV) and has now, with E6(R3) and RBQM, largely concluded the checking doesn't pay. What survived is the *declaration* half — Define-XML — cheap, machine-readable, mandatory, and mostly ignored until submission. Lesson from the most regulated version of this primitive on earth: **the enumerated evidence-kind vocabulary is the part that works and costs nothing; human verification of it is the part that costs everything and finds nothing.**

---

## `cites:`

```
- standard · https://database.ich.org/sites/default/files/ICH_E6(R3)_Step4_FinalGuideline_2025_0106.pdf · Guideline for Good Clinical Practice E6(R3), adopted 06 January 2025 · ICH, 2025
- standard · https://database.ich.org/sites/default/files/E6_R2_Addendum.pdf · Integrated Addendum to ICH E6(R1): Guideline for Good Clinical Practice E6(R2) · ICH, 2016
- docs · https://www.federalregister.gov/documents/2025/09/09/2025-17311/e6r3-good-clinical-practice-international-council-for-harmonisation-guidance-for-industry · E6(R3) Good Clinical Practice; ICH; Guidance for Industry; Availability (90 FR 43460, Docket FDA-2023-D-1955) · FDA, 2025
- standard · https://www.law.cornell.edu/cfr/text/21/11.10 · 21 CFR §11.10 — Controls for closed systems
- standard · https://www.law.cornell.edu/cfr/text/21/11.50 · 21 CFR §11.50 — Signature manifestations
- standard · https://www.law.cornell.edu/cfr/text/21/11.100 · 21 CFR §11.100 — General requirements for electronic signatures
- standard · https://www.law.cornell.edu/cfr/text/21/312.62 · 21 CFR §312.62 — Investigator recordkeeping and record retention
- standard · https://www.law.cornell.edu/cfr/text/21/312.70 · 21 CFR §312.70 — Disqualification of a clinical investigator
- docs · https://www.fda.gov/media/85183/download · Guidance for Industry: Electronic Source Data in Clinical Investigations · FDA (CDER/CBER/CDRH), 2013
- docs · https://www.fda.gov/media/153632/download · Study Data Technical Conformance Guide, Technical Specifications Document, v6.2.1 · FDA (CBER/CDER), June 2026
- docs · https://www.fda.gov/media/185927/download · FDA Data Standards Catalog v11.0 (xlsx) · FDA
- docs · https://www.fda.gov/industry/fda-data-standards-advisory-board/study-data-standards-resources · Study Data Standards Resources · FDA
- docs · https://www.fda.gov/media/190190/download?attachment · Inspectional Observation Data Set, FY2025 (Bioresearch Monitoring tab) · FDA, 2025
- docs · https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-references/inspection-observations · Inspection Observations · FDA
- docs · https://www.accessdata.fda.gov/scripts/sda/sdNavigation.cfm?sd=clinicalinvestigatorsdisqualificationproceedings · Clinical Investigators — Disqualification Proceedings (232 records) · FDA
- standard · https://www.cdisc.org/standards/data-exchange/define-xml · Define-XML (v2.1.11, 2026-04-06) · CDISC
- standard · https://www.cdisc.org/standards/data-exchange/odm · ODM-XML v2.0 (released 2023-08-23) · CDISC
- standard · https://www.cdisc.org/standards/foundational/cdash · CDASH / CDASHIG v2.3 (2023-09-28) · CDISC
- repo · https://raw.githubusercontent.com/cdisc-org/DataExchange-ODM/main/schema/ODM-clinicaldata.xsd · ODM v2.0 clinical data schema (AuditRecord, Signature) · CDISC
- repo · https://raw.githubusercontent.com/cdisc-org/DataExchange-ODM/main/schema/ODM-admindata.xsd · ODM v2.0 admin data schema (SignatureDef: Meaning, LegalReason) · CDISC
- repo · https://raw.githubusercontent.com/cdisc-org/DataExchange-ODM/main/schema/ODM-enumerations.xsd · ODM v2.0 enumerations (UserType, OrganizationType) · CDISC
- repo · https://raw.githubusercontent.com/cdisc-org/DataExchange-ODM/main/schema/ODM-foundation.xsd · ODM v2.0 foundation schema (Annotation, Flag, FlagValue, FlagType) · CDISC
- repo · https://raw.githubusercontent.com/cdisc-org/define-xml-2.1-stylesheets/master/cdisc-2019/examples/DefineXML-2-1-SDTM/defineV21-SDTM.xml · Define-XML v2.1 SDTM worked example (def:Origin Type/Source/DocumentRef) · CDISC
- dataset · https://api-evsrest.nci.nih.gov/api/v1/subset/ncit/C170449/members?include=minimal&pageSize=50 · NCIt C170449 CDISC Define-XML Origin Type Terminology · NCI EVS
- dataset · https://api-evsrest.nci.nih.gov/api/v1/subset/ncit/C170450/members?include=minimal&pageSize=50 · NCIt C170450 CDISC Define-XML Origin Source Terminology · NCI EVS
- paper · https://journals.sagepub.com/doi/full/10.1177/2168479014554400 · Evaluating Source Data Verification as a Quality Control Measure in Clinical Trials · Sheetz; Wilson; Benedict; Huffman; Lawton; Travers; Nadolny; Young; Given; Florin · TransCelerate BioPharma · Ther Innov Regul Sci 48(6) · 2014
- paper · https://pubmed.ncbi.nlm.nih.gov/25327707/ · Impact of source data verification on data quality in clinical trials · Andersen et al. · Br J Clin Pharmacol · 2015
- paper · https://pubmed.ncbi.nlm.nih.gov/36478289/ · Impact of monitoring approaches on data quality in clinical trials · Andersen et al. · Br J Clin Pharmacol · 2023
- paper · https://pubmed.ncbi.nlm.nih.gov/34878168/ · Monitoring strategies for clinical intervention studies · Klatte et al. · Cochrane Database Syst Rev · 2021
- paper · https://pubmed.ncbi.nlm.nih.gov/33258688/ · Clinical trial monitoring effectiveness: Remote risk-based monitoring versus on-site monitoring with 100% source data verification · Yamada; Chiu; Takata; Abe; Shoji; Kyotani; Endo; Shimada; Tamura; Yamaguchi · Clinical Trials · 2021
- paper · https://pubmed.ncbi.nlm.nih.gov/30236013/ · Extended Risk-Based Monitoring Model, On-Demand Query-Driven Source Data Verification, and Their Economic Impact on Clinical Trial Operations · Tantsyura; Dunn; Waters; Fendt; Kim; Viola; Mitchel · Ther Innov Regul Sci 50(1) · 2016
- paper · https://pubmed.ncbi.nlm.nih.gov/42348072/ · Quantifying the Financial Return on Investment of Risk-Based Quality Management Implementation in Clinical Development · Dirks et al. · Ther Innov Regul Sci · 2026
- paper · https://pubmed.ncbi.nlm.nih.gov/26729259/ · The impact of clinical trial monitoring approaches on data integrity and cost · Olsen et al. · Eur J Clin Pharmacol · 2016
- paper · https://aspe.hhs.gov/reports/examination-clinical-trial-costs-barriers-drug-development-0 · Examination of Clinical Trial Costs and Barriers for Drug Development · Sertkaya; Birkenbach; Berlind; Eyraud · Eastern Research Group for HHS/ASPE · 2014
- product · https://scdm.org/gcdmp/ · Good Clinical Data Management Practices (GCDMP) · Society for Clinical Data Management
- product · https://www.castoredc.com/pricing/ · Castor EDC pricing (no public prices published) · Castor
```

**[could not verify]:** EDC list price per study or per site (no vendor publishes); PMDA's Define-XML mandate from a PMDA primary source (only CDISC's assertion reached); named criminal prosecutions for clinical trial data falsification (DOJ search blocked this session).
