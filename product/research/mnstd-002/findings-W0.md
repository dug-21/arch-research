<!-- Persisted verbatim by research-leader from the factory-researcher's inline return (subagent file write was blocked; OBS-2: leader persists). Extracted mechanically from the agent's final message. -->
# findings-W0 — Foundations (C1 #336, C2 #335)

**Scope:** mnstd-002 · workstream W0 · researcher `factory-researcher` · 2026-11-13
**Status of everything below:** research. Nothing here is proof, and no grade moves on it.
The probes were run in the pinned image, in a scratch dir outside the repo (`/tmp/claude-1000/w0probe/`). They
are **measurements (ours, unvalidated)**. They have not been demonstrated at the firewall, and the POC must
re-run them. Every claim carries one of three labels:
**[doc]** a doc-claim from a vendor or third party · **[src]** read in the gem source shipped inside the pinned
image · **[probe]** observed by us in a scratch probe.

## 0. Headline (for the leader)
1. **C2 looks assemblable, but the honest call is BUILD-thin-glue.** Metanorma has no native "locator → element"
   resolver and no sourcemap in its output. It does supply every *ingredient*: element numbers in the presentation XML
   joined to semantic ids by `@semx-id` [probe][src], and the AsciiDoc block start lines via Asciidoctor's `sourcemap`
   API, which runs inside the image so N2 stays clean [probe]. That makes C2 roughly 200–300 lines of Python glue plus
   one roughly 20-line Ruby helper run in the container.
2. **Auto-generated ids are NOT stable under edits (C2.4 risk, demonstrated by probe).** The semantic id is
   `"_" + MD5(xpath + "////" + element.text)` [src]. The id is byte-stable across identical recompiles [probe].
   Inserting one clause before clause 4 changed **37 of 66** ids [probe]. Editing a paragraph also changes the id of
   every ancestor. Author `[[anchors]]` survive as `@anchor`. **C2.4 must be built**: anchor-keyed matching for
   structural elements plus text alignment for paragraphs.
3. **Q3: line numbers DO exist natively, but only in the PDF.** `:presentation-metadata-linenumbers: true` produces
   line numbers that restart on every page [doc][src][probe]. They are not in the semantic XML, the presentation XML
   or the HTML. **Verdict: do not promote Q3.** Keep `line` informational, optionally as `page:line`.
4. **NEW BLOCKER-CLASS FLAG (N6.1 vs C1): PDF needs ~730 MB of fonts downloaded at compile time.** The image ships no
   fonts. With `--network none`, the PDF fails with exit 1 [probe]. N6.1 allows only the image pull. The leader or
   owner must rule on this (§5).
5. **Exit code is not a reliable "broken source" signal.** An undefined xref, an unterminated table, malformed
   passthrough and even a **Severity-0** duplicate anchor all exit 0, **with or without `--strict`** [probe]. Only an
   unresolved `include::` was FATAL (exit 1). This matters for C1.2 and C4.3 (W3).

## 1. Candidate technologies
| # | Candidate | What it does | Maturity / maintenance | Verdict |
|---|---|---|---|---|
| T1 | `metanorma/metanorma@sha256:836b7ab2…dff3da` | metanorma 2.5.24, cli 1.18.6, metanorma-iso 3.5.14, standoc 3.5.20, isodoc 3.7.14, mn2pdf 2.74, asciidoctor 2.0.26, ruby 4.0.7, OpenJDK 21 [probe] | Active. Built ~14 h before the probe. Version tags correlate with metanorma-cli [doc] | **ADOPT** (C1). Pin by digest |
| T2 | metanorma-iso flavor | ISO AsciiDoc → semantic XML → presentation XML → HTML/PDF | Active, 3.5.14 | **ADOPT** (C1) |
| T3 | Presentation XML numbering (`fmt-title`/`fmt-name` caption labels, `@autonum`, `fmt-xref-label`, `@semx-id`) | Native carrier of every clause, table, figure, note and annex number, linked back to the semantic id | Native (isodoc 3.7.14) | **ASSEMBLE**: basis of C2.1 |
| T4 | Asciidoctor `sourcemap: true` (`Block#source_location.lineno`), run with the image's Ruby | Block start line plus author id for every block | Core Asciidoctor API | **ASSEMBLE**: basis of C2.2. In container (N2.2-clean) |
| T5 | Author anchors `[[id]]` → semantic `@anchor`, HTML `id`, presentation `@id` | Stable, author-controlled keys | Native | **ASSEMBLE**: stable key for C2.4 structural elements |
| T6 | Resolver glue (Python 3.14 stdlib `xml.etree` + `difflib`) | Locator parsing, file:line enclosure, v1→v2 alignment, rejection with reasons | Ours | **BUILD** (C2.1–C2.4) |
| T7 | `:presentation-metadata-linenumbers: true` | Per-page line numbers, PDF only | Documented [doc]; XSL hook [src]; works [probe] | Optional assemble for Q3 display. Not a resolver input |
| T8 | `canon` gem (in image: `canon diff`/`format`) | Semantic XML/HTML canonicalisation and diff | Ribose, 0.3.125 | Candidate for N3/W2. Not evaluated |
| T9 | Own Python AsciiDoc line parser | Re-parse the source for block boundaries | Build | Rejected below T4 (fragile, duplicates Asciidoctor) |
| T10 | Raw semantic `@id` as the cross-version key | — | — | Rejected for C2.4 (unstable, demonstrated by probe) |

No native Metanorma v1↔v2 element-mapping facility was found; the three dry searches in §8 surfaced none.

## 2. C1 — document model and compile recipe
### 2.1 Minimum header (CD draft) — compiles [probe]; attribute meanings [doc]
```asciidoc
= Widget calibration -- Procedure for fictitious gauges
:docnumber: 99999
:partnumber: 1
:edition: 1
:revdate: 2026-11-13            // fix it: feeds bibdata date/version (N3)
:copyright-year: 2026
:language: en
:title-intro-en: Widgets
:title-main-en: Calibration procedure for fictitious gauges
:title-part-en: General
:title-intro-fr: ...            // fr titles silence ISO_11/13/15
:title-main-fr: ...
:title-part-fr: ...
:doctype: international-standard
:docstage: 30                   // 20 WD, 30 CD, 40 DIS [doc]
:docsubstage: 00
:technical-committee-type: TC
:technical-committee-number: 999
:technical-committee: Fictitious widgets
:secretariat: XYZ               // without it the tool injects an annotation (§2.5)
:mn-document-class: iso
:mn-output-extensions: xml,html,pdf,rxl
:local-cache-only:
:no-isobib:                     // or per-ref nofetch(...)
:data-uri-image:
:presentation-metadata-linenumbers: true   // optional, PDF only
```
### 2.2 Section and block syntax (all compiled to exit 0) [probe]
- `.Foreword` paragraph before the first `==` → `preface/foreword`. `== Introduction` → `preface/introduction`.
- `== Scope` → `clause[@type='scope']`. `[bibliography]\n== Normative references` → `bibliography/references[@normative='true']`. `== Terms and definitions` then `=== term` → `terms/term`.
- `==`/`===`/`====` give clauses and subclauses. Annex: `[appendix,obligation=informative]\n== Title`.
- Table: `[[tab-x]]\n.Caption\n|===…|===`. Figure: `[[fig-x]]\n.Caption\nimage::f.png[]`. Note: `[[note-x]]\nNOTE: text`.
- Ref: `* [[[ref1,nofetch(ID)]]], _Title_`. Must be fictitious (N8). The probe used a real title; the POC must not.
- **Note relocation [probe]:** a `NOTE:` after a paragraph is nested inside that `<p>`. A `NOTE:` after an image becomes a figure note inside `<figure>`.

### 2.3 Compile invocation (measured)
```sh
IMG=metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da
docker run --rm --network none \
  -v "$FONTS/metanorma":/root/.metanorma -v "$FONTS/fontist":/config \
  -v "$BUILD":/metanorma -w /metanorma "$IMG" \
  sh -c 'metanorma compile -t iso --agree-to-terms sample.adoc; rc=$?; chown -R '"$(id -u):$(id -g)"' /metanorma; exit $rc'
```
- Image config: entrypoint `[]`, cmd `metanorma`, workdir `/metanorma`, user root, `FONTIST_PATH=/config` [probe].
- Outputs land next to the source: `sample.xml`, `sample.presentation.xml`, `sample.html`, `sample.pdf`, `sample.rxl`, `sample.err.html` (validation log), `sample.asciidoc.log.txt`, `sample.pdf.err`, and `relaton/` [probe].
- **`-o` is broken when xml is requested.** Both `-o out` and `-o /metanorma/out` exit 1 with `Errno::ENOENT …/out/sample.xml` [probe]. Compile in place in a per-build copy instead.
- `-x xml,html` overrides the extensions and is good for fast resolver builds [probe].
- `--user 1000:1000` breaks fontist (`Etc.getpwuid: can't find user for 1000`) [probe]. Run as root and `chown` inside the container.
- Warm-cache timing is ~24 s for xml+html+pdf. A cold networked first run took 5 min 22 s [probe].

### 2.4 Semantic XML model [probe]
- Root: `<metanorma xmlns="https://www.metanorma.org/ns/standoc" type="semantic" version="3.5.14" schema-version="v2.3.0" flavor="iso">`. Flavor is also in `bibdata/ext/flavor`.
- Stage: `bibdata/status/stage[@abbreviation='CD']`=30, `substage`=00, `ext/stagename`, `metanorma-extension/semantic-metadata/stage-published`=false, docidentifier `ISO/CD 99999-1:2026`.
- Body: `preface/{foreword,introduction}`, `sections/{clause[@type=scope],terms,clause…}`, `annex`, `bibliography/references[@normative=true]`. **Normative references move to bibliography,** so XML order ≠ source order.
- Every element has a content-hash `@id`. Author anchors appear as `@anchor`.
- **No numbers** in the semantic XML. **No source-line info** in either XML. No sourcemap option was found in the standoc, iso or isodoc sources [src].
- Tool-injected boilerplate: the copyright statement, the terms intro plus the OBP/Electropedia list, the normative-references intro, and the draft warning in the presentation XML. Declare these (Q6/N8.2).

### 2.5 Presentation XML: where numbers live [probe][src]
- `@semx-id` equals the semantic `@id`; all 76 resolved. The presentation `@id` is replaced by the author anchor where one exists.
- Number carriers: `fmt-title//span[@class='fmt-caption-label']` ("1", "4.1", "4.2.1", "Annex A", "A.1", term "3.1"); `fmt-name//…caption-label` ("Table 1", "Figure 1", "NOTE"); `@autonum`; `fmt-xref-label` ("Clause 4, Note", "Figure 1, Note"), with `@container` naming the owning element.
- A sole note is unnumbered ("NOTE"). Recommendation: accept `Note 1` for the sole note and record `normalized: sole-note`.
- **Auto annotation:** without `:secretariat:`, the draft gets `<annotation reviewer="Metanorma">` "Metadata warnings: Secretariat is missing" in `annotation-container`. With it set, the count is 0. This affects the C6.2 count (W4). The annotation element is `<annotation from to reviewer date>`, rendered via `fmt-annotation-start/-end/-body`. Visibility comes from `presentation-metadata/render-document-annotations`, falling back to unpublished [src isodoc footnotes.rb:251]. metanorma.org documents `:draft:` and does not list `render-document-annotations` [doc]. W4 must reconcile this.

### 2.6 HTML [probe]
Element `id` = author anchor, else the semantic hash id. Heading and TOC ids are random v4 UUIDs per run, so HTML is not byte-reproducible.

### 2.7 Determinism (N3 input) [probe]
On the same day, identical compiles gave a byte-identical `sample.xml` and `sample.presentation.xml`. The HTML differs (heading and TOC UUIDs) and the PDF differs. Volatile candidates: HTML UUIDs, PDF bytes, `annotation/@date` (the compile date), and `:revdate:`-driven fields (fix that attribute). Cross-day determinism was not tested. The cleanup pass rewrites GUID ids to content hashes in both the semantic and presentation steps [src standoc cleanup/inline.rb:137–148; isodoc ids.rb:115–126].

### 2.8 Warnings for a minimal doc (C1.2) [probe]
Fixable in source:
- ISO_11/13/15: missing fr titles.
- ISO_21: table or annex never cross-referenced.
- "subclause is only child".
- "possible decimal point 4.1" in prose.
- "term definition starts with article".

Tool-attributable, on the injected boilerplate: the "'iso' lowercase" and "digit '8' in prose" warnings, plus STANDOC_68 suppression (sev 3). The `nofetch` normative ref produces "non-ISO/IEC reference…", so declare it. **Check:** exit 0 AND no `Severity 0` in `sample.err.html`.

### 2.9 Broken-source behaviour (handed to W3 for C4.3) [probe]
| Seeded defect | exit | exit `--strict` | sev-0 |
|---|---|---|---|
| `include::missing-file.adoc[]` | **1** (FATAL: Unresolved directive) | **1** | — |
| undefined xref + unterminated table | 0 | 0 | none |
| malformed passthrough | 0 | 0 | none |
| duplicate `[[cl-test]]` | 0 | 0 | **1** |
Recommendation: the seeded broken branch uses a missing include. The gate rule is `exit≠0 OR Severity 0`.

## 3. C2 — resolver design (ranked)
### 3.1 C2.1 locator → id. Build thin glue on T3 (rank 1)
1. Walk the presentation XML and build `clause_no→semx-id`, `Table N→id` and `Figure N→id` from the caption labels.
2. **para N** = the Nth direct-child `p` of the clause in the semantic XML. Nested notes do not count. Declare whether injected boilerplate paragraphs count.
3. **Note N** = note descendants whose nearest ancestor clause is X, excluding figure and table notes. Cross-check with `fmt-xref-label/@container`.
4. Table and figure numbers are global in the body and `A.n` in annexes (confirm in the POC).
5. Reject 0 or >1 matches with a reason.
A stdlib prototype (`/tmp/claude-1000/w0probe/tools/numbermap.py`) printed the full map correctly [probe].
Rank 2 (rejected): re-derive the numbering from the semantic XML. That re-implements isodoc's xref logic.

### 3.2 C2.2 file:line → element. Assemble T4 in the container plus build the join (rank 1)
```ruby
# srcmap.rb — docker run --rm --network none -v $SRC:/metanorma:ro -v $TOOLS:/tools:ro $IMG ruby /tools/srcmap.rb sample.adoc
require "asciidoctor"; require "json"
doc = Asciidoctor.load_file(ARGV[0], sourcemap: true, safe: :safe)
out = []
walk = ->(b) { b.blocks.each { |c| out << { ctx: c.context, id: c.id, line: c.source_location&.lineno,
  level: (c.context == :section ? c.level : nil), title: (c.title rescue nil), style: c.style }; walk.(c) if c.respond_to?(:blocks) } }
walk.(doc); puts JSON.generate(out)
```
Observed [probe]: `45 paragraph p-4-1`, `50 admonition note-4-1`, `53 section L2 cl-test`, `58 table tab-conds`, `76 image fig-layout`, `68 section L3 _gauge`.
Join rules:
- The enclosing block is the last block whose start ≤ line and whose next block starts after the line.
- Block → element: by author anchor (`block.id == @anchor`). Asciidoctor auto ids such as `_scope` are **not** in the semantic XML. Otherwise by ordinal (k-th section at the same level under the matched parent; k-th paragraph block ↔ k-th direct `p`), applying the note-relocation rule and skipping injected boilerplate.
- Header, blank and comment lines → reject.
Rank 2: a Python AsciiDoc scanner (T9).

### 3.3 C2.4 v1→v2. Build (auto ids demonstrated unstable)
Probe: inserting a clause before clause 4 and editing a 4.2 paragraph kept 29 of 66 ids and changed 37 (clauses 4–6). Mechanism [src]: `MD5("#{elem.path}////#{elem.text}")`, with a positional path and descendant text. An earlier insertion shifts every later subtree. A text edit changes the element and all its ancestors.
1. **Hybrid (recommended):** anchor clauses, tables, figures, notes and annexes. Leave paragraphs unanchored and align them by normalized text inside the matched parent (exact first, then `difflib` ratio ≥ τ, order-preserving). Report renumbering as `old→new` by anchor (e.g. `cl-test: 4.1 → 5.1`).
2. Anchor everything. C2.4 becomes trivial, and the validator may see a rigged fixture. Fallback only, and declare it.
3. Full tree alignment. Over-built; park it.
State the anchoring policy in the run report: C2 is then proven for drafts authored with structural anchors.

### 3.4 C2.3 negative fixture
`9.9`; `Table 7`; `4 para 9`; `Note 3` (in a clause with one note); `B` (no annex B); a header line `sample.adoc:3`; a blank line; a line past EOF. Each emits `{status: rejected, reason}` and never a nearest-match.

## 4. Q3 verdict
`:presentation-metadata-linenumbers: true` puts line numbers in the PDF only [doc metanorma.org; src iso XSL l.943 `<?add_line_numbers?>`]. The probe PDF numbered lines per page (p.1: 1–30, p.2: 1–8; pdfminer extraction). They are absent from the XML and HTML. **Keep the Q3 default.** Optionally enable the attribute and record `page:line` (format-validated only).

## 5. Environment notes and flags
- Pin `@sha256:836b7ab2…dff3da`. Record the `metanorma --version` line (2.5.24 / Cli 1.18.6 / Standoc 3.5.20 / IsoDoc 3.7.14 / Iso 3.5.14).
- **FONTS vs N6.1 (ruling needed).** `/config/fonts` is empty. A PDF compile downloads 164 MB into `/config` (fontist) and 563 MB of Noto into `/root/.metanorma/fonts` from github.com. Offline, it fails with exit 1 (`NotoSans-Regular.ttf` not found). The measured fix is one networked `--agree-to-terms` run with both dirs mounted from the host; later runs with `--network none` succeed [probe].
  - (a) A dated Extension declaring a one-time font fetch, with a gitignored cache and a `make fonts` target. **Recommended.**
  - (b) A derived image with fonts baked in. Its build still needs network, it must not be committed, and it adds a digest to record.
  - (c) Drop the PDF. C1.1, C5.3 and C6.1 then fail.
  - FOP warns that the variable Inter fonts are unsupported and substitutes Noto. Cosmetic; list it under C1.2.
- Relaton: without `:no-isobib:` or `nofetch`, compiling tries an online lookup, which offline degrades to a warning.
- `--network none` is the N6 instrument for every compile after the font fetch.
- Output files are root-owned unless you `chown` them.
- Asciidoctor is already in the image; no extra gems are needed.

## 6. POC recipe (W0 clauses)
```make
IMG := metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da
FONTS := .cache/fonts
fonts:   # only networked step besides the image pull (ruling needed)
	mkdir -p $(FONTS)/fontist $(FONTS)/metanorma
	docker run --rm -v $(PWD)/$(FONTS)/fontist:/config -v $(PWD)/$(FONTS)/metanorma:/root/.metanorma \
	  -v $(PWD)/build/fontwarm:/metanorma -w /metanorma $(IMG) metanorma compile -t iso --agree-to-terms sample.adoc
compile-v1:
	docker run --rm --network none -v $(PWD)/$(FONTS)/fontist:/config -v $(PWD)/$(FONTS)/metanorma:/root/.metanorma \
	  -v $(PWD)/build/v1:/metanorma -w /metanorma $(IMG) sh -c 'metanorma compile -t iso --agree-to-terms sample.adoc; rc=$$?; chown -R $(shell id -u):$(shell id -g) /metanorma; exit $$rc'
```
Expected observables:
- **C1.1:** exit 0 and all four outputs exist.
- **C1.2:** zero `Severity 0` entries, and a warnings table from `err.html` plus `pdf.err`.
- **C1.3:** XPath (`m=https://www.metanorma.org/ns/standoc`) checks `/m:metanorma/@flavor='iso'`, `//m:bibdata/m:status/m:stage[@abbreviation]`, and `stage-published='false'`. Every authored element has an `@id`. Its number comes from the presentation XML via `@semx-id`; state this join in the run report.
- **C2.1–C2.3:** `resolver.py locate` gives a results table.
- **C2.2:** `srcmap.rb` gives `srcmap.json`, then `resolver.py line` covers ≥10 lines across levels 1–3.
- **C2.4:** compile v2 (a clause inserted before clause 4, 3 elements edited), then `resolver.py map v1 v2` gives `{v1_id→v2_id,status}` plus `old→new` number pairs.

Sample checklist:
- `:secretariat:` set; fr titles present.
- xrefs to every table, figure and annex.
- No lone subclause, and no "4.1"-style digits in prose.
- A fictitious `nofetch` ref.
- Structural anchors only; paragraphs unanchored.
- ≥2 notes in one clause, plus one figure note and one annex table.

## 7. Citations
| type | ref | title | org | note |
|---|---|---|---|---|
| docs | https://www.metanorma.org/flavors/iso/ref/document-attributes/ | Metanorma ISO: document attributes | Ribose (Metanorma) | docstage, secretariat, `:draft:`, linenumbers, no-isobib, local-cache-only [doc] |
| repo | https://github.com/metanorma/metanorma-docker | metanorma-docker README | Ribose | run syntax; tags ↔ cli; fonts under /config/fonts [doc] |
| repo | metanorma/metanorma-utils (2.0.12, lib/utils/anchor.rb) | Metanorma::Utils.contenthash | Ribose | id hash [src] |
| repo | metanorma/metanorma-standoc (3.5.20, lib/metanorma/cleanup/inline.rb) | contenthash_id_cleanup | Ribose | [src] |
| repo | metanorma/isodoc (3.7.14, presentation_function/ids.rb, footnotes.rb) | presentation ids; display_comments_global? | Ribose | [src] |
| repo | metanorma/metanorma-iso (3.5.14, iso.international-standard.xsl) | ISO PDF XSL linenumbers hook | Ribose | [src] |
| repo | metanorma/metanorma-cli (1.18.6) | `metanorma help compile` | Ribose | [src] |
| repo | asciidoctor/asciidoctor (2.0.26) | sourcemap / Block#source_location | Asciidoctor project | [probe] |
| repo | metanorma/canon (0.3.125) | Canon: semantic comparison for serialization formats | Ribose | [doc] |
Probe artefacts (scratch, not evidence): `/tmp/claude-1000/w0probe/`.

## 8. Coverage log (K=3, N=2)
1. Unimatrix search "metanorma semantic XML element id anchor resolver sourcemap line numbers" → #335/#336/#281 only (≤0.43). No reuse.
2. Web, document attributes → docstage. **New.**
3. Web, id generation → nothing. Answered from source instead.
4. Web, docker fonts offline → **new** (font/offline mechanism).
5. Fetched the metanorma.org attributes page ×2 → **new** (linenumbers, `:draft:`, no-isobib).
6. Web, "line numbers ISO PDF" → **dry 1**.
7. Web, "mn2pdf add_line_numbers" → **dry 2**.
8. Web, "anchors cross-references annex" → **dry 3**.
9. Fetched the metanorma-docker README.
10. Source greps in the image: sourcemap/lineno (none in Ruby), contenthash, linenumbers, render-document-annotations.

K=3 met. N≥2 per leading mechanism:
| Mechanism | Sources |
|---|---|
| Compile | README + CLI + probe |
| Numbers via semx-id | src + probe |
| Hash ids | src + probe |
| Sourcemap | API + probe |
| PDF line numbers | doc + XSL + probe |
| Fonts | README + probe |

**W0 proposed DRY.**

**Open:**
- Cross-day determinism.
- `Table A.1` numbering.
- Numbering with ≥2 notes per clause.
- Whether `--user` with a mounted `/etc/passwd` works.
- The `-o` root cause.
- Whether `--strict` ever changes the exit code.
- Reviewer-note syntax (W4).
