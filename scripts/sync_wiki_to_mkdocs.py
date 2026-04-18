#!/usr/bin/env python3
"""
Sync wiki/ → site/docs/ for MkDocs build.

Rewrites Obsidian [[wikilinks]] into MkDocs-compatible relative markdown links.

Supported wikilink forms:
    [[concepts/order-flow-imbalance]]          -> [order-flow-imbalance](../concepts/order-flow-imbalance.md)
    [[concepts/order-flow-imbalance|OFI]]      -> [OFI](../concepts/order-flow-imbalance.md)
    [[order-flow-imbalance]]                   -> resolved to the first page matching that slug

Usage:
    python scripts/sync_wiki_to_mkdocs.py
    python scripts/sync_wiki_to_mkdocs.py --watch   # re-sync on file changes (requires watchdog)
"""

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.parent
WIKI_DIR = ROOT / "wiki"
DOCS_DIR = ROOT / "site" / "docs"

WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")


def build_page_index(wiki_dir: Path) -> dict[str, str]:
    """Map bare slugs (e.g. 'order-flow-imbalance') to their folder/slug path."""
    index: dict[str, str] = {}
    for md in wiki_dir.rglob("*.md"):
        rel = md.relative_to(wiki_dir).with_suffix("")
        slug = rel.name
        rel_str = rel.as_posix()
        index[rel_str] = rel_str  # full path (folder/slug)
        index.setdefault(slug, rel_str)  # bare slug -> full path (first match wins)
    return index


def rewrite_wikilinks(text: str, source_page: Path, index: dict[str, str]) -> str:
    """Replace [[target]] and [[target|alias]] with MkDocs relative links."""
    source_dir = source_page.parent

    def _replace(match: re.Match) -> str:
        target = match.group(1).strip()
        alias = match.group(2).strip() if match.group(2) else None

        # Strip optional .md suffix the user might have included
        if target.lower().endswith(".md"):
            target = target[:-3]

        resolved = index.get(target)
        if resolved is None:
            # Unknown link: leave a visible marker so lint can catch it later
            label = alias or target
            return f"[{label}](# \"Broken wikilink: {target}\")"

        target_path = DOCS_DIR / f"{resolved}.md"
        try:
            rel_path = Path(
                *_relative_posix(source_dir, target_path).split("/")
            ).as_posix()
        except ValueError:
            rel_path = target_path.as_posix()

        display = alias or Path(resolved).name
        return f"[{display}]({rel_path})"

    return WIKILINK_RE.sub(_replace, text)


def _relative_posix(source_dir: Path, target: Path) -> str:
    """Return target relative to source_dir using forward slashes."""
    # Walk up from source_dir to find the common ancestor, then descend to target.
    source_parts = source_dir.resolve().parts
    target_parts = target.resolve().parts
    common = 0
    while (
        common < len(source_parts)
        and common < len(target_parts)
        and source_parts[common] == target_parts[common]
    ):
        common += 1
    ups = [".."] * (len(source_parts) - common)
    downs = list(target_parts[common:])
    return "/".join(ups + downs) if ups or downs else "."


def sync() -> int:
    if not WIKI_DIR.exists():
        raise SystemExit(f"Wiki dir not found: {WIKI_DIR}")

    # Wipe stale content in docs (preserve docs/javascripts/ so mathjax-config survives)
    if DOCS_DIR.exists():
        for item in DOCS_DIR.iterdir():
            if item.name == "javascripts":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    index = build_page_index(WIKI_DIR)

    copied = 0
    rewritten = 0
    for src in WIKI_DIR.rglob("*.md"):
        rel = src.relative_to(WIKI_DIR)
        dst = DOCS_DIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        text = src.read_text(encoding="utf-8")
        new_text = rewrite_wikilinks(text, dst, index)
        if new_text != text:
            rewritten += 1
        dst.write_text(new_text, encoding="utf-8")
        copied += 1

    print(f"Synced {copied} pages ({rewritten} had wikilinks rewritten) to {DOCS_DIR}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watch", action="store_true", help="Re-sync on file changes")
    args = parser.parse_args()

    if args.watch:
        try:
            from watchdog.events import FileSystemEventHandler
            from watchdog.observers import Observer
        except ImportError:
            raise SystemExit("watchdog not installed: pip install watchdog")

        import time

        class Handler(FileSystemEventHandler):
            def on_any_event(self, event):
                if event.is_directory or not str(event.src_path).endswith(".md"):
                    return
                try:
                    sync()
                except Exception as exc:
                    print(f"Sync failed: {exc}")

        sync()
        observer = Observer()
        observer.schedule(Handler(), str(WIKI_DIR), recursive=True)
        observer.start()
        print(f"Watching {WIKI_DIR}... Ctrl+C to stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    else:
        sync()


if __name__ == "__main__":
    main()
