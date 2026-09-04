"""
Detects content candidate fields and repeated DOM structures from parsed HTML.
"""

from collections import Counter
from typing import Any, Dict, List

from .html_analyzer import DOMNode

SKIP_CHILDREN_TAGS = {"script", "style", "head"}
NON_CONTENT_TAGS = {"html", "body", "meta", "link", "title", "[root]"}


class ContentDetector:
    """
    Detects dynamic content candidates and repeated sibling structures without
    arbitrarily inferring business semantics.
    """

    def detect_candidates(self, root: DOMNode) -> List[Dict[str, Any]]:
        """
        Extracts content candidate elements that contain direct or meaningful text.
        Each candidate is flagged with review_required=True.
        """
        candidates: List[Dict[str, Any]] = []

        def _scan(node: DOMNode):
            if node.tag in SKIP_CHILDREN_TAGS:
                return

            if node.tag not in NON_CONTENT_TAGS:
                direct_text = node.text
                if direct_text:
                    candidates.append({
                        "selector": node.get_selector(),
                        "tag": node.tag,
                        "id": node.get_id(),
                        "classes": sorted(list(node.get_classes())),
                        "value": direct_text,
                        "review_required": True
                    })

            for child in node.children:
                _scan(child)

        _scan(root)
        return candidates

    def detect_repeated_structures(self, root: DOMNode, min_occurrences: int = 2) -> List[Dict[str, Any]]:
        """
        Detects repeating sibling structures under the same parent element
        (e.g., multiple rows in a table, cards in a grid, metrics in a list).
        """
        repeated_groups: List[Dict[str, Any]] = []

        def _find_repeats(node: DOMNode):
            if len(node.children) >= min_occurrences:
                # Group direct children by tag + primary class
                child_signatures = []
                for child in node.children:
                    classes = sorted(list(child.get_classes()))
                    sig = (child.tag, ".".join(classes) if classes else "")
                    child_signatures.append(sig)

                counts = Counter(child_signatures)
                for (sig_tag, sig_class), count in counts.items():
                    if count >= min_occurrences:
                        desc = f"{sig_tag}.{sig_class}" if sig_class else sig_tag
                        repeated_groups.append({
                            "parent_selector": node.get_selector(),
                            "pattern": desc,
                            "tag": sig_tag,
                            "class": sig_class,
                            "count": count,
                            "loop_candidate": True,
                            "review_required": True
                        })

            for child in node.children:
                _find_repeats(child)

        _find_repeats(root)
        return repeated_groups
