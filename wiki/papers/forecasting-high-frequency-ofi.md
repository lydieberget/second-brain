---
title: "Forecasting High Frequency Order Flow Imbalance"
type: paper
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/2408.03594.md
tags:
  - order-flow-imbalance
  - hawkes-process
  - high-frequency
  - forecasting
  - market-microstructure
  - nse
  - superior-predictive-ability
related:
  - concepts/order-flow-imbalance.md
  - methods/hawkes-process.md
  - concepts/market-microstructure.md
  - papers/price-impact-order-book-events.md
  - papers/order-flow-filtration.md
  - papers/csi300-ou-levy-ofi.md
  - papers/price-impact-generalized-ofi.md
confidence: medium
---

# Forecasting High Frequency Order Flow Imbalance

**Authors**: Aditya Nittur Anantha, Shashi Jain
**Institution**: SigmaQuant Technologies Pvt. Ltd. / Indian Institute of Science
**Year**: 2024 (arXiv August 2024)
**arXiv**: [2408.03594](https://arxiv.org/abs/2408.03594)
**Categories**: q-fin.TR

---

## Plain-language abstract

OFI tells you about the current imbalance between buy and sell pressure in the order book — but can you predict OFI itself? This paper uses **Hawkes processes** to model the arrival rates of buy- and sell-classified trades as a mutually exciting point process, exploiting a feature of NSE tick data that allows **deterministic** trade classification (no Lee–Ready needed). It develops a method to forecast the near-term **distribution** of OFI (not just its mean) and a framework for comparing an arbitrary number of competing forecasting models via Hansen's test for Superior Predictive Ability (SPA). On NIFTY futures tick data, a Hawkes process with a **sum-of-exponentials kernel** outperforms all alternatives.

---

## Key contributions

1. **Deterministic OFI from order IDs**: every TRADE tick in NSE data carries two exchange order numbers — the passive resting order and the aggressive order that crossed the book. This allows classifying each trade as BUY or SELL without estimation (contrast with Lee–Ready or bulk classification).
2. **Trade-based OFI at tick frequency**: OFI is defined here as the normalised trade-count imbalance over a trailing window $h$, not Cont et al.'s event-based OFI. This is closer to Easley–O'Hara order-imbalance indicators.
3. **Hawkes with cross-excitation**: joint bid/ask intensity captures both *self-excitation* (BUY trades beget BUY trades, i.e., clustering) and *cross-excitation* (BUY trades trigger SELL activity) that VAR and PIN cannot represent.
4. **Distribution forecast via simulation**: Ogata's modified thinning algorithm simulates future event times from the fitted intensity; repeated simulations yield an empirical distribution $\tilde{F}_m$ of OFI over the forecast horizon.
5. **SPA-based model comparison**: builds on Diebold–Mariano (pairwise) and White's reality check; uses **Hansen (2005) SPA test** with centring/normalisation correction. Iteratively sets each candidate as benchmark to find the superior model family.

---

## Method summary

### Data
- **NIFTY futures** (expiring 27 September 2018), NSE India.
- One trading day: **19 September 2018**, tick-by-tick.
- Tick types filtered: `NEW_TICK`, `MODIFY_TICK`, `CANCEL_TICK`, `TRADE`.
- Minute-level aggregation → **375 OFI observations** per day.

### OFI definition used

$$\text{OFI}(T, h) = \frac{\Delta N^b_{T-h, T} - \Delta N^s_{T-h, T}}{\Delta N^b_{T-h, T} + \Delta N^s_{T-h, T}}$$

where $\Delta N^{b/s}$ is the count of BUY- / SELL-classified trades over window $h$ ending at $T$. Summary stats (minute bars, one day): count 315, mean $-0.076$, std $0.323$, range $[-0.779, 0.765]$. ACF/PACF show strong persistence — motivating both VAR and Hawkes models.

### Models compared

| Class | Model | Notes |
|---|---|---|
| Hawkes (parametric) | Exponential kernel | $\phi(t) = \alpha e^{-\beta t}$ |
| Hawkes (parametric) | **Sum-of-exponentials kernel** | $\phi(t) = \sum_j \alpha_j e^{-\beta_j t}$ — **winner** |
| Hawkes (parametric) | Power-law kernel | heavy-tailed memory |
| Hawkes (non-parametric) | EM / kernel smoothing | flexible form, higher variance |
| Linear baseline | VAR($p$) on $[\Delta N^b, \Delta N^s]$ | captures linear cross-dependence only |

### Estimation & simulation
- **Fitting window**: 1 hour rolling. **Forecast horizon**: 1 minute. Roll in 10-minute intervals.
- Parametric Hawkes: MLE by stochastic gradient descent on $-\ln L$, using Rubin (1972) / Ozaki (1977) form of the log-likelihood.
- Simulation: **Ogata's modified thinning algorithm** → arrival-time arrays → $\tilde{\text{OFI}}$ distribution.

### Loss & SPA test
Loss is the **negative log-likelihood** of the realised OFI under each model's empirical forecast distribution $\tilde{F}_m$, aggregated over 10-minute blocks. The vector $\{\Delta L\}$ of loss differences is fed into Hansen's SPA test with block bootstrap to control degenerate-distribution bias when the benchmark dominates.

---

## Main results

- **Sum-of-exponentials Hawkes wins** the SPA test against single-exponential, power-law, non-parametric, and VAR baselines.
- **Cross-excitation matters**: kernels restricted to self-excitation underperform, confirming that BUY and SELL flows are informationally coupled, not independent.
- **VAR is a weak baseline**: it captures lagged linear dependence but not the point-process clustering at sub-second scales. PIN (Easley–O'Hara) is similarly limited by its independence assumption.
- **Distribution forecasts are informative**: the empirical distribution of simulated OFI typically has enough spread to be useful for quoting and risk — a single-point forecast discards this information.

---

## Limitations

- **One day, one instrument, one exchange**: NIFTY futures on 2018-09-19 from NSE. Robustness across instruments and market regimes is not tested.
- **Stationarity assumption inside windows**: Hawkes processes fit on 1-hour windows assume local stationarity; the intraday regime shift is handled by rolling rather than by model structure.
- **Trade OFI ≠ event OFI**: this paper's OFI uses trade counts, whereas Cont et al. (2010) use all book events (limit adds, cancels, trades). They measure related but distinct quantities — keep this in mind when comparing $R^2$-type claims.
- **No P&L link**: OFI forecasts are evaluated by statistical loss (NLL), not by integration into a market-making or execution strategy.

---

## Connections

- Builds directly on [[papers/price-impact-order-book-events]] (Cont et al.'s OFI definition).
- The Hawkes process methodology: [[methods/hawkes-process]].
- Core concept: [[concepts/order-flow-imbalance]].
- Companion paper on OFI filtration by the same authors: [[papers/order-flow-filtration]].
