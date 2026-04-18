---
title: "How Markets Slowly Digest Changes in Supply and Demand"
type: paper
created: 2026-04-17
updated: 2026-04-17
sources:
  - raw/papers/0809.0822.md
tags:
  - market-impact
  - propagator-model
  - long-memory
  - order-flow
  - market-microstructure
  - review
  - foundational
related:
  - concepts/price-impact.md
  - concepts/order-flow-imbalance.md
  - concepts/market-microstructure.md
  - concepts/adverse-selection.md
  - methods/propagator-model.md
  - papers/price-impact-order-book-events.md
  - papers/brokmann-slow-decay-impact.md
confidence: high
---

# How Markets Slowly Digest Changes in Supply and Demand

**Authors**: Jean-Philippe Bouchaud, J. Doyne Farmer, Fabrizio Lillo
**Institutions**: Capital Fund Management (Paris); Santa Fe Institute / LUISS Guido Carli (Roma); Università di Palermo
**Year**: 2008 (book chapter, arXiv September 2008)
**arXiv**: [0809.0822](https://arxiv.org/abs/0809.0822)
**Categories**: q-fin.TR (book chapter in Hens & Schenk-Hoppé eds., "Handbook of Financial Markets: Dynamics and Evolution")

---

## Plain-language abstract

A canonical survey / manifesto of the **"econophysics" view of price formation**. Large orders cannot be executed instantly — they must be **sliced and traded incrementally over hours to months** — so the visible order flow is a strongly persistent, long-memory process. Reconciling long-memory order flow with the empirical fact that price series are close to martingales forces a specific theoretical structure: **market impact must be transient, with a slowly decaying kernel**, and liquidity must co-adjust. The paper reviews the **propagator model** (response function $G$), the long-memory facts, concave impact of individual trades, the square-root law of aggregate impact, spread-impact links, and empirical tests on equities. Its central claim is that most of the information processed by markets comes from **supply and demand itself**, not from external news.

---

## Key concepts and formulas

### The propagator (transient impact) model

See [[methods/propagator-model]] for a dedicated method page. The mid-price return at time $t$ is a linear superposition of the impact of all past signed trades $\varepsilon_{t'} \in \{+1, -1\}$:

$$r_t = \sum_{t' \leq t} G(t - t') \cdot \varepsilon_{t'} + \eta_t$$

where:
- $G(\tau)$ is the **response function / propagator**, typically a slowly decaying power law $G(\tau) \sim \tau^{-\beta}$ with $\beta \approx 0.2$–$0.5$.
- $\eta_t$ is an uncorrelated noise term.

For prices to be diffusive despite long-memory in $\varepsilon$, the decay of $G$ must **exactly offset** the persistence of $\varepsilon$ — a non-trivial self-consistency constraint.

### Long memory of order flow

Sign autocorrelation of trades decays as a power law:

$$\mathbb{E}[\varepsilon_t \varepsilon_{t+\tau}] \sim \tau^{-\gamma}, \qquad 0 < \gamma < 1$$

on any liquid equity, for $\tau$ over hours to days. Explained by **order splitting of large hidden meta-orders**: a few hundred large parent orders executed over long horizons generate the persistence.

### Concave individual-transaction impact

Average price shift caused by a single trade of volume $v$:

$$\mathbb{E}[\Delta p \mid v] \sim \log(v) \quad \text{or} \quad \mathbb{E}[\Delta p \mid v] \sim v^\alpha, \; \alpha \in [0, 0.5]$$

Concave: doubling the trade does not double the impact.

### Square-root law of aggregate (metaorder) impact

For a metaorder of total size $Q$:

$$I(Q) \sim \sigma \cdot \left(\frac{Q}{V}\right)^{1/2}$$

with $\sigma$ daily volatility, $V$ daily volume. This is **Kyle's 1/2 exponent** emerging empirically from the propagator dynamics + long-memory flow, not assumed a priori.

### Spread and impact (Glosten-Milgrom / MRR models)

The bid-ask spread compensates market makers for two things:
1. **Adverse selection** — trading against better-informed agents.
2. **Inventory carrying risk**.

In the Glosten-Milgrom model, spread is exactly the asymmetric-information expected loss per trade. The paper reviews why empirical spreads sit close to this theoretical floor for liquid stocks.

---

## Key empirical findings surveyed

- **Signed order flow is long-memory** in 30+ liquid equities across exchanges and decades.
- **Impact is roughly concave** in single-trade volume, power-law with $\alpha \approx 0.1$–$0.3$.
- **Metaorder impact follows square-root law** with coefficient proportional to volatility / $\sqrt{\text{volume}}$.
- **Impact decays over time** after metaorder completion: partial reversion but some permanent residual.
- **Spread and impact are strongly correlated** — larger average spreads on days with larger realised volatility.
- **Spread has diurnal pattern** (U-shape) matching volatility / impact.
- **Liquidity evaporates before price moves**: the paper documents the "queue depletion" phenomenon where depth at best quotes decreases before a price tick.

---

## Two interpretive frameworks contrasted

### Fixed permanent impact (Kyle / MRR)
Each trade permanently shifts the efficient price. Requires that informed vs uninformed trades can be distinguished. Simple but struggles with:
- Long memory of order flow should imply predictable returns, which is absent empirically.
- Concavity of individual-trade impact is unexplained.

### Transient impact (propagator) model
Each trade temporarily shifts prices; impact decays over time. Handles long-memory order flow cleanly: returns remain unpredictable *because* a persistent order flow is absorbed by a decaying response kernel. Predicts the right qualitative shape of impact. The paper argues this framework is more empirically supported.

The authors also discuss **"history-dependent permanent impact"** as a third unified framework that recovers both as limits.

---

## Main theoretical claims

- Market efficiency + long-memory order flow **jointly force** a transient, slowly-decaying impact kernel.
- Square-root law of metaorder impact is a **consequence** of this kernel structure plus long-memory flow — not an empirical accident nor a derivation from rational expectations.
- The **"volatility puzzle"** (excess volatility vs fundamental volatility) is partially resolved by noting that most order flow is uninformed (noise + order-splitting) and still causes real price movement through the propagator.
- Supply–demand itself carries most of the *processed* information in markets, not external news. Most informed agents are at best **weakly informed**.

---

## Limitations (acknowledged in the paper and since)

- **Linear propagator model** — real impact has interaction terms (e.g., sign-dependent, spread-dependent).
- **Constant kernel $G$** — in reality $G$ is **state-dependent** (stress regimes, intraday patterns).
- **No distinction between limit and market order impact** — later work (e.g., Eisler–Bouchaud–Kockelkoren) generalises with a multivariate propagator.
- **Most empirics are on equities** — FX, futures, and crypto later show partial but not exact agreement.
- Spread–impact link is broadly correct but the ratio is not universal across assets.

---

## Why it matters for this wiki

This paper is one of the **three foundational references** on market impact theory, alongside Kyle (1985) and Almgren-Chriss (2001). It is cited by essentially every paper already in the wiki that talks about impact: [[papers/price-impact-order-book-events]], [[papers/mpc-trade-execution]], [[papers/reality-gap-lob-simulation]], [[papers/order-flow-filtration]].

The **propagator formulation** is what motivated Noble–Rosenbaum–Souilmi ([[papers/reality-gap-lob-simulation]]) to add a power-law impact feedback kernel to their QR simulator. It also underlies the Bacry et al. multivariate-Hawkes impact decomposition referenced in [[papers/forecasting-high-frequency-ofi]] and [[papers/order-flow-filtration]].

---

## Connections

- **Definitional anchor** for [[concepts/price-impact]] — propagator decomposition, square-root law, spread-impact link.
- **Classical comparator** to [[papers/price-impact-order-book-events]] — CKS derive a *linear* impact from OFI rather than a propagator-kernel on signed trades. Different inputs, complementary conclusions.
- **Long-memory order flow** is the foundation underneath [[methods/hawkes-process]] approaches in [[papers/forecasting-high-frequency-ofi]] and [[papers/order-flow-filtration]].
- **Glosten-Milgrom review** inside this paper provides the adverse-selection foundation for [[concepts/adverse-selection]] and [[concepts/market-making]] — despite GM itself not being on arXiv.
- **Kyle model review** — the paper references Kyle 1985 (also not arXiv) but reconstructs its key results.
