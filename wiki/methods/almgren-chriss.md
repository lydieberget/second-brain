---
title: "Almgren-Chriss Model"
type: method
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/0809.0822.md
  - raw/papers/1407.3390.md
  - raw/papers/1704.00847.md
  - raw/papers/2603.28898.md
tags:
  - optimal-execution
  - mean-variance
  - market-impact
  - execution-schedule
related:
  - concepts/optimal-execution.md
  - concepts/price-impact.md
  - methods/propagator-model.md
  - methods/signal-aware-optimal-execution.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/brokmann-slow-decay-impact.md
  - papers/lehalle-neuman-signals-optimal-trading.md
  - papers/mpc-trade-execution.md
confidence: high
---

# Almgren-Chriss Model

## Algorithm description

The **Almgren-Chriss model** (2001) is the canonical static mean-variance framework for optimal execution of a large order. It splits impact into a permanent linear component and a temporary linear component, then minimises the Markowitz-style cost functional

$$\mathcal{C}(X) \;=\; \mathbb{E}[\text{execution cost}] \;+\; \lambda \cdot \text{Var}[\text{execution cost}]$$

over a deterministic trading schedule $X_t$ on $[0, T]$ with $X_0 = x$ (initial inventory) and $X_T = 0$ (full liquidation).

The continuous-time solution is an **exponentially-decaying trading rate**:

$$X^*_t \;=\; x \cdot \frac{\sinh(\kappa (T - t))}{\sinh(\kappa T)}, \qquad \kappa = \sqrt{\lambda \sigma^2 / \eta}$$

where $\sigma$ is volatility, $\eta$ is the temporary-impact coefficient, and $\lambda$ is the risk-aversion parameter. Rate $dX^*_t / dt$ is highest near $t = 0$ and $t = T$, lowest in the middle — unless $\lambda = 0$, in which case the optimum collapses to uniform trading (**TWAP**).

---

## The cost model

Almgren-Chriss assumes two linear impact components:

- **Permanent impact** $g(\dot X_t) = \gamma \dot X_t$: a drift term that persists. Quadratic contribution to total cost via $\int \dot X \cdot X \, dt$.
- **Temporary impact** $h(\dot X_t) = \eta \dot X_t$: a slippage on each instantaneous trade. Quadratic contribution via $\int \eta \dot X_t^2 \, dt$.

Expected cost:

$$\mathbb{E}[\text{cost}] \;=\; \frac{\gamma}{2} x^2 \;+\; \eta \int_0^T \dot X_t^2 \, dt$$

Cost variance (from unhedged price risk on remaining inventory):

$$\text{Var}[\text{cost}] \;=\; \sigma^2 \int_0^T X_t^2 \, dt$$

The minimiser of $\mathbb{E} + \lambda \text{Var}$ is the closed-form $X^*_t$ above.

---

## The efficient frontier

Varying $\lambda$ traces out an **efficient frontier** analogous to Markowitz portfolio theory:

- $\lambda \to 0$: risk-neutral, schedule is TWAP (uniform trading), cost minimised but variance maximal.
- $\lambda \to \infty$: risk-averse, schedule front-loads aggressively to shrink exposure time, cost high but variance minimal.
- Intermediate $\lambda$: exponential-decay schedule trading off cost vs variance.

Practitioners pick a point on the frontier based on their mandate (cost-sensitive asset manager vs urgency-sensitive portfolio liquidator).

---

## Variants and extensions

| Variant | Modification |
|---|---|
| Bertsimas-Lo (1998) | Discrete-time DP; linear impact; no risk term → always TWAP. Precursor to AC. |
| Almgren-Chriss (2001) | Adds quadratic risk term; introduces the efficient frontier. |
| Almgren (2003) | Nonlinear (power-law) temporary impact; preserves closed-form family. |
| Obizhaeva-Wang (2013) | Replaces the flat impact with **transient impact** (exponential decay kernel); schedule becomes singular (jumps at endpoints). |
| Gatheral-Schied-Slynko | Generalises Obizhaeva-Wang to arbitrary positive-definite decay kernels. See [[methods/propagator-model]]. |
| Cartea-Jaimungal | Instantaneous impact + continuous adaptive trading with a Markovian signal. |
| **Lehalle-Neuman** | Adds a Markovian signal to GSS. See [[methods/signal-aware-optimal-execution]]. |

The lineage is: Almgren-Chriss → Obizhaeva-Wang (add impact decay) → Lehalle-Neuman (add signal). Almgren-Chriss is the baseline every subsequent framework compares against.

---

## Why it's the baseline

Every modern execution paper benchmarks against Almgren-Chriss because:

1. **Analytical tractability.** Closed-form schedule, closed-form cost, closed-form variance. Easy to sanity-check numerical algorithms.
2. **Interpretability.** The three parameters $(\sigma, \eta, \lambda)$ each map to a concrete intuition (volatility, temporary impact, risk aversion).
3. **Industry default.** TWAP and VWAP algos are AC special cases ($\lambda \to 0$ and $\lambda \to 0$ with volume-weighting respectively). Any new algorithm needs to beat AC on either cost, variance, or robustness to non-stationarity.
4. **Pedagogical clarity.** The mean-variance structure mirrors portfolio theory, making the tradeoff legible to anyone with a Markowitz background.

---

## When to use / when not to

**Use when:**
- You need a quick, interpretable baseline schedule.
- Your market has roughly linear temporary impact and you're only trading a few tens of minutes.
- You want the simplest possible risk-adjusted execution plan.

**Don't use when:**
- Impact is strongly concave (square-root law dominates at larger sizes).
- You have a short-horizon signal you want to exploit — use [[methods/signal-aware-optimal-execution]] or MPC instead.
- Market impact is transient with long memory — use [[methods/propagator-model]] for correct self-impact accounting.
- You need an adaptive online strategy — AC is a static schedule set once at $t = 0$.

---

## Limitations

- **Linear impact is a strong assumption.** Empirical impact is concave (square-root law); AC underestimates cost for large orders.
- **Permanent-vs-temporary split is a modelling convention.** Real impact decays on multiple timescales; AC collapses this into two numbers.
- **No signal awareness.** The schedule doesn't react to market information. Any predictive edge is left on the table.
- **No transaction costs or fees.** These are assumed folded into $\eta$ but rarely dominate the shape of the solution.
- **No multi-venue routing.** Modern fragmented markets require cross-venue decisions AC doesn't address.
- **Deterministic schedule.** The realised path doesn't adapt to the actual fills — in practice, brokers re-plan periodically, which is an ad-hoc patch on AC's static nature.

---

## Implementations

- **Industry**: virtually every broker's execution desk ships an AC-based algorithm as the "urgency slider" control ($\lambda$) on implementation-shortfall schedulers.
- **Open source**: `QuantLib`, `pyfolio-execution`, and many Python execution toolkits include AC as a reference.
- **In this wiki**: referenced as baseline in [[papers/mpc-trade-execution]] (MPC improves on AC), [[papers/lehalle-neuman-signals-optimal-trading]] (AC is the no-signal limit), [[papers/brokmann-slow-decay-impact]] (propagator-corrected AC cost estimates), and [[papers/bouchaud-farmer-lillo-propagator]] (AC's permanent-impact component contradicts the empirical slow-decay story).

---

## Connections

- [[concepts/optimal-execution]] — AC is the canonical mean-variance baseline.
- [[concepts/price-impact]] — AC's linear-impact assumption is the first-order model; more realistic variants (square-root, propagator) refine it.
- [[methods/propagator-model]] — transient-impact replacement for AC's flat temporary impact.
- [[methods/signal-aware-optimal-execution]] — signal-augmented extension of AC via the Lehalle-Neuman framework.
- [[papers/bouchaud-farmer-lillo-propagator]] — argues the AC permanent-impact primitive is empirically implausible.
- [[papers/mpc-trade-execution]] — modern data-driven alternative to AC.
