---
title: "Multi-Level Order-Flow Imbalance in a Limit Order Book"
type: paper
created: 2026-04-17
updated: 2026-04-17
sources:
  - raw/papers/1907.06230.md
tags:
  - order-flow-imbalance
  - multi-level-ofi
  - limit-order-book
  - nasdaq
  - ridge-regression
  - tick-size
  - signal-design
related:
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - concepts/price-impact.md
  - papers/price-impact-order-book-events.md
  - papers/deep-lob-forecasting.md
  - papers/explainable-crypto-microstructure.md
  - methods/integrated-ofi.md
  - papers/cross-impact-ofi-equity-markets.md
  - papers/gould-bonart-queue-imbalance.md
confidence: high
---

# Multi-Level Order-Flow Imbalance in a Limit Order Book

**Authors**: Ke Xu, Martin D. Gould, Sam D. Howison
**Institution**: Mathematical Institute, University of Oxford
**Year**: 2019 (arXiv July 2019)
**arXiv**: [1907.06230](https://arxiv.org/abs/1907.06230)
**Categories**: q-fin.TR, q-fin.GN, q-fin.ST

---

## Plain-language abstract

Cont–Kukanov–Stoikov's OFI ([[papers/price-impact-order-book-events]]) only looks at the best bid/ask — the first level of the book. In Appendix B3 of that paper the authors briefly extended to deeper levels and concluded the extra information added little. This paper revisits that claim with cleaner data and better econometrics. It defines **MLOFI as an $M$-dimensional vector** (one OFI component per price level for the first $M$ levels on each side), fits a linear relationship between MLOFI and contemporaneous mid-price changes on 6 liquid Nasdaq stocks (2016), and finds that **deeper levels do carry significant information** — CKS's original conclusion was a consequence of OLS instability due to cross-level correlation. Switching to **Ridge regression** produces stable fits in which every level's coefficient is statistically significant, and out-of-sample RMSE improves by **65–75% for large-tick stocks** and **15–30% for small-tick stocks** when going from 1-level to multi-level.

---

## Key contributions

1. **MLOFI — formal multi-level OFI vector**. For $m = 1, \ldots, M$ price levels on each side, define signed contributions $e_n^m$ tracking limit-order arrivals, cancellations, and trades at each level. Sum over a time interval:

   $$\text{MLOFI}_k^m = \sum_{n: \tau_n \in (t_{k-1}, t_k]} e_n^m$$

   giving a vector $\text{MLOFI}_k \in \mathbb{R}^M$.

2. **Revisit of CKS's level-depth conclusion**. CKS (2014, Appendix B3) used multivariate OLS and found little improvement from adding levels. Xu–Gould–Howison show this was because OLS is unstable: the sample correlations between the per-level net order flows are strong, so individual coefficients are poorly identified in OLS even when the collective information content is high.

3. **Ridge regression makes deep-level information legible**. With a small L2 penalty, all $M$ coefficients become statistically significant and the fit stabilises. Out-of-sample goodness-of-fit monotonically improves with each additional level up to the tested depth.

4. **Tick-size dependence**. The benefit of multi-level information is **much larger for large-tick stocks** (65–75% RMSE improvement) than small-tick stocks (15–30%). Large-tick books concentrate liquidity at a few discrete levels whose queue dynamics couple tightly with mid-price; small-tick books have more dispersion and less per-level signal.

5. **Clean high-frequency dataset**: full LOB event stream (not TAQ-aggregated estimates as in CKS) for 6 liquid Nasdaq names over 2016. Enables exact MLOFI calculation without the CKS-style volume-change approximation.

---

## Method summary

### Notation recap
- $b^m(\tau_n), a^m(\tau_n)$ — level-$m$ bid / ask price after event $n$.
- $r^m(\tau_n), q^m(\tau_n)$ — total size at level-$m$ bid / ask after event $n$.
- Per-level signed contribution $e_n^m$ depends on whether the price and/or size at level $m$ increased or decreased — the natural multi-level extension of CKS's signed-event definition.

### Regression spec

$$\Delta P(t_{k-1}, t_k) = \alpha + \sum_{m=1}^{M} \beta_m \cdot \text{MLOFI}_k^m + \varepsilon_k$$

- $M = 1$ case reproduces CKS exactly.
- For $M > 1$, fit by **Ridge regression** (L2 penalty) rather than OLS.
- Split into in-sample (model fitting + λ selection) and out-of-sample windows.

### Data
- **6 liquid Nasdaq stocks** (the paper tests a cross-section spanning tick-size regimes).
- **Full calendar year 2016**.
- Full LOB event data — not TAQ volume approximations.
- Regression on event-time intervals (varying length), matched mid-price changes.

### Evaluation
- In-sample vs out-of-sample $R^2$ and RMSE.
- OLS vs Ridge side-by-side.
- Goodness-of-fit as a function of $M$ (levels included).

---

## Main results

- **OLS is unstable** for multi-level MLOFI: individual $\beta_m$ coefficients flip sign, become insignificant, or show OOS degradation vs IS — symptoms of multicollinearity.
- **Ridge regression stabilises** all coefficients; every level up to the tested depth is significant.
- **OOS RMSE decreases monotonically** in $M$ for all 6 stocks — adding more levels helps, not hurts.
- **Magnitude of improvement**:
  - Large-tick stocks: **65–75%** OOS RMSE reduction vs M=1.
  - Small-tick stocks: **15–30%** OOS RMSE reduction vs M=1.
- **CKS's original "best quotes are enough" conclusion is overturned** for large-tick stocks — a methodological artefact of OLS + multicollinearity, not a property of the data.

---

## Limitations

- **6 stocks, one year**. Robustness across markets, years, and regimes not tested in this paper.
- **Linear model only** — non-linear interactions (e.g. sign-dependent impact) not explored.
- **Ridge λ tuning** is done in-sample; a small OOS drift remains.
- **Latency and execution costs ignored** — this is an explanatory-fit paper, not a backtest. No claim that exploiting MLOFI yields P&L after costs.
- **No regime decomposition** — the paper reports period-average effects; intraday and high-volatility regimes could show different per-level informativeness.

---

## Connections

- **Direct extension of [[papers/price-impact-order-book-events]]** — this paper *overturns* one of CKS's conclusions (the one in their Appendix B3). The main OFI result (linear, robust, high R²) stands; only the "depth doesn't help" claim is revised.
- **Tick-size regime theme** — large-tick stocks benefit most from multi-level information. This is a **third independent confirmation** of the tick-size-matters-for-LOB-signals thread, alongside [[papers/deep-lob-forecasting]] (Briola et al. 2024: DL forecastability by tick regime) and [[papers/explainable-crypto-microstructure]] (Bieganowski–Ślepaczuk 2026: OBI SHAP magnitude by relative tick). Add to [[connections/deep-learning-meets-market-microstructure]].
- **Ridge-regression motivation** is a methodological contribution: when stacking correlated LOB features, always check OLS stability vs regularised alternatives.
- **Complements [[papers/price-impact-generalized-ofi]]** (Su et al. 2021, GOFI): GOFI extends OFI by handling multi-tick moves on Chinese data; MLOFI extends by handling multi-level depth on US data. Orthogonal axes of generalisation.
- **Ingredient for Deep OFI**: Kolm–Turiel–Westray (2021, *Mathematical Finance*, not on arXiv) use a DOFI vector conceptually similar to MLOFI as input to deep-learning models. If that paper ever gets ingested via Semantic Scholar, it will link directly here.
