---
title: "Adverse Selection"
type: concept
created: 2026-04-15
updated: 2026-04-15
sources:
  - raw/papers/2602.00776.md
  - raw/papers/2507.22712.md
tags:
  - market-microstructure
  - adverse-selection
  - market-making
  - informed-trading
related:
  - concepts/market-microstructure.md
  - concepts/limit-order-book.md
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - papers/explainable-crypto-microstructure.md
  - papers/order-flow-filtration.md
confidence: high
---

# Adverse Selection

## Definition

**Adverse selection** in financial markets refers to the risk that a market maker (or any liquidity provider) faces when trading against a counterparty who possesses superior information. The market maker posts a bid and ask; if the incoming order is from an *informed trader* who knows the true value of the asset is outside the current spread, the market maker will consistently lose. This is the cost of providing liquidity.

---

## Historical context

Formalised in the Glosten-Milgrom (1985) model of the spread: the equilibrium bid-ask spread is set wide enough that the market maker breaks even across both informed and uninformed order flow. Kyle (1985) modelled the informed trader's optimal strategy as a linear demand schedule, giving the famous $\lambda$ price impact coefficient.

---

## How it works

In a market with mixed informed and uninformed traders:
- **Uninformed (noise) traders** arrive randomly and provide profits to the market maker.
- **Informed traders** arrive when they have private information; they always trade on the right side of the spread.
- The market maker cannot distinguish between them in real time.
- The spread must compensate: losses to informed traders are subsidised by profits from noise traders.

The **permanent price impact** of a trade is driven by the probability that it comes from an informed source. High adverse selection → wide spread, lower depth.

---

## Empirical validation in this wiki

The flash crash analysis in [[papers/explainable-crypto-microstructure]] provides a compelling natural experiment:
- **Taker strategy** (aggressive orders): collapses during the flash crash — the taker is picking off stale quotes but also getting run over by informed sellers.
- **Maker strategy** (passive orders): survives — consistent with makers withdrawing or resting orders that benefit from the post-crash mean reversion.

This supports classic adverse selection theory: during extreme events, the composition of order flow shifts heavily towards informed (or at least directional) flow, and liquidity provision becomes dangerous.

[[papers/order-flow-filtration]] operationalises this: filters targeting the parent orders of executed trades isolate informed flow, strengthening the OBI-return signal.

---

## Implications

- **Bid-ask spread** is partially an adverse selection premium.
- **Market depth** decreases when adverse selection risk is high (informed flow suspected).
- **Quote withdrawal** (market makers pulling liquidity) is a rational response to detected informed flow.
- **[[concepts/order-flow-imbalance]]** can be used to detect adverse selection risk in real time.

---

## Open questions

- How can market makers distinguish informed from uninformed flow in real time?
- Do structural LOB filters (as in [[papers/order-flow-filtration]]) reduce adverse selection costs?
- Is adverse selection risk quantifiably higher in crypto markets than equity markets?

---

## Connections

- [[concepts/market-microstructure]] — adverse selection is a core microstructure concept.
- [[concepts/limit-order-book]] — adverse selection manifests in LOB dynamics.
- [[concepts/order-flow-imbalance]] — informed flow drives OFI; filtering reveals it.
- [[papers/explainable-crypto-microstructure]] — flash crash validates adverse selection theory.
- [[papers/order-flow-filtration]] — filtration isolates informed flow.
