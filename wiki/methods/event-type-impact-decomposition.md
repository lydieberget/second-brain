---
title: "Event-Type Impact Decomposition (EBK)"
type: method
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/0904.0900.md
  - raw/papers/1107.3364.md
tags:
  - price-impact
  - order-book-events
  - propagator-model
  - bare-impact
  - tick-size
  - signal-design
related:
  - concepts/price-impact.md
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - methods/propagator-model.md
  - papers/eisler-bouchaud-kockelkoren-order-book-events.md
  - papers/models-for-all-order-book-events.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/price-impact-order-book-events.md
  - entities/jean-philippe-bouchaud.md
  - entities/zoltan-eisler.md
confidence: high
---

# Event-Type Impact Decomposition (EBK)

## Algorithm description

The **Eisler–Bouchaud–Kockelkoren (EBK) event-type decomposition** generalises the single-event-type propagator model by tracking the *bare impact* of each distinct order-book event type. Instead of one propagator $G(\tau)$ for "market orders", one measures six propagators $G_\pi(\tau)$ for $\pi \in \{\text{MO}^0, \text{MO}', \text{LO}^0, \text{LO}', \text{CA}^0, \text{CA}'\}$.

The mid-price at time $t$ is:

$$p_t \;=\; p_0 + \sum_{t' < t}\;\sum_\pi\; G_\pi(t - t') \;\cdot\; \epsilon_{t'} \;\cdot\; I(\pi_{t'} = \pi)$$

where $\pi_{t'}$ is the type of the event at time $t'$, $\epsilon_{t'}$ is its signed direction, and $G_\pi(\tau)$ is the bare impact of event type $\pi$ at lag $\tau$. The six $G_\pi$ are recovered by inverting the relation between measured response functions $R_\pi(\ell)$ and signed event-event correlations $C_{\pi_1, \pi_2}(\ell)$.

---

## The six event types

| $\pi$ | Description |
|---|---|
| MO⁰ | market order, volume $<$ outstanding at best (does NOT change best price) |
| MO' | market order, volume $\geq$ outstanding at best (changes best price) |
| LO⁰ | limit order at the current best (does NOT change best price, just adds size) |
| LO' | limit order inside the spread (changes best price) |
| CA⁰ | partial cancellation at the best (does NOT change best price) |
| CA' | complete cancellation of the best level (changes best price) |

Event sign $\epsilon \in \{-1, +1\}$ defined by the expected directional effect: $+1$ for buy market orders, cancelled sell limit orders, and incoming buy limit orders; $-1$ for their counterparts. The side $s$ (bid or ask) is a separate variable because limit orders on the bid push the price *up* (positive $\epsilon$) — limit-order sign $\neq$ side.

---

## Inversion formula

For each event type $\pi$, the observed response function is:

$$R_\pi(\ell) \;=\; \sum_{\pi_1}\;\sum_{\ell' = 0}^{\ell - 1}\; G_{\pi_1}(\ell - \ell') \;\cdot\; P(\pi_1) \;\cdot\; C_{\pi, \pi_1}(\ell')$$

This is a block-Toeplitz linear system. Stacking across lags $\ell = 0, \ldots, L$ and event types $\pi = 1, \ldots, 6$ gives a matrix equation:

$$\mathbf{R} \;=\; \mathbf{M} \cdot \mathbf{G}, \qquad \mathbf{M}_{(\pi, \ell), (\pi_1, \ell')} \;=\; P(\pi_1) \cdot C_{\pi, \pi_1}(\ell - \ell')$$

Invert (with regularisation at large $L$) to recover $\mathbf{G}$. The paper uses $L = 1000$ lags; accuracy is good up to $\ell \sim 300$.

---

## Two regimes: large-tick vs small-tick

**Large-tick stocks** (spread typically 1 tick; e.g. MSFT, INTC, CSCO in 2008):
- Bare impacts $G_\pi(\tau) \approx G_\pi$ — permanent and non-fluctuating.
- Simple constant-impact model fits response functions and price diffusion almost perfectly.
- Fit procedure: set $G_\pi$ = constant and use realised average gaps $\Delta^R_\pi$.

**Small-tick stocks** (spread typically 3–4 ticks; e.g. AAPL, AMZN in 2008):
- Bare impacts appear history-dependent — gaps behind the best quote fluctuate.
- Constant-impact model misses ~30% of the volatility.
- Correction: linear AR model on gaps as a function of past order flow (see [[papers/models-for-all-order-book-events]]).

---

## History-dependent gap model (small-tick extension)

For small-tick stocks, the gap $\Delta_{\pi, \epsilon, t}$ is modelled as:

$$\Delta_{\pi, \epsilon, t} \;=\; \Delta^R_\pi + \sum_{\pi'} \sum_{\ell > 0} K_{\pi, \pi'}(\ell) \cdot \epsilon_{t-\ell} \cdot I(\pi_{t - \ell} = \pi')$$

The kernels $K_{\pi, \pi'}(\ell)$ are OLS-fitted from the empirical realised-gap vs past-order-flow cross-correlations. The 2011 follow-up paper (arXiv:1107.3364) gives the fully dynamic extension.

---

## Three-way decomposition of impact

For any event, the expected price change at a future horizon splits into three contributions:

1. **Instantaneous jump** — the immediate price change from the event itself ($\Delta \neq 0$ only for price-changing events).
2. **Modification of future event rates** — the event raises/lowers the probability of subsequent MO, LO, CA events. Captured by the signed correlation $C_{\pi_1, \pi_2}$.
3. **Modification of future jump sizes** — the event changes the conditional mean gap $\Delta$ of future price-changing events. Captured by the kernels $K$.

All three are measurable from data; each has a distinct economic interpretation.

---

## When to use / when not to

**Use when:**
- You have full L2 or L3 data at the best quotes (prices, sizes, events).
- You want a structural model of price impact that separates "trade impact" from "limit-order impact".
- You're designing a signal that should treat MO, LO, and CA flow differently (most signals implicitly do this anyway — EBK makes the weighting explicit).
- You want to reconcile your propagator model with Hasbrouck's VAR framework.

**Don't use when:**
- You only have trade-tape data (no LO / CA information). Fall back to the single-event propagator model ([[methods/propagator-model]]).
- You're modelling horizons much longer than seconds — the EBK decomposition is inherently event-time / sub-second.
- You need non-linear impact. The superposition-of-bare-impacts is linear; extreme events or stressed regimes likely break it.

---

## Relationship to other decompositions

| Feature | OFI (Cont-Kukanov-Stoikov) | EBK (Eisler-Bouchaud-Kockelkoren) |
|---|---|---|
| Aggregation | Single scalar OFI per interval | Per-event-type bare impact |
| Output | Linear price-change slope $\beta$ | Six propagator functions $G_\pi$ |
| Tick-size treatment | Universal linear model | Explicit large-tick vs small-tick split |
| Gap dynamics | Not modelled | Explicit for small-tick |
| Canonical for | Short-horizon signal construction | Structural impact decomposition |

Both start from the same empirical primitive (order-book events at the best quote); they differ in how much structure they carry over into the signal.

---

## Implementation notes

- **Event labelling**: classify events by which price level they touch. Common mistake: grouping cancellations at the best bid and "cancellations somewhere on the bid side" — they're different events.
- **Matrix inversion**: the block-Toeplitz matrix is well-conditioned when the event-event correlation decay is slow; at $L > 500$ lags add Tikhonov regularisation.
- **Gap definitions**: for MO' the "gap" is half the distance between old best and the new best after the sweep. For LO' inside the spread, the gap is half the distance from the previous best on the same side. Sign conventions trip up implementations.
- **Sanity check**: $R_\pi(\ell=1)$ should equal $\Delta^R_\pi$ by construction for price-changing events and zero for non-price-changing events. If not, event signs are inverted.

---

## Connections

- [[concepts/price-impact]] — EBK is the canonical event-type-level impact decomposition.
- [[concepts/order-flow-imbalance]] — OFI is a linear combination of event counts; EBK exposes the per-event coefficients.
- [[methods/propagator-model]] — EBK is the multi-event-type generalisation.
- [[concepts/limit-order-book]] — the data domain; EBK needs best-quote events.
- [[papers/eisler-bouchaud-kockelkoren-order-book-events]] — the paper introducing this framework.
- [[papers/models-for-all-order-book-events]] — the 2011 follow-up with full dynamic extension.
