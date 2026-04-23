---
title: "Jean-Philippe Bouchaud"
type: entity
created: 2026-04-23
updated: 2026-04-23
sources:
  - raw/papers/0809.0822.md
  - raw/papers/0904.0900.md
  - raw/papers/1107.3364.md
  - raw/papers/1407.3390.md
tags:
  - person
  - market-microstructure
  - econophysics
  - price-impact
related:
  - entities/zoltan-eisler.md
  - papers/bouchaud-farmer-lillo-propagator.md
  - papers/eisler-bouchaud-kockelkoren-order-book-events.md
  - papers/models-for-all-order-book-events.md
  - papers/brokmann-slow-decay-impact.md
  - concepts/price-impact.md
  - methods/propagator-model.md
  - methods/event-type-impact-decomposition.md
confidence: high
---

# Jean-Philippe Bouchaud

## Affiliation

Chairman and Head of Research at Capital Fund Management (CFM), Paris. Professor at École normale supérieure, École polytechnique, and Collège de France. Member of the French Academy of Sciences.

## Key contributions

- **Propagator model of price impact** — co-creator of the [[methods/propagator-model|transient impact framework]] reconciling long-memory order flow with near-martingale prices. Core reference for modelling meta-order execution cost.
- **Event-type impact decomposition** — with Eisler and Kockelkoren, extended the propagator to six distinct order-book event types (market, limit, cancel × inside-spread / at-best). See [[methods/event-type-impact-decomposition]].
- **Square-root law of impact** — empirical and theoretical work establishing that meta-order impact scales as $\sqrt{Q/V} \cdot \sigma$ across many markets. The Patzelt–Bouchaud (2017) universality extension generalised the scaling to non-linear regimes.
- **Slow decay of impact / deconvolution** — with Brokmann and CFM, separated the "structural" impact decay from the spurious persistence caused by a trader's own correlated order flow. Shows the true propagator decays to zero, contradicting the "2/3 permanent impact" folklore. See [[papers/brokmann-slow-decay-impact]].
- **Dissecting cross-impact** — with Benzaquen, Mastromatteo, Eisler, empirical decomposition of multi-asset impact — the precursor to the current [[concepts/cross-impact]] literature.
- **Random matrix theory for finance** — Laloux–Cizeau–Potters–Bouchaud (2000) seminal paper on cleaning empirical covariance matrices for portfolio construction.
- **Econophysics methodology** — long-standing advocate of the physicist's empirical approach to finance ("eyeball econometrics" plus parsimonious models), distinct from equilibrium micro-economics.

## Notable papers (in this wiki)

- [[papers/bouchaud-farmer-lillo-propagator]] — "How Markets Slowly Digest Changes in Supply and Demand" (with Farmer, Lillo, 2008).
- [[papers/eisler-bouchaud-kockelkoren-order-book-events]] — "The Price Impact of Order Book Events: Market Orders, Limit Orders and Cancellations" (with Eisler, Kockelkoren, 2009/2012).
- [[papers/models-for-all-order-book-events]] — "Models for the Impact of All Order Book Events" (with Eisler, Kockelkoren, 2011).
- [[papers/brokmann-slow-decay-impact]] — "Slow Decay of Impact in Equity Markets" (with Brokmann, Lempérière, 2014).

## Connections

- [[entities/zoltan-eisler]] — frequent collaborator on impact decomposition work at CFM.
- [[concepts/price-impact]] — Bouchaud's research programme has largely defined the modern empirical theory of price impact.
- [[methods/propagator-model]] — the framework most directly associated with his name.
- [[methods/event-type-impact-decomposition]] — the refinement that generalises the propagator to the full LOB event stream.
