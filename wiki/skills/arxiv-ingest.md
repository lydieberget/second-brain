---
name: arxiv-ingest
description: Ingest an arXiv paper (or batch of papers) into the research wiki. Downloads PDF, converts to full-text markdown via pymupdf4llm, then creates/updates wiki pages following the schema in CLAUDE.md. Invoke when the user says "ingest paper X", "add paper X", "ingest the new papers in raw/", or when a new file appears in raw/papers/.
---

# arxiv-ingest — Ingest an arXiv paper into the wiki

Use this skill whenever a new paper enters the corpus. Follow every step; do not shortcut.

## Step 1 — Get the source into `raw/`

Run the ingest script to download the PDF and convert to full-text markdown:

```bash
python scripts/ingest_arxiv.py <arxiv_id_or_url>
# Or for a batch file:
python scripts/ingest_arxiv.py --batch <path/to/batch.txt>
# Or search-then-choose:
python scripts/ingest_arxiv.py --search "<query>" --max 5
```

The script writes `raw/papers/<id>.pdf` and `raw/papers/<id>.md`. Conversion uses `pymupdf4llm` (primary) with `marker-pdf` as optional upgrade.

**Verify before continuing**: open the markdown, confirm the title matches the requested arXiv ID. A common failure mode is arxiv IDs that decode to unrelated papers (happened twice in 2026-04-17 batch). If the title doesn't match, delete the raw files and search arXiv by title for the correct ID.

## Step 2 — Read the raw markdown fully

Read `raw/papers/<id>.md` end to end. Note:
- Title, authors, affiliations, year, arXiv category.
- Abstract and contribution claims.
- **Every named formula, technique, or model** — this is the enumeration that drives method-page creation (Step 4).
- Data used (instruments, venues, date ranges, sample sizes).
- Empirical results with their magnitudes.
- Limitations acknowledged.
- Citations to other work already in the wiki.

## Step 3 — Create the paper page

Write `wiki/papers/<slug>.md` following the frontmatter and page conventions in CLAUDE.md. A paper page must contain:

- YAML frontmatter with `title`, `type: paper`, `created`, `updated`, `sources`, `tags`, `related`, `confidence`.
- Authors, institution, year, arXiv ID, categories.
- Plain-language abstract (your synthesis, not a copy).
- Key contributions (numbered list).
- Method summary (with formulas in LaTeX: `$...$` inline, `$$...$$` display).
- Main results (tables where structured).
- Limitations.
- Connections section with wikilinks to other wiki pages.

## Step 4 — Method-promotion rule (MANDATORY)

For every **named formula, technique, or model** the paper introduces or centrally uses, check whether a `wiki/methods/<name>.md` page exists. If not, **create one** unless it's clearly too generic (e.g., "linear regression" alone).

Promotion signal — create a method page if **any** of:
1. The method is referenced by ≥2 papers in the wiki, or is likely to be.
2. The paper's primary contribution is *defining* or *extending* the method.
3. A reader searching "how does X work?" would expect a standalone page.

Examples that should have been promoted but weren't in the 2026-04-17 batch: propagator model, microprice, OFI event decomposition, impact deconvolution, MLOFI construction. Do not repeat that mistake.

## Step 5 — Update related concept pages

For every concept the paper touches that **already has a page**, update it:
- Add the paper's arxiv ID to the `sources:` list in frontmatter.
- Extend the page with any new evidence, formula variants, or empirical findings.
- Add a wikilink from the concept to the new paper.

For concepts that don't have a page but deserve one (use the same promotion signal), create them in `wiki/concepts/`.

## Step 6 — Hunt for cross-paper connections

Before finishing, search the wiki for:
- **Contradictions** — does the new paper claim something that conflicts with an existing wiki page? Flag explicitly in the log and in both pages.
- **Confirmations** — does the new paper confirm a cross-study pattern (e.g., the tick-size regime theme)? Update the relevant connection page (`wiki/connections/`) with the new evidence.
- **Author / institution overlaps** — does the paper share authors with papers already in the wiki? Update the entity page.

## Step 7 — Update `wiki/index.md`

- Bump the paper count.
- Add the new paper to its domain grouping in "By domain".
- Update "Recent additions" with a one-line entry.

## Step 8 — Append to `wiki/log.md`

Write a log entry listing **every page created or updated**, using this format:

```markdown
## <YYYY-MM-DD> — Ingested: "<title>" (<arxiv_id>)
- Created: papers/<slug>.md
- Created: methods/<name>.md        # if a new method was promoted
- Updated: concepts/<name>.md        # list every updated page
- Contradiction flagged: <page>      # if any
```

## Target

**10–20 wiki pages touched per ingested paper.** If you're under 5, you probably skipped Steps 4, 5, or 6. Go back and audit before declaring done.

## Failure modes to avoid

1. **Wrong arXiv ID** → verify title before writing the paper page.
2. **Method references but no method page** → the 2026-04-17 anti-pattern. Trigger the method-promotion rule.
3. **Paper page with only 1 other page touched** → you missed concepts/methods/connections.
4. **Not updating log.md** → breaks the audit trail; future lints can't reconstruct history.
