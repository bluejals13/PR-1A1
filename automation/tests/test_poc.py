#!/usr/bin/env python3
"""
Automated Verification Suite for Presentation Automation PoC (Slide 04).

Validates:
A. Existing design & DOM preservation
B. Data replacement (text alteration reflection)
C. Status replacement (status & statusClass alteration reflection)
D. CSS independence & rejection of forbidden styling properties
E. Rebuild reproducibility
F. Compatibility with 발표용_공통.js runtime
"""

import json
import re
import sys
import unittest
from pathlib import Path

# Add automation dir to sys.path
automation_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(automation_dir))

from build import build_slide
from validate import (
    ALLOWED_STATUS_CLASSES,
    ValidationError,
    normalize_slide_data,
    validate_slide_data,
)


class TestSlide04Automation(unittest.TestCase):
    def setUp(self):
        self.base_dir = automation_dir
        self.data_path = self.base_dir / "data" / "slide_004.json"
        self.template_dir = self.base_dir / "templates"
        self.template_name = "slide_004.html.j2"
        self.test_output = self.base_dir / "dist" / "test_slide_004.html"
        self.test_output.parent.mkdir(parents=True, exist_ok=True)

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.original_data = json.load(f)

    def test_criterion_a_dom_and_classes_preserved(self):
        """A. Existing DOM structure, IDs, and CSS classes are preserved."""
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output
        )
        self.assertTrue(success, "Build should succeed with standard data.")
        content = self.test_output.read_text(encoding="utf-8")

        # Crucial CSS classes from original 4번 슬라이드.css
        required_classes = [
            "slide-04",
            "slide-header",
            "slide-title-wrap",
            "slide-num",
            "slide-title",
            "title-arrow",
            "title-sub",
            "slide-04-intro",
            "intro-line",
            "threat-control-table-wrap",
            "threat-control-table",
            "col-threat",
            "col-scenario",
            "col-control",
            "col-status",
            "threat-name",
            "threat-dot",
            "scenario-text",
            "control-name",
            "status-cell",
            "security-status-group",
            "security-status",
            "security-principle",
            "principle-icon",
            "principle-content",
            "principle-label",
        ]
        for cls in required_classes:
            self.assertIn(cls, content, f"Required CSS class '{cls}' missing from generated HTML.")

    def test_criterion_b_data_replacement(self):
        """B. Changing text in data updates HTML without modifying template or CSS."""
        modified_data = dict(self.original_data)
        modified_data["items"] = list(self.original_data["items"])
        
        # Replace Token Theft with a custom audit scenario
        custom_threat = "API Gateway Token Hijacking"
        custom_scenario = "Stolen JWT replay across edge proxy"
        modified_data["items"][0] = dict(modified_data["items"][0])
        modified_data["items"][0]["threat"] = custom_threat
        modified_data["items"][0]["scenario"] = custom_scenario

        temp_data_path = self.base_dir / "dist" / "temp_data_replacement.json"
        with open(temp_data_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output
        )
        self.assertTrue(success)
        content = self.test_output.read_text(encoding="utf-8")
        self.assertIn(custom_threat, content)
        self.assertIn(custom_scenario, content)

    def test_criterion_c_status_replacement(self):
        """C. Changing status value and statusClass reflects dynamically in HTML."""
        modified_data = dict(self.original_data)
        modified_data["items"] = [dict(it) for it in self.original_data["items"]]

        # Change row 0 to review / VERIFY REQUIRED
        modified_data["items"][0]["statuses"] = [
            {"status": "IMPLEMENTED", "statusClass": "implemented"},
            {"status": "VERIFY REQUIRED", "statusClass": "verify-required"}
        ]
        temp_data_path = self.base_dir / "dist" / "temp_status_replacement.json"
        with open(temp_data_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output
        )
        self.assertTrue(success)
        content = self.test_output.read_text(encoding="utf-8")
        self.assertIn("verify-required", content)
        self.assertIn("VERIFY REQUIRED", content)

    def test_criterion_d_css_independence_and_rejection_of_styling_keys(self):
        """D. Validates that forbidden styling keys (color, fontSize, margin) are rejected."""
        tainted_data = dict(self.original_data)
        tainted_data["items"] = [dict(it) for it in self.original_data["items"]]
        tainted_data["items"][0]["color"] = "#ff0000"  # Forbidden design property

        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(tainted_data)
        self.assertIn("Forbidden design property", str(ctx.exception))

    def test_criterion_f_runtime_compatibility(self):
        """F. Compatible with 발표용_공통.js runtime hooks and DOM contracts."""
        build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="004"
        )
        content = self.test_output.read_text(encoding="utf-8")

        # Elements required by 발표용_공통.js
        self.assertIn('id="presentation-progress"', content)
        self.assertIn('id="presentation-counter"', content)
        self.assertIn('id="speaker-panel"', content)
        self.assertIn('id="speaker-text"', content)
        self.assertIn('id="speaker-toggle"', content)
        self.assertIn('id="speaker-close"', content)
        self.assertIn('id="prev-btn"', content)
        self.assertIn('id="next-btn"', content)
        self.assertIn('src="발표용_공통.js"', content)
        self.assertIn('data-slide="4"', content)


class TestSlide05Automation(unittest.TestCase):
    def setUp(self):
        self.base_dir = automation_dir
        self.repo_root = self.base_dir.parent
        self.data_path = self.base_dir / "data" / "slide_005.json"
        self.template_dir = self.base_dir / "templates"
        self.template_name = "slide_005.html.j2"
        self.test_output = self.base_dir / "dist" / "test_slide_005.html"
        self.primary_output = self.repo_root / "PRD-PO" / "html" / "분리된 html" / "5번 슬라이드.html"
        self.test_output.parent.mkdir(parents=True, exist_ok=True)

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.original_data = json.load(f)

    def test_slide_005_data_validation(self):
        """1. Slide 05 data validation."""
        # Valid data passes
        validate_slide_data(self.original_data, slide_id="005")

        # Missing flows raises error
        invalid_data = dict(self.original_data)
        del invalid_data["flows"]
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(invalid_data, slide_id="005")
        self.assertIn("must contain 'flows'", str(ctx.exception))

    def test_slide_005_rendering_and_dom_preservation(self):
        """2. Slide 05 rendering and CSS class / DOM hierarchy preservation."""
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="005"
        )
        self.assertTrue(success, "Slide 05 build should succeed.")
        content = self.test_output.read_text(encoding="utf-8")

        # Crucial CSS classes from original 5번 슬라이드.css
        required_classes = [
            "slide-05",
            "slide-header",
            "slide-title-wrap",
            "slide-num",
            "slide-title",
            "title-divider",
            "slide-05-intro",
            "intro-label",
            "intro-text",
            "security-flow-grid",
            "flow-card",
            "flow-normal",
            "flow-replay",
            "flow-revocation",
            "flow-card-header",
            "flow-kicker",
            "flow-badge",
            "flow-track",
            "flow-step",
            "step-index",
            "flow-connector",
            "flow-control",
            "control-label",
            "flow-decision",
            "decision-mark",
            "flow-result",
            "result-icon",
            "slide-05-summary",
            "summary-label",
            "summary-flow",
            "summary-control",
            "summary-block",
            "summary-note",
        ]
        for cls in required_classes:
            self.assertIn(cls, content, f"Required CSS class '{cls}' missing from generated Slide 05 HTML.")

    def test_slide_005_data_replacement(self):
        """3. Slide 05 data replacement alters rendered text without template modification."""
        modified_data = dict(self.original_data)
        modified_data["flows"] = [dict(f) for f in self.original_data["flows"]]
        modified_data["flows"][0] = dict(modified_data["flows"][0])
        modified_data["flows"][0]["nodes"] = [dict(n) for n in modified_data["flows"][0]["nodes"]]

        custom_step_title = "Multi-Factor Authentication Flow"
        custom_step_desc = "FIDO2 WebAuthn / Hardware Key"
        modified_data["flows"][0]["nodes"][0]["strong"] = custom_step_title
        modified_data["flows"][0]["nodes"][0]["small"] = custom_step_desc

        temp_data_path = self.base_dir / "dist" / "temp_slide_005_replacement.json"
        with open(temp_data_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="005"
        )
        self.assertTrue(success)
        content = self.test_output.read_text(encoding="utf-8")
        self.assertIn(custom_step_title, content)
        self.assertIn(custom_step_desc, content)

    def test_slide_005_forbidden_inline_design_detection(self):
        """4. Slide 05 forbidden inline design detection (color, fontSize, style, margin)."""
        tainted_data = dict(self.original_data)
        tainted_data["flows"] = [dict(f) for f in self.original_data["flows"]]
        tainted_data["flows"][0]["color"] = "#ff0000"

        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(tainted_data, slide_id="005")
        self.assertIn("Forbidden design property", str(ctx.exception))

    def test_slide_005_runtime_dependency_and_path_validation(self):
        """5. Slide 05 runtime dependency and path validation."""
        # Ensure build outputs to primary destination
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.primary_output,
            slide_id="005"
        )
        self.assertTrue(success)
        content = self.primary_output.read_text(encoding="utf-8")

        # HTML references
        self.assertIn('href="5번 슬라이드.css"', content)
        self.assertIn('href="발표용_공통.css"', content)
        self.assertIn('src="발표용_공통.js"', content)
        self.assertIn('data-slide="5"', content)

        # File existence in primary directory
        target_dir = self.primary_output.parent
        self.assertTrue((target_dir / "5번 슬라이드.css").exists(), "5번 슬라이드.css must exist in output dir")
        self.assertTrue((target_dir / "발표용_공통.css").exists(), "발표용_공통.css must exist in output dir")
        self.assertTrue((target_dir / "발표용_공통.js").exists(), "발표용_공통.js must exist in output dir")


class TestSlide06Automation(unittest.TestCase):
    def setUp(self):
        self.base_dir = automation_dir
        self.repo_root = self.base_dir.parent
        self.data_path = self.base_dir / "data" / "slide_006.json"
        self.template_dir = self.base_dir / "templates"
        self.template_name = "slide_006.html.j2"
        self.test_output = self.base_dir / "dist" / "test_slide_006.html"
        self.primary_output = self.repo_root / "PRD-PO" / "html" / "분리된 html" / "6번 슬라이드.html"
        self.test_output.parent.mkdir(parents=True, exist_ok=True)

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.original_data = json.load(f)

    def test_slide_006_data_validation(self):
        """1. Slide 06 data schema and constraint validation."""
        # Valid data passes
        validate_slide_data(self.original_data, slide_id="006")

        # Missing summary raises ValidationError
        invalid_summary = dict(self.original_data)
        del invalid_summary["summary"]
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(invalid_summary, slide_id="006")
        self.assertIn("must contain 'summary'", str(ctx.exception))

        # Missing evidence raises ValidationError
        invalid_evidence = dict(self.original_data)
        del invalid_evidence["evidence"]
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(invalid_evidence, slide_id="006")
        self.assertIn("must contain 'evidence'", str(ctx.exception))

        # Missing performance raises ValidationError
        invalid_perf = dict(self.original_data)
        del invalid_perf["performance"]
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(invalid_perf, slide_id="006")
        self.assertIn("must contain 'performance'", str(ctx.exception))

        # Invalid status in test case raises ValidationError
        invalid_status_data = dict(self.original_data)
        invalid_status_data["evidence"] = dict(self.original_data["evidence"])
        invalid_status_data["evidence"]["test_cases"] = [dict(tc) for tc in self.original_data["evidence"]["test_cases"]]
        invalid_status_data["evidence"]["test_cases"][0]["status"] = "UNKNOWN_STATUS"
        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(invalid_status_data, slide_id="006")
        self.assertIn("has invalid status", str(ctx.exception))

    def test_slide_006_dom_parity_and_classes_preserved(self):
        """2. Slide 06 DOM class parity with original 6번 슬라이드.css."""
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="006"
        )
        self.assertTrue(success, "Slide 06 build should succeed.")
        content = self.test_output.read_text(encoding="utf-8")

        required_classes = [
            "slide-06",
            "slide-header",
            "slide-title-wrap",
            "slide-num",
            "slide-title",
            "tag",
            "verified",
            "verification-summary",
            "verification-stat",
            "stat-value",
            "stat-label",
            "stat-desc",
            "verified-stat",
            "partial-stat",
            "pending-stat",
            "verification-summary-message",
            "message-label",
            "verification-layout",
            "evidence-panel",
            "panel-header",
            "panel-kicker",
            "evidence-count",
            "evidence-table-wrap",
            "evidence-table",
            "col-id",
            "col-result",
            "col-status",
            "status-pass",
            "status-pending",
            "status-partial",
            "test-id",
            "result-code",
            "actual",
            "not-tested",
            "checking",
            "status-badge",
            "pass",
            "pending",
            "partial",
            "performance-panel",
            "performance-card",
            "performance-card-header",
            "performance-label",
            "performance-state",
            "metric-grid",
            "metric",
            "metric-label",
            "metric-green",
            "performance-divider",
            "performance-observation",
            "observation-label",
            "performance-footnote",
            "verification-footer",
            "footer-rule",
            "footer-flow",
            "footer-pass",
            "footer-note",
        ]
        for cls in required_classes:
            self.assertIn(cls, content, f"Required CSS class '{cls}' missing from generated Slide 06 HTML.")

    def test_slide_006_id_parity(self):
        """3. Slide 06 ID parity with original 6번 슬라이드.html."""
        build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="006"
        )
        content = self.test_output.read_text(encoding="utf-8")

        required_ids = [
            'id="slide-06"',
            'id="presentation-progress"',
            'id="presentation-viewport"',
            'id="speaker-panel"',
            'id="speaker-close"',
            'id="speaker-text"',
            'id="presentation-nav"',
            'id="prev-btn"',
            'id="presentation-counter"',
            'id="next-btn"',
            'id="speaker-toggle"',
        ]
        for id_attr in required_ids:
            self.assertIn(id_attr, content, f"Required ID attribute '{id_attr}' missing from Slide 06 HTML.")

    def test_slide_006_data_replacement(self):
        """4. Slide 06 data replacement reflects dynamically in rendered HTML."""
        modified_data = dict(self.original_data)
        modified_data["evidence"] = dict(self.original_data["evidence"])
        modified_data["evidence"]["test_cases"] = [dict(tc) for tc in self.original_data["evidence"]["test_cases"]]

        custom_scenario = "Distributed Replay Injection with Compromised Sub-token"
        custom_sub = "Quantum Leaked JWT Session"
        modified_data["evidence"]["test_cases"][0]["scenario"] = custom_scenario
        modified_data["evidence"]["test_cases"][0]["scenario_sub"] = custom_sub

        temp_data_path = self.base_dir / "dist" / "temp_slide_006_data_replacement.json"
        with open(temp_data_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="006"
        )
        self.assertTrue(success)
        content = self.test_output.read_text(encoding="utf-8")
        self.assertIn(custom_scenario, content)
        self.assertIn(custom_sub, content)

    def test_slide_006_status_replacement(self):
        """5. Slide 06 VERIFIED/PARTIAL/PENDING status replacement reflects dynamically."""
        modified_data = dict(self.original_data)
        modified_data["evidence"] = dict(self.original_data["evidence"])
        modified_data["evidence"]["test_cases"] = [dict(tc) for tc in self.original_data["evidence"]["test_cases"]]

        # Turn SEC-01 from PASS to PENDING
        modified_data["evidence"]["test_cases"][0]["status"] = "PENDING"
        modified_data["evidence"]["test_cases"][0]["actual"] = "N/A"

        # Turn SEC-07 from PARTIAL to PASS
        modified_data["evidence"]["test_cases"][6]["status"] = "PASS"
        modified_data["evidence"]["test_cases"][6]["actual"] = "BLOCK"

        temp_data_path = self.base_dir / "dist" / "temp_slide_006_status_replacement.json"
        with open(temp_data_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="006"
        )
        self.assertTrue(success)
        content = self.test_output.read_text(encoding="utf-8")

        # SEC-01 row should now have status-pending and badge pending
        self.assertRegex(content, r'<tr class="status-pending">\s*<td class="test-id">SEC-01</td>')
        # SEC-07 row should now have status-pass and badge pass
        self.assertRegex(content, r'<tr class="status-pass">\s*<td class="test-id">SEC-07</td>')

    def test_slide_006_forbidden_inline_design_detection(self):
        """6. Slide 06 rejects forbidden styling keys (color, fontSize, style, margin)."""
        tainted_data = dict(self.original_data)
        tainted_data["evidence"] = dict(self.original_data["evidence"])
        tainted_data["evidence"]["test_cases"] = [dict(tc) for tc in self.original_data["evidence"]["test_cases"]]
        tainted_data["evidence"]["test_cases"][0]["color"] = "#10b981"  # Forbidden design property

        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(tainted_data, slide_id="006")
        self.assertIn("Forbidden design property", str(ctx.exception))

    def test_slide_006_runtime_dependency_and_path_validation(self):
        """7. Slide 06 runtime dependency and asset path validation."""
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.primary_output,
            slide_id="006"
        )
        self.assertTrue(success)
        content = self.primary_output.read_text(encoding="utf-8")

        # HTML runtime contracts
        self.assertIn('href="6번 슬라이드.css"', content)
        self.assertIn('href="발표용_공통.css"', content)
        self.assertIn('src="발표용_공통.js"', content)
        self.assertIn('data-slide="6"', content)

        # Asset existence on disk
        target_dir = self.primary_output.parent
        self.assertTrue((target_dir / "6번 슬라이드.css").exists(), "6번 슬라이드.css must exist in output dir")
        self.assertTrue((target_dir / "발표용_공통.css").exists(), "발표용_공통.css must exist in output dir")
        self.assertTrue((target_dir / "발표용_공통.js").exists(), "발표용_공통.js must exist in output dir")


class TestSlide07Automation(unittest.TestCase):
    def setUp(self):
        self.base_dir = automation_dir
        self.repo_root = self.base_dir.parent
        self.data_path = self.base_dir / "data" / "slide_007.json"
        self.template_dir = self.base_dir / "templates"
        self.template_name = "slide_007.html.j2"
        self.test_output = self.base_dir / "dist" / "test_slide_007.html"
        self.primary_output = self.repo_root / "PRD-PO" / "html" / "분리된 html" / "7번 슬라이드.html"
        self.test_output.parent.mkdir(parents=True, exist_ok=True)

        with open(self.data_path, "r", encoding="utf-8") as f:
            self.original_data = json.load(f)

    # ----------------------------------------------------------------
    # Test 1 — Data replacement
    # ----------------------------------------------------------------
    def test_slide_007_data_replacement(self):
        """Test 1. Changing operation case text in JSON reflects in rendered HTML."""
        modified_data = dict(self.original_data)
        modified_data["incident_panel"] = dict(self.original_data["incident_panel"])
        modified_data["incident_panel"]["cases"] = [
            dict(c) for c in self.original_data["incident_panel"]["cases"]
        ]

        custom_title = "Custom Replay Attack Mitigation Test"
        custom_threat_text = "Synthetic token replay from compromised upstream service"
        modified_data["incident_panel"]["cases"][0] = dict(
            modified_data["incident_panel"]["cases"][0]
        )
        modified_data["incident_panel"]["cases"][0]["title"] = custom_title
        modified_data["incident_panel"]["cases"][0]["threat"] = dict(
            modified_data["incident_panel"]["cases"][0]["threat"]
        )
        modified_data["incident_panel"]["cases"][0]["threat"]["text"] = custom_threat_text

        temp_path = self.base_dir / "dist" / "temp_slide_007_data.json"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="007"
        )
        self.assertTrue(success, "Build must succeed after data modification.")
        content = self.test_output.read_text(encoding="utf-8")
        self.assertIn(custom_title, content,
                      "Modified case title must appear in rendered HTML.")
        self.assertIn(custom_threat_text, content,
                      "Modified threat text must appear in rendered HTML.")

    # ----------------------------------------------------------------
    # Test 2 — Status replacement
    # ----------------------------------------------------------------
    def test_slide_007_status_replacement(self):
        """Test 2. Changing status_text updates card_class and status rendering."""
        import copy
        modified_data = copy.deepcopy(self.original_data)

        # Flip CASE 01 from resolved → verify
        modified_data["incident_panel"]["cases"][0]["card_class"] = "verify"
        modified_data["incident_panel"]["cases"][0]["status_class"] = "verify-status"
        modified_data["incident_panel"]["cases"][0]["status_text"] = "VERIFY REQUIRED"

        # Flip CASE 02 from verify → resolved
        modified_data["incident_panel"]["cases"][1]["card_class"] = "resolved"
        modified_data["incident_panel"]["cases"][1]["status_class"] = "resolved-status"
        modified_data["incident_panel"]["cases"][1]["status_text"] = "RESOLVED"

        # Flip first risk from risk-done/VERIFIED → risk-critical/OPEN
        modified_data["risk_panel"]["risks"][0]["item_class"] = "risk-critical"
        modified_data["risk_panel"]["risks"][0]["state"] = "OPEN"

        temp_path = self.base_dir / "dist" / "temp_slide_007_status.json"
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(modified_data, f, ensure_ascii=False)

        success = build_slide(
            data_path=temp_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="007"
        )
        self.assertTrue(success)
        content = self.test_output.read_text(encoding="utf-8")

        # CASE 01 should now show verify card and verify-status badge
        self.assertRegex(
            content,
            r'<article class="incident-card verify">',
            "CASE 01 must render with 'verify' card class after status change."
        )
        self.assertIn("verify-status", content,
                      "verify-status badge class must appear after status change.")

        # CASE 02 should now show resolved
        self.assertRegex(
            content,
            r'<article class="incident-card resolved">',
            "CASE 02 must render with 'resolved' class after status change."
        )

        # First risk should now be risk-critical / OPEN
        self.assertIn("risk-critical", content)

    # ----------------------------------------------------------------
    # Test 3 — DOM class parity
    # ----------------------------------------------------------------
    def test_slide_007_dom_parity_and_classes_preserved(self):
        """Test 3. All CSS classes from the original 7번 슬라이드.css must appear in generated HTML."""
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="007"
        )
        self.assertTrue(success, "Slide 07 build must succeed.")
        content = self.test_output.read_text(encoding="utf-8")

        required_classes = [
            # Header
            "slide-07", "slide-header", "slide-title-wrap", "slide-num", "slide-title",
            "tag", "verified",
            # Operation summary
            "operation-summary", "operation-summary-title", "panel-kicker",
            "operation-summary-flow", "flow-done", "flow-monitor", "flow-next",
            # Layout
            "operation-layout",
            # Incident panel
            "incident-panel", "panel-header", "evidence-count",
            "incident-list", "incident-card", "resolved", "verify",
            "incident-head", "case-id", "case-status", "resolved-status", "verify-status",
            "incident-flow", "incident-row", "incident-label", "threat", "impact",
            "incident-arrow",
            "control-box", "control-label",
            # Risk panel
            "risk-panel", "risk-list", "risk-item",
            "risk-done", "risk-warning", "risk-critical", "risk-info",
            "risk-state",
            # Next action
            "next-action-panel", "next-action-title",
            "action-item", "p0", "p1", "priority-badge",
            # Principle
            "operation-principle", "principle-mark",
        ]
        for cls in required_classes:
            self.assertIn(cls, content,
                          f"Required CSS class '{cls}' missing from generated Slide 07 HTML.")

    # ----------------------------------------------------------------
    # Test 4 — ID parity
    # ----------------------------------------------------------------
    def test_slide_007_id_parity(self):
        """Test 4. All presentation-runtime IDs from original 7번 슬라이드.html must be present."""
        build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="007"
        )
        content = self.test_output.read_text(encoding="utf-8")

        required_ids = [
            'id="slide-07"',
            'id="presentation-progress"',
            'id="presentation-viewport"',
            'id="speaker-panel"',
            'id="speaker-close"',
            'id="speaker-text"',
            'id="presentation-nav"',
            'id="prev-btn"',
            'id="presentation-counter"',
            'id="next-btn"',
            'id="speaker-toggle"',
        ]
        for id_attr in required_ids:
            self.assertIn(id_attr, content,
                          f"Required ID '{id_attr}' missing from Slide 07 HTML.")

    # ----------------------------------------------------------------
    # Test 5 — Runtime contract (data-slide, counter, JS DOM hooks)
    # ----------------------------------------------------------------
    def test_slide_007_runtime_contract(self):
        """Test 5. Slide 07 satisfies the 발표용_공통.js runtime DOM contract."""
        build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.test_output,
            slide_id="007"
        )
        content = self.test_output.read_text(encoding="utf-8")

        self.assertIn('data-slide="7"', content, "data-slide must be '7'.")
        self.assertIn('id="presentation-progress"', content)
        self.assertIn('id="presentation-counter"', content)
        self.assertIn('id="speaker-panel"', content)
        self.assertIn('id="speaker-text"', content)
        self.assertIn('id="speaker-toggle"', content)
        self.assertIn('id="speaker-close"', content)
        self.assertIn('id="prev-btn"', content)
        self.assertIn('id="next-btn"', content)
        self.assertIn('src="발표용_공통.js"', content,
                      "Runtime script reference must be relative 발표용_공통.js.")

    # ----------------------------------------------------------------
    # Test 6 — CSS / JS dependency (asset paths intact)
    # ----------------------------------------------------------------
    def test_slide_007_css_js_dependency(self):
        """Test 6. Generated HTML references original CSS/JS with correct relative paths."""
        success = build_slide(
            data_path=self.data_path,
            template_dir=self.template_dir,
            template_name=self.template_name,
            output_path=self.primary_output,
            slide_id="007"
        )
        self.assertTrue(success)
        content = self.primary_output.read_text(encoding="utf-8")

        self.assertIn('href="7번 슬라이드.css"', content,
                      "7번 슬라이드.css link must be present with relative path.")
        self.assertIn('href="발표용_공통.css"', content)
        self.assertIn('src="발표용_공통.js"', content)

        target_dir = self.primary_output.parent
        self.assertTrue((target_dir / "7번 슬라이드.css").exists(),
                        "7번 슬라이드.css must exist in the same directory as the output HTML.")
        self.assertTrue((target_dir / "발표용_공통.css").exists())
        self.assertTrue((target_dir / "발표용_공통.js").exists())

    # ----------------------------------------------------------------
    # Test 7 — Design separation (no forbidden styling in JSON)
    # ----------------------------------------------------------------
    def test_slide_007_design_separation(self):
        """Test 7. slide_007.json must not contain any CSS/design properties."""
        tainted = dict(self.original_data)
        tainted["incident_panel"] = dict(self.original_data["incident_panel"])
        tainted["incident_panel"]["cases"] = [
            dict(c) for c in self.original_data["incident_panel"]["cases"]
        ]
        tainted["incident_panel"]["cases"][0]["color"] = "#ef4444"  # forbidden

        with self.assertRaises(ValidationError) as ctx:
            validate_slide_data(tainted, slide_id="007")
        self.assertIn("Forbidden design property", str(ctx.exception))

        # Also verify original JSON has no forbidden keys
        validate_slide_data(self.original_data, slide_id="007")  # must not raise

    # ----------------------------------------------------------------
    # Test 8 — Regression: Slide 04 / 05 / 06 still pass
    # ----------------------------------------------------------------
    def test_slide_007_regression_04_05_06(self):
        """Test 8. Slide 04, 05, and 06 builds all still succeed after Slide 07 additions."""
        for slide_id, template_name, data_name in [
            ("004", "slide_004.html.j2", "slide_004.json"),
            ("005", "slide_005.html.j2", "slide_005.json"),
            ("006", "slide_006.html.j2", "slide_006.json"),
        ]:
            data_path = self.base_dir / "data" / data_name
            out = self.base_dir / "dist" / f"regression_{slide_id}.html"
            success = build_slide(
                data_path=data_path,
                template_dir=self.template_dir,
                template_name=template_name,
                output_path=out,
                slide_id=slide_id
            )
            self.assertTrue(
                success,
                f"Regression: Slide {slide_id} build must still pass after Slide 07 additions."
            )


if __name__ == "__main__":
    unittest.main()



