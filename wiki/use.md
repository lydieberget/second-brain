---
title: "Using the Wiki in Code Projects"
---

# Using the wiki as context for Claude Code, Copilot, and other LLMs

The wiki isn't just for reading. Its real value is as a **distilled knowledge layer** you can hand to an LLM when coding — so the model writes informed code that references microstructure theory correctly instead of reinventing half-remembered definitions from its training data.

This page explains three concrete workflows, ranked by how cleanly each tool integrates external knowledge.

---

## Why this works

The three-layer architecture ([home page](index.md) explains it) means:

- **Raw papers** (~400 K tokens): full-text arXiv source, the archive.
- **Wiki pages** (~50 K tokens): synthesised, opinionated, cross-linked — already a working-memory-sized knowledge layer.
- **Schema** ([CLAUDE.md](schema.md), ~2 K tokens): always-on conventions.

For coding help, the **wiki layer is what you want in context**. It's ~8× smaller than the raw corpus and already encodes the judgement calls you've made. Only drop into raw when you need a verbatim formula or table.

---

## 1. Claude Code — cleanest fit

Claude Code has native `Read` / `Grep` / `Glob` tools and honours `CLAUDE.md` pointers automatically. The setup:

### In your code project, create a CLAUDE.md:

```markdown
# <Project name>

## Domain knowledge — microstructure wiki

When working on limit-order-book, execution, market-making, or OFI-related code,
consult the wiki at:
`<path/to/the/cloned-repo>/wiki/`

**Start from** `wiki/index.md`. For specific topics, go directly to:

- `wiki/concepts/order-flow-imbalance.md` — OFI definitions (event-based vs trade-based)
- `wiki/concepts/limit-order-book.md` — LOB mechanics + tick-size taxonomy
- `wiki/concepts/price-impact.md` — impact models, square-root law
- `wiki/concepts/optimal-execution.md` — TWAP / VWAP / Almgren-Chriss / MPC
- `wiki/concepts/market-making.md` — LOB quoting + AMM liquidity provision
- `wiki/methods/propagator-model.md` — transient impact kernel formula
- `wiki/methods/microprice.md` — queue-weighted fair value
- `wiki/methods/queue-reactive-model.md` — LOB simulator
- `wiki/methods/hawkes-process.md` — self-exciting point processes

Before designing a new component, grep the wiki for related work. **Do not**
auto-load `raw/papers/` — it's ~400 K tokens of source material the wiki has
already distilled. Only crack open a specific `raw/papers/<id>.md` if you need
a verbatim formula or table.

For execution and LOB code specifically, the **tick-size regime** findings
apply: large-tick assets behave very differently from small-tick ones.
```

### How Claude Code then works

1. Starts a session, reads CLAUDE.md (~1 K tokens).
2. You ask: *"write a toy LOB simulator"*.
3. Claude greps/reads the wiki pages listed — typically pulls ~5–10 K tokens of relevant context.
4. Writes informed code: uses the QR-model state projection, adds an impact-feedback kernel, handles tick-size regimes, cites the wiki pages in comments or the README.

**Cost**: ~10 K tokens per task vs ~400 K if you tried to load everything. That's the wiki earning its keep.

---

## 2. GitHub Copilot — also supports instruction files

Copilot has three surfaces with different levels of external-context support:

| Surface | Reads instruction files? | Filesystem access |
|---|---|---|
| **Copilot Coding Agent** (autonomous, creates PRs) | **yes** — `AGENTS.md` or `.github/copilot-instructions.md` | Full repo, navigates like Claude Code |
| **Copilot Chat** (interactive in VS Code) | **yes** — `.github/copilot-instructions.md` | Open workspace only |
| **Copilot inline autocomplete** | no | Surrounding code + editor context only |

So yes — for the first two surfaces, an instruction file with a pointer to the wiki works much like `CLAUDE.md` does for Claude Code.

### Catch: workspace-scoped filesystem access

Copilot can only read files inside the workspace it's opened on. If the wiki lives at `C:/…/arxiv-second-brain/wiki/` and your code project is elsewhere, a pointer in AGENTS.md alone won't reach it.

### Two ways to make the wiki visible

- **Multi-root workspace** — a `.code-workspace` file listing both folders. Copilot treats both as workspace. Cleanest for local dev.
- **Git submodule / subtree** — pull the wiki into your code repo at `docs/wiki/`. Heavier but survives cloning, and works for the Copilot Coding Agent (which runs against a git repo, not your local filesystem).

### Example AGENTS.md for a code project

```markdown
# Microstructure execution engine

## Setup
`pip install -r requirements.txt`

## Domain knowledge
This project implements OFI-based execution. Before writing microstructure
code, consult the wiki at `wiki/` (added to workspace via .code-workspace,
or included as a git submodule at `docs/wiki/`).

Start from `wiki/index.md`, then drill into:
- `wiki/concepts/order-flow-imbalance.md`
- `wiki/concepts/limit-order-book.md` (tick-size taxonomy)
- `wiki/concepts/optimal-execution.md`
- `wiki/methods/propagator-model.md`
- `wiki/methods/queue-reactive-model.md`
- `wiki/methods/microprice.md`

Do not auto-load `wiki/raw/papers/` — it is ~400 K tokens of source material
the wiki has already distilled.

## Code style
- Python 3.11, PEP 8, type hints required.
- Tests in `tests/`, run with `pytest`.

## Tick-size regime
Large-tick and small-tick assets have different signal behaviours — see
`wiki/concepts/limit-order-book.md`. Keep this in mind when writing
regime-sensitive logic.
```

The **Coding Agent** will actually navigate the wiki pages it needs. **Chat** will reference them when you prompt it to. **Inline** will not — for inline suggestions, rely on well-named identifiers and local comments instead.

---

## 3. Other LLMs (ChatGPT, Claude.ai web, Gemini, etc.)

No tool-calling with the filesystem, so you paste.

- **Claude.ai Projects**: drop the relevant concept / method / paper pages into the project's file set. Reusable across chats.
- **ChatGPT Custom GPTs**: same idea — upload wiki pages as knowledge.
- **Raw paste**: keep a consolidated "microstructure primer" (~5–10 K tokens condensed from the wiki) as a reusable prompt prefix.

---

## Which pages to load — budget per task

| Task | Load from wiki | ~Tokens |
|---|---|---|
| Write a toy LOB simulator | [limit-order-book](concepts/limit-order-book.md) + [queue-reactive-model](methods/queue-reactive-model.md) + [reality-gap-lob-simulation](papers/reality-gap-lob-simulation.md) | ~8 K |
| Implement OFI signal | [order-flow-imbalance](concepts/order-flow-imbalance.md) + [price-impact-order-book-events](papers/price-impact-order-book-events.md) | ~6 K |
| Build an execution algorithm | [optimal-execution](concepts/optimal-execution.md) + [mpc-trade-execution](papers/mpc-trade-execution.md) + [propagator-model](methods/propagator-model.md) | ~10 K |
| Discuss market-making strategy | [market-making](concepts/market-making.md) + [adverse-selection](concepts/adverse-selection.md) + [microprice](methods/microprice.md) | ~8 K |
| Something spanning the whole domain | [index](index.md) + [mindmaps/market-microstructure](mindmaps/market-microstructure.md) + drill down | ~5 K then as needed |

---

## Golden rules

1. **Start from `wiki/index.md`** in a fresh session. It's the cheapest entry point and tells the LLM where everything is.
2. **Don't bulk-load the wiki**. 50 K tokens is manageable but wasteful if you only need three pages.
3. **Don't load `raw/papers/`**. ~400 K tokens of source material; the wiki has already distilled it. Only crack open a specific raw file during ingest or for a verbatim formula.
4. **When a coding task frequently needs raw papers**, that's a signal the corresponding wiki page is too thin — worth deepening.

---

## What stays behind (never loaded)

- Full-text PDFs in `raw/papers/` (the archive).
- The `.claude/skills/` files (only relevant in the wiki's own Claude Code session, not in code projects).

For coding, the wiki almost always has what you need.

---

## Also worth reading

- [Home page](index.md) — the three-layer architecture explained.
- [Schema (CLAUDE.md)](schema.md) — the always-loaded instructions that drive the wiki itself.
- [Skills](skills/index.md) — how the schema is split into on-demand playbooks.
