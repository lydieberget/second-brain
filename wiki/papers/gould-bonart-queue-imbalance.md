---
title: "Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit Order Book"
type: paper
created: 2026-04-17
updated: 2026-04-17
sources:
  - raw/papers/1512.03492.md
tags:
  - queue-imbalance
  - order-book-imbalance
  - logistic-regression
  - nasdaq
  - tick-size
  - signal-design
  - limit-order-book
related:
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - methods/microprice.md
  - papers/lipton-quote-imbalance.md
  - papers/mlofi-xu-gould-howison.md
  - papers/price-impact-order-book-events.md
confidence: high
---

# Queue Imbalance as a One-Tick-Ahead Price Predictor in a Limit Order Book

**Authors**: Martin D. Gould, Julius Bonart
**Institution**: CFM–Imperial Institute of Quantitative Finance, Imperial College London
**Year**: 2015 (December 2015)
**arXiv**: [1512.03492](https://arxiv.org/abs/1512.03492)
**Categories**: q-fin.TR

---

## Plain-language abstract

Does the **queue imbalance** at the best bid/ask genuinely forecast the direction of the next mid-price move? Despite widespread practitioner use of this signal, rigorous quantification of its predictive power had been limited. This paper fits **logistic regressions** of mid-price direction on queue imbalance for 10 liquid Nasdaq stocks over 2014. All 10 are strongly statistically significant. vs a "no-signal" null, the logistic model improves binary direction classification by **50–60% for large-tick stocks** and **10–30% for small-tick stocks**; probabilistic predictions improve by 20–30% and 2–6% respectively. **Local logistic regression** (semi-parametric) marginally improves on the global fit but at much higher compute cost.

---

## Key contributions

1. **Rigorous baseline for the queue-imbalance signal**:

   $$I(t) = \frac{n^b(b(t), t) - n^a(a(t), t)}{n^b(b(t), t) + n^a(a(t), t)} \in [-1, 1]$$

   where $n^b, n^a$ are the total queue sizes at best bid/ask.

2. **Two-model evaluation framework**:
   - **Binary classifier** — logistic regression of $\text{sgn}(\Delta m)$ on $I$.
   - **Probabilistic classifier** — $P(\Delta m > 0 \mid I)$ via the logistic sigmoid.

3. **Formal out-of-sample evaluation** across 10 Nasdaq stocks, 2014 — first paper to quantify QI's predictive power with full LOBSTER data at event-by-event resolution under a proper null.

4. **Local (non-parametric) logistic regression** as a semi-parametric counterpart that relaxes the logistic-sigmoid shape constraint. Reveals that the true conditional direction probability is **flatter in the tails** than the sigmoid implies for small-tick stocks — suggesting tick-size-specific functional forms.

5. **Tick-size dependence**: large-tick vs small-tick stocks show **very different** magnitudes of predictive improvement. Large-tick improvements are ~2–3× the small-tick improvements, consistent with the thesis that large-tick LOBs concentrate predictive information at the top of book.

---

## Method summary

### Data
- **LOBSTER** full event stream for **10 Nasdaq stocks** spanning tick-size regimes.
- Entire calendar year **2014** — 252 trading days.
- Trading hours filtered to **10:00–15:30 ET** (exclude opening/closing 30-min auctions).
- Tick size $\pi = \$0.01$ (constant across Nasdaq names); **relative tick size** $\pi / \text{price}$ drives the regime classification.

### Inputs & target
- Input $I$ computed at every change in best bid or ask (event time, not calendar time).
- Target: sign of the next mid-price change (binary) or probability that next change is upward (probabilistic).

### Models

$$\Pr(\Delta m > 0 \mid I) = \sigma(\alpha + \beta I) \qquad \sigma(x) = \frac{1}{1 + e^{-x}}$$

- **Global logistic regression**: one $(\alpha, \beta)$ per stock.
- **Local logistic regression**: kernel-weighted logistic regression evaluated at each prediction point; trades parametric rigidity for computational cost.

### Null model
Random guess biased by the unconditional up-frequency — the baseline any non-trivial predictor must beat.

---

## Main results

### Binary classification (accuracy vs null)

| Tick regime | Global logistic | Local logistic |
|---|---|---|
| Large-tick | **+50–60%** | slightly better |
| Small-tick | **+10–30%** | slightly better |

### Probabilistic classification (log-loss / calibration vs null)

| Tick regime | Global logistic | Local logistic |
|---|---|---|
| Large-tick | **+20–30%** | slightly better |
| Small-tick | **+2–6%** | slightly better |

- **All 10 stocks** reject the null at high statistical significance — QI is genuinely predictive.
- **Local logistic wins marginally** but cost-per-sample is orders of magnitude higher; rarely worth it in practice.
- **Large-tick dominance** echoes the finding seen across the wiki: large-tick LOBs concentrate predictive information at the best quotes.

---

## Limitations

- **Single country, single venue**: Nasdaq 2014. Cross-venue / cross-country robustness not tested.
- **Linear feature only**: only $I$ is used; multi-level imbalance ([[papers/mlofi-xu-gould-howison]]) not combined here.
- **Sigmoid shape constraint** shown to be restrictive for small-tick stocks — but the paper doesn't try other parametric forms (e.g., piecewise-linear, tanh-like with different scale).
- **Static fit**: no regime-aware fitting across intraday periods or volatility regimes.
- **No trading simulation**: predictive accuracy only; no P&L after costs.

---

## Connections

- **Sister paper to [[papers/lipton-quote-imbalance]]**: Lipton–Pesavento–Sotiropoulos (2013) model the same queue-imbalance signal via a diffusive queue process and derive a closed-form $P_\uparrow(q^b, q^a) = \phi / \varpi$. Gould–Bonart here take the empirical/econometric route and fit logistic regressions. Together these two give a theoretical-model + empirical-regression pair on the exact same signal.
- **Distinct from [[concepts/order-flow-imbalance|OFI]]**: QI is the **instantaneous ratio** of queue sizes at best bid/ask; OFI is the **cumulative sum of signed event contributions** over an interval. Both are short-horizon LOB signals; QI is simpler to compute but discards event-time structure.
- **Multi-level sibling [[papers/mlofi-xu-gould-howison]]** by the same Gould (co-author) extends QI-style thinking to multiple price levels; the tick-size magnitudes (65–75% / 15–30% for MLOFI vs 50–60% / 10–30% here) are remarkably consistent.
- **Tick-size regime theme**: now confirmed across **four papers** in the wiki — Briola (2024), Bieganowski–Ślepaczuk (2026), Xu–Gould–Howison (2019), and this. The large-tick/small-tick divide is the single most robust cross-study finding in the microstructure cluster.
- **Stoikov microprice** builds directly on QI: microprice $= m + f(I)$ with $f$ fit from local dynamics. The Gould–Bonart local logistic regression is exactly a non-parametric estimator of Stoikov's adjustment function.
