---
title: "Limit Order Book"
type: concept
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/1011.6402.md
  - raw/papers/2403.09267.md
  - raw/papers/2602.00776.md
  - raw/papers/2603.24137.md
tags:
  - market-microstructure
  - high-frequency
  - trading
related:
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/market-microstructure.md
  - concepts/adverse-selection.md
  - papers/price-impact-order-book-events.md
  - papers/deep-lob-forecasting.md
  - papers/explainable-crypto-microstructure.md
  - concepts/market-making.md
  - concepts/optimal-execution.md
  - concepts/universal-price-formation.md
  - connections/deep-learning-meets-market-microstructure.md
  - methods/event-type-impact-decomposition.md
  - methods/integrated-ofi.md
  - methods/microprice.md
  - methods/queue-reactive-model.md
confidence: high
---

# Limit Order Book (LOB)

## Definition

A **Limit Order Book (LOB)** is the real-time data structure used by electronic exchanges to record all outstanding buy and sell orders for an asset. It organises orders by price level and time priority, and the current state of the LOB represents the full supply and demand schedule for the asset at any instant.

---

## Structure

The LOB has two sides:
- **Bid side** — buy limit orders, ordered from highest to lowest price. The highest bid price is the **best bid**.
- **Ask side** — sell limit orders, ordered from lowest to highest price. The lowest ask price is the **best ask**.

The **bid-ask spread** = best ask − best bid. The **mid-price** = (best bid + best ask) / 2.

Each price level contains a queue of orders (FIFO priority). The **market depth** at a level is the total quantity resting there.

---

## Order types

| Type | Description |
|---|---|
| Limit order | Rest in the book at a specified price until filled or cancelled |
| Market order | Execute immediately against the best available prices |
| Cancellation | Remove a resting limit order |
| Modification | Change the quantity (and sometimes price) of a resting order |

---

## LOB as data

LOB data comes in two forms:
- **Full order-by-order (tick data)** — every individual event (add, cancel, modify, trade) with nanosecond timestamps.
- **Snapshot data** — periodic snapshots of the top $N$ price levels (e.g., every second). Loses event-level detail.

**LOBSTER** (LOB System for NASDAQ data) is a common academic data source used in papers like [[papers/deep-lob-forecasting]].

---

## Key empirical properties

- Mid-price changes are driven primarily by [[concepts/order-flow-imbalance]] at the best bid/ask (Cont et al., [[papers/price-impact-order-book-events]]).
- Deep learning models can predict short-horizon mid-price direction from LOB snapshots, but accuracy doesn't always translate to trading utility ([[papers/deep-lob-forecasting]]).
- Across crypto assets, the same engineered LOB features (OFI, spread, depth ratios) have stable predictive importance ([[papers/explainable-crypto-microstructure]]).

### Tick-size taxonomy (Briola et al. 2024)

Stocks behave differently depending on the ratio of mean spread $\langle\sigma\rangle$ to tick size $\theta$:

| Regime | Condition | Empirical profile |
|---|---|---|
| Small-tick | $\langle\sigma\rangle \gtrsim 3\theta$ | Wide, heavy-tailed spread distribution; thin queues; hardest to forecast |
| Medium-tick | $1.5\theta \lesssim \langle\sigma\rangle \lesssim 3\theta$ | "Borderline" — mixed behaviour (AAPL ≈ large-tick; ABBV/PM ≈ small-tick) |
| Large-tick | $\langle\sigma\rangle \lesssim 1.5\theta$ | Spread pinned near 1 tick; deep queues; queues shrink before transactions (directional leak); most forecastable |

This taxonomy is the strongest single predictor of whether a DL model will work on a given stock — see [[papers/deep-lob-forecasting]].

---

## Open questions

- How much of the LOB signal is genuine informed flow vs noise from high-frequency market makers?
- What is the right level of the book to model? Best bid/ask vs multi-level?
- How do LOB dynamics change under different market regimes (normal, stressed, flash crash)?

---

## Simulation and modelling

Interactive LOB simulators are essential for backtesting, execution benchmarking, and strategy stress-testing:
- **Zero-intelligence models** (Smith et al. 2003; Cont–De Larrard 2013) — constant-rate arrivals, fit first-order statistics only.
- **Queue-Reactive (QR) model** (Huang et al. 2015) — event intensities conditioned on queue state; see [[methods/queue-reactive-model]].
- **Extended QR** — [[papers/reality-gap-lob-simulation]] adds state projection onto (imbalance, spread), non-exponential inter-event times capturing latency-race bursts, and power-law impact feedback so post-execution dynamics are realistic.

## Connections

- [[concepts/order-flow-imbalance]] — the key signal derived from LOB event flow.
- [[concepts/price-impact]] — how LOB imbalances translate into price movement.
- [[concepts/adverse-selection]] — informed traders leave footprints in the LOB.
- [[concepts/market-microstructure]] — the LOB is the central object of microstructure theory.
- [[methods/queue-reactive-model]] — workhorse stochastic LOB model.
- [[papers/reality-gap-lob-simulation]] — practical recipe for realistic LOB simulation.
