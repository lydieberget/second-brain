# Setup Guide — ArXiv Second Brain

## Prerequisites

- Python 3.11+
- Node.js 18+ (for Netlify functions)
- Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- Obsidian (free, for viewing the wiki locally)
- Git + GitHub account
- Netlify account (you already have one)

---

## Step 1 — Clone and initialise

```bash
# Create the project
mkdir arxiv-second-brain && cd arxiv-second-brain
git init

# Create directory structure
mkdir -p raw/{papers,articles,code,notes}
mkdir -p wiki/{papers,concepts,entities,methods,comparisons,open-questions,connections,mindmaps}
mkdir -p scripts
mkdir -p site/{docs,overrides,netlify/functions}
mkdir -p .github/workflows
```

## Step 2 — Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step 3 — Set up Obsidian

1. Open Obsidian
2. "Open folder as vault" → select `wiki/`
3. Enable Community Plugins:
   - **Dataview** (query your frontmatter)
   - **Graph Analysis** (enhanced graph view)
   - **Templater** (optional, for manual notes)
4. The graph view will auto-populate as Claude Code builds your wiki

## Step 4 — Open in Claude Code

```bash
cd arxiv-second-brain
claude
```

Claude Code will read `CLAUDE.md` and understand the project.

First commands to try:
```
> ingest 1706.03762
  (Attention Is All You Need — good first test)

> ingest 2301.13848
  (Toolformer — tests cross-referencing)

> lint
  (Check wiki health)

> mindmap transformer
  (Generate a concept map)
```

## Step 5 — Set up daily arXiv ingestion (optional)

Add your `ANTHROPIC_API_KEY` as a GitHub Actions secret, then the
workflow in `.github/workflows/daily-arxiv.yml` will:
- Run at 07:00 UTC daily
- Fetch new papers in your categories
- Convert PDFs to markdown
- Commit to `raw/papers/`
- Claude Code can then ingest on your next session

## Step 6 — Deploy to Netlify

```bash
# Link to Netlify (you know the drill)
netlify init

# Set environment variable
netlify env:set ANTHROPIC_API_KEY sk-ant-...

# Deploy
git push  # Netlify auto-builds from git
```

Your wiki will be live at `https://your-site.netlify.app/`

---

## Daily workflow

1. **Morning**: Check if daily-arxiv.yml found new papers
2. **Open Claude Code**: `claude` in project directory
3. **Ingest new papers**: `ingest 2406.xxxxx` or `ingest --batch today.txt`
4. **Ask questions**: Claude searches your wiki and answers with citations
5. **Weekly lint**: `lint` to catch contradictions, orphans, stale content
6. **Share**: Push to git → Netlify auto-deploys → friends see updated wiki

---

## Architecture diagram

```
┌─────────────────────────────────────────────────┐
│                  YOUR MACHINE                    │
│                                                  │
│  ┌──────────┐    ┌────────────┐    ┌──────────┐ │
│  │  arXiv   │───▶│  raw/      │───▶│  Claude  │ │
│  │  API     │    │  papers/   │    │  Code    │ │
│  └──────────┘    └────────────┘    └────┬─────┘ │
│                                         │       │
│                                    reads/writes  │
│                                         │       │
│  ┌──────────┐    ┌────────────┐    ┌────▼─────┐ │
│  │ Obsidian │◀───│  wiki/     │◀───│ CLAUDE.md│ │
│  │ (viewer) │    │  (Layer 2) │    │ (schema) │ │
│  └──────────┘    └─────┬──────┘    └──────────┘ │
│                        │                         │
└────────────────────────┼─────────────────────────┘
                         │ git push
                         ▼
              ┌──────────────────┐
              │   GitHub Repo    │
              │                  │
              │  GitHub Actions  │
              │  (daily arXiv)   │
              └────────┬─────────┘
                       │ auto-deploy
                       ▼
              ┌──────────────────┐
              │    Netlify       │
              │                  │
              │  MkDocs site     │──▶  friends visit
              │  + query API     │     your-wiki.netlify.app
              │  (Claude API)    │
              └──────────────────┘
```
