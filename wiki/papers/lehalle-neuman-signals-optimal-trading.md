---
title: "Incorporating Signals into Optimal Trading"
type: paper
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/1704.00847.md
tags:
  - optimal-execution
  - order-book-imbalance
  - ornstein-uhlenbeck
  - transient-impact
  - stochastic-control
  - signal-design
related:
  - concepts/optimal-execution.md
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - methods/signal-aware-optimal-execution.md
  - methods/propagator-model.md
  - methods/almgren-chriss.md
  - papers/cross-impact-ofi-equity-markets.md
  - papers/mpc-trade-execution.md
  - entities/charles-albert-lehalle.md
confidence: high
---

# Incorporating Signals into Optimal Trading

**Authors**: [[entities/charles-albert-lehalle|Charles-Albert Lehalle]], Eyal Neuman
**Institution**: Capital Fund Management; CFM-Imperial College Institute; Imperial College London
**Year**: 2017 (arXiv April 2017; published *Finance and Stochastics* 23(2), 2019)
**arXiv**: [1704.00847](https://arxiv.org/abs/1704.00847)
**Categories**: q-fin.TR, q-fin.MF

---

## Plain-language abstract

Classical optimal-execution theory (Almgren-Chriss, Bertsimas-Lo, Gatheral-Schied-Slynko, Cartea-Jaimungal) models a trader who wants to minimise trading costs while offloading a large inventory. These frameworks typically assume the underlying price is a martingale — no predictive information. But real traders run **short-horizon signals**, and they rationally tilt their schedule when the signal favours or opposes their direction. This paper plugs a generic Markovian signal into the Gatheral-Schied-Slynko framework (transient market impact with fuel constraint), proves existence and uniqueness of the optimal strategy, and derives a **closed-form solution for the Ornstein-Uhlenbeck signal + exponentially-decaying market impact case** — the standard assumption for order-book-imbalance (OBI) signals. Empirically the paper calibrates OBI on NASDAQ OMX (13 stocks, 9 months, ~9B trades) and shows HFT market makers and proprietary traders already condition their trading rate on it. The OU model for OBI is empirically supported.

---

## Key contributions

1. **Signal-in-GSS theorem (existence & uniqueness)** — For a generic càdlàg Markov signal $I$ and strictly positive-definite impact kernel $G$, the optimal deterministic admissible execution strategy for the cost functional

$$\mathcal{C}(X) = \mathbb{E}\left[\int_0^T I_s X_s ds + \frac{1}{2}\int_0^T\!\int_0^T G(|t-s|) dX_t dX_s + \phi \int_0^T X_t^2 dt\right]$$

exists and is unique. Characterised as the solution to an integral equation (Theorems 2.3, 2.4 in the paper).

2. **Closed-form for OU signal + exponential impact** (Corollary 2.7) — When $I$ is Ornstein-Uhlenbeck with mean-reversion rate $\gamma$ and volatility $\sigma$, and $G(t) = \kappa \rho e^{-\rho t}$ (Obizhaeva-Wang-style decay), the optimal schedule $X^*_t$ is **linear in both initial inventory $x$ and initial signal value $\iota$**, plus a time-varying drift from OU dynamics. Reduces to Obizhaeva-Wang (2013) when $\iota = 0$.

3. **Asymptotic equivalence of GSS → CJ frameworks** — As the impact decay rate $\rho \to \infty$, the transient impact kernel converges to Dirac delta (instantaneous impact), the singular GSS strategy's jumps vanish, and the optimal schedule becomes a smooth function matching the Cartea-Jaimungal framework. First bridge between the two literatures in a signal-enriched setting.

4. **Non-monotone optimal strategies** — With a signal, the optimal execution is **not necessarily monotone in inventory**. A seller may temporarily *buy* when the signal points the wrong way. This opens the possibility of **transaction-triggered price manipulation** within a valid model. An open question: what conditions on $G$ and $I$ prevent this?

5. **Empirical validation of OBI as an OU signal** — 9 months, 13 stocks, NASDAQ OMX. OBI is predictive of the next price move, exhibits mean-reverting behaviour consistent with an OU process, and calibration gives concrete $\gamma$, $\sigma$ estimates.

6. **Evidence practitioners use OBI** — Using NASDAQ OMX's counterparty-identified trade data, the authors classify participants into four categories (global investment banks, institutional brokers, HFT market makers, HFT proprietary traders) and show that **HFT participants systematically condition their trading rate on OBI**, while long-only investors and brokers do not. Direct evidence that the signal-in-execution model is not just theoretical.

7. **Time-inconsistency discussion** — Transient impact creates a control-theoretic inconsistency: the optimal strategy on $[0, T]$ computed at $t=0$ is not in general the same as the concatenation of optimal strategies on $[t, T]$ computed at $t$. Three practical options discussed: commit to the $t=0$ optimal, re-plan continuously (approximate), or use the (CJ) instantaneous-impact limit (time-consistent).

---

## Method summary

### Model setup

Asset price decomposes as $P_t = M_t + \int_0^t I_s ds$, where $M$ is a martingale and $I$ is the signal (drift component). Trader's visible price with transient impact:

$$S_t \;=\; P_t \;+\; \int_0^t G(t - s) \, dX_s$$

where $X_t$ is inventory held at time $t$ and $G$ is the impact decay kernel. Fuel constraint: $X_T = 0$ (liquidate fully).

### Cost functional (GSS + signal)

$$\mathcal{C}(X) \;=\; \mathbb{E}\left[\int_0^T I_s X_s ds + \frac{1}{2}\int_0^T\!\int_0^T G(|t-s|)\, dX_t\, dX_s + \phi \int_0^T X_t^2 dt\right]$$

The three terms:
- $\int I_s X_s ds$ — the **signal-inventory term**. Having inventory $X_s$ during a signal $I_s > 0$ is profitable for a buyer (price going up) or costly for a seller.
- $\frac{1}{2} \iint G(|t-s|) dX_t dX_s$ — **impact cost**. Quadratic form in the flow $dX$.
- $\phi \int X_t^2 dt$ — **inventory risk penalty**.

### Optimal schedule for OU + exponential impact

With $I_t$ OU and $G(t) = \kappa\rho e^{-\rho t}$, the optimal strategy has the form:

$$X^*_t \;=\; b_0(t) \cdot x \;+\; b_1(t) \cdot I_0 \;+\; b_2(t) \cdot \int_0^t e^{-\gamma(t-s)} dW_s$$

for explicit functions $b_0, b_1, b_2$ depending on $\gamma, \sigma, \kappa, \rho, T$. Linear in initial inventory $x$ and initial signal $I_0$. Jumps occur at $t = 0$ and $t = T$ (singular part of the strategy), continuous in between.

### Cartea-Jaimungal limit

In the $\rho \to \infty$ (impact instantaneous) limit with instantaneous-impact kernel $G(dt) = \kappa \delta_0$, the framework reduces to a standard HJB problem. With terminal penalty $\varrho X_T^2$ instead of the fuel constraint:

$$r^*_t \;=\; \frac{v_1(t, I_t) - 2 v_2(t) X_t}{2\kappa}$$

where $v_1, v_2$ solve a system of ODEs (Proposition 3.1). Matches Cartea-Jaimungal with a signal.

---

## Empirical results

### Data

- NASDAQ OMX (Nordic European exchange), 9 months.
- 13 stocks, > 9 billion transactions.
- CFM proprietary order-book database merged with NASDAQ OMX's counterparty-identified trade tape.

### OBI as a signal

Define OBI at the best quotes. Shown:
- Positive correlation with next-move direction.
- Mean-reverting; OU fit passes standard diagnostics.
- Typical calibration range: $\gamma \in [0.1, 1]$ per minute, $\sigma$ stock-dependent.

### Who uses OBI?

Average OBI value *just before* each trade, split by counterparty class:

| Class | Conditional on signal? |
|---|---|
| Global investment banks | No / weak |
| Institutional brokers | No |
| HFT market makers | **Yes — strongly** |
| HFT proprietary traders | **Yes — strongly** |

Fig. 9 of the paper shows trading speed as a function of OBI within a 10-minute window — monotone-increasing, matching the theory's prediction that signal-aware strategies condition on current signal state.

---

## Limitations

- **Deterministic strategies only.** Theorems cover strategies using $I_0$ alone, not signal-adaptive strategies (Remark 2.9). The latter is explicitly flagged as open.
- **Price manipulation possibility** is not resolved. Non-monotone strategies can arise; conditions that rule out manipulation are an open problem.
- **Linear cost structure.** Impact enters quadratically (linear marginal impact per unit of flow). Realistic impact is concave (square-root law) at larger sizes.
- **Specific kernel pair.** Closed form is only for OU signal + exponential decay kernel. Other combinations (power-law decay, jump-diffusion signals) are not treated explicitly.
- **Time inconsistency.** The framework is acknowledged time-inconsistent under transient impact; three workarounds discussed but no principled resolution.
- **European mid-cap universe.** Empirical validation is 13 NASDAQ-OMX stocks; US large-caps or futures may behave differently.
- **Counterparty classification.** The four-class taxonomy depends on NASDAQ-OMX metadata that is no longer published (post-2014).

---

## Connections to other wiki pages

- **Framework**: [[concepts/optimal-execution]] — extends with an explicit signal term in the cost functional.
- **Signal source**: [[concepts/order-flow-imbalance]] — the OU model for OBI connects the execution theory back to the empirical OFI literature.
- **Impact primitive**: [[methods/propagator-model]] — the GSS transient-impact kernel is a propagator; the paper uses the exponential decay variant (Obizhaeva-Wang). The paper's empirical results on OBI mean-reversion parallel the propagator's $\tau^{-\beta}$ decay story.
- **Method**: [[methods/signal-aware-optimal-execution]] (new) — the general framework this paper introduces.
- **Natural companion**: [[papers/cross-impact-ofi-equity-markets]] — OBI-driven execution naturally extends to multi-asset settings using cross-asset OFI as the signal.
- **Cartea-Jaimungal**: referenced extensively but not (yet) in this wiki as a dedicated paper page. Their framework is the $\rho \to \infty$ limit.

### Signal-design takeaways

For someone building an L3 / LOB-snapshot signal *specifically for execution*:

1. **Model your signal as an OU process.** OBI and related features are empirically mean-reverting; an OU calibration plugs directly into the closed-form schedule of Corollary 2.7.
2. **Estimate signal $\gamma$ (mean-reversion rate) before anything else.** The optimal tilt in the schedule is a function of $\gamma$ and the fuel horizon $T$ — mis-estimating $\gamma$ rescales the effective signal size incorrectly.
3. **Use the signal even if you can only use its value at $t=0$.** The deterministic-strategy theorem guarantees the closed-form schedule with only initial-signal information is a valid optimiser. Adaptive updating is better but not strictly necessary.
4. **Size impact carefully.** The exponential-decay rate $\rho$ interacts with $\gamma$ — if $\rho \ll \gamma$, the signal changes faster than impact resolves, and the schedule flattens. If $\rho \gg \gamma$, you're effectively in the CJ instantaneous-impact regime.
5. **Watch for non-monotone orders.** If your closed-form says to buy while liquidating, that's mathematically optimal but may be blocked by pre-trade risk controls, cross-venue best-execution rules, or internal compliance. Bake a monotonicity constraint in if needed — at a cost.
6. **HFTs already do this.** If you're a slower trader, the signal is already partially priced in by HFT flow that reacts faster than you can. Check the post-HFT residual information content before relying on OBI too heavily.
