---
title: "Price Impact"
type: concept
created: 2026-04-15
updated: 2026-04-15
sources:
  - raw/papers/1011.6402.md
  - raw/papers/2112.02947.md
tags:
  - market-microstructure
  - price-impact
  - execution
  - trading
related:
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - concepts/market-microstructure.md
  - concepts/adverse-selection.md
  - papers/price-impact-order-book-events.md
  - papers/price-impact-generalized-ofi.md
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
