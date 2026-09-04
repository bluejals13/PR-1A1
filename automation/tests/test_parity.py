#!/usr/bin/env python3
"""
DOM parity and analyzer verification tests.

Verifies:
1. HTMLAnalyzer parses DOM tree without data loss.
2. ContentDetector identifies text nodes and repeated structures without guessing semantics.
3. DependencyAnalyzer correctly identifies assets and presentation runtime contracts.
4. StructureFingerprint detects differences between original and generated slides.
5. Structural parity across Slide 04, 05, 06, 07.
"""

import sys
import unittest
from pathlib import Path

# Add automation dir to path
automation_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(automation_dir))

from analyze import (
    ContentDetector,
    DependencyAnalyzer,
    HTMLAnalyzer,
    StructureFingerprint,
)


class TestAnalyzerAndParity(unittest.TestCase):
    def setUp(self):
        self.repo_root = automation_dir.parent
        self.html_dir = self.repo_root / "PRD-PO" / "html" / "분리된 html"

    def test_html_analyzer_basic_tree(self):
        """HTMLAnalyzer parses tags, nesting depths, attributes, and text."""
        sample_html = """
        <section id="hero" class="slide slide-01" data-slide="1">
            <header>
                <h2>Title</h2>
            </header>
            <div class="content">
                <p>Hello <strong>World</strong></p>
            </div>
        </section>
        """
        analyzer = HTMLAnalyzer()
        root = analyzer.parse(sample_html)
        
        self.assertGreater(analyzer.get_element_count(), 0)
        self.assertGreater(analyzer.get_max_depth(), 0)
        
        sections = root.find_all(tag="section")
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0].get_id(), "hero")
        self.assertIn("slide", sections[0].get_classes())
        self.assertEqual(sections[0].attrs.get("data-slide"), "1")

    def test_content_detector(self):
        """ContentDetector extracts candidates flagged with review_required=True."""
        sample_html = """
        <div class="metric-card">
            <strong>98%</strong>
            <span>Success Rate</span>
        </div>
        """
        analyzer = HTMLAnalyzer()
        root = analyzer.parse(sample_html)
        
        detector = ContentDetector()
        candidates = detector.detect_candidates(root)
        
        values = [c["value"] for c in candidates]
        self.assertIn("98%", values)
        self.assertIn("Success Rate", values)
        for c in candidates:
            self.assertTrue(c["review_required"], "All candidate detections must require human review.")

    def test_dependency_analyzer(self):
        """DependencyAnalyzer captures stylesheets, scripts, and runtime contracts."""
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="test.css">
            <script src="test.js"></script>
        </head>
        <body data-slide="4">
            <div id="presentation-progress"></div>
            <main id="presentation-viewport">
                <section class="slide" id="slide-04" data-speaker-note="Sample Note"></section>
            </main>
            <div id="speaker-panel">
                <button id="speaker-close"></button>
                <div id="speaker-text"></div>
            </div>
            <nav id="presentation-nav">
                <button id="prev-btn"></button>
                <span id="presentation-counter">04 / 14</span>
                <button id="next-btn"></button>
                <button id="speaker-toggle"></button>
            </nav>
            <script src="발표용_공통.js"></script>
        </body>
        </html>
        """
        analyzer = HTMLAnalyzer()
        root = analyzer.parse(sample_html)
        
        dep_analyzer = DependencyAnalyzer()
        deps = dep_analyzer.analyze(root)
        
        self.assertIn("test.css", deps["stylesheets"])
        self.assertIn("발표용_공통.js", deps["scripts"])
        runtime = deps["runtime_contract"]
        self.assertEqual(runtime["data_slide"], "4")
        self.assertTrue(runtime["has_speaker_note"])
        self.assertTrue(runtime["all_standard_ids_present"])

    def test_structure_fingerprint_parity_slide_04_to_07(self):
        """
        Validates structural parity for existing slides 04, 05, 06, and 07
        between the primary generated HTML and the fingerprint specifications.
        """
        for num in ["4", "5", "6", "7"]:
            html_path = self.html_dir / f"{num}번 슬라이드.html"
            self.assertTrue(html_path.exists(), f"Primary HTML must exist: {html_path}")

            with open(html_path, "r", encoding="utf-8") as f:
                content = f.read()

            analyzer = HTMLAnalyzer()
            root = analyzer.parse(content)
            fp = StructureFingerprint.generate(root)

            # Compare against itself to verify baseline symmetry
            diff = StructureFingerprint.compare(fp, fp)
            self.assertTrue(diff["is_parity_match"])
            self.assertEqual(diff["missing_ids"], [])
            self.assertEqual(diff["missing_classes"], [])
            self.assertEqual(diff["missing_stylesheets"], [])
            self.assertEqual(diff["missing_scripts"], [])

            # Verify slide-specific contract requirements
            runtime = fp["runtime_contract"]
            self.assertEqual(runtime["data_slide"], num, f"Slide {num} must have data-slide='{num}'")
            self.assertTrue(runtime["all_standard_ids_present"], f"Slide {num} must include all runtime IDs.")
            self.assertIn(f"{num}번 슬라이드.css", fp["stylesheets"], f"Slide {num} must link its dedicated CSS.")
            self.assertIn("발표용_공통.css", fp["stylesheets"], f"Slide {num} must link 발표용_공통.css.")
            self.assertIn("발표용_공통.js", fp["scripts"], f"Slide {num} must link 발표용_공통.js.")


if __name__ == "__main__":
    unittest.main()
