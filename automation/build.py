#!/usr/bin/env python3
"""
Presentation Document Automation Build Script.

Supports single and multi-slide builds via CLI parameters:
  python build.py --slide 004
  python build.py --slide 005
  python build.py --slide 004 --output /custom/path.html

Reads source presentation data (JSON), validates and normalizes fields via validate.py,
renders using Jinja2 template, and writes output HTML without altering CSS or layout.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add current directory to path for local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import JinjaRenderer, RenderError, Renderer
from validate import ValidationError, normalize_slide_data, validate_slide_data

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


def resolve_slide_info(slide_input: str):
    """Normalizes slide input into standard identifiers (e.g. '004' -> '004', 4)."""
    s = str(slide_input).strip()
    if s.isdigit():
        num = int(s)
        key = f"{num:03d}"
    else:
        num = s
        key = s
    return key, num


def get_slide_paths(slide_input: str = "004"):
    """Computes default file paths for a specific slide identifier."""
    base_dir = Path(__file__).resolve().parent
    repo_root = base_dir.parent
    
    slide_key, slide_num = resolve_slide_info(slide_input)
    
    data_path = base_dir / "data" / f"slide_{slide_key}.json"
    template_dir = base_dir / "templates"
    template_name = f"slide_{slide_key}.html.j2"
    
    # Primary presentation target in existing separated slides
    default_output = repo_root / "PRD-PO" / "html" / "분리된 html" / f"{slide_num}번 슬라이드.html"
    dist_output = base_dir / "dist" / f"{slide_num}번 슬라이드.html"
    
    return base_dir, repo_root, slide_key, data_path, template_dir, template_name, default_output, dist_output


def build_slide(
    data_path: Path,
    template_dir: Path,
    template_name: str,
    output_path: Path,
    dist_path: Path = None,
    slide_id: str = "004",
    validate_only: bool = False,
    renderer: Renderer = None
) -> bool:
    slide_key, _ = resolve_slide_info(slide_id)
    print(f"[EXTRACT] [Slide {slide_key}] Loading presentation data from: {data_path}")
    if not data_path.exists():
        print(f"[ERROR] Data file not found: {data_path}", file=sys.stderr)
        return False

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}", file=sys.stderr)
        return False

    # 1. Validate
    print(f"[VALIDATE] [Slide {slide_key}] Running schema and constraint validation...")
    try:
        validate_slide_data(raw_data, slide_id=slide_key)
        print("  ✓ Common design constraints passed (no forbidden styling in data)")
        print(f"  ✓ Schema integrity check passed for slide {slide_key}")
    except ValidationError as ve:
        print(f"[VALIDATION FAILED] {ve}", file=sys.stderr)
        return False

    if validate_only:
        print("[VALIDATE-ONLY] Validation complete. No files written.")
        return True

    # 2. Normalize
    print(f"[NORMALIZE] [Slide {slide_key}] Normalizing data structure for template context...")
    try:
        context = normalize_slide_data(raw_data, slide_id=slide_key)
    except Exception as e:
        print(f"[NORMALIZE ERROR] Failed normalizing data: {e}", file=sys.stderr)
        return False

    # 3. Render
    print(f"[RENDER] [Slide {slide_key}] Rendering template: {template_name} via Renderer")
    renderer = renderer or JinjaRenderer()
    try:
        rendered_html = renderer.render(
            template_name=template_name,
            context=context,
            template_dir=template_dir
        )
    except RenderError as re:
        print(f"[RENDER ERROR] {re}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[RENDER ERROR] Failed rendering template: {e}", file=sys.stderr)
        return False

    # 4. Output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)
    print(f"[OUTPUT] Generated slide written to: {output_path} ({len(rendered_html)} bytes)")

    if dist_path:
        dist_path.parent.mkdir(parents=True, exist_ok=True)
        with open(dist_path, "w", encoding="utf-8") as f:
            f.write(rendered_html)
        print(f"[DIST] Artifact copy written to: {dist_path}")

    print(f"[SUCCESS] Slide {slide_key} build completed successfully.")
    return True


def main():
    parser = argparse.ArgumentParser(description="Build presentation HTML slides via Python + Jinja2")
    parser.add_argument("--slide", type=str, default="004", help="Slide identifier (e.g. 004, 005, 4, 5)")
    parser.add_argument("--data", type=Path, default=None, help="Path to slide JSON data file (optional)")
    parser.add_argument("--template-dir", type=Path, default=None, help="Directory containing Jinja2 templates (optional)")
    parser.add_argument("--template", type=str, default=None, help="Template filename (optional)")
    parser.add_argument("--output", type=Path, default=None, help="Path for generated HTML slide (optional)")
    parser.add_argument("--dist", type=Path, default=None, help="Secondary path for dist/artifact output (optional)")
    parser.add_argument("--validate-only", action="store_true", help="Validate data without rendering")

    args = parser.parse_args()

    base_dir, repo_root, slide_key, def_data, def_tpl_dir, def_tpl_name, def_out, def_dist = get_slide_paths(args.slide)

    data_path = args.data if args.data is not None else def_data
    template_dir = args.template_dir if args.template_dir is not None else def_tpl_dir
    template_name = args.template if args.template is not None else def_tpl_name
    output_path = args.output if args.output is not None else def_out
    dist_path = args.dist if args.dist is not None else def_dist

    success = build_slide(
        data_path=data_path,
        template_dir=template_dir,
        template_name=template_name,
        output_path=output_path,
        dist_path=dist_path,
        slide_id=slide_key,
        validate_only=args.validate_only
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

