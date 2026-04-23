---
title: "The Price Impact of Order Book Events: Market Orders, Limit Orders and Cancellations"
type: paper
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/0904.0900.md
tags:
  - price-impact
  - order-book-events
  - propagator-model
  - tick-size
  - market-orders
  - limit-orders
  - cancellations
  - signal-design
related:
  - concepts/price-impact.md
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - methods/event-type-impact-decomposition.md
  - methods/propagator-model.md
  - papers/price-impact-order-book-events.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/models-for-all-order-book-events.md
  - entities/jean-philippe-bouchaud.md
  - entities/zoltan-eisler.md
confidence: high
---

# The Price Impact of Order Book Events: Market Orders, Limit Orders and Cancellations

**Authors**: [[entities/zoltan-eisler|Zoltán Eisler]], [[entities/jean-philippe-bouchaud|Jean-Philippe Bouchaud]], Julien Kockelkoren
**Institution**: Capital Fund Management, Paris
**Year**: 2009 (arXiv April 2009; published *Quantitative Finance* 12(9), 2012)
**arXiv**: [0904.0900](https://arxiv.org/abs/0904.0900)
**Categories**: q-fin.TR, q-fin.ST

---

## Plain-language abstract

The standard impact-model story treats "a trade" as the object that moves prices. This paper says no — on modern electronic markets every order-book event (market order, limit order arrival, cancellation, at or inside the spread) contributes, and you should measure them all. By tracking **six event types** (MO⁰, MO', LO⁰, LO', CA⁰, CA' — with ' meaning "changes the best price") on 14 NASDAQ stocks in 2008, the authors extract the **"bare" impact** of each event type — what the event would contribute if it happened in isolation, stripped of correlations with surrounding flow. Two headline findings: (i) for **large-tick stocks**, bare impacts are **permanent and non-fluctuating** — a simple constant-impact model fits; (ii) for **small-tick stocks**, bare impacts are **history-dependent** — the gap behind the best quote fluctuates and carries a non-trivial memory of past flow, accurately modelled by an autoregressive correction. The decomposition framework generalises the earlier market-order-only propagator model and connects to Hasbrouck's VAR.

---

## Key contributions

1. **Six-event-type taxonomy** — MO⁰, MO', LO⁰, LO', CA⁰, CA' (0 = no price change at best; ' = changes best price). Each event carries a sign $\epsilon$ (direction of expected price effect) and a gap $\Delta$ (size of price move if it moves the price). This taxonomy is now standard in empirical microstructure.
2. **Bare vs dressed impact distinction** — The market-order propagator $G(\tau)$ measured in trades-only data is "dressed" by unobserved limit-order / cancellation flow. The authors derive the bare-impact extraction:

$$R_\pi(\ell) = \sum_{\pi_1} \sum_{\ell' = 0}^{\ell - 1} G_{\pi_1}(\ell - \ell') P(\pi_1) C_{\pi, \pi_1}(\ell')$$

where $R_\pi$ is the observed response to event type $\pi$, $C_{\pi, \pi'}$ is the signed event-event correlation, and $G_\pi$ is the unobserved bare impact. Inverting this linear system recovers $G_\pi$.
3. **Constant-impact model works for large-tick stocks** — Assuming $G_\pi(\ell) = \text{const}$ for each event type and using constant realised gaps $\Delta^R_\pi$, the predicted response functions and price diffusion match data nearly perfectly. Large-tick stocks have negligible gap fluctuations, so the propagator is truly permanent.
4. **Small-tick stocks need gap dynamics** — Gap fluctuations behind the best quote carry history dependence. A linear AR model on past order flow $\Delta^R_\pi$ captures this:

$$\Delta_{\pi, \epsilon, t} = \Delta^R_\pi + \sum_{\pi', \ell > 0} K_{\pi, \pi'}(\ell) \cdot \epsilon_{t-\ell} \cdot I(\pi_{t-\ell} = \pi')$$

The kernels $K$ are fitted via OLS from empirical cross-correlations and restore the fit to data.
5. **Limit-order impact is real** — Contrary to earlier trade-only work, limit orders have measurable (though smaller) impact than market orders. Implies that a cancellation inside the spread is nearly as potent as a market sell at the bid, and that "market-order impact" in earlier studies conflates the bare impact with induced limit-order/cancellation flow.
6. **Three-way impact decomposition** — The price change triggered by an event splits into: (a) the instantaneous jump, (b) the modification of future event-type rates (induced compensating flow), (c) the modification of future gap sizes. All three observable within this framework.
7. **Hasbrouck VAR relation** — The propagator model is a structural restriction of the VAR framework: $B_{rr}(\ell) = 0$ (past returns cannot directly affect current returns) plus a specific causal interpretation.
8. **Spread dynamics** — Appendix extends the framework to the bid-ask spread, which is expressed as a linear function of past signed events — a bonus by-product.

---

## Method summary

### The six event types

| Event | Description | Gap $\Delta$ |
|---|---|---|
| MO⁰ | market order, volume $<$ outstanding at best | 0 (no price move) |
| MO' | market order, volume $\geq$ outstanding at best | half the gap to the second-best |
| CA⁰ | partial cancellation at the best | 0 |
| LO⁰ | limit order at the current best | 0 |
| CA' | complete cancellation of the best | half the gap to the second-best |
| LO' | limit order inside the spread | half distance from the previous best |

Event sign $\epsilon = +1$ for buy-side (buy MO, cancelled sell LO, incoming buy LO), $-1$ for sell-side. Side $s$ distinguishes bid vs ask — different from $\epsilon$ for LO events.

### The response function

For event type $\pi$ with sign $\epsilon$ at time $t$, the mid-price moves by $p_{t+\ell} - p_t$ on average:

$$R_\pi(\ell) = \mathbb{E}[(p_{t+\ell} - p_t) \cdot \epsilon_t \cdot I(\pi_t = \pi)] / P(\pi)$$

Six response functions measured directly from data.

### Correlation structure

Signed event-event correlations $C_{\pi_1, \pi_2}(\ell)$: 36 of them, measured. Unsigned $\Pi_{\pi_1, \pi_2}(\ell)$ captures clustering. Key empirical finding: the sign of events overall ($\epsilon_t$) is **short-range correlated** (auto-corr dies at ~100 events), but the *side* of events ($s_t$) is long-range correlated with decay exponent $\gamma \approx 0.7$. The mixing of limit orders and market orders compensates the market-order persistence to keep prices near-diffusive.

### Temporary impact model (generalised)

$$p_t = p_0 + \sum_{t' < t} \sum_\pi G_\pi(t - t') \cdot \epsilon_{t'} \cdot I(\pi_{t'} = \pi)$$

Recover $G_\pi$ by inverting the response equation. Diagnostic: compute the predicted price variance $D(\ell)/\ell$ and compare to data. Large-tick: poor fit. Small-tick: decent but not great.

### Constant-impact model

Replace $G_\pi(\ell) \to G_\pi$ and $\Delta_{\pi, \epsilon, t} \to \Delta^R_\pi$. Both conditions ("permanent impact" + "no gap fluctuations"). Works well for large-tick. For small-tick, extend with the linear AR model on gap fluctuations.

### Data

- 14 NASDAQ stocks, 3 Mar – 19 May 2008 (53 trading days).
- ~10⁶–10⁷ events per stock.
- Split large-tick (spread ~1 tick: AMAT, CMCSA, CSCO, DELL, INTC, MSFT, ORCL) vs small-tick (spread ~3–4 ticks: AAPL, AMZN, APOL, COST, ESRX, GILD).

---

## Main results

### Large-tick stocks

- Event-type frequencies: LO⁰ ≈ CA⁰ ≈ 40% each, MO⁰ ≈ 5%, price-changing events total ~3%.
- Constant-impact model: near-perfect fit to both $R_\pi(\ell)$ and $D(\ell)/\ell$.
- Bare impacts: permanent and non-fluctuating. Limit-order impact ~ 60–70% of market-order impact.

### Small-tick stocks

- Event-type frequencies: LO⁰ ~ 33%, CA⁰ ~ 26%, MO⁰ ~ 5%, price-changing events ~35–40%.
- Realised gaps much larger than average gaps (AAPL: $2\Delta^R_{\text{MO'}} = 1.31$ ticks vs $2\langle\Delta_{\text{MO'}}\rangle = 1.14$). The act of moving the price is correlated with opening a larger gap.
- Constant-impact model noticeably off. History-dependent AR model restores the fit.

### Stylised facts reconfirmed / refined

- Market-order signs $\epsilon_{\text{MO}}$ are long-range correlated ($\gamma \approx 0.7$). All-event signs $\epsilon$ are not — the reverting limit-order flow compensates.
- MO, CA, LO cluster in time — aggressive orders induce more aggressive orders.
- "Stimulated refill" of liquidity after a price-changing market order (LO' arrives quickly to rebuild the book).
- Time-reversal symmetry holds for some event pairs (MO⁰/CA⁰, MO'/CA') but not all (MO'/LO' is asymmetric).

---

## Limitations

- **Level-1 only.** Events deeper in the book are treated as unobserved; their influence appears as residual "dressing" of the bare impact. A stronger version would observe all levels.
- **Multi-venue liquidity.** Stocks trade across many platforms; events on other venues are unobserved and also "dress" the impacts measured on NASDAQ.
- **Short data window.** 53 days in 2008 only — a turbulent year. Stability across regimes not tested.
- **Signless volume.** Volume dependence is weak and collapsed into a dichotomy (moves-price vs does-not-move-price). A richer volume treatment might uncover non-linearities.
- **Linearity assumption.** The superposition-of-bare-impacts model is linear. Large events or stressed regimes likely break linearity.
- **Gaps only between levels 1 and 2.** The AR gap model covers only the first hidden gap — deeper gap dynamics are lumped in the residual.

---

## Connections to other wiki pages

- **Extends**: [[papers/price-impact-order-book-events]] (Cont-Kukanov-Stoikov 2014, same data idea at a different resolution — OFI vs event-type decomposition); [[papers/bouchaud-farmer-lillo-propagator]] (the single-event market-order propagator).
- **Directly extended by**: [[papers/models-for-all-order-book-events]] (Eisler-Bouchaud-Kockelkoren 2011) — elaborates the history-dependent model for small-tick stocks with explicit dynamic gap modelling.
- **Cross-connection**: [[papers/cross-impact-ofi-equity-markets]] — which side of the "bare impact" story does integrated OFI capture? Almost all of it for large-tick stocks; small-tick behaviour still partially non-linear via gap dynamics.
- **Method it defines**: [[methods/event-type-impact-decomposition]] — the per-event-type bare-impact extraction framework.
- **Relates to**: [[methods/propagator-model]] — this paper is its multi-event-type generalisation.
- **Companion**: [[concepts/order-flow-imbalance]] — OFI as defined by Cont-Kukanov-Stoikov is a specific linear combination of the event-type counts ($L^b - C^b - M^s - L^a + C^a + M^b$); this paper dissects those ingredients individually.

### Signal-design takeaways

For someone building an L3 signal from order-book events:

1. **Treat event types separately.** Collapsing everything into "buy volume – sell volume" throws away structure that matters — especially the MO vs LO vs CA distinction.
2. **Tick size is the key regime.** Large-tick: a simple linear-event-weighted signal works (think OFI). Small-tick: need the gap-fluctuation correction — your signal must depend on the current book shape.
3. **Limit-order cancellations count.** A cancelled best limit order on the bid is nearly a sell market order in directional content. If you filter for executions only, you miss a third of the signal.
4. **Signed correlations tell you which events cluster with which.** Useful for designing state-conditional signals (e.g. "a MO' at the ask attracts LO' inside the spread within ~10 events" = a refill signal).
5. **Bare vs dressed matters.** If you fit a market-order-only propagator on your own data without limit-order awareness, the estimated $G$ decays in a time-scale that reflects average limit-order compensation, not true impact decay. Mis-calibrated executions follow.
