<!-- Persisted verbatim by research-leader from the factory-researcher's inline return (subagent file write was blocked; OBS-2: leader persists). Extracted mechanically from the agent's final message. -->
# mnstd-002 — findings W1: Intake (C3 #334)

- **Researcher:** factory-researcher. **Phase:** tech-discovery. **Date:** 2026-11-13.
- **Partition:** W1. The C3 done_when is read from node #334: C3.1 ≥2 reviewers, ≥2 MB/NC, ≥8 comments, all of ge/te/ed, one register. C3.2 every valid row gets a C2-resolved element id. C3.3 seeded invalid rows are rejected per row, the validator exits non-zero, and no seeded row enters the register. C3.4 merging gives no id collisions and keeps the reviewer.
- **Governed by:** N4 (ISO template field fidelity) and N5 (traceability). Every POC choice below must also respect N1 (one command), N2 (container only, no host Ruby), N3 (determinism) and N6 (no network beyond the image pull).
- **Evidence classes used here:**
  - **doc-claim:** a README or vendor documentation says it.
  - **source-read:** I read it in the code at a pinned commit.
  - **probe:** I measured it in a throwaway container under `/tmp/claude-1000/w1probe/`. A probe is a measurement, not proof, and nothing here moves a grade.

## 1. Verdict

**BUILD the validator and register as host glue (Python 3.14, matching the C2 resolver's language). ASSEMBLE only the vocabulary:**
- the ISO 2012-03 template's eight columns,
- `commenter`'s YAML field names,
- `commenter`'s `{MB}-{org}-{seq}` id pattern.

`commenter` is **not** on the gated path. It may run as an ungated, in-container cross-check (`commenter validate`) and as the W4 DOCX stretch (`commenter fill`).

**Determining constraint:** anchor-vs-document validation. No assemble candidate does it except ISO's own online (OSD) platform, which is out of scope. That check *is* C3.2/C3.3, so it must be built, and it is a thin caller of the C2 resolver. **If C2 fails, C3.2 and the anchor rows of C3.3 are BLOCKED.** The structural rows (type `xx`, missing field, duplicate id) remain evaluable.

Why `commenter` stays off the gated path (each point carries its evidence class):

| # | Gap vs C3/N-clauses | Evidence |
|---|---|---|
| G1 | **No anchor-vs-document check at all.** `validate` checks version, stage, id present, comment text present, duplicate ids and type (as a warning). Locality is never inspected. | source-read `lib/commenter/sheet_validator.rb` @ `b1758ce`; probe: `clause: '9.9'` and `element: 'Table 7'` passed silently |
| G2 | **Missing MB/NC (`body`) is not detected.** C3.3 names a missing MB/NC as a required seeded case. | probe: row GB-013 with no `body` produced no message |
| G3 | **Type `xx` is only a WARNING.** The non-zero exit comes from a quirk: `validate` raises whenever *any* problem exists, and printed "0 error(s) found" while exiting 1. | source-read `cli.rb` L90–105; probe `typeonly.yaml` exit=1 with "0 error(s)" |
| G4 | **The bundled JSON Schema is not enforced.** It is an editor hint (`# yaml-language-server: $schema=…`). No JSON-Schema library is in the gemspec deps, so the `required`, `pattern` and `enum` rules in `schema/iso_comment_2012-03.yaml` never run. | source-read gemspec, `comment_sheet.rb` L37–38, grep of `lib/` for a schema validator (none) |
| G5 | **Type codes are rewritten.** On load/serialize `te` becomes `technical` (`CommentType.full_name`). This breaks N4.2 (vocabulary exactly `ge`/`te`/`ed`) unless it is mapped back. | probe: `merge` output `type: technical`; source-read `comment.rb` `type_from_yaml` |
| G6 | **`merge` is all-or-nothing.** A conflicting duplicate id raises and writes nothing, with no per-row reasons and no partial register. Identical duplicates are silently deduped. C3.3 needs per-row rejection while valid rows still flow. | probe: exit 1, no `m.yaml`; source-read `ballot.rb` `deduplicate` |
| G7 | **Extension fields would be dropped.** Our fields (`resolved_id`, `reviewer`, `channel`, `source`) are not lutaml-model attributes, so a register round-tripped through `commenter` would lose them. Not probed. | source-read `comment.rb` (only mapped attributes serialize) |
| G8 | **Not in the image, and installing it needs the network.** `gem install commenter -v 0.7.0` pulled 5 gems from rubygems.org. That is runtime network beyond the image pull, which breaches N6.1. A derived image breaks N2.1's "pinned by digest" for the compile image. Vendored `.gem` files are tarballs, which breaches N7.2. | probe (see §4) |
| G9 | **Bundler-locked image.** `RUBYOPT=-rbundler/setup` and `BUNDLE_GEMFILE=/setup/Gemfile` make a freshly installed `commenter` fail with `Gem::Exception … not currently included in the bundle` until `BUNDLE_GEMFILE`, `BUNDLE_APP_CONFIG` and `RUBYOPT` are unset. | probe |

What we **reuse** from `commenter`: the field names (`id`, `body`, `locality.{line_number,clause,element}`, `type`, `comments`, `proposed_change`, `observations`) and the id regex `^[A-Z*]{2,3}-\d{2,3}(-\d{3})?$`. We also keep the register **projectable** to commenter-shaped YAML, so that `commenter validate`, `stats` and `fill` can be pointed at it (W4 stretch) without a translation layer.

## 2. Candidate landscape (ranked)

| Rank | Candidate | Role | State | Fit |
|---|---|---|---|---|
| 1 | **Custom validator + register (Python 3.14 stdlib `csv`/`json`, with an optional pinned YAML emitter) calling the C2 resolver** | gated intake | to build | Only option that does C3.2/C3.3 anchor checks with per-row reasons, exact ge/te/ed, deterministic output, and no network. |
| 2 | `metanorma/commenter` 0.7.0 (Ribose) | schema vocabulary; ungated cross-check; DOCX `fill` stretch (W4) | active. Repo created 2025-06-03; v0.7.0 tagged/released 2026-09-08; `validate` was added the same day (`a190b4b`); 1 star; 0 open issues; rubygems lists 430 downloads of 0.7.0. | Structural only (G1–G9). |
| 3 | ISO OSD comment import (ISO online platform) | the precedent for anchor validation | proprietary, online | Out of scope (no external services, no real ISO process). Its rules are the best spec for *what* to validate (§3.3). |
| 4 | ISO Comment Collation Tool (CCT) | collation | Word macros; doc-claim: no macOS, no 64-bit Office (JSA mirror) | Unusable on this host. It merges and sorts by clause and does not check anchors. |
| 5 | Generic DOCX comment parsers (e.g. `docx-comment-parser` on PyPI) | — | — | Wrong object: they read Word balloon comments, while ISO comments are table rows. Rejected. |
| — | `metanorma-tools` "comment management (planned — integrating commenter)" | — | doc-claim: planned | Not a candidate. The page was unreachable (HTTP 521); I saw only the search snippet. |

## 3. Register schema (N4 mapping)

### 3.1 ISO template columns (corroborated)

Source of truth: the 2012-03 template, whose footer reads "ISO/IEC/CEN/CENELEC electronic balloting commenting template/version 2012-03".
- **Column order:** I read it from `header2.xml` of the DOCX bundled in `commenter` at `data/iso_comment_template_2012-03.docx`.
- **Corroborated by:** the ISO Helpdesk "Commenting template guidelines" page (updated 2026-07-29) and the ANSI-hosted copy of the template.
- **Header block:** `Date`, `Document`, `Project`.
- **Footnote 1:** MB = Member body / NC = National Committee, entered as the ISO 3166 two-letter code. `**` marks the ISO/CS editing unit.
- **Footnote 2:** ge = general, te = technical, ed = editorial.

The bundled DOCX also carries an older FORM 13B (2001-09) header. It has 7 columns ("Clause/Subclause/Annex/Figure/Table", "Paragraph/List item/Note") with the footnote "Columns 1, 2, 4, 5 are compulsory". **Use 2012-03, not 13B.**

| # | ISO 2012-03 column | ISO mandatory? (Helpdesk 299) | Sheet CSV header | commenter YAML key | Register field | Notes |
|---|---|---|---|---|---|---|
| 1 | MB/NC | yes | `mb` | `body` | `mb` | `^([A-Z]{2}\|\*\*)$`. Also used as the id prefix. |
| 2 | Line number | no | `line` | `locality.line_number` | `line` | Q3: optional and informational. ISO Helpdesk: "rarely shown in ISO documents and are not used for sorting." |
| 3 | Clause/Subclause | yes | `clause` | `locality.clause` | `clause` | Number only. No "cl."/"Clause" prefix (CEN rule). For whole-document comments, see §3.3 R5. |
| 4 | Paragraph/Figure/Table/(Note) | no | `element` | `locality.element` | `element` | Uses document-wide numbering (ISO 659), e.g. `Table 1`, `Table B.6`, `Figure 3 a)`, `Note 4`, `Table 4 Note 1`. |
| 5 | Type of comment | yes | `type` | `type` (commenter expands it; we do not) | `type` | Exactly `ge`\|`te`\|`ed` (N4.2). |
| 6 | Comments | yes | `comment` | `comments` | `comment` | Non-empty after trim. |
| 7 | Proposed change | no | `proposed_change` | `proposed_change` | `proposed_change` | May be empty. |
| 8 | Observations of the secretariat | n/a (left empty by commenters) | `observations` | `observations` | `observations` | Must be **empty at intake** (CEN rule 4). Filled by W2 (disposition plus observation). |

**Renames are documented, not silent (N4.1):** `body`→`mb` and `comments`→`comment`. Alternatively, keep the commenter keys verbatim. Either choice satisfies N4.1 because this table is the documented mapping. The POC must copy the table into the run report.

### 3.2 Added register fields (additions, not renames)

| Field | Content |
|---|---|
| `id` | Register id `{MB}-{RR}-{NNN}`, where `RR` is the reviewer ordinal within that MB (2 digits) and `NNN` is the reviewer's row sequence (3 digits). This matches commenter's `DE-01-002` pattern, so ids stay commenter-compatible. |
| `source_id` | The id as the reviewer wrote it (e.g. `GB-001`), or empty. |
| `reviewer` | Reviewer handle from the sheet header (C3.4 "originating reviewer preserved"). |
| `channel` | `sheet` \| `pr` (Q2: one register; C4 writes `pr`). |
| `source` | `sheets/gb-alice.csv:7` for sheets; `{commit}:{file}:{line}` for the PR channel. |
| `locator` | The original locator, verbatim (`clause` + `element` + `line`). C3.2 requires it **next to** the resolved id. |
| `resolved_id` | Element id from the C2 resolver (v1 semantic XML). |
| `resolved_number` | Clause number the resolver confirms (useful for C2.4 renumbering). |
| `disposition` | Empty at intake. Owned by W2 (`accept\|modify\|reject`). |

**Sheet header** (CSV leading `#key: value` lines, or YAML top level): `version: 2012-03`, `document`, `date`, `project`, `reviewer`, `mb`.

### 3.3 Validation rules (validator design)

Each rule emits a stable reason code. **All rules run on every row**: collect every reason, do not stop at the first failure.

| Code | Rule | C3.3 case |
|---|---|---|
| S0 (sheet) | Header columns equal the expected list, in order. `version == 2012-03`. Sheet `document` equals the v1 docidentifier, read from the semantic XML. A violation rejects the whole sheet and exits 2. | structure-unaltered (N4.3 analogue) |
| R1 `missing_field` | `mb`, `clause`, `type`, `comment` are non-empty. | missing comment text / MB |
| R2 `bad_mb` | `mb` matches `^([A-Z]{2}\|\*\*)$` and equals the sheet-header `mb`. | — |
| R3 `bad_type` | `type ∈ {ge,te,ed}`, exact and lowercase. Full words are **rejected**, not normalized, to keep N4.2 literal. | type `xx` |
| R4 `bad_id` / `duplicate_id` | `source_id` (if given) matches the pattern. The derived register id is unique. On a duplicate, the **first in deterministic order wins**: sheets sorted by path, then by row. Later rows are rejected with `duplicate_id (first: <source>)`. Identical duplicates are rejected too (unlike commenter's silent dedupe), because ISO says one comment per row. | duplicate id |
| R5 `clause_not_found` / `clause_ambiguous` | `resolve(clause)` returns exactly one element. The resolver's reason is passed through verbatim. Whole-document comments use `clause: General`, which the resolver maps to the document root. The convention is a **W0/C2 decision**: ISO 659 says "General"-type plus an empty clause; CEN says "General"; commenter's example uses `_whole document`. | non-existent clause |
| R6 `element_not_found` / `element_ambiguous` | If `element` is non-empty, `resolve(clause, element)` returns exactly one element. Numbering is document-wide (ISO 659). | unresolvable element locator |
| R7 `bad_line` | `line`, if present, is a positive integer. It is not resolved against the output (Q3) unless W0 finds draft line numbering. | — |
| R8 `observations_not_empty` | `observations` is empty at intake. | — |

**Outputs:**
- `register.yaml` and `register.csv`: accepted rows only, ISO column order first and then the added fields, sorted by `id`. No timestamps (N3.1).
- `rejects.csv`: `source`, `source_id`, the list of reason codes, and the resolver message.

**Exit codes:** 0 when all rows are accepted, 1 when any row is rejected, 2 on a sheet-level or structural error or a missing prerequisite (N1.3).

**Interface to C2:** call it in-process (`from resolver import resolve`) and **do not shell out** to it, which keeps it deterministic and fast. The contract is `resolve(clause:str, element:str|None) -> Ok(id, number) | Err(code, message)`. The C4 PR channel calls `resolve_line(file, line)` (C2.2) and then the same R1–R8 pipeline with `channel: pr`, so "rejected exactly like C3.3" holds by construction: **one validator, two adapters.**

**C3.4 collision-freedom:**
- Ids are minted by the merger. Reviewer-supplied ids are kept only as `source_id`.
- Two reviewers from the **same** MB who both number from `GB-001` become `GB-01-001` and `GB-02-001`.
- The fixture must include this case. ≥2 distinct MBs alone would make collision-freedom trivially true.

## 4. Probe log (measurements, not proof)

All runs used `metanorma/metanorma@sha256:836b7ab2…dff3da`, `docker run --rm`, with a scratch dir under `/tmp/claude-1000/w1probe/`.

| Probe | Observation |
|---|---|
| Image Ruby | `ruby 4.0.7`. Gems: `metanorma 2.5.24`, `metanorma-cli 1.18.6`, `metanorma-iso 3.5.14`, `thor 1.5.0`. **`commenter` not installed.** |
| Image env | `ENTRYPOINT` null, `CMD ["metanorma"]`, `WORKDIR /metanorma`. `RUBYOPT=-rbundler/setup`, `BUNDLE_GEMFILE=/setup/Gemfile`. In `bash -lc`, `metanorma: command not found` (the login shell resets PATH). **Flag for W0:** invoke as `docker run IMG metanorma …` or plain `bash -c`, never `bash -lc`. |
| Install | `gem install commenter -v 0.7.0` succeeded; it needs network (5 gems including `octokit`, `docx`, `dotenv`). It runs only with the bundler vars unset. |
| `validate` valid sheet | exit 0, "OK: 1 comments". |
| `validate` 6-row invalid sheet | exit 1. Reported: WARNING type `xx`; ERROR missing comment text; ERROR duplicate id. **Not reported:** clause `9.9`, element `Table 7`, missing `body`. |
| `validate` with only type `xx` | exit 1 with "0 error(s) found" (G3 quirk). |
| `merge` with a conflicting id | exit 1, `Duplicate comment IDs with differing content: GB-001`, no output file. |
| `merge` of an identical sheet twice | exit 0, deduped to 1, `type: te` → `technical`. |

## 5. POC guidance (for factory-poc)

**Layout:**
- `poc/intake/sheets/` holds valid sheets.
- `poc/intake/fixtures/invalid.csv` holds the seeded fixture.
- `poc/intake/intake.py` is the CLI. It imports the C2 resolver module.
- The only dependency is a pinned YAML emitter (`PyYAML==<pin>`), or emit YAML by hand. Use stdlib `csv`.

**Valid sheets (C3.1/C3.4):** ≥3 sheets and ≥9 rows.

| Sheet | Reviewer | MB | Rows |
|---|---|---|---|
| `gb-alice.csv` | alice | GB | GB-001 ge `General`; GB-002 te `5.2`/`para 2`; GB-003 ed `6`/`Table 1`; GB-004 te `A.1` (annex) |
| `gb-bob.csv` | bob | GB | GB-001 te `4`/`Note 1`, a deliberate local-id clash with alice; GB-002 ed `3.1` |
| `fr-claire.csv` | claire | FR | FR-001 te `6`/`Figure 1`; FR-002 ed `5.1`/`para 1`; FR-003 ge `1` |

Expected register: 9 rows; ids `GB-01-001…004`, `GB-02-001…002`, `FR-01-001…003`; all three types; MBs {GB, FR}.

**Seeded invalid fixture (C3.3):** one sheet, MB `DE`, run *together with* the valid sheets.

| Row | Seed | Expected reason |
|---|---|---|
| I1 | `clause: 9.9` | `clause_not_found` |
| I2 | `5.2` / `Table 7` (when 2 tables exist) | `element_not_found` |
| I3 | `type: xx` | `bad_type` |
| I4 | empty `comment` | `missing_field:comment` |
| I5 | empty `mb` | `missing_field:mb` |
| I6 | `source_id` equal to an earlier row in the same sheet (I1's id) | `duplicate_id` |
| I7 (recommended) | `element: para` with no number in a multi-paragraph clause | `element_ambiguous` |
| I8 (recommended) | `clause: cl. 5` | `clause_not_found`, or a prefix-specific reason |
| I9 (recommended) | `type: technical` | `bad_type` (N4.2 exactness) |
| I10 (recommended) | pre-filled `observations` | `observations_not_empty` |

Rows I1–I6 are the five named cases, with the missing-required-field case covered twice (comment and MB).

**Observable / check recipe:**
1. `intake sheets/*.csv` exits 0 and writes `register.A`.
2. `intake sheets/*.csv fixtures/invalid.csv` exits 1 and writes `register.B` plus `rejects.csv`.
3. Assert: `diff register.A register.B` is empty (no seeded row entered). `rejects.csv` has exactly the fixture rows, each with its expected reason code; compare against a committed `fixtures/invalid.expected.csv`. Every register row has a non-empty `resolved_id` next to its `locator`. The ids are unique. `reviewer` is present.
4. Run twice and compare bytes for N3.1.

**Ungated cross-check (optional, label as such):** run `commenter validate` on a commenter-shaped projection of the register inside the pinned image with the bundler vars unset. This is only possible if the N6.1/N7.2 cost of getting the gem in is accepted, and that decision belongs to the leader. **Recommendation: skip it in the gated `make demo`.**

## 6. Flags

- **C2 dependency.** R5/R6 and C3.2 are BLOCKED if the resolver fails. The `General` / Introduction / annex locator conventions and the "para N" convention are **resolver (W0) decisions**. ISO numbers tables, figures and notes but not paragraphs. "para N" is our convention; ISO 659 gives no paragraph example.
- **N6.1 vs `commenter`.** Any in-run `gem install` is network access beyond the image pull. A derived Dockerfile moves the compile pin away from the digest. Both are leader calls; my recommendation is to keep `commenter` off the gated path.
- **License ambiguity.** The gemspec says `BSD-2-Clause`. The repo has no LICENSE file, and the GitHub API reports `license: null`. This does not matter if we only reuse field names and the regex.
- **`validate` is very new** (added 2026-09-08, the day of the 0.7.0 release). Its behaviour may change. Pin `0.7.0` if it is used at all.
- **Mandatory-column disagreement.** FORM 13B says columns 1, 2, 4, 5. ISO Helpdesk 299 says MB, Clause, Type, Comment. CEN says MB, Clause, Type, Comment. I follow the 2012-03 / Helpdesk set.
- **Not verified:** the OSD XLSX export column layout (out of scope); `metanorma-tools` status (page returned HTTP 521).

## 7. Coverage log (K = 3, N = 2)

| # | Query / surface | New candidate or mechanism? |
|---|---|---|
| 1 | GitHub `metanorma/commenter` README (fetch) + source clone @ `b1758ce` + rubygems API | yes: commenter 0.7.0 (baseline) |
| 2 | web: "ISO/IEC/CEN/CENELEC … template 2012-03 columns …" | no tool; template columns (mechanism: schema) |
| 3 | fetch: CEN BOSS "Use of the Commenting Form" | no tool; rules corroborated |
| 4 | web: "metanorma commenter gem … validate merge" | no new candidate; `metanorma-tools` (planned only) |
| 5 | web: "open source tool validate ISO ballot comment sheet against draft clause numbers …" | yes: ISO CCT (proprietary Word macros; rejected) and ISO OSD import validation (precedent; out of scope) |
| 6 | fetch: ISO Helpdesk 299 | no; corroborates the columns |
| 7 | web: "github python ISO commenting template docx parse …" | **no** (dry 1) |
| 8 | web: "metanorma ISO comment resolution workflow GitHub … AsciiDoc review tooling" | **no** (dry 2) |
| 9 | web: "ISO OSD comments export xlsx open source converter clause anchored comment register validation" | **no** new candidate (dry 3); OSD anchor rules gave the validation-rule spec |
| 10 | fetch: ISO Helpdesk 659 | no; corroborates the element-locator rules |

**K = 3 met** (queries 7–9 were consecutive and dry). The workstream closes on a **build** verdict, as SCOPE allows.

**N ≥ 2 per mechanism:**

| Mechanism | Corroborating sources |
|---|---|
| ISO column set and order | commenter's bundled DOCX (read by us) + ISO Helpdesk 299 + CEN BOSS + ANSI template copy |
| Type vocabulary ge/te/ed | template footnote + ISO 299 + CEN |
| One comment per row; no structural change | ISO 299 + CEN |
| Anchor validation must match document numbering | ISO 659 + ISO OSD best-practices search result (same org, so 1 independent org; marked) |
| commenter gaps G1–G6 | source-read + probe (2 independent methods) |

## 8. Citations (D14)

```yaml
- type: repo
  ref: github.com/metanorma/commenter
  title: commenter — Library to work with ISO comment sheets in DOCX and XLSX formats
  author: Tse
  org: Ribose
  year: 2026
  surface: active-dev
- type: product
  ref: https://rubygems.org/gems/commenter/versions/0.7.0
  title: commenter 0.7.0 (rubygems)
  org: Ribose
  year: 2026
  surface: products
- type: docs
  ref: https://helpdesk-docs.iso.org/article/299-commenting-template-guidelines
  title: Commenting template guidelines
  org: ISO
  year: 2026
  surface: products
- type: docs
  ref: https://helpdesk-docs.iso.org/article/659-upload-experts-comments-from-iso-iec-commenting-template
  title: Upload and submit experts comments from ISO/IEC commenting template
  org: ISO
  year: 2026
  surface: products
- type: docs
  ref: https://boss.cen.eu/reference-material/Guidancedoc/Pages/GD-ComForm
  title: Use of the Commenting Form
  org: CEN
  year: 2019
  surface: products
- type: standard
  ref: https://share.ansi.org/ISOT/ISOT Voting Resources/ISO Commenting Template.doc
  title: Template for comments and secretariat observations (ISO/IEC/CEN/CENELEC electronic balloting commenting template, version 2012-03)
  org: ISO
  surface: products
- type: docs
  ref: https://helpdesk-docs.iso.org/article/316-comment-collation-tool-cct
  title: Comment Collation Tool (CCT)
  org: ISO
  surface: products
- type: docs
  ref: https://www.rubydoc.info/gems/metanorma-tools
  title: metanorma-tools (README; comment management listed as planned)
  org: Metanorma
  surface: products
```

Notes on the citations:
- The `author: Tse` on the commenter repo is from the commit authorship of the `validate` commits. The gemspec author is "Ribose".
- The CCT and `metanorma-tools` entries were seen only via search snippets. The `metanorma-tools` page fetch failed with HTTP 521, so both are doc-claim at most.
