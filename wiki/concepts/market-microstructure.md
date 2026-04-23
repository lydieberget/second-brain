---
title: "Market Microstructure"
type: concept
created: 2026-04-15
updated: 2026-04-15
sources:
  - raw/papers/1011.6402.md
  - raw/papers/2403.09267.md
  - raw/papers/2507.22712.md
  - raw/papers/2602.00776.md
tags:
  - market-microstructure
  - finance
  - trading
related:
  - concepts/limit-order-book.md
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/adverse-selection.md
  - entities/rama-cont.md
  - entities/sasha-stoikov.md
  - methods/hawkes-process.md
confidence: high
---

# Market Microstructure

## Definition

**Market microstructure** is the branch of financial economics that studies the process by which assets are traded — specifically, how information, order flow, prices, and liquidity interact at the level of individual transactions. It sits between macro price theory (what prices should be) and market mechanics (how the exchange actually works).

---

## Core questions

1. How do prices form from individual order submissions?
2. How much does each trade move the price ([[concepts/price-impact]])?
3. How do informed and uninformed traders interact ([[concepts/adverse-selection]])?
4. What is the fair bid-ask spread, and what drives it?
5. How does market design (tick size, order types, latency) affect efficiency?

---

## Key building blocks

| Concept | Role |
|---|---|
| [[concepts/limit-order-book]] | The mechanism that matches buyers and sellers |
| [[concepts/order-flow-imbalance]] | The primary short-horizon price signal |
| [[concepts/price-impact]] | How orders move prices; central to execution cost |
| [[concepts/adverse-selection]] | Why market makers require a spread to break even |
| Bid-ask spread | Compensation to liquidity providers for adverse selection risk |
| Market depth | How much liquidity exists at each price level |

---

## Historical context

Modern microstructure theory formalised in the 1980s–90s with the Glosten-Milgrom (1985) and Kyle (1985) models. The LOB-based empirical tradition accelerated with the availability of high-frequency tick data in the 2000s. Key empirical milestones:

- Kyle (1985): informed trader model; $\lambda$ as price impact coefficient.
- Glosten-Milgrom (1985): adverse selection model of the spread.
- Cont, Kukanov, Stoikov (2010): OFI-based empirical price impact — [[papers/price-impact-order-book-events]].

---

## Research domains in this wiki

Papers in this wiki approaching microstructure from different angles:

| Paper | Angle |
|---|---|
| [[papers/price-impact-order-book-events]] | Foundational OFI-price impact relationship |
| [[papers/price-impact-generalized-ofi]] | OFI generalisation for non-standard tick sizes |
| [[papers/forecasting-high-frequency-ofi]] | Hawkes process OFI forecasting |
| [[papers/order-flow-filtration]] | Filtering noise vs informed flow |
| [[papers/deep-lob-forecasting]] | Deep learning for mid-price prediction |
| [[papers/explainable-crypto-microstructure]] | Cross-asset LOB feature stability in crypto |

---

## Open questions

- Is there a universal LOB representation that works across asset classes?
- How do algorithmic market makers adapt to detected informed flow?
- How does microstructure change near market open/close (liquidity cycles)?

---

## Connections

- [[concepts/limit-order-book]] — the core data object.
- [[concepts/order-flow-imbalance]] — the dominant short-horizon signal.
- [[entities/rama-cont]] and [[entities/sasha-stoikov]] — key contributors to empirical microstructure.
- [[connections/deep-learning-meets-market-microstructure]] — ML methods applied to microstructure problems.
