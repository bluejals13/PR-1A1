#!/usr/bin/env python3
"""
Slide Scaffold Creator CLI.

Analyzes original presentation HTML files to generate JSON data scaffolds,
Jinja2 template scaffolds, and structure parity baselines without AI dependency.

Enforces human-in-the-loop review:
- Generates candidates, never assumes business semantics.
- Preserves 100% of the original DOM structure in template scaffold.
- Emits 'HUMAN REVIEW REQUIRED' notices.

Usage:
  python automation/create_slide.py --slide 008
  python automation/create_slide.py --slide 008 --force
  python automation/create_slide.py --input "PRD-PO/html/분리된 html/8번 슬라이드.html"
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

# Add current directory to path for local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from analyze import (
    ContentDetector,
    DependencyAnalyzer,
    HTMLAnalyzer,
    StructureFingerprint,
)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def resolve_slide_info(slide_input: str):
    """Normalizes slide input into standard identifiers (e.g. '008' -> '008', 8)."""
    s = str(slide_input).strip()
    if s.isdigit():
        num = int(s)
        key = f"{num:03d}"
    else:
        num = s
        key = s
    return key, num


def find_original_html(repo_root: Path, slide_num: Any) -> Path:
    """Locates the original HTML file in the primary separated html directory."""
    candidates = [
        repo_root / "PRD-PO" / "html" / "분리된 html" / f"{slide_num}번 슬라이드.html",
        repo_root / "PRD-PO" / "html" / "분리된 html" / f"{slide_num}번 슬라이드.original.html",
    ]
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


def create_slide_scaffold(
    original_html_path: Path,
    slide_id: str,
    output_dir: Path,
    force: bool = False
) -> bool:
    slide_key, slide_num = resolve_slide_info(slide_id)
    print(f"[ANALYZE] [Slide {slide_key}] Inspecting original HTML: {original_html_path}")

    if not original_html_path.exists():
        print(f"[ERROR] Original HTML file not found: {original_html_path}", file=sys.stderr)
        return False

    try:
        with open(original_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read HTML file: {e}", file=sys.stderr)
        return False

    # 1. DOM Tree Parsing
    analyzer = HTMLAnalyzer()
    root = analyzer.parse(html_content)
    print(f"  ✓ DOM parsed: {analyzer.get_element_count()} elements, max depth {analyzer.get_max_depth()}")

    # 2. Dependency Analysis
    dep_analyzer = DependencyAnalyzer()
    deps = dep_analyzer.analyze(root)
    print(f"  ✓ Dependencies detected: {len(deps['stylesheets'])} stylesheets, {len(deps['scripts'])} scripts")
    runtime_info = deps.get("runtime_contract", {})
    print(f"  ✓ Runtime contract: data-slide='{runtime_info.get('data_slide')}', has_speaker_note={runtime_info.get('has_speaker_note')}")

    # 3. Content Candidate Detection
    content_detector = ContentDetector()
    candidates = content_detector.detect_candidates(root)
    repeats = content_detector.detect_repeated_structures(root)
    print(f"  ✓ Content candidates: {len(candidates)} text nodes flagged for review")
    print(f"  ✓ Repeated structures: {len(repeats)} potential loop groups detected")

    # 4. Structure Fingerprint Baseline
    fingerprint = StructureFingerprint.generate(root)
    baseline_dir = output_dir / "dist"
    baseline_dir.mkdir(parents=True, exist_ok=True)
    baseline_path = baseline_dir / f"baseline_slide_{slide_key}.json"
    with open(baseline_path, "w", encoding="utf-8") as f:
        json.dump(fingerprint, f, ensure_ascii=False, indent=2)
    print(f"[BASELINE] Structural fingerprint saved to: {baseline_path}")

    # 5. Generate JSON Scaffold
    data_dir = output_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    json_path = data_dir / f"slide_{slide_key}.json"

    # Extract title if present in DOM
    title_text = f"Slide {slide_num}"
    for title_node in root.find_all(tag="h2"):
        if title_node.text:
            title_text = title_node.text
            break

    # Extract speaker note if present
    speaker_note_text = ""
    for sec_node in root.find_all(tag="section"):
        if "data-speaker-note" in sec_node.attrs:
            speaker_note_text = sec_node.attrs["data-speaker-note"]
            break

    json_scaffold = {
        "HUMAN_REVIEW_REQUIRED": True,
        "_notice": (
            "Generated artifacts are scaffolds. Content semantics were NOT automatically verified. "
            "Review JSON data model and Jinja2 Template before building."
        ),
        "slide_meta": {
            "slide_num": f"SLIDE {slide_key}",
            "title": title_text,
            "header_tag": {
                "text": "REVIEW REQUIRED",
                "class": "info"
            }
        },
        "speaker_note": speaker_note_text,
        "content_candidates": candidates,
        "repeated_structures": repeats,
        "nav": {
            "brand": "APMS.SR / PRESENTATION",
            "hint": "← → 방향키 · Space 다음 · N 발표 노트",
            "counter": f"{slide_key} / 14",
            "runtime_script": "발표용_공통.js"
        }
    }

    if json_path.exists() and not force:
        print(f"[SKIP] JSON data file already exists (use --force to overwrite): {json_path}")
    else:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_scaffold, f, ensure_ascii=False, indent=2)
        print(f"[OUTPUT] JSON scaffold created: {json_path}")

    # 6. Generate Jinja2 Template Scaffold
    templates_dir = output_dir / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    template_path = templates_dir / f"slide_{slide_key}.html.j2"

    if template_path.exists() and not force:
        print(f"[SKIP] Jinja2 template already exists (use --force to overwrite): {template_path}")
    else:
        # Prepend human review notice comment to original HTML
        template_content = (
            "{# ========================================================\n"
            f"   SLIDE {slide_key} TEMPLATE SCAFFOLD\n"
            "   HUMAN REVIEW REQUIRED: Replace static candidate texts with\n"
            "   semantic context variables while preserving original DOM.\n"
            "   ======================================================== #}\n"
            + html_content
        )
        with open(template_path, "w", encoding="utf-8") as f:
            f.write(template_content)
        print(f"[OUTPUT] Jinja2 template scaffold created: {template_path}")

    # 7. Print Human Review Required Notice
    print("\n" + "=" * 60)
    print("⚠️   HUMAN REVIEW REQUIRED")
    print("=" * 60)
    print("1. Generated artifacts are initial scaffolds, NOT verified production code.")
    print("2. Content candidates were extracted without guessing domain semantics.")
    print(f"3. Please review '{json_path}' and define domain field names.")
    print(f"4. Map domain fields into '{template_path}' without altering DOM classes or IDs.")
    print(f"5. Add validate_slide_{slide_key}() in automation/validate.py before running build.")
    print("=" * 60 + "\n")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Analyze original HTML and create slide automation scaffolds (JSON + Jinja2 + Baseline)"
    )
    parser.add_argument("--slide", type=str, default="008", help="Slide identifier (e.g. 008, 009, 8)")
    parser.add_argument("--input", type=Path, default=None, help="Explicit path to source HTML file")
    parser.add_argument("--output-dir", type=Path, default=None, help="Base automation directory (default: current)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing JSON and template scaffolds")

    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parent
    output_dir = args.output_dir if args.output_dir is not None else base_dir

    slide_key, slide_num = resolve_slide_info(args.slide)

    if args.input is not None:
        source_html = args.input
    else:
        source_html = find_original_html(repo_root, slide_num)

    success = create_slide_scaffold(
        original_html_path=source_html,
        slide_id=slide_key,
        output_dir=output_dir,
        force=args.force
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
