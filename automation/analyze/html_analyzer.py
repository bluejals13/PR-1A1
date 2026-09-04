"""
DOM tree parser and analyzer using Python's standard library html.parser.
"""

from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Set

VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr"
}


class DOMNode:
    """Represents a node in the parsed HTML DOM tree."""

    def __init__(
        self,
        tag: str,
        attrs: Optional[Dict[str, str]] = None,
        parent: Optional["DOMNode"] = None,
        depth: int = 0
    ):
        self.tag: str = tag.lower()
        self.attrs: Dict[str, str] = attrs or {}
        self.text_parts: List[str] = []
        self.children: List["DOMNode"] = []
        self.parent: Optional["DOMNode"] = parent
        self.depth: int = depth

    @property
    def text(self) -> str:
        """Returns direct text content concatenated and stripped."""
        return " ".join(part.strip() for part in self.text_parts if part.strip())

    def all_text(self) -> str:
        """Returns recursive text content of this node and all its descendants."""
        parts = [self.text] if self.text else []
        for child in self.children:
            child_text = child.all_text()
            if child_text:
                parts.append(child_text)
        return " ".join(parts).strip()

    def get_classes(self) -> Set[str]:
        """Returns the set of CSS class names on this element."""
        class_attr = self.attrs.get("class", "")
        return set(class_attr.split()) if class_attr else set()

    def get_id(self) -> Optional[str]:
        """Returns the id attribute of this element if present."""
        return self.attrs.get("id")

    def get_selector(self) -> str:
        """Constructs a CSS-like selector path representing this node."""
        parts = [self.tag]
        node_id = self.get_id()
        if node_id:
            parts.append(f"#{node_id}")
        classes = sorted(self.get_classes())
        if classes:
            parts.append("." + ".".join(classes))
        
        current = "".join(parts)
        if self.parent and self.parent.tag != "[root]":
            return f"{self.parent.get_selector()} > {current}"
        return current

    def find_all(
        self,
        tag: Optional[str] = None,
        class_name: Optional[str] = None,
        id_value: Optional[str] = None
    ) -> List["DOMNode"]:
        """Finds all descendant nodes matching the given tag, class, or id criteria."""
        matches: List["DOMNode"] = []

        def _traverse(node: "DOMNode"):
            is_match = True
            if tag and node.tag != tag.lower():
                is_match = False
            if class_name and class_name not in node.get_classes():
                is_match = False
            if id_value and node.get_id() != id_value:
                is_match = False

            if is_match and node.tag != "[root]":
                matches.append(node)

            for child in node.children:
                _traverse(child)

        _traverse(self)
        return matches

    def to_dict(self) -> Dict[str, Any]:
        """Serializes node and descendants to a dictionary."""
        return {
            "tag": self.tag,
            "attrs": self.attrs,
            "text": self.text,
            "selector": self.get_selector(),
            "depth": self.depth,
            "children": [child.to_dict() for child in self.children]
        }


class _DOMBuilder(HTMLParser):
    """HTMLParser that builds a DOMNode tree."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = DOMNode(tag="[root]", depth=0)
        self.current: DOMNode = self.root
        self.element_count = 0
        self.max_depth = 0

    def handle_starttag(self, tag: str, attrs: List[tuple]):
        tag_lower = tag.lower()
        attr_dict = {k.lower(): v for k, v in attrs if k is not None}
        new_depth = self.current.depth + 1
        self.element_count += 1
        if new_depth > self.max_depth:
            self.max_depth = new_depth

        node = DOMNode(
            tag=tag_lower,
            attrs=attr_dict,
            parent=self.current,
            depth=new_depth
        )
        self.current.children.append(node)

        if tag_lower not in VOID_ELEMENTS:
            self.current = node

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if tag_lower in VOID_ELEMENTS:
            return

        curr = self.current
        while curr and curr.tag != "[root]":
            if curr.tag == tag_lower:
                self.current = curr.parent or self.root
                break
            curr = curr.parent

    def handle_data(self, data: str):
        cleaned = data.strip()
        if cleaned:
            self.current.text_parts.append(cleaned)


class HTMLAnalyzer:
    """Analyzes HTML documents by parsing into a structured DOM tree."""

    def __init__(self):
        self.root: Optional[DOMNode] = None
        self.element_count = 0
        self.max_depth = 0

    def parse(self, html_content: str) -> DOMNode:
        """Parses HTML string into a DOMNode tree root."""
        builder = _DOMBuilder()
        builder.feed(html_content)
        self.root = builder.root
        self.element_count = builder.element_count
        self.max_depth = builder.max_depth
        return self.root

    def get_element_count(self) -> int:
        return self.element_count

    def get_max_depth(self) -> int:
        return self.max_depth

    def get_all_elements(self) -> List[DOMNode]:
        if not self.root:
            return []
        return self.root.find_all()
