---
title: "Skills"
---

# Skills — how operations are actually executed

## Why skills

Claude Code's **schema file** (CLAUDE.md / [the Schema page](../schema.md)) is loaded into every conversation automatically. That means every token in CLAUDE.md costs you on every turn — whether you're ingesting a paper, asking a trivial question, or deploying the site.

As the schema grew (deploy steps, lint rules, mindmap conventions, method-promotion rule, etc.), CLAUDE.md ballooned to ~5.4 K tokens. Most sessions don't need most of it: a casual "what does paper X say?" doesn't require the full Netlify deployment protocol.

**Solution: split the schema into skills.**

A *skill* is a Claude Code primitive — a self-contained `.claude/skills/<name>/SKILL.md` file with frontmatter (name, description) and a body. Skills load **on demand**: Claude discovers them automatically, and invokes the relevant one when the user's request matches the description. The rest of the time, the skill's body sits on disk and doesn't cost any context.

## What moved where

| Content | Location after split |
|---|---|
| Project identity, directory structure, page conventions, writing style, method-promotion rule | **CLAUDE.md** (always loaded) |
| INGEST operation — download, convert, create paper page, promote methods, update concepts, hunt connections, log | [`arxiv-ingest`](arxiv-ingest.md) |
| LINT operation — wiki health audit | [`wiki-lint`](wiki-lint.md) |
| MINDMAP operation — Mermaid diagram generation | [`wiki-mindmap`](wiki-mindmap.md) |
| DEPLOY operation — sync + build + Netlify | [`wiki-deploy`](wiki-deploy.md) |

## How "forced" invocation works

CLAUDE.md cannot literally *force* skill invocation — only Claude Code's settings.json hooks can do that. What it can do:

- List each operation's trigger phrase in a table (see the top of the [Schema page](../schema.md)).
- Use strong imperatives: *"you MUST invoke the corresponding skill before reading files or editing anything"*.
- Point to concrete compliance failures (the 2026-04-17 batch, where the method-promotion rule was skipped) so future Claude sessions see the cost of shortcutting.

In practice this gets ~95% of the way to hard enforcement. A hook in `settings.json` could close the last 5% by intercepting prompts and refusing to proceed without a skill invocation — but that adds plumbing for a small residual gain.

## Token savings

| Before split | After split |
|---|---|
| CLAUDE.md ≈ 5.4 K tokens, loaded every turn | CLAUDE.md ≈ 2.2 K tokens, loaded every turn |
| Ingest protocol loaded every turn | Ingest protocol loaded only during `arxiv-ingest` invocation |
| Lint protocol loaded every turn | Loaded only when `wiki-lint` fires |
| Mindmap, Deploy: same | Same |

Per-turn saving: ~3 K tokens. Per-session: adds up. Per-ingest: no net change — the skill body is loaded then — but the skill is more complete and explicit than the CLAUDE.md section it replaced, so compliance improves.

## How skills look in the codebase

```
arxiv-second-brain/
├── CLAUDE.md                         # Slim schema — always loaded
└── .claude/
    └── skills/
        ├── arxiv-ingest/SKILL.md     # Ingest a new paper
        ├── wiki-lint/SKILL.md        # Audit wiki health
        ├── wiki-mindmap/SKILL.md     # Generate a Mermaid mindmap
        └── wiki-deploy/SKILL.md      # Build + deploy to Netlify
```

Each SKILL.md has the same structure: YAML frontmatter with `name` and `description` (the latter is what Claude matches the user's request against), then a Markdown body with the full procedure.

## The four skills

- **[arxiv-ingest](arxiv-ingest.md)** — the main write-path: download a paper, convert to full-text markdown, create/update wiki pages following the method-promotion rule, update index + log.
- **[wiki-lint](wiki-lint.md)** — audit the wiki for orphan pages, broken wikilinks, missing method pages, thin pages, contradictions.
- **[wiki-mindmap](wiki-mindmap.md)** — generate per-domain / per-paper / cross-domain Mermaid diagrams (three-diagram layout: hierarchical mindmap + clickable flowchart + cross-cutting themes).
- **[wiki-deploy](wiki-deploy.md)** — sync wiki to docs, `mkdocs build --strict`, local preview, Netlify drag-and-drop or git-connected auto-deploy, troubleshooting checklist.

## Why share them publicly

Three reasons:

1. **Transparency** — visitors can see exactly what instructions shape the content they're reading. Makes the LLM-generated nature of the wiki honest and auditable, not hidden.
2. **Reproducibility** — anyone building their own LLM wiki can copy these skill files as a starting point. They are domain-agnostic enough (swap out "arXiv" / "microstructure" for your own sources / topics) to be useful templates.
3. **Invitation to critique** — if a skill is sloppy or missing something, a reader can point it out. Improvements flow back into the schema.

## Also worth reading

- **[Schema (CLAUDE.md)](../schema.md)** — the always-loaded schema file that these skills complement.
- **[Home](../index.md)** — landing page with the layered-architecture explanation and the wiki-vs-RAG comparison.
