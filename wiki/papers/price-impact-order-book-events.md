---
title: "The Price Impact of Order Book Events"
type: paper
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/1011.6402.md
tags:
  - order-flow-imbalance
  - price-impact
  - market-microstructure
  - limit-order-book
  - high-frequency
related:
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/limit-order-book.md
  - concepts/market-microstructure.md
  - entities/rama-cont.md
  - entities/sasha-stoikov.md
  - papers/price-impact-generalized-ofi.md
  - papers/forecasting-high-frequency-ofi.md
  - concepts/optimal-execution.md
  - concepts/universal-price-formation.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/brokmann-slow-decay-impact.md
  - papers/cross-impact-ofi-equity-markets.md
  - papers/csi300-ou-levy-ofi.md
  - papers/eisler-bouchaud-kockelkoren-order-book-events.md
  - papers/explainable-crypto-microstructure.md
  - papers/lipton-quote-imbalance.md
  - papers/mlofi-xu-gould-howison.md
  - papers/models-for-all-order-book-events.md
  - papers/mpc-trade-execution.md
  - papers/order-flow-filtration.md
  - papers/universal-price-formation-sirignano-cont.md
confidence: high
---

# The Price Impact of Order Book Events

**Authors**: Rama Cont, Arseniy Kukanov, Sasha Stoikov
**Institution**: Columbia University (Cont), Cornell University (Stoikov)
**Year**: 2010
**arXiv**: [1011.6402](https://arxiv.org/abs/1011.6402)
**Categories**: q-fin.TR, q-fin.ST

---

## Plain-language abstract

Every order book event — a limit order submission, a market order execution, or a cancellation — moves prices. This paper quantifies how and why. Using NYSE data for 50 stocks, the authors show that short-horizon price changes are driven almost entirely by **order flow imbalance (OFI)**: the net pressure at the best bid and ask. The relationship is linear, with the slope set by the market depth. This framework also explains the empirical "square-root law" of price impact.

---

## Key contributions

1. **Definition of OFI** — formally defined as the difference between the rate of buy-side and sell-side order book events at the best prices. Captures supply/demand imbalance more cleanly than raw trade volume.
2. **Linear price impact model** — $\Delta p \approx \beta \cdot \text{OFI}$, where $\beta \propto 1 / \text{depth}$.
3. **Square-root law derivation** — the empirically observed $\Delta p \propto \sqrt{Q}$ (price impact proportional to square root of trade size $Q$) is derived from the linear OFI model via a scaling argument.
4. **Robustness** — results are stable across time scales, intraday seasonality effects, and across 50 heterogeneous NYSE stocks.
5. **OFI vs volume** — OFI is a more reliable predictor of price changes than trade volume; the volume relationship is noisier.

---

## Method summary

### Data
One calendar month (April 2010) of TAQ data for 50 S&P 500 stocks chosen by random number generator, obtained via WRDS. Level 1 only (best bid/ask and queue sizes). Intraday 10-second time grid (21 trading days). **The ratio of quote updates to trades is ≈ 40 : 1** — this disparity motivates the use of quote flow over trade flow.

### OFI construction

Per-event signed contribution $e_n$ to the bid queue:

- $P^B$ unchanged: $e_n = q^B_n - q^B_{n-1}$ (limit add, market sell, or cancel at the best bid)
- $P^B$ increases: $e_n = q^B_n$ (price-improving limit buy lifts the best)
- $P^B$ decreases: $e_n = q^B_{n-1}$ (entire queue removed by market order or cancel)

Ask-side events use opposite signs. Aggregated over an interval:

$$\text{OFI}_k = \sum_{n = N(t_{k-1})+1}^{N(t_k)} e_n = L^b - C^b - M^s \;-\; L^s + C^s + M^b$$

where $L, C, M$ count limit orders, cancels, and market orders on each side. **Market sells and bid cancels are treated equivalently** since they have identical effect on the bid queue.

### Model

Under a stylized book with depth $D$ at each level beyond the best, the relation

$$\Delta P_k = \frac{\delta}{D}\,\text{OFI}_k + \epsilon_k$$

holds exactly (tick size $\delta$, depth $D$). Empirically the authors fit

$$\Delta P_k = \alpha_i + \beta_i \,\text{OFI}_k + \epsilon_k, \qquad \beta_i = c \cdot AD_i^{-\lambda}$$

by OLS on 273 half-hour sub-samples per stock, with $AD_i$ the average best-quote depth in sub-sample $i$. Standard errors are White (for the $\beta$ regression) and Newey–West (for the $\lambda$ regression).

---

## Main results

- **Linear OFI fits extremely well**: average $R^2 = 65\%$ across 50 stocks × 273 sub-samples. Adding a quadratic term $\gamma \cdot \text{OFI}_k|\text{OFI}_k|$ raises $R^2$ to 68% but the quadratic coefficient is insignificant for most samples — the relationship is well-modelled as linear.
- **Depth exponent $\lambda \approx 1$**: the hypothesis $\lambda = 1$ cannot be rejected for 35 out of 50 stocks (Newey–West, 5%). Depth enters approximately linearly, confirming the stylized model.
- **Tautology check**: even after removing price-changing events from $\text{OFI}_k$, average $R^2$ stays in 35–60% — the explanatory power is not just a mechanical artefact.
- **Intraday pattern**: depth at market open is ~½ of its daily average, so $\beta$ is ~2× higher; across the full session, $\beta$ at open is ~5× higher than at close. This explains the well-known intraday volatility U-shape using only depth and OFI — no need to invoke information asymmetry.
- **Robust to timescale**: $R^2$ rises with $\Delta t$ but qualitative results are unchanged from sub-second up to 10 minutes.
- **Trade volume alone is noisier**: restricting to trade volume gives an apparent square-root impact (via data aggregation), but it is less stable and less interpretable than the OFI linear model.

---

## Limitations

- **Level 1 only**: queue sizes at the best bid/ask only; deeper-level information is ignored. Later work (see [[papers/price-impact-generalized-ofi]]) extends to multi-level OFI.
- **Residuals heteroscedastic and somewhat autocorrelated** — White / Newey–West standard errors mitigate but do not remove this.
- **Exceptions**: for wide-spread / low-depth stocks (APOL, AZO, CME in the sample) the depth regression fits poorly — the Level-1 framework breaks when hidden orders or deep-book dynamics dominate.
- **Tautology risk**: price-changing events are both regressor and cause of the response; acknowledged but quantified (R² drops to 35–60% after exclusion).
- **Dataset vintage**: April 2010 NYSE, post-decimalisation but pre-modern HFT saturation. Market structure has continued to evolve.

---

## Connections

- Directly extended by [[papers/price-impact-generalized-ofi]] (log-GOFI for Chinese markets).
- Hawkes process forecasting of OFI built on this foundation: [[papers/forecasting-high-frequency-ofi]].
- Applied to crypto markets in [[papers/explainable-crypto-microstructure]].
- Core concept: [[concepts/order-flow-imbalance]].
- [[entities/rama-cont]] and [[entities/sasha-stoikov]] are central figures in microstructure.
