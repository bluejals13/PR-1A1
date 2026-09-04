"""
Renderer abstraction interface for presentation automation framework.

Decouples the automation orchestration pipeline from specific template engines.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class Renderer(ABC):
    """Abstract base class for template renderers in the automation framework."""

    @abstractmethod
    def render(self, template_name: str, context: Dict[str, Any], template_dir: Path) -> str:
        """
        Renders a template with the given data context.

        Args:
            template_name: The name/filename of the template to render.
            context: The normalized data dictionary to bind into the template.
            template_dir: Directory where templates are located.

        Returns:
            The rendered HTML string.

        Raises:
            RenderError: If template loading or rendering fails.
        """
        raise NotImplementedError


class RenderError(Exception):
    """Raised when template rendering fails."""
    pass
