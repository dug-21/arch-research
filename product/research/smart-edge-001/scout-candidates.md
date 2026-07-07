# scout-candidates.md — theme-scan `smart-edge-001`

**Theme:** `theme:smart-edge` · **Source:** owner-injection · **Seed:** Lextrait, *"Under Claude Code's Hood: Generative Grammars Doing the Heavy Lifting"* (LinkedIn) · **agent_id:** `smart-edge-001-scout`

**Reuse-first result:** Searched Unimatrix (`technology` + `finding`) for the generative-grammar / GLR / tree-sitter / ast-grep / FSA-regex / PEG / grammar-constrained-decoding family and near neighbors. **No existing node covers this family.** All returned hits (`#41 SGLang`, `#39 vLLM`, `#15 Goose`, `#11 aider`, `#48 Codestral-Mamba`, `#76 output-confidence signals`, `#80 egress filter`) are LLM-inference / harness / routing tech from prior `shd-004/005` runs — semantically adjacent only by keyword ("decoding", "lightweight"), not the same mechanism. **Every candidate below is NEW.** None should be treated as re-surfaced.

## Candidate list
1. **tree-sitter** (incremental GLR parsing engine) → **in-lens** → **new**
2. **ast-grep** (grammar-driven structural search/rewrite) → **in-lens** → **new**
3. **DFA/FSA regex engines** (RE2, Hyperscan) → **in-lens** → **new**
4. **PEG / packrat parsers** (incl. pika reformulation) → **in-lens (with envelope caveat)** → **new**
5. **Grammar-constrained decoding** (GBNF / llguidance / outlines) → **borderline-in via envelope-exception** → **new**

> **Family note for the hypothesizer:** these are one *family* (deterministic, grammar/automata-based text & pattern processing) but **five distinct filings** because mechanism and resource envelope differ materially. #2 is built *on* #1; #5 is the only one that touches an LM at all. Keep them separate — each offers a different capability primitive.

---

## 1. tree-sitter — incremental GLR parsing engine

**What it is / how it works.** A parser-generator + runtime that turns a declarative grammar into a fast, error-tolerant parser producing a concrete syntax tree. Uses an **incremental GLR** algorithm (a generalized LR parser — Lang 1974 lineage): ambiguity is resolved at compile-time via precedence annotations and at run-time via GLR's parallel-stack exploration. Its defining property is **incremental re-parse**: on an edit it updates only the affected subtree rather than re-parsing the file, and it is **error-recovering** (produces a usable tree from incomplete/invalid source). Written in **C** (plus a Rust CLI/generator); the runtime is a small C library with **no runtime dependencies**, embeddable via WASM and bindings for ~15 languages.

**Resource envelope.** Compiled grammars are C tables; the runtime is a small self-contained library (order hundreds of KB, no heap of dependencies). Parse-tree memory scales ~linearly with source size. Incremental edits touch only changed nodes, which is why editors (Neovim, Emacs, Zed, Helix) run it **on every keystroke** on large files without lag — i.e. effectively sub-millisecond incremental updates on typical edits. It runs fully **on-device, CPU-only, deterministic, zero network**. *Concrete throughput/MB and steady-state memory figures I could NOT verify from a primary benchmark (Wikipedia and repo give none); the "faster than clangd / real-time in editors" claims are qualitative and widely reproduced but I have no attached numbers.*

**Maturity & evidence.** **Demonstrated (high):** production-embedded in GitHub code-nav, Neovim, Emacs 29+, Zed, Helix, Atom, and reportedly Claude Code's parsing path (the seed's central claim — author-report, not independently verified by me). Mature since 2018, broad grammar ecosystem. **Doc-claim/unverified:** exact memory/latency numbers; the specific internal role inside Claude Code.

**cites:**
- `{type: docs, ref: https://en.wikipedia.org/wiki/Tree-sitter_(parser_generator), title: "Tree-sitter (parser generator) — Wikipedia"}`
- `{type: repo, ref: https://github.com/tree-sitter/tree-sitter, title: "tree-sitter/tree-sitter — incremental parsing system"}`
- `{type: blog, ref: https://www.linkedin.com/pulse/under-claude-code-hood-generative-grammars-doing-heavy-lextrait-j0f7c/, title: "Under Claude Code's Hood: Generative Grammars (Lextrait)"}` *(secondary thought-piece / seed)*

**Source signal:** owner-injection.
**Lens rationale:** Small dependency-free C library doing deterministic syntactic analysis in real time on-device — replaces an LLM call for syntactic precision at near-zero compute. Passes the include-test on footprint.

---

## 2. ast-grep — grammar-driven structural search & rewrite

**What it is / how it works.** A Rust CLI ("`grep`, but on AST nodes") for **structural search, lint, and rewrite** across many languages — the seed's "ast-sed / ast-awk." Patterns are written as ordinary code with `$VAR` meta-variables that match AST subtrees; it parses source with **tree-sitter** (so it inherits #1's substrate), then matches/rewrites nodes. Optimization: each rule carries `potential_kinds`, so nodes whose kind can't match are skipped during traversal (no wasted subtree descent).

**Resource envelope.** Rust, **CPU-only, multi-core**, no model, no network. Cost ≈ one tree-sitter parse per file + a filtered tree walk — i.e. proportional to code size, cache-friendly, trivially parallel across files. Designed to sweep large codebases interactively. *The "10X faster after optimization" figure is the project's own engineering-blog author-report; I could NOT verify an independent throughput benchmark.*

**Maturity & evidence.** **Demonstrated (high):** widely adopted OSS structural-search/codemod tool with a stable pattern DSL and rule config; used in real CI/lint pipelines. **Doc-claim/unverified:** specific speed multipliers (self-reported). Distinct from #1 because it offers a *search-and-transform capability*, not just a parse tree — worth its own node.

**cites:**
- `{type: repo, ref: https://github.com/ast-grep/ast-grep, title: "ast-grep — CLI for code structural search, lint, rewriting (Rust)"}`
- `{type: docs, ref: https://ast-grep.github.io/advanced/how-ast-grep-works.html, title: "How ast-grep Works: A bird's-eye view"}`
- `{type: blog, ref: https://ast-grep.github.io/blog/optimize-ast-grep.html, title: "Optimize ast-grep to get 10X faster"}`

**Source signal:** owner-injection.
**Lens rationale:** Deterministic, on-device pattern-match-and-rewrite over structure — does mechanically what an LLM is often asked to do for code edits, at negligible compute. In-lens.

---

## 3. DFA/FSA regex engines — RE2 & Hyperscan

**What it is / how it works.** Finite-state-automata pattern recognizers. **RE2** compiles a regex to a **DFA** and matches in **guaranteed linear time with no backtracking** (immune to catastrophic-backtracking blowup). **Hyperscan** (Intel) targets **multi-pattern** matching (thousands of regexes at once) via graph decomposition into string + FA matching, **SIMD-accelerated**, streaming-capable — built for deep-packet-inspection / IDS. This is the "classical automata" wing of the family: not parsing structure but recognizing/classifying patterns deterministically.

**Resource envelope (most concrete of the set — but secondary-sourced).** From a DPI/IDS survey: **RE2 ~8–16 MB, ~10–15 ms/MB**; **Hyperscan ~32–64 MB, ~2–5 ms/MB** with SIMD, reported **8.7× Snort throughput** on real traffic and up to **10.3× over RE2 / 2.3× over PCRE2**. All CPU-only, deterministic, streaming (bounded memory over unbounded input). *These figures come from a secondary survey (arXiv/ACM summaries), not a first-party benchmark I ran — treat as author-report; the ranking (Hyperscan > RE2 > PCRE) is robust and widely reproduced, the exact ms/MB less so.*

**Maturity & evidence.** **Demonstrated (very high):** RE2 (Google) and Hyperscan (Intel/open-sourced) are battle-tested in production search, security, and networking for a decade+. **Doc-claim/unverified:** the precise numbers above.

**cites:**
- `{type: paper, ref: https://dl.acm.org/doi/10.5555/3323234.3323286, title: "Hyperscan: a fast multi-pattern regex matcher for modern CPUs (NSDI'19)"}`
- `{type: paper, ref: https://arxiv.org/pdf/0803.0037, title: "A Survey on Deep Packet Inspection for Intrusion Detection Systems"}`
- `{type: repo, ref: https://github.com/google/re2, title: "google/re2 — linear-time DFA regex engine"}`

**Source signal:** owner-injection (surfaced by scout as family kin, not named in seed).
**Lens rationale:** Classic linear-time, bounded-memory deterministic pattern recognition — the archetypal smart-edge primitive. Strongly in-lens.

---

## 4. PEG / packrat parsers (incl. pika reformulation)

**What it is / how it works.** Parsing Expression Grammars: an unambiguous, ordered-choice grammar formalism. **Packrat** parsing memoizes every (rule, position) result to guarantee **linear-time** recursive-descent parsing. The **pika parser** reformulates packrat as bottom-up, right-to-left dynamic programming, keeping linear time **and** gaining direct/indirect **left-recursion** support plus better error recovery. Represents the deterministic-single-parse alternative to GLR (no ambiguity, no parallel stacks).

**Resource envelope — the caveat filing.** Linear *time*, but classic packrat's **memory ∝ input size × grammar-dependent constant** (it memoizes essentially everything, including the full input) — that constant can be large, which is **anti-edge for big inputs**. Mitigations exist: Mizushima et al. show practical grammars run in "**mostly constant space**" with cut operators; pika keeps linear time with different memory behavior. So the envelope is **acceptable-with-tuning, not free** — the hypothesizer must weight this. CPU-only, deterministic, no model.

**Maturity & evidence.** **Demonstrated (high):** PEG/packrat is decades-old, widely implemented (e.g. runtime-extensible SQL parsers in DuckDB); pika is newer (2020, peer-reviewed) but implemented and published. **Doc-claim/unverified:** real-world memory numbers are grammar- and input-specific; I have no concrete MB figure to attach.

**cites:**
- `{type: paper, ref: https://arxiv.org/pdf/cs/0603077, title: "Packrat Parsing: Simple, Powerful, Lazy, Linear Time (Ford)"}`
- `{type: paper, ref: https://arxiv.org/pdf/2005.06444, title: "Pika parsing: reformulating packrat parsing as dynamic programming (Hutchison)"}`
- `{type: paper, ref: https://kmizu.github.io/papers/paste513-mizushima.pdf, title: "Packrat Parsers Can Handle Practical Grammars in Mostly Constant Space"}`

**Source signal:** owner-injection (scout-surfaced family kin).
**Lens rationale:** Deterministic linear-time parsing on-device — in-lens, but flagged: naive packrat's memory footprint can violate the include-test on large inputs unless the space-optimized/pika variant is used.

---

## 5. Grammar-constrained decoding — GBNF / llguidance / outlines

**What it is / how it works.** A deterministic **grammar overlay on an LM's sampler**: at each decode step, candidate tokens are tested against a grammar (GBNF / Lark-style CFG / JSON-Schema) and any token that can't extend a valid parse has its logit masked to −∞. Guarantees the output is *always* grammatically valid (valid JSON, valid syntax) in a single pass — no retry loop, no post-hoc validation. **llguidance** and **outlines** are fast implementations; GBNF is llama.cpp's built-in form. This is the family's **bridge to the LM boundary**: the grammar (deterministic, classical) does the correctness work; the model only fills content.

**Resource envelope.** The grammar machinery itself is tiny (a parser/automaton over the token vocabulary); the cost is a **per-token mask computation** whose overhead is small for simple grammars but "can significantly impact generation speed" for complex ones. llama.cpp skips the mask when the sampled token is already grammar-valid; llguidance is engineered for real-time. Research (CFGzIP / token-space compression) reports **10–20× latency reduction on the masking step, 2–7.5× total** on complex grammars — *arXiv author-claims, unverified by me.* Net edge relevance: it lets a **smaller/quantized model reliably emit valid structured output**, cutting the need for a larger model or multi-shot retry.

**Maturity & evidence.** **Demonstrated (high):** shipped in llama.cpp, vLLM, outlines, guidance — used daily for structured output on local models. **Doc-claim/unverified:** the specific speedup multipliers; the general "constraining shrinks the model you need" claim is plausible-but-unquantified here.

**cites:**
- `{type: docs, ref: https://deepwiki.com/ggml-org/llama.cpp/7.3-grammar-and-structured-output, title: "Grammar and Structured Output — llama.cpp (GBNF)"}`
- `{type: repo, ref: https://github.com/guidance-ai/llguidance, title: "llguidance — constrained decoding library (CFG/JSON-Schema)"}`
- `{type: paper, ref: https://arxiv.org/html/2502.14969v1, title: "Lost in Space: Optimizing Tokens for Grammar-Constrained Decoding"}`

**Source signal:** owner-injection (scout-surfaced as the family's LM-boundary member).
**Lens rationale:** **Borderline — admitted via the reduce-the-envelope exception, flagged.** It is *not* an LLM and does *not* itself shrink a model; it is a deterministic grammar technique whose edge value is enabling a *smaller* model to produce reliably valid output (fewer retries, smaller model sufficient). Include-test is *conditionally* met — the hypothesizer/triage should confirm the footprint-reduction is material, not assumed.

---

## Flags for the leader / hypothesizer / triage
- **Reuse:** 0 existing nodes cover this family — all 5 are genuinely new; nothing to dedup against.
- **Envelope evidence is uneven.** #3 has the only concrete (but *secondary-sourced*) numbers; #1, #2, #4 rest on qualitative "real-time in editors / 10× / linear-time" claims — **no first-party benchmark attached to any candidate.** A POC would need to measure actual footprint on Unimatrix-relevant workloads.
- **#4 (packrat) and #5 (constrained decoding) carry lens caveats** — packrat's memory can violate the include-test on large inputs; constrained-decoding rides the SLM envelope-exception and should be confirmed, not assumed, at triage.
- **#5 is the only candidate touching an LM** — keep the firewall tight so it isn't mis-read as general LLM work.
- All candidates are **`claimed` at most** — discovery moved structure only; nothing is proven, no POC run by me.
- The seed's specific assertion that tree-sitter/GLR is load-bearing *inside Claude Code* is **author-report (Lextrait), not independently verified** — do not file it as fact.

**Curator note:** file all 5 as `technology`, `grade:claimed`, tagged `theme:smart-edge` + `smart-edge-001`. #2 `Prerequisite`→#1 relation is a candidate edge for the curator's judgment (ast-grep depends on tree-sitter).
