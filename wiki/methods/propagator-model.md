---
title: "Propagator Model (Transient Impact Kernel)"
type: method
created: 2026-04-18
updated: 2026-04-18
sources:
  - raw/papers/0809.0822.md
  - raw/papers/1407.3390.md
  - raw/papers/2603.24137.md
  - raw/papers/0904.0900.md
  - raw/papers/1107.3364.md
tags:
  - market-impact
  - propagator-model
  - transient-impact
  - impact-decay
  - long-memory
  - market-microstructure
related:
  - concepts/price-impact.md
  - concepts/order-flow-imbalance.md
  - concepts/optimal-execution.md
  - methods/hawkes-process.md
  - methods/event-type-impact-decomposition.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/brokmann-slow-decay-impact.md
  - papers/reality-gap-lob-simulation.md
  - papers/order-flow-filtration.md
  - papers/eisler-bouchaud-kockelkoren-order-book-events.md
  - papers/models-for-all-order-book-events.md
  - entities/jean-philippe-bouchaud.md
  - methods/signal-aware-optimal-execution.md
  - papers/lehalle-neuman-signals-optimal-trading.md
confidence: high
---

# Propagator Model (Transient Impact Kernel)

## Algorithm description

The **propagator model** (also "transient impact model") represents the mid-price return at time $t$ as a linear superposition of the decaying impact of all past signed order-flow events. Each event leaves a "footprint" that fades over time according to a kernel $G$.

$$r_t = \sum_{t' \leq t} G(t - t') \cdot \varepsilon_{t'} + \eta_t$$

where:
- $\varepsilon_{t'} \in \{-1, +1\}$ (or signed volume) is the signed trade / order-flow event at time $t'$.
- $G(\tau) \geq 0$ is the **response function / propagator**: how much price impact from an event at lag $\tau$ remains at the current instant.
- $\eta_t$ is an uncorrelated residual.

For a **meta-order** executed over a window, the expected price displacement decomposes as:

$$\mathbb{E}[p(t+\tau) - p(t)] = \theta(Q) \cdot I(\tau) + \alpha \cdot H(\tau)$$

where $\theta(Q) = \epsilon Y_0 \sigma (Q/V)^\delta$ is the instantaneous (square-root) impact, $I(\tau)$ is the mechanical impact-decay kernel with $I(0) = 1$, $I(\infty) \approx 0$, and $\alpha \cdot H(\tau)$ is a (possibly zero) predictor-induced term for informed trades.

---

## Typical functional forms

| Form | Formula | Used in |
|---|---|---|
| Power-law decay | $G(\tau) \sim \tau^{-\beta}$, $\beta \in [0.2, 0.5]$ | BFL 2008, Noble-Rosenbaum-Souilmi 2026 |
| Stretched exponential | $G(\tau) \sim e^{-(\tau/\tau_0)^\gamma}$ | fits some FX and futures data |
| Exponential | $G(\tau) = A e^{-\tau/\tau_0}$ | tractable; too fast for equity meta-orders |
| Multivariate Hawkes kernel | $G_{ij}(\tau)$ matrix of kernels | Bacry et al.; see [[methods/hawkes-process]] |

The paper of record ([[papers/bouchaud-farmer-lillo-propagator]]) argues for **slow power-law decay** as the best empirical fit on equities.

---

## Why it works (the long-memory reconciliation)

The empirical puzzle the propagator model solves:

- **Signed order flow is long-memory** — autocorrelation $\mathbb{E}[\varepsilon_t \varepsilon_{t+\tau}] \sim \tau^{-\gamma}$ with $\gamma < 1$ on most liquid equities, driven by meta-order splitting over days.
- **Prices are near-martingales** — returns have negligible autocorrelation at short horizons.

A *fixed* permanent impact model ($G(\tau) = \text{const}$) would imply predictable returns, contradicting martingality. A *purely temporary* impact model ($G$ with short memory) cannot explain why large metaorders move prices over days.

The propagator framework reconciles both: $G$ decays slowly enough to let long-memory flow accumulate into persistent price moves, yet fast enough that returns remain unpredictable. The two power-law exponents must satisfy a self-consistency relation: $\beta + \gamma/2 \approx 1$ (Bouchaud et al.).

---

## Deconvolution

The **raw** measured impact of meta-orders is biased upward at long lags because correlated subsequent trades from the same investor keep reinforcing the original direction. [[papers/brokmann-slow-decay-impact]] shows that after **deconvolving** the investor's own autocorrelated order flow, the mechanical propagator $I(\tau)$ decays essentially all the way to zero — the commonly-reported "2/3 plateau" is an artefact, not a structural feature.

Deconvolution proceeds via an OU-predictor toy model that yields an analytic convolution relating $I_\text{raw}$ to the true $I$ and the signal autocorrelation; inversion gives the true kernel.

---

## Stability / self-consistency

For the propagator to produce finite, stationary returns:

$$\int_0^\infty |G(\tau)|^2 \, d\tau < \infty$$

A fat-tailed $G$ with $\beta < 1/2$ can diverge. In multivariate (multi-asset, multi-event-type) extensions, the spectral radius of the kernel matrix must stay below 1 (same stability condition as for Hawkes processes).

---

## Computational complexity

- **Naive simulation**: $O(n^2)$ for $n$ events (each event sums over all past).
- **With exponential kernel**: $O(n)$ via recursive updates.
- **With sum-of-exponentials**: $O(Kn)$ for $K$ components — common approximation for power-law kernels.
- **Fitting / deconvolution**: iterative Wiener-filter-style inversion; or MLE under a specific kernel family.

---

## Applications in this wiki

| Paper | Role of propagator |
|---|---|
| [[papers/bouchaud-farmer-lillo-propagator]] | Introduces the framework; surveys empirics |
| [[papers/eisler-bouchaud-kockelkoren-order-book-events]] | Generalises propagator to six event types (MO/LO/CA × at-best/inside-spread). See [[methods/event-type-impact-decomposition]]. |
| [[papers/models-for-all-order-book-events]] | Fully dynamic extension — history-dependent bare impacts for small-tick stocks via linear AR model on gaps. |
| [[papers/brokmann-slow-decay-impact]] | Empirical calibration via deconvolution on CFM meta-orders |
| [[papers/reality-gap-lob-simulation]] | Embeds a power-law decay kernel into an extended queue-reactive simulator to reproduce concave impact during execution and partial reversion after |
| [[papers/order-flow-filtration]] | Uses Hawkes kernel norms — the multivariate generalisation — as diagnostic of OBI→return excitation |
| [[papers/csi300-ou-levy-ofi]] | OU-Lévy process is an alternative framing of the same "transient response to a shock" idea |

---

## When to use / when not to use

**Use when:**
- Modelling metaorder execution cost over minutes to days.
- Backtesting strategies where self-impact matters (propagator tells you the cost of your own trading).
- Reconciling long-memory order flow with near-martingale prices.

**Avoid or adapt when:**
- Sub-second horizons — individual event impact is more naturally modelled via queue dynamics (e.g., [[methods/queue-reactive-model]]).
- Non-stationary regimes (crashes, auctions) — $G$ is state-dependent; constant-kernel assumption breaks.
- Highly concave/non-linear interactions at large sizes — the linear superposition assumption becomes poor.

---

## Relationship to other impact models

| Model | Permanent? | Transient? | Nonlinearity |
|---|---|---|---|
| **Fixed permanent (Kyle)** | yes | no | any |
| **Propagator (BFL)** | no (decays to 0) | yes | linear superposition |
| **History-dependent permanent** | yes | yes | interpolates both |
| **Square-root meta-order law** | phenomenological | concave in $Q$ | emergent from propagator + long-memory |

The square-root law of meta-order impact $I(Q) \sim \sigma(Q/V)^{1/2}$ is an **emergent consequence** of the propagator + long-memory flow — it is not assumed; it falls out.

---

## Implementations

- **Hawkes libraries** (`tick.hawkes`, `hawkeslib`) implement multivariate propagator kernels.
- Custom MLE / Wiener-filter deconvolution in NumPy/SciPy suffices for exponential and power-law kernels.
- `LOBFrame` ([[papers/deep-lob-forecasting]]) does not model propagator impact explicitly — a gap that a hybrid LOBFrame+propagator simulator would close.

---

## Connections

- **Concept anchor**: [[concepts/price-impact]] — propagator is the dominant framework for *temporal* impact decomposition.
- **Sister method**: [[methods/hawkes-process]] — multivariate Hawkes kernels are propagator models on a point-process substrate. Strong overlap; Hawkes is to events as propagator is to returns.
- **Contrasts with**: [[methods/queue-reactive-model]] — QR is event-driven, Markovian, and local in time; propagator is aggregate and long-memory.
- **Empirical grounding**: [[papers/bouchaud-farmer-lillo-propagator]], [[papers/brokmann-slow-decay-impact]].
- **Practical integration**: [[papers/reality-gap-lob-simulation]] shows how to fold a propagator into an interactive LOB simulator.
