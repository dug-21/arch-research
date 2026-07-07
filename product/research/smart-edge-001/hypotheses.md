# hypotheses.md — theme-scan `smart-edge-001`

**Theme:** `theme:smart-edge` · **Use-case:** #1 Unimatrix (MCP `context_*` surface + this repo's dogfood usage) · **Input:** `product/research/smart-edge-001/scout-candidates.md` · **agent_id:** `smart-edge-001-hypothesizer`

**Firewall note:** every entry is a `claimed` conjecture. Nothing here is graded, ranked, or a go/no-go — triage (goal-owner) cuts; the curator files each as a `finding` tagged `hypothesis`, `theme:smart-edge`, `smart-edge-001`.

## Index (statement → class → target)

| # | Statement (compressed) | Class | Target |
|---|---|---|---|
| H1 | tree-sitter validates structured node content at write time | obvious | context_store / context_correct |
| H2 | tree-sitter segments the observation buffer into a typed event tree for review | adjacent | context_cycle_review |
| H3 | tree-sitter's incremental re-parse makes hotspot detection *online during* a cycle | non-obvious | context_cycle / observation buffer |
| H4 | tree-sitter enables AST-granular chunking for code-bearing node embeddings | adjacent | context_search |
| H5 | tree-sitter subtree paths make edges claim-level instead of node-level | non-obvious | context_edge / graph model |
| H6 | tree-sitter tree-diff gives machine-readable deltas across supersession chains | non-obvious | context_correct / context_graph(chain) |
| H7 | ast-grep adds a third retrieval mode: structural pattern match over code-bearing nodes | obvious | retrieval (beside search/lookup) |
| H8 | ast-grep rewrite rules run deterministic convention codemods over the KB | adjacent | context_correct (bulk migration) |
| H9 | ast-grep meta-variables lift structured fields out of free-text nodes | non-obvious | content structuring / backfill |
| H10 | ast-grep rule bank lints the factory's own skills/protocol files (dogfood surface) | adjacent | repo dogfood (weak MCP-tool fit — noted) |
| H11 | Hyperscan multi-pattern bank streams the cycle buffer for hotspot/anti-pattern hits | obvious | context_cycle_review |
| H12 | RE2/Hyperscan exact-identifier channel fixes embedding blindness → hybrid search | adjacent | context_search |
| H13 | Write-time secret/PII pattern scan auto-routes nodes to quarantine | adjacent | context_store + context_quarantine |
| H14 | Hyperscan streaming upgrades the shd-006 egress filter to DPI-grade multi-pattern | adjacent (composition) | egress filter (prior proven work) |
| H15 | Reverse search: per-node signature bank streams the *live session* — knowledge surfaces itself | non-obvious (whitespace) | context_briefing (proactive) |
| H16 | Regular path queries: regex-over-edge-labels via DFA×graph product | non-obvious | context_graph |
| H17 | RE2 tag-grammar enforcement stops tag drift at write time | obvious | context_tag / context_store |
| H18 | Canonicalize-then-hash catches near-duplicate nodes content_hash misses | non-obvious | dedup / content_hash |
| H19 | PEG gives Unimatrix a runtime-extensible query DSL (DuckDB precedent) | non-obvious | query surface (lookup+graph combinators) |
| H20 | pika error-recovering parse lifts template fields from malformed agent output | adjacent | write path (competes with H1/H9 — flag) |
| H21 | Grammar-constrained decoding lets a small quantized model emit template-valid nodes in one pass | obvious | write path / edge story (shd N4) |
| H22 | Constrained decoding makes cycle_review output machine-consumable JSON | adjacent | context_cycle_review |
| H23 | SLM + grammar extracts findings/lessons from the buffer *on-device* at cycle close | non-obvious | knowledge-yield pipeline |
| H24 | Inversion: grammar-valid agent drafts create a validated write-inbox, easing the curator bottleneck | non-obvious (inversion) | write discipline (single-writer preserved) |

**Cross-cutting triage flags:** H1/H9/H20 and (partly) H19 compete for the *same slot* (a grammar for node content) with different engines — triage should pick one substrate, not fund four. H2→H3→H23 is a dependency chain (one grammar investment amortizes across three hypotheses). H14 composes with prior proven work rather than opening new surface.

---

## tree-sitter (incremental GLR, error-recovering CST, tiny dependency-free C/WASM lib)

### H1 — Write-time structural validation of node content
- **Statement:** tree-sitter could enhance `context_store`/`context_correct` of Unimatrix by parsing node content against a declarative grammar for the factory's templates (finding structure, `cites:` blocks, `done_when`, `proven_by`) at write time, flagging or rejecting malformed structure deterministically.
- **Mechanism:** error-recovering parse — tree-sitter produces a *usable tree from invalid input*, so a partially-malformed node yields a precise list of which sections parse and which don't, instead of a binary pass/fail or an LLM's judgment call. Runtime is a dependency-free C/WASM lib, so it can live inside the MCP server itself.
- **Target:** `context_store` / `context_correct`; indirectly the firewall (a `proven` grade requiring a well-formed `proven_by` block becomes machine-checkable — see also H17).
- **Class:** obvious · **Level-up vs linear:** linear (quality/discipline gain, same capability).
- **Cheapest test:** write a minimal grammar for the finding template; parse ~50 real nodes from the live KB; count (a) true malformations caught, (b) false rejections of legitimate free-text.
- **Key assumption:** node content is *conventional enough* to be grammatized — the free-text-plus-structure mix has a stable skeleton. **Biggest risk:** the KB's content is deliberately free-form; a grammar strict enough to catch errors may fight the "free-text + structured" design and generate false-positive friction.

### H2 — Typed event tree over the observation buffer
- **Statement:** tree-sitter could enhance `context_cycle_review` of Unimatrix by parsing the cycle's observation/transcript buffer with a purpose-built grammar into a typed event tree (tool-call spans, code blocks, gate markers, phase boundaries), making the per-phase timeline and hotspot analysis *structural* rather than heuristic text-scanning.
- **Mechanism:** GLR error recovery over messy, interleaved transcript text — the exact property that lets editors parse half-typed code lets a grammar parse a half-structured transcript and still emit a usable tree; ambiguity between overlapping span types is resolved by GLR's parallel stacks.
- **Target:** `context_cycle_review` (the owner-pondered target, taken structurally rather than lexically).
- **Class:** adjacent · **Level-up vs linear:** level-up — moves review from "search the text" to "query the structure" (e.g. *tool-calls inside a failed gate span*), a query class heuristics can't express.
- **Cheapest test:** hand-write a ~20-rule transcript grammar; parse one real completed cycle buffer; check that ≥90% of tool-call and gate spans are segmented correctly against a manual annotation.
- **Key assumption:** the buffer has enough syntactic regularity (tool-call markers, delimiters) to anchor a grammar. **Biggest risk:** transcript format is owned by the platform and may change without notice — the grammar becomes a maintenance liability coupled to an unstable upstream format.

### H3 — Online (in-cycle) hotspot detection via incremental re-parse
- **Statement:** tree-sitter could enhance `context_cycle` of Unimatrix by maintaining a *live* parse of the growing observation buffer — each append is an incremental edit touching only the new subtree — so hotspot/anti-pattern detection runs continuously during the cycle instead of post-hoc at review.
- **Mechanism:** incremental re-parse — the defining property: an append to an N-MB buffer costs ~the size of the appended region, not O(N). This is what makes *continuous* structural monitoring affordable where full re-parse per event would not be.
- **Target:** `context_cycle` / the observation pipeline (review's analysis moves upstream into the session).
- **Class:** non-obvious · **Level-up vs linear:** level-up — post-hoc review can only report; in-cycle detection can *intervene* (surface a lesson-learned mid-run, flag a retry loop while it's happening).
- **Cheapest test:** replay a real cycle buffer as a sequence of appends; measure incremental re-parse latency per append vs full re-parse; confirm sub-linear scaling holds on transcript-shaped input (not just code).
- **Key assumption:** depends on H2's grammar existing; and that the platform exposes the buffer *during* a cycle, not only at review (telemetry is named-cycle-only — this hypothesis works within that constraint but needs mid-cycle read access). **Biggest risk:** if the buffer is only readable at `context_cycle_review` time, the incremental property has nothing to attach to and the hypothesis dies on platform access, not on the technology.

### H4 — AST-granular embedding chunks for code-bearing nodes
- **Statement:** tree-sitter could enhance `context_search` of Unimatrix by chunking code-bearing node content at AST-node granularity (function, rule, config block) before embedding, so the 384-dim vectors represent coherent semantic units instead of arbitrary text windows.
- **Mechanism:** the concrete syntax tree gives semantically meaningful chunk boundaries for free — a capability no fixed-window or sentence chunker has on code; 384 dims is a small embedding space, so chunk coherence matters proportionally more than it would at 1536+.
- **Target:** `context_search` (embedding/indexing side).
- **Class:** adjacent · **Level-up vs linear:** linear (retrieval-precision gain).
- **Cheapest test:** take ~20 code-bearing nodes; embed once as-is and once at subtree granularity; run 10 known-answer queries; compare hit-rate/rank.
- **Key assumption:** a meaningful fraction of KB nodes carry code/config worth structural chunking. **Biggest risk:** the current KB is mostly prose findings — the addressable content may be too small for the gain to register; serves the theme broadly but possibly *this* use-case weakly (note per themes.md: score lens and value-target separately).

### H5 — Claim-level edges via stable subtree addressing (whitespace)
- **Statement:** tree-sitter could enhance `context_edge`/the graph model of Unimatrix by letting edges reference a *subtree path within* a node's parsed content, so `Supports`/`Contradicts` can point at the specific claim rather than the whole node.
- **Mechanism:** a parsed content tree gives every span a structural address (path of node kinds + positions); edges gain sub-node resolution without changing the node model — the tree is derived, not stored.
- **Target:** `context_edge`, `context_graph` (evidence topology).
- **Class:** non-obvious (whitespace — inverts the assumption that the node is the atomic unit of evidence).
- **Level-up vs linear:** level-up — `Contradicts` at node level is noisy (nodes contain many claims); claim-level contradiction is a different evidence instrument.
- **Cheapest test:** for 5 real Supports/Contradicts edges, hand-derive the subtree path of the actual claim; then apply a `context_correct`-style content edit and check whether the path survives or can be re-anchored.
- **Key assumption:** subtree paths are stable enough across edits/supersession to be worth storing in edge metadata. **Biggest risk:** `context_correct` reissues ids and rewrites content — paths may rot faster than they're useful, turning precision into dangling references.

### H6 — Structural diff across supersession chains
- **Statement:** tree-sitter could enhance `context_correct`/`context_graph(mode:"chain")` of Unimatrix by tree-diffing old vs new content at correction time and storing a machine-readable structural delta ("cites added, done_when changed, mechanism section untouched") alongside the chain.
- **Mechanism:** two concrete syntax trees admit a semantic diff (matched/moved/edited subtrees) that raw text diff cannot give; the same grammar as H1 is reused.
- **Target:** `context_correct`, lineage audit via `chain`.
- **Class:** non-obvious · **Level-up vs linear:** linear (audit-quality gain; chains become self-explaining).
- **Cheapest test:** pick 3 real supersession chains; produce tree-diffs; ask whether the delta summary answers "what changed and why" better than eyeballing both versions.
- **Key assumption:** H1's grammar exists (shared substrate). **Biggest risk:** low standalone value — worth doing only as a rider on H1, not as its own investment; triage should treat it as a bundle candidate.

## ast-grep (structural search/rewrite, `$VAR` meta-variables, parallel, `potential_kinds` pruning)

### H7 — A third retrieval mode: structural pattern match
- **Statement:** ast-grep could enhance retrieval in Unimatrix by adding structural pattern matching over code-bearing node content — `context_search` is semantic, `context_lookup` is exact-filter; neither can answer "find every node whose snippet calls `context_tag` with `action:"replace"`" — a `$VAR` pattern can, deterministically.
- **Mechanism:** meta-variable patterns match AST *shapes*, not strings — immune to formatting/renaming noise that defeats regex, and requiring no embedding similarity at all; `potential_kinds` pruning keeps a KB-wide sweep proportional to matching-kind nodes only.
- **Target:** the retrieval surface (a new primitive beside search/lookup).
- **Class:** obvious · **Level-up vs linear:** level-up *for code-bearing knowledge* (a query class neither existing tool can express); linear for the KB as it stands today.
- **Cheapest test:** export code-bearing node contents to files; run 5 ast-grep patterns answering real questions an agent has actually had (e.g. "which stored snippets use the deprecated store-then-deprecate idiom"); compare against context_search on the same questions.
- **Key assumption:** same as H4 — enough code in the KB to matter. **Biggest risk:** same corpus-thinness risk as H4; the two should be triaged together since they rise and fall on the same fact about KB composition.

### H8 — Deterministic convention codemods over the KB
- **Statement:** ast-grep could enhance `context_correct`-driven maintenance of Unimatrix by expressing convention migrations (cites-format changes, template renames, idiom deprecations) as rewrite rules swept deterministically across all node content, instead of an LLM rewriting each node with per-node drift risk.
- **Mechanism:** grammar-driven rewrite — `$VAR` capture + template substitution transforms exactly the matched structure and provably nothing else; parallel across nodes; the diff per node is mechanically identical, which is what makes a bulk `context_correct` sweep auditable.
- **Target:** `context_correct` (bulk), curator workflow.
- **Class:** adjacent · **Level-up vs linear:** linear (cost/reliability of maintenance).
- **Cheapest test:** take one past convention change (e.g. the grade-tag migration in recent commits); write it as a rewrite rule; dry-run over exported node contents; count correct/incorrect/missed transforms vs what was actually done by hand.
- **Key assumption:** KB conventions change often enough to amortize rule-writing. **Biggest risk:** node content is mostly prose — ast-grep needs a grammar for the content format (dependency on the H1 substrate) or applies only to embedded code islands, shrinking the addressable surface.

### H9 — Meta-variable extraction: lifting structure out of free text
- **Statement:** ast-grep could enhance content structuring in Unimatrix by using `$VAR` patterns as *extractors* — matching semi-structured islands in free-text nodes (`cites:` entries, `done_when:` clauses, `{type, ref, title}` tuples) and lifting them into structured fields, deterministically backfilling the KB.
- **Mechanism:** the same match machinery as H7, pointed at extraction instead of search: a pattern's captured meta-variables *are* the extracted record — no model, no hallucinated fields, and misses are explicit (no match) rather than silent fabrications.
- **Target:** write path / structured-content backfill; downstream everything that filters on structured fields.
- **Class:** non-obvious · **Level-up vs linear:** linear per node, but potentially level-up in aggregate if it unlocks structured queries over previously opaque prose.
- **Cheapest test:** write extraction patterns for `cites:` blocks; run over all findings in the KB; measure precision/recall against a hand-labeled sample of 30.
- **Key assumption:** the semi-structured islands follow their templates closely enough for shape-matching. **Biggest risk:** competes directly with H1 (parse everything with a grammar) and H20 (pika) for the same slot — triage should pick *one* structuring substrate; funding all three is waste.

### H10 — Dogfood lint bank over the factory's own method files
- **Statement:** ast-grep could enhance the factory's dogfood surface by encoding this repo's conventions (skill frontmatter shape, workflow-protocol structure, unimatrix-access rules like "never deprecate-then-store" in example snippets) as a rule bank run in CI/pre-commit — deterministic enforcement of what currently lives only in prompt discipline.
- **Mechanism:** the rule-config system (YAML rules + `potential_kinds`-pruned sweep) is built exactly for lint pipelines; markdown/YAML tree-sitter grammars exist, so the method files are parseable substrate.
- **Target:** the repo dogfood surface — **note: weak fit to the MCP tool surface itself** (serves the use-case's periphery, not a `context_*` capability; the theme allows this, scored separately).
- **Class:** adjacent · **Level-up vs linear:** linear.
- **Cheapest test:** encode 3 real conventions from `.claude/rules/unimatrix-access.md` as rules; run over the repo; check they catch a deliberately-planted violation and pass the current tree.
- **Key assumption:** prompt-discipline violations actually occur at a rate worth automating (the retros would show this). **Biggest risk:** conventions here are *semantic* ("grade moves only via context_tag") more than *syntactic* — the lintable fraction may be small.

## RE2 / Hyperscan (linear-time DFA, multi-pattern SIMD, streaming, bounded memory)

### H11 — Multi-pattern hotspot bank for cycle review
- **Statement:** Hyperscan could enhance `context_cycle_review` of Unimatrix by compiling a bank of hundreds-to-thousands of anti-pattern signatures (retry loops, error strings, permission-prompt storms, gate-failure markers, tool-call sequences symptomatic of thrash) into one automaton and streaming the observation buffer through it in a single pass at ms/MB cost.
- **Mechanism:** simultaneous multi-pattern matching — Hyperscan's graph decomposition matches *thousands* of patterns in one streaming scan with bounded memory; the pattern-count-at-no-marginal-cost property is what turns "grep for a few known smells" into "screen against the factory's entire accumulated smell library on every review."
- **Target:** `context_cycle_review` (the owner-pondered target, taken lexically — complementary to H2's structural take, not competing: this needs no grammar and works today).
- **Class:** obvious · **Level-up vs linear:** linear at small pattern counts; level-up once the bank grows past what per-regex scanning could afford — the lessons-learned corpus itself becomes the pattern source (each lesson compiles to a signature), making review sharpen automatically as the KB grows.
- **Cheapest test:** hand-derive ~50 signatures from existing lesson-learned nodes and past retro observations; scan one completed cycle buffer; compare hits against what the manual retro actually flagged.
- **Key assumption:** the hotspots worth catching have lexical signatures at all. **Biggest risk:** the interesting failures are semantic/sequential (visible only in event *order* or *phase structure*) — exactly the residue H2 exists for; a lexical bank might catch the trivial 60% and mislead review into thinking coverage is complete.

### H12 — Hybrid retrieval: exact-identifier channel beside embeddings
- **Statement:** RE2/Hyperscan could enhance `context_search` of Unimatrix by running a deterministic exact-pattern channel (tool names, node ids, tags, error strings, version strings) in parallel with 384-dim vector similarity and fusing the ranks — fixing the known weakness of small embeddings on rare exact identifiers.
- **Mechanism:** guaranteed-linear-time matching with no pathological inputs (RE2's no-backtracking DFA) makes it safe to run *every* query through a large identifier-pattern bank as a free side-channel; embeddings blur `context_tag` vs `context_get` — a DFA never does.
- **Target:** `context_search` (ranking).
- **Class:** adjacent · **Level-up vs linear:** level-up for identifier-shaped queries (a failure class goes away), linear overall.
- **Cheapest test:** collect ~10 real queries where search returned poor results on exact-identifier intent (the scout's own reuse-search noise — "semantically adjacent by keyword, not mechanism" — is evidence this class exists); measure recall@5 with and without the lexical channel.
- **Key assumption:** identifier-blindness is a real, recurring miss pattern in this KB, not an anecdote. **Biggest risk:** rank fusion is where hybrid search projects die — a bad fusion heuristic can *worsen* the common case to fix the rare one.

### H13 — Write-time secret/PII scan → auto-quarantine
- **Statement:** RE2/Hyperscan could enhance `context_store` + `context_quarantine` of Unimatrix by scanning every incoming node against a secret/PII/credential pattern bank at write time and routing hits to quarantine automatically, at deterministic bounded cost per write.
- **Mechanism:** multi-pattern single-pass scan (the DPI/IDS design center of Hyperscan, per the scout's NSDI cite) — the entire secret-pattern corpus (the same families gitleaks/trufflehog encode) applied as one automaton at negligible per-node cost.
- **Target:** `context_store` write path, `context_quarantine` lifecycle.
- **Class:** adjacent · **Level-up vs linear:** linear (a safety property the write path currently lacks entirely — arguably a small step-function from "none" to "systematic").
- **Cheapest test:** run a standard secret-pattern set over the *existing* KB export — if it finds anything, the hypothesis proves its value retroactively in one afternoon; if clean, measure cost-per-write to decide if prevention is nearly free anyway.
- **Key assumption:** agents occasionally paste env vars, tokens, or personal data into findings (base rates elsewhere say yes). **Biggest risk:** false-positive quarantines adding friction to the single-writer path; entropy-based token patterns are noisy.

### H14 — Composition: DPI-grade egress filtering (upgrades shd-006)
- **Statement:** Hyperscan could enhance the egress-enforcement capability proven in shd-006 by replacing per-rule checking with streaming multi-pattern scanning — thousands of egress rules (secrets, internal hostnames, PII shapes) evaluated in one pass over outbound content with bounded memory over unbounded streams.
- **Mechanism:** streaming mode — match state persists across chunk boundaries with fixed memory, so outbound data can be scanned *as it flows* rather than buffered whole; this is literally the IDS workload the engine was built for, transplanted.
- **Target:** the egress filter (existing proven `technology` node from shd-005/006 — a `Prerequisite` composition, not new surface).
- **Class:** adjacent (composition with existing proven work) · **Level-up vs linear:** linear at today's rule counts; level-up if the confidence-gated routing vision needs rule counts that per-regex evaluation can't sustain.
- **Cheapest test:** benchmark the current shd-006 filter's pattern-set on Hyperscan vs its existing engine on a sample stream; also measure the actual memory envelope (the scout's 32–64 MB figure is secondary-sourced — verify it, don't inherit it).
- **Key assumption:** the egress filter's rule set will grow enough to need this. **Biggest risk:** premature optimization — if shd-006's rule count stays at dozens, the engine swap buys integration cost for no felt gain.

### H15 — Reverse search: the knowledge base watches the session (whitespace)
- **Statement:** Hyperscan could enhance `context_briefing` of Unimatrix by *inverting retrieval*: compile a signature pattern (or several) per KB node into one bank, stream the live session transcript through it, and let matches trigger proactive surfacing — knowledge finds the agent at the moment of relevance, instead of waiting for the agent to know what to search for.
- **Mechanism:** the thousands-of-patterns-at-once property is the entire trick — one pattern per node is exactly the workload shape (n patterns, one stream) that Hyperscan's decomposition was designed for and that per-regex scanning makes unaffordable; streaming mode means the session is scanned as it happens, bounded memory, no batch step.
- **Target:** `context_briefing` (from session-start pull to continuous push); composes with the confidence/usage telemetry per node (hit-rates feed back into signature quality).
- **Class:** non-obvious / whitespace — inverts the query direction of the entire retrieval surface.
- **Level-up vs linear:** level-up — "you don't know what you don't know" is the standing failure mode of pull-retrieval (agents skip the search they didn't think to run); push-retrieval attacks the failure class itself, and it compounds: every stored node makes the watcher smarter at zero marginal scan cost.
- **Cheapest test:** derive signatures (distinctive terms, tool idioms, error strings) for ~50 nodes; replay 3 historical session transcripts through the bank; score precision (were surfaced nodes actually relevant at that moment?) and the money metric — did it surface a node the agent *demonstrably needed and never searched for*? One such hit validates the mechanism.
- **Key assumption:** nodes admit *distinctive* lexical signatures (auto-derivable, or authored by the curator per node). **Biggest risk:** the signature-derivation problem is the hard part hiding behind the easy matcher — generic signatures → alert fatigue and the feature gets ignored; this may quietly need an SLM/embedding assist for signature quality, eroding the pure-deterministic envelope claim.

### H16 — Regular path queries over the graph
- **Statement:** DFA machinery could enhance `context_graph` of Unimatrix by supporting regular path queries — path constraints written as regexes over edge-type labels (e.g. `Motivates · Prerequisite+ · Advances`: "findings that motivated a technology chain ultimately advancing a goal") evaluated as the product of the automaton with the graph.
- **Mechanism:** the classical RPQ construction — compile the label-regex to a tiny DFA, run BFS over (node, automaton-state) product pairs; linear in graph×states, no backtracking, and the six-edge-type alphabet (D8) makes the automata trivially small. This is the *theory* the family rests on applied to the graph rather than to text — no engine dependency, just the automaton.
- **Target:** `context_graph` (a new query mode beside chain/neighbors/subgraph/path).
- **Class:** non-obvious · **Level-up vs linear:** level-up — multi-hop *typed-sequence* questions ("full provenance from finding to goal") currently require agents to chain multiple graph calls and reassemble by hand; one declarative query replaces an error-prone orchestration.
- **Cheapest test:** export the current graph; implement product-BFS in ~100 lines for one query (`Motivates · Prerequisite* · Advances`); compare its answer and call-count against an agent doing it today via chained `context_graph` calls.
- **Key assumption:** multi-hop typed-path questions recur often enough in factory practice (funnel provenance queries suggest yes). **Biggest risk:** this is a platform feature request on Unimatrix, not a bolt-on — value is real but delivery depends on the Unimatrix roadmap, which triage must weigh as effort, not just fit.

### H17 — Tag-grammar enforcement at write time
- **Statement:** RE2 could enhance `context_tag`/`context_store` of Unimatrix by validating every tag against the factory's tag grammar (`grade:` ∈ {missing,claimed,partial,proven}, `theme:<slug>`, run-id shape, the "never a tag literally named status" rule) at write time — mechanically enforcing what `.claude/rules/unimatrix-access.md` currently enforces by prompt.
- **Mechanism:** linear-time anchored matching with guaranteed no pathological cost — cheap enough to sit inline on every write; the tag conventions are already regular expressions in prose form, so the encoding is direct.
- **Target:** `context_tag`, `context_store`; the firewall's audit trail (bad grades become impossible rather than findable).
- **Class:** obvious · **Level-up vs linear:** linear (small, cheap, closes a real discipline gap — the ~60/hr rate-limit makes each wasted malformed tag-write doubly costly).
- **Cheapest test:** write the tag regexes; run over all existing tags in the KB; count violations already present (a nonzero count both proves need and pays for the test).
- **Key assumption:** tag drift actually occurs. **Biggest risk:** near-zero — the risk is opportunity cost only; triage should note this is almost too small to be a proof-goal by itself (bundle with H13 as "write-path deterministic guards").

### H18 — Canonicalize-then-hash: near-duplicate detection
- **Statement:** RE2 could enhance dedup in Unimatrix by canonicalizing content (strip timestamps, run-ids, whitespace variance, formatting noise via a fixed regex pipeline) *before* content-hashing, so `content_hash` catches trivially-varying re-statements that byte-exact hashing misses.
- **Mechanism:** deterministic normalization — a fixed, ordered set of linear-time rewrites yields a canonical form; equality on the canonical form is a strictly larger (still exact, still cheap) equivalence class than raw-byte equality. (Alternative substrate: tree-sitter parse→normalize→re-serialize gives *structural* hashing — note for triage as the stronger/costlier variant of the same idea.)
- **Target:** the `content_hash` dedup property; reuse-first discipline (near-dup findings across runs are the failure mode).
- **Class:** non-obvious · **Level-up vs linear:** linear.
- **Cheapest test:** canonicalize all existing node contents; re-hash; count new hash collisions and hand-check whether they are genuine near-dups (any true positive on the current KB is the confirmation).
- **Key assumption:** near-dups entering the KB differ mostly by *surface noise*, not paraphrase. **Biggest risk:** real duplicates are paraphrases — a semantic problem regex canonicalization cannot touch, in which case this catches ~nothing and embedding-similarity dedup was the actual answer.

## PEG / packrat / pika (deterministic linear-time single parse; memory caveat on large inputs)

### H19 — A runtime-extensible query DSL
- **Statement:** a PEG parser could enhance Unimatrix's query surface by providing a small, runtime-extensible DSL that composes today's separate primitives (lookup filters + graph traversal + grade/tag predicates) into one declarative expression — the DuckDB runtime-extensible-SQL precedent the scout cites, at knowledge-engine scale.
- **Mechanism:** PEG's ordered choice is closed under composition — new grammar rules can be added at *runtime* without regenerating parser tables (the property GLR/table-driven parsers lack), so the DSL can grow per-deployment; packrat's memory caveat is irrelevant at query-string sizes (bytes, not MB — the anti-edge flag does not bind here).
- **Target:** the query surface as a whole (`context_lookup` + `context_graph` composition).
- **Class:** non-obvious · **Level-up vs linear:** level-up — agents currently orchestrate multi-call query plans by hand (the D5 intent-table in the access rules exists precisely because choosing/chaining tools is error-prone); a query language collapses that class of orchestration error.
- **Cheapest test:** define a 10-rule grammar covering the three most common composite queries from real factory transcripts; parse-and-plan them against the existing tools (parser emits a call plan, no engine change); check an agent using the DSL makes fewer/correcter calls than one using the raw tools.
- **Key assumption:** the multi-call orchestration burden is a measured pain (cycle_review hotspot data could confirm — nice reflexive loop). **Biggest risk:** DSLs for LLM agents can *underperform* raw tools — models are heavily pretrained on the tool-call idiom but not on your invented syntax; the fix might be worse than the disease. Also a platform feature, same effort caveat as H16.

### H20 — Error-recovering field extraction from malformed agent output
- **Statement:** the pika parser could enhance Unimatrix's write path by parsing agent-produced node drafts with recovery — extracting every well-formed template field from a partially-malformed draft and pinpointing exactly where structure broke, rather than rejecting wholesale or accepting silently.
- **Mechanism:** pika's bottom-up right-to-left dynamic programming recovers *all* parseable fragments after an error (classic recursive-descent PEG stops dead) — the specific published improvement over standard packrat, per the scout's Hutchison cite; node-sized inputs keep the memoization-memory caveat unbound.
- **Target:** `context_store`/`context_correct` intake.
- **Class:** adjacent · **Level-up vs linear:** linear.
- **Cheapest test:** collect ~10 real malformed drafts (from transcripts where the curator had to fix agent output); run a pika-based template parser; count fields correctly recovered vs a strict parser's all-or-nothing.
- **Key assumption + biggest risk:** **this occupies the same slot as H1 (tree-sitter, also error-recovering) and H9 (ast-grep extraction)** — the honest framing is *substrate bake-off, not independent hypothesis*. Triage should fund at most one of H1/H9/H20, chosen by a head-to-head on recovery quality and integration cost; pika's risk specifically is ecosystem thinness (one 2020 implementation vs tree-sitter's decade of production hardening).

## Grammar-constrained decoding (GBNF / llguidance / outlines — the LM-boundary member; envelope-exception, keep firewall tight)

### H21 — Grammar-guaranteed node emission from small local models
- **Statement:** grammar-constrained decoding could enhance Unimatrix's write path by letting a small quantized on-device model (llama.cpp + GBNF) emit template-valid node content in a single pass — the grammar carries all structural correctness, so model size buys only content quality, not validity.
- **Mechanism:** per-step logit masking against the template grammar — tokens that cannot extend a valid parse are unsampleable, so *no* output is structurally invalid, ever, regardless of model size; this deletes the retry/validate/repair loop that is precisely where small models bleed tokens and reliability. The scout's envelope-exception logic in one line: the determinism is in the grammar, the model is just the fill.
- **Target:** write path (`context_store` intake); the shd-N4 edge/multi-machine story (a Pi-class node capturing knowledge locally with guaranteed-valid structure).
- **Class:** obvious (for this candidate) · **Level-up vs linear:** level-up *for the edge story* — it's the difference between "edge devices can capture knowledge reliably" and "edge devices need a frontier model in the loop"; linear for the datacenter path where big models already mostly comply.
- **Cheapest test:** write a GBNF grammar for the finding template; run a ~3–4B quantized model on 20 extraction/authoring tasks, constrained vs unconstrained; measure valid-first-pass rate, retry count, and tokens/task — this doubles as the envelope-exception confirmation triage asked for (footprint reduction material, not assumed).
- **Key assumption:** structural invalidity (not content quality) is the binding failure mode of small-model authoring. **Biggest risk:** grammar-valid ≠ true — masking guarantees shape, and a confidently-shaped hallucination is *more* dangerous to the KB than a malformed one, because nothing downstream looks wrong. The firewall (curator review, grades) must not be relaxed one inch on the basis of validity; the scout's "don't over-claim" flag applies squarely here.

### H22 — Machine-consumable cycle-review output
- **Statement:** grammar-constrained decoding could enhance `context_cycle_review` of Unimatrix by constraining the review's generated report to a JSON grammar (phases, hotspots, gate outcomes, knowledge-yield as typed fields), making review output a data artifact that downstream automation — funnel metrics, the A/B telemetry loop in this very agent-def's footer — can consume without a parsing step that can fail.
- **Mechanism:** JSON-Schema-driven masking (llguidance's design center) — the report is valid against the schema at generation time, by construction; the "measured, not asserted" improvement loop needs machine-readable review output as its substrate, and this removes the flakiest link (free-text report → ad-hoc parse).
- **Target:** `context_cycle_review` (output side); the factory's reflexive telemetry loop (§9).
- **Class:** adjacent · **Level-up vs linear:** linear (reliability of an existing flow, but it *unblocks* the measurement loop, which has option value).
- **Cheapest test:** define the review-report schema; run one cycle review with constrained output; feed it to a 20-line metrics script; confirm zero parse failures across 3 cycles.
- **Key assumption:** review generation runs somewhere a sampler can be constrained (local/open model or an API exposing structured-output constraints) — if review is generated by a closed model without grammar hooks, the mechanism has no attachment point. **Biggest risk:** exactly that platform question; also schema rigidity suppressing the free-text observations that make retros valuable — the grammar must leave a prose field open.

### H23 — On-device knowledge extraction at cycle close
- **Statement:** grammar-constrained decoding composed with an SLM could enhance Unimatrix's knowledge-yield pipeline by extracting candidate findings/lessons-learned from the cycle's observation buffer *on-device* at cycle close — grammar guarantees each candidate arrives in valid template form; the frontier model (or human) only judges, never reformats.
- **Mechanism:** the composition is the point — H11/H2 machinery *locates* hotspot regions cheaply and deterministically; the SLM reads only those small regions; the grammar makes its output structurally perfect. Each stage covers the previous one's weakness: automata can't summarize, SLMs can't be trusted with structure, grammars can't find anything. Total envelope: one quantized model + automata — no frontier call in the extraction loop.
- **Target:** the knowledge-yield step of `context_cycle_review` → curator intake; the compounding-asset objective directly (yield-per-cycle is the factory's own metric).
- **Class:** non-obvious (composition) · **Level-up vs linear:** level-up if extraction cost is currently why yield is lower than it should be — cheap extraction means *every* cycle tithes knowledge, not just the ones that get a full retro.
- **Cheapest test:** take one completed cycle buffer; run hotspot-locate (even grep-grade) → SLM+grammar extraction; have the curator judge the candidates against what the actual human retro extracted from the same cycle — overlap and novel-catch rate are the numbers.
- **Key assumption:** extraction (not judgment) is the expensive step in today's yield pipeline. **Biggest risk:** garbage-yield — a cheap extractor that emits plausible, valid, mediocre findings *shifts* the cost to curator triage rather than removing it, and could bloat the KB with well-formed noise; the quarantine/enroll lifecycle would need to gate this intake from day one.

### H24 — Inversion: the validated write-inbox
- **Statement:** grammar-constrained decoding could enhance Unimatrix's write discipline by removing the constraint it targets — malformed agent writes — thereby enabling a *validated draft inbox*: any agent may emit grammar-guaranteed-valid draft nodes into a staging queue (quarantine lifecycle), and the single-writer curator's job compresses from "reformat and verify structure and judge" to "judge and file."
- **Mechanism:** the inversion move on the family's constraint. Structural validity is currently entangled with the trust argument for single-writer; grammar masking cleanly *separates* them — validity becomes free and universal, so what remains of single-writer is exactly its true core (auditability + firewall judgment), now cheaper to operate because every intake item is already well-formed. `context_quarantine`/`context_enroll` are the staging primitives already on the surface.
- **Target:** write discipline / curator throughput; `context_quarantine` → `context_enroll` flow.
- **Class:** non-obvious (inversion) · **Level-up vs linear:** level-up for factory throughput if curator intake is (or becomes, at multi-goal scale — see the multi-goal focus) the bottleneck; irrelevant if it isn't.
- **Cheapest test:** measure first — instrument one full run for curator time split between *reformatting/structural fixing* vs *judging*; if reformatting is a material fraction, pilot the inbox on one specialist's output for one run.
- **Key assumption:** curator time is meaningfully spent on structure, not judgment (unmeasured — the test is the measurement). **Biggest risk:** mis-read as a proposal to weaken single-writer — it is not; the risk is social/architectural, that a validated inbox normalizes drift toward multi-writer and erodes the firewall's auditability, which validity does nothing to protect. The D-decisions boundary must be restated in any POC scope.

---

## Flags for the leader / triage
1. **Substrate collision (biggest triage economy):** H1 / H9 / H20 (and H19's parser choice) all want "a grammar over node content" — fund a bake-off or pick one substrate; four parallel proof-goals here would be waste. tree-sitter's maturity vs pika's recovery vs ast-grep's extraction ergonomics is the actual question.
2. **Dependency chains:** H2 → H3 → (feeds) H23; H1 → H6; H11's pattern bank ← lessons-learned corpus (reflexive loop). H14 rides on proven shd-006 work.
3. **Platform-feature vs bolt-on split:** H16, H19 (and partly H5) require Unimatrix engine changes — different effort class than agent-side bolt-ons (H8, H10, H11-as-script); triage should weight effort accordingly.
4. **Envelope verification debt:** no candidate has first-party numbers (scout flag) — every cheapest-test above includes measuring the envelope it assumes; do not inherit the secondary-sourced MB/ms figures into any proof-goal's `done_when`.
5. **#5-family firewall watch:** H21–H24 touch an LM; per the scout, keep them framed as grammar-does-correctness, and the H21 test doubles as the envelope-exception confirmation triage owes itself.
6. **Use-case-fit caveats (theme allows, score separately):** H4/H7 depend on how much *code* the KB actually holds (thin today); H10 serves the repo periphery, not the MCP surface.
7. **Nothing here is graded.** 24 conjectures, all `claimed` at most; class distribution — 5 obvious, 9 adjacent, 10 non-obvious/whitespace/inversion.
