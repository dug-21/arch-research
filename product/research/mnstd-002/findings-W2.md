<!-- Persisted verbatim by research-leader from the factory-researcher's inline return (subagent file write was blocked; OBS-2: leader persists). Extracted mechanically from the agent's final message. -->
# findings-W2 — Resolution (C5 #333): dispositions, scripted edits, trace, N3 normalization

**Scope:** mnstd-002 · **Workstream:** W2 · **Capability:** C5 #333 (`grade:missing`) · **NFRs touched:** N3 #339,
N5 #341 (trace), N4 #340 (observations field) · **Author:** `factory-researcher` · **Date:** 2026-11-13
**Evidence classes:** `doc-claim` (vendor or standards text we did not run) · `source` (read in the pinned image's
installed gem source, i.e. what the pinned build *should* do) · `probe` (a lightweight measurement we ran in
`/tmp`, image digest `sha256:836b7ab2…dff3da`, x86_64, `--network none`). Probes are measurements, **not proof**,
and nothing here moves a grade.

**Pinned toolchain observed in the image (probe):** Metanorma 2.5.24 · metanorma-cli 1.18.6 · metanorma-standoc
3.5.20 · metanorma-iso 3.5.14 · isodoc 3.7.14 · metanorma-utils 2.0.12 · asciidoctor 2.0.26 · canon 0.3.125 ·
mn2pdf 2.74. **`commenter` is NOT installed in the image** (`gem list` shows no `commenter`). For W1 this means
assembling `commenter` N2-cleanly needs a derived image, which is a new pin.

---

## 0. Headline verdicts

| Mechanism (C5 clause) | Verdict | Determining fact |
|---|---|---|
| Disposition record (C5.1) | **Build** a thin YAML schema; **assemble the vocabulary and labels** from the ISO template and `commenter` conventions | ISO puts the decision in one free-text column, *Observations of the secretariat*. No tool supplies a 3-value enum plus a mandatory observation |
| Edit application (C5.2, N3.2) | **Build**: exact-match find/replace operations, one commit per comment id, fixed git identity and dates | No maintained lossless AsciiDoc editor exists for Node or Python. Metanorma has no "apply comment" feature |
| Diff attribution (C5.2) | **Assemble from git**: `Comment-Id:` trailers, `git log --format=%(trailers…)` and range checks | Native git. A probe showed deterministic commit hashes |
| v2 containment (C5.3) | **Build** on C2.4 plus a text normalizer over the semantic XML | Semantic XML auto-ids are hashes of content and position, so they change on edit or insert. Text is typographically rewritten |
| Trace table (C5.4) | **Build** (CSV + YAML, sorted, LF line endings) | — |
| Native change record in v2 (optional; strengthens C5.2/N5) | **Assemble**: Metanorma *Document History* (YAML in `metanorma-extension` → `bibdata/relation[@type=updatedBy]/bibitem/amend`) | Probe shows it lands in the semantic XML. ISO HTML does not render it |
| Visible redline (optional, not gated) | **Assemble**: `add:[…]` / `del:[…]` inline macros → `<add>/<del>` → HTML `span.addition/.deletion` | Probe-confirmed. But it *modifies the source*: use it only in a derived "redline" build, never in the v2 source, or it breaks C5.2 attribution and C5.3 containment |
| N3 determinism (v2 semantic XML) | **Byte-identical without normalization** in a same-day probe, *if* the date-bearing attributes are pinned. Declare a short defensive list | See §6 |

**Determining constraint for W2:** C5.3 depends on **C2.4** (the v1→v2 element mapping). In the probe, a v2 that
inserted one clause changed 16 of 54 v1 ids, so auto-ids are NOT stable and C5.3 cannot assume "same id in v2".
If C2.4 is BLOCKED, C5.3 and the v2 column of C5.4 are BLOCKED too (the scope's dependency rule).

---

## 1. How ISO practice records dispositions (the observations of the secretariat)

- The ISO commenting template has eight columns: MB/NC, Line number, Clause/Subclause, Paragraph/Figure/Table,
  Type of comment, Comments, Proposed change, **Observations of the secretariat**. Commenters leave the last
  column "**empty**"; it is "Used by the Secretariat to indicate the decision taken on each submitted comment."
  One comment per row, and "The commenting template should not be modified in any way." — **doc-claim** [C1].
- ISO's current tooling (OSD) offers five resolution types: **accepted, partially accepted, not accepted, noted,
  deferred**. A motivation is optional only for *noted* — **doc-claim** [C2]. So current ISO practice records
  (a) a categorical status plus (b) a motivation, and the template folds both into one text cell.
- Historical committee practice writes free-text labels ("Accepted", "Accepted in principle", "Noted",
  "Rejected") at the head of the observation — **doc-claim / user-report** (committee documents surfaced in
  search, e.g. [C3]). The vocabulary varies between committees, and I found no single normative definition.
- `metanorma/commenter` follows the same model — **doc-claim** [C4]:
  - `observations` is a free-text field ("Secretariat observations (optional)").
  - `stats` derives the disposition by *pattern-matching the observation text* into Accepted, AWM ("Accepted with
    modifications"), Noted, Rejected (`reject(ed)?|not accepted`) or TODO.
  - The OSD import has a separate `resolution_status` field and "builds" observations from
    `resolution_status + motivation`.

**Recommended mapping.** Q7 fixes `accept|modify|reject`. Map these to the ISO and `commenter` labels, so the
register's ISO `observations` column stays faithful and `commenter stats` can still read it:

| Q7 disposition | ISO OSD resolution | commenter label (observation prefix) |
|---|---|---|
| `accept` | accepted | `Accepted.` |
| `modify` | partially accepted (≈ "accepted with modifications" / "in principle") | `Accepted with modifications.` |
| `reject` | not accepted | `Rejected.` |

**Flag (Q7 is settled; this only names the gap):** ISO practice also has `noted` and `deferred`, commonly used
for `ge` comments that need no text change. Under Q7, a fixture `ge` comment must be forced into
accept/modify/reject, and `reject` (no source change) is the honest fit for "noted". Record this mapping in the
run report rather than making the choice silently.

## 2. Disposition record schema (C5.1) — build

Keep the secretariat's decisions in a separate **authored input**, `dispositions.yaml`. A deterministic merge
folds it into the register to produce the resolved register that C7 reads. C7.1 says the report is "generated from
the register only", so the merge result *is* the register of record. Keeping intake output and disposition input
in separate files keeps N5.2 and C3 checkable.

```yaml
# dispositions.yaml — one record per register comment id, no others
- id: DE-001                 # must exist in register (N5.2); exactly once (C5.1)
  disposition: accept        # accept|modify|reject — exact enum (Q7)
  observation: "Rewording adopted as proposed."   # non-empty, required for all three
  edits:                     # REQUIRED and non-empty for accept/modify; FORBIDDEN for reject
    - file: sections/05-general.adoc
      find: "Second para."   # literal; must occur exactly once in file at apply time
      replace: "Second para, reworded."
  expect_in_v2: "Second para, reworded."   # accept: MUST equal register.proposed_change (C5.3)
                                           # modify: the recorded modified text (C5.3)
- id: GB-003
  disposition: modify
  observation: "Accepted in principle; wording aligned with clause 3 terms."
  modified_text: "widget grip force"
  edits: [{file: sections/05-general.adoc, find: "grip strength", replace: "widget grip force"}]
  expect_in_v2: "widget grip force"
- id: FR-002
  disposition: reject
  observation: "Out of scope of this document."
```

**Validator rules** (fail fast, exit non-zero on any violation):
- The set of ids equals the set of register ids.
- `disposition` is exactly one of the three enum values, and `observation` is non-empty.
- `accept` ⇒ `edits` present, and `expect_in_v2 == proposed_change` (string-equal after the §5 normalizer).
- `modify` ⇒ `modified_text` present, and `expect_in_v2 == modified_text`.
- `reject` ⇒ no `edits`.
- The fixture has at least one of each disposition, and at least one comment from each channel if C4 is present
  (C5.1).

**Key design point:** an ISO `proposed_change` is often prose ("Replace X by Y"), yet C5.3 checks containment
*against `proposed_change`*. So the **fixture's accepted comments must carry literal replacement text** in
`proposed_change`. The `edits` operation is the machine instruction, and `expect_in_v2` ties it back to the ISO
field. Do not try to parse prose proposals: that is the agent path Q4 keeps out of the gate.

**Merge into the register:** add `disposition` (a new field, documented as an N4 extension) and set
`observations` (the ISO column) to `"<label>. <observation>"` using the §1 table. The trace step fills `commit` and
the `v2_*` columns later.

## 3. Edit application (C5.2, Q4, N3.2) — ranked

| Rank | Mechanism | Verdict | Notes |
|---|---|---|---|
| **1** | **Literal find/replace operations** (Python 3.14 stdlib or Node 24, no dependencies). Applied in sorted comment-id order, asserting each match is unique (`count == 1`), one commit per comment id | **Build — recommended** | Deterministic by construction, with the same semantics as common "exact unique string replace" editors. Failure is loud: zero or several matches exits non-zero, naming the id. To insert a new clause, `find` an anchor line and `replace` it with that line plus the new block |
| 2 | Per-comment unified diffs applied with `git apply` (`--check` first) | Assemble (git) | Deterministic, but patches are bound to line context and earlier edits shift it. Writing patches for the fixture is more work than find/replace and no stronger. Acceptable fallback |
| 3 | AST-level edit (Asciidoctor Ruby API inside the container) | Build, heavier | Asciidoctor has an AST but no lossless writer. Re-serialising AsciiDoc would reformat untouched lines and violate "no unattributed change". Rejected. No lossless AsciiDoc editor was found for Python or Node (§8) |
| 4 | Metanorma ISO amendment blocks (`[change=modify]`, `amend.rb`) | Not applicable | These model an *Amendment document* that describes changes to a base standard, not edits to the base source |
| — | Agent-applied edits | Out of gate (Q4) | May be shown, not ruled |

**Recipe for rank 1** (every step deterministic, N3.2):
```
git -C work tag v1                                  # v1 = the compiled baseline commit
for id in $(sorted accept/modify ids):              # lexical sort of comment id
  apply edits[id] (assert each find occurs exactly once, else exit 2 "id: find not unique/absent")
  git add -A
  GIT_AUTHOR_NAME=secretariat GIT_AUTHOR_EMAIL=secretariat@example.invalid \
  GIT_COMMITTER_NAME=… GIT_COMMITTER_EMAIL=… \
  GIT_AUTHOR_DATE=2026-01-01T00:00:00Z GIT_COMMITTER_DATE=2026-01-01T00:00:00Z \
  git -c commit.gpgsign=false commit -m "Resolve $id ($disp)" --trailer "Comment-Id: $id"
git tag v2
```

**Probe (measurement):** two independent repos committed the same tree with fixed author and committer names,
emails and dates, and both produced the **same commit hash** (`0d4c47f6…`).
`git log --format='%(trailers:key=Comment-Id,valueonly)'` returned the id. So commit hashes can appear in the
trace table without breaking N3.1, **but only if every commit uses fixed identities and dates, including the C4
merge commits and the v1 baseline.** One commit with a live timestamp upstream changes every hash after it.

**Conflict policy:** if two comments edit the same span, the second `find` fails. Either design the fixture so the
spans are disjoint, or write the later comment's `find` against the post-edit text (the order is fixed, so this
stays deterministic). State the policy in the run report.

## 4. Diff-attribution check (C5.2) — assemble from git

Every step is mechanical and uses git history only (it also serves N5.1):
1. Every commit in `git rev-list --no-merges v1..v2` has at least one `Comment-Id` trailer
   (`git log --format='%H %(trailers:key=Comment-Id,valueonly,separator=%x2C)'`), and every trailer id is in the
   register.
2. Every `accept`/`modify` id appears in **exactly one** commit. For PR-channel comments it appears in the merge
   commit instead (C4.4): read merges with `--merges` and require the trailer there. Every `reject` id appears in
   **no** commit.
3. No unattributed change. Since step 1 shows that `v1..v2` contains only attributed commits, the cumulative diff
   `git diff v1 v2` is the composition of attributed commits. Strengthen this with a per-commit scope check: for
   each commit, `git diff --unified=0 C^ C` may touch only lines covered by that comment's `edits` (the `replace`
   text on the `+` side, the `find` text on the `-` side). This catches a stray edit smuggled into an attributed
   commit.
4. Optional belt-and-braces: in `git blame --line-porcelain v2 -- <file>`, every line not from the v1 boundary maps
   to a commit whose trailer is an accept/modify id.

**Recommended negative fixture:** a commit that edits one line beyond its `edits`. Step 3 must flag it.

## 5. v2 containment check (C5.3) — build on C2.4

**Per accept/modify comment:**
1. Take the register's v1 `resolved_id` and map it to the v2 element via **C2.4**.
2. Extract that element's text from the **v2 semantic XML** (`itertext()` over the element) and normalize it.
3. Assert that `normalize(expect_in_v2)` is a substring. For a deletion, assert that `normalize(find)` is absent.

A comment that *inserts* a new clause has no v1 counterpart in v2. Resolve it by searching v2 for the inserted
text, require exactly one match, and record the v1 element as the insertion anchor.

The check must handle two facts (both **probe** unless marked):

**Auto ids are hashes of content and position, not random.**
- `contenthash_id_make` replaces every GUID id with `MD5("#{elem.path}////#{elem.text}")`, formatted as a UUID
  (`metanorma-standoc cleanup/inline.rb`, `metanorma-utils utils/anchor.rb#contenthash`) — **source**.
- So ids are stable run-to-run for identical input: in the probe, the semantic XML was byte-identical across two
  runs.
- But an id **changes when the element's text changes or its XPath position shifts**. The probe v2 inserted one
  clause before `General` and reworded one paragraph: 38 of 54 v1 ids survived and 16 changed. The clause anchored
  by the author as `[[cl-req]]` got a new `id` but kept `anchor="cl-req"`.
- Therefore C5.3 **must** go through C2.4. C2.4's cheapest stable handle is the `anchor` attribute, where the
  author set one (W0 owns this; the flag is passed on).

**Typography is rewritten in the semantic XML.**
- The source `the widget's "grip" -- 5 mm...` became `the widget’s “grip” — 5 mm…\u200b`.
- Inline markup became `<sup>`, `<strong>` and `<tt>` child elements.
- Normalizer (declare it in the run report):
  - apply Unicode NFC;
  - map `’‘` → `'` and `“”` → `"`;
  - map `—` → `--`, collapsing the surrounding spaces;
  - map `…` → `...` and drop U+200B;
  - strip AsciiDoc inline markup from the expected string (`*x*`, `_x_`, `` `x` ``, `^x^`, `~x~`);
  - collapse whitespace.
- Cheaper alternative: write the fixture's `proposed_change` texts in plain ASCII words with no quotes, dashes or
  markup, and keep the normalizer as a defence.

## 6. N3 — determinism and the volatile-field list (v2 semantic XML; also register, trace and report)

**Probe:** the same source compiled twice (`metanorma compile --no-install-fonts -t iso -x xml,html`,
`--network none`, pinned digest).
- `d.xml`, `d.presentation.xml` and `d.err.html` were **byte-identical**.
- `d.html` differed **only** in random v4 UUID anchors (`_xxxxxxxx-xxxx-4xxx-…`), and was identical once those
  were replaced.
- Same-day only. Cross-day behaviour below is inferred from **source**.

The real cross-day risks are values the tools fill from the clock (`Date.today` call sites in the pinned gems):

| Field | Where | Fix (prefer pinning over normalizing) |
|---|---|---|
| `bibdata/copyright/from`, and every boilerplate id hashed from that text | `standoc front_contributor.rb:119` (`copyright-year`, else `Date.today.year`) | Set `:copyright-year:`. Probe: without it, `from` was 2026 from the clock |
| Year in the document identifier (`ISO/AWI 99999-1:2026`) | `iso front_id.rb:142`, falls back to `Date.today.year` | Set `:copyright-year:` / `:revdate:` |
| `bibdata/version`, `date[@type=updated]` | Taken from `:revdate:` (absent if unset) | Set `:revdate:` |
| Reviewer annotation `@date` | `standoc blocks_notes.rb:27` (the `date` attribute, else `Date.today`) | The C6 projection must always emit `date=` |
| ISO "Metadata warnings" annotation (`date=Date.today`, `reviewer="Metanorma"`) | `iso presentation_section.rb:31`, **presentation XML only**. Injected when secretariat, committee or document date is missing | **Probe: injected in our minimal document ("Secretariat is missing.").** Set `:secretariat:` and the committee attributes. It also **inflates the C6.2 annotation count** → passed to W4 |
| `schema-version` attributes | Tied to gem versions | Constant under the digest pin; list as image-bound |
| HTML random v4 ids, random image filenames | `isodoc html_function/postprocess.rb:121,134` | HTML is not in N3.1's gated set. If compared, normalize the v4-pattern ids |
| PDF | Not probed (mn2pdf likely embeds creation timestamps) | Keep PDF out of the N3 identity set. Unmeasured — flag |

Asciidoctor itself honours `SOURCE_DATE_EPOCH` (source: `asciidoctor/document.rb`, `cli/invoker.rb`). Metanorma's
own `Date.today` calls do **not** (no hits in standoc, iso, isodoc or cli). Set it anyway, since it is cheap, but
rely on the explicit attributes.

**Recommended declared N3 list for v2 semantic XML: empty by construction.** That holds when the source pins
`:revdate:`, `:copyright-year:`, `:secretariat:` and the committee attributes, and the image is pinned by digest.
Compare with `cmp`.

Declare a **defensive** normalization list anyway. Apply it only if `cmp` fails, and report each hit:
1. `//bibdata/copyright/from`
2. the year suffix of `//bibdata/docidentifier`
3. `//bibdata/date/on` and `//bibdata/version`
4. `annotation/@date`
5. any `@schema-version`

Do **not** normalize `@id` in the semantic XML. Ids are content hashes, so an id difference signals a real content
difference.

**Implementation:** Python stdlib `xml.etree` (no dependencies, so N2.3 holds). The in-image `canon diff --format
xml` is a second-choice cross-check (**source/help text**): it offers `--attribute-values ignore`,
`--text-content normalize` and match profiles, but these are global switches, not per-attribute, so it cannot
express the named list.

**Register, trace table and report** are deterministic without normalization, compared with `cmp`, if:
- inputs are sorted by comment id;
- git identity and dates are fixed (§3);
- YAML/CSV is emitted with fixed key order, LF line endings, UTF-8 and no timestamps.

## 7. Trace table (C5.4) — spec

Emit `trace.csv` and `trace.yaml`: one row per register comment, sorted by `id`. No cell may be blank except the v2
columns for `reject`.

| column | source |
|---|---|
| `id` | register |
| `channel` (`sheet`/`pr`) | register |
| `mb_nc`, `type` | register |
| `locator` (original ISO locator or `file:line`) | register |
| `v1_element_id`, `v1_anchor` (if any), `v1_clause` | register (`resolved_id`) + C2 |
| `disposition` | dispositions.yaml |
| `commit` (full hash; the merge commit's hash for the PR channel) | `git log` trailers |
| `v2_element_id`, `v2_clause` | C2.4 mapping / insertion search |
| `renumbered` (`old→new`, or `=`) | C2.4 |
| `containment` (`pass`/`n/a`) | §5 check |

Use the plain sentinel `n/a` (not a dash) in a reject's v2 cells, so "no blank cell" is mechanically checkable.

Optional native mirror: emit one Document-History `amend` entry per accepted or modified comment (below), so the
v2 XML itself carries the id → location trail.

**Native document history (assemble, optional).**
- **Syntax:** a `metanorma-extension` section placed **before the Foreword**, with a `=== Document History`
  subclause holding a YAML block (`date`, `edition`, `amend: {description, location, change, classification}`).
- **Output:** it becomes `bibdata/relation[@type="updatedBy"]/bibitem/{edition, date, amend[@change]/description,
  location/localityStack}` — **probe**-confirmed. Source: `cleanup/dochistory.rb`. The YAML model matches the
  README of Ribose's `revix` gem — **doc-claim** [C6].
- **Trap:** placed *after* the annex, the same block was silently treated as an ordinary preface clause
  (**probe**).
- **Not rendered** in ISO HTML.
- **Value for C5:** one `amend` entry per comment, with `classification: {tag: comment-id, value: DE-001}` and
  `location: clause=5`, gives a machine-readable trail *inside v2*.
- **Cost:** adding it is itself a source change. Make it the **last commit**, carrying every accept/modify id in
  its trailer, or the diff-attribution check (§4) will flag it.

## 8. Coverage log (K = 3, N = 2)

**Searches and reads, in order:**
- `commenter` README (two fetches)
- ISO comment-resolution vocabulary
- ISO helpdesk "Resolve comments"
- ISO helpdesk "Commenting template guidelines"
- ISO Directives Part 1 (fetch returned 403; not read)
- Metanorma document-history docs (metanorma.org returned 404; covered instead by gem source and a probe)
- `add:`/`del:` macros
- `revix` README

**The last three targeted searches surfaced no new candidate:**
- (a) lossless programmatic AsciiDoc editing in Python or Node: none. The Rust and .NET parsers found are
  semantic, not lossless.
- (b) comment-resolution → commit traceability in docs-as-code: only practice examples, such as the OASIS CSAF
  comment-resolution log that links rows to commits [C7]. No tool.
- (c) reproducible or deterministic Metanorma output: nothing Metanorma-specific.

**K = 3 met.**

**Corroboration (N = 2) per leading mechanism:**
- Disposition model: ISO template guidelines [C1] + ISO OSD resolution types [C2] + `commenter` [C4]. ✔
- Edit application: a **build** verdict, which closes on K because there is no assemble candidate. The mechanism
  is corroborated by the git docs [C8] and a probe. ✔
- Diff attribution: git trailer docs [C8][C9] + probe. ✔
- Containment / id behaviour: gem source (`contenthash`) + probe. ✔
- N3 list: gem source (`Date.today` and `random_uuid` call sites) + probe. ✔
- Document history: gem source + `revix` README [C6] + probe. ✔
- Redline `add`/`del`: gem source + probe (+ an older rubydoc API page [C5]). ✔

**W2 status proposal: dry.**

## 9. POC guidance (for factory-poc)

**Inputs:**
- `register.yaml` (from C3/C4).
- `dispositions.yaml` (§2), containing at least one accept, at least one modify (including one clause inserted
  *before* an existing clause) and at least one reject, with both channels if C4 is present.
- The v1 source, tagged `v1`.

**Commands (one `make resolve` target):**
1. `validate-dispositions` (§2 rules) → exit 0. A seeded bad file (unknown id, missing observation, a reject
   with edits) → non-zero exit.
2. `apply-edits` (§3) → tags `v2`. Repeating it from a clean state → the same `git rev-parse v2`.
3. `check-attribution` (§4) → exit 0. A seeded stray-edit commit on a scratch branch → non-zero exit.
4. Compile v2 with the C1 recipe (`metanorma compile --no-install-fonts -t iso -x xml,html,pdf`,
   `--network none`, digest pin).
   - **Observed:** without `--no-install-fonts`, the compile tries to `git clone
     https://github.com/fontist/formulas.git` and fails offline (exit 1). This matters for N6.1 ("only network
     access is the image pull").
   - W0/W3 should confirm the HTML and PDF fonts are adequate offline.
5. `check-containment` (§5, using the C2.4 output) → a pass table per comment.
6. `emit-trace` (§7) → `trace.csv` / `trace.yaml`, then the blank-cell check.
7. N3: run a second time from clean, then `cmp` the register, trace, report and v2 `d.xml`. On a mismatch, apply
   the §6 defensive list and report each normalized hit.

**Expected observables:** every check exits 0 on the good fixture and non-zero on its seeded negative. `git log`
shows one trailer-bearing commit per accept/modify id and none for rejects.

**Source attributes the v1/v2 sample must set** (for N3, and to keep the C6.2 count clean): `:revdate:`,
`:copyright-year:`, `:secretariat:`, `:technical-committee:` and its number, `:docstage:` / `:docsubstage:`.
Container environment: `SOURCE_DATE_EPOCH`.

## 10. Flags

1. **C2.4 is the hard dependency** for C5.3 and the v2 columns of C5.4 (§0, §5).
2. **`commenter` is not in the pinned image.** W1's assemble path needs a derived image (a new digest pin), or
   `commenter` stays a reference for vocabulary only.
3. **ISO's "Metadata warnings" auto-annotation** (presentation XML, `reviewer="Metanorma"`, `Date.today`) appears
   when secretariat, committee or date is missing. **W4 must exclude or prevent it**, or C6.2's count will be off
   by one and N3 will drift across days.
4. **An offline compile needs `--no-install-fonts`** (probe) — relevant to W0 and N6.
5. **`noted` and `deferred` have no Q7 slot.** A recorded mapping is needed (§1).
6. PDF determinism is unmeasured. Keep PDF out of the N3 identity set.
7. Probes ran on one day only. The cross-day claims rest on gem source.

## Citations

- [C1] type: docs · ref: https://helpdesk-docs.iso.org/article/299-commenting-template-guidelines · title:
  Commenting template guidelines · org: ISO · year: 2026
- [C2] type: docs · ref: https://helpdesk-docs.iso.org/article/640-resolve-comments · title: Resolve comments ·
  org: ISO · year: 2026
- [C3] type: docs · ref: https://www.jtc1sc32.org/doc/N1551-1600/32N1595-disp_of_comments-PDTR2_15944-6_doc ·
  title: ISO/IEC JTC 1/SC 32 N 1595 · org: ISO/IEC JTC 1/SC 32 — surfaced in search, not opened
- [C4] type: repo · ref: https://github.com/metanorma/commenter · title: commenter · org: Metanorma; Ribose
- [C5] type: docs · ref: https://www.rubydoc.info/gems/metanorma-standoc/1.9.2/Asciidoctor/Standoc/DelMacro ·
  title: Class: Asciidoctor::Standoc::DelMacro · org: Metanorma
- [C6] type: repo · ref: https://github.com/metanorma/revix · title: revix · org: Ribose
- [C7] type: docs · ref: https://docs.oasis-open.org/csaf/csaf/v2.0/cs03/csaf-v2.0-cs03-comment-resolution-log.pdf ·
  title: CSAF v2.0 CS03 comment resolution log · org: OASIS — surfaced in search, not opened
- [C8] type: docs · ref: https://git-scm.com/docs/git-interpret-trailers · title: git-interpret-trailers · org: Git
  project
- [C9] type: docs · ref: https://git-scm.com/docs/pretty-formats · title: git pretty formats · org: Git project
- [C10] type: repo · ref: metanorma/metanorma-standoc (v3.5.20 as installed in the pinned image; files
  cleanup/inline.rb, cleanup/dochistory.rb, converter/macros_inline.rb, converter/blocks_notes.rb,
  converter/front_contributor.rb) · title: metanorma-standoc · org: Metanorma
- [C11] type: repo · ref: metanorma/metanorma-utils (v2.0.12 installed; utils/anchor.rb, utils/random_uuid.rb) ·
  title: metanorma-utils · org: Metanorma
- [C12] type: repo · ref: metanorma/metanorma-iso (v3.5.14 installed; isodoc/iso/presentation_section.rb,
  metanorma/iso/front_id.rb) · title: metanorma-iso · org: Metanorma
- [C13] type: repo · ref: canon gem v0.3.125 (installed in image; `canon help diff`) · title: canon
- [C14] type: docs · ref: https://reproducible-builds.org/docs/source-date-epoch/ · title: SOURCE_DATE_EPOCH ·
  org: Reproducible Builds — cited from general knowledge, not opened this run
