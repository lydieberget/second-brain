---
title: "Microprice"
type: method
created: 2026-04-18
updated: 2026-04-18
sources:
  - raw/papers/1312.0514.md
  - raw/papers/2603.24137.md
  - raw/papers/2602.00776.md
tags:
  - microprice
  - queue-imbalance
  - fair-value
  - market-microstructure
  - signal-design
related:
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - concepts/price-impact.md
  - papers/lipton-quote-imbalance.md
  - papers/gould-bonart-queue-imbalance.md
  - papers/reality-gap-lob-simulation.md
  - papers/explainable-crypto-microstructure.md
  - papers/cfmm-liquidity-provision-pricing.md
confidence: high
---

# Microprice

## Definition

The **microprice** is a refined "fair value" estimator for an asset, built on top of the mid-price by weighting it with queue imbalance. It attempts to extract a **continuous latent price** from discrete book state — a value that sits *within* the spread, biased toward whichever side of the book carries more resting volume.

Introduced formally by Stoikov (2018) as a Markov-chain correction to the mid; the underlying intuition goes back to Cao, Hansch & Wang (2009) and appears under various names in the practitioner literature.

---

## Core formulas

### Basic queue-weighted microprice

The simplest form weights the best bid and ask by the *opposite* queue size — when the ask queue is large, the short-term fair value sits closer to the bid, and vice versa:

$$p_{\text{micro}}^{(0)} = \frac{q^a \cdot p^b + q^b \cdot p^a}{q^a + q^b}$$

Equivalently, in terms of queue imbalance $I = (q^b - q^a)/(q^b + q^a)$:

$$p_{\text{micro}}^{(0)} = m + \frac{s}{2} \cdot I$$

where $m = (p^a + p^b)/2$ is the mid-price and $s = p^a - p^b$ is the spread.

### Stoikov (2018) Markov-chain microprice

Stoikov's refinement iterates the expected mid-price conditional on $(I, s)$ under a Markov model of queue dynamics:

$$p_\text{micro}(I, s) = m + g(I, s)$$

where $g$ is computed as a fixed-point of the expected mid-price shift when the next price-changing event fires. The key insight: the basic formula above is biased in regimes where spread is elevated; the Markov correction accounts for the fact that a wide spread will typically close from *one* side with probability biased by $I$.

---

## Why it's useful

1. **Predictive of next mid-move**: the microprice leads the mid by a few milliseconds — crossing the microprice through the mid is a short-horizon direction signal.
2. **Better fair value for market makers**: quoting around the microprice rather than the mid reduces adverse selection.
3. **Bridges discrete book state to continuous latent price**: in the limit of large relative tick size, the microprice is essentially a readable version of the continuous efficient price (strongly validated empirically — see the W/USDT experiment in [[papers/explainable-crypto-microstructure]] where spot OBI correlates at $c = 0.94$ with the perp's implied continuous price).
4. **Natural benchmark for queue-imbalance signals**: any QI-based predictor should be compared against a microprice-marked baseline rather than a mid-marked one.

---

## Empirical properties

- Microprice position within the spread is **~linear in $I$** for moderate imbalance; **saturates toward the opposite best** at high $|I|$. This is the queue-imbalance-as-predictor curve studied in [[papers/lipton-quote-imbalance]] and [[papers/gould-bonart-queue-imbalance]].
- **Tick-size dependence**: the microprice–mid gap carries more information in large-tick books where depth at the best concentrates; converges toward the mid in small-tick books where depth is dispersed. This is the same tick-size thread documented in [[papers/deep-lob-forecasting]] and [[papers/mlofi-xu-gould-howison]].
- **Consistent with Stoikov's Markov framework**: empirical microprice profiles match the semi-analytic forms Stoikov derived for common parameter choices.

---

## When to use / when not to use

**Use when:**
- Marking inventory or computing fair value at the sub-second horizon.
- Deciding whether to post passively or cross the spread in an execution algorithm.
- Generating a short-horizon direction signal cheaper than a full OFI computation.
- Market-making (quoting around microprice reduces adverse selection).

**Avoid when:**
- Modelling long-horizon price dynamics — microprice is a microstructure primitive, not a macro signal.
- Small-tick assets with small $I$ — the microprice-mid gap is vanishingly small and the mid is fine.
- You need a signal robust to spoofing; large visible queues that later cancel will move the microprice spuriously.

---

## Computational complexity

- **Basic formula**: $O(1)$ per update — read best bid/ask queues, apply a ratio.
- **Stoikov Markov version**: $O(1)$ per update once the fixed-point $g(I, s)$ table is precomputed (typically a small lookup grid over discretised $(I, s)$).
- Trivially real-time on any HFT stack.

---

## Implementations

- Native primitive in virtually every HFT market-making codebase.
- Open-source reference: Sasha Stoikov's companion code to the 2018 paper (Cornell FE).
- `LOBFrame` ([[papers/deep-lob-forecasting]]) implicitly uses microprice-like features via its input representation.
- CFMM LP pricing ([[papers/cfmm-liquidity-provision-pricing]]) uses a continuous price analogous to the microprice as the natural coordinate for the bonding curve.

---

## Relation to other signals

| Signal | Computation | What it captures |
|---|---|---|
| **Mid-price** | $(p^a + p^b)/2$ | Naïve midpoint; ignores book state |
| **Microprice** | queue-weighted mid | Continuous latent price within spread |
| **Quote Imbalance** | $(q^b - q^a)/(q^b + q^a)$ | Direction signal only (not a price) |
| **VWAP** | $\sum v p / \sum v$ | Execution-weighted price over a window; backward-looking |
| **OFI-adjusted mid** | $m + \beta \cdot \text{OFI}$ | Cumulative event-flow adjustment |

The microprice is **the natural fair-value companion to queue imbalance** — QI tells you direction, microprice tells you the best scalar-valued fair price given that direction.

---

## Connections

- **Direct users**: [[papers/lipton-quote-imbalance]] (theoretical framework implying microprice); [[papers/gould-bonart-queue-imbalance]] (logistic regressions on QI that are functionally equivalent to a non-parametric microprice); [[papers/reality-gap-lob-simulation]] (uses $(I, n)$ state projection — microprice is a natural summary statistic of this state); [[papers/explainable-crypto-microstructure]] (validates microprice empirically via W/USDT spot-vs-perp experiment); [[papers/cfmm-liquidity-provision-pricing]] (CFMM spot-price is a microprice analogue on the bonding curve).
- **Conceptual anchors**: [[concepts/order-flow-imbalance]] (QI is the atomic ingredient of microprice); [[concepts/limit-order-book]] (the substrate); [[concepts/price-impact]] (microprice is what a low-impact execution should aim for).
- **Sister method**: [[methods/queue-reactive-model]] — the Markov chain used to define Stoikov's microprice is closely related to QR dynamics.
- **Foundational but non-arXiv references**:
  - Stoikov, S. (2018). "The Micro-Price: A High-Frequency Estimator of Future Prices." *Quantitative Finance* 18(12), 1959–1966. **Not on arXiv**; would need Semantic Scholar / SSRN retrieval to ingest directly.
  - Cao, Hansch & Wang (2009). "The Information Content of an Open Limit-Order Book." *Journal of Futures Markets* 29(1), 16–41. **Not on arXiv.**
