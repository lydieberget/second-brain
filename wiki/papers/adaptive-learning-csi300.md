---
title: "Forecasting High-Frequency Financial Time Series: An Adaptive Learning Approach with the Order Book Data"
type: paper
created: 2026-04-17
updated: 2026-04-17
sources:
  - raw/papers/2103.00264.md
tags:
  - order-flow-imbalance
  - order-book-imbalance
  - adaptive-learning
  - chinese-markets
  - csi300
  - time-series
  - non-stationarity
  - signal-design
related:
  - concepts/order-flow-imbalance.md
  - concepts/market-microstructure.md
  - papers/price-impact-order-book-events.md
  - papers/price-impact-generalized-ofi.md
  - papers/csi300-ou-levy-ofi.md
confidence: medium
---

# Forecasting High-Frequency Financial Time Series — An Adaptive Learning Approach with the Order Book Data

**Authors**: Parley Ruogu Yang
**Institution**: Faculty of Mathematics, University of Cambridge / Department of Statistics, University of Oxford
**Year**: 2021 (arXiv February 2021; written September 2020)
**arXiv**: [2103.00264](https://arxiv.org/abs/2103.00264)
**Categories**: q-fin.ST, econ.EM, q-fin.TR, stat.AP

---

## Plain-language abstract

The order book's OBI and OFI are useful features for HF forecasting — but they are also **non-stationary**, which breaks fixed ARIMA-style models. This paper proposes an **adaptive learning** wrapper that lets window size and model order adapt over time. On CSI 300 Index Futures data (105 trading days, 2017–2018), adaptive models match or beat the best-fixed alternatives and are materially more resilient in volatile regimes.

---

## Key contributions

1. **Two-feature signal set**: defines **OBI** (pure queue-size imbalance, Avellaneda–Reed–Stoikov style) and **OFI** (Cont–Kukanov–Stoikov signed event contributions) on CSI 300 Futures.
2. **P-score transformation**: normal-CDF wrap of $(x - \mu)/\sigma$ restricts values to $[0, 1]$; trades variance for stationarity — useful preprocessing for time-series models that need bounded inputs.
3. **Rolling ADF testing** of stationarity. Documents that at small windows ($w=12$ observations), stationarity is highly intermittent; at larger windows ($w=48, 96$), mostly stationary but with occasional shifts requiring higher-order differencing.
4. **Adaptive learning model group** that picks window size and model order per decision point rather than fixing them globally. Beats best-fixed ARIMA/multivariate baselines on forecast accuracy and stability under non-stationarity.
5. **Rolling-window hypothesis-testing application**: shows how the adaptive model produces valid testing distributions for parameter significance across the trading session.

---

## Data and features

### Dataset
- **CSI 300 Index Futures**, intraday.
- **10 November 2017 → 17 April 2018**, 105 trading days (provided by CIFCO Guangzhou).
- Two sessions per day (09:30–11:30, 13:00–15:00).
- Raw entries: 1–2 per second; includes best bid / ask prices and quantities plus last trade.

### Bracketing & target
- Each 2-hour session divided into **24 brackets of 5 minutes**.
- Per-bracket target: **Volume-Weighted Mean (VWM)** price $= \sum v_s p_s / \sum v_s$.
- First 6 observations (30 min) of each session excluded to let the book stabilise.
- Day-gap and lunch-gap observations excluded via dummies.

### Features

$$\text{OIB}_s = \frac{BQ_s - AQ_s}{BQ_s + AQ_s}, \qquad \text{OFI}_s = e_s^{\text{CKS}}$$

where $e_s^{\text{CKS}}$ is the Cont–Kukanov–Stoikov signed event contribution depending on whether prices changed, whether queues grew, and on which side. See [[concepts/order-flow-imbalance]] for the full event decomposition.

Per bracket, summary statistics: mean and **p-score** (normal-CDF wrap) of the per-entry feature sequence.

$$\text{pscore}(x_{[t-1, t]}) = \Phi\!\left(\frac{\text{mean}(x) - \mu_\text{global}}{\text{sd}_\text{global}}\right)$$

---

## Method

### Fixed-model baselines
- Univariate ARIMA$(p, d, q)$ on VWM.
- Multivariate ARIMAX including OBI/OFI lagged features.
- Model order / window size chosen up-front from exploratory ADF + AIC.

### Adaptive learning (the proposal)

At each forecast step $t$:
1. Candidate set of windows $\mathcal{W} = \{12, 24, 48, 96\}$ observations (1, 2, 4, 8 hours).
2. Candidate model orders $\mathcal{M}$ (ARIMA(p,d,q) over a grid).
3. **Evaluate** each candidate over a recent validation slice; pick the combination minimising MAE / MSE.
4. **Re-fit** and forecast one step ahead.
5. Advance $t$ by one bracket and repeat.

Penalty criteria (AIC, MDL) applied optionally to avoid overfitting to the validation window.

### Hypothesis testing application
Rolling-window approach: test $H_0$: coefficient $= 0$ on each fit; collect a time series of $p$-values; interpret as a significance regime indicator.

---

## Main results

- **Adaptive models outperform best-fixed** on forecast accuracy (MAE, MSE) averaged over the test period.
- **Stability under non-stationarity**: during volatile sessions, fixed models degrade more sharply than adaptive ones.
- **Best window size varies** across the session — fixed choices (even optimal in-sample ones) are suboptimal out-of-sample.
- **Second-order differencing occasionally required**: rolling ADF at $w=12$ frequently rejects stationarity; adaptive models automatically step up the differencing order.

---

## Limitations

- **Single instrument, short window**: CSI 300 Futures, 105 trading days. Robustness across instruments and years untested.
- **Feature set is intentionally simple**: OIB + OFI only. Multi-level OFI, microprice, VWAP deviations not included — complementary with [[papers/csi300-ou-levy-ofi]] which adds Lambda and AvgEn.
- **5-minute brackets** are coarse for HFT; the "high-frequency" framing is at minute-to-hour horizons, not sub-second.
- **ARIMA backbone** is limited; deep-learning comparisons are mentioned but deferred as future work (cited: Sirignano & Cont 2018).
- **P-score preprocessing trades variance for stationarity** — useful for stability, but discards magnitude information that could carry short-horizon predictive content.

---

## Connections

- **Chinese-markets sibling papers** in the wiki: [[papers/price-impact-generalized-ofi]] (Su et al. 2021 on CSI 500, GOFI) and [[papers/csi300-ou-levy-ofi]] (Hu & Zhang 2025 on CSI 300 with OU-Lévy). Together they span CSI 300/500 with three complementary modelling approaches: regression R² (GOFI), adaptive ARIMA (this paper), and stochastic differential equations (Hu & Zhang).
- **OIB vs OFI distinction**: this paper is one of the cleanest in the wiki at separating the two. OIB is pure-queue imbalance (quantities only); OFI is event-based signed contribution. Updated in [[concepts/order-flow-imbalance]].
- **Non-stationarity is the key motivating pain point** — same structural issue addressed by different means in [[papers/reality-gap-lob-simulation]] (rolling-calibrated simulator) and the rolling-window z-score in [[papers/deep-lob-forecasting]].
- **P-score preprocessing** is a candidate normalisation trick worth reusing for other signal pages; connects philosophically to the log-transformation in [[papers/price-impact-generalized-ofi]] (both aim to stabilise heavy-tailed queue-size distributions).
