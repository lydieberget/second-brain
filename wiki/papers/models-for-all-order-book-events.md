---
title: "Models for the Impact of All Order Book Events"
type: paper
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/1107.3364.md
tags:
  - price-impact
  - order-book-events
  - propagator-model
  - history-dependent-impact
  - tick-size
  - liquidity-refill
related:
  - concepts/price-impact.md
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - methods/event-type-impact-decomposition.md
  - methods/propagator-model.md
  - papers/eisler-bouchaud-kockelkoren-order-book-events.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/price-impact-order-book-events.md
  - entities/jean-philippe-bouchaud.md
  - entities/zoltan-eisler.md
confidence: high
---

# Models for the Impact of All Order Book Events

**Authors**: [[entities/zoltan-eisler|Zoltán Eisler]], [[entities/jean-philippe-bouchaud|Jean-Philippe Bouchaud]], Julien Kockelkoren
**Institution**: Capital Fund Management, Paris
**Year**: 2011 (arXiv July 2011; published *Quantitative Finance*, 2012)
**arXiv**: [1107.3364](https://arxiv.org/abs/1107.3364)
**Categories**: q-fin.TR, q-fin.ST

---

## Plain-language abstract

Follow-up to the 2009 event-type decomposition paper. Where the earlier work established the machinery and showed it fits data, this paper proposes **two competing structural models** for multi-event-type impact and adjudicates between them. The **TIM (Transient Impact Model)** just generalises the market-order propagator: every event type $\pi$ has its own decaying kernel $G_\pi(\tau)$. The **HDIM (History-Dependent Impact Model)** is more principled: only *price-changing* events cause instantaneous price jumps, but the *size* of each jump depends on the past history of all six event types via an "influence matrix" $\kappa_{\pi_1, \pi'}$. The influence matrix is the quantitative handle on a well-known phenomenon: **aggressive market orders soften future impact of same-sign market orders and amplify opposite-sign impact** — the mechanism that keeps prices diffusive despite strongly autocorrelated trade signs. Empirically the TIM fits data slightly better even though HDIM is theoretically cleaner; the authors attribute this to the Gaussian factorisation approximation required to calibrate HDIM.

---

## Key contributions

1. **Two competing structural models for multi-event impact**:
   - **TIM (Transient Impact Model)**: $p_t = p_0 + \sum_{t' < t} \sum_\pi G_\pi(t-t') \cdot \epsilon_{t'} \cdot I(\pi_{t'} = \pi)$. Each event type has a bare propagator $G_\pi(\tau)$ (derived from the 2009 paper). Theoretically inconsistent: assigns non-zero impact to non-price-changing events.
   - **HDIM (History-Dependent Impact Model)**: Return at $t$ is zero unless $\pi_t$ is a price-changing event, in which case the jump $\Delta_t$ depends on past order flow via $\Delta_t = \Delta^R_\pi + \sum_{\pi_1, \ell > 0} \kappa_{\pi_1, \pi'}(\ell) \cdot \epsilon_{t-\ell} \cdot I(\pi_{t-\ell} = \pi_1)$.
2. **Equivalence condition**: TIM and HDIM coincide iff $G_\pi(\ell) - G_\pi(1) = \sum_{\ell' \leq \ell} \kappa_{\pi, \pi'}(\ell')$ — a strong structural restriction not supported by data.
3. **Empirical influence matrix $\kappa_{\pi_1, \pi'}(\ell)$** (6 × 3 = 18 kernels):
   - $\kappa_{\text{MO}', \text{MO}'} < 0$: a price-moving buy market order **reduces** the subsequent gap (on the same side) for future price-moving market orders — the book "hardens" against further aggression.
   - $\kappa_{\text{MO}^0, \pi'} > 0$: a small (non-price-moving) market order **softens** the book — gaps grow.
   - Queue events (LO⁰, CA⁰) also harden the book for small-tick stocks.
   - Large-tick stocks: $\kappa \approx 0$ (gaps are always one tick).
4. **Three-process interpretation of price dynamics**:
   - Instantaneous jumps from price-changing events.
   - Future event-rate modulation (captured by $C_{\pi_1, \pi_2}$ correlations).
   - Future jump-size modulation (captured by $\kappa_{\pi_1, \pi'}$).
5. **Verdict: TIM beats HDIM on volatility fit** despite HDIM's cleaner structure. Root cause is the Gaussian factorisation approximation used to calibrate $\kappa$ — multiplying calibrated $\kappa$ by 3 restores most of the fit. Suggests a numerically heavier but more accurate calibration is needed.
6. **Relation to VAR**: The TIM is a multi-event extension of Hasbrouck's VAR model with no direct past-return regressor. The HDIM is a VAR model with event-type-specific return equations.

---

## Method summary

### TIM (Transient Impact Model)

$$p_t \;=\; p_0 \;+\; \sum_{t' < t}\;\sum_\pi\; G_\pi(t - t') \;\cdot\; \epsilon_{t'} \;\cdot\; I(\pi_{t'} = \pi)$$

Inversion formula for $G_\pi$:

$$R_\pi(\ell) \;=\; \sum_{\pi_1}\; P(\pi_1) \sum_{\ell' = 0}^{\ell-1} G_{\pi_1}(\ell - \ell') \cdot C_{\pi, \pi_1}(\ell')$$

Numerically better to invert in terms of increments $\Delta G_\pi(\ell) = G_\pi(\ell+1) - G_\pi(\ell)$, which yields a stable block-Toeplitz system.

### HDIM (History-Dependent Impact Model)

Return at $t$:

$$r_t \;=\; \epsilon_t \cdot \Delta_t \cdot I(\pi_t = \pi')$$

where for price-changing $\pi'$ (MO', LO', CA'):

$$\Delta_t \;=\; \Delta^R_{\pi'} \;+\; \sum_{\pi_1}\;\sum_{\ell > 0}\; \kappa_{\pi_1, \pi'}(\ell) \;\cdot\; \epsilon_{t - \ell} \;\cdot\; I(\pi_{t-\ell} = \pi_1)$$

The influence matrix $\kappa_{\pi_1, \pi'}(\ell)$ is 6 event-types $\times$ 3 price-changing-event-types $\times$ lags $\ell$. Calibrated via the return-response cross-correlation $S_{\pi_1, \pi'}(\ell) = \langle r_{t+\ell} \cdot \epsilon_t I(\pi_t = \pi_1) \rangle$, under a Gaussian factorisation approximation for the three-point correlation.

### Volatility prediction

The time-lagged price diffusion $D(\ell) = \mathbb{E}[(p_{t+\ell} - p_t)^2]$ has explicit expressions in both models (Appendix A of the paper). This is the primary empirical test: a correctly-calibrated model should reproduce $D(\ell)/\ell$ at all lags.

### Data

Same as the 2009 paper: 14 NASDAQ stocks, 3 Mar – 19 May 2008. Large-tick and small-tick sub-samples handled separately. Excludes first 30 / last 40 minutes of the trading day.

---

## Main results

### Large-tick stocks

- $\kappa \approx 0$ (constant-gap limit).
- Both TIM and HDIM reduce to the constant-impact model.
- Fit to $R_\pi(\ell)$ and $D(\ell)/\ell$ is near-perfect (small residuals accounted for by gap-fluctuation correction).

### Small-tick stocks

- $\kappa$ is non-trivial and event-type-dependent.
- **TIM fits $D(\ell)/\ell$ very well at long lags** (surprisingly accurate given the model's theoretical inconsistency).
- **HDIM overshoots $D(\ell)$ by ~15%** with the naive Gaussian-factorisation calibration. Multiplying $\kappa$ by 3 restores the fit to within ~5%.
- Both models miss a small high-frequency term $D_{\text{hf}} \approx 0.04$ ticks² — attributed to limit-order placements-then-cancellations inside the gap not covered by the event-type taxonomy.

### The influence matrix $\kappa_{\text{MO}', \pi'}(\ell)$

- $\kappa_{\text{MO}', \text{MO}'} < 0$: a MO' reduces the gap for future same-sign MO'. "Hard book" after aggressive trade on the same side.
- $\kappa_{\text{MO}', \text{CA}'}$, $\kappa_{\text{MO}', \text{LO}'}$: generally also negative but smaller.
- Integrated effect: $\sum_\ell \kappa_{\pi_1, \pi'}(\ell)$ is mostly negative for price-changing events on the same side — formal confirmation of the "liquidity refill" hypothesis.
- Small market orders (MO⁰) have positive $\kappa$: they "soften" the book (gaps grow), indicating they're often followed by liquidity withdrawal or limit-order repositioning.

---

## Limitations

- **Calibration approximation error.** HDIM calibration via Eq. (19) uses a Gaussian factorisation of three- and four-point correlations. The factorisation error dominates residuals; a historical-simulation calibration would be more accurate but much more computationally expensive.
- **Linear ansatz for gap dynamics.** Only quadratic-in-$\epsilon$ terms are retained. Higher-order ($\epsilon^4$) gap responses are documented to exist but omitted.
- **L1 only.** Events deeper in the book are unobserved; their effect shows up as residual dressing of the bare impacts.
- **Multi-venue.** Same 2008 NASDAQ-only data as the 2009 paper; off-NASDAQ flow unobserved.
- **Volume-agnostic.** MO' and MO⁰ differentiate on price-moving vs not, but within each class the volume dependence is collapsed.
- **TIM theoretical inconsistency.** TIM assigns non-zero impact to non-price-changing events, which is structurally wrong. The empirical success of TIM over HDIM remains unexplained.

---

## Connections to other wiki pages

- **Direct prequel**: [[papers/eisler-bouchaud-kockelkoren-order-book-events]] — this paper's formalism and six-event-type taxonomy are inherited verbatim.
- **Method**: [[methods/event-type-impact-decomposition]] — the EBK framework both papers define; this one extends it with the HDIM formulation.
- **Parent framework**: [[methods/propagator-model]] — the market-order-only propagator is the single-event-type limit of both TIM and HDIM.
- **Relates to**: [[papers/price-impact-order-book-events]] (Cont-Kukanov-Stoikov, 2014) — a different linear combination of the same event counts (OFI) that focuses on forecasting rather than structural decomposition.
- **Relates to**: [[methods/queue-reactive-model]] — alternative, state-based framing of gap dynamics at a single level.

### Signal-design takeaways

For an L3 signal developer working from this paper:

1. **Influence matrix as a feature.** The sign-asymmetric response to past events (MO' softens future same-sign MO' impact, hardens opposite-sign) is a real state-variable signal. If you can estimate even a crude $\kappa_{\text{MO}', \text{MO}'}$ on your market, a signal conditional on "recent same-sign MO' count" has non-trivial edge.
2. **TIM is the pragmatic workhorse.** HDIM is cleaner but harder to calibrate. For production use, a multi-event-type propagator (TIM) with per-event-type kernels is a sensible baseline — HDIM-like refinements are second-order.
3. **Large-tick simplification.** If your universe is large-tick, $\kappa = 0$ is a good first approximation — the signal reduces to a linear combination of event-type counts (essentially OFI).
4. **Event-type classification matters more than volume bucketing.** The paper's binary MO / MO' split captures more of the signal than fine volume quantisation does. Similarly for LO and CA.
5. **Watch for three- and four-body effects in small-tick stocks.** Higher-order terms in the gap dynamics are known to exist; if you linearise at 2nd order and fit doesn't close, this is where to look.
