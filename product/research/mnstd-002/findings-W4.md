<!-- Persisted verbatim by research-leader from the factory-researcher's inline return (subagent file write was blocked; OBS-2: leader persists). Extracted mechanically from the agent's final message. -->
# findings-W4 — Review output (C6 #331, C7 #330)

- **Scope:** mnstd-002 · tech-discovery · workstream W4 · `agent_id: factory-researcher`
- **Date:** 2026-11-13
- **Image probed:** `metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da`
  (Metanorma 2.5.24, metanorma-cli 1.18.6, **metanorma-standoc 3.5.20, isodoc 3.7.14, metanorma-iso 3.5.14**,
  mn2pdf 2.74). Host x86_64.

**Evidence labels:**
- **[doc]**: a vendor doc-claim.
- **[src]**: a reading of the gem source shipped *inside the pinned image*.
- **[probe]**: a measurement we ran on the pinned image, in scratch at `/tmp/claude-1000/w4probe/`. Probes are
  measurements, not proof.

Nothing here grades anything `proven`. §7 gives the recipe to reproduce the probes.

---

## 0. Headline

1. **The syntax is current, but the XML element is not `<review>`.**
   - `[reviewer=…,date=…,from=…,to=…]` plus a `****` sidebar still works [doc][src][probe].
   - In semantic XML it becomes **`<annotation>`**, moved into a root-level **`<annotation-container>`**.
2. **The render override exists:** `:presentation-metadata-render-document-annotations: true|false` [doc][src][probe].
   - `:draft:` is **no longer observed** [doc].
   - In ISO, "unpublished" means stage < 60 [src].
3. **Contradiction for C6.1: native HTML renders NO annotations** in metanorma-iso 3.5.14 [src][probe].
   - The doc says annotations render in HTML, PDF and Word [doc].
   - In the isodoc HTML converter, `comments()` and `fmt_annotation_body_parse` are no-ops. 0 comment texts
     appeared in HTML across 9 compiles.
   - **PDF** renders them as native PDF sticky notes (`/Subtype /Text`, `/T` = reviewer, `/M` = date,
     `/Contents` = text) [probe].
   - Verdict: **C6.1-HTML = build** (glue injection). **C6.1-PDF = assemble.**
4. **Contradiction: the PDF ignores the stage rule.**
   - At stage 60 (published), and with the override set to `false`, the PDF still showed every sticky note [probe].
   - The stage/override switch only gates presentation-XML `fmt-annotation-body`, which the Word output uses.
   - So C6.3's "clean build shows none" must come from **leaving the review blocks out of the source**, never
     from the stage. C6.4 must state this.
5. **Undocumented sharp edges, all found by probe:**
   - A note whose `from` anchor is a **table** makes the whole **PDF fail** (FOP: `"fo:block" is not a valid
     child of "fo:table"`). Anchoring on a **table cell** works.
   - A note anchored on a **whole list** (`[[x]]` before `* …`) is **silently dropped** from the PDF. A
     **list-item** anchor works.
   - A **dangling `from`** **crashes** the presentation stage (`NoMethodError … comment_bookmarks_locate`). No
     PDF and no presentation XML are produced.
   - A `TODO:` with no `from` gets an auto-bookmark and is **dropped from the PDF**. Its date defaults to *today*.
   - So **the C6.2 count must cover the semantic XML *and* the PDF.**
6. **PDF needs fonts that are not in the image.**
   - `/config/fonts` is empty and no Noto font is installed.
   - Compiling offline fails on missing `NotoSans-Regular.ttf`, with or without `--continue-without-fonts`.
   - A one-time **network** fetch (fontist) downloads about 560 MB into `~/.metanorma/fonts`. After that,
     compiles run with `--network none` [probe].
   - **This is an N6.1 issue** ("only network access is the image pull").
7. **`commenter` is not in the image** (absent from `gem list`) [probe].
   - Using it needs a `gem install` (network, N6) or a derived image.
   - `stats` parses the disposition out of free-text `observations` (Accepted / AWM / Noted / Rejected / TODO).
     There is no `disposition` field and no v2 location [doc].
   - So **C7 = build** (a small Python generator). `commenter` is only an ungated cross-check stretch.

## 1. Current syntax — verdict on the stale doc-claims

| Stale claim (mnstd-001) | Current status | Evidence |
|---|---|---|
| `[reviewer=…,date=…,from=…,to=…]` + `****` | **Holds.** `reviewer` is required per the doc. The code falls back to `source`, then `"(Unknown)"`. `to` defaults to `from`. | [doc] annotations.adoc; [src] `blocks_notes.rb#sidebar_attrs`; [probe] p2/p7 |
| `date` | `YYYY-MM-DD`; `T00:00:00Z` is appended. **If absent it defaults to `Date.today`, which breaks N3.** The projection must always emit it. | [src]; [probe] the TODO got 2026-11-13 |
| `type` | Default is `review`. `todo` and `ignore-log` are reserved; **`ignore-log` suppresses validation log entries**. Do **not** put `ge/te/ed` in `type`. It is not rendered [probe], so carry type and MB in the note text. | [doc]; [src] `metadata.rb#annotation_cleanup` |
| `TODO` → reviewer note | **Holds** (`TODO:` or `[TODO]`, `type="todo"`). Avoid it in the prototype: it is dropped from the PDF when it has no `from`. | [doc]; [src]; [probe] p6 |
| Render only at draft stage | **Partly.** Gates presentation `fmt-annotation-body` only; **the PDF renders regardless**. ISO `published?` = `stage >= 60`; `:docstage-published:` overrides it. | [src] iso `cleanup.rb`, standoc `bibdata.rb`; [probe] p3 |
| `:presentation-metadata-render-document-annotations:` | **Holds** (standoc ≥ 3.1.1). Emits `<presentation-metadata><render-document-annotations>`, which `display_comments_global?` reads. | [doc]; [src] isodoc `footnotes.rb:250`; [probe] p3 |
| `:draft:` | **Retired.** | [doc] |

**C6.4 mechanism to record:** stage `30` plus `:presentation-metadata-render-document-annotations: true`, in the
*derived review input only*. Also state that the PDF renders whatever the stage.

**ISO side-effect (C6.2):**
- At an unpublished stage, metanorma-iso injects its own annotation (`reviewer='Metanorma'`, "Metadata warnings")
  when the secretariat, committee or document date is missing [src] `presentation_section.rb`.
- Set `:secretariat:`, `:technical-committee:` and `:revdate:`. Probe p2 set them, and no warning appeared.
- Also exclude `reviewer="Metanorma"` in the oracle.

## 2. Semantic XML (C6.2 oracle)

```xml
<annotation-container>
  <annotation id="_d3f4…" reviewer="DE" from="scope-p1" to="scope-p2" type="review" date="2026-11-02T00:00:00Z">
    <p id="…">…</p>
  </annotation>
</annotation-container>
```

- `review_cleanup` moves **every** `//annotation` into the container [src].
  - So the projection can append blocks anywhere, such as at the end of the document.
  - Doc-claim: notes "can be placed far from the annotated text". The code agrees, but end-of-document placement
    is not probed; the POC should confirm it.
- `from`/`to` keep the **author anchor**. The target element carries `anchor="scope-p1"` and a generated `_uuid` id.
- Presentation XML adds `fmt-annotation-start`, `fmt-annotation-end` and `fmt-annotation-body` only when display
  is on. **Do not count it.**
- **Determinism [probe]:**
  - Two compiles gave **byte-identical semantic XML** and identical presentation XML.
  - The generated ids look content-hashed.
  - The PDF bytes differ (timestamps), so do not diff PDFs for N3.

**Oracle:** PASS iff R = X = P = H, and each register id appears exactly once in each. The id is embedded in the
note text.
- `R`: register count.
- `X`: `count(annotation-container/annotation[@type='review'][@reviewer!='Metanorma'])` in the semantic XML.
- `P`: PDF `/Type /Annot` objects with `/Subtype /Text`, after inflating FlateDecode streams. Match on
  `/Subtype` and `/T`: `/Contents` may be hex-encoded when the text is non-ASCII.
- `H`: injected HTML nodes.

Probe p6 shows why P is required: X = 6 but P = 4.

## 3. Projection — verdict: **assemble (PDF) + build (projection, HTML injection)**

`project_review.py register.yaml v1/draft.adoc → build/review/draft.adoc`:

1. Copy the v1 source **unchanged**. Never write into `v1/` (D4, C6.3).
2. In the copy only, set `:docstage: 30` and `:presentation-metadata-render-document-annotations: true`.
3. Append one block per register row, sorted by id:
   ```
   [reviewer="{MB}",date={YYYY-MM-DD},from={anchor},to={anchor_to|anchor}]
   ****
   [{id}] {MB} · {type} · {clause}/{element}: {comment} Proposed change: {proposed_change}
   ****
   ```
4. **Anchor safety.** `from` must be one of these, all of which rendered in the PDF in probes:
   - paragraph, clause, note
   - **list item**, **table cell**, inline span

   Remap a table target to its first cell and a list target to its first item.

   Not tested: figure, formula, term and example targets, and whether `from` may name a generated `_uuid` id.
5. Fail closed on any anchor missing from the v1 semantic XML, because a dangling anchor crashes the build.

**Clean build (C6.3):**
- Compile `v1/draft.adoc` directly. Expect X = P = H = 0 (probe p4: 0/0).
- `grep -c '^\[reviewer=' v1/draft.adoc` must be 0.

**HTML (build):**
- The native HTML keeps author anchors as element ids, for example `<p id="scope-p1">` [probe].
- Post-process: for each semantic `<annotation>`, insert
  `<aside class="mn-review" data-comment-id data-from data-to>` after the `from` element. Show reviewer, date,
  MB, type and text.
- Validator ruling needed: does this satisfy "Metanorma-native"? The data is native, but the rendering is our glue.
- Word `.doc` has native comment code [src]. A quick probe found none, and it was not pursued (Q8).

## 4. PDF availability (N2, N6)

- mn2pdf 2.74 and Java are present. `FONTIST_PATH=/config/fonts` is **empty** in this digest.
- First compile (network, `--agree-to-terms`):
  - takes about 5 min 40 s;
  - downloads about 560 MB into `/root/.metanorma/fonts`, plus a fontist cache;
  - mount both as volumes.
- After that, `--network none --no-install-fonts` compiles succeed in about 20–45 s [probe].
- Run as root in the container, then `chown`. With `-u 1000`, fontist fails with `Etc.getpwuid: can't find user
  for 1000`.
- **N6.1 options:**
  - (a) A derived image with the fonts baked in, pinned by its own digest. Recommended.
  - (b) A declared one-time font-provisioning network step.
  - (c) Drop PDF, which fails C6.1.

## 5. Disposition report (C7) — verdict: **build**; `commenter` = optional stretch

**Why not commenter:**
- It is not in the image.
- It has no disposition field and no v2-location concept.
- `fill` produces DOCX only, which Q1 makes an ungated stretch.
- `validate` is schema-only [doc].

**Adopt its YAML keys for the register (N4.1):**
- `id, body, locality{clause,element,line_number}, type, comments, proposed_change, observations`
  (`iso_comment_2012-03`).
- Add `disposition` (`accept|modify|reject`, Q7) and `v2_location`.

**Generator:** `report.py register.yaml trace.csv v2/draft.xml → report.{html,yaml,csv}`
- Register only, no hand edits. Sorted by id and byte-deterministic.
- Columns: MB/NC · Line number · Clause/Subclause · Paragraph/Figure/Table · Type · Comments · Proposed change ·
  Observations of the secretariat · Disposition · v2 location.
- A declared key→header mapping table.
- The HTML footer reconciles type × disposition × MB. Accept and modify rows link to `v2.html#{anchor}`.

**C7.2 check:**
- Compute `Counter((type, disposition, body))` from the register, the YAML, the CSV and the parsed HTML rows.
- All four must be equal, the totals must equal the register length, and there must be no duplicate ids.

**C7.3 check:**
- Every accept/modify row has a non-empty `v2_location`.
- It resolves to `//*[@anchor=$a or @id=$a]` in the v2 semantic XML.
- The fragment exists as an `id` in `v2.html`.
- Exit non-zero on any miss.

**Stretch:**
- In a derived image, run `gem install commenter` and `commenter stats --format yaml`.
- Diff its counts against ours, mapping AWM → modify. `observations` must start with the disposition word.
- Run `commenter fill` → DOCX for N4.3.

## 6. Verdicts

| Clause | Mechanism | Verdict |
|---|---|---|
| C6.1 PDF | native `annotation` → mn2pdf sticky notes | **assemble** (probe: 4 anchor kinds OK) |
| C6.1 HTML | glue injection from semantic XML | **build** (validator ruling on "native") |
| C6.1 range | `from`/`to` | assemble (probe) |
| C6.2 | R = X = P = H script | **build** (small) |
| C6.3 | projection to `build/review/` + clean compile | **build** (small) |
| C6.4 | stage 30 + override, PDF stage-independence stated | assemble + declare |
| C7.1–3 | Python generator + checks | **build** |

**Determining constraint:** PDF font provisioning against N6.1. Second: the HTML "native" wording.

## 7. POC recipe

```sh
IMG=metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da
# one-time, network (declare under N6, or bake into a derived image)
docker run --rm -e FONTIST_PATH=/fh -v $PWD/.cache/fontist:/fh -v $PWD/.cache/mn:/root/.metanorma \
  -v $PWD/build/review:/w -w /w $IMG metanorma compile -t iso -x pdf --agree-to-terms draft.adoc
# gated runs, offline
docker run --rm --network none -e FONTIST_PATH=/fh -v …same mounts… -v $PWD/build/review:/w -w /w $IMG \
  sh -c 'metanorma compile -t iso -x xml,html,pdf,presentation --no-install-fonts draft.adoc; chown -R 1000:1000 /w'
```

**Expected observables:**
- XML: N annotations.
- PDF: N `/Subtype /Text`, with `/T` = MB.
- HTML: 0 annotations natively, N after injection.
- Clean build: 0/0/0.

**Fixture must include:**
- ≥1 ranged comment
- ≥1 table-cell anchor
- ≥1 list-item anchor
- no whole-table or whole-list targets unless remapped

**Optional seeded negative:** an unremapped table anchor, to show the guard trips.

## 8. Coverage log (K=3, N=2)

| # | Source | New? |
|---|---|---|
| 1 | standoc 3.5.20 source in the image (`blocks_notes.rb`, `cleanup/review.rb`, `annotation_container.rb`) | yes: `<annotation>` and its container |
| 2 | isodoc 3.7.14 (`footnotes.rb`, `html.rb`, `word_function/comments.rb`) and the iso XSL | yes: HTML no-op, PDF Annot, override reader |
| 3 | metanorma.org repo `author/topics/reviewing.adoc`, `blocks/annotations.adoc` (last commit 2025-12-07) | corroborates the syntax and override; contradicts the HTML claim |
| 4 | `metanorma/commenter` README | commenter model and its limits |
| 5 | Web: "metanorma reviewer notes render-document-annotations" | none new (old `:draft:`) |
| 6 | Web: site:metanorma.org reviewer notes | none new |
| 7 | metanorma.org `/author/topics/blocks/reviewer-notes/` | 404, none new |

**K = 3 is met** (searches 5–7 found nothing new).

**N = 2:**
- Syntax, element and override: docs + source + probe.
- HTML/PDF behavior: source + probe. The doc contradicts it.
- C7 verdict: README + image gem list.

**W4 status: dry, proposed sufficient.**

## 9. Flags

- **F1 (N6.1):** the PDF font download. Decide between a derived image and a declared network step.
- **F2 (C6.1):** HTML annotations cannot be native in iso 3.5.14. Needs a validator ruling on glue.
- **F3 (C6.2):** an XML-only count can pass while the PDF drops notes. Count the PDF.
- **F4 (to W1/C2):** reject dangling anchors (they crash the build). Remap table- and list-level targets.
- **F5 (doc drift):** the docs claim HTML rendering and stage gating that the pinned image does not do. Do not
  cite the docs as rendering evidence.

**Not verified:**
- figure, formula, term and example anchors
- `from` pointing at a `_uuid` id
- draft line numbering (W0)
- Word `.doc` comments
- commenter runtime behavior (doc-claim only)

## Citations

- `repo` · `metanorma/metanorma-standoc` · *metanorma-standoc v3.5.20: converter/blocks_notes.rb, cleanup/review.rb, cleanup/bibdata.rb, cleanup/metadata.rb, standoc/document/annotation_container.rb* · org: Metanorma
- `repo` · `metanorma/isodoc` · *isodoc v3.7.14: presentation_function/footnotes.rb, html_function/html.rb, function/inline_simple.rb, word_function/comments.rb* · org: Metanorma
- `repo` · `metanorma/metanorma-iso` · *metanorma-iso v3.5.14: metanorma/iso/cleanup.rb, isodoc/iso/presentation_section.rb, iso.international-standard.xsl, docx/comment_renderer.rb* · org: Metanorma
- `docs` · https://github.com/metanorma/metanorma.org/blob/main/author/topics/blocks/annotations.adoc · *Annotations (editor notes, reviewer notes, to-dos)* · org: Metanorma · year: 2025
- `docs` · https://github.com/metanorma/metanorma.org/blob/main/author/topics/reviewing.adoc · *Reviewing documents* · org: Metanorma
- `repo` · https://github.com/metanorma/commenter · *commenter (README)* · org: Metanorma
- `product` · `docker.io/metanorma/metanorma@sha256:836b7ab28c538262d58a3ce10d8504e2bb699a57bbc7ae2a5309c27368dff3da` · *metanorma/metanorma Docker image (Metanorma 2.5.24)* · org: Metanorma
- `docs` · https://www.rubydoc.info/gems/metanorma-standoc/1.1.2 · *metanorma-standoc 1.1.2 README (historical `:draft:` rule; stale)* · org: Metanorma
