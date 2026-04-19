#!/usr/bin/env python3
"""Preflight check for MathJax rendering on the MkDocs site.

Validates the four regression-prone conditions that broke math rendering three
times in April 2026 (see wiki/log.md). Invoked by the wiki-deploy skill before
`mkdocs build`. Exits non-zero with a specific failure code if any check fails.

Checks:
    M — mkdocs.yml
        M1: `extra_javascript` block is present.
        M2: `mathjax-config.js` is listed in `extra_javascript`.
        M3: MathJax CDN is listed in `extra_javascript`.
        M4: config script loads BEFORE the CDN (else window.MathJax is ignored).
    C — site/docs/javascripts/mathjax-config.js
        C1: tex.inlineMath and tex.displayMath delimiter arrays exist.
        C2: neither array contains a bare $-delimiter (conflicts with arithmatex).
        C3: document$.subscribe is called (required for SPA-nav re-typeset).
        C4: document$ access is guarded (typeof check + setTimeout retry).
        C5: MathJax.typesetClear is called on navigation.
        C6: MathJax.startup.output.clearCache is called on navigation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "[preflight-mathjax] PyYAML not installed — run `pip install pyyaml`",
        file=sys.stderr,
    )
    sys.exit(2)


REPO_ROOT = Path(__file__).resolve().parent.parent
MKDOCS_YML = REPO_ROOT / "site" / "mkdocs.yml"
MATHJAX_CONFIG = REPO_ROOT / "site" / "docs" / "javascripts" / "mathjax-config.js"


def fail(code: str, msg: str) -> None:
    print(f"[preflight-mathjax] FAIL {code}: {msg}", file=sys.stderr)
    sys.exit(1)


def check_load_order() -> None:
    if not MKDOCS_YML.exists():
        fail("M0", f"{MKDOCS_YML} not found")

    raw = MKDOCS_YML.read_text(encoding="utf-8")
    # mkdocs.yml uses !!python/name:... for custom fences — strip those before
    # safe_load, since we only care about extra_javascript here.
    raw = re.sub(r"!!python/name:\S+", '""', raw)

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as e:
        fail("M1", f"mkdocs.yml is not valid YAML: {e}")

    entries = data.get("extra_javascript") if isinstance(data, dict) else None
    if not entries:
        fail("M1", "no extra_javascript entries in mkdocs.yml")

    config_idx = next(
        (i for i, e in enumerate(entries) if isinstance(e, str) and "mathjax-config" in e),
        None,
    )
    cdn_idx = next(
        (
            i
            for i, e in enumerate(entries)
            if isinstance(e, str) and e.startswith("http") and "mathjax" in e.lower()
        ),
        None,
    )

    if config_idx is None:
        fail("M2", "mathjax-config.js not listed in extra_javascript")
    if cdn_idx is None:
        fail("M3", "MathJax CDN URL not listed in extra_javascript")
    if config_idx > cdn_idx:
        fail(
            "M4",
            f"mathjax-config.js (position {config_idx}) must load BEFORE the MathJax CDN "
            f"(position {cdn_idx}); window.MathJax is ignored otherwise",
        )


def check_config_js() -> None:
    if not MATHJAX_CONFIG.exists():
        fail("C0", f"{MATHJAX_CONFIG} not found")

    text = MATHJAX_CONFIG.read_text(encoding="utf-8")
    stripped = re.sub(r"//.*", "", text)
    stripped = re.sub(r"/\*[\s\S]*?\*/", "", stripped)

    for key in ("inlineMath", "displayMath"):
        m = re.search(rf"\b{key}\s*:\s*(\[[^\]]*\])", stripped)
        if not m:
            fail("C1", f"mathjax-config.js missing tex.{key} delimiter list")
        arr = m.group(1)
        if re.search(r"""["']\$+["']""", arr):
            fail(
                "C2",
                f"tex.{key} contains a bare $-delimiter — conflicts with "
                f"arithmatex(generic: true); use only \\\\(...\\\\) / \\\\[...\\\\]",
            )

    if "document$.subscribe" not in stripped:
        fail(
            "C3",
            "mathjax-config.js missing document$.subscribe; MathJax will not re-typeset "
            "after Material instant-navigation page swaps",
        )
    if not re.search(r"typeof\s+document\$\s*===\s*['\"]undefined['\"]", stripped):
        fail(
            "C4",
            "document$.subscribe is not guarded (no `typeof document$ === \"undefined\"` "
            "check) — document$ is not defined at script-parse time; add a guard and "
            "setTimeout retry",
        )

    for fn, code in (("typesetClear", "C5"), ("clearCache", "C6")):
        if fn not in stripped:
            fail(
                code,
                f"mathjax-config.js does not call MathJax.{fn} on navigation; "
                f"subsequent pages render stale after SPA page swaps",
            )


def main() -> int:
    check_load_order()
    check_config_js()
    print("[preflight-mathjax] OK — all static checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
