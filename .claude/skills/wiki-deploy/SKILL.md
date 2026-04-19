---
name: wiki-deploy
description: Build and deploy the public MkDocs site (sync wiki to docs, mkdocs build, Netlify). Invoke when the user says "deploy", "push the site", "redeploy the site", "build the site", or similar.
---

# wiki-deploy — Build and deploy the public site

Use this skill to turn the `wiki/` vault into a polished public site on Netlify.

## Prerequisites (assumed set up already)

- `site/mkdocs.yml` exists with Material theme + mermaid2 plugin (`securityLevel: loose`).
- `scripts/sync_wiki_to_mkdocs.py` exists and rewrites Obsidian wikilinks.
- Python deps installed: `mkdocs-material`, `pymdown-extensions`, `mkdocs-mermaid2-plugin`, `pymupdf4llm`.
- `netlify.toml` at project root with correct build command + publish dir.

## Build steps

### 1. Sync wiki → docs

```bash
python scripts/sync_wiki_to_mkdocs.py
```

The script copies everything in `wiki/` to `site/docs/` and rewrites `[[wikilinks]]` into MkDocs-compatible relative links. Preserves `site/docs/javascripts/` (MathJax config) across runs.

### 2. Preflight: MathJax sanity check

```bash
python scripts/preflight_mathjax.py
```

Validates the four regression-prone conditions that broke math rendering on 2026-04-16 / -17 / -18: mathjax-config.js load order in `mkdocs.yml`, delimiter set in the config (no bare `$`), `document$.subscribe` guard for Material's instant-nav observable, and cache clears on SPA page swaps. Non-zero exit must block the deploy — do not proceed to the build step until it passes. If it fails, the error code (M1..M4, C1..C6) identifies the specific regression; see `scripts/preflight_mathjax.py` docstring for the full list.

### 3. Build statically

```bash
cd site && mkdocs build --strict
```

`--strict` flags broken links. Investigate any warning before deploying.

Output lands in `site/site/`. Expected: `index.html`, 404 page, `assets/`, `javascripts/`, one directory per section (`papers/`, `concepts/`, `methods/`, etc.).

### 4. Local preview (optional but recommended)

```bash
cd site && mkdocs serve
```

Open `http://127.0.0.1:8000`. Checks to run:
- Home page loads with all 6+ nav tabs.
- A paper page with LaTeX renders cleanly (e.g. `/papers/price-impact-order-book-events/` should show the OFI formula typeset, not raw `\(...\)`).
- The mindmap page (`/mindmaps/market-microstructure/`) renders all three Mermaid diagrams.
- Clicking a node in the flowchart navigates to the target page.
- `/schema/` shows the CLAUDE.md reproduction.

## Deploy options

### Option A — Netlify drag-and-drop (fastest, no git)

1. Open https://app.netlify.com/drop.
2. Drag the folder `arxiv-second-brain/site/site/` (the build output) onto the drop zone.
3. Netlify assigns a URL (or updates the existing one if you're logged in).
4. Rename the site in "Site settings → Change site name" if desired.

Current public URL: the `https://<owner>.github.io/second-brain/` after GitHub Pages deploy — see the repo's Pages settings for the exact URL.

### Option B — Git-connected Netlify (auto-deploy on push)

1. Ensure project is a git repo with sensible `.gitignore` (ignore `site/docs/`, `site/site/`, `raw/papers/*.pdf`).
2. Push to GitHub / GitLab.
3. In Netlify: "Add new site → Import from Git" → select repo. Netlify reads `netlify.toml` and builds on every push.
4. Netlify's build command runs `mkdocs build` from `site/` but does NOT run `sync_wiki_to_mkdocs.py`. Either:
   - Prepend `python scripts/sync_wiki_to_mkdocs.py && ` to the build command in `netlify.toml`, OR
   - Commit `site/docs/` and skip the sync at build time (less clean but simpler).

## Troubleshooting

- **Equations render as raw LaTeX**: run `python scripts/preflight_mathjax.py` — it covers the four recurring causes (load order in `mkdocs.yml`, bare `$` delimiters conflicting with arithmatex `generic: true`, unguarded `document$.subscribe`, missing SPA-nav cache clears). Failure codes map 1:1 to each cause.
- **Mermaid diagrams don't render**: check `mermaid2` plugin is listed in `mkdocs.yml` plugins and Mermaid version ≥ 10.x (for `mindmap` type support).
- **Click on diagram node does nothing**: the `mermaid2` plugin config must include `arguments: { securityLevel: loose }`. Mermaid defaults to `strict` which silently blocks `click` directives.
- **Dev server shows old content after sync**: kill and restart `mkdocs serve` — it occasionally caches. `netstat -ano | grep :8000` then `taskkill //F //PID <pid>`.

## After deploy

Update `wiki/log.md` with a deploy entry:

```markdown
## <YYYY-MM-DD> — Deployed to <URL>
- Built <N> pages, <MB> total
- New content since last deploy: <summary>
```
