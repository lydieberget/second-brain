---
title: "Cross-Impact"
type: concept
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/2112.13213.md
tags:
  - market-microstructure
  - price-impact
  - multi-asset
  - cross-sectional
related:
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/limit-order-book.md
  - methods/integrated-ofi.md
  - papers/cross-impact-ofi-equity-markets.md
  - entities/mihai-cucuringu.md
  - entities/rama-cont.md
confidence: high
---

# Cross-Impact

## Definition

**Cross-impact** is the influence of order flow on asset $j$ on the price of asset $i \neq j$. It is the multi-asset generalisation of [[concepts/price-impact|price impact]] — where standard price impact asks "how much does AAPL's order flow move AAPL's price?", cross-impact asks "how much does AAPL's order flow move GOOG's price?".

---

## Two regimes

| Regime | Claim | Evidence |
|---|---|---|
| **Contemporaneous cross-impact** | Weak or absent once within-asset multi-level information is aggregated. | [[papers/cross-impact-ofi-equity-markets|Cont-Cucuringu-Zhang 2023]] — integrated OFI leaves no room for cross-asset terms to add OOS $R^2$. |
| **Predictive (lagged) cross-impact** | Real at short horizons ($\leq$ few minutes), decays rapidly. | Same paper — lagged cross-asset OFIs add economic PnL in 1-min-ahead forecasting even with integrated OFI. |

This asymmetry is the central finding of the 2023 Cont-Cucuringu-Zhang paper and reconciles earlier apparent-conflict results: Benzaquen et al. (2017) and others argued cross-impact was meaningful; Capponi-Cont (2020) argued that a common factor subsumed it. The resolution: *contemporaneously* Capponi-Cont are right; *for forecasting* Benzaquen et al. are right.

---

## Why contemporaneous cross-impact vanishes under multi-level aggregation

Consider a multi-asset portfolio trader who splits their order across AAPL (best-level) and GOOG (deep level) simultaneously. A best-level-only OFI model for AAPL misses the GOOG leg and has to "borrow" that information via the cross-impact coefficient $\beta_{\text{AAPL, GOOG}}$. But a [[methods/integrated-ofi|multi-level integrated OFI]] for AAPL already captures the deep-level order directly, so the cross-impact term becomes redundant.

Mechanism in the paper's notation: information along the path $A_j \to A_i \to \text{ofi}^3_i \to r_i$ is absorbed by integrated OFI; only $A_j \to B_i$ (truly "other-stock-affects-this-stock") cross-routes survive, and those are rare.

---

## Why predictive cross-impact persists

Traders do not instantly react to order flow in other stocks. There is a "flow formation period" — a few minutes between when a trade pattern appears in one stock and when related stocks' prices adjust. Cohen-Frazzini (2008) and Hou (2007) independently documented this lead-lag as "industry information diffusion" or "attention constraints". Cross-asset lagged OFIs are therefore a *predictive* signal, even when contemporaneous cross-impact is absent.

Decay profile (from Cont-Cucuringu-Zhang):
- **1 min horizon**: cross-impact doubles PnL vs own-OFI only (0.43 vs 0.21 annualised).
- **3 min**: advantage narrows.
- **30 min**: no advantage remains.

---

## Data requirements

To estimate cross-impact on $N$ stocks with 1-min bars over $T$ minutes:
- At minimum $T \gg N$ to make OLS well-posed; in practice LASSO is needed even when $T > N$ because of high cross-asset OFI correlations.
- The cross-impact coefficient matrix exhibits a dominant "market mode" singular value (rank-1 structure) plus 6–8 "sector-mode" singular values.

---

## Sector structure

Empirically (Nasdaq-100, 2017–2019), cross-impact is concentrated in three "source" sectors:

1. **Communication Services** (highest out-degree).
2. **Consumer Discretionary**.
3. **Information Technology**.

Top individual stocks by out-degree centrality (forward-looking, 1-min): AMZN, NFLX, NVDA, GOOG, GOOGL. These tend to lead the rest of the market.

Tick-size dependency: stocks with larger tick-to-price ratio (small prices or large ticks) show stronger cross-impact — consistent with the [[papers/price-impact-generalized-ofi|tick-size regime effect]] in single-asset OFI work.

---

## Portfolio-level implications

Even when individual-asset cross-impact is zero, *portfolio returns* still depend on cross-impact via the angle between the portfolio weight vector $\vec{w}$ and the impact coefficient vector $\vec{\beta}$:

$$
r_p = \sum_i w_i r_i = \sum_i w_i \beta_{i,i} \text{ofi}_i + \sum_{i \neq j} w_i \beta_{i,j} \text{ofi}_j + \epsilon
$$

Only if $\vec{\beta}$ and $\vec{w}$ are parallel *and* all $\beta_{i,i}$ are equal does the cross-term vanish. For eigenportfolios and equal-weighted portfolios on Nasdaq-100, cross-impact adds $\sim\!3\%$ OOS $R^2$ over the own-OFI-only portfolio model.

---

## Open questions

- How do multi-level cross-impact matrices evolve over time? Current estimates are static within 30-minute windows.
- Can level-aware multi-level cross-impact (not collapsed via PCA) beat the integrated-OFI predictive cross-impact baseline at short horizons?
- Does cross-impact depend on client-ID-level order flow data (i.e. knowing the same trader is behind orders in multiple assets)? Authors speculate yes, but no public dataset to test.
- Cross-impact in futures, FX, crypto, and options markets — does the decay profile differ?
- Beyond linear models — does deep learning on cross-asset LOB vectors improve short-horizon forecasting?

---

## Connections

- [[concepts/order-flow-imbalance]] — cross-impact is the multi-asset extension of OFI-based impact.
- [[concepts/price-impact]] — cross-impact is one of the "determinants" when analysing a multi-asset portfolio.
- [[methods/integrated-ofi]] — the multi-level aggregation that neutralises contemporaneous cross-impact.
- [[papers/cross-impact-ofi-equity-markets]] — the defining empirical reference.
