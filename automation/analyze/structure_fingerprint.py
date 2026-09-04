"""
Generates and compares structural fingerprints of HTML DOM trees.

Provides structural parity validation between original and generated slides
without relying on fragile raw whitespace string comparisons.
"""

from typing import Any, Dict, List, Set

from .dependency_analyzer import DependencyAnalyzer
from .html_analyzer import DOMNode


class StructureFingerprint:
    """
    Generates deterministic structural fingerprints and computes parity diffs.
    """

    @classmethod
    def generate(cls, root: DOMNode) -> Dict[str, Any]:
        """
        Creates a structural fingerprint representing tags, IDs, classes,
        depth, counts, data attributes, ARIA attributes, and dependencies.
        """
        element_count = 0
        tag_sequence: List[str] = []
        id_set: Set[str] = set()
        class_set: Set[str] = set()
        data_attrs: Set[str] = set()
        aria_attrs: Set[str] = set()
        max_depth = 0

        def _walk(node: DOMNode):
            nonlocal element_count, max_depth
            if node.tag != "[root]":
                element_count += 1
                tag_sequence.append(node.tag)
                if node.depth > max_depth:
                    max_depth = node.depth

                node_id = node.get_id()
                if node_id:
                    id_set.add(node_id)

                for cls_name in node.get_classes():
                    class_set.add(cls_name)

                for attr_key in node.attrs.keys():
                    if attr_key.startswith("data-"):
                        data_attrs.add(attr_key)
                    elif attr_key.startswith("aria-"):
                        aria_attrs.add(attr_key)

            for child in node.children:
                _walk(child)

        _walk(root)

        dep_analyzer = DependencyAnalyzer()
        deps = dep_analyzer.analyze(root)

        return {
            "element_count": element_count,
            "max_depth": max_depth,
            "tag_sequence": tag_sequence,
            "id_set": sorted(list(id_set)),
            "class_set": sorted(list(class_set)),
            "data_attrs": sorted(list(data_attrs)),
            "aria_attrs": sorted(list(aria_attrs)),
            "stylesheets": deps.get("stylesheets", []),
            "scripts": deps.get("scripts", []),
            "runtime_contract": deps.get("runtime_contract", {})
        }

    @classmethod
    def compare(cls, original_fp: Dict[str, Any], generated_fp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compares two fingerprints and returns structured parity details.
        """
        orig_ids = set(original_fp.get("id_set", []))
        gen_ids = set(generated_fp.get("id_set", []))
        missing_ids = sorted(list(orig_ids - gen_ids))
        extra_ids = sorted(list(gen_ids - orig_ids))

        orig_classes = set(original_fp.get("class_set", []))
        gen_classes = set(generated_fp.get("class_set", []))
        missing_classes = sorted(list(orig_classes - gen_classes))
        extra_classes = sorted(list(gen_classes - orig_classes))

        orig_data = set(original_fp.get("data_attrs", []))
        gen_data = set(generated_fp.get("data_attrs", []))
        missing_data = sorted(list(orig_data - gen_data))

        orig_aria = set(original_fp.get("aria_attrs", []))
        gen_aria = set(generated_fp.get("aria_attrs", []))
        missing_aria = sorted(list(orig_aria - gen_aria))

        orig_css = set(original_fp.get("stylesheets", []))
        gen_css = set(generated_fp.get("stylesheets", []))
        missing_css = sorted(list(orig_css - gen_css))

        orig_js = set(original_fp.get("scripts", []))
        gen_js = set(generated_fp.get("scripts", []))
        missing_js = sorted(list(orig_js - gen_js))

        # Core runtime parity check
        runtime_ok = (
            original_fp.get("runtime_contract", {}).get("data_slide") ==
            generated_fp.get("runtime_contract", {}).get("data_slide")
        )

        is_parity_match = (
            len(missing_ids) == 0 and
            len(missing_classes) == 0 and
            len(missing_css) == 0 and
            len(missing_js) == 0 and
            runtime_ok
        )

        return {
            "is_parity_match": is_parity_match,
            "element_count": {
                "original": original_fp.get("element_count", 0),
                "generated": generated_fp.get("element_count", 0),
                "diff": generated_fp.get("element_count", 0) - original_fp.get("element_count", 0)
            },
            "missing_ids": missing_ids,
            "extra_ids": extra_ids,
            "missing_classes": missing_classes,
            "extra_classes": extra_classes,
            "missing_data_attrs": missing_data,
            "missing_aria_attrs": missing_aria,
            "missing_stylesheets": missing_css,
            "missing_scripts": missing_js,
            "runtime_slide_match": runtime_ok
        }
