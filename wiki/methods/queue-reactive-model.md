---
title: "Queue-Reactive (QR) Model"
type: method
created: 2026-04-16
updated: 2026-04-16
sources:
  - raw/papers/2603.24137.md
tags:
  - limit-order-book
  - simulation
  - stochastic-process
  - market-microstructure
  - markov-jump
related:
  - concepts/limit-order-book.md
  - concepts/order-flow-imbalance.md
  - papers/reality-gap-lob-simulation.md
confidence: high
---

# Queue-Reactive (QR) Model

## Algorithm description

The **Queue-Reactive (QR) model** (Huang, Lehalle, Rosenbaum 2015) represents the limit order book as a continuous-time Markov jump process whose event intensities depend on the current observable state of the book. Three event types modify the book at each price level:

- **Limit order insertions** (Add)
- **Cancellations** (Cancel)
- **Market orders** (Trade)

For each event type $e$ on queue $q_i$, the arrival intensity is a function of the book state:

$$\lambda^e = \lambda^e(q_{-K}, \ldots, q_{-1}, q_1, \ldots, q_K)$$

In the simplest version each queue is independent — $\lambda^e(q_i)$ — which makes estimation trivial but ignores bid–ask coupling. The original paper extends this to $\lambda^e(q_1, q_{-1})$, conditioning on both best queues, at the cost of aggressive binning to get enough observations per bin.

The price reference $p_\text{ref}$ is shifted by a separate stochastic mechanism when the best queue is depleted or a new level is created inside the spread.

---

## Why it matters

QR is a **workhorse for interactive LOB simulation** used by market makers, prop trading firms, and brokerages. Its key virtues over zero-intelligence models (Smith et al. 2003; Cont–De Larrard 2013):

- **Data-driven**: transition rates estimated empirically, no ad-hoc parameter tuning.
- **Interpretable**: each rate is the empirical event frequency under an observable state.
- **Captures queue dependence**: event intensities respond to book asymmetries.

---

## Known limitations (motivating extensions)

1. **Exponential inter-event times**: a continuous-time Markov jump process generates exponential waiting times by construction. Real markets exhibit **pronounced clustering at exchange round-trip latency** (latency races account for ~20% of volume per Aquilina et al. 2021) — QR averages this out entirely.
2. **No post-execution market impact**: after a metaorder completes, the book in QR evolves as if nothing happened. For strategy evaluation this is a critical flaw — simulated P&L **systematically overstates profit and understates risk**.
3. **Sparse state space under heavy conditioning**: conditioning on full queue-size tuples leaves most cells poorly populated, forcing coarse binning.

---

## Extensions

The most practical recent extension is [[papers/reality-gap-lob-simulation]] (Noble, Rosenbaum, Souilmi 2026), which:

- **Projects** the state onto $(\text{Imb}, n)$ — volume imbalance + spread — making estimation tractable with a single scalar of bid-ask coupling.
- Replaces the exponential inter-event distribution with a flexible empirical one, capturing the latency-race mode.
- Adds a **power-law market-impact feedback kernel** so post-execution book dynamics reflect the metaorder's footprint.
- Uses **random order volumes** drawn from state-conditional empirical distributions rather than unit sizes, so queue depletion arises naturally.

---

## When to use / when not to use

**Use when:**
- You need an interactive simulator for backtesting or strategy stress tests.
- The asset is large-tick and the book state is well-summarised by imbalance + spread.
- You want interpretable, data-driven transition rates.

**Avoid or adapt when:**
- Modelling small-tick assets where $n \gg 1$ is common — the imbalance projection breaks down.
- Studying mechanisms that require non-Markov memory (e.g., persistent meta-order impact) — extend with explicit feedback kernels.
- Modelling latency races explicitly — you need non-exponential inter-event times.

---

## Implementations

- Huang–Lehalle–Rosenbaum 2015 code (original Markov QR).
- Noble–Rosenbaum–Souilmi 2026 simulator — extensions described above; code on GitHub.

---

## Connections

- Extended by [[papers/reality-gap-lob-simulation]] into a practical interactive simulator.
- Relies on [[concepts/order-flow-imbalance]] as the central state-projection variable.
- Central data structure: [[concepts/limit-order-book]].
- Impact-feedback extensions connect to the Hawkes-process impact literature — see [[methods/hawkes-process]] and [[papers/forecasting-high-frequency-ofi]].
