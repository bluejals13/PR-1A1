"""
Analyzes external assets and presentation runtime contract dependencies.
"""

from typing import Any, Dict, List, Optional

from .html_analyzer import DOMNode

STANDARD_RUNTIME_IDS = [
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
]


class DependencyAnalyzer:
    """
    Extracts asset dependencies and verifies presentation runtime contract compliance.
    """

    def analyze(self, root: DOMNode) -> Dict[str, Any]:
        """
        Extracts linked stylesheets, scripts, images, and runtime DOM contracts.
        """
        stylesheets: List[str] = []
        scripts: List[str] = []
        images: List[str] = []
        fonts: List[str] = []

        # Find all link elements
        for node in root.find_all(tag="link"):
            rel = node.attrs.get("rel", "").lower()
            href = node.attrs.get("href", "")
            if "stylesheet" in rel and href:
                stylesheets.append(href)
            elif "preconnect" in rel and href:
                fonts.append(href)
            elif href and ("fonts.googleapis.com" in href or "fonts.gstatic.com" in href):
                fonts.append(href)

        # Find all script elements
        for node in root.find_all(tag="script"):
            src = node.attrs.get("src", "")
            if src:
                scripts.append(src)

        # Find all img elements
        for node in root.find_all(tag="img"):
            src = node.attrs.get("src", "")
            if src:
                images.append(src)

        # Presentation runtime contracts
        data_slide: Optional[str] = None
        data_speaker_note: Optional[str] = None

        # body data-slide
        for node in root.find_all(tag="body"):
            if "data-slide" in node.attrs:
                data_slide = node.attrs["data-slide"]

        # section.slide data-speaker-note
        for node in root.find_all(tag="section"):
            if "slide" in node.get_classes() or (node.get_id() and node.get_id().startswith("slide-")):
                if "data-speaker-note" in node.attrs:
                    data_speaker_note = node.attrs["data-speaker-note"]
                if not data_slide and "data-slide" in node.attrs:
                    data_slide = node.attrs["data-slide"]

        # Runtime IDs present
        present_ids = set()
        for node in root.find_all():
            node_id = node.get_id()
            if node_id:
                present_ids.add(node_id)

        runtime_ids_status = {
            id_name: (id_name in present_ids)
            for id_name in STANDARD_RUNTIME_IDS
        }

        # Check for slide section ID (slide-04, slide-05, etc.)
        slide_section_id = None
        for pid in present_ids:
            if pid.startswith("slide-"):
                slide_section_id = pid
                break

        return {
            "stylesheets": stylesheets,
            "scripts": scripts,
            "images": images,
            "fonts": fonts,
            "runtime_contract": {
                "data_slide": data_slide,
                "has_speaker_note": data_speaker_note is not None,
                "speaker_note_preview": data_speaker_note[:80] + "..." if data_speaker_note and len(data_speaker_note) > 80 else data_speaker_note,
                "slide_section_id": slide_section_id,
                "standard_runtime_ids": runtime_ids_status,
                "all_standard_ids_present": all(runtime_ids_status.values())
            }
        }
