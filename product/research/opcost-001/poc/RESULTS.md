# POC RESULTS — B1 feasibility, demonstrated on real captured data

*Run `opcost-001` · artifact `opcost_poc.py` · executed 2026-07-10 on this machine (Claude Code v2.1.205)*

**Claim demonstrated:** Per-repo, per-day Claude token usage is reconstructable from local transcripts (`~/.claude/projects/**/*.jsonl`) with no manual tallying — and the counts are trustworthy **when all four `message.usage` fields are summed.**

## The R2 "10–100× off" flag is a field-selection artifact, NOT an inaccuracy
Where tokens actually live (all repos, all-time on this machine):

| Field | % of all tokens |
|---|---|
| `input_tokens` | 0.4% |
| `output_tokens` | 1.3% |
| `cache_creation_input_tokens` | 11.9% |
| `cache_read_input_tokens` | **86.5%** |

A naive parser summing `input+output` captures **1.7%** of real usage → a **~60× undercount** (matches R2's "100× off"). Summing all four is complete and internally consistent. **Resolution: the transcript numbers are reliable; the bug is summing the wrong fields.**

## The bucket is real — measured, not theoretical
| repo | msgs | naive (in+out) | full (incl. cache) | ratio |
|---|---|---|---|---|
| arch-research | 3,170 | 7,620,072 | **459,293,665** | 60.3× |
| hotspot-bank | 53 | 235,886 | **21,045,387** | 89.2× |
| **TOTAL** | 3,223 | 7,855,958 | **480,339,052** | 61.1× |

→ cross-repo split ≈ **96% / 4%**. Per-day buckets populated for every active day (peak 2026-06-26 = 92.7M). Model mix **~97% Opus** (3,129 Opus / 80 Haiku / 13 Fable) → token-share ≈ real quota-share holds well; model-weighting error is small for this user.

## Open design choice (surfaced, not decided)
`cache_read` is 86.5% of tokens but is the **cheapest** input class and lightest on the real quota. Two valid bucket units:
- **Raw context tokens** (sum all four) — simple, consistent; overstates quota/cost impact.
- **Cost/quota-weighted** (e.g. `input + output + 1.25×cache_creation + 0.1×cache_read`) — closer to the real bucket. Recommended if the bucket should track the actual subscription cap rather than raw throughput.

## Grade
B1 (#114): missing → **partial** — measurement + per-repo attribution demonstrated by us on real data; not yet a standing/autonomous instrument. Artifact: `product/research/opcost-001/poc/opcost_poc.py`.
