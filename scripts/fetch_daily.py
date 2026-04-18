#!/usr/bin/env python3
"""
Daily arXiv fetch: poll categories, filter by keywords, download matches.

Usage:
    python fetch_daily.py
    python fetch_daily.py --categories "q-fin.TR,q-fin.MF" --max 5
    python fetch_daily.py --dry-run
"""

import argparse
import datetime
import re
from pathlib import Path

import arxiv
import requests
from rich.console import Console
from rich.table import Table

from discovery_config import (
    PRIMARY_CATEGORIES,
    CROSSLIST_CATEGORIES,
    TIER1_MUST_INGEST,
    TIER2_LIKELY_RELEVANT,
    TIER3_CONTEXT,
    DAILY_FETCH_CONFIG,
)

console = Console()
RAW_DIR = Path(__file__).parent.parent / "raw" / "papers"


def _keyword_matches(kw: str, text_lower: str, text_original: str) -> bool:
    """Match a keyword against text.

    - Short uppercase acronyms (<=5 chars, all caps, no spaces) require
      word-boundary match against the original-case text. This stops "OBI" from
      matching "obi" inside "symbiotic" / "OBJ-" etc. and requires the uppercase
      form (which is how acronyms appear in papers).
    - Everything else falls back to a lowercase substring match, so phrases
      like "limit order book" match naturally.
    """
    is_short_acronym = (
        len(kw) <= 5 and kw.isupper() and kw.isalpha()
    )
    if is_short_acronym:
        return re.search(rf"\b{re.escape(kw)}\b", text_original) is not None
    return kw.lower() in text_lower


def matches_tier(title: str, abstract: str) -> tuple[int, str]:
    """Check which keyword tier a paper matches. Returns (tier, keyword)."""
    text_original = f"{title} {abstract}"
    text_lower = text_original.lower()

    for kw in TIER1_MUST_INGEST:
        if _keyword_matches(kw, text_lower, text_original):
            return (1, kw)
    for kw in TIER2_LIKELY_RELEVANT:
        if _keyword_matches(kw, text_lower, text_original):
            return (2, kw)
    for kw in TIER3_CONTEXT:
        if _keyword_matches(kw, text_lower, text_original):
            return (3, kw)
    return (0, "")


def is_primary_category(categories: list[str]) -> bool:
    """Check if paper has a primary q-fin category."""
    return any(cat in PRIMARY_CATEGORIES for cat in categories)


def fetch_daily(
    categories: list[str] | None = None,
    keywords: str | None = None,
    max_papers: int = 10,
    lookback_days: int = 1,
    output_dir: str | None = None,
    dry_run: bool = False,
):
    """Fetch new papers from arXiv matching our criteria."""
    if categories is None:
        categories = PRIMARY_CATEGORIES + CROSSLIST_CATEGORIES
    if output_dir:
        raw_dir = Path(output_dir)
    else:
        raw_dir = RAW_DIR

    raw_dir.mkdir(parents=True, exist_ok=True)

    # Build arXiv query
    cat_query = " OR ".join(f"cat:{cat}" for cat in categories)
    query = f"({cat_query})"

    # Add keyword filter if provided (command line override)
    if keywords:
        kw_list = [kw.strip() for kw in keywords.split(",")]
        kw_query = " OR ".join(f'all:"{kw}"' for kw in kw_list)
        query = f"({cat_query}) AND ({kw_query})"

    console.print(f"[blue]Querying arXiv...[/blue]")
    console.print(f"[dim]Categories: {', '.join(categories)}[/dim]")
    console.print(f"[dim]Lookback: {lookback_days} day(s)[/dim]")

    # Fetch recent papers
    search = arxiv.Search(
        query=query,
        max_results=200,  # Fetch more, filter locally
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    client = arxiv.Client()
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=lookback_days + 1)

    tier1_papers = []
    tier2_papers = []
    tier3_papers = []

    for paper in client.results(search):
        # Check date
        if paper.published.replace(tzinfo=datetime.timezone.utc) < cutoff:
            break

        arxiv_id = paper.entry_id.split("/")[-1].split("v")[0]
        # Remove version suffix
        arxiv_id = re.sub(r"v\d+$", "", arxiv_id)

        # Skip if already downloaded
        if (raw_dir / f"{arxiv_id}.md").exists() or (raw_dir / f"{arxiv_id}.pdf").exists():
            continue

        # Check keyword tier
        tier, keyword = matches_tier(paper.title, paper.summary)

        if tier == 0:
            continue

        paper_info = {
            "arxiv_id": arxiv_id,
            "title": paper.title,
            "authors": [a.name for a in paper.authors[:3]],
            "categories": paper.categories,
            "published": paper.published.strftime("%Y-%m-%d"),
            "tier": tier,
            "keyword": keyword,
            "is_primary": is_primary_category(paper.categories),
        }

        if tier == 1:
            tier1_papers.append(paper_info)
        elif tier == 2 and paper_info["is_primary"]:
            tier2_papers.append(paper_info)
        elif tier == 2:
            tier3_papers.append(paper_info)  # Downgrade to tier 3 if not primary category
        elif tier == 3:
            tier3_papers.append(paper_info)

    # Summary table
    all_papers = tier1_papers + tier2_papers + tier3_papers

    if not all_papers:
        console.print("[yellow]No new papers found matching criteria.[/yellow]")
        return

    table = Table(title=f"New papers found: {len(all_papers)}")
    table.add_column("Tier", justify="center", width=4)
    table.add_column("arXiv ID", style="blue", width=12)
    table.add_column("Title", max_width=45)
    table.add_column("Keyword", max_width=20)
    table.add_column("Action", width=10)

    to_download = []

    for p in tier1_papers:
        table.add_row("[green]T1[/green]", p["arxiv_id"], p["title"][:45], p["keyword"][:20], "[green]INGEST[/green]")
        to_download.append(p["arxiv_id"])

    for p in tier2_papers:
        table.add_row("[yellow]T2[/yellow]", p["arxiv_id"], p["title"][:45], p["keyword"][:20], "[yellow]INGEST[/yellow]")
        to_download.append(p["arxiv_id"])

    for p in tier3_papers:
        table.add_row("[dim]T3[/dim]", p["arxiv_id"], p["title"][:45], p["keyword"][:20], "[dim]REVIEW[/dim]")

    console.print(table)

    # Limit downloads
    to_download = to_download[:max_papers]

    if dry_run:
        console.print(f"\n[yellow]DRY RUN — would download {len(to_download)} papers[/yellow]")
        return

    # Download
    if to_download:
        console.print(f"\n[bold]Downloading {len(to_download)} papers...[/bold]")
        for arxiv_id in to_download:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            pdf_path = raw_dir / f"{arxiv_id}.pdf"
            try:
                resp = requests.get(pdf_url, timeout=60)
                resp.raise_for_status()
                pdf_path.write_bytes(resp.content)
                console.print(f"  [green]✓[/green] {arxiv_id}")
            except Exception as e:
                console.print(f"  [red]✗[/red] {arxiv_id} — {e}")

        console.print(f"\n[green]Done. {len(to_download)} PDFs saved to {raw_dir}[/green]")
        console.print("[bold]Next:[/bold] Open Claude Code and say: \"ingest the new papers in raw/\"")

    # Log tier 3 for manual review
    if tier3_papers:
        review_file = raw_dir.parent / "review_queue.txt"
        with open(review_file, "a") as f:
            f.write(f"\n# {datetime.date.today()}\n")
            for p in tier3_papers:
                f.write(f"{p['arxiv_id']} | T{p['tier']} | {p['keyword']} | {p['title'][:80]}\n")
        console.print(f"[dim]Tier 3 papers logged to {review_file}[/dim]")


def main():
    parser = argparse.ArgumentParser(description="Daily arXiv paper fetch")
    parser.add_argument("--categories", help="Comma-separated arXiv categories")
    parser.add_argument("--keywords", help="Comma-separated keywords (overrides config)")
    parser.add_argument("--max", type=int, default=DAILY_FETCH_CONFIG["max_papers_per_day"])
    parser.add_argument("--lookback", type=int, default=DAILY_FETCH_CONFIG["lookback_days"])
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    cats = args.categories.split(",") if args.categories else None
    fetch_daily(
        categories=cats,
        keywords=args.keywords,
        max_papers=args.max,
        lookback_days=args.lookback,
        output_dir=args.output,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
