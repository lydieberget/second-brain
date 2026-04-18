---
title: "The Price Impact of Generalized Order Flow Imbalance"
type: paper
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/2112.02947.md
tags:
  - order-flow-imbalance
  - price-impact
  - market-microstructure
  - high-frequency
  - chinese-markets
related:
  - concepts/order-flow-imbalance.md
  - concepts/price-impact.md
  - concepts/limit-order-book.md
  - papers/price-impact-order-book-events.md
  - papers/forecasting-high-frequency-ofi.md
confidence: medium
---

**Institution**: School of Economics and Finance / Software Engineering, Xi'an Jiaotong University


# The Price Impact of Generalized Order Flow Imbalance

**Authors**: Yuhan Su, Zeyu Sun, Jiarong Li, Xianghui Yuan
**Year**: 2021
**arXiv**: [2112.02947](https://arxiv.org/abs/2112.02947)
**Categories**: q-fin.TR

---

## Plain-language abstract

Standard OFI (from [[papers/price-impact-order-book-events]]) assumes a fixed minimum tick size, which breaks down when stocks trade in non-minimum quotation units. This paper introduces a generalised construction that handles variable tick sizes, then applies a log-stationarisation step to produce **log-GOFI** (Generalised Stationarised OFI). On CSI 500 constituent stocks, log-GOFI dramatically outperforms the original OFI: out-of-sample $R^2$ rises from ~35–43% to ~84–86% across three time scales.

---

## Key contributions

1. **Generalised OFI construction** — extends Cont et al.'s OFI to handle non-minimum quotation units, common in Chinese equity markets.
2. **log-GOFI** — log-stationarised version of generalised OFI; combines stationarity with the generalised construction.
3. **Empirical validation on CSI 500** — 10 representative stocks at 30s, 1min, 5min scales; all show substantial improvement over vanilla OFI.
4. **Stability** — log-GOFI's explanatory power is consistently strong across all three time scales, while OFI degrades at longer scales.

---

## Motivation and method

### Why standard OFI breaks on Chinese data

Chinese stock exchanges publish **order-book snapshots every 3 seconds**, not on every event. In a 3-second window the best bid/ask can jump by **multiple ticks** (e.g., $2\delta$) — several limit-arrival / cancel cycles happen before the next observation. Standard OFI assumes within-interval price moves of at most $\delta$, so it misrepresents these multi-tick displacements.

### GOFI construction

Instead of tracking the best-price *position* and its single-tick moves, GOFI tracks the *value* of queue sizes across all price levels that participated in the optimal-price movement:

$$\text{GOFI}_n = \sum_{i=1}^{W_n^b} q^{b,i}_n - \sum_{i=1}^{W_n^b} q^{b,i-1}_n \;-\; \sum_{i=1}^{W_n^a} q^{a,i}_n + \sum_{i=1}^{W_n^a} q^{a,i-1}_n$$

where $W_n^{b/a}$ is the number of price levels the best bid/ask swept through in interval $n$, and $q^{b,i}_n$ is the queue size at the $i$-th level. This absorbs multi-tick moves cleanly.

**log variants** (from Wang et al. 2021) replace each raw $q$ with $\log q$ to reduce the heavy-tailed variance of queue sizes, giving log-OFI and log-GOFI.

### Four variants compared

| Variant | Handles multi-tick moves? | Log-stationarised? |
|---|---|---|
| OFI | no | no |
| log-OFI | no | yes |
| GOFI | yes | no |
| **log-GOFI** | **yes** | **yes** |

---

## Main results

Average $R^2$ across 10 CSI 500 stocks, out-of-sample linear regression of mid-price change on each indicator:

| Indicator | $R^2$ (30s) | $R^2$ (1min) | $R^2$ (5min) |
|---|---|---|---|
| OFI (Cont et al.) | 32.89% | 38.13% | 42.57% |
| log-OFI | 40.35% | 46.27% | 51.65% |
| GOFI | 76.37% | 77.85% | 77.36% |
| **log-GOFI** | **83.57%** | **85.37%** | **86.01%** |

**Two effects stack**:
- The **generalisation** (GOFI vs OFI) is the big lift on 3-second Chinese data — going from ~35% to ~77% R² by properly handling multi-tick moves.
- The **log stationarisation** adds a further ~8 percentage points on top.
- log-GOFI is also the most **stable across time scales**: 83 → 86% as horizon grows from 30s to 5min, whereas OFI degrades at shorter horizons where multi-tick moves dominate.

---

## Limitations

- Data is from Chinese equity markets (CSI 500) only; generalisation to other exchanges is unverified.
- Evaluation uses linear regression only; non-linear models may perform differently relative to the baseline.
- The paper focuses on a small sample of 10 stocks; broader validation would strengthen the claim.

---

## Connections

- Directly extends [[papers/price-impact-order-book-events]] by Cont, Kukanov, Stoikov.
- Both papers study [[concepts/order-flow-imbalance]] and [[concepts/price-impact]].
- For Hawkes-based OFI forecasting, see [[papers/forecasting-high-frequency-ofi]].
- For cross-asset stability of LOB features, see [[papers/explainable-crypto-microstructure]].
