---
title: "Market Making"
type: concept
created: 2026-04-16
updated: 2026-04-16
sources:
  - raw/papers/2603.01344.md
  - raw/papers/1011.6402.md
tags:
  - market-making
  - liquidity-provision
  - market-microstructure
  - inventory-risk
  - adverse-selection
  - algorithmic-trading
related:
  - concepts/adverse-selection.md
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/limit-order-book.md
  - papers/cfmm-liquidity-provision-pricing.md
  - papers/explainable-crypto-microstructure.md
confidence: high
---

# Market Making

## Definition

**Market making** is the activity of simultaneously quoting bid and offer prices for an asset and earning the spread from trades that occur against those quotes. The market maker provides **liquidity** in exchange for being compensated for two risks:

- **Inventory risk** — accumulating a directional position the market maker did not want.
- **Adverse selection** — being systematically picked off by better-informed traders (see [[concepts/adverse-selection]]).

Modern market making is almost entirely algorithmic.

---

## Two paradigms

### 1. Limit Order Book (LOB) market making

Quote passive limit orders on both sides of the book; earn the spread when both sides fill. This is the dominant model on traditional exchanges (equities, futures, FX, options).

Key decisions:
- **Quote prices** (distance from mid) — wider = less adverse selection, but lower fill probability.
- **Inventory management** — skew quotes asymmetrically when inventory drifts.
- **Cancellation/replacement** — respond to order-flow imbalance signals.

Foundational models:
- **Avellaneda & Stoikov (2008)** — stochastic-control model that derives optimal bid/ask quotes from an inventory penalty and a terminal utility.
- **Guéant–Lehalle–Fernandez-Tapia (2013)** — asymptotic expansion, closed-form solutions for high-frequency limits.
- **Glosten–Milgrom (1985)** — information-based spread from adverse selection.

### 2. Automated Market Maker (AMM) liquidity provision

Deposit tokens into a smart contract with a **bonding curve** $f(x, y) = K$; the contract mechanically trades on your behalf according to the curve. This is the DeFi paradigm (Uniswap, Balancer, Curve).

Key structural facts:
- An LP position is a **derivative** of the pool assets, not a passive deposit.
- LPs earn fees but incur **Impermanent Loss (IL)** — value lost to price divergence vs simple buy-and-hold.
- LPs also lose to informed arbitrageurs via **Loss-Versus-Rebalancing (LVR)** — the AMM analogue of adverse selection.

See [[papers/cfmm-liquidity-provision-pricing]] for a rigorous derivatives-pricing framework that characterises LP payoffs and IL as option strips.

---

## Comparison

| Dimension | LOB market making | AMM liquidity provision |
|---|---|---|
| Venue | Traditional exchanges | DeFi / smart contracts |
| Pricing rule | Market maker sets quotes dynamically | Deterministic bonding curve |
| Inventory control | Active — skew, cancel, reprice | Passive — dictated by curve |
| Adverse selection | Glosten–Milgrom spread | Loss-Versus-Rebalancing |
| Revenue | Spread + rebates | Pool fees |
| Capital efficiency | High (fractional inventory) | Lower (full capital locked) |
| Risk decomposition | Inventory + adverse selection | Impermanent Loss + LVR |
| Typical horizon | Sub-second to minutes | Minutes to weeks |

---

## Connections between the two

Despite very different machinery, both paradigms share the same **structural tension**: liquidity providers earn a spread/fee but lose systematically to informed flow. The microstructure theory of adverse selection (Kyle 1985; Glosten–Milgrom 1985) re-emerges in DeFi as LVR; the mathematical tools (stochastic control for LOB; option-pricing theory for AMMs) differ, but the economic intuition is the same.

In hybrid settings (crypto markets trade on both centralised order books and DEXs), arbitrageurs bridge the two — e.g., the W/USDT spot vs perpetual tick-size experiment in [[papers/explainable-crypto-microstructure]] shows how CEX book imbalance carries information that AMM prices implicitly track.

---

## Open questions

- What is the optimal market-making strategy in a hybrid CEX+DEX ecosystem where the same asset trades on both venue types?
- Can LOB-learned inventory-management policies transfer to AMM range-selection in Uniswap v3 concentrated liquidity?
- How do recent order-book regulations (e.g., persistent-noise-creator penalties in India — see [[papers/order-flow-filtration]]) affect market-maker economics?
- RL and MPC approaches to LOB market making are well-studied (Nevmyvaka et al.; Hendricks–Wilcox); equivalent for dynamic range selection in AMMs is still early-stage.

---

## Connections

- [[concepts/adverse-selection]] — the structural risk both paradigms share.
- [[concepts/order-flow-imbalance]] — the main short-horizon signal used in LOB market making for quote adjustment.
- [[concepts/limit-order-book]] — the venue for traditional market making.
- [[papers/cfmm-liquidity-provision-pricing]] — rigorous pricing framework for AMM LP positions.
- [[papers/explainable-crypto-microstructure]] — SHAP analysis of LOB features in crypto; links centralised-exchange market making to the same assets that trade on AMMs.
- [[concepts/optimal-execution]] — the dual problem (the market maker is the counterparty to the executing trader).
