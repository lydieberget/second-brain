---
title: "SHAP Values"
type: method
created: 2026-04-15
updated: 2026-04-15
sources:
  - raw/papers/2602.00776.md
tags:
  - explainability
  - machine-learning
  - shap
  - feature-importance
related:
  - papers/explainable-crypto-microstructure.md
  - concepts/market-microstructure.md
confidence: high
---

# SHAP Values (SHapley Additive exPlanations)

## Algorithm description

**SHAP** is a model-agnostic explainability framework based on Shapley values from cooperative game theory. It assigns each input feature a contribution to a specific model prediction, satisfying desirable axioms (efficiency, symmetry, dummy, additivity).

For a prediction $f(x)$, the SHAP value for feature $i$ is:

$$\phi_i = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|!\,(|F|-|S|-1)!}{|F|!} \left[f_{S \cup \{i\}}(x_{S \cup \{i\}}) - f_S(x_S)\right]$$

where $F$ is the set of all features and $f_S$ is the model restricted to feature subset $S$ (other features marginalised out).

In practice, exact Shapley values are exponential to compute. Model-specific approximations are used:
- **TreeSHAP**: exact and polynomial-time for tree-based models (XGBoost, CatBoost, LightGBM).
- **KernelSHAP**: model-agnostic approximation for any model.
- **LinearSHAP**: exact for linear models.

---

## Key equations

**Additive decomposition**: SHAP values decompose the prediction as:

$$f(x) = E[f(X)] + \sum_{i=1}^{p} \phi_i(x)$$

Each $\phi_i$ is the average marginal contribution of feature $i$, weighted over all possible feature coalitions.

---

## Computational complexity

| Method | Complexity | Notes |
|---|---|---|
| Exact Shapley | $O(2^p)$ | Infeasible for large $p$ |
| TreeSHAP | $O(T L D^2)$ | $T$ trees, $L$ leaves, $D$ depth — fast in practice |
| KernelSHAP | $O(p^2 n_\text{samples})$ | Approximate; slower |

---

## Use in this wiki

[[papers/explainable-crypto-microstructure]] uses TreeSHAP with CatBoost to explain LOB feature contributions to short-horizon return predictions. Key finding: SHAP importances and dependence shapes are stable across BTC, LTC, ETC, ENJ, and ROSE despite very different market cap and liquidity. The dominant features are OFI, bid-ask spread, and depth ratios — consistent with microstructure theory.

---

## When to use / when not to use

**Use when:**
- You need consistent, theoretically-grounded feature importance (not permutation importance, which can be misleading).
- You want per-prediction explanations, not just global feature rankings.
- Debugging a tree-based model (TreeSHAP is fast).

**Caution:**
- SHAP values measure correlation, not causality.
- Correlated features can share SHAP mass unpredictably.
- "Stable SHAP importances across assets" does not imply the same causal mechanism; it implies similar correlational structure.

---

## Implementations

- **shap** (Python): `shap.TreeExplainer`, `shap.KernelExplainer`
- Built into XGBoost, LightGBM, CatBoost natively.

---

## Connections

- Applied in [[papers/explainable-crypto-microstructure]] to crypto LOB models.
- Feature importance informs [[concepts/order-flow-imbalance]] theory: SHAP confirms OFI is the dominant signal.
