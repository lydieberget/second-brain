---
title: "Signal-Aware Optimal Execution"
type: method
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/1704.00847.md
tags:
  - optimal-execution
  - stochastic-control
  - market-impact
  - ornstein-uhlenbeck
  - transient-impact
  - signal-design
related:
  - concepts/optimal-execution.md
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - methods/propagator-model.md
  - papers/lehalle-neuman-signals-optimal-trading.md
  - papers/mpc-trade-execution.md
  - entities/charles-albert-lehalle.md
confidence: high
---

# Signal-Aware Optimal Execution

## Algorithm description

**Signal-aware optimal execution** extends classical optimal-execution theory (Almgren-Chriss, Obizhaeva-Wang, Gatheral-Schied-Slynko, Cartea-Jaimungal) by adding a **short-horizon predictive signal** $I_t$ to the underlying price dynamics. The trader solves a stochastic control problem in which three objectives compete:

1. **Impact cost** — the unwanted price move caused by their own trading.
2. **Inventory risk** — exposure to price moves while holding non-zero inventory.
3. **Signal alpha** — the expected return from holding inventory aligned with the signal direction.

Formally, for inventory $X_t$ decreasing from $x$ to 0 over $[0, T]$, the cost functional is:

$$\mathcal{C}(X) \;=\; \mathbb{E}\left[\underbrace{\int_0^T I_s X_s ds}_{\text{signal term}} \;+\; \underbrace{\tfrac{1}{2}\int_0^T\!\!\int_0^T G(|t-s|)\, dX_t\, dX_s}_{\text{impact cost}} \;+\; \underbrace{\phi \int_0^T X_t^2 dt}_{\text{risk penalty}} \right]$$

where $G$ is the transient impact kernel and $\phi \geq 0$ is the risk aversion. The optimal $X^*$ minimises $\mathcal{C}$ over admissible (deterministic, finite-variation, fuel-constrained) strategies.

---

## Two flavours

| Framework | Impact kernel $G$ | Terminal condition | Optimal form |
|---|---|---|---|
| **GSS (Gatheral-Schied-Slynko)** | transient, e.g. $G(t) = \kappa\rho e^{-\rho t}$ | hard fuel constraint $X_T = 0$ | singular (jumps at $t = 0, T$) |
| **CJ (Cartea-Jaimungal)** | instantaneous, $G(dt) = \kappa \delta_0$ | soft penalty $\varrho X_T^2$ | smooth (absolutely continuous) |

As the decay rate $\rho \to \infty$, the GSS framework's singular jumps vanish and the schedule converges to the CJ smooth schedule (Lehalle-Neuman 2019).

---

## Closed-form for OU signal + exponential impact

Under the assumptions:

- Signal $I_t$ is Ornstein-Uhlenbeck: $dI_t = -\gamma I_t\, dt + \sigma dW_t$
- Impact kernel: $G(t) = \kappa \rho e^{-\rho t}$
- Zero risk aversion: $\phi = 0$

The optimal schedule decomposes into three components (Lehalle-Neuman Corollary 2.7):

$$X^*_t \;=\; b_0(t) \cdot x \;+\; b_1(t) \cdot I_0 \;+\; b_2(t) \cdot \int_0^t e^{-\gamma(t-s)} dW_s$$

where:
- $b_0(t)$ is the **no-signal schedule** (Obizhaeva-Wang style liquidation curve).
- $b_1(t)$ scales the **initial-signal correction** — weighted linearly in $I_0$.
- $b_2(t)$ is the **OU residual correction** — depends on the signal path after $t = 0$ (only non-zero for signal-adaptive strategies).

Jumps at $t = 0$ (initial burst) and $t = T$ (final burst) are part of the singular control; the continuous middle portion rides the signal.

---

## Key parameters

| Parameter | Interpretation |
|---|---|
| $T$ | Execution horizon (fuel window) |
| $x$ | Initial inventory to liquidate |
| $\gamma$ | Signal mean-reversion rate (1/minute typically) |
| $\sigma$ | Signal volatility |
| $\kappa$ | Impact scale |
| $\rho$ | Impact decay rate |
| $\phi$ | Inventory risk aversion |
| $\varrho$ | Terminal penalty (CJ only) |

**Interaction effect**: if $\rho \ll \gamma$ (impact persists longer than signal auto-correlation), the signal tilt in the schedule is muted. If $\rho \gg \gamma$, the framework collapses to the instantaneous-impact CJ limit.

---

## Empirical calibration recipe

For deploying signal-aware execution on a real universe:

1. **Choose the signal.** Typical choice: order-book imbalance (OBI) at best, multi-level OFI, or [[methods/integrated-ofi|integrated OFI]]. OBI is empirically OU on NASDAQ OMX data.
2. **Calibrate $\gamma, \sigma$** of the OU signal from a recent window (30 min – 1 day of minute bars).
3. **Estimate $\kappa, \rho$** from your own trading history. $\rho$ is notoriously unstable — see [[methods/propagator-model]] literature for alternative transient-impact calibrations.
4. **Choose $\phi$** from your risk budget — trades off execution time vs holding risk.
5. **Plug into closed form.** For OU signal + exponential impact, Corollary 2.7's formula gives the schedule in closed form. For other kernels, solve the integral equation (2.7) numerically.

---

## Non-monotonicity and price manipulation

A striking consequence of signal-aware execution is that **the optimal inventory path is not always monotone**. If the signal opposes the trade direction early, the optimal strategy may *increase* inventory (buy while liquidating) before reversing.

This creates a theoretical possibility of **transaction-triggered price manipulation**: a trader could in principle engineer a sequence of trades whose total expected cost is *lower* than unwinding the position, by exploiting the interaction between their own impact and the signal. Open problem: what restrictions on $G$ and $I$ rule this out? (Remark 2.10 of the paper.)

Practical implication: pre-trade risk and compliance checks may flag non-monotone schedules. A monotonicity constraint imposes extra cost but may be required.

---

## Time inconsistency

Under transient impact, the problem is **time-inconsistent**: the optimum on $[0, T]$ computed at $t = 0$ is not the concatenation of optima on $[t, T]$ computed at each $t$. Three practical resolutions:

1. **Commit**: use the $t = 0$ optimal schedule for the full horizon. Gives the best total cost but can't react to new information.
2. **Re-plan**: solve a new $t_0 = t$ problem periodically with remaining inventory as initial condition. Approximate — no longer globally optimal.
3. **Use CJ limit**: drop transient impact ($\rho \to \infty$). Time-consistent, fully adaptive, but loses the structural impact-decay information.

In practice, re-planning at a moderate frequency (e.g. every 1 minute) is the pragmatic choice.

---

## When to use / when not to

**Use when:**
- You have a predictive short-horizon signal with documented mean-reversion (OBI, OFI, microprice deviation).
- You execute large orders and need to balance signal alpha vs market impact.
- Your execution horizon is minutes to hours — where signal persistence is comparable to impact decay.

**Don't use when:**
- Signal horizon $\ll$ execution horizon: signal has decayed before you can act on it. Use the no-signal Obizhaeva-Wang schedule.
- Signal horizon $\gg$ execution horizon: the signal is essentially constant drift. Almgren-Chriss with a simple drift term is simpler and sufficient.
- Non-linear impact matters (large order / thin market): the quadratic-impact assumption underpredicts cost for big trades.

---

## Relationship to other execution methods

| Method | Signal-aware? | Impact kernel | Strategy type |
|---|---|---|---|
| TWAP / VWAP | No | Implicit linear | Static schedule |
| Almgren-Chriss | No | Linear, no decay | Static mean-variance |
| Obizhaeva-Wang | No | Exponential decay | Singular |
| Cartea-Jaimungal | Bounded Markov signal | Instantaneous | Absolutely continuous |
| GSS (Gatheral-Schied-Slynko) | No | Arbitrary positive-definite | Singular |
| **Lehalle-Neuman (signal in GSS)** | Markov signal | Transient | Singular |
| MPC execution | Data-driven signal | Learned | Absolutely continuous |

---

## Connections

- [[concepts/optimal-execution]] — the parent concept.
- [[concepts/order-flow-imbalance]] — OBI is the canonical signal for this method.
- [[methods/propagator-model]] — supplies the transient impact kernel $G$.
- [[papers/lehalle-neuman-signals-optimal-trading]] — the defining reference.
- [[papers/mpc-trade-execution]] — modern data-driven alternative using MPC.
- [[papers/cross-impact-ofi-equity-markets]] — multi-asset OFI, natural signal input for a multi-asset extension.
