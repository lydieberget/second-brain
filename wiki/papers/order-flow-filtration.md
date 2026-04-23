---
title: "Order-Flow Filtration and Directional Association with Short-Horizon Returns"
type: paper
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/2507.22712.md
tags:
  - order-flow-imbalance
  - market-microstructure
  - high-frequency
  - hawkes-process
  - emerging-markets
  - market-quality
  - regulation
related:
  - concepts/order-flow-imbalance.md
  - concepts/market-microstructure.md
  - concepts/adverse-selection.md
  - methods/hawkes-process.md
  - papers/forecasting-high-frequency-ofi.md
  - papers/price-impact-order-book-events.md
  - methods/propagator-model.md
confidence: medium
---

# Order-Flow Filtration and Directional Association with Short-Horizon Returns

**Authors**: Aditya Nittur Anantha, Shashi Jain, Prithwish Maiti
**Institution**: Indian Institute of Science / SigmaQuant Technologies / AlgoQuant Technologies
**Year**: 2025 (submitted December 2025)
**arXiv**: [2507.22712](https://arxiv.org/abs/2507.22712)
**Categories**: q-fin.TR, q-fin.CP, q-fin.GN, q-fin.ST, stat.ME

---

## Plain-language abstract

Electronic markets are flooded with transient orders (fleeting limit orders, rapid modifications, aggressive cancellations) that dilute the directional signal in **order book imbalance (OBI)**. This paper asks: can simple structural filters — order lifetime, modification count, or modification timing — sharpen the OBI–return relationship? Using **BankNifty index futures** on NSE India across three days spanning a monthly expiry cycle, the authors find that **filtering the aggregate order flow makes little difference**, but **applying the same filters to parent orders of executed trades** produces systematically stronger Hawkes cross-excitation from OBI regimes to return regimes. The framework doubles as a policy diagnostic: OBI–return association becomes a measurable proxy for market quality under regulatory schemes (India's "Persistent Noise Creator" rules) that penalise noisy order flow.

---

## Key contributions

1. **Three structural filters at the order level** (not aggregated): lifetime $T_j$, modification count $M_j$, and inter-modification time $\mathcal{M}_j$. Cancellations and trades are coupled as "exit events"; modifications handled separately.
2. **Two imbalance constructions**:
   - Order-based **OBI** (events at best quotes, all directional messages);
   - Trade-based **OBI^(T)** (signed executed trades only) — an execution-based benchmark immune to quote flicker.
3. **Three-layer diagnostic ladder** for association strength:
   - Pearson correlation between values;
   - Discretised regime alignment (9-regime OBI × 3-regime returns), with a smooth anti-diagonal directional mask ($\gamma = 0.2$);
   - Hawkes **kernel norms** from OBI regimes to return regimes (used as diagnostic, not forecast).
4. **Residualised + lagged variants**: fit univariate ARMA to each regime-count series and rerun the scores on residuals + across a grid of positive lags to isolate genuinely predictive alignment from serial co-movement.
5. **Parent-order filtration is the key finding** — applying filters to the *parents* of executed trades (not the aggregate flow) yields systematically stronger Hawkes cross-excitation norms.
6. **Policy framing**: interprets OBI–return association as a market-quality diagnostic, directly relevant to Indian regulators' 2021–22 Persistent Noise Creator surveillance on excessive modifications/cancellations.

---

## Method summary

### Data
- **BankNifty index futures**, NSE India, tick-by-tick with per-order IDs.
- **Three trading days** selected to span early / middle / late points of a monthly futures expiry cycle.

### Quantities per evaluation window $(\tau-h, \tau]$

| Symbol | Definition |
|---|---|
| $\Delta N^{b/s}$ | directional event counts |
| $\text{OBI}(\tau, h)$ | $(\Delta N^b - \Delta N^s) / (\Delta N^b + \Delta N^s)$ over all events |
| $\text{OBI}^{(T)}(\tau, h)$ | same ratio over signed *trades* only |
| $\tilde r_{(\tau-h,\tau]}$ | realised return: last-trade $-$ first-trade mid in window |

### Filters
- **Lifetime**: remove events from orders with $T_j = t_j^{(2)} - t_j^{(1)} < \bar T$.
- **Modification count**: remove events with $M_j > \bar M$.
- **Modification time**: remove orders whose last two modifications are less than a threshold apart.

Each filter applied independently. Applied twice: (i) to the aggregate event stream, producing $\text{OBI}^{(F)}$; (ii) to the parent orders of realised trades, producing a filtered trade-based imbalance.

### Scoring ladder
1. **Contemporaneous correlation**: $S^{\rho}(\mathcal{F}, \tau) = \text{corr}(\text{OBI}, \tilde r)$.
2. **Regime scores**: for each window compute regime-count vectors $Q_\tau \in \mathbb{R}^9$ (OBI) and $R_\tau \in \mathbb{R}^3$ (returns). Produces:
   - **Directional correlation score** — weighted sum of the $9\times 3$ correlation matrix via a smooth anti-diagonal mask (weights $>1$ on aligned pairs, $<1$ on misaligned, $\approx 1$ near neutral).
   - **Regression regime score** — $\sum_\tau R^2$ of OLS regression $R_\tau = \beta Q_\tau + \epsilon_\tau$.
   Both variants also computed on ARMA residuals and at positive lags.
3. **Hawkes diagnostics**: promote regime transitions to point-process events; fit a parametric multivariate Hawkes process and interpret kernel norms / branching ratios as OBI → return excitation strength.

---

## Main results

- **Aggregate-flow filtration is disappointing**: lifetime/modification filters applied to all events produce only marginal changes in Pearson correlation, regime scores, and Hawkes norms across the three days. The intuition from the fleeting-order literature does not straightforwardly translate into sharper signals when the filter is applied globally.
- **Parent-order filtration works**: the same filters, when applied only to orders that actually participated in executed trades, yield systematically **stronger Hawkes cross-excitation kernel norms** from OBI to return regimes. This holds across all three filter types and across all three trading days in the sample.
- **Interpretation**: not all trades contribute equally to price formation; trades whose parent orders survive the filters (i.e., were not fleeting or over-revised) carry more of the directional information.
- **Unfiltered BankNifty OBI is already strong** — consistent with prior literature; the paper is framed as "can filtering improve on a known-strong baseline?", and the answer is "only if you filter in the right way".
- **The paper is deliberately diagnostic**, not forecasting: no P&L or OOS forecast evaluation is claimed.

---

## Limitations

- **Single instrument**: BankNifty index futures only; equity cash, options, and cross-exchange behaviour untested.
- **Three days, expiry-structured sample**: designed to stratify by activity level, not to span a full regime set (no extreme-volatility days, no regulatory-change days).
- **Thresholds not optimised**: filter thresholds $\bar T, \bar M$ are discussed but not tuned — results are comparative across filters, not at an optimal operating point.
- **Diagnostic, not predictive**: Hawkes models are used for kernel-norm interpretation only; no out-of-sample forecast or trading evaluation.
- **Policy framing is suggestive**: the paper links OBI–return association to market-quality diagnostics under NPC rules, but stops short of causal claims about regulation effects.

---

## Connections

- Same authors' companion paper on OFI forecasting: [[papers/forecasting-high-frequency-ofi]].
- Foundational OFI framework: [[papers/price-impact-order-book-events]].
- Hawkes process methodology: [[methods/hawkes-process]].
- Core concept: [[concepts/order-flow-imbalance]].
