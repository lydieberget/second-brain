---
title: "Attention Is All You Need"
type: paper
created: 2026-04-15
updated: 2026-04-16
sources:
  - raw/papers/1706.03762.md
tags:
  - transformer
  - attention
  - sequence-modelling
  - nlp
  - deep-learning
related:
  - concepts/transformer-architecture.md
  - methods/multi-head-attention.md
  - entities/google-brain.md
  - connections/deep-learning-meets-market-microstructure.md
confidence: high
---

# Attention Is All You Need

**Authors**: Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin
**Institution**: Google Brain / Google Research
**Year**: 2017
**arXiv**: [1706.03762](https://arxiv.org/abs/1706.03762)
**Categories**: cs.CL, cs.LG

---

## Plain-language abstract

Prior sequence-to-sequence models (used for tasks like translation) relied on recurrent networks (RNNs, LSTMs) and convolutions. This paper proposes the Transformer — a network architecture built entirely from attention mechanisms, with no recurrence or convolutions at all. The result trains faster (because it is fully parallelisable), achieves better translation quality, and generalises cleanly to other tasks.

---

## Key contributions

1. **The Transformer architecture** — encoder-decoder model built entirely on self-attention and feed-forward layers; no sequential processing step.
2. **Multi-head attention** — running $h$ attention heads in parallel, each attending to different representational subspaces, then concatenating.
3. **Scaled dot-product attention** — $\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V$, with the $\sqrt{d_k}$ scaling preventing vanishing gradients in high-dimensional spaces.
4. **Positional encodings** — sinusoidal embeddings injected into the input to give the model a sense of token order without recurrence.
5. **Training efficiency** — the fully parallel architecture trains ~10× faster than comparable RNN models at equal or better quality.

---

## Method summary

The Transformer stacks $N=6$ encoder layers and $N=6$ decoder layers. Each encoder layer has two sub-layers: a multi-head self-attention mechanism and a position-wise feed-forward network, each wrapped in a residual connection and layer normalisation. The decoder additionally has a cross-attention sub-layer attending to the encoder output. The model dimension is $d_\text{model} = 512$ with $h = 8$ attention heads ($d_k = d_v = 64$ each); the FFN inner dimension is $d_{ff} = 2048$. Input/output embeddings and the pre-softmax projection share weights (scaled by $\sqrt{d_\text{model}}$).

### Why self-attention (Section 4 argument)

The paper justifies attention over RNNs/CNNs along three axes:

| Layer | Complexity per layer | Sequential ops | Max path length |
|---|---|---|---|
| Self-attention | $O(n^2 d)$ | $O(1)$ | $O(1)$ |
| Recurrent | $O(n d^2)$ | $O(n)$ | $O(n)$ |
| Convolutional | $O(k \cdot n d^2)$ | $O(1)$ | $O(\log_k n)$ |

The **constant path length** between any two positions is the core theoretical advantage — gradients flow directly without traversing sequential steps, making long-range dependencies tractable to learn.

---

## Training setup

- **Data**: WMT 2014 EN→DE (4.5M pairs, 37K shared BPE vocab); EN→FR (36M sentences, 32K word-piece vocab). Batches of ~25K source + 25K target tokens.
- **Hardware**: 8× NVIDIA P100 GPUs. Base: 100K steps / 12h (0.4s/step). Big: 300K steps / 3.5 days (1.0s/step).
- **Optimiser**: Adam with $\beta_1=0.9$, $\beta_2=0.98$, $\epsilon=10^{-9}$ — note the **unusually high $\beta_2$**, reported to stabilise training.
- **LR schedule**: linear warmup over 4 000 steps, then inverse-square-root decay (`lrate = d_model^(-0.5) · min(step^(-0.5), step · warmup^(-1.5))`).
- **Regularisation**: residual dropout $P_\text{drop}=0.1$ (base) / $0.3$ (big, EN→DE) / $0.1$ (big, EN→FR); label smoothing $\epsilon_{ls}=0.1$.
- **Inference**: beam size 4, length penalty $\alpha=0.6$; checkpoint averaging (last 5 for base, last 20 for big).

---

## Main results

| Task | Score | Notes |
|---|---|---|
| WMT 2014 EN→DE (newstest2014) | **28.4 BLEU** | +2 BLEU over prior best ensemble |
| WMT 2014 EN→FR (newstest2014) | **41.8 BLEU** | New single-model SOTA, ¼ of previous cost |
| WSJ constituency parsing (WSJ-only) | 91.3 F1 | Outperforms BerkeleyParser (90.4) with only 40K training sentences |
| WSJ constituency parsing (semi-supervised) | 92.7 F1 | Competitive with specialist models |

Training FLOPs for EN→DE: base $3.3 \times 10^{18}$, big $2.3 \times 10^{19}$ — one to two orders of magnitude below prior SOTA ensembles.

### Ablation findings (Table 3, EN→DE dev)

- **Heads**: single-head is 0.9 BLEU worse than $h=8$; $h=32$ also degrades — sweet spot in the middle.
- **Key dim**: reducing $d_k$ below 64 hurts quality — dot-product compatibility is not trivial.
- **Dropout is critical**: $P_\text{drop}=0$ drops BLEU from 25.8 to 24.6.
- **Sinusoidal ≈ learned positional embeddings** (25.7 vs 25.8) — sinusoids chosen for extrapolation to longer sequences at inference.
- **Bigger models help**: 6-layer $d_\text{model}=1024$ big model reaches 26.4 dev BLEU / 4.33 perplexity.

---

## Limitations

- **Quadratic complexity**: self-attention is $O(n^2)$ in sequence length $n$; the paper suggests restricting attention to a neighbourhood of size $r$ (raising path length to $O(n/r)$) as future work.
- **No inherent order**: position must be injected explicitly; the model has no native sequential inductive bias.
- **Fixed-length positional encodings**: the sinusoidal scheme works but later work (RoPE, ALiBi) improves on it.
- **No systematic study at scale**: the paper does not explore scaling laws — that comes in later work (Kaplan 2020, Chinchilla 2022).

---

## Connections

- Foundation for virtually all modern LLMs: BERT, GPT, T5, and every subsequent large language model builds on this architecture. See [[concepts/transformer-architecture]].
- [[methods/multi-head-attention]] explains the core mechanism in detail.
- For LOB forecasting applications of Transformer-style models, see [[papers/deep-lob-forecasting]].
- [[entities/google-brain]] produced this paper.
