---
title: "ArXiv Second Brain"
---

# ArXiv Second Brain

## TL;DR

- **What**: a personal research wiki synthesised by Claude Opus 4.7 from arXiv papers, published as a static site. 18 papers, 42 pages, 1 mindmap.
- **Pattern**: Karpathy's three-layer LLM Wiki — raw PDFs ([Layer 1](#what-this-is)) → curated wiki pages (Layer 2) → slim schema + on-demand [skills](skills/index.md) (Layer 3).
- **Focus**: market microstructure.
- **Not RAG**: pages are pre-synthesised, opinionated, and cross-linked rather than retrieved ad-hoc from chunks — see [wiki vs RAG](#how-it-differs-from-rag).
- **Usable as LLM context**: drop a pointer in your project's `CLAUDE.md` or `AGENTS.md` and hand Claude Code / Copilot a 50 K-token distilled knowledge layer instead of 400 K of raw PDFs — see [Using the Wiki in Code](use.md).
- **Start here**: skim the [mindmap](mindmaps/market-microstructure.md) for a bird's-eye view, then drill into whichever [paper](papers/price-impact-order-book-events.md) or [concept](concepts/order-flow-imbalance.md) looks relevant.

---

A **living, compounding knowledge base** of research papers, concepts, and connections — currently anchored in market microstructure (order flow imbalance, limit-order-book dynamics, price impact, market making, optimal execution) with forays into deep learning and decentralised finance.

The wiki is the primary artifact. Every paper ingested makes it smarter. Every query that produces an insight gets filed back.

---

## What this is

This site is a personal research second brain — not a blog, not a notebook, not a paper collection. It is an opinionated, synthesised knowledge layer built on top of a raw corpus of arXiv papers.

Three layers:

1. **Layer 1 — Raw sources** (`raw/papers/`): immutable arXiv PDFs + full-text markdown conversions. The source of truth.
2. **Layer 2 — The wiki** (`wiki/`, what you're reading): LLM-generated synthesis pages organised by type (papers, concepts, methods, entities, comparisons, connections, open questions, mindmaps), wikilinked into a graph.
3. **Layer 3 — The schema + skills**: a slim always-on [schema file (CLAUDE.md)](schema.md) defines page types, frontmatter conventions, writing style, and the method-promotion rule. The LLM reads it at the start of every session. Operation-specific protocols (ingest, lint, mindmap, deploy) live in **[skills](skills/index.md)** that load on demand, keeping the always-on context small.

---

## The Karpathy inspiration

The three-layer pattern comes from **Andrej Karpathy's LLM Wiki** idea, posted publicly on X/Twitter. The core insights:

- The wiki is the **primary artifact**, not the chat log or the query interface. You read the wiki; the LLM writes it.
- The schema file ([CLAUDE.md](schema.md)) is **load-bearing**: every new LLM session starts without memory, so the schema is what keeps output structured and consistent over weeks and months.
- Synthesis is a **forcing function** — compressing a 30-page paper into a 3-page wiki page forces the model (and the reader) to actually understand it.
- Each ingest should touch **10–20 pages** so knowledge compounds rather than accumulating in isolation.

The *specific* CLAUDE.md on this site is customised for this project (quant-finance focus, Obsidian wikilinks, MkDocs + Netlify stack). The pattern is Karpathy's; the implementation is mine.

---

## How it differs from RAG

This wiki is **not** a Retrieval-Augmented Generation system. They sit at different layers.

|  | LLM Wiki (this site) | RAG |
|---|---|---|
| Primary artifact | Curated pages | Chunks in a vector DB |
| When synthesis happens | Up-front, at ingest | Never — always on-demand retrieval |
| Consumption | **Browse / read** | **Query / ask** |
| Structure | Typed pages + wikilinks | Flat chunks, no cross-references |
| Encodes judgment | Yes — pages take a view | No — returns whatever's similar |
| Compression | High — pages distill | None — verbatim chunks |
| Works without an LLM at query time | Yes (just read) | No |
| Value per paper | Compounds across pages | Adds chunks independently |

**When each wins**:

- **Wiki** is better for *"what is the state of knowledge on X?"* — a thinking agent has already synthesised it.
- **RAG** is better for *"find the exact equation in paper Y"* — it preserves detail a wiki throws away.

Mature setups combine both: RAG over the wiki (synthesised, confident answers) and RAG over the raw corpus (detail fallback).

---

## How much can this architecture hold?

Today (April 2026):

| Layer | Tokens (approx) |
|---|---|
| Wiki (this site) | ~38 K |
| Raw corpus (full text of 25 papers) | ~400 K |
| Schema (CLAUDE.md) | ~3 K |

Context: modern frontier LLMs have 1M-token windows, so the whole thing currently fits in a single prompt with ~2× headroom.

**Where this pattern scales cleanly**: up to **~50–100 papers / ~500 wiki pages** before a single-prompt approach becomes impractical and you want embeddings-based retrieval on top.

**What breaks at larger scale**:

- Context window — once raw + wiki exceed ~1M tokens, fresh LLM sessions can't read the whole thing up-front.
- Cross-page drift without a lint pass — past ~100 pages, manual consistency checking becomes archaeology.
- One global mindmap becomes illegible — you'd move to per-sub-domain mindmaps.

Karpathy's original target was personal-research scale, which is exactly where this pattern is strongest.

---

## Tech stack

| Layer | Tool |
|---|---|
| Source download / PDF → markdown | `arxiv` + `pymupdf4llm` |
| Discovery (daily arXiv sweep) | custom Python, keyword tiers in `discovery_config.py` |
| Wiki authoring (ingest, lint, mindmap, deploy) | **Claude Opus 4.7** (1M context) via Claude Code, driven by [skills](skills/index.md) |
| Local viewer | **Obsidian** — vault opens on `wiki/` directly |
| Diagrams | Mermaid (flowchart, mindmap, timeline) |
| Public site | **MkDocs Material** + **mkdocs-mermaid2-plugin** + MathJax |
| Hosting | **Netlify** |

The sync from vault to static site is done by `scripts/sync_wiki_to_mkdocs.py`, which rewrites Obsidian `[[wikilinks]]` into MkDocs-compatible relative links.

### About the skills

Each recurring operation has its own playbook loaded on demand — see [Skills](skills/index.md) for the full explanation of why the schema was split this way and how each skill works. The four current skills are [arxiv-ingest](skills/arxiv-ingest.md), [wiki-lint](skills/wiki-lint.md), [wiki-mindmap](skills/wiki-mindmap.md), and [wiki-deploy](skills/wiki-deploy.md).

---

## What's in here right now

- **18 papers** with full wiki synthesis pages — anchored in market microstructure signal design, with Chinese-market and classical foundational coverage.
- **7 more papers** sitting as full-text markdown in the raw corpus, waiting to be wiki'd next.
- **8 concept pages**, **4 method pages**, **3 entity pages**, **1 cross-domain connection page**.
- **1 per-domain mindmap** ([market microstructure](mindmaps/market-microstructure.md)) with three interactive Mermaid diagrams.
- Two orthogonal OFI conventions correctly distinguished — the *event-based* one from Cont–Kukanov–Stoikov vs the *trade-based* one in the Easley–O'Hara / Anantha–Jain tradition.
- A cross-paper tick-size finding: large-tick assets are most forecastable, converging evidence from equities (Briola et al. 2024) and crypto (Bieganowski–Ślepaczuk 2026).

---

## Navigating the wiki

- **Browse** by topic tab above (Papers / Concepts / Methods / Connections / Entities / Mind Maps).
- **Search** — press `Ctrl+K` for full-text search.
- **Graph / mindmap** — see [market-microstructure mindmap](mindmaps/market-microstructure.md) for a clickable bird's-eye view.
- **Schema** — the LLM's instruction file is at [CLAUDE.md](schema.md) if you want to replicate the pattern.

---

# Catalog

## By domain

### Machine Learning & Deep Learning
- [Attention Is All You Need](papers/attention-is-all-you-need.md) — Vaswani et al., 2017

### Quantitative Finance — Market Microstructure (OFI / OBI / Impact)
- [The Price Impact of Order Book Events](papers/price-impact-order-book-events.md) — Cont, Kukanov, Stoikov, 2010
- [How Markets Slowly Digest Changes in Supply and Demand](papers/bouchaud-farmer-lillo-propagator.md) — Bouchaud, Farmer, Lillo, 2008
- [Slow Decay of Impact in Equity Markets](papers/brokmann-slow-decay-impact.md) — Brokmann, Sérié, Kockelkoren, Bouchaud, 2014
- [Trade Arrival Dynamics and Quote Imbalance](papers/lipton-quote-imbalance.md) — Lipton, Pesavento, Sotiropoulos, 2013
- [Queue Imbalance as a One-Tick-Ahead Price Predictor](papers/gould-bonart-queue-imbalance.md) — Gould, Bonart, 2015
- [Multi-Level Order-Flow Imbalance](papers/mlofi-xu-gould-howison.md) — Xu, Gould, Howison, 2019

### Quantitative Finance — Chinese Markets
- [The Price Impact of Generalized OFI](papers/price-impact-generalized-ofi.md) — Su et al., 2021 (CSI 500)
- [Stochastic Price Dynamics in Response to OFI — CSI 300](papers/csi300-ou-levy-ofi.md) — Hu, Zhang, 2025
- [Adaptive Learning with Order Book Data — CSI 300](papers/adaptive-learning-csi300.md) — Yang, 2021

### Quantitative Finance — Forecasting, Execution, Simulation
- [Deep Limit Order Book Forecasting](papers/deep-lob-forecasting.md) — Briola, Bartolucci, Aste, 2024
- [Forecasting High Frequency OFI](papers/forecasting-high-frequency-ofi.md) — Anantha, Jain, 2024
- [Order-Flow Filtration](papers/order-flow-filtration.md) — Anantha, Jain, Maiti, 2025
- [Explainable Patterns in Crypto Microstructure](papers/explainable-crypto-microstructure.md) — Bieganowski, Ślepaczuk, 2026
- [Bridging the Reality Gap in LOB Simulation](papers/reality-gap-lob-simulation.md) — Noble, Rosenbaum, Souilmi, 2026
- [Model Predictive Control For Trade Execution](papers/mpc-trade-execution.md) — McAuliffe et al., 2026
- [Pricing and Hedging for Liquidity Provision in CFMM](papers/cfmm-liquidity-provision-pricing.md) — Risk, Tung, Wang, 2026
- [Entropic Signatures of Market Response](papers/entropic-signatures-market-response.md) — Drzazga-Szczȩśniak et al., 2026 (macro-flavoured)

## By type

**Papers (18)** — see domain groupings above.

### Concepts (8)
- [Order Flow Imbalance](concepts/order-flow-imbalance.md) — central signal for short-horizon price prediction
- [Limit Order Book](concepts/limit-order-book.md) — the mechanism and data structure underlying microstructure
- [Price Impact](concepts/price-impact.md) — how order flow moves prices
- [Market Microstructure](concepts/market-microstructure.md) — overarching domain
- [Transformer Architecture](concepts/transformer-architecture.md) — foundational DL architecture
- [Adverse Selection](concepts/adverse-selection.md) — informed vs uninformed flow; spread theory
- [Optimal Execution](concepts/optimal-execution.md) — balancing completion / impact / opportunity cost
- [Market Making](concepts/market-making.md) — LOB quoting and AMM liquidity provision unified

### Methods (6)
- [Multi-Head Attention](methods/multi-head-attention.md) — core Transformer mechanism
- [Hawkes Process](methods/hawkes-process.md) — self-exciting point process for order flow modelling
- [SHAP Values](methods/shap-values.md) — model explainability via Shapley values
- [Queue-Reactive Model](methods/queue-reactive-model.md) — Markov jump LOB simulator
- [Propagator Model (Transient Impact Kernel)](methods/propagator-model.md) — $r_t = \sum G(t-t') \cdot \varepsilon_{t'}$ framework for market impact
- [Microprice](methods/microprice.md) — queue-weighted fair-value estimator above the mid

### Entities (3)
- [Rama Cont](entities/rama-cont.md) — co-inventor of OFI
- [Sasha Stoikov](entities/sasha-stoikov.md) — co-inventor of OFI; Avellaneda-Stoikov market making model
- [Google Brain](entities/google-brain.md) — institution behind the Transformer

### Connections & Mindmaps
- [Deep Learning meets Market Microstructure](connections/deep-learning-meets-market-microstructure.md)
- [Market Microstructure Mindmap](mindmaps/market-microstructure.md)

---

## Recent additions

- **2026-04-17**: Overnight batch wiki-ingest of 8 signal-design papers (Lipton-Pesavento-Sotiropoulos, Xu-Gould-Howison MLOFI, Gould-Bonart queue imbalance, Bouchaud-Farmer-Lillo propagator, Brokmann slow-decay impact, Hu-Zhang CSI 300 OU-Lévy, Yang CSI 300 adaptive learning, Drzazga-Szczȩśniak entropic signatures). VPIN skipped — not on arXiv. **Tick-size regime theme now confirmed across 4 independent papers**.
- **2026-04-17**: Landing page rewritten with three-layer architecture explanation, Karpathy-inspiration note, RAG-vs-wiki comparison, scalability / token-count section.
- **2026-04-16**: Wiki-ingest of 3 new microstructure papers; mindmap created; site shipped to Netlify.
- **2026-04-16**: Full-text re-ingest of all 7 original papers via `pymupdf4llm`; tick-size-regime convergence surfaced.
- **2026-04-15**: Initial ingest of 7 papers — 20 wiki pages created.

---

## Contradictions & flags

- None currently detected.
- Note: "OFI" has **two distinct conventions** in this wiki. Event-based (Cont–Kukanov–Stoikov, 2010) aggregates signed queue contributions from all LOB events. Trade-based (Easley–O'Hara tradition, used by Anantha–Jain 2024/2025) is the normalised signed-trade-count imbalance. See [Order Flow Imbalance](concepts/order-flow-imbalance.md).
