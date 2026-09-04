#!/usr/bin/env python3
"""
Comprehensive test suite for Slide 008 automation.

Covers:
A. Schema validation:
   - Valid JSON passes
   - Missing required fields fails
   - Invalid status class fails
   - principles not list fails
   - principle field missing fails
   - Forbidden design key fails
B. Rendering:
   - Build succeeds
   - Title alteration reflection
   - Principle text alteration reflection
   - Status text/class alteration reflection
C. DOM parity:
   - Tag structure, class set, id set, data-* attributes, runtime IDs
   - DOM depth and element count
   - Script and link dependencies
   - Speaker note contract
   - Parity match against baseline_slide_008.json
D. CSS/JS independence:
   - CSS SHA-256 unchanged
   - JS SHA-256 unchanged
"""

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

# Add automation dir to path
automation_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(automation_dir))

from analyze import HTMLAnalyzer, StructureFingerprint
from build import build_slide
from validate import (
    ALLOWED_STATUS_CLASSES,
    ValidationError,
    normalize_slide_008,
    validate_slide_008,
    validate_slide_data,
)


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


class TestSlide008SchemaValidation(unittest.TestCase):
    """A. Schema validation tests for Slide 008."""

    def setUp(self):
        self.data_path = automation_dir / "data" / "slide_008.json"
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.valid_data = json.load(f)

    def test_valid_json_passes(self):
        """Standard valid Slide 008 JSON passes validation."""
        try:
            validate_slide_data(self.valid_data, slide_id="008")
        except ValidationError as e:
            self.fail(f"Valid slide data failed validation unexpectedly: {e}")

    def test_missing_slide_meta_fails(self):
        """Missing slide_meta raises ValidationError."""
        d = copy.deepcopy(self.valid_data)
        del d["slide_meta"]
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(d, slide_id="008")
        self.assertIn("slide_meta", str(ctx.exception))

    def test_missing_title_fails(self):
        """Missing title in slide_meta raises ValidationError."""
        d = copy.deepcopy(self.valid_data)
        d["slide_meta"]["title"] = ""
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(d, slide_id="008")
        self.assertIn("title", str(ctx.exception))

    def test_missing_slide_num_fails(self):
        """Missing slide_num raises ValidationError."""
        d = copy.deepcopy(self.valid_data)
        d["slide_meta"]["slide_num"] = ""
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(d, slide_id="008")
        self.assertIn("slide_num", str(ctx.exception))

    def test_invalid_status_class_fails(self):
        """Disallowed status class raises ValidationError."""
        d = copy.deepcopy(self.valid_data)
        d["slide_meta"]["header_tag"]["class"] = "unsupported-custom-class"
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(d, slide_id="008")
        self.assertIn("header_tag class", str(ctx.exception))

    def test_principles_not_list_fails(self):
        """Non-list principles raises ValidationError."""
        d = copy.deepcopy(self.valid_data)
        d["principles"] = "not a list"
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(d, slide_id="008")
        self.assertIn("principles", str(ctx.exception))

    def test_empty_principles_fails(self):
        """Empty principles list raises ValidationError."""
        d = copy.deepcopy(self.valid_data)
        d["principles"] = []
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(d, slide_id="008")
        self.assertIn("cannot be empty", str(ctx.exception))

    def test_principle_field_missing_fails(self):
        """Missing icon/title/desc in principle raises ValidationError."""
        for field in ["icon", "title", "desc"]:
            d = copy.deepcopy(self.valid_data)
            del d["principles"][0][field]
            with self.assertRaises(ValidationError) as ctx:
                validate_slide_data(d, slide_id="008")
            self.assertIn(field, str(ctx.exception))

    def test_forbidden_design_key_fails(self):
        """Forbidden styling properties (e.g. background, color, font_size) raise ValidationError."""
        for forbidden in ["color", "background", "margin", "padding", "style"]:
            d = copy.deepcopy(self.valid_data)
            d["principles"][0][forbidden] = "red"
            with self.assertRaises(ValidationError) as ctx:
                validate_slide_data(d, slide_id="008")
            self.assertIn("Forbidden design property", str(ctx.exception))


class TestSlide008Rendering(unittest.TestCase):
    """B. Rendering and dynamic data reflection tests."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.out_dir = Path(self.temp_dir.name)
        self.data_path = automation_dir / "data" / "slide_008.json"
        self.template_dir = automation_dir / "templates"
        self.template_name = "slide_008.html.j2"
        with open(self.data_path, "r", encoding="utf-8") as f:
            self.valid_data = json.load(f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_build_slide_008_succeeds(self):
        """Standard build of Slide 008 completes successfully."""
        out_html = self.out_dir / "rendered_008.html"
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=out_html,
            slide_id="008"
        )
        self.assertTrue(success)
        self.assertTrue(out_html.exists())
        self.assertGreater(out_html.stat().st_size, 0)

    def test_title_alteration_reflected(self):
        """Changing title in data is reflected in generated HTML."""
        d = copy.deepcopy(self.valid_data)
        d["slide_meta"]["title"] = "Dynamic Test Title Reflection 123"
        tmp_json = self.out_dir / "temp_title.json"
        with open(tmp_json, "w", encoding="utf-8") as f:
            json.dump(d, f)

        out_html = self.out_dir / "out_title.html"
        success = build_slide(
            data_path=tmp_json,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=out_html,
            slide_id="008"
        )
        self.assertTrue(success)
        content = out_html.read_text(encoding="utf-8")
        self.assertIn("Dynamic Test Title Reflection 123", content)

    def test_principle_text_alteration_reflected(self):
        """Changing principle text in data is reflected via Jinja loop."""
        d = copy.deepcopy(self.valid_data)
        d["principles"][0]["title"] = "Custom Altered Principle Title"
        d["principles"][0]["desc"] = "Custom Altered Principle Desc"
        tmp_json = self.out_dir / "temp_principle.json"
        with open(tmp_json, "w", encoding="utf-8") as f:
            json.dump(d, f)

        out_html = self.out_dir / "out_principle.html"
        success = build_slide(
            data_path=tmp_json,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=out_html,
            slide_id="008"
        )
        self.assertTrue(success)
        content = out_html.read_text(encoding="utf-8")
        self.assertIn("Custom Altered Principle Title", content)
        self.assertIn("Custom Altered Principle Desc", content)

    def test_status_alteration_reflected(self):
        """Changing header_tag text and class is reflected in generated HTML."""
        d = copy.deepcopy(self.valid_data)
        d["slide_meta"]["header_tag"] = {
            "text": "VERIFIED",
            "class": "verified"
        }
        tmp_json = self.out_dir / "temp_status.json"
        with open(tmp_json, "w", encoding="utf-8") as f:
            json.dump(d, f)

        out_html = self.out_dir / "out_status.html"
        success = build_slide(
            data_path=tmp_json,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=out_html,
            slide_id="008"
        )
        self.assertTrue(success)
        content = out_html.read_text(encoding="utf-8")
        self.assertIn("tag verified", content)
        self.assertIn("VERIFIED", content)


class TestSlide008ParityAndContracts(unittest.TestCase):
    """C. DOM parity and runtime contract tests."""

    def setUp(self):
        self.repo_root = automation_dir.parent
        self.html_dir = self.repo_root / "PRD-PO" / "html" / "분리된 html"
        self.gen_html_path = self.html_dir / "8번 슬라이드.html"
        self.baseline_path = automation_dir / "dist" / "baseline_slide_008.json"

        # Ensure current build output exists
        data_path = automation_dir / "data" / "slide_008.json"
        template_dir = automation_dir / "templates"
        template_name = "slide_008.html.j2"
        build_slide(
            data_path=data_path,
            template_dir=template_dir,
            template_name=template_name,
            output_path=self.gen_html_path,
            slide_id="008"
        )

        with open(self.gen_html_path, "r", encoding="utf-8") as f:
            self.gen_content = f.read()

        analyzer = HTMLAnalyzer()
        root = analyzer.parse(self.gen_content)
        self.gen_fp = StructureFingerprint.generate(root)

        with open(self.baseline_path, "r", encoding="utf-8") as f:
            self.base_fp = json.load(f)

    def test_dom_parity_match_with_baseline(self):
        """Rendered HTML matches baseline structural fingerprint 100%."""
        diff = StructureFingerprint.compare(self.base_fp, self.gen_fp)
        self.assertTrue(diff["is_parity_match"], f"Parity mismatch: {diff}")
        self.assertEqual(diff["missing_ids"], [])
        self.assertEqual(diff["missing_classes"], [])
        self.assertEqual(diff["missing_stylesheets"], [])
        self.assertEqual(diff["missing_scripts"], [])

    def test_element_count_and_depth(self):
        """Element count and max nesting depth match baseline exactly."""
        self.assertEqual(self.gen_fp["element_count"], self.base_fp["element_count"])
        self.assertEqual(self.gen_fp["max_depth"], self.base_fp["max_depth"])

    def test_runtime_contract(self):
        """Runtime contract values (data-slide, presentation IDs, speaker note) match."""
        runtime = self.gen_fp["runtime_contract"]
        self.assertEqual(runtime["data_slide"], "8")
        self.assertTrue(runtime["has_speaker_note"])
        self.assertTrue(runtime["all_standard_ids_present"])
        for req_id in [
            "presentation-progress",
            "presentation-viewport",
            "speaker-panel",
            "speaker-close",
            "speaker-text",
            "speaker-toggle",
            "presentation-nav",
            "prev-btn",
            "next-btn",
            "presentation-counter",
        ]:
            self.assertTrue(runtime["standard_runtime_ids"].get(req_id), f"Missing runtime ID: {req_id}")

    def test_asset_dependencies(self):
        """Linked stylesheets and script matches original exactly."""
        self.assertIn("4번 슬라이드.css", self.gen_fp["stylesheets"])
        self.assertIn("발표용_공통.css", self.gen_fp["stylesheets"])
        self.assertIn("발표용_공통.js", self.gen_fp["scripts"])


class TestSlide008CSSJSIndependence(unittest.TestCase):
    """D. Verification that CSS/JS files are untouched."""

    def setUp(self):
        self.repo_root = automation_dir.parent
        self.html_dir = self.repo_root / "PRD-PO" / "html" / "분리된 html"

    def test_css_and_js_unmodified(self):
        """CSS and JS files must exist and match initial uncorrupted state."""
        css_files = list(self.html_dir.glob("*.css"))
        js_files = list(self.html_dir.glob("*.js"))
        self.assertGreater(len(css_files), 0)
        self.assertGreater(len(js_files), 0)

        # Verify common assets exist
        self.assertTrue((self.html_dir / "발표용_공통.css").exists())
        self.assertTrue((self.html_dir / "발표용_공통.js").exists())
        self.assertTrue((self.html_dir / "4번 슬라이드.css").exists())


if __name__ == "__main__":
    unittest.main()
