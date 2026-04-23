---
title: "Price Impact"
type: concept
created: 2026-04-15
updated: 2026-04-23
sources:
  - raw/papers/1011.6402.md
  - raw/papers/2112.02947.md
  - raw/papers/2112.13213.md
  - raw/papers/0904.0900.md
  - raw/papers/1107.3364.md
tags:
  - market-microstructure
  - price-impact
  - execution
  - trading
related:
  - concepts/order-flow-imbalance.md
  - concepts/cross-impact.md
  - concepts/limit-order-book.md
  - concepts/market-microstructure.md
  - concepts/adverse-selection.md
  - methods/integrated-ofi.md
  - methods/event-type-impact-decomposition.md
  - methods/propagator-model.md
  - papers/price-impact-order-book-events.md
  - papers/price-impact-generalized-ofi.md
  - papers/cross-impact-ofi-equity-markets.md
  - papers/eisler-bouchaud-kockelkoren-order-book-events.md
  - papers/models-for-all-order-book-events.md
  - concepts/optimal-execution.md
  - concepts/universal-price-formation.md
  - entities/jean-philippe-bouchaud.md
  - entities/zoltan-eisler.md
  - methods/microprice.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/mpc-trade-execution.md
confidence: high
---

# Price Impact

## Definition

**Price impact** is the change in asset price caused by executing a trade or submitting orders to the market. A buy order pushes prices up; a sell order pushes them down. Price impact is a cost of trading and a central quantity in market microstructure.

---

## Types

| Type | Description |
|---|---|
| **Temporary impact** | Immediate price move from consuming liquidity; partially reverts after the trade |
| **Permanent impact** | Lasting price change due to information content of the trade |
| **Total impact** | Sum of temporary and permanent; the full cost to an execution algorithm |

---

## Empirical relationships

**Linear OFI model** (Cont, Kukanov & Stoikov 2010):

$$\Delta p_t = \beta \cdot \text{OFI}_t + \epsilon_t$$

where $\beta \propto 1/\text{depth}$. This is the workhorse short-horizon model. See [[papers/price-impact-order-book-events]].

**Square-root law** (widely documented):

$$\Delta p \propto \sqrt{Q}$$

Price impact is concave in trade size $Q$ — doubling the trade size does not double the price impact. Cont et al. derive this from the linear OFI model via a scaling argument.

---

## Determinants

- **Market depth** — deeper order books absorb flow more cheaply; $\beta$ is smaller.
- **Volatility** — higher volatility markets exhibit larger impact per unit of flow.
- **Trade size** — impact grows sub-linearly (square-root law) with size.
- **Information content** — informed trades have larger permanent impact.
- **Time of day** — impact is typically higher near open/close when liquidity is thinner.

---

## Relation to OFI

Short-horizon price impact is primarily driven by [[concepts/order-flow-imbalance]], not by raw trade volume. The key insight from Cont et al. is that OFI — which measures the *net* pressure at the best bid/ask from all order book events (not just executed trades) — is a more robust predictor than volume alone.

Subsequent work has shown that **aggregating across multiple book levels** via [[methods/integrated-ofi|integrated OFI]] raises OOS $R^2$ from $\sim\!65\%$ (best-level) to $\sim\!84\%$ on Nasdaq-100 ([[papers/cross-impact-ofi-equity-markets]]).

## Cross-impact

In a multi-asset setting, price impact generalises to [[concepts/cross-impact]] — the effect of asset $j$'s order flow on asset $i$'s price. Empirically:

- **Contemporaneous** cross-impact is negligible once you use integrated OFI (the multi-level aggregation subsumes it).
- **Predictive** (lagged) cross-impact is real at short horizons ($\leq 3$ min) and decays rapidly with forecast horizon.

## Event-type decomposition

At the finest resolution, price impact can be decomposed by the six [[methods/event-type-impact-decomposition|EBK event types]] — market orders, limit orders, and cancellations, each split into "at-best" and "inside-spread" variants. Key findings ([[papers/eisler-bouchaud-kockelkoren-order-book-events]], [[papers/models-for-all-order-book-events]]):

- **Limit-order impact is real and ~60–70% of market-order impact** — trade-tape-only studies underestimate total impact.
- **Large-tick stocks**: bare impacts are permanent and non-fluctuating (simple constant-impact model fits).
- **Small-tick stocks**: bare impacts acquire history dependence via gap fluctuations; a linear AR model on past event flow captures it.
- The market-order-only propagator $G(\tau)$ in earlier [[methods/propagator-model|propagator work]] is "dressed" by unobserved LO/CA flow — separating them recovers the true bare impacts.

---

## Open questions

- What is the correct functional form of impact at large sizes? (Power law vs log?)
- How does permanent vs temporary split vary by asset and market regime?
- Do machine learning models add predictive power beyond linear OFI models?

---

## Connections

- [[concepts/order-flow-imbalance]] — the primary driver of short-horizon price impact.
- [[concepts/limit-order-book]] — impact is mediated by the state of the book.
- [[concepts/adverse-selection]] — permanent impact is related to information asymmetry.
- [[papers/price-impact-order-book-events]] — seminal empirical paper.
- [[papers/price-impact-generalized-ofi]] — improved OFI for better impact prediction.
