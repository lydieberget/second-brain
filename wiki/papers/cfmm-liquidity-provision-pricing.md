---
title: "Pricing and Hedging for Liquidity Provision in Constant Function Market Making"
type: paper
created: 2026-04-16
updated: 2026-04-16
sources:
  - raw/papers/2603.01344.md
tags:
  - market-making
  - decentralized-finance
  - automated-market-maker
  - cfmm
  - uniswap
  - impermanent-loss
  - option-pricing
  - cryptocurrency
related:
  - concepts/market-making.md
  - concepts/adverse-selection.md
  - methods/microprice.md
  - papers/explainable-crypto-microstructure.md
confidence: medium
---

# Pricing and Hedging for Liquidity Provision in Constant Function Market Making

**Authors**: Jimmy Risk, Shen-Ning Tung, Tai-Ho Wang
**Year**: 2026 (March 2026)
**arXiv**: [2603.01344](https://arxiv.org/abs/2603.01344)
**Categories**: q-fin.MF

---

## Plain-language abstract

In DeFi, **Constant Function Market Makers** (CFMMs) like **Uniswap** and **Balancer** replace the traditional limit order book with a deterministic **bonding curve** $f(x, y) = K$ relating token reserves to prices. A Liquidity Provider (LP) deposits tokens into a smart contract and effectively sells them to the market according to this rule — so an LP position is really a derivative, not a passive deposit. This paper reframes CFMM analysis from the usual (token reserves) coordinates into a **(price, intrinsic liquidity)** coordinate system that is dimensionally consistent across bonding curves. Under this coordinate change, reserves and value functions become **linear** in the liquidity profile, which in turn lets the authors characterise **Impermanent Loss as a weighted strip of vanilla options** via the Carr–Madan spanning formula. Empirical validation on Uniswap v3 ETH/USDC pools vs Deribit option implied-vol surfaces confirms a crypto-consistent volatility smile.

---

## Key contributions

1. **Dimensionally consistent "intrinsic liquidity"** — the standard $K$ in bonding curves like $\sqrt{xy} = K$ (CPMM) or $x^\alpha y^{1-\alpha} = K$ (G3M) carries **different physical dimensions** across protocols, so you cannot compare liquidity across them numerically. The authors define a local intrinsic liquidity $\ell(x, y)$ that always has dimension $\sqrt{\text{ETH} \times \text{USDC}}$, regardless of the functional form of $f$.
2. **Canonical parametrization theorem** — reserves $(x, y)$ can be recovered from the pair (spot price $p$, local intrinsic liquidity profile $\ell(p)$) via integral representations, independent of the bonding-curve parametrisation.
3. **Linear structure** — mark-to-market value $V_L(p)$ is linear in the liquidity profile $L(q)$, which simplifies arbitrage-free pricing, delta hedging, and systematic risk management.
4. **IL as weighted options strip** — via Carr–Madan, Impermanent Loss can be decomposed into a weighted strip of vanilla calls/puts with weights set by $L(q)$. This gives a **fine-structure implied volatility** for liquidity profiles.
5. **Path-dependent IL via last-passage time** — provides granular risk analysis of when IL is actually realised.
6. **Empirical consistency**: Uniswap v3 ETH/USDC pool data vs Deribit option markets shows a volatility smile consistent with crypto-asset dynamics.

---

## Method summary

### Coordinate change: reserves → (price, liquidity)

For a smooth bonding curve $f(x, y) = K$, the local intrinsic liquidity at reserve state $(x, y)$ is defined via partial derivatives of $f$ so that the result always carries dimension $\sqrt{\text{ETH}\times\text{USDC}}$ — matching CPMM's $K$ regardless of the underlying form.

- **Locality**: $\ell$ depends on the current reserve point (it is state-dependent, unlike $K$).
- **Invariance**: $\ell$ is intrinsic to the geometry of the level curve; unchanged under reparametrisations like $xy = K^2$ vs $\sqrt{xy} = K$.

### The canonical parametrization (Theorem 2.2)

Given smooth, strictly increasing, convex $f$, the reserves at price $p$ are:

$$x(p) = \int_p^\infty \frac{L(q)}{q} \, dq, \qquad y(p) = \int_0^p q \cdot L(q) \, dq \cdot \text{(with appropriate scaling)}$$

where $L(q) = \ell(q)/q$ is the **liquidity profile**. This expresses the CFMM in a coordinate system that is protocol-agnostic.

### LP value as covered-call strip

Mark-to-market value with token $Y$ as numéraire:

$$V_L(p) = \int_0^\infty \min\{p, q\} \cdot L(q) \, dq$$

Since $\min\{p, q\} = p - (p - q)^+$ is a covered call payoff, $V_L$ is a **weighted strip of covered calls** indexed by $L(q)$. This is the bridge to derivatives pricing.

### Impermanent Loss via Carr–Madan

Using Carr–Madan's spanning formula, IL decomposes into a weighted combination of vanilla options, yielding a risk-neutral decomposition amenable to delta hedging with standard option instruments.

### Empirical validation

- Uniswap v3 ETH/USDC pool liquidity profiles.
- Deribit ETH options for comparison implied-vol smile.
- Fitted fine-structure IV from LP positions matches crypto-asset volatility smile properties.

---

## Main results

- LP positions in Uniswap v2 (CPMM) and Uniswap v3 (concentrated liquidity) unify under the same price–liquidity coordinate system.
- Impermanent Loss is exactly hedgeable via a static option strip whose weights are determined by the current liquidity profile.
- The implied-vol structure extracted from LP fee streams is consistent with Deribit-observed crypto vol smile.
- The framework subsumes / recovers existing partial results (Fukasawa et al. variance-swap IL hedge, Angeris–Evans–Chitra CFMM payoff space, Loss-Versus-Rebalancing as continuous-installment option, etc.).

---

## Limitations

- **Geometry assumes smooth, convex, increasing $f$** — some newer AMM invariants (proactive market makers with discontinuities) are out of scope.
- **Continuous-time setting**: discrete fee events, gas costs, and MEV extraction are abstracted away.
- **Single-pool analysis**: cross-pool arbitrage, multi-asset baskets (Balancer n-token pools beyond G3M), and routing across DEX aggregators not modelled.
- **No informed-flow / adverse-selection model**: LPs in reality lose systematically to arbitrageurs (Loss-Versus-Rebalancing); this paper prices LP positions risk-neutrally but does not model the structural *drag* of trading against informed flow in equilibrium.
- **Empirical scope**: ETH/USDC on Uniswap v3 only; alt-L2 pools and stable-stable pools have different dynamics.

---

## Connections

- This is **market making in the AMM paradigm** — a parallel world to traditional LOB market making. See [[concepts/market-making]] for the combined picture.
- Crypto-native setting complements the centralised-exchange crypto work in [[papers/explainable-crypto-microstructure]], which studies Binance Futures perpetuals (order-book venue). The two together span the main venues where LPs operate.
- **Adverse selection** is the conceptual link to traditional microstructure: Loss-Versus-Rebalancing is the AMM analogue of Glosten–Milgrom adverse selection — LPs lose to informed arbitrageurs who rebalance pools when prices move. See [[concepts/adverse-selection]].
- Carr–Madan spanning sits in the broader derivatives literature; this paper's main engineering value is the **coordinate change** that makes that classical tool apply cleanly to LP positions.
