---
title: "Optimal Execution"
type: concept
created: 2026-04-16
updated: 2026-04-16
sources:
  - raw/papers/2603.28898.md
  - raw/papers/1704.00847.md
tags:
  - optimal-execution
  - market-microstructure
  - algorithmic-trading
  - market-impact
  - slippage
  - trading
related:
  - concepts/price-impact.md
  - concepts/market-microstructure.md
  - concepts/limit-order-book.md
  - concepts/order-flow-imbalance.md
  - methods/signal-aware-optimal-execution.md
  - methods/propagator-model.md
  - methods/almgren-chriss.md
  - papers/mpc-trade-execution.md
  - papers/price-impact-order-book-events.md
  - papers/lehalle-neuman-signals-optimal-trading.md
  - entities/charles-albert-lehalle.md
  - papers/brokmann-slow-decay-impact.md
  - papers/lipton-quote-imbalance.md
confidence: high
---

# Optimal Execution

## Definition

**Optimal execution** is the problem of trading a large order (the "metaorder" or "parent order") over a finite time window while balancing three intrinsically competing objectives:

- **Completion** — finish the order inside the window.
- **Market impact** — minimise the adverse price move caused by your own trading.
- **Opportunity / timing cost** — minimise slippage versus a benchmark (arrival price, VWAP, TWAP, or a custom reference) while avoiding exposure to adverse price moves.

It sits at the intersection of stochastic control, market microstructure, and production engineering.

---

## The canonical tradeoff

Two extreme policies frame the problem:

| Policy | Completion risk | Market impact | Opportunity cost |
|---|---|---|---|
| Full market order up front | None | Maximal | None (done in one shot) |
| Tiny passive limit-order slices over the full window | High (may not fill) | Minimal | High (exposed to drift) |

Good policies interpolate; that's where the modelling happens.

---

## Core frameworks

### Static schedules (classical era)

- **Bertsimas & Lo (1998)** — DP formulation under linear impact → optimum is **TWAP**; the baseline for flat linear impact.
- **[[methods/almgren-chriss|Almgren & Chriss (2001)]]** — mean-variance formulation penalises cost *uncertainty*; produces an **efficient frontier of execution paths** analogous to Markowitz. Static schedule set once before trading. Remains the industry-default baseline.
- **VWAP-tracking** — industry default; follows the intraday U-shaped volume profile. Introduced by Berkowitz et al.

### Dynamic / online methods

- **Cartea & Jaimungal** — mix of limit and market orders: post passively when ahead of schedule, cross the spread to catch up when behind. Rule-based online adjustment.
- **Busetti & Boyd (2005)** — LQG stochastic control under VWAP benchmark, handles revealed-volume uncertainty via DP.
- **Reinforcement Learning** (Nevmyvaka 2006; Hendricks–Wilcox; Moallemi–Wang; Li et al. hierarchical RL) — model-free execution policies trained directly on LOB data; action spaces vary from raw aggressiveness scalar to fractions of an Almgren-Chriss schedule.
- **Model Predictive Control** — treats execution as approximate DP with one-step lookahead and a rollout base policy; solves a fast QP per decision step. See [[papers/mpc-trade-execution]].

### Signal-aware frameworks

- **Lehalle-Neuman (2019)** — incorporate a Markovian (e.g. Ornstein-Uhlenbeck) signal into the Gatheral-Schied-Slynko transient-impact problem. Closed-form optimal schedule for OU signal + exponential-decay impact, linear in both initial inventory and initial signal value. See [[methods/signal-aware-optimal-execution]] and [[papers/lehalle-neuman-signals-optimal-trading]].
- **Cartea-Jaimungal (2015-)** — continuous absolutely-continuous trading under instantaneous impact + bounded Markov signal. The $\rho \to \infty$ limit of Lehalle-Neuman.
- Key empirical input: order-book imbalance is an OU-like signal, actively used by HFT market makers to tilt their trading rate.

---

## Slippage definitions (caveat lector)

There is no single "slippage". Common variants:

| Slippage type | Benchmark |
|---|---|
| Arrival slippage | Mid-price at order arrival |
| Interval slippage | Mid-price at each child-order placement |
| VWAP slippage | Volume-weighted average price over the window |
| Implementation shortfall | Arrival mid − execution average, including opportunity cost of unfilled shares |

Papers and brokers use different conventions — **always check which benchmark is being reported** before comparing algorithms.

---

## Connection to price impact

The cost of executing a metaorder is determined by the **impact function**. Two workhorses:

- **Linear impact on OFI** ([[papers/price-impact-order-book-events]]): $\Delta p \propto \text{OFI}$ with slope inversely proportional to market depth.
- **Square-root impact on volume**: $\Delta p \propto \sqrt{Q}$ for trade size $Q$. Cont et al. derive this from the linear OFI model via a scaling argument; Almgren-Chriss-style models take it as a primitive.
- **Power-law decay kernels** ([[papers/reality-gap-lob-simulation]]; Bacry et al.) — accumulate signed flow with a memory kernel so that impact decays toward mean reversion after execution, a key feature for realistic simulation.

See [[concepts/price-impact]] for the full picture.

---

## Open questions

- How much of the [[methods/almgren-chriss|Almgren-Chriss]] efficient frontier survives once realistic, non-linear, non-stationary impact is used?
- What is the right base policy for MPC rollout, and can it be learned rather than handcrafted?
- Are RL policies trained in simulation actually robust in live trading, or do they overfit to the simulator's impact model?
- Cross-venue routing (fragmented markets, dark pools) introduces a much richer action space — how do classical frameworks extend?
- ~~How should executed volume be sized against short-horizon [[concepts/order-flow-imbalance]] signals?~~ — largely addressed by [[methods/signal-aware-optimal-execution]] for OU-type signals; open for non-OU signals and for cross-asset OFI inputs.
- Does signal-aware execution admit transaction-triggered **price manipulation**? Lehalle-Neuman show non-monotone optimal strategies exist; the conditions on impact kernel and signal that rule out manipulation are open.
- How to handle signal-aware execution's **time inconsistency** under transient impact? Re-planning vs commit-at-$t=0$ vs collapse to CJ limit — no principled resolution.

---

## Connections

- **Impact theory**: [[concepts/price-impact]], [[papers/price-impact-order-book-events]].
- **Modern MPC approach**: [[papers/mpc-trade-execution]].
- **Simulator fidelity** for backtesting execution algos: [[papers/reality-gap-lob-simulation]].
- **LOB mechanics**: [[concepts/limit-order-book]].
- **Market-making (dual problem)**: posting vs taking is the same fundamental tradeoff seen from the liquidity-provider side.
