---
title: "Transformer Architecture"
type: concept
created: 2026-04-15
updated: 2026-04-15
sources:
  - raw/papers/1706.03762.md
tags:
  - transformer
  - deep-learning
  - attention
  - sequence-modelling
  - nlp
related:
  - methods/multi-head-attention.md
  - papers/attention-is-all-you-need.md
  - papers/deep-lob-forecasting.md
  - connections/deep-learning-meets-market-microstructure.md
  - entities/google-brain.md
confidence: high
---

# Transformer Architecture

## Definition

The **Transformer** is a neural network architecture introduced in [[papers/attention-is-all-you-need]] (Vaswani et al., 2017) that processes sequences using self-attention mechanisms exclusively — no recurrence, no convolutions. It is the foundation of virtually all modern large language models.

---

## Historical context

Prior to 2017, sequence modelling was dominated by RNNs and LSTMs, which process tokens sequentially and suffer from vanishing gradients on long sequences. The Transformer dispensed with sequential processing entirely, enabling full parallelism and dramatically reducing training time. It was originally proposed for machine translation but generalised far beyond NLP.

---

## How it works

### Core building block: Scaled dot-product attention

$$\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$$

Queries ($Q$), Keys ($K$), and Values ($V$) are linear projections of the input. Each token attends to all others, weighted by compatibility (dot product), scaled to prevent saturation at high dimensions.

### Multi-head attention

$h$ attention heads run in parallel, each attending to different subspaces:

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)W^O$$

This allows the model to jointly attend to information from different representational perspectives. See [[methods/multi-head-attention]] for full detail.

### Encoder-decoder structure

- **Encoder**: $N$ identical layers, each with self-attention + feed-forward sub-layers, residual connections, and layer normalisation.
- **Decoder**: $N$ layers with masked self-attention (causal), cross-attention to encoder outputs, and feed-forward sub-layers.

### Positional encodings

Since attention is permutation-invariant, position information is injected via sinusoidal embeddings added to the input:

$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_\text{model}})$$
$$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_\text{model}})$$

---

## Key properties

| Property | Value |
|---|---|
| Sequential processing | None — fully parallelisable |
| Attention complexity | $O(n^2 d)$ in sequence length $n$ |
| Inductive bias | Minimal — learns relationships from data |
| Context window | Bounded by quadratic cost; extended by variants (Flash Attention, etc.) |

---

## Descendants

- **BERT** (2018): bidirectional encoder-only Transformer; pre-trained by masked language modelling.
- **GPT** (2018–present): decoder-only Transformer; autoregressive.
- **T5** (2019): encoder-decoder; framed all NLP tasks as text-to-text.
- **Vision Transformer (ViT)** (2020): applied to image patches.
- **Temporal Fusion Transformer**: time-series adaptation.
- **TransLOB**: applied to LOB prediction — see [[papers/deep-lob-forecasting]].

---

## Open questions

- Can Transformers achieve true causal reasoning, or are they sophisticated pattern matchers?
- How do positional encodings best generalise to long sequences? (active area: RoPE, ALiBi, etc.)
- What is the minimal architecture needed for in-context learning?

---

## Connections

- Introduced in [[papers/attention-is-all-you-need]].
- Core mechanism: [[methods/multi-head-attention]].
- Applied to LOB prediction: [[papers/deep-lob-forecasting]].
- Produced by [[entities/google-brain]].
- [[connections/deep-learning-meets-market-microstructure]] explores how Transformer-style models apply to finance.
