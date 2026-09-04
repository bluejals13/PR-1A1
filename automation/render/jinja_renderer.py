"""
Jinja2 implementation of the Renderer interface.
"""

from pathlib import Path
from typing import Any, Dict

import jinja2

from .renderer import RenderError, Renderer


class JinjaRenderer(Renderer):
    """
    Renders presentation HTML templates using the Jinja2 templating engine.
    """

    def __init__(self, autoescape: bool = True):
        self.autoescape = autoescape

    def _create_environment(self, template_dir: Path) -> jinja2.Environment:
        """Configures and returns a Jinja2 Environment for HTML presentation slides."""
        autoescape_val = jinja2.select_autoescape(["html", "xml"]) if self.autoescape else False
        return jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(template_dir)),
            autoescape=autoescape_val,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render(self, template_name: str, context: Dict[str, Any], template_dir: Path) -> str:
        """
        Loads and renders a Jinja2 template with the given context.
        """
        try:
            env = self._create_environment(template_dir)
            template = env.get_template(template_name)
            return template.render(**context)
        except jinja2.TemplateNotFound as e:
            raise RenderError(f"Template '{template_name}' not found in '{template_dir}': {e}") from e
        except Exception as e:
            raise RenderError(f"Failed to render Jinja2 template '{template_name}': {e}") from e
