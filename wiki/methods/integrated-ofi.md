---
title: "Integrated OFI"
type: method
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/2112.13213.md
tags:
  - order-flow-imbalance
  - pca
  - dimensionality-reduction
  - multi-level-lob
  - signal-design
related:
  - concepts/order-flow-imbalance.md
  - concepts/limit-order-book.md
  - papers/cross-impact-ofi-equity-markets.md
  - papers/mlofi-xu-gould-howison.md
  - papers/price-impact-generalized-ofi.md
  - concepts/cross-impact.md
  - concepts/price-impact.md
confidence: high
---

# Integrated OFI

## Definition

**Integrated OFI** is a single scalar signal that aggregates order-flow imbalance across the top $M$ levels of the limit order book. It is constructed as the first principal component of the multi-level OFI vector, normalised so the weights sum to 1. Introduced by Cont, Cucuringu & Zhang (2023) as the base feature for contemporaneous and predictive impact models.

Formally, for stock $i$ and interval $(t-h, t]$:

$$
\text{ofi}^I_{i,t,h} \;=\; \langle \tilde{\mathbf{w}}_1, \;\mathbf{of}^{(h)}_{i,t}\rangle, \qquad \tilde{\mathbf{w}}_1 \;=\; \frac{\mathbf{w}_1}{\|\mathbf{w}_1\|_1}
$$

where $\mathbf{w}_1$ is the first principal vector of the depth-scaled multi-level OFI vector $\mathbf{of}^{(h)}_{i,t} = (\text{ofi}^1_{i,t,h}, \ldots, \text{ofi}^M_{i,t,h})^T$, computed from historical minute-level data.

---

## Construction algorithm

1. **Compute per-level OFIs.** For each level $m = 1, \ldots, M$:

   $$\text{OF}^{m,b}_{i,n} = \begin{cases} q^{m,b}_{i,n} & \text{if } P^{m,b}_{i,n} > P^{m,b}_{i,n-1} \\ q^{m,b}_{i,n} - q^{m,b}_{i,n-1} & \text{if } P^{m,b}_{i,n} = P^{m,b}_{i,n-1} \\ -q^{m,b}_{i,n-1} & \text{if } P^{m,b}_{i,n} < P^{m,b}_{i,n-1} \end{cases}$$

   Symmetrically for the ask side. Sum over events $n$ in the interval, subtract ask from bid, and scale by the average top-$M$ depth $Q^{M,h}_{i,t}$ to neutralise intraday depth patterns.

2. **Stack into vector.** $\mathbf{of}^{(h)}_{i,t} = (\text{ofi}^1_{i,t,h}, \ldots, \text{ofi}^M_{i,t,h})^T \in \mathbb{R}^M$.

3. **Fit PCA on historical data.** Using minute-level observations across a chosen calibration window, compute the first principal component $\mathbf{w}_1 \in \mathbb{R}^M$ of the empirical covariance of $\mathbf{of}^{(h)}$.

4. **Normalise.** $\tilde{\mathbf{w}}_1 = \mathbf{w}_1 / \|\mathbf{w}_1\|_1$ so the scalar retains OFI-like units and the weights sum to 1.

5. **Project.** For any future $(t, h)$: $\text{ofi}^I_{i,t,h} = \tilde{\mathbf{w}}_1^T \mathbf{of}^{(h)}_{i,t}$.

In the original paper $M = 10$ and the calibration is refreshed on a rolling basis (implicitly through the 30-minute re-estimation windows of the downstream regressions).

---

## Why PCA-normalised aggregation?

**The problem.** Multi-level OFIs are highly collinear — pairwise correlations across levels exceed 75% in the Nasdaq-100 sample. A plain OLS with 10 OFI features is numerically unstable and most coefficients are statistically indistinguishable from zero.

**The resolution.** The first PC captures **>89%** of total variance (std 6%) in the 10-OFI covariance matrix (Cont-Cucuringu-Zhang, Table 2), while the remaining components contribute <5% each. Collapsing onto the first PC retains almost all signal with $10\times$ dimensionality reduction.

**The $\ell_1$ normalisation** $\|\mathbf{w}_1\|_1 = 1$ is a normalisation choice, not a constraint on the fit — it ensures the resulting scalar has interpretable units (a convex combination of per-level OFIs) and is directly comparable with the per-level OFIs at the same scale.

---

## Empirical weight structure

The first principal component weights show:

- **Lowest weight on best-level OFI**, highest standard deviation across stocks — the top-of-book is the most idiosyncratic level.
- **Deeper levels (2–3) receive most weight on average** — consistent with evidence that depth at levels 2–3 often exceeds depth at level 1 (Hautsch-Huang, Chakrabarty et al.).
- **Stock-characteristic dependence**:
  - *High-volume* stocks: deeper-level OFIs dominate the PC weights.
  - *Low-volatility* stocks: same — deeper OFIs win.
  - *Low-volume / large-spread* stocks: best-level OFI weight rises.

This suggests that for actively traded liquid names, the useful signal is not where the order book starts but where institutional flow parks itself.

---

## Performance (from [[papers/cross-impact-ofi-equity-markets|Cont, Cucuringu, Zhang 2023]])

| Feature | Model | IS $R^2$ | OOS $R^2$ |
|---|---|---|---|
| Best-level OFI | PI¹ | 71.16% | 64.64% |
| Integrated OFI | PIᴵ | **87.14%** | **83.83%** |

A +16–20 point $R^2$ jump from a single aggregation step.

---

## When to use / when not to

**Use integrated OFI when:**
- You want a single feature that captures most multi-level information for minute-resolution impact modelling.
- You're running a linear / penalised linear regression and want to avoid collinearity headaches from raw multi-level OFIs.
- Interpretability matters (weights are a convex combination of per-level OFIs).

**Don't use when:**
- You need horizon-specific level information. The PC collapse loses which level is "doing the work" — for questions about strategic order placement, use per-level OFIs directly.
- Your data window is too short to estimate a stable first PC (need at least several hundred minute bars per stock).
- You're training a deep model that can absorb the raw multi-level vector — DNNs may benefit from the extra dimensions ([[papers/price-impact-generalized-ofi|Kolm-Turiel-Westray]]).

---

## Variants

| Aggregation | Source | Notes |
|---|---|---|
| Integrated OFI (PCA, $\ell_1$-norm) | [[papers/cross-impact-ofi-equity-markets]] | Default recommendation; variance-weighted across levels |
| Multi-level OFI vector (no aggregation) | [[papers/mlofi-xu-gould-howison]] | Preserves level info; used as input to deep models |
| log-GOFI | [[papers/price-impact-generalized-ofi]] | Log-transform for non-minimum-tick stocks; generalised to R² ~84% on CSI 500 |
| Equal-weighted multi-level OFI | Baseline (not recommended) | Ignores that best-level is idiosyncratic |

---

## Implementation notes

- **Scale before PCA**: divide each $\text{OF}^{m,\cdot}_{i,n}$ by $Q^{M,h}_{i,t}$ (average depth across the top $M$ levels in the interval) before forming the vector. Not doing this bakes intraday depth patterns into the PC weights.
- **Cross-sectional or stock-specific PC?** The original paper fits the PC cross-sectionally per stock, not globally. Globally-fitted PCs are more stable but may lose stock-idiosyncratic level structure.
- **Refresh frequency**: the paper rolls the calibration with the 30-min regression window. A much longer window (e.g. one day) would bias against recent regime changes; much shorter is noisy.

---

## Connections

- [[concepts/order-flow-imbalance]] — integrated OFI is a variance-maximising aggregation of the per-level OFI vector.
- [[concepts/limit-order-book]] — inputs come from multi-level LOB snapshots.
- [[methods/propagator-model]] — orthogonal approach: propagator is a per-event kernel, integrated OFI is a per-snapshot aggregation.
- [[papers/cross-impact-ofi-equity-markets]] — paper that introduced this method.
- [[papers/mlofi-xu-gould-howison]] — the vector form ("MLOFI") this aggregation was built over.
