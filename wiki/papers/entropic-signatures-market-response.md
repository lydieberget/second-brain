---
title: "Entropic Signatures of Market Response under Concentrated Policy Communication"
type: paper
created: 2026-04-17
updated: 2026-04-17
sources:
  - raw/papers/2603.12040.md
tags:
  - entropy
  - information-theory
  - equity-indices
  - policy-shocks
  - extreme-events
  - shannon-entropy
  - macro
related:
  - concepts/market-microstructure.md
confidence: medium
---

# Entropic Signatures of Market Response under Concentrated Policy Communication

**Authors**: Drzazga-Szczȩśniak, Gupta, Kaczmarek, Gnyp, Jarosik, Waligóra, Kielak, Gupta, Gurzyńska, Gil, Szczepanik, Kielak, Szczȩśniak (13 authors)
**Institutions**: Częstochowa University of Technology; Jan Długosz University; Purdue; NC State; Gdańsk; Le Mans; Analitico (Katowice)
**Year**: 2026 (March 2026)
**arXiv**: [2603.12040](https://arxiv.org/abs/2603.12040)
**Categories**: q-fin.ST

---

## Scope note

**This paper sits at the macro / equity-index level, not LOB microstructure.** It was included in the signal-design batch because its abstract mentioned "entropic signatures" — but on full reading the signals operate on daily / 5-minute equity-index returns globally, not on order-book features. It is still useful as an information-theoretic complement to dispersion-based volatility measures, and introduces two entropy signals (Shannon and cumulative) that could in principle be adapted to LOB features.

---

## Plain-language abstract

Uses the first 100 days of the second Trump presidency (Jan 20 – Apr 30 2025) as a "**concentrated policy communication**" natural experiment. Analyses major equity indices across the Americas, Europe, Asia, and Oceania using both **standard deviation** (dispersion) and **Shannon entropy** (information complexity). Documents a **decoupling** between the two measures — entropy is not a proxy for amplitude, it reflects the *diversity of populated outcomes*. Introduces a **sliding-window cumulative entropy** to localise extreme episodes. Finds short-term globally-coupled but regionally-modulated market impacts with clear links to specific policy announcements.

---

## Key contributions

1. **Shannon entropy as a market disturbance measure** — defines entropy on binned return distributions with Velleman's rule for bin count. Complementary to standard deviation: entropy compresses under "structured volatility" (large but repetitive moves driven by a small set of narratives) even when std is high.

   $$H = -\sum_{i=1}^{m} p_i \log p_i$$

   where $p_i$ is the empirical frequency of returns falling in bin $i$.

2. **Cumulative entropy with sliding window** — constructs an expanding-window Shannon entropy trajectory that produces "ramp-like" signatures around extreme events without needing to pre-specify event windows or a parametric shock model.

3. **Structured-volatility hypothesis**: when a small number of salient narratives channel market reactions into similar configurations, entropy compresses while volatility stays high. Provides a quantitative test by reading $H$ and $\sigma$ jointly on the same windows.

4. **Cross-regional empirics** across 15 indices (US, Brazil, Canada, Eurozone, UK, Germany, Poland, Japan, China, Hong Kong, India, Australia, New Zealand) at daily and 5-minute granularity.

---

## Method summary

### Data
- **15 equity indices** across Americas / Europe / Asia / Oceania.
- **Daily**: full 100-day windows before and after 2025-01-20 (Trump inauguration).
- **5-minute**: used only for cumulative-entropy calculations, for information density.
- Multiple data vendors: Stooq, Investing.com, EOD Historical Data, Dukascopy, Bluecapital.
- Standardised into a MariaDB relational database for analysis.

### Signals

**Shannon entropy** on binned return distributions — computed per window with Velleman-rule bin count.

**Cumulative entropy** — a spectrum of entropies over increasing subsets $T_0 \subset T_1 \subset \ldots \subset T_m$ where each $T_k$ extends $T_{k-1}$ by a fixed $\Delta t$. Produces a trajectory $H_0, H_1, \ldots$ whose shape encodes when informational complexity builds fastest and how persistent the elevated state is.

### Jointly reading $H$ vs $\sigma$

| State | $\sigma$ | $H$ | Interpretation |
|---|---|---|---|
| Calm | low | high | Efficient random walk |
| Structured volatile | high | **low** | Large moves but narratively constrained (policy shock regime) |
| Unstructured volatile | high | high | Large moves with diverse drivers (idiosyncratic / multi-shock) |

The paper's key finding is that the policy-concentrated period shows **structured volatility** — high $\sigma$, low $H$ — which standard volatility-only analysis would mislabel as generic turbulence.

---

## Main results

- **Decoupling** between standard deviation and Shannon entropy is substantial across most indices in the post-inauguration window — entropy adds genuine information beyond volatility.
- **Cumulative entropy ramps** align precisely with major announcement days (tariffs, geopolitical interventions, industrial-policy declarations).
- **Global coupling**: extreme entropy signatures appear near-simultaneously across regions, consistent with event-driven global market response.
- **Regional modulation**: magnitude and persistence of entropy elevations vary by region; indices with tighter US trade linkage (Canada's TSX, Germany's DAX, Japan's Nikkei) show sharper responses.

---

## Limitations

- **Macro / index-level, not LOB-level**: entropy is computed on daily/5-min index returns, not on order-book features. The framework could be adapted to LOB signals but this paper doesn't do that.
- **One natural experiment**: 100-day Trump-2 window + 100-day pre-window reference. No cross-validation on other policy-concentration periods.
- **Binning sensitivity**: entropy values depend on bin count via Velleman's rule; robustness to alternative binning not extensively tested.
- **Descriptive, not predictive**: the paper shows entropy correlates with extreme events but does not build a forward-looking signal.
- **Thirteen authors, eight institutions** — unusually broad authorship; may reflect a methods paper with shared credit rather than a tight empirical focus.

---

## Connections

- **Conceptually adjacent to microstructure signal-design** but operating at a different scale. The idea that *information complexity* is orthogonal to *price amplitude* is directly applicable to LOB signals — e.g., binning OFI realisations and computing Shannon entropy would give a complement to OFI magnitude.
- **Contrasts with the OFI / LOB tradition**: microstructure papers in this wiki ([[papers/price-impact-order-book-events]], [[papers/gould-bonart-queue-imbalance]], [[papers/mlofi-xu-gould-howison]]) focus on *directional* signals; this paper focuses on *distributional* signals (how many distinct outcomes are populated, not which direction they go).
- **Future research vector**: the cumulative-entropy construction could be a natural extreme-event detector for LOB data — potentially useful for volatility-regime-aware execution algorithms (cf. [[papers/mpc-trade-execution]]).
- **Mostly useful as**: a reference for entropy as a market signal, an example of information-theoretic analysis applied to financial time series, and a reminder that dispersion-only volatility measures miss structural information about the distribution shape.
