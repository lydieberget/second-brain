---
title: "Bridging the Reality Gap in Limit Order Book Simulation"
type: paper
created: 2026-04-16
updated: 2026-04-16
sources:
  - raw/papers/2603.24137.md
tags:
  - limit-order-book
  - simulation
  - queue-reactive
  - market-impact
  - latency
  - market-microstructure
  - large-tick
related:
  - concepts/limit-order-book.md
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/market-microstructure.md
  - methods/queue-reactive-model.md
  - methods/propagator-model.md
  - methods/microprice.md
  - papers/price-impact-order-book-events.md
  - papers/deep-lob-forecasting.md
confidence: high
---

# Bridging the Reality Gap in Limit Order Book Simulation

**Authors**: Patrick Noble (Jump Trading), Mathieu Rosenbaum (Université Paris Dauphine-PSL), Saad Souilmi (École Polytechnique)
**Year**: 2026 (March 2026)
**arXiv**: [2603.24137](https://arxiv.org/abs/2603.24137)
**Categories**: q-fin.TR

---

## Plain-language abstract

Electronic market participants (market makers, prop firms, brokerages) rely on LOB simulators to stress-test strategies before going live. Existing zero-intelligence and queue-reactive models fit first-order statistics but fail on two dimensions that matter for strategy evaluation: (i) inter-event times are **not exponential** — real markets exhibit pronounced clustering at exchange round-trip latency from latency races, and (ii) a metaorder leaves no **market impact** after completion, so simulated P&L systematically **overstates profit and understates risk**. This paper extends the Huang–Rosenbaum Queue-Reactive (QR) model with three modifications that turn it into a practical, interactive simulator for large-tick assets.

---

## Key contributions

1. **State projection onto $(\text{Imb}, n)$** — collapse the high-dimensional queue state into a 2D representation of volume imbalance at the best level + spread in ticks. Keeps the bid-ask cross-dependence in a single scalar and makes empirical estimation tractable (the full queue-by-queue conditioning is too sparse).
2. **Non-exponential inter-event times** — replace the Markov Poisson assumption with a flexible empirical distribution. This reveals a **sharp mode at the exchange round-trip latency** consistent with simultaneous reactions and latency races (Aquilina et al. 2021: ~20% of volume).
3. **Power-law market-impact feedback kernel** — accumulate signed trade flow, bias subsequent trades toward mean reversion. Reproduces two well-known empirical facts: concave impact *during* execution (square-root law) and partial reversion *after* (impact decay). The same mechanism can inject custom signals into book dynamics.
4. **Random order volumes** — replace unit sizes (vanilla QR) with state-conditional empirical size distributions, capped at 50 × median event size. Queue depletion then emerges naturally whenever a small best queue is hit by a moderate trade, eliminating the need for a special "depletion" event type.
5. **Methodology framed as a recipe** — *project → estimate → validate → adapt* — rather than a rigid model. Practitioners decide which features matter for their asset and strategy.

---

## Method summary

### Data
- **4 S&P 500 large-tick stocks around $30**: INTC, VZ, T, PFE.
- **Databento** L2 data, **December 2023 → December 2025** (~2 years).
- Paper illustrates results on PFE; equivalents for the other three in the appendix.
- Code available on GitHub.

### State projection

$$\Phi(\text{LOB}) = (\text{Imb}, n), \qquad \text{Imb} = \frac{q_{-1} - q_1}{q_{-1} + q_1}$$

- $\text{Imb}$ discretised into **21 bins of width 0.1**; special point bin at $\text{Imb}=0$ to avoid mixing opposite signs.
- $n$ = spread in ticks (for large-tick assets, typically $n = 1$; $n \geq 2$ is transient and resolved by `CreateBid`/`CreateAsk` events).
- Queue sizes normalised by **median event size (MES)** per level, more robust than the mean used in original QR.
- Optional extra dim $\ell = q_{-1} + q_1$ (total resting size) was tested but **did not significantly improve** the reproducing power while diluting observations — rejected.

### Event space

$e = (\mathcal{T}, s, i)$ with type $\mathcal{T} \in \{\text{Add, Cancel, Trade, CreateBid, CreateAsk}\}$, side $s \in \{-1, +1\}$, queue level $i$.

- Adds/Cancels target queues up to $q_{\pm 2}$.
- Trades target only the best queues $q_{\pm 1}$ (marketable limit orders); "walk-the-book" trades are aggregated into a single total-volume trade.
- Create events: a new best on either side when the spread opens; the subsequent burst of Adds at the new price is aggregated into the Create's size.

### Market-impact feedback

A power-law decay kernel accumulates signed trade flow and biases subsequent trade intensities:

$$I_t = \sum_{s < t} \text{sign}(v_s) \cdot |v_s|^\alpha \cdot \phi(t - s), \qquad \phi(\tau) \propto \tau^{-\beta}$$

This reproduces (a) **concave impact during execution** and (b) **partial reversion after** — both essential for realistic strategy evaluation. The same mechanism can be repurposed to inject exogenous alpha signals.

### Validation

Simulated vs empirical statistics compared on: imbalance-conditional event probabilities, inter-event time distributions (showing the round-trip-latency mode), spread dynamics, and impact response curves. PFE traces reproduce the fine-scale temporal structure; the QR-exponential baseline flattens it.

---

## Case studies

1. **Mid-frequency signal-based strategy** — reveals how profitability depends on execution parameters when the simulator correctly models market impact.
2. **High-frequency imbalance strategy** — demonstrates that naïve QR without the latency-race mode and impact feedback overstates realised P&L by an economically meaningful margin.

---

## Limitations

- **Large-tick assets only**: the state projection relies on $n = 1$ being the dominant regime (<5% of trades on PFE happen at $n \geq 2$). Small-tick equities (GOOG, CHTR etc. in [[papers/deep-lob-forecasting]]) would require a different representation.
- **Four-stock sample**: all INTC / VZ / T / PFE near $30 — no generalisation test across price levels or sectors.
- **Point-in-time kernel calibration**: the impact kernel is fit on one window; regime changes (e.g., around earnings or macro events) are not modelled.
- **Walk-the-book events aggregated, not explicitly modelled**: acceptable given their rarity, but a simulator targeting crash periods would need to treat them separately.

---

## Connections

- The **QR framework** this paper builds on is worth a dedicated method page: [[methods/queue-reactive-model]].
- Volume imbalance is the central state variable, linking directly to [[concepts/order-flow-imbalance]] and to **microprice** (Stoikov 2018) as a continuous latent price within the spread — the same mechanism [[papers/explainable-crypto-microstructure]] validates in crypto via the W/USDT spot-vs-perp experiment ($c = 0.94$).
- The **large-tick focus** reinforces the cross-paper tick-size finding surfaced by re-ingest: large-tick assets are where queue-imbalance signals are readable and simulatable; small-tick assets require different machinery (see [[connections/deep-learning-meets-market-microstructure]]).
- Power-law impact kernel matches the Bacry et al. (2016) Hawkes-based impact literature referenced by [[papers/forecasting-high-frequency-ofi]] and [[papers/order-flow-filtration]].
- Practical implication for backtesting: the taker/maker divergence in [[papers/explainable-crypto-microstructure]]'s flash crash would likely be much sharper in a simulator with this paper's impact feedback than in a naïve QR baseline.
