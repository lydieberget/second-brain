---
title: "Model Predictive Control For Trade Execution"
type: paper
created: 2026-04-16
updated: 2026-04-16
sources:
  - raw/papers/2603.28898.md
tags:
  - optimal-execution
  - model-predictive-control
  - algorithmic-trading
  - market-impact
  - slippage
  - quadratic-programming
  - dynamic-programming
related:
  - concepts/optimal-execution.md
  - concepts/price-impact.md
  - concepts/market-microstructure.md
  - concepts/limit-order-book.md
  - papers/price-impact-order-book-events.md
  - methods/signal-aware-optimal-execution.md
  - methods/almgren-chriss.md
confidence: high
---

# Model Predictive Control For Trade Execution

**Authors**: Thomas P. McAuliffe, Samuel Liew, Yuchao Li, Andrey Ushenin, Chihang Wang, Alexandros Tasos, Jack Pearce, Dimitris Tasoulis, **Dimitri P. Bertsekas**, Theodoros Tsagaris
**Institutions**: Bayforest Technologies (London); Arizona State University; MIT
**Year**: 2026 (April 2026)
**arXiv**: [2603.28898](https://arxiv.org/abs/2603.28898)
**Categories**: q-fin.TR

---

## Plain-language abstract

Executing a large client order in a continuous double-auction market means balancing three competing objectives:

- **Completion risk** — finish inside the window.
- **Market impact cost** — pushing price against yourself by trading fast.
- **Opportunity cost** — missing favourable moves by trading slow.

Static schedules like TWAP / VWAP are the industry workhorse but cannot react online to changing liquidity or short-horizon signals. This paper proposes a **production-grade MPC (Model Predictive Control) framework** that at each decision step solves a **fast quadratic program** trading off expected cost against deviation from the schedule, with a **residual cost term from a base policy** (a rollout approximation). On 6 months of NASDAQ Level-3 data, the MPC algorithm reduces **schedule shortfall by 40–50%** vs spread-crossing benchmarks and materially cuts slippage. Adding predictive price information on top improves results further.

---

## Key contributions

1. **MPC = approximate DP for execution** — cast the execution problem as a stochastic discrete-time control problem; at each stage, do one-step lookahead with a learned cost-to-go $\tilde J_{t+1}$ approximating future stage costs via **rollout** of a simple base policy. Scales and runs in production time; exact DP is intractable.
2. **Fast quadratic-program per decision step** — trade off expected transaction cost against schedule deviation, with **explicit bounds** on schedule adherence and **variance constraints** for direct risk control. Runs fast enough to manage hundreds–thousands of simultaneous orders without stale state.
3. **Modular, production-oriented design** — explicit separation of concerns (single-responsibility components with their own KPIs, per Li et al.'s hierarchical-RL spirit) so forecasting, scheduling, and placement can be improved independently.
4. **Rich action space** — not just market/limit binary; full parameterisation across order types, venues, brokers, ATSs. Interactions can happen at Level-3 granularity.
5. **Empirically validates against strong baselines** — spread-crossing, pure TWAP/VWAP, and industry broker algorithms on NASDAQ L3 data for 6 months.

---

## Method summary

### Stochastic control formulation
- State $x_t$ = market state (prices, volatility, book features) + order state (filled quantity, schedule residual).
- Control $u_t$ = vector of child orders (prices, sizes, venues) drawn from feasibility set $U_t(x_t)$.
- Disturbance $w_t$ = market-driven uncertainty in fills and future prices.
- Dynamics $x_{t+1} = f_t(x_t, u_t, w_t)$.
- Objective: minimise $\mathbb{E}\left[g_T(x_T) + \sum_{t=0}^{T-1} g_t(x_t, u_t, w_t)\right]$.

### MPC with rollout

$$\tilde u_t \in \arg\min_{u_t \in U_t(x_t)} \mathbb{E}\bigl\{ g_t(x_t, u_t, w_t) + \tilde J_{t+1}\bigl(f_t(x_t, u_t, w_t)\bigr) \bigr\}$$

- **Base policy** for rollout: a simple, well-understood strategy (e.g., TWAP-tracking spread cross) whose expected residual cost $\tilde J_{t+1}$ approximates the value function.
- Per-step optimisation is a **quadratic program**: quadratic in $u_t$ (convex transaction cost + schedule-deviation penalty), linear + variance constraints.
- Solves in low milliseconds, enabling realistic deployment.

### Objectives & constraints
| Objective | Control mechanism |
|---|---|
| Schedule adherence | Explicit bounds on cumulative deviation from TWAP/VWAP |
| Cost minimisation | Quadratic penalty on expected spread + impact |
| Risk | Variance constraint on deviation |
| Opportunity | Residual cost from rollout base policy |

### Extensions considered
- Augmenting $\tilde J_{t+1}$ with **predictive price information** further improves performance — demonstrates the framework's plug-in flexibility for alpha signals or microstructure forecasters.
- Multistep MPC lookahead is flagged as future work; the paper uses one-step lookahead + rollout only.

---

## Main results (NASDAQ L3, 6 months)

- **Schedule shortfall reduced by ≈ 40–50%** vs spread-crossing benchmarks.
- Significant improvements in **slippage** (arrival-price, VWAP, and interval slippage — defined in Section 5.2 of the paper).
- Adding a simple predictive price component on top of the rollout base policy gives a further performance lift.
- The QP per decision step is fast enough for live deployment with realistic order counts.

---

## Relation to prior work

| Strand | Paper | Role |
|---|---|---|
| DP for execution | Bertsimas & Lo 1998 | TWAP as DP optimum under linear impact |
| Mean-variance execution | Almgren & Chriss 2001 | Efficient frontier of paths; static |
| Dynamic VWAP | Busetti & Boyd 2005 | LQG stochastic control with revealed-volume uncertainty |
| Limit + market mix | Cartea & Jaimungal 2015 | Passive when ahead, aggressive when behind |
| RL-based | Nevmyvaka et al. 2006 | Q-learning directly on NASDAQ LOB |
| RL mapping to schedule | Hendricks & Wilcox | Action = fraction-of-Almgren-Chriss |
| Price-forecast RL | Moallemi & Wang | DDQN with return-forecast features |
| Hierarchical RL | Li et al. | Macro / meta / micro separation — this paper adopts the spirit |
| Prior MPC | Clinet et al.; Plessen & Bemporad | Earlier MPC framings, less production-oriented |

MPC is acknowledged to be **closely related to RL** — some of the most reliable RL methods *are* MPC (per Bertsekas's own RL/MPC textbooks). This paper positions MPC as a pragmatic sweet spot between rigid static schedules and full-stack RL.

---

## Limitations

- **One-step lookahead only** — multistep MPC is left for future work.
- **Single market**: NASDAQ L3 only; cross-venue / dark-pool / ATS routing is in scope conceptually but not benchmarked.
- **Base-policy dependence**: the rollout quality depends on the base policy; a poor base policy yields a poor $\tilde J_{t+1}$ approximation.
- **No live trading validation**: backtests on simulated orders against 6 months of L3 data — simulator fidelity matters (see [[papers/reality-gap-lob-simulation]] for why this is non-trivial).
- **No formal regret bound**: empirical wins, no theoretical optimality guarantee versus the true DP solution.

---

## Connections

- Defines the central execution tradeoff: see [[concepts/optimal-execution]] for the concept page.
- Builds on the Almgren–Chriss / Bertsimas–Lo / Cartea–Jaimungal lineage of optimal-execution research.
- Complementary to [[papers/reality-gap-lob-simulation]] — any serious MPC evaluation needs a simulator that reproduces market impact realistically; combining the two gives a credible offline evaluation stack.
- Impact modelling connects to [[concepts/price-impact]] and the OFI-based linear impact of [[papers/price-impact-order-book-events]].
