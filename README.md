# ArXiv Second Brain

A personal research wiki built on [Karpathy's LLM Wiki pattern](https://x.com/karpathy), currently focused on **market microstructure**. Synthesised by Claude Opus 4.7 from arXiv papers, published as a static site.

Live site: see the **Pages** tab once deployed.

## Structure

Three layers:

- `raw/papers/` — arXiv PDFs + full-text markdown conversions (immutable source).
- `wiki/` — LLM-generated synthesis pages organised by type (papers, concepts, methods, entities, comparisons, connections, mindmaps).
- `CLAUDE.md` + `.claude/skills/` — schema and operation protocols that drive how the wiki is built.

See the [site Home page](https://) for the full layer-architecture explanation and wiki-vs-RAG comparison.

## Local development

Install dependencies:

```bash
pip install -r requirements.txt
pip install mkdocs-material pymdown-extensions mkdocs-mermaid2-plugin
```

Preview locally:

```bash
python scripts/sync_wiki_to_mkdocs.py
cd site && mkdocs serve
```

Opens at `http://127.0.0.1:8000`.

## Ingesting a new paper

See [`.claude/skills/arxiv-ingest/SKILL.md`](.claude/skills/arxiv-ingest/SKILL.md) for the full procedure. Short form:

```bash
python scripts/ingest_arxiv.py <arxiv_id>
# Then open Claude Code and say: "ingest the new paper in raw/"
```

## Deploy

Every push to `main` triggers [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) which builds and publishes to GitHub Pages.

## License

Source material (PDFs in `raw/papers/`) retains its original arXiv licensing. Wiki synthesis content is owned by the repo owner.
