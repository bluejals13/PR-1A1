#!/usr/bin/env python3
"""
Unit tests for the template rendering abstraction and build orchestration.
"""

import tempfile
import unittest
from pathlib import Path

# Add automation dir to path
automation_dir = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(automation_dir))

from build import build_slide
from render import JinjaRenderer, RenderError, Renderer


class DummyRenderer(Renderer):
    """A mock renderer to verify Renderer dependency injection in build_slide."""
    def __init__(self, output_content: str = "<p>Mock Rendered</p>"):
        self.output_content = output_content
        self.called_with = None

    def render(self, template_name: str, context: dict, template_dir: Path) -> str:
        self.called_with = {
            "template_name": template_name,
            "context": context,
            "template_dir": template_dir
        }
        return self.output_content


class TestRendererAbstraction(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.template_dir = Path(self.temp_dir.name)
        
        # Write a sample Jinja2 template
        sample_tpl = self.template_dir / "sample.html.j2"
        sample_tpl.write_text("<h1>{{ title }}</h1><p>{{ value }}</p>", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_jinja_renderer_success(self):
        """JinjaRenderer correctly loads and renders a template."""
        renderer = JinjaRenderer()
        output = renderer.render(
            template_name="sample.html.j2",
            context={"title": "Hello", "value": "World"},
            template_dir=self.template_dir
        )
        self.assertEqual(output, "<h1>Hello</h1><p>World</p>")

    def test_jinja_renderer_missing_template(self):
        """JinjaRenderer raises RenderError if the template file does not exist."""
        renderer = JinjaRenderer()
        with self.assertRaises(RenderError) as ctx:
            renderer.render(
                template_name="nonexistent.html.j2",
                context={},
                template_dir=self.template_dir
            )
        self.assertIn("not found", str(ctx.exception))

    def test_build_slide_with_renderer_injection(self):
        """build_slide accepts a custom Renderer instance via dependency injection."""
        data_path = automation_dir / "data" / "slide_004.json"
        mock_renderer = DummyRenderer("<section id='slide-04'>Mocked Content</section>")
        output_path = Path(self.temp_dir.name) / "out.html"

        success = build_slide(
            data_path=data_path,
            template_dir=self.template_dir,
            template_name="dummy.j2",
            output_path=output_path,
            slide_id="004",
            renderer=mock_renderer
        )
        self.assertTrue(success)
        self.assertIsNotNone(mock_renderer.called_with)
        self.assertEqual(mock_renderer.called_with["template_name"], "dummy.j2")
        self.assertEqual(output_path.read_text(encoding="utf-8"), "<section id='slide-04'>Mocked Content</section>")


if __name__ == "__main__":
    unittest.main()
