# User Context as Market Signals: Behavioral Indicators Analysis

## Summary Verdict: **Interesting Framework, Sparse Data Problem**

The concept of using trading indicators (RSI, MACD, Bollinger Bands) on user behavior is creative but faces a fundamental constraint: personal PKM generates insufficient data for these indicators to be meaningful.

---

## The Data Reality Check

### Trading Indicator Data Requirements vs. PKM Reality

| Indicator | Trading Data Points | PKM Equivalent | PKM Reality |
|-----------|---------------------|----------------|-------------|
| RSI (14-period) | 14+ data points minimum | 14 topic vectors | 14 sessions (~2 weeks) |
| MACD (12,26,9) | 35+ data points | 35 interactions | 35 sessions (~5 weeks) |
| Bollinger Bands | 20+ periods | 20 topic vectors | 20 sessions (~3 weeks) |
| Volume indicators | Continuous tick data | Interaction events | ~50/day sparse |

**Problem**: Trading indicators are designed for high-frequency data (thousands to millions of data points). Personal PKM generates ~30-100 meaningful interactions per day. Most indicators won't stabilize for weeks.

---

## Individual Indicator Assessment

### RSI for Topic Exploration

**Claim**: RSI > 70 = "overbought" (excessive focus), RSI < 30 = "undersold" (neglected areas)

**Analysis**:
- **Conceptually appealing**: Detecting when user is going too deep or neglecting areas
- **Practically problematic**:
  - "Excessive focus" might be exactly what user needs (deep work)
  - "Neglected areas" might be deliberately deprioritized
  - False signals when user legitimately changes interests

**Better Alternative**: Simple recency-weighted topic distribution. No indicator needed—just show "You haven't explored X in 3 weeks."

---

### MACD for Research Direction

**Claim**: MACD crossovers indicate new research direction vs. return to established interests

**Analysis**:
- **Requires embedding arithmetic** on topic vectors—mathematically coherent
- **Lag problem**: MACD is a lagging indicator. By the time it signals direction change, user already knows they changed direction.
- **No actionable insight**: What does the system DO with this signal? The user already knows they switched topics.

**Verdict**: Technically implementable, provides no value over "you recently started exploring X" message.

---

### Volatility as Uncertainty Indicator

**Claim**: High volatility in topic embeddings indicates uncertain research direction

**This one has merit, with caveats:**

**Valid use case**: When user's queries are scattered across semantic space, they may be:
1. Starting a new interdisciplinary project (need orientation)
2. Confused about what they're looking for (need clarification)
3. Procrastinating/browsing randomly (need focus prompts)

**Implementation reality**: Simple standard deviation of recent query embeddings achieves this without trading metaphor overhead.

---

### Sentiment Analysis Through Implicit Signals

**Claim**: Create sentiment oscillator from annotation sentiment, query phrasing, reading rhythm

**Analysis**:
- **Annotation sentiment**: Requires NLP on annotations—adds latency, complexity. Most users don't annotate frequently.
- **Query phrasing**: Distinguishing "exploratory vs. targeted" queries is useful but simple rule-based detection works.
- **Reading rhythm**: Valuable signal (fragmented reading = struggling), easy to implement without "oscillator" framing.

**Honest Assessment**: These signals are valuable. Wrapping them in "sentiment oscillator" trading language adds no value and obscures the simple underlying metrics.

---

### Cognitive State Regimes

**Claim**: Use Hidden Markov Model to detect focused/exploration/learning/reference modes

**This is the strongest concept in the behavioral indicators section:**

**Why it works**:
1. Users DO operate in different modes
2. Modes ARE detectable from behavior patterns
3. Mode-appropriate recommendations ARE more useful

**Over-engineering concern**: HMM is overkill. Simple rule-based detection works:
- Short dwell time + many documents = reference mode
- Long dwell time + few documents = focused mode
- Mixed topics + moderate dwell = exploration mode
- Sequential difficulty progression = learning mode

**2035 Relevance**: By 2035, LLMs will likely detect cognitive state through conversation, making behavioral proxies less necessary.

---

## What's Actually Useful

| Concept | Strip Away Trading Metaphor | Actual Implementation |
|---------|---------------------------|----------------------|
| RSI overbought/undersold | Topic coverage balance | % time on each topic cluster |
| MACD crossovers | Topic shift detection | Embedding centroid change detection |
| Volatility | Query scatter | Standard deviation of query embeddings |
| Sentiment oscillator | Engagement quality | Time-on-page + annotation rate |
| Regime detection | Mode classification | Rule-based state machine |

**Key Insight**: Every useful signal in this section can be implemented with simple statistics. The trading indicator framing adds:
- Complexity in implementation
- Confusion in interpretation
- Zero additional predictive value

---

## Correlation Matrix Analysis

**Claim**: Build correlation matrices between behavioral signals, use PCA to extract latent factors

**Reality Check**:
- Correlation analysis requires stable distributions—PKM behavior is non-stationary
- PCA on sparse, changing data will produce unstable factors
- "Engagement level" and "exploration vs exploitation" can be measured directly without matrix decomposition

**This is academic research methods applied without considering data reality.**

---

## Verdict for 2035

**Behavioral signal mining will exist but be invisible.**

By 2035:
- AI assistants will naturally adapt to user state through conversation
- Explicit indicator calculation will be unnecessary
- "Cognitive state detection" will happen through dialogue, not metrics

**What survives**: The underlying insight that user behavior signals should influence recommendations. The specific trading indicator implementations will be forgotten.
