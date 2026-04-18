---
title: "Explainable Patterns in Cryptocurrency Microstructure"
type: paper
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/2602.00776.md
tags:
  - cryptocurrency
  - market-microstructure
  - limit-order-book
  - machine-learning
  - shap
  - order-flow-imbalance
  - adverse-selection
  - catboost
  - microprice
related:
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - concepts/adverse-selection.md
  - concepts/market-microstructure.md
  - methods/shap-values.md
  - methods/microprice.md
  - papers/price-impact-order-book-events.md
  - papers/deep-lob-forecasting.md
  - connections/deep-learning-meets-market-microstructure.md
confidence: medium
---

# Explainable Patterns in Cryptocurrency Microstructure

**Authors**: Bartosz Bieganowski, Robert Ślepaczuk
**Institution**: University of Warsaw, Faculty of Economic Sciences — Department of Quantitative Finance and Machine Learning
**Year**: 2026 (February 2026)
**arXiv**: [2602.00776](https://arxiv.org/abs/2602.00776)
**Categories**: q-fin.TR, q-fin.CP, q-fin.ST

---

## Plain-language abstract

Do crypto markets share a **universal microstructure**? This paper trains CatBoost gradient-boosted trees with a direction-aware GMADL objective on Binance Futures perpetual contracts for five assets spanning **an order of magnitude** in market capitalisation — BTC, LTC, ETC, ENJ, ROSE (market-cap ranks 1 / 20 / 40 / 60 / 100 at the start of 2022). **SHAP** analysis shows that both feature importance *rankings* and partial-effect *shapes* are strikingly similar across all five assets despite very different liquidity profiles. A major **flash crash** provides a natural experiment: the taker strategy collapses while the maker strategy survives — empirical validation of classical adverse-selection theory. Authors argue for a portable universal feature library for crypto short-horizon returns.

---

## Key contributions

1. **Cross-asset SHAP universality** — feature importance rankings are highly Spearman-correlated across five assets; dependence-curve *shapes* coincide after relative-price / relative-flow normalisation.
2. **Direction-aware GMADL objective** — Generalized Mean Absolute Directional Loss, rewarding sign-correct forecasts scaled by return magnitude. Models are trained with squared-error loss but **selected by GMADL** on inner-fold performance.
3. **Tick-size modulation**: cross-asset, the high-quantile SHAP magnitude of OBI rises with effective tick size. Validated with a clever natural experiment — W/USDT spot (tick $10^{-4}$) vs W/USDT perp (tick $10^{-5}$) — spot OBI correlates at $c = 0.94$ with the futures mid's position within the spot spread. **OBI in large-tick markets is a visible proxy for the latent continuous price**, linking directly to Stoikov's microprice.
4. **Paired taker / maker backtest** — top-of-book taker uses conservative unfavourable-side inventory marking; a fixed-depth maker complement allows the flash-crash adverse-selection contrast.
5. **Flash-crash stress test** — taker and maker performance diverge sharply during a major crash in a way that matches Glosten–Milgrom predictions about uninformed liquidity providers being picked off.

---

## Method summary

### Data
- **Binance Futures perpetual contracts**: BTC, LTC, ETC, ENJ, ROSE.
- **1-second frequency**, 1 January 2022 → 12 October 2025.
- Top-of-book quotes synchronised with trades.
- **Target**: 3-second log return of mid price, $r_{t \to t+3s}$.

### Feature families
- **Top-of-book metrics** — mid, spread, best-bid/ask sizes.
- **Order / trade imbalances** — net signed flows.
- **VWAP-to-mid deviations** — for buy- and sell-side trades separately.

Features kept in original scale (tree models are scale-invariant). Relative measures (spread/mid, VWAP/mid) preferred for cross-asset comparability.

### Model & training
- **CatBoost** (ordered boosting, TreeExplainer-compatible).
- **Optuna TPE** Bayesian hyperparameter optimisation (depth, iterations, lr, ℓ₂ leaf reg, subsampling temperature, discretisation granularity).
- **Nested time-series CV**: inner CV inside each training window for tuning; outer walk-forward folds with a **purge window** between train and test to prevent leakage from slow-moving features.
- Models trained with squared-error loss; the GMADL-scored checkpoint is retained for explanation + backtest (squared-error variant kept as robustness check).

### Backtests
- **Taker**: signals derived by thresholding predictions, $\hat R_t > \theta$. Buy at best ask, sell at best bid. Inventory **marked to the unfavourable side** of the book — systematically pessimistic accounting. Position changes only on signal flips. Latency not modelled → upper bound in fastest regime.
- **Maker**: fixed-depth limit-order strategy for the flash-crash contrast.

---

## Main results

### Cross-asset stability
- SHAP feature-importance rankings are highly Spearman-correlated across all five assets.
- Same three families dominate mean-absolute SHAP everywhere: **OFI, bid-ask spread, VWAP-to-mid deviations**.
- Dependence-curve shapes agree:
  - **OFI** — largely monotone with **concavity at the extremes** (diminishing marginal effect as pressure accumulates).
  - **Spread** — wider spread → attenuated predictive effect (adverse selection rises, confidence falls).
  - **VWAP-to-mid** — asymmetric; coherent with transient pressure followed by microstructure reversion as depth replenishes.

### Tick-size effect
Across assets, high-quantile imbalance SHAP rises with effective relative tick size. The W/USDT spot-vs-perp natural experiment (finer tick in perp) gives a correlation of **0.94** between spot OBI and the perp-implied continuous price location within the spot spread — i.e. in large-tick markets OBI is essentially a readable microprice. *Connects directly to the small/medium/large-tick taxonomy in [[papers/deep-lob-forecasting]].*

### Taker backtest (gross, fixed notional)

| Asset | ARC | ASD | IR* | MDD | Buy-and-hold ARC |
|---|---|---|---|---|---|
| BTC | 0.13 | 0.53 | 0.25 | 0.29 | 0.83 |
| LTC | 0.07 | 0.99 | 0.07 | 0.64 | 0.53 |
| ETC | 5.78 | 0.64 | 8.97 | 0.24 | −0.10 |
| ENJ | 4.06 | 0.62 | 6.58 | 0.26 | −0.67 |
| ROSE | 7.00 | 1.33 | 5.28 | 0.43 | −0.71 |

Signal quality is strongest on smaller-cap assets where the universal feature set is less priced in — BTC gets similar IR to buy-and-hold, while ROSE/ETC/ENJ dominate their own buy-and-hold on a risk-adjusted basis.

### Flash-crash case study
During a major flash crash event, the taker strategy's equity collapses; the maker strategy remains resilient. The divergence is directionally correct under adverse-selection theory (Glosten–Milgrom): in a one-way market, takers are hit at increasingly unfavourable prices while makers who stand aside are protected — but the paper's fixed-depth maker gets picked off at the onset, matching the picking-off predictions too.

---

## Limitations

- **Binance Futures only** — one venue, perpetual contracts; spot, traditional exchanges, and fragmented crypto venues untested.
- **1-second frequency** — tick-level and minute-level behaviour may differ; execution latency not modelled (results = upper bound under zero latency).
- **Five assets** — strong universality signal but a small sample; "long tail" below rank 100 not covered.
- **No walk-forward online deployment** — all backtests are offline replays of historical data, no live trading validation.
- **Flash-crash analysis is a case study**, not a systematic stress test across multiple events or regimes.

---

## Connections

- Uses [[concepts/order-flow-imbalance]] as the central signal, extending [[papers/price-impact-order-book-events]].
- Flash crash validates [[concepts/adverse-selection]] theory.
- Connects to DL-based LOB forecasting: [[papers/deep-lob-forecasting]].
- Explainability method: [[methods/shap-values]].
- Broader cross-domain insight: [[connections/deep-learning-meets-market-microstructure]].
