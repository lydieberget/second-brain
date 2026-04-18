---
title: "Multi-Head Attention"
type: method
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/1706.03762.md
tags:
  - transformer
  - attention
  - deep-learning
  - nlp
related:
  - concepts/transformer-architecture.md
  - papers/attention-is-all-you-need.md
  - papers/deep-lob-forecasting.md
confidence: high
---

# Multi-Head Attention

## Algorithm description

**Multi-head attention** runs $h$ scaled dot-product attention operations in parallel, each operating on a different linear projection of the input. The outputs are concatenated and projected back to the model dimension.

Given input matrices (or sequences) $X$, compute $h$ "heads":

$$\text{head}_i = \text{Attention}(XW_i^Q,\; XW_i^K,\; XW_i^V)$$

where each $W_i^Q \in \mathbb{R}^{d_\text{model} \times d_k}$, $W_i^K \in \mathbb{R}^{d_\text{model} \times d_k}$, $W_i^V \in \mathbb{R}^{d_\text{model} \times d_v}$.

The scaled dot-product attention for each head:

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Then:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\, W^O$$

where $W^O \in \mathbb{R}^{hd_v \times d_\text{model}}$.

---

## Key equations

**Scaling**: The $\frac{1}{\sqrt{d_k}}$ factor prevents dot products from growing large in high dimensions, which would saturate the softmax and cause near-zero gradients.

**Typical hyperparameters** (from [[papers/attention-is-all-you-need]]):
- Base: $d_\text{model} = 512$, $h = 8$, $d_k = d_v = 64$
- Big: $d_\text{model} = 1024$, $h = 16$, same $d_k = d_v = 64$
- Total parameters per attention layer: $4 d_\text{model}^2$

**Ablation evidence** (Vaswani et al., Table 3):
- Single-head attention scores 0.9 BLEU worse than $h=8$; $h=32$ also degrades.
- Reducing $d_k$ below 64 hurts quality — dot-product compatibility is not trivially learnable.
- The sweet spot is "enough heads to diversify subspaces, not so many that each head loses capacity".

---

## Computational complexity

| Dimension | Cost |
|---|---|
| Time (per layer) | $O(n^2 d)$ — quadratic in sequence length $n$ |
| Space | $O(n^2)$ for attention weight matrix |
| Compared to RNN | RNN is $O(nd^2)$ but sequential; Transformer is parallelisable |

---

## When to use / when not to use

**Use when:**
- Modelling long-range dependencies in sequences.
- Full parallelism during training is desirable.
- Sufficient data to learn attention patterns from scratch.

**Avoid or adapt when:**
- Sequences are very long (>10k tokens): $O(n^2)$ becomes prohibitive. Use Flash Attention, linear attention variants, or sliding-window attention.
- Low-data regime: the minimal inductive bias of attention may cause overfitting.

---

## Implementations

- **PyTorch**: `torch.nn.MultiheadAttention`
- **HuggingFace Transformers**: standard in all Transformer models
- **Flash Attention** (Dao et al., 2022): IO-efficient implementation; same output, faster for long sequences

---

## Papers that introduced or improved it

- Introduced: [[papers/attention-is-all-you-need]] (Vaswani et al., 2017)
- Flash Attention: Dao et al. (2022) — GPU-efficient implementation
- Applied to LOB: [[papers/deep-lob-forecasting]] (TransLOB and related models)

---

## Connections

- Central to [[concepts/transformer-architecture]].
- Used in LOB forecasting models evaluated in [[papers/deep-lob-forecasting]].
