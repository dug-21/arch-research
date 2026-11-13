# mnstd-002: goal-owner relevance review (synthesis, advisory)

- **Reviewer:** `goal-owner` (role A, synthesis review). I only read; I wrote nothing to the graph. Advisory to the human gate.
- **Read:** `mnstd-001/OWNER-BRIEF.md`, `REPORT.md`, `SCOPE.md` (including both Extensions), `reports/gate-feasibility.md`,
  `reports/gate-feasibility-rework1.md`, `GRADES.md`, `poc/README.md`, `artifacts/RESULT.md`, `artifacts/SNAPSHOT.md`,
  `findings-W1.md` and `findings-W4.md` (for native-feature claims). Live: position #384 and goal #329 (Active).
- **Confidence:** validated (proof). Under this role's conditioning, the step-function check is **suppressed**, because the
  SCOPE states no level-up question. §2 therefore records options to keep, not recommendations to pursue.

## Stance: **ACCEPT-WITH-NOTES**

The run answered the owner's question as asked. All four demonstrations are present. The one shortfall (C6 HTML) is
reported honestly as `partial`, not inflated. My notes concern how the owner gets to see the result, one native route the
run left unprobed, and the order of the follow-ons. None of them is a reason to revise.

---

## 1. Drift: did the run answer the owner's actual question?

**ALIGNED on substance.** I mapped the owner brief to the evidence:

| Owner ask (verbatim intent) | Delivered | Fidelity |
|---|---|---|
| ISO-style authoring in Metanorma | C1/C2: a fictitious ISO CD draft with the full ISO section set compiles to XML, HTML and PDF; locators resolve | Met. Authoring is shown as *a compiled, addressable draft*. The editor's view of authoring (writing ISO AsciiDoc, stages, xrefs, terms, boilerplate) is shown only by the sample source itself. That is thin but sufficient for a prototype, and it is not drift. |
| (1) Structured, clause-anchored intake validated against the document | C3: 3 reviewers, 2 MB/NC, 10 comments; 11 seeded-invalid rows rejected | Met, and it goes beyond `commenter validate`, which never checks anchors (G1). |
| (2) Resolution loop: dispositions, edits applied, v2 with traced resolutions | C5: 13 dispositions, one commit per comment id, traced v2, containment recomputed | Met. |
| (3) Git/PR review on the AsciiDoc source, local simulation | C4: local repo, line-anchored reviews, compile gate (exit code shown to be insufficient), `Resolves:` trailers, no remote | Met. The gate-verdict finding (#356) is a real lesson that others can reuse. |
| (4) Rendered output with native review blocks, plus a disposition report | C6 PDF native (13/13), HTML 0 native; C7 report | PDF and report met. HTML not met natively, and recorded as such (#358). |

**One legibility gap, against the owner's verb "show".** The brief says "build a prototype that is able to *show*
this". The committed snapshot is about 0.4 MB of JSON, CSV and YAML. N7 keeps every rendered PDF and HTML out of git.
So today the only way for the owner to *look at* the review PDF, the disposition report or v2 is a 10-minute Docker run
plus an 833 MiB networked font fetch. The run was tuned for **validator checkability** (37 checks, 37 self-tests,
tamper cases), and that was correct for the firewall. It was not tuned for **owner viewing**. This is an
under-delivery on presentation, not a wrong question. The fix is cheap (F0 below).

**Constraint alignment.** NFR literalism almost over-weighted tie-breakers into gates. N1.1 and N6.1 turned the font fetch
into a SCOPE FAIL, and C1.3 failed on "semantic vs presentation XML". The owner's rulings 1 and 2 corrected this in the
right direction, because the substantive need was met in both cases. Ruling 3 (C6 HTML) is a legitimate owner call. The
bar's `why` explicitly excludes a bespoke overlay, so `partial` is the honest grade. **Lesson for the retro, not this run:**
mnstd-001 wrote environment specifics ("only Docker, Node, Python"; "only network access is the image pull") into
`done_when` before anyone knew the toolchain's real prerequisites. That made the bar brittle.

## 2. Under-reach / step-function (suppressed: validated scope; options recorded only)

Under-reach is not called, since the check is suppressed. Two options came out of the run's own evidence and should be
recorded so they are not lost (defer-and-record, D10/D11):

1. **Native Word review comments: the unprobed native route, and the one most relevant to real ISO practice.**
   findings-W4 cites `metanorma-iso docx/comment_renderer.rb` and `isodoc word_function/comments.rb`. It also states that
   the stage/override switch gates `fmt-annotation-body`, "which the Word output uses". The route was dropped after "a quick
   probe found none" under Q8 ("no Word draft output"). ISO's working currency for drafts and comments is Word (the Form 13
   template is a DOCX). So the Metanorma path most likely to be **native** for in-document review is Word, not HTML, and it
   was never measured properly.
   - **Buys:** a possible native review rendering in a second output; a realistic round trip with real reviewer artefacts
     (DOCX draft with comments; Form 13 DOCX in via `commenter import`, out via `commenter fill`).
   - **Cost:** one compile with `-x doc` on the existing derived review input, about an hour, structure only. The commenter
     leg costs more: a derived image, which means a new pin and an N6.1/N2.1 decision.
   - **Caveat:** it would **not** clear C6.1 as worded, which requires HTML and PDF. Using it needs an owner
     frontier-change on C6 (D3), either "native in PDF and Word" or a new capability.
   - **Call:** defer-and-record. Probe it first if the owner wants C6 to move.
2. **The register as the single source of truth.** One validated register already drives intake, PDF annotations, the
   trace, v2 edits and the report. That is the architectural asset. A level-up would let real ISO-format sheets (DOCX or
   XLSX via `commenter import`) and real forge PR comments feed it, turning a prototype into a usable review tool.
   - **Cost:** high. It needs a forge, external side effects (currently forbidden) and Word fidelity.
   - **Call:** decline for now. Re-enter if the owner signals intent to use this for real drafting, not only to understand it.

## 3. Follow-ons: priority check and next run

REPORT §9 lists F1–F6. Position #384 lists only F1–F4. **Reconcile them** (curator, via `context_correct` on #384, or
note F5 and F6 in the report as non-graph hygiene). My order:

| Priority | Item | Why | Vehicle |
|---|---|---|---|
| **1** | **F0 (new): owner viewing bundle.** The review PDF (native notes), the clean v1 PDF and v2 PDF, the disposition-report HTML, and a one-page walkthrough mapping each of the 4 demonstrations to the file to open. | It closes the gap behind the owner's "show this" at near-zero cost. Attach the files to Issue #74 (allowed by the brief) rather than committing them, so N7 stays intact. | Leader or poc task. Not a run. No grade. |
| 2 | **F6:** correct #357 with the empirical result. | It is a false-in-graph state that another run could read; it costs nothing. | Curator, now. |
| 3 | **F5:** wire the font-pin check into `make demo`. | It is a one-line hardening step that makes the ruling 1 condition self-enforcing. | Poc, now. |
| 4 | **F1, reframed.** (a) Probe native Word comments first (§2.1). It is cheap and decides whether a native non-PDF route exists. (b) Owner decides on C6: amend the bar, or accept a permanent `partial`. (c) Upstream metanorma-iso issue: **this is an external side effect outside the brief's permission** (only GitHub Issues in dug-21/arch-research), so it needs explicit owner authorization before anyone files it. | As written, F1 offers the upstream issue as a garage action and treats "another output" vaguely. Word is the concrete candidate, and filing upstream is not ours to do unasked. | Small **directional** probe, then an owner ruling. |
| 5 | **F3:** fresh-clone, cross-day, second-host run, including `make fonts` on an empty cache. | It is the real envelope risk, because upstream font drift is the most likely way the prototype rots. It matters only if the prototype will be re-run or handed on. | Only on reuse intent. |
| 6 | F2: the C2.4 checker re-derives the mapping. | The residual is caught by N5.1. It hardens the rig but does not change the grade. | Opportunistic. |
| 7 | F4: DOCX report via `commenter fill`. | Fold it into the Word probe in item 4 if the owner wants the Word leg. Otherwise park it. | Bundle with item 4. |

**Next run:** **none is required.** The goal as asked is delivered, with an honest `partial` on C6. Items 1–3 are
housekeeping, not runs. If the owner wants C6 to move, the next run should be a **small directional probe**, "Native
review rendering in metanorma-iso Word output (+ commenter round trip)", with one question: *does any metanorma-iso 3.5.14
output other than PDF render reviewer annotations natively?* Its answer decides between a C6 frontier-change with a
validated re-test and closing C6 as permanently `partial` pending upstream. Do not open a validated re-scope of C6 before
that probe and the owner's bar decision. As C6 is currently worded, only an upstream change can clear it.

## Verdict

**ALIGNED** (no drift). **Under-reach not called** (validated; step-function suppressed; two options recorded).
**Stance: ACCEPT-WITH-NOTES.**
- Notes: (a) add the owner viewing bundle; (b) reconcile the follow-on lists in #384 and REPORT; (c) reframe F1 so that
  the Word probe comes first and an upstream issue requires owner authorization; (d) retro lesson: keep environment
  specifics out of `done_when`.

The human decides.
