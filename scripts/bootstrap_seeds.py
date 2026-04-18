#!/usr/bin/env python3
"""
Bootstrap the seed corpus: download seed papers and expand via Semantic Scholar.

Usage:
    python bootstrap_seeds.py                  # Full bootstrap
    python bootstrap_seeds.py --seeds-only     # Just download seed papers
    python bootstrap_seeds.py --expand-only    # Just expand via citations
    python bootstrap_seeds.py --dry-run        # Show what would be fetched
"""

import argparse
import json
import time
from pathlib import Path

import requests
from rich.console import Console
from rich.table import Table

from discovery_config import (
    SEED_PAPERS,
    SEED_PAPERS_NON_ARXIV,
    SEMANTIC_SCHOLAR_CONFIG,
    TIER1_MUST_INGEST,
    TIER2_LIKELY_RELEVANT,
)

console = Console()
S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_REC_BASE = "https://api.semanticscholar.org/recommendations/v1"
RAW_DIR = Path(__file__).parent.parent / "raw" / "papers"
METADATA_DIR = Path(__file__).parent.parent / "raw" / "metadata"


def s2_search_by_title(title: str) -> dict | None:
    """Find a paper on Semantic Scholar by title."""
    resp = requests.get(
        f"{S2_BASE}/paper/search",
        params={"query": title, "limit": 1, "fields": "paperId,title,externalIds,citationCount,year"},
        timeout=15,
    )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("data"):
            return data["data"][0]
    return None


def s2_get_paper(paper_id: str) -> dict | None:
    """Get paper details from Semantic Scholar."""
    resp = requests.get(
        f"{S2_BASE}/paper/{paper_id}",
        params={"fields": "paperId,title,abstract,externalIds,citationCount,year,authors,venue"},
        timeout=15,
    )
    if resp.status_code == 200:
        return resp.json()
    return None


def s2_get_citations(paper_id: str, limit: int = 50) -> list[dict]:
    """Get papers that cite this paper."""
    resp = requests.get(
        f"{S2_BASE}/paper/{paper_id}/citations",
        params={"fields": "paperId,title,abstract,externalIds,citationCount,year", "limit": limit},
        timeout=30,
    )
    if resp.status_code == 200:
        return [c["citingPaper"] for c in resp.json().get("data", []) if c.get("citingPaper")]
    return []


def s2_get_references(paper_id: str, limit: int = 20) -> list[dict]:
    """Get papers this paper cites."""
    resp = requests.get(
        f"{S2_BASE}/paper/{paper_id}/references",
        params={"fields": "paperId,title,abstract,externalIds,citationCount,year", "limit": limit},
        timeout=30,
    )
    if resp.status_code == 200:
        return [r["citedPaper"] for r in resp.json().get("data", []) if r.get("citedPaper")]
    return []


def s2_get_recommendations(paper_id: str, limit: int = 20) -> list[dict]:
    """Get recommended similar papers."""
    resp = requests.post(
        f"{S2_REC_BASE}/papers",
        json={"positivePaperIds": [paper_id]},
        params={"fields": "paperId,title,abstract,externalIds,citationCount,year", "limit": limit},
        timeout=30,
    )
    if resp.status_code == 200:
        return resp.json().get("recommendedPapers", [])
    return []


def matches_keywords(text: str) -> tuple[int, str]:
    """Check if text matches any keyword tier. Returns (tier, matched_keyword)."""
    if not text:
        return (0, "")
    text_lower = text.lower()
    for kw in TIER1_MUST_INGEST:
        if kw.lower() in text_lower:
            return (1, kw)
    for kw in TIER2_LIKELY_RELEVANT:
        if kw.lower() in text_lower:
            return (2, kw)
    return (0, "")


def get_arxiv_id(paper: dict) -> str | None:
    """Extract arXiv ID from Semantic Scholar paper data."""
    ext = paper.get("externalIds", {})
    return ext.get("ArXiv")


def save_metadata(papers: list[dict], filename: str):
    """Save paper metadata to JSON for reference."""
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    path = METADATA_DIR / filename
    with open(path, "w") as f:
        json.dump(papers, f, indent=2)
    console.print(f"[dim]Metadata saved: {path}[/dim]")


def bootstrap_seeds(dry_run: bool = False):
    """Download all seed papers."""
    console.print("[bold]Phase 1: Downloading seed papers[/bold]\n")

    # arXiv seeds
    arxiv_ids = []
    for arxiv_id, desc in SEED_PAPERS:
        console.print(f"  [blue]{arxiv_id}[/blue] — {desc}")
        arxiv_ids.append(arxiv_id)

    if not dry_run:
        # Write batch file for ingest_arxiv.py
        batch_file = Path(__file__).parent / "seed_batch.txt"
        batch_file.write_text("\n".join(arxiv_ids))
        console.print(f"\n[green]Batch file written: {batch_file}[/green]")
        console.print("[bold]Run:[/bold] python ingest_arxiv.py --batch seed_batch.txt")

    # Non-arXiv seeds (search Semantic Scholar)
    console.print(f"\n[bold]Searching Semantic Scholar for {len(SEED_PAPERS_NON_ARXIV)} non-arXiv papers...[/bold]")
    found_non_arxiv = []
    for title in SEED_PAPERS_NON_ARXIV:
        paper = s2_search_by_title(title)
        if paper:
            arxiv_id = get_arxiv_id(paper)
            status = f"arXiv:{arxiv_id}" if arxiv_id else f"S2:{paper['paperId'][:8]}..."
            console.print(f"  [green]✓[/green] {title[:60]}... → {status}")
            found_non_arxiv.append(paper)
            if arxiv_id:
                arxiv_ids.append(arxiv_id)
        else:
            console.print(f"  [red]✗[/red] {title[:60]}... — not found")
        time.sleep(0.5)  # Rate limit

    save_metadata(found_non_arxiv, "seed_non_arxiv.json")
    console.print(f"\n[bold green]Total seed papers: {len(arxiv_ids)} arXiv + {len(found_non_arxiv)} other[/bold green]")
    return arxiv_ids


def expand_via_citations(seed_arxiv_ids: list[str], dry_run: bool = False):
    """Expand seed corpus via Semantic Scholar citation graph."""
    console.print("\n[bold]Phase 2: Expanding via citation graph[/bold]\n")

    config = SEMANTIC_SCHOLAR_CONFIG
    all_expanded = {}  # arxiv_id -> paper_info
    seen_s2_ids = set()

    for i, arxiv_id in enumerate(seed_arxiv_ids[:10]):  # Limit to first 10 seeds for API rate limits
        console.print(f"[blue]({i+1}/{min(len(seed_arxiv_ids), 10)}) Expanding arXiv:{arxiv_id}...[/blue]")

        # Get S2 paper ID
        paper = s2_get_paper(f"ArXiv:{arxiv_id}")
        if not paper:
            console.print(f"  [yellow]Not found on S2, skipping[/yellow]")
            time.sleep(1)
            continue

        s2_id = paper["paperId"]
        seen_s2_ids.add(s2_id)

        # Get citations (newer work)
        citations = s2_get_citations(s2_id, config["max_citations"])
        time.sleep(0.5)

        # Get references (older foundational work)
        references = s2_get_references(s2_id, config["max_references"])
        time.sleep(0.5)

        # Get recommendations
        recommendations = []
        if config["use_recommendations"]:
            recommendations = s2_get_recommendations(s2_id, config["recommendation_limit"])
            time.sleep(0.5)

        # Filter and collect
        candidates = citations + references + recommendations
        for p in candidates:
            if not p or not p.get("paperId"):
                continue
            if p["paperId"] in seen_s2_ids:
                continue
            seen_s2_ids.add(p["paperId"])

            # Apply filters
            cite_count = p.get("citationCount", 0) or 0
            year = p.get("year") or 0

            if cite_count < config["min_citation_count"]:
                continue
            if year < 2011:
                continue

            # Keyword check
            searchable = f"{p.get('title', '')} {p.get('abstract', '')}"
            tier, keyword = matches_keywords(searchable)

            if config["require_keywords"] and tier == 0:
                continue

            aid = get_arxiv_id(p)
            if aid and aid not in all_expanded:
                all_expanded[aid] = {
                    "arxiv_id": aid,
                    "title": p.get("title", ""),
                    "year": year,
                    "citations": cite_count,
                    "tier": tier,
                    "matched_keyword": keyword,
                    "source_seed": arxiv_id,
                }

        console.print(f"  Found {len(citations)} citations, {len(references)} references, {len(recommendations)} recommendations")
        time.sleep(1)  # Rate limit between seeds

    # Summary
    table = Table(title=f"Expanded corpus: {len(all_expanded)} papers")
    table.add_column("arXiv ID", style="blue")
    table.add_column("Title", max_width=50)
    table.add_column("Year")
    table.add_column("Cites", justify="right")
    table.add_column("Tier", justify="center")
    table.add_column("Keyword", max_width=25)

    sorted_papers = sorted(all_expanded.values(), key=lambda x: (-x["tier"], -x["citations"]))
    for p in sorted_papers[:30]:  # Show top 30
        tier_color = {1: "green", 2: "yellow"}.get(p["tier"], "dim")
        table.add_row(
            p["arxiv_id"],
            p["title"][:50],
            str(p["year"]),
            str(p["citations"]),
            f"[{tier_color}]T{p['tier']}[/{tier_color}]",
            p["matched_keyword"][:25],
        )

    console.print(table)
    if len(all_expanded) > 30:
        console.print(f"[dim]  ... and {len(all_expanded) - 30} more[/dim]")

    # Save
    save_metadata(sorted_papers, "expanded_corpus.json")

    if not dry_run:
        batch_file = Path(__file__).parent / "expanded_batch.txt"
        batch_file.write_text("\n".join(p["arxiv_id"] for p in sorted_papers))
        console.print(f"\n[green]Batch file written: {batch_file}[/green]")
        console.print("[bold]Run:[/bold] python ingest_arxiv.py --batch expanded_batch.txt")

    return all_expanded


def main():
    parser = argparse.ArgumentParser(description="Bootstrap seed corpus and expand via citations")
    parser.add_argument("--seeds-only", action="store_true", help="Only download seed papers")
    parser.add_argument("--expand-only", action="store_true", help="Only expand via citations")
    parser.add_argument("--dry-run", action="store_true", help="Show plan without downloading")
    args = parser.parse_args()

    seed_ids = [arxiv_id for arxiv_id, _ in SEED_PAPERS]

    if not args.expand_only:
        seed_ids = bootstrap_seeds(dry_run=args.dry_run)

    if not args.seeds_only:
        expand_via_citations(seed_ids, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
