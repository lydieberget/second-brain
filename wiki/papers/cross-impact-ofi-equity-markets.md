---
title: "Cross-Impact of Order Flow Imbalance in Equity Markets"
type: paper
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/2112.13213.md
tags:
  - order-flow-imbalance
  - cross-impact
  - multi-level-lob
  - multi-asset
  - lasso
  - pca
  - signal-design
related:
  - concepts/order-flow-imbalance.md
  - concepts/cross-impact.md
  - concepts/price-impact.md
  - concepts/limit-order-book.md
  - methods/integrated-ofi.md
  - papers/price-impact-order-book-events.md
  - papers/mlofi-xu-gould-howison.md
  - papers/price-impact-generalized-ofi.md
  - entities/rama-cont.md
  - entities/mihai-cucuringu.md
  - concepts/universal-price-formation.md
  - papers/lehalle-neuman-signals-optimal-trading.md
confidence: high
---

# Cross-Impact of Order Flow Imbalance in Equity Markets

**Authors**: [[entities/rama-cont|Rama Cont]], [[entities/mihai-cucuringu|Mihai Cucuringu]], Chao Zhang
**Institution**: University of Oxford (Mathematical Institute, Department of Statistics, Oxford-Man Institute), The Alan Turing Institute
**Year**: 2021 (first draft); published *Quantitative Finance* 23(10), 2023
**arXiv**: [2112.13213](https://arxiv.org/abs/2112.13213)
**Categories**: q-fin.TR, q-fin.CP, q-fin.ST

---

## Abstract (plain-language)

When a large trader moves AAPL's order book, does it also shift GOOG's price? This paper tests that question — *cross-impact* — on Nasdaq-100 stocks and arrives at a subtle answer. Using top-10 LOB levels instead of just the best-level, they build a single aggregate signal (**integrated OFI**) by taking the first principal component of the per-level OFI vector. That signal alone explains **87%** of contemporaneous minute-return variance, up from 71% for best-level OFI. Crucially, once you use integrated OFI, *contemporaneous* cross-impact from other stocks adds nothing — the multi-level aggregation has already absorbed whatever information cross-asset OFIs carried. But *lagged* cross-asset OFI **does** help forecast the next minute's return and translates into higher PnL in a forecast-implied trading strategy. Cross-impact is a short-horizon phenomenon that decays within minutes.

---

## Key contributions

1. **Integrated OFI** — First systematic procedure for aggregating top-$M$ multi-level OFIs into a single signal. PCA on the 10-level OFI vector captures >89% of variance in the first component; re-normalising by $\ell_1$ norm gives weights that sum to 1. See [[methods/integrated-ofi]].
2. **Contemporaneous-impact result** — Best-level single-asset OFI model (PI¹): adjusted $R^2 = 71\%$ IS, $65\%$ OOS. Integrated-OFI single-asset model (PIᴵ): $R^2 = 87\%$ IS, $84\%$ OOS. Adding cross-asset OFIs (LASSO-selected) to the best-level model buys $\sim\!1.4\%$ OOS; adding them to the integrated-OFI model buys essentially nothing ($-0.2\%$). Conclusion: **integrated OFI subsumes contemporaneous cross-asset information**.
3. **Predictive cross-impact** — Lagged cross-asset OFIs (up to 30 min of lags) improve 1-minute-ahead return forecasts in both best-level and integrated variants. At the 1% confidence level, the cross-impact predictive model (FCI) beats the own-OFI predictive model (FPI) for *all* tested stocks.
4. **Economic gains** — In a Chinco-et-al.-style forecast-implied trading strategy (trade only when $|\hat{r}| > $ spread, weight by signal/volatility), FCI doubles the annualised PnL versus FPI (0.43 vs. 0.21 for best-level; 0.39 vs. 0.23 for integrated). Predictability decays rapidly with horizon — by 30 min cross-impact provides no advantage.
5. **Portfolio-level cross-impact is real** — Even when individual-stock cross-impact is absent (integrated OFI case), the portfolio-level projection depends on the angle between $\vec{\beta}$ and the portfolio weight vector $\vec{w}$. For eigenportfolios and equal-weighted portfolios, cross-impact adds $\sim\!3\%$ OOS $R^2$.
6. **Mechanism** — Proposes that integrated OFI captures "multi-asset portfolio trades" (a trader simultaneously placing correlated orders across assets) as paths like $A_j \to A_i \to \text{ofi}^3_i \to r_i$, whereas best-level OFI misses them and has to borrow information via the cross-impact terms.

---

## Method summary

### Integrated OFI construction

For stock $i$, interval $(t-h, t]$:

$$
\text{ofi}^m_{i,t,h} \;=\; \frac{1}{Q^{M,h}_{i,t}} \sum_{n=N(t-h)+1}^{N(t)} \text{OF}^{m,b}_{i,n} - \text{OF}^{m,a}_{i,n}
$$

where $\text{OF}^{m,b}_{i,n}$ is the signed event contribution at bid level $m$ (positive for arrivals / upticks, negative for cancels / downticks); $Q^{M,h}_{i,t}$ is the average book depth across the top $M$ levels, used to scale for intraday depth patterns.

Stacking across $m = 1, \ldots, 10$ gives the multi-level OFI vector $\mathbf{of}^{(h)}_{i,t}$. The integrated OFI is the first principal component normalised so its weights sum to 1:

$$
\text{ofi}^I_{i,t,h} \;=\; \langle \tilde{\mathbf{w}}_1, \mathbf{of}^{(h)}_{i,t}\rangle, \quad \tilde{\mathbf{w}}_1 = \frac{\mathbf{w}_1}{\|\mathbf{w}_1\|_1}
$$

where $\mathbf{w}_1$ is the first principal vector from historical data. Full algorithm on [[methods/integrated-ofi]].

### Four regression models

Let $r^{(h)}_{i,t}$ be the $h$-minute log return of stock $i$. The paper defines four contemporaneous regressions:

| Model | Equation | Fit |
|---|---|---|
| **PI¹** | $r = \alpha + \beta \cdot \text{ofi}^1 + \epsilon$ | OLS |
| **PIᴵ** | $r = \alpha + \beta \cdot \text{ofi}^I + \epsilon$ | OLS |
| **CI¹** | $r_i = \alpha + \beta_{i,i} \cdot \text{ofi}^1_i + \sum_{j \ne i} \beta_{i,j} \cdot \text{ofi}^1_j + \epsilon$ | LASSO |
| **CIᴵ** | $r_i = \alpha + \beta_{i,i} \cdot \text{ofi}^I_i + \sum_{j \ne i} \beta_{i,j} \cdot \text{ofi}^I_j + \epsilon$ | LASSO |

LASSO is essential — with ~100 stocks and 30-minute estimation windows at 1-minute resolution, OLS is ill-posed and multicollinearity (cross-asset OFI correlations up to 0.6) makes unpenalised estimation hopeless.

Forward-looking variants (**FPI¹, FPIᴵ, FCI¹, FCIᴵ**) use lagged OFIs in $L = \{1, 2, 3, 5, 10, 20, 30\}$ to predict $r^{(f)}_{i,t+f}$ for forecasting horizons $f \in \{1, 2, 3, 5, 10, 20, 30\}$ minutes.

### Data

- **Source**: Nasdaq ITCH via LOBSTER.
- **Universe**: top 100 S&P 500 constituents by market cap as of 2019-12-31.
- **Period**: 2017-01-01 to 2019-12-31.
- **Frequency**: minute-level OFIs + returns.
- **Windowing**: 30-minute rolling estimation windows, excluding first and last 30 minutes of the trading day.

---

## Main results

### Contemporaneous ($R^2$, OOS, %)

| | Best-level OFIs | Integrated OFIs |
|---|---|---|
| PI¹ / PIᴵ | 64.64 (21.82) | 83.83 (16.90) |
| CI¹ / CIᴵ | 66.03 (19.51) | 83.62 (14.53) |

Integrated OFI gives a +19-point OOS jump over best-level OFI. Adding cross-impact to integrated OFI is *worse* OOS (overfitting signal).

### Tick-size dependency (OOS $R^2$ by tick-to-price quartile)

Larger tick-to-price ratio → cross-asset OFIs explain more. For lowest-quartile (small tick) stocks, PIᴵ = 68%, CIᴵ = 72%. For highest-quartile (large tick), PIᴵ = 90%, CIᴵ = 91%. Cross-impact mattering more for discrete-price stocks is consistent with tick-size regime literature.

### Predictive ($R^2$, 1-min-ahead, OOS, %)

| | Best-level | Integrated | Returns |
|---|---|---|---|
| FPI / FPIᴵ / AR | −0.37 | −0.36 | −0.36 |
| FCI / FCIᴵ / CAR | −0.10 | −0.10 | −0.10 |

All models have *negative* OOS $R^2$ (signal-to-noise is low at 1 min), but cross-impact variants consistently less negative. Per Kelly et al. (2022), negative $R^2$ does not rule out positive economic performance — confirmed below.

### Economic performance (annualised PnL)

| | Best-level | Integrated | Returns |
|---|---|---|---|
| FPI / FPIᴵ / AR | 0.21 | 0.23 | 0.23 |
| FCI / FCIᴵ / CAR | 0.43 | 0.39 | 0.40 |

Cross-impact roughly doubles the annualised PnL of the forecast-implied strategy. Ignores transaction costs — authors note this is not the focus.

### Network structure

Coefficient matrices exhibit low-rank structure dominated by a "market mode" (top singular value). Out-degree centrality is concentrated in Communication Services, Consumer Discretionary, and Information Technology — these sectors lead the others. Highest-centrality individual stocks: AMZN, NFLX, NVDA, GOOG/GOOGL.

---

## Limitations

- **Horizon is minute-level.** The mesoscopic analysis deliberately ignores sub-minute microstructure effects. Cross-impact findings might not transfer to sub-second trading.
- **Transaction costs ignored** in the PnL comparison.
- **Integrated OFI drops level information.** A limitation acknowledged in Section 4.4 — depth-specific strategic order placement is collapsed into a single number. A multi-level cross-impact model with explicit level awareness is left as future work.
- **US equities only.** No evidence it generalises to futures, FX, crypto, or markets with different tick-size regimes at the universe level.
- **Static factor structure assumption.** LASSO cross-impact coefficients are re-estimated every 30 minutes; the paper does not model how the cross-impact network itself evolves.
- **In-sample PC fitted globally.** Principal vector $\mathbf{w}_1$ is computed from historical data across all stocks, not stock-specific. This is a feature for stability, but may lose stock-level structure.

---

## Connections to other wiki pages

- **Extends**: [[papers/price-impact-order-book-events]] (single-asset best-level OFI) and [[papers/mlofi-xu-gould-howison]] (multi-level OFI as a vector) — this paper unifies them with an aggregation step.
- **Relates to**: [[papers/price-impact-generalized-ofi]] — both address the multi-level-OFI question, but with different aggregations (log-GOFI vs. PCA-normalised integrated OFI).
- **Uses**: [[methods/integrated-ofi]] (new, introduced here) as primary feature, LASSO for sparse cross-impact selection.
- **Companion result**: Kolm, Turiel, Westray (Mathematical Finance, 2023) — "Deep Order Flow Imbalance: Extracting Alpha at Multiple Horizons" — shows DNNs on multi-level OFIs beat LOB-direct inputs. This paper is the interpretable-linear-model counterpart.
- **Contrasts with**: Benzaquen, Mastromatteo, Eisler, Bouchaud (2017) — which argued for meaningful cross-impact — by showing that cross-impact disappears once within-asset multi-level information is integrated.
- **Concept page**: [[concepts/cross-impact]] (new).

### Direct signal-design takeaways

For anyone building an LOB-snapshot or L3 signal:

1. **Use multiple levels.** Level-1 OFI leaves $\sim\!20$ points of $R^2$ on the table vs. integrated OFI.
2. **PCA-aggregate across levels.** The first PC is stable across stocks and captures most of the signal; re-normalising by $\ell_1$ keeps weights interpretable.
3. **Don't bother with contemporaneous cross-asset features** if you already aggregate levels properly — it's overfitting.
4. **Do use cross-asset OFI for short-horizon forecasting** ($\leq 3$ min). LASSO keeps it tractable.
5. **Scale OFIs by intraday depth** ($Q^{M,h}_{i,t}$), not just by the previous day's average.
