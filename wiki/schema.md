---
title: "Schema (CLAUDE.md)"
---

# Schema — CLAUDE.md

This is the **Layer 3 schema file** that governs how the wiki is built. Claude Opus 4.7 reads it at the start of every session so output stays consistent across conversations.

It is verbatim the project's `CLAUDE.md`. Reproduced here so visitors can see exactly what instructions shape the wiki.

As of 2026-04-18, the schema is intentionally **slim**. Operation-specific protocols (how to ingest a paper, how to lint the wiki, how to generate a mindmap, how to deploy the site) live in **skills** — see [Skills](skills/index.md) for details. This keeps the always-loaded context small while still enforcing detailed procedure when operations fire.

If you want to replicate this pattern, start by copying and customising this file for your own domain, then build skills for each recurring operation.

---

# ArXiv Second Brain — LLM Wiki

> A personal research knowledge base built on Karpathy's LLM Wiki pattern.
> Stack: Claude Code (agent), Obsidian (viewer), MkDocs Material (public site), Netlify (hosting).

---

## Operations via skills — read before acting

When the user asks for any of the following, you **MUST invoke the corresponding skill** before reading files or editing anything. The skill contains the full protocol; acting from partial memory of the procedure has produced compliance failures in the past (see `wiki/log.md` 2026-04-17 / 2026-04-18 for examples).

| Trigger phrase / situation | Skill to invoke |
|---|---|
| "ingest paper X", "add paper X", "ingest the new papers in raw/", new file appears in `raw/papers/` | `arxiv-ingest` |
| "lint", "audit the wiki", "check wiki health" | `wiki-lint` |
| "mindmap X", "generate mindmap for X", "map the cluster" | `wiki-mindmap` |
| "deploy", "push the site", "redeploy", "build the site" | `wiki-deploy` |

Do NOT execute these operations from memory of prior sessions or partial understanding of the procedure. **Load the skill in full first.**

For substantive questions about wiki content ("what does paper X say?", "what's our stance on Y?"): prefer **reading the relevant wiki pages directly** over recalling from conversation. The wiki on disk is the authoritative artifact.

---

## Project purpose

Build and maintain a **living, compounding knowledge base** from arXiv research papers. The wiki is the primary artifact — not the chat, not the search results. Every paper ingested makes the wiki smarter. Every query that produces insight gets filed back.

Research domains of interest (non-exhaustive, will evolve):
- Machine learning & deep learning (architectures, training, optimisation)
- Quantitative finance (market microstructure, signal research, options pricing)
- Bioinformatics & computational biology (genomics, systems biology)
- Statistical methods (time series, Bayesian inference, causal inference)
- AI safety & alignment
- Reinforcement learning

---

## Directory structure

```
arxiv-second-brain/
├── CLAUDE.md                  # This file — slim schema, always loaded
├── .claude/skills/            # Operation-specific playbooks (loaded on invocation)
│   ├── arxiv-ingest/SKILL.md  # INGEST protocol
│   ├── wiki-lint/SKILL.md     # LINT protocol
│   ├── wiki-mindmap/SKILL.md  # MINDMAP protocol
│   └── wiki-deploy/SKILL.md   # DEPLOY protocol
├── raw/                       # Layer 1 — immutable source documents
│   ├── papers/                # arXiv PDFs + pymupdf4llm-converted markdown
│   ├── articles/              # Blog posts, technical articles
│   ├── code/                  # Notable repos or code snippets
│   └── notes/                 # Owner's private notes (NOT published to site)
├── wiki/                      # Layer 2 — LLM-generated synthesis pages
│   ├── index.md               # Master catalog + landing page
│   ├── schema.md              # Verbatim copy of this file for public site
│   ├── log.md                 # Chronological record of all operations
│   ├── papers/                # One summary page per paper
│   ├── concepts/              # Concept pages (e.g. order-flow-imbalance.md)
│   ├── methods/               # Algorithms, techniques, named formulas
│   ├── entities/              # People, institutions, datasets
│   ├── comparisons/           # Side-by-side analyses
│   ├── connections/           # Cross-domain links
│   ├── open-questions/        # Unsolved problems, research gaps
│   └── mindmaps/              # Mermaid diagrams (domain / per-paper)
├── scripts/
│   ├── ingest_arxiv.py        # Download arxiv PDF + convert (used by arxiv-ingest skill)
│   ├── fetch_daily.py         # Keyword-filtered daily discovery (q-fin focus)
│   ├── discovery_config.py    # Keyword tiers, seed papers, category lists
│   ├── bootstrap_seeds.py     # Semantic Scholar expansion from seeds
│   ├── sync_wiki_to_mkdocs.py # wiki/ → site/docs/ + wikilink rewrite
│   └── seed_batch.txt         # Curated arXiv ID list
├── site/
│   ├── mkdocs.yml             # Material theme + mermaid2 + MathJax
│   ├── docs/                  # Auto-generated by sync_wiki_to_mkdocs.py
│   └── site/                  # MkDocs build output (drag to Netlify)
├── netlify.toml               # Build config (project root)
└── requirements.txt
```

---

## Wiki page conventions (apply to ALL edits)

### Frontmatter (YAML) — required on every page

```yaml
---
title: "<exact title>"
type: paper | concept | entity | method | comparison | open-question | connection | mindmap
created: <YYYY-MM-DD>
updated: <YYYY-MM-DD>
sources:
  - raw/papers/<id>.md
tags:
  - tag-1
  - tag-2
related:
  - concepts/<slug>.md
  - methods/<slug>.md
confidence: high | medium | low | speculative
---
```

### Page types

- **Paper** (`wiki/papers/`): authors, institution, year, arXiv ID; plain-language abstract; key contributions; method summary; main results (with confidence flags); limitations; connections. Direct quotes minimised — paraphrase and synthesise.
- **Concept** (`wiki/concepts/`): definition; historical context; how it works (technical but accessible); key papers that define or extend it; related concepts (wikilinks); open questions.
- **Entity** (`wiki/entities/`): person, institution, or dataset — affiliation / focus / notable outputs.
- **Method** (`wiki/methods/`): algorithm description; key equations (LaTeX); computational complexity; when to use / when not to use; implementations; papers that introduced or improved it.
- **Comparison** (`wiki/comparisons/`): two or more items side by side; dimensions of comparison (table); verdict / recommendations by use case.
- **Connection** (`wiki/connections/`): cross-domain insight; why the domains relate; transfer opportunities; key bridging papers.
- **Open question** (`wiki/open-questions/`): unsolved problem; what's known; candidate approaches; what would settle it.
- **Mindmap** (`wiki/mindmaps/`): Mermaid diagrams produced via the `wiki-mindmap` skill.

### Wikilinks

Use Obsidian-compatible wikilinks: `[[concept-name]]` or `[[folder/page-name|Display Text]]`.

- Every page should have at least **3 outgoing wikilinks**.
- Orphan pages (no incoming wikilinks) are flagged by `wiki-lint`.

### Writing style

- Clear, precise, technical but not jargon-heavy.
- **British English** (optimisation, behaviour, colour).
- Active voice preferred.
- **LaTeX for equations**: `$E = mc^2$` inline, `$$` blocks for display. Use only these delimiters — MathJax + arithmatex are configured for them, not `\(...\)` or `\[...\]` written by hand.
- Code blocks with language tags.
- Tables for structured comparisons.

---

## Method-promotion rule (applies to every ingest)

When a paper introduces or centrally uses a **named formula, technique, or model** (examples: propagator model, microprice, OFI, Hawkes kernel, MLOFI, VPIN, queue-reactive model, Ornstein–Uhlenbeck process), **create a dedicated `wiki/methods/<slug>.md` page**. Do not embed the formula *only* inside the paper page.

Promotion signal — create a method page if **any** of the following hold:
1. The method is referenced by ≥2 papers in the wiki, or is likely to be (named primitive in the domain).
2. The paper's contribution is primarily *defining* or *extending* the method itself.
3. A reader searching for "how does X work?" would expect a standalone page for X.

This rule also applies to named signals that belong as concepts rather than methods — promote them to `wiki/concepts/` under the same test.

Anti-pattern to avoid (what went wrong 2026-04-17): ingesting 8 papers but only touching ~1.2 wiki pages per paper because methods mentioned in the text were never promoted to their own pages. The `methods/` directory should grow roughly in proportion to novel primitives introduced.

---

## `wiki/index.md` purpose

Master catalog + landing page. Maintained in sync by the `arxiv-ingest` and `wiki-deploy` skills. Contains:

- Hero / project overview (for public-facing visitors).
- Layer-architecture explanation + RAG-vs-wiki comparison.
- Current paper / page counts.
- By-domain grouping of all papers.
- By-type catalog (concepts / methods / entities / connections / mindmaps).
- Recent additions (last 3–5 entries).
- Contradictions & flags.

---

## Environment variables

```
ANTHROPIC_API_KEY=sk-ant-...         # For Netlify serverless query function (not yet deployed)
ARXIV_CATEGORIES=cs.LG,cs.AI,q-fin   # For daily discovery via fetch_daily.py
ARXIV_MAX_DAILY=10                    # Max papers per discovery run
```

---

## First-session checklist (for a fresh Claude Code session)

1. Read this CLAUDE.md in full.
2. Skim `wiki/index.md` for current state.
3. Check `raw/papers/` for any source files without a corresponding `wiki/papers/<slug>.md` page — these are pending ingests.
4. If the user asks for any operation in the table above: **invoke the skill first**.
5. Before declaring any ingest done, verify compliance with the method-promotion rule.

---

## Schema file visibility

This file is copied verbatim to `wiki/schema.md` (via the sync script) and rendered on the public site at `/schema/`. Visitors can read the schema that drives the wiki. Keep it tight and self-contained.
