#!/usr/bin/env python3
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
"""
Fetch and convert arXiv papers to markdown for wiki ingestion.

Usage:
    python ingest_arxiv.py 1706.03762
    python ingest_arxiv.py https://arxiv.org/abs/2301.13848
    python ingest_arxiv.py --batch papers.txt
    python ingest_arxiv.py --search "transformer market making" --max 5
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

import arxiv
import requests
from rich.console import Console
from rich.panel import Panel

console = Console(legacy_windows=False)
RAW_DIR = Path(__file__).parent.parent / "raw" / "papers"


def extract_arxiv_id(input_str: str) -> str:
    """Extract arXiv ID from URL or direct ID."""
    patterns = [
        r"arxiv\.org/abs/(\d{4}\.\d{4,5})(v\d+)?",
        r"arxiv\.org/pdf/(\d{4}\.\d{4,5})(v\d+)?",
        r"^(\d{4}\.\d{4,5})(v\d+)?$",
    ]
    for pattern in patterns:
        match = re.search(pattern, input_str)
        if match:
            return match.group(1)
    return input_str  # Return as-is, let arxiv library handle errors


def download_and_convert(arxiv_id: str) -> dict:
    """Download PDF and convert to markdown."""
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    pdf_path = RAW_DIR / f"{arxiv_id}.pdf"
    md_path = RAW_DIR / f"{arxiv_id}.md"

    # Skip if already processed
    if md_path.exists():
        console.print(f"[yellow]Already processed: {arxiv_id}[/yellow]")
        return {"id": arxiv_id, "status": "skipped", "md_path": str(md_path)}

    # Fetch metadata
    console.print(f"[blue]Fetching metadata for {arxiv_id}...[/blue]")
    client = arxiv.Client()
    search = arxiv.Search(id_list=[arxiv_id])
    try:
        paper = next(client.results(search))
    except StopIteration:
        console.print(f"[red]Paper not found: {arxiv_id}[/red]")
        return {"id": arxiv_id, "status": "not_found"}

    console.print(Panel(
        f"[bold]{paper.title}[/bold]\n"
        f"Authors: {', '.join(a.name for a in paper.authors[:5])}\n"
        f"Published: {paper.published.strftime('%Y-%m-%d')}\n"
        f"Categories: {', '.join(paper.categories)}",
        title=f"arXiv:{arxiv_id}"
    ))

    # Download PDF
    if not pdf_path.exists():
        console.print("[blue]Downloading PDF...[/blue]")
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        resp = requests.get(pdf_url, timeout=60)
        resp.raise_for_status()
        pdf_path.write_bytes(resp.content)
        console.print(f"[green]PDF saved: {pdf_path}[/green]")

    # Convert to markdown — try pymupdf4llm (fast, default), then marker (heavy, optional), then abstract fallback
    header = f"""---
title: "{paper.title}"
arxiv_id: "{arxiv_id}"
authors: {[a.name for a in paper.authors]}
published: "{paper.published.strftime('%Y-%m-%d')}"
categories: {paper.categories}
---

# {paper.title}

**Authors**: {', '.join(a.name for a in paper.authors)}
**Published**: {paper.published.strftime('%Y-%m-%d')}
**arXiv**: [{arxiv_id}](https://arxiv.org/abs/{arxiv_id})
**Categories**: {', '.join(paper.categories)}

## Abstract

{paper.summary}

---

"""

    converted = False
    try:
        import pymupdf4llm
        console.print("[blue]Converting to markdown with pymupdf4llm...[/blue]")
        body = pymupdf4llm.to_markdown(str(pdf_path), show_progress=False)
        md_path.write_text(header + "## Full text\n\n" + body, encoding="utf-8")
        converted = True
        console.print(f"[green]Converted ({len(body):,} chars): {md_path}[/green]")
    except ImportError:
        pass
    except Exception as e:
        console.print(f"[yellow]pymupdf4llm failed ({e}); trying marker...[/yellow]")

    if not converted:
        try:
            console.print("[blue]Trying marker-pdf...[/blue]")
            subprocess.run(
                ["marker_single", str(pdf_path), str(RAW_DIR)],
                check=True,
                capture_output=True,
                text=True,
            )
            marker_output = RAW_DIR / pdf_path.stem
            if marker_output.is_dir():
                for f in marker_output.glob("*.md"):
                    f.rename(md_path)
                import shutil
                shutil.rmtree(marker_output, ignore_errors=True)
            converted = True
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

    if not converted:
        console.print("[yellow]No PDF converter available; writing abstract-only markdown.[/yellow]")
        md_path.write_text(
            header + "*Note: Install `pymupdf4llm` or `marker-pdf` for full-text extraction.*\n",
            encoding="utf-8",
        )

    console.print(f"[green]Ready for wiki ingestion: {md_path}[/green]")
    return {
        "id": arxiv_id,
        "title": paper.title,
        "status": "ready",
        "pdf_path": str(pdf_path),
        "md_path": str(md_path),
    }


def search_arxiv(query: str, max_results: int = 5, categories: list[str] | None = None):
    """Search arXiv and list papers for selection."""
    console.print(f"[blue]Searching arXiv for: {query}[/blue]")

    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    client = arxiv.Client()

    results = []
    for i, paper in enumerate(client.results(search)):
        arxiv_id = paper.entry_id.split("/")[-1].split("v")[0]
        if categories:
            if not any(cat in paper.categories for cat in categories):
                continue
        results.append(arxiv_id)
        console.print(
            f"  [{i+1}] [bold]{paper.title}[/bold]\n"
            f"      {arxiv_id} | {paper.published.strftime('%Y-%m-%d')} | "
            f"{', '.join(paper.categories[:3])}"
        )

    return results


def main():
    parser = argparse.ArgumentParser(description="Fetch arXiv papers for wiki ingestion")
    parser.add_argument("arxiv_id", nargs="?", help="arXiv ID or URL")
    parser.add_argument("--batch", help="File with one arXiv ID per line")
    parser.add_argument("--search", help="Search arXiv by query")
    parser.add_argument("--max", type=int, default=5, help="Max results for search")
    args = parser.parse_args()

    if args.search:
        ids = search_arxiv(args.search, args.max)
        console.print(f"\n[bold]Found {len(ids)} papers. To ingest:[/bold]")
        for arxiv_id in ids:
            console.print(f"  python ingest_arxiv.py {arxiv_id}")
        return

    if args.batch:
        batch_file = Path(args.batch)
        if not batch_file.exists():
            console.print(f"[red]Batch file not found: {args.batch}[/red]")
            sys.exit(1)
        ids = [line.strip() for line in batch_file.read_text().splitlines() if line.strip()]
    elif args.arxiv_id:
        ids = [extract_arxiv_id(args.arxiv_id)]
    else:
        parser.print_help()
        sys.exit(1)

    results = []
    for arxiv_id in ids:
        result = download_and_convert(arxiv_id)
        results.append(result)

    # Summary
    ready = [r for r in results if r["status"] == "ready"]
    skipped = [r for r in results if r["status"] == "skipped"]
    console.print(f"\n[bold green]{len(ready)} papers ready for ingestion[/bold green]")
    if skipped:
        console.print(f"[yellow]  {len(skipped)} already processed (skipped)[/yellow]")
    console.print("\n[bold]Next step:[/bold] Open Claude Code and say:")
    console.print('  [italic]"ingest the new papers in raw/"[/italic]')


if __name__ == "__main__":
    main()
