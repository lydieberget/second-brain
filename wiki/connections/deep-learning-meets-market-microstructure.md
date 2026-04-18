---
title: "Deep Learning Meets Market Microstructure"
type: connection
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/1706.03762.md
  - raw/papers/2403.09267.md
  - raw/papers/2602.00776.md
tags:
  - connection
  - deep-learning
  - market-microstructure
  - limit-order-book
  - cross-domain
related:
  - concepts/transformer-architecture.md
  - concepts/limit-order-book.md
  - concepts/market-microstructure.md
  - papers/attention-is-all-you-need.md
  - papers/deep-lob-forecasting.md
  - papers/explainable-crypto-microstructure.md
confidence: medium
---

# Deep Learning Meets Market Microstructure

## The bridge

Modern deep learning — especially Transformer and CNN-based architectures — is being applied to limit order book (LOB) data to predict short-horizon mid-price direction. This connection is productive but nuanced: high ML accuracy does not automatically translate to tradeable signals.

---

## Why these domains relate

LOB mid-price prediction is a sequence modelling problem: the current state of the book, plus recent order flow history, contains information about the next price move. This maps naturally onto the strengths of deep learning:

- **Transformers** ([[concepts/transformer-architecture]]) handle sequential patterns with long-range attention.
- **CNNs** capture local patterns in the book (e.g., depth changes at adjacent price levels).
- **Gradient boosting** (CatBoost in [[papers/explainable-crypto-microstructure]]) handles tabular LOB features with good sample efficiency.

From the microstructure side, the theoretical underpinning is [[concepts/order-flow-imbalance]]: the market already tells you whether buyers or sellers are dominant — deep models can learn more complex, multi-level patterns from the same raw data.

---

## Transfer opportunities

| From ML | To Microstructure |
|---|---|
| Attention mechanisms | Identify which LOB levels and time lags matter most |
| SHAP / explainability | Validate that models learn theoretically-motivated features (OFI, spread) |
| Distributional forecasting | OFI distribution forecasts ([[papers/forecasting-high-frequency-ofi]]) |
| Self-supervised pre-training | Pre-train on LOB data across many assets before fine-tuning |

| From Microstructure | To ML |
|---|---|
| OFI as a feature | Strong, interpretable baseline to beat |
| Adverse selection theory | Informs which predictions are likely to be tradeable |
| Market regime awareness | When models should trust their signals less (flash crashes, news) |
| Operational metrics | Probability of complete transactions > raw ML accuracy |

---

## Key papers

| Paper | Contribution |
|---|---|
| [[papers/attention-is-all-you-need]] | Introduced the Transformer; enabling technology for sequence-based LOB models |
| [[papers/deep-lob-forecasting]] | Systematic benchmark of DL models on NASDAQ LOB; proposes operational evaluation metric |
| [[papers/explainable-crypto-microstructure]] | CatBoost + SHAP on crypto LOB; shows cross-asset feature stability |

---

## Tensions and open questions

- **Accuracy vs tradability**: [[papers/deep-lob-forecasting]] shows high accuracy does not guarantee trading utility. Why? Execution latency, transaction costs, adverse selection on the other side.
- **Black box vs theory**: tree models with SHAP recover microstructure theory (OFI dominant). Do Transformer attention weights also recover it?
- **Non-stationarity**: LOB microstructure evolves (market structure changes, new participants). Do DL models that train on historical data overfit to regime-specific patterns?
- **Universal LOB features**: [[papers/explainable-crypto-microstructure]] argues for portable features across crypto assets. Does this extend to equities or FX?

---

## Cross-paper convergence: tick size is the key regime variable

Two papers arriving from different angles converge on the same finding:

- **Equities (NASDAQ)** — [[papers/deep-lob-forecasting]]: classifies 15 stocks into small / medium / large-tick regimes via $\langle\sigma\rangle/\theta$. **Large-tick stocks are the most forecastable** for DL models; queues shrink before transactions, leaking directional information.
- **Crypto (Binance Futures)** — [[papers/explainable-crypto-microstructure]]: across 5 assets, high-quantile OBI SHAP value **increases monotonically with relative tick size**. A natural experiment (W/USDT spot vs perp) shows spot OBI correlates at $c = 0.94$ with the perp's implied continuous-price location within the spot spread.

Both results match the microprice intuition (Stoikov 2018): when ticks are coarse, depth asymmetry maps more directly into discrete price moves, amplifying the signal carried by OBI. **The actionable implication**: before deploying a DL-on-LOB model on a new asset, check its tick-size regime first — it is the strongest predictor of whether the model will work.

---

## Connections

- [[concepts/transformer-architecture]] — the architectural enabling technology.
- [[concepts/limit-order-book]] — the data domain.
- [[concepts/order-flow-imbalance]] — the theoretical signal DL models (should) learn.
- [[concepts/adverse-selection]] — explains when DL signals fail (high adverse selection regimes).
