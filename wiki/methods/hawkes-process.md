---
title: "Hawkes Process"
type: method
created: 2026-04-15
updated: 2026-04-15
sources:
  - raw/papers/2408.03594.md
  - raw/papers/2507.22712.md
tags:
  - point-process
  - hawkes
  - high-frequency
  - market-microstructure
  - time-series
related:
  - concepts/order-flow-imbalance.md
  - concepts/market-microstructure.md
  - papers/forecasting-high-frequency-ofi.md
  - papers/order-flow-filtration.md
confidence: high
---

# Hawkes Process

## Algorithm description

A **Hawkes process** is a self-exciting point process: past events increase the probability of future events. In its multivariate form, events in one stream can excite other streams, making it well-suited to modelling the mutual dependence between bid and offer order flows in a limit order book.

The conditional intensity (instantaneous event rate) for process $k$ at time $t$:

$$\lambda^k(t) = \mu^k + \sum_{j=1}^{K} \sum_{t_i^j < t} \phi^{kj}(t - t_i^j)$$

where:
- $\mu^k > 0$ is the background (baseline) rate for stream $k$.
- $\phi^{kj}(\cdot) \geq 0$ is the excitation kernel: how a past event in stream $j$ affects stream $k$.
- The sum runs over all past event times $t_i^j$ in stream $j$.

---

## Kernel choices

| Kernel | Form | Notes |
|---|---|---|
| Exponential | $\alpha e^{-\beta t}$ | Simple; fast decay; closed-form likelihood |
| Sum of Exponentials | $\sum_m \alpha_m e^{-\beta_m t}$ | Multi-scale memory; best in [[papers/forecasting-high-frequency-ofi]] |
| Power law | $\alpha (t + c)^{-p}$ | Slower decay; models long memory |
| Non-parametric | Estimated from data | Flexible but harder to fit |

---

## Stability condition

The process is stationary (doesn't explode) if and only if the spectral radius of the branching matrix $\|\int_0^\infty \Phi(t)\,dt\|_2 < 1$, where $\Phi_{kj} = \int_0^\infty \phi^{kj}(t)\,dt$.

---

## Fitting

Maximum likelihood estimation (MLE). The log-likelihood for a realisation on $[0, T]$:

$$\mathcal{L} = \sum_k \left[ -\int_0^T \lambda^k(t)\,dt + \sum_{t_i^k \leq T} \log \lambda^k(t_i^k) \right]$$

Optimised by gradient descent or EM algorithms. For Sum of Exponentials kernels, the integral $\int \lambda^k(t)\,dt$ has an efficient recursive form.

---

## Computational complexity

- Fitting: $O(n^2)$ naively; $O(n)$ with recursive likelihood for exponential kernels.
- Simulation: $O(n \log n)$ via thinning algorithm.

---

## Applications in this wiki

| Paper | Use |
|---|---|
| [[papers/forecasting-high-frequency-ofi]] | Model bid/offer order flow; forecast OFI distribution |
| [[papers/order-flow-filtration]] | Measure Hawkes excitation between OBI and return regimes |

---

## When to use / when not to use

**Use when:**
- Modelling arrival processes where past events cluster future events (order flow, earthquakes, social media cascades).
- You need a causal, interpretable model (not a black box).
- Distributional forecasts of arrival counts matter (not just point estimates).

**Avoid when:**
- Events are approximately independent (Poisson suffices).
- Very non-stationary environments (e.g., intraday seasonality requires careful handling).

---

## Implementations

- **tick** (Python): `tick.hawkes`
- **PtProcess** (R)
- **hawkeslib** (Python)
- Custom MLE in PyTorch/JAX for differentiable fitting.

---

## Connections

- Applied to [[concepts/order-flow-imbalance]] modelling in [[papers/forecasting-high-frequency-ofi]].
- Used as diagnostic in [[papers/order-flow-filtration]].
- Related to [[concepts/market-microstructure]] — captures the self-exciting, mutually triggering nature of order flow.
