---
title: "Slow Decay of Impact in Equity Markets"
type: paper
created: 2026-04-17
updated: 2026-04-17
sources:
  - raw/papers/1407.3390.md
tags:
  - market-impact
  - meta-order
  - impact-decay
  - propagator-model
  - deconvolution
  - equity-markets
  - signal-design
related:
  - concepts/price-impact.md
  - concepts/order-flow-imbalance.md
  - concepts/optimal-execution.md
  - methods/propagator-model.md
  - methods/almgren-chriss.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/price-impact-order-book-events.md
  - entities/jean-philippe-bouchaud.md
confidence: high
---

# Slow Decay of Impact in Equity Markets

**Authors**: X. Brokmann, E. Sérié, J. Kockelkoren, J.-P. Bouchaud
**Institution**: Capital Fund Management, Paris
**Year**: 2014 (arXiv July 2014; published *Market Microstructure and Liquidity* 2015)
**arXiv**: [1407.3390](https://arxiv.org/abs/1407.3390)
**Categories**: q-fin.TR, cond-mat.stat-mech

---

## Plain-language abstract

After a large meta-order finishes executing, does its price impact **decay to zero** (mechanical, purely technical) or **plateau at some fraction** of the peak (a signature that the trade was informed and the information has been permanently impounded)? Prior empirical work was split. This paper uses **CFM's proprietary meta-order data + prediction signals** and a deconvolution method to separate the impact of a single meta-order from the impact of all *correlated subsequent trades*. Finding: after proper deconvolution, impact **decays essentially all the way to zero** — possibly as a power-law — over ~10 trading days. The apparent plateau seen in the raw, un-deconvolved data is a statistical artefact of order-flow autocorrelation (order splitting across days), not genuine permanent impact. The square-root law of peak impact is confirmed with $\delta \approx 0.6$.

---

## Key contributions

1. **Decomposition of measured meta-order impact**:

   $$\mathbb{E}[p(t + \tau) - p(t) \mid \text{metaorder at } t] = \theta(Q) \cdot I(\tau) + \alpha \cdot H(\tau)$$

   where:
   - $\theta(Q) = \epsilon(Q) Y_0 \sigma (Q/V)^\delta$ is the instantaneous **square-root impact** ($\delta \approx 0.6$ empirically; $Y_0$ order 1),
   - $I(\tau)$ is the **mechanical impact propagator** decaying from $I(0) = 1$ to $I(\infty) \approx 0$,
   - $\alpha$ is the predictor amplitude (zero for uninformed trades),
   - $H(\tau)$ is the way the prediction realises over time (e.g., $H(\tau) = 1 - e^{-\Gamma \tau}$ for an OU predictor).

2. **Deconvolution method** to separate $I(\tau)$ from the raw measured profile. Shows that autocorrelated order flow (the same trader executing a series of same-signed orders over days) artificially inflates the apparent long-horizon plateau when no deconvolution is applied.

3. **Toy-model demonstration**: an optimising investor with an OU signal and instantaneously-decaying true impact produces a raw measured impact that *appears* to decay slowly — purely because the investor's continued trading keeps reinforcing the original direction. Proves the artefact is quantitatively what's seen in raw data.

4. **Empirical calibration on CFM meta-order data**:
   - Volume fractions $Q/V$ in 0.1–5%.
   - Predictor horizons $\Gamma^{-1}$ from 10 to 100 days.
   - Signals market-neutral, unit-variance-normalised.
   - Execution near 100% (no selection bias).

5. **Confirms square-root law**: $\delta \approx 0.6$, within the empirical 0.4–0.7 band reported across other studies.

6. **Finds impact decays to zero** (or a very small residual) after deconvolution. Contradicts the $2/3$-of-peak plateau prediction from the no-arbitrage argument of [Farmer et al. 2013] when applied without deconvolution. Reconciles with that argument's *spirit* by noting that residual permanent impact should be attributable to true information content ($\alpha \cdot H(\infty)$), not to the mechanical impact $I(\tau)$.

---

## Method summary

### Signal & prices
- Daily observation times $t$ when meta-orders start.
- Execution prices $p_x(t)$ and daily mids $p_d(t)$.
- **Strike slippage** $r_x(t) = (p_x(t) - p_d(t))/p_d(t)$.
- **Daily return** $r_d(t) = (p_d(t+1) - p_d(t))/p_d(t)$.

### Raw vs deconvolved impact
- **Raw impact** $I_\text{raw}(\tau)$: average price change $\tau$ days after meta-order completion, over all meta-orders. Contaminated by the continued trading of the same investor on correlated signals.
- **Deconvolved impact** $I(\tau)$: obtained by subtracting the contribution of all correlated subsequent meta-orders (using the investor's signal autocorrelation structure) from $I_\text{raw}$.

### Deconvolution via toy model
In the OU-signal toy model, the optimal position is:

$$\pi(t) = \phi_0 \int_{-\infty}^t e^{-\omega(t-t')} s(t') \, dt'$$

with a specific $\omega$ depending on the predictor horizon $\Gamma$ and impact coefficient $\gamma$. This gives an analytic formula for $I_\text{raw}$ as a convolution of the "true" $I$ with the position-process autocorrelation — which can be inverted.

### Functional form of $I(\tau)$
Consistent with a **power-law decay** $I(\tau) \sim \tau^{-\beta}$ at long times, or a stretched-exponential; the data can't distinguish between these cleanly but both imply $I(\infty) \approx 0$.

---

## Main results

- Peak impact matches square-root law with $\delta \approx 0.6$.
- **Deconvolved $I(\tau)$ decays to within statistical noise of zero** over 10 trading days.
- **Raw $I_\text{raw}(\tau)$** shows the widely reported 1/3-2/3 plateau artefact — this is now explained quantitatively by the toy model.
- Holds across US / Europe / Japan equity datasets (CFM trades across multiple markets); approximately universal.
- The residual long-horizon impact that remains after deconvolution is attributed to the genuine information content of informed trades (i.e., $\alpha$), not to a permanent mechanical footprint.

---

## Limitations

- **Proprietary data**: CFM-only; impossible to reproduce without access. But the methodology generalises.
- **Quasi-linear assumption**: meta-orders assumed to add linearly. Known to be an approximation — the paper acknowledges this explicitly. True short-time impact is strongly concave (square-root), not linear; the quasi-linear framework is a convenient long-time abstraction.
- **10-day horizon** is the empirical ceiling due to noise; can't rule out tiny residual impact beyond.
- **Single functional-form fit**: power-law vs stretched-exponential is not discriminated; both decay to zero.
- **Equities only**: futures, FX, crypto may show different decay patterns — untested here.
- **Informed vs uninformed decomposition** via $\alpha$ is model-structural; extracting $\alpha$ empirically depends on the predictor's known structure.

---

## Connections

- **Direct empirical support for the propagator framework** surveyed in [[papers/bouchaud-farmer-lillo-propagator]]. That paper advocated a transient-impact view; this paper is the definitive empirical test on proprietary meta-orders.
- **Contrasts with permanent-impact view** (fixed permanent impact per trade) — shows it can't survive proper deconvolution.
- **Relevant for [[concepts/optimal-execution]] practitioners**: if mechanical impact decays fully, the "cost-of-trading" calculation used in Almgren-Chriss / MPC frameworks should use the propagator form, not a fixed permanent component. Impacts practical execution cost estimation.
- **Complementary to [[papers/price-impact-order-book-events]]**: CKS give the linear OFI→mid-price coefficient at sub-minute horizons; this paper gives the shape of meta-order impact decay over days. Together: short-horizon contemporaneous impact plus long-horizon relaxation.
- **Motivates the impact-feedback kernel in [[papers/reality-gap-lob-simulation]]** — the power-law decay of that paper's simulator kernel is calibrated to be consistent with findings like these.
- **Connects to [[concepts/adverse-selection]]**: the residual $\alpha \cdot H(\infty)$ is the permanent component attributable to information content — the signature of informed trading in the Kyle / Glosten-Milgrom sense.
