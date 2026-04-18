---
name: wiki-lint
description: Audit the wiki for structural health problems — orphan pages, broken wikilinks, missing frontmatter, thin pages, contradictions, missing method pages for named formulas referenced across papers. Invoke when the user says "lint", "lint the wiki", "audit the wiki", or "check wiki health".
---

# wiki-lint — Audit the research wiki

Use this skill to run a full structural audit of the wiki before major milestones (end of a batch ingest, before deployment, or periodically as the corpus grows). Report findings and ask before auto-fixing.

## Checks to perform

### 1. Missing frontmatter
Every `wiki/**/*.md` page must have YAML frontmatter with `title`, `type`, `created`, `updated`. Report any page without.

### 2. Broken wikilinks
For every `[[folder/page]]` wikilink, verify the target file exists. Report broken ones.

### 3. Orphan pages
Any page (except `index.md`, `log.md`, `schema.md`) that receives **zero incoming wikilinks** from other wiki pages. Orphans either need integration or removal.

### 4. Thin pages
Any page with fewer than 100 words (excluding frontmatter). Often a sign of stub pages created but never filled in.

### 5. Missing method pages (method-promotion compliance)
For every formula or named technique mentioned in `wiki/papers/*.md` that is referenced ≥2 times across papers, confirm a `wiki/methods/*.md` page exists. Flag ungratified references. This catches the 2026-04-17 compliance failure.

### 6. Contradictions
Scan for pages making conflicting empirical claims on the same topic. Heuristic: look for pages about the same concept with opposed `confidence:` labels or contradictory number ranges. Flag for manual review.

### 7. Stale content
Papers superseded by newer work (check `created:` dates + paper citations). Doesn't mean delete; means flag for review.

### 8. Missing backlinks in `related:`
If page A has a wikilink in its body to page B, page B's frontmatter `related:` should include A. Mutual references make Obsidian / MkDocs backlinks work.

### 9. Index / log sync
- `wiki/index.md` paper count matches actual count in `wiki/papers/`.
- `wiki/log.md` has an entry for every paper in `wiki/papers/` (check by scanning slug appearance).

### 10. Source-file existence
For each `sources:` entry in any page's frontmatter, confirm the file exists in `raw/`.

## Output

Write a lint report as a new section in `wiki/log.md`:

```markdown
## <YYYY-MM-DD> — Lint report
- Total pages scanned: <N>
- Broken wikilinks: <count> — see details below
- Orphans: <count>
- Thin pages: <count>
- Missing method pages: <count>
- Contradictions flagged: <count>
```

## Auto-fix policy

For mechanical issues (missing `updated:` date, missing `related:` backlinks), propose a diff but **ask the user before applying**. For substantive issues (contradictions, missing method pages), always require user decision.

## Target frequency

Run after every batch ingest (>3 papers added) and at least weekly as the corpus grows past 30 pages.

## When the lint script exists

A Python lint script `scripts/lint_wiki.py` is on the roadmap. Until then, perform the checks using `Grep`, `Glob`, and `Read` tools directly. When the script exists, run:

```bash
python scripts/lint_wiki.py --report wiki/log.md
```
