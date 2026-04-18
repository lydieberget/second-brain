# Wiki Operation Log

Chronological record of all ingest, lint, and build operations.

---

## 2026-04-18 — CLAUDE.md split into skills; public Skills section added

### Rationale

CLAUDE.md had grown to ~5.4 K tokens and was loaded into every conversation whether relevant or not (casual question → still paying for full INGEST/LINT/MINDMAP/DEPLOY protocols). Split the operation-specific content into four Claude Code skills; kept identity / directory / page conventions / writing style / method-promotion rule in the slim CLAUDE.md.

### Files created

- `.claude/skills/arxiv-ingest/SKILL.md` — INGEST protocol (download, convert, paper page, method promotion, concept updates, cross-connections, log).
- `.claude/skills/wiki-lint/SKILL.md` — LINT protocol (orphans, broken wikilinks, thin pages, missing methods, contradictions, index/log sync).
- `.claude/skills/wiki-mindmap/SKILL.md` — MINDMAP protocol (three-diagram layout, clickable flowchart, JSON triples).
- `.claude/skills/wiki-deploy/SKILL.md` — DEPLOY protocol (sync → build → preview → Netlify, troubleshooting checklist).

### Public visibility

- `wiki/skills/index.md` — new explainer page for site visitors: why skills, what moved where, how "forced" invocation works via CLAUDE.md imperatives, token savings, how to read the four skills.
- `wiki/skills/arxiv-ingest.md`, `wiki-lint.md`, `wiki-mindmap.md`, `wiki-deploy.md` — verbatim copies of the SKILL.md files, so visitors can see exactly what instructions drive each operation.
- `site/mkdocs.yml` — added "Skills" nav section.
- `wiki/index.md` — landing page updated to point to Skills; tech-stack table refreshed.
- `wiki/schema.md` — prepended intro explaining the split and pointing to Skills.

### CLAUDE.md before vs after

| | Before | After |
|---|---|---|
| Lines | 455 | 186 |
| Approx tokens | ~5.4 K | ~2.2 K |
| Content | Identity + dir + conventions + INGEST + QUERY + LINT + MINDMAP + arxiv-script spec + mkdocs spec + netlify spec | Identity + dir + conventions + method-promotion rule + skill invocation table |

Savings per turn: ~3 K tokens. Per-ingest: neutral (skill body loads then), but skill content is more complete than the replaced CLAUDE.md section.

### Enforcement model

CLAUDE.md now explicitly tables: trigger phrase → skill to invoke. Strong imperative: *"you MUST invoke the corresponding skill before reading files or editing anything"*. Not a hook, so not literally enforced — but gets ~95% compliance with good framing. A settings.json hook could close the remaining gap if compliance drifts.

### Summary
- Pages created: 5 (4 skill copies + skills/index.md).
- Pages updated: 3 (index.md, schema.md, log.md).
- Files created outside wiki: 4 SKILL.md files in `.claude/skills/`.
- Wiki total: 18 papers, 42 pages.

---

## 2026-04-18 — Method-page backfill + CLAUDE.md method-promotion rule

Audit of the 2026-04-17 signal-design batch revealed a compliance failure: 8 papers ingested, only ~1.2 wiki pages touched per paper (vs CLAUDE.md's 10–20 target). Methods referenced inside paper pages (propagator, microprice, etc.) were not promoted to dedicated `wiki/methods/*.md` pages.

### CLAUDE.md updated

Added a **Method-promotion rule** to the INGEST operation:
- When a paper introduces or centrally uses a named formula / technique, create a dedicated method page.
- Promotion signal: ≥2 papers reference it, or the paper's contribution is primarily *defining* the method, or a reader searching "how does X work?" would expect a standalone page.
- Compliance check before marking ingest complete: enumerate methods, confirm a page exists for each, log explicitly.

### Method pages created

- **`methods/propagator-model.md`** — transient impact kernel $r_t = \sum G(t-t') \varepsilon_{t'} + \eta_t$. Formula, functional forms (power-law / stretched-exp / exp / multivariate Hawkes), self-consistency with long-memory order flow, deconvolution method, complexity, when to use / avoid. Referenced by BFL 2008, Brokmann 2014, Reality Gap 2026, Order-Flow Filtration 2025, CSI 300 OU-Lévy 2025.
- **`methods/microprice.md`** — queue-weighted fair-value estimator. Basic formula $p_\text{micro} = (q^a p^b + q^b p^a)/(q^a + q^b)$ and Stoikov's Markov-chain refinement. Properties, tick-size dependence, complexity, references to Stoikov 2018 (non-arXiv). Referenced by Lipton 2013, Gould-Bonart 2015, Reality Gap 2026, Crypto Microstructure 2026, CFMM 2026.

### Paper pages updated (frontmatter `related:` + wikilinks)

- `papers/bouchaud-farmer-lillo-propagator.md` — added `methods/propagator-model` + inline wikilink.
- `papers/brokmann-slow-decay-impact.md` — added `methods/propagator-model`.
- `papers/reality-gap-lob-simulation.md` — added `methods/propagator-model`, `methods/microprice`.
- `papers/lipton-quote-imbalance.md` — added `methods/microprice`.
- `papers/gould-bonart-queue-imbalance.md` — added `methods/microprice`.
- `papers/explainable-crypto-microstructure.md` — added `methods/microprice`.
- `papers/cfmm-liquidity-provision-pricing.md` — added `methods/microprice`.

### Summary
- Pages created: 2 (method pages).
- Pages updated: 7 paper pages (frontmatter backlinks) + CLAUDE.md.
- Methods directory now: 6 (up from 4).
- Wiki total: 18 papers, 37 pages.

### Still deferred / candidates for future method pages
- `methods/impact-deconvolution.md` — could fold into propagator, or stand alone if Brokmann-style technique grows in prominence.
- `methods/ridge-regression-lob.md` — methodological point from Xu-Gould-Howison but probably too narrow for its own page.
- `methods/shannon-entropy-markets.md` — from the entropic-signatures paper; borderline relevance.
- `methods/ou-levy-process.md` — from Hu-Zhang CSI 300; could be useful if more OU-based impact papers arrive.

---

## 2026-04-17 — Signal-design batch: 8 papers wiki'd (including 2 Chinese-market)

Overnight batch run focused on microstructure **signal design with explicit formulas**, per user request. Identified candidates via arXiv search filtered to q-fin primary categories + microstructure keywords with strict word-boundary acronym matching (the bug-fixed `fetch_daily.py`).

### Papers ingested

**Chinese-market signal-design (2)**:

- **2505.17388** — Hu & Zhang (2025) — "Stochastic Price Dynamics in Response to OFI: Evidence from CSI 300 Index Futures". Models OFI response as OU process driven by Lévy jumps; derives quasi-Sharpe "response ratio". 1 year of CSI 300 tick data (~6M ticks). Page: `papers/csi300-ou-levy-ofi.md`.
- **2103.00264** — Yang (2021) — "Adaptive Learning Approach with Order Book Data". Adaptive ARIMA framework for OBI + OFI on CSI 300 Futures with rolling-ADF diagnostics. Page: `papers/adaptive-learning-csi300.md`.

**Classical signal-design with formulas (6)**:

- **1312.0514** — Lipton, Pesavento, Sotiropoulos (2013) — "Trade Arrival Dynamics and Quote Imbalance". 2D/3D diffusion model for bid/ask queues + trade arrival; closed-form up-tick probability $P(\phi) = \phi/\varpi$ via polar transform; documents ~60% loss of theoretical spread capture in passive fills. Page: `papers/lipton-quote-imbalance.md`.
- **1907.06230** — Xu, Gould, Howison (2019) — "Multi-Level Order-Flow Imbalance". Extends CKS OFI to per-price-level vector MLOFI; shows Ridge regression overturns CKS's Appendix-B3 "depth doesn't help" conclusion; **65-75% OOS RMSE improvement for large-tick stocks**, 15-30% for small-tick. Page: `papers/mlofi-xu-gould-howison.md`.
- **1512.03492** — Gould, Bonart (2015) — "Queue Imbalance as a One-Tick-Ahead Price Predictor". Logistic regression on QI, 10 Nasdaq stocks 2014; 50-60% binary-classification improvement for large-tick, 10-30% for small-tick. Page: `papers/gould-bonart-queue-imbalance.md`.
- **0809.0822** — Bouchaud, Farmer, Lillo (2008) — "How Markets Slowly Digest Changes in Supply and Demand". Foundational review of market impact; propagator formulation $r_t = \sum G(t-t') \varepsilon_{t'} + \eta_t$; long-memory order flow; square-root law; Glosten-Milgrom + MRR reviews. Page: `papers/bouchaud-farmer-lillo-propagator.md`.
- **1407.3390** — Brokmann, Sérié, Kockelkoren, Bouchaud (2014) — "Slow Decay of Impact in Equity Markets". Deconvolution of meta-order impact using CFM proprietary data + prediction signals; shows mechanical impact decays to zero after deconvolution; the observed ~2/3 plateau in raw data is an artefact of autocorrelated order flow. Page: `papers/brokmann-slow-decay-impact.md`.
- **2603.12040** — Drzazga-Szczȩśniak et al. (2026) — "Entropic Signatures of Market Response under Concentrated Policy Communication". Scope mismatch flagged: operates at equity-index level, not LOB microstructure. Still ingested as a reference for information-theoretic signal design (Shannon entropy, cumulative entropy) that could be ported to LOB features in future. Page: `papers/entropic-signatures-market-response.md`.

### Ingest errors encountered

Three arXiv IDs I had initially were **wrong papers**:

- `1605.07076` — turned out to be math/RT ("Intégrales orbitales sur GL(N, F_q((t)))"). Correct Gould-Bonart paper is `1512.03492` (now ingested).
- `0903.0192` — turned out to be math/CO ("Generalized Road Coloring Problem"). Correct Bouchaud-Farmer-Lillo propagator paper is `0809.0822` (now ingested).
- `1301.3228` — turned out to be cond-mat ("Stress- and temperature-dependent hysteresis in solid helium"). The **Easley-López de Prado-O'Hara VPIN** paper is not on arXiv (published in *Review of Financial Studies* 2012); would need Semantic Scholar or SSRN retrieval.

Also noted earlier: `1906.07762` ≠ Sirignano-Cont 2019; that paper appears not to be on arXiv directly either.

**Remediation**: going forward, always verify arxiv ID → title match before treating a batch file as authoritative. The `fetch_daily.py` discovery path avoids this entirely since it searches arxiv directly.

### Cross-paper themes surfaced

1. **Tick-size regime is the single most robust finding in the microstructure cluster**. Now four independent papers confirm that large-tick stocks concentrate more predictive information at the top of book than small-tick: [[papers/deep-lob-forecasting]] (Briola 2024, DL on NASDAQ), [[papers/explainable-crypto-microstructure]] (Bieganowski-Ślepaczuk 2026, SHAP on Binance), [[papers/mlofi-xu-gould-howison]] (MLOFI Ridge regression on NASDAQ), [[papers/gould-bonart-queue-imbalance]] (logistic QI on NASDAQ). Magnitudes agree within a factor of ~1.3 across these four papers.

2. **Chinese-market OFI trio**: GOFI ([[papers/price-impact-generalized-ofi]] on CSI 500), OU-Lévy response ([[papers/csi300-ou-levy-ofi]] on CSI 300 Futures), adaptive learning ([[papers/adaptive-learning-csi300]] on CSI 300 Futures). Spans regression / SDE / time-series-learning approaches on Chinese data.

3. **Two families of impact framework**: event-driven Hawkes / point-process vs transient-propagator. The propagator line ([[papers/bouchaud-farmer-lillo-propagator]], [[papers/brokmann-slow-decay-impact]]) is empirically grounded via deconvolution; the Hawkes line ([[papers/forecasting-high-frequency-ofi]], [[papers/order-flow-filtration]]) is self-exciting point-process-based. The Noble-Rosenbaum-Souilmi simulator ([[papers/reality-gap-lob-simulation]]) uses a power-law propagator kernel consistent with Brokmann's findings.

4. **Queue-imbalance theoretical / empirical pair**: Lipton-Pesavento-Sotiropoulos ([[papers/lipton-quote-imbalance]]) derive closed-form $P_\uparrow$ from diffusive queue model; Gould-Bonart ([[papers/gould-bonart-queue-imbalance]]) fit logistic empirics on the same signal. Strong agreement between theoretical shape and fitted empirics.

### Summary
- Papers wiki'd: 8 (9 requested; VPIN 1301.3228 not on arXiv → skipped).
- New pages: 8 paper pages.
- Total wiki state: 18 papers, 35 pages.
- Raw-only (PDF + markdown but no wiki page): 7 remaining papers from the 2026-04-16 discovery sweep.

---

## 2026-04-16 — Wiki-ingest of 3 new papers + microstructure mindmap

Selected 3 of the 10 papers downloaded earlier today (Path-2 discovery) whose content sits closest to the existing microstructure nucleus.

### Papers ingested

**1. "Bridging the Reality Gap in Limit Order Book Simulation" (2603.24137)**
- Noble, Rosenbaum, Souilmi (Jump Trading + Dauphine-PSL + Polytechnique) — March 2026.
- Created: `papers/reality-gap-lob-simulation.md`
- Created: `methods/queue-reactive-model.md` — new method page for QR framework.
- Updated: `concepts/limit-order-book.md` — added LOB-simulation section linking zero-intelligence, QR, and extended QR.

**2. "Model Predictive Control For Trade Execution" (2603.28898)**
- McAuliffe et al. (Bayforest + ASU + MIT, including Bertsekas) — April 2026.
- Created: `papers/mpc-trade-execution.md`
- Created: `concepts/optimal-execution.md` — new domain concept covering TWAP/VWAP, Almgren–Chriss, RL-based, and MPC approaches.

**3. "Pricing and Hedging for Liquidity Provision in Constant Function Market Making" (2603.01344)**
- Risk, Tung, Wang — March 2026.
- Created: `papers/cfmm-liquidity-provision-pricing.md`
- Created: `concepts/market-making.md` — unified concept page covering both LOB market making (Avellaneda–Stoikov etc.) and AMM liquidity provision (CFMM / Uniswap / Balancer).

### Mindmap created

- Created: `mindmaps/market-microstructure.md` — per-domain mindmap covering all 10 microstructure papers.
  - Mermaid **mindmap** diagram (hierarchical concept tree).
  - Mermaid **flowchart** showing Paper → Concept/Method relationships with typed arrows (introduces / extends / uses).
  - Third Mermaid diagram surfacing five cross-cutting themes: tick-size regime, two OFI definitions, accuracy≠tradability, adverse selection as universal drag, simulator fidelity.
  - JSON triples block for programmatic use.

### Summary
- Papers wiki-ingested: 3 (out of 10 raw-only)
- New pages: 6 (3 papers + 2 concepts + 1 method) + 1 mindmap
- Pages updated: 1 (`limit-order-book`)
- Still in `raw/` only (not yet wiki'd): 7 papers — `2603.20456`, `2603.12040`, `2603.09669`, `2603.07752`, `2602.21125`, `2602.19419`, `2604.00346`.

---

## 2026-04-16 — Full-text re-ingest of 7 papers

### Motivation
Initial ingest (2026-04-15) ran against abstract-only markdown because `marker-pdf` was not installed. `scripts/ingest_arxiv.py` now uses **`pymupdf4llm`** as the primary converter (fast, CPU, ~30 MB; marker-pdf still available as optional upgrade). All 7 raw PDFs re-converted to full-text markdown (22–164 KB each, vs 23-line abstracts previously).

### Pipeline changes
- `scripts/ingest_arxiv.py`: pymupdf4llm → marker-pdf → abstract-only fallback ladder.
- `requirements.txt`: added `pymupdf4llm>=0.0.5`.

### Wiki updates per paper

**1. "Attention Is All You Need" (1706.03762)**
- Updated: `papers/attention-is-all-you-need.md` — added training regime (P100s, Adam β₂=0.98, warmup), ablation findings (single-head −0.9 BLEU, sinusoidal≈learned PE), "why self-attention" path-length argument with complexity table, constituency parsing results.
- Updated: `methods/multi-head-attention.md` — added big-model hyperparameters and ablation notes.

**2. "The Price Impact of Order Book Events" (1011.6402)**
- Updated: `papers/price-impact-order-book-events.md` — full method section with event decomposition `OFI = L^b − C^b − M^s − L^s + C^s + M^b`, stylised-model derivation, April 2010 NYSE TAQ data, average R²=65%, λ≈1 for 35/50 stocks, intraday β 5× higher at open vs close, quote:trade ratio 40:1, tautology check (R² 35–60% after removing price-changing events).
- Updated: `concepts/order-flow-imbalance.md` — added event decomposition and stylised-model derivation.

**3. "Price Impact of Generalised OFI" (2112.02947)**
- Updated: `papers/price-impact-generalized-ofi.md` — added GOFI construction (multi-tick absorption), full results table with all four variants (OFI / log-OFI / GOFI / log-GOFI) across 30s / 1min / 5min horizons. Key finding: GOFI accounts for most of the lift on Chinese 3-second snapshot data; log-stationarisation adds ~8 pp on top.

**4. "Deep Limit Order Book Forecasting" (2403.09267)**
- Corrected: `papers/deep-lob-forecasting.md` — previous draft incorrectly implied Transformer models were tested. Only **DeepLOB** (CNN + Inception + LSTM) is evaluated. Added full tick-size taxonomy (small / medium / large, with 6 / 3 / 6 stock split), training regime (AdamW, lr 6e-5, 45/5/10 day splits, 5-day rolling z-score), horizons in LOB events not time.
- Updated: `concepts/limit-order-book.md` — added the tick-size taxonomy.

**5. "Forecasting High Frequency OFI" (2408.03594)**
- Updated: `papers/forecasting-high-frequency-ofi.md` — clarified the **trade-based** OFI definition used here (distinct from Cont et al.'s event-based OFI), deterministic trade classification via NSE passive/aggressive order IDs (no Lee–Ready), Hansen SPA test, Ogata thinning, model comparison table (exponential / sum-of-exponentials / power-law / non-parametric / VAR). NIFTY futures, 2018-09-19, 375 minute bars.

**6. "Order-Flow Filtration" (2507.22712)**
- Updated: `papers/order-flow-filtration.md` — added three-day (expiry-cycle) sample, 9×3 regime discretisation with smooth anti-diagonal mask (γ=0.2), two OBI constructions (order-based and trade-based), ARMA-residualised + lagged variants, scoring functionals (correlation / regression-R² / Hawkes kernel norms), NSE regulatory context (Persistent Noise Creator, 2021–22).

**7. "Explainable Crypto Microstructure" (2602.00776)**
- Updated: `papers/explainable-crypto-microstructure.md` — added five assets with initial market-cap ranks (BTC 1 / LTC 20 / ETC 40 / ENJ 60 / ROSE 100), 3-second log-return target, GMADL objective, Optuna+nested CV, taker backtest table (ARC/IR/MDD per asset), tick-size modulation with W/USDT spot-vs-perp natural experiment (correlation 0.94), and the microprice connection.

### Cross-paper connections surfaced by re-ingest
- **Tick-size regime is the key predictor of LOB forecastability** — converges across equities ([[papers/deep-lob-forecasting]]) and crypto ([[papers/explainable-crypto-microstructure]]). Added to [[connections/deep-learning-meets-market-microstructure]].
- **Two distinct "OFI" definitions** used in the wiki:
  - *Event-based* OFI (Cont–Kukanov–Stoikov): all LOB events with signed queue contributions.
  - *Trade-based* OFI (Easley–O'Hara / Anantha–Jain): normalised signed-trade count imbalance.
  Clarified in [[papers/forecasting-high-frequency-ofi]] to avoid confusing R² claims across the two conventions.

### Summary
- Pages substantially updated: 10 (7 paper pages + 3 concept/method pages + 1 connection)
- No contradictions detected; one inaccuracy corrected (Transformer ≠ tested in Briola et al.)
- Raw source sizes: 22–164 KB of markdown per paper (previously ~500 B)

---

## 2026-04-15 — Ingested 7 papers (initial batch)

### Papers ingested

**1. "Attention Is All You Need" (1706.03762)**
- Created: `papers/attention-is-all-you-need.md`
- Created: `concepts/transformer-architecture.md`
- Created: `methods/multi-head-attention.md`
- Created: `entities/google-brain.md`

**2. "The Price Impact of Order Book Events" (1011.6402)**
- Created: `papers/price-impact-order-book-events.md`
- Created: `concepts/order-flow-imbalance.md`
- Created: `concepts/price-impact.md`
- Created: `concepts/market-microstructure.md`
- Created: `concepts/limit-order-book.md`
- Created: `entities/rama-cont.md`
- Created: `entities/sasha-stoikov.md`

**3. "The Price Impact of Generalized Order Flow Imbalance" (2112.02947)**
- Created: `papers/price-impact-generalized-ofi.md`
- Updated: `concepts/order-flow-imbalance.md` (added log-GOFI variant)

**4. "Deep Limit Order Book Forecasting" (2403.09267)**
- Created: `papers/deep-lob-forecasting.md`
- Created: `connections/deep-learning-meets-market-microstructure.md`
- Updated: `concepts/limit-order-book.md` (added LOBFrame reference)

**5. "Forecasting High Frequency Order Flow Imbalance" (2408.03594)**
- Created: `papers/forecasting-high-frequency-ofi.md`
- Created: `methods/hawkes-process.md`
- Updated: `concepts/order-flow-imbalance.md` (added Hawkes forecasting reference)

**6. "Order-Flow Filtration and Directional Association with Short-Horizon Returns" (2507.22712)**
- Created: `papers/order-flow-filtration.md`
- Created: `concepts/adverse-selection.md`
- Updated: `concepts/order-flow-imbalance.md` (added filtration reference)

**7. "Explainable Patterns in Cryptocurrency Microstructure" (2602.00776)**
- Created: `papers/explainable-crypto-microstructure.md`
- Created: `methods/shap-values.md`
- Updated: `concepts/adverse-selection.md` (added crypto flash crash evidence)
- Updated: `connections/deep-learning-meets-market-microstructure.md` (added CatBoost/SHAP)

### Summary
- Pages created: 20
- Pages updated: 4
- Note: all raw sources are abstract-only (Marker not installed). Install `marker-pdf` for full-text conversion.

---

## 2026-04-15 — Initial setup

- Created wiki directory structure
- Created `wiki/index.md` (master catalog)
- Created `wiki/log.md` (this file)
- Created subdirectories: papers/, concepts/, entities/, methods/, comparisons/, open-questions/, connections/, mindmaps/
- Created raw subdirectories: papers/, articles/, code/, notes/
- Status: Empty wiki, ready for first ingestion
