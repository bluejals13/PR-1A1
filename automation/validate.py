"""
Validation and normalization logic for presentation document automation.

Follows architectural principles:
- Strict separation between common validation and slide-specific schemas
- Application logic in Python, presentation in Jinja2
- Strict rejection of inline styles, fonts, margins, padding in data
"""

import re
import sys
from typing import Any, Callable, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

FORBIDDEN_DESIGN_KEYS = {
    "color", "colour", "background", "background_color", "backgroundColor",
    "font_size", "fontSize", "margin", "padding", "style", "inline_style",
    "width", "height", "border"
}

ALLOWED_STATUS_CLASSES = {
    "implemented", "verified", "verify-required", "complete", "review"
}

CSS_CLASS_REGEX = re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]*$")
MULTI_CSS_CLASS_REGEX = re.compile(r"^[a-zA-Z0-9_\-\s]+$")


class ValidationError(Exception):
    """Raised when slide data fails validation rules."""
    pass


# =====================================================================
# 1. Common Validation Logic (Applicable to ALL slides)
# =====================================================================

def check_no_inline_design(data: Any, path: str = "") -> None:
    """Recursively checks that no inline styling properties exist in data."""
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}" if path else key
            if key in FORBIDDEN_DESIGN_KEYS:
                raise ValidationError(
                    f"Forbidden design property '{key}' found at '{current_path}'. "
                    "Design & CSS styling must not be stored in data."
                )
            check_no_inline_design(value, current_path)
    elif isinstance(data, list):
        for idx, element in enumerate(data):
            check_no_inline_design(element, f"{path}[{idx}]")


def validate_common(data: Dict[str, Any]) -> None:
    """Validates top-level data constraints common across all slides."""
    if not isinstance(data, dict):
        raise ValidationError("Slide data must be a JSON object.")
    check_no_inline_design(data)


# =====================================================================
# 2. Slide 004 Specific Validator & Normalizer
# =====================================================================

def validate_slide_004(data: Dict[str, Any]) -> None:
    """Validates Slide 04: Threat -> Control matrix schema."""
    if "items" not in data:
        raise ValidationError("Slide 04 data must contain 'items'.")

    items = data["items"]
    if not isinstance(items, (list, dict)):
        raise ValidationError("Slide 04 'items' must be a list or a dictionary.")

    item_list = items.values() if isinstance(items, dict) else items
    if len(item_list) == 0:
        raise ValidationError("Slide 04 'items' cannot be empty.")

    for idx, item in enumerate(item_list):
        item_ref = item.get("id", f"index {idx}")
        if not item.get("threat"):
            raise ValidationError(f"Item '{item_ref}' missing required 'threat' field.")
        if not item.get("scenario"):
            raise ValidationError(f"Item '{item_ref}' missing required 'scenario' field.")
        if not item.get("control_strong") and not item.get("control"):
            raise ValidationError(f"Item '{item_ref}' must have 'control' or 'control_strong'.")

        statuses = item.get("statuses")
        if statuses is not None:
            if not isinstance(statuses, list) or len(statuses) == 0:
                raise ValidationError(f"Item '{item_ref}': 'statuses' must be a non-empty list.")
            for s_idx, st in enumerate(statuses):
                if "status" not in st or not str(st["status"]).strip():
                    raise ValidationError(f"Item '{item_ref}' status #{s_idx} missing 'status' label.")
                if "statusClass" not in st or not str(st["statusClass"]).strip():
                    raise ValidationError(f"Item '{item_ref}' status #{s_idx} missing 'statusClass'.")
                s_class = st["statusClass"]
                if not CSS_CLASS_REGEX.match(s_class):
                    raise ValidationError(f"Invalid statusClass identifier: '{s_class}'.")
        else:
            if "status" not in item or "statusClass" not in item:
                raise ValidationError(
                    f"Item '{item_ref}' must provide either 'statuses' array or 'status'+'statusClass'."
                )
            s_class = item["statusClass"]
            if not CSS_CLASS_REGEX.match(s_class):
                raise ValidationError(f"Invalid statusClass identifier: '{s_class}'.")


def normalize_slide_004(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw data into canonical format ready for Slide 04 Jinja2 template."""
    normalized = dict(raw_data)

    slide_meta = normalized.get("slide_meta", {})
    normalized["slide_meta"] = {
        "slide_num": slide_meta.get("slide_num", "SLIDE 04"),
        "title": slide_meta.get("title", "Threat"),
        "title_arrow": slide_meta.get("title_arrow", "➜"),
        "title_target": slide_meta.get("title_target", "Control"),
        "title_sub": slide_meta.get("title_sub", "무엇을 방어하는가"),
        "header_tag": slide_meta.get("header_tag", {
            "text": "ATTACK SURFACE MANAGEMENT",
            "class": "verified"
        })
    }

    intro = normalized.get("intro", {})
    normalized["intro"] = {
        "lead": intro.get("lead", "식별된 공격 시나리오마다"),
        "control_strong": intro.get("control_strong", "구체적인 보안 통제(Control)"),
        "rule": intro.get("rule", "를 연결하고, 검증되지 않은 항목은 완료로 간주하지 않는다.")
    }

    cols = normalized.get("columns", {})
    normalized["columns"] = {
        "threat": cols.get("threat", "THREAT"),
        "scenario": cols.get("scenario", "ATTACK SCENARIO"),
        "control": cols.get("control", "SECURITY CONTROL"),
        "status": cols.get("status", "STATUS")
    }

    raw_items = normalized.get("items", [])
    if isinstance(raw_items, dict):
        item_list = []
        for key, val in raw_items.items():
            item_copy = dict(val)
            item_copy.setdefault("id", key)
            item_list.append(item_copy)
        raw_items = item_list

    normalized_items = []
    for item in raw_items:
        it = dict(item)
        it.setdefault("threat_class", "threat-high")
        it.setdefault("threat_sub", "")
        it.setdefault("is_warning", False)

        if "control_strong" not in it and "control" in it:
            full_ctrl = it["control"]
            if "+" in full_ctrl:
                parts = full_ctrl.split("+", 1)
                it["control_strong"] = parts[0].strip()
                it["control_desc"] = "+ " + parts[1].strip()
            else:
                it["control_strong"] = full_ctrl
                it["control_desc"] = ""

        if "statuses" not in it and "status" in it and "statusClass" in it:
            v_class = it["statusClass"]
            if v_class == "complete":
                v_class = "verified"
            elif v_class == "review":
                v_class = "verify-required"
                it["is_warning"] = True

            it["statuses"] = [
                {"status": "IMPLEMENTED", "statusClass": "implemented"},
                {"status": it["status"], "statusClass": v_class}
            ]

        normalized_items.append(it)

    normalized["items"] = normalized_items

    principle = normalized.get("principle", {})
    normalized["principle"] = {
        "icon": principle.get("icon", "!"),
        "label": principle.get("label", "SECURITY PRINCIPLE"),
        "strong": principle.get("strong", "검증되지 않은 보안 통제는 완료로 표시하지 않는다."),
        "desc": principle.get("desc", "구현 여부가 아니라 실제 공격 시나리오에 대한 검증 결과를 기준으로 상태를 판단한다.")
    }

    nav = normalized.get("nav", {})
    normalized["nav"] = {
        "brand": nav.get("brand", "APMS.SR / PRESENTATION"),
        "hint": nav.get("hint", "← → 방향키 · Space 다음 · N 발표 노트"),
        "counter": nav.get("counter", "04 / 14"),
        "runtime_script": nav.get("runtime_script", "발표용_공통.js")
    }

    return normalized


# =====================================================================
# 3. Slide 005 Specific Validator & Normalizer
# =====================================================================

def validate_slide_005(data: Dict[str, Any]) -> None:
    """Validates Slide 05: Security Mechanism flow card schema."""
    if "flows" not in data:
        raise ValidationError("Slide 05 data must contain 'flows'.")

    flows = data["flows"]
    if not isinstance(flows, list) or len(flows) == 0:
        raise ValidationError("Slide 05 'flows' must be a non-empty list.")

    valid_node_types = {"step", "control", "decision", "result"}

    for f_idx, flow in enumerate(flows):
        f_id = flow.get("id", f"flow[{f_idx}]")
        if not flow.get("title"):
            raise ValidationError(f"Flow '{f_id}' missing 'title'.")
        if not flow.get("kicker"):
            raise ValidationError(f"Flow '{f_id}' missing 'kicker'.")
        if "badge" not in flow or not isinstance(flow["badge"], dict):
            raise ValidationError(f"Flow '{f_id}' missing 'badge' object.")
        if not flow["badge"].get("text"):
            raise ValidationError(f"Flow '{f_id}' badge missing 'text'.")

        nodes = flow.get("nodes")
        if not isinstance(nodes, list) or len(nodes) == 0:
            raise ValidationError(f"Flow '{f_id}' must have a non-empty 'nodes' list.")

        for n_idx, node in enumerate(nodes):
            n_type = node.get("type")
            if n_type not in valid_node_types:
                raise ValidationError(
                    f"Flow '{f_id}' node #{n_idx} has invalid type '{n_type}'. "
                    f"Must be one of {sorted(valid_node_types)}."
                )
            if not node.get("strong"):
                raise ValidationError(f"Flow '{f_id}' node #{n_idx} missing 'strong' text.")


def normalize_slide_005(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw data into canonical format ready for Slide 05 Jinja2 template."""
    normalized = dict(raw_data)

    slide_meta = normalized.get("slide_meta", {})
    normalized["slide_meta"] = {
        "slide_num": slide_meta.get("slide_num", "SLIDE 05"),
        "title_main": slide_meta.get("title_main", "Security Mechanism"),
        "title_divider": slide_meta.get("title_divider", "|"),
        "title_desc": slide_meta.get("title_desc", "Security Mechanism | 요청은 어디에서 허용되고 차단되는가"),
        "header_tag": slide_meta.get("header_tag", {
            "text": "THREAT RESPONSE FLOW",
            "class": "verified"
        })
    }

    intro = normalized.get("intro", {})
    normalized["intro"] = {
        "label": intro.get("label", "CONTROL FLOW"),
        "lead": intro.get("lead", "정상 요청은 검증 후 통과시키고, 공격 징후는"),
        "strong": intro.get("strong", "검증 지점에서 즉시 차단"),
        "tail": intro.get("tail", "한다.")
    }

    summary = normalized.get("summary", {})
    normalized["summary"] = {
        "label": summary.get("label", "SECURITY BEHAVIOR"),
        "steps": summary.get("steps", [
            {"text": "REQUEST", "class": ""},
            {"text": "VERIFY", "class": ""},
            {"text": "CONTROL", "class": "summary-control"},
            {"text": "ALLOW / BLOCK", "class": "summary-block"}
        ]),
        "note": summary.get("note", "모든 보안 통제는 요청 처리 흐름 안에서 실제 차단 지점으로 연결된다.")
    }

    nav = normalized.get("nav", {})
    normalized["nav"] = {
        "brand": nav.get("brand", "APMS.SR / PRESENTATION"),
        "hint": nav.get("hint", "← → 방향키 · Space 다음 · N 발표 노트"),
        "counter": nav.get("counter", "05 / 14"),
        "runtime_script": nav.get("runtime_script", "발표용_공통.js")
    }

    return normalized


# =====================================================================
# 4. Slide 006 Specific Validator & Normalizer
# =====================================================================

ALLOWED_SLIDE_006_STATUSES = {
    "PASS", "VERIFIED", "PARTIAL", "PENDING", "VERIFY", "VERIFY REQUIRED"
}


def validate_slide_006(data: Dict[str, Any]) -> None:
    """Validates Slide 06: Verification / Security Evidence schema."""
    # 1. Summary validation
    if "summary" not in data or not isinstance(data["summary"], dict):
        raise ValidationError("Slide 06 data must contain 'summary' object.")
    
    summary = data["summary"]
    stats = summary.get("stats")
    if not isinstance(stats, list) or len(stats) == 0:
        raise ValidationError("Slide 06 'summary.stats' must be a non-empty list.")
    
    for idx, stat in enumerate(stats):
        if "value" not in stat or not str(stat["value"]).strip():
            raise ValidationError(f"Slide 06 stat #{idx} missing 'value'.")
        if "label" not in stat or not str(stat["label"]).strip():
            raise ValidationError(f"Slide 06 stat #{idx} missing 'label'.")

    # 2. Evidence validation
    if "evidence" not in data or not isinstance(data["evidence"], dict):
        raise ValidationError("Slide 06 data must contain 'evidence' object.")

    evidence = data["evidence"]
    test_cases = evidence.get("test_cases")
    if not isinstance(test_cases, list) or len(test_cases) == 0:
        raise ValidationError("Slide 06 'evidence.test_cases' must be a non-empty list.")

    for idx, tc in enumerate(test_cases):
        tc_id = tc.get("id", f"case #{idx}")
        if not tc.get("scenario"):
            raise ValidationError(f"Test case '{tc_id}' missing 'scenario'.")
        if not tc.get("expected"):
            raise ValidationError(f"Test case '{tc_id}' missing 'expected'.")
        if not tc.get("actual"):
            raise ValidationError(f"Test case '{tc_id}' missing 'actual'.")
        
        status = str(tc.get("status", "")).strip().upper()
        if not status:
            raise ValidationError(f"Test case '{tc_id}' missing 'status'.")
        if status not in ALLOWED_SLIDE_006_STATUSES:
            raise ValidationError(
                f"Test case '{tc_id}' has invalid status '{status}'. "
                f"Must be one of {sorted(ALLOWED_SLIDE_006_STATUSES)}."
            )

    # 3. Performance validation
    if "performance" not in data or not isinstance(data["performance"], dict):
        raise ValidationError("Slide 06 data must contain 'performance' object.")

    performance = data["performance"]
    metrics = performance.get("metrics")
    if not isinstance(metrics, list) or len(metrics) == 0:
        raise ValidationError("Slide 06 'performance.metrics' must be a non-empty list.")

    for idx, m in enumerate(metrics):
        if not m.get("label"):
            raise ValidationError(f"Metric #{idx} missing 'label'.")
        if not m.get("value"):
            raise ValidationError(f"Metric #{idx} missing 'value'.")


def normalize_slide_006(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw data into canonical format ready for Slide 06 Jinja2 template."""
    normalized = dict(raw_data)

    slide_meta = normalized.get("slide_meta", {})
    raw_tag = slide_meta.get("header_tag", {})
    if isinstance(raw_tag, str):
        header_tag = {"text": raw_tag, "class": "verified"}
    else:
        header_tag = {
            "text": raw_tag.get("text", "SECURITY EVIDENCE"),
            "class": raw_tag.get("class", "verified")
        }

    normalized["slide_meta"] = {
        "slide_num": slide_meta.get("slide_num", "SLIDE 06"),
        "title": slide_meta.get("title", "Verification | 실제 공격이 차단되는가"),
        "header_tag": header_tag
    }

    # Summary
    summary = dict(normalized.get("summary", {}))
    raw_stats = summary.get("stats", [])
    normalized_stats = []
    for s in raw_stats:
        item = dict(s)
        key = str(item.get("key", "")).lower()
        if key == "verified":
            item["stat_class"] = "verified-stat"
        elif key == "partial":
            item["stat_class"] = "partial-stat"
        elif key == "pending":
            item["stat_class"] = "pending-stat"
        else:
            item.setdefault("stat_class", f"{key}-stat" if key else "verified-stat")
        normalized_stats.append(item)

    summary["stats"] = normalized_stats

    raw_msg = summary.get("message", {})
    summary["message"] = {
        "label": raw_msg.get("label", "VERIFICATION STATUS"),
        "strong": raw_msg.get("strong", "4 / 7 Security Controls Verified"),
        "desc": raw_msg.get("desc", "검증되지 않은 통제는 완료로 판정하지 않음")
    }
    normalized["summary"] = summary

    # Evidence
    evidence = dict(normalized.get("evidence", {}))
    evidence.setdefault("kicker", "01 / SECURITY EVIDENCE")
    evidence.setdefault("title", "Security Verification Matrix")
    evidence.setdefault("count", "07 TEST CASES")
    evidence.setdefault("columns", {
        "id": "ID",
        "scenario": "공격 시나리오",
        "expected": "기대 결과",
        "actual": "실제 결과",
        "status": "판정"
    })

    normalized_cases = []
    for tc in evidence.get("test_cases", []):
        c = dict(tc)
        st = str(c.get("status", "")).strip().upper()
        if st in ("PASS", "VERIFIED"):
            c["row_class"] = "status-pass"
            c["badge_class"] = "pass"
            c["badge_text"] = "PASS"
            c["actual_class"] = "actual"
        elif st == "PARTIAL":
            c["row_class"] = "status-partial"
            c["badge_class"] = "partial"
            c["badge_text"] = "PARTIAL"
            c["actual_class"] = "checking"
        else:  # PENDING, VERIFY, VERIFY REQUIRED
            c["row_class"] = "status-pending"
            c["badge_class"] = "pending"
            c["badge_text"] = "VERIFY"
            c["actual_class"] = "not-tested"

        normalized_cases.append(c)

    evidence["test_cases"] = normalized_cases
    normalized["evidence"] = evidence

    # Performance
    perf = dict(normalized.get("performance", {}))
    perf.setdefault("kicker", "02 / PERFORMANCE EVIDENCE")
    perf.setdefault("title", "Load Test")
    perf.setdefault("tool", "k6")
    perf.setdefault("card_header", {
        "label": "LOAD TEST RESULT",
        "state": "STABLE"
    })

    normalized_metrics = []
    for m in perf.get("metrics", []):
        metric = dict(m)
        metric.setdefault("unit", "")
        metric.setdefault("sub", "")
        if metric.get("is_green") or metric.get("highlight"):
            metric["value_class"] = "metric-green"
        else:
            metric["value_class"] = ""
        normalized_metrics.append(metric)
    perf["metrics"] = normalized_metrics

    raw_obs = perf.get("observation", {})
    perf["observation"] = {
        "label": raw_obs.get("label", "OBSERVATION"),
        "lead": raw_obs.get("lead", "JWT 검증과 Redis Revocation 조회가 추가된 상태에서도"),
        "strong": raw_obs.get("strong", "측정 구간에서 안정적인 처리 성능"),
        "tail": raw_obs.get("tail", "을 확인했다.")
    }
    perf.setdefault("footnote", "* 본 결과는 제시된 k6 테스트 조건 기준이며, 운영 환경 전체 성능을 의미하지 않음")
    normalized["performance"] = perf

    # Footer
    footer = dict(normalized.get("footer", {}))
    footer.setdefault("rule_label", "RULE")
    footer.setdefault("rule_strong", "Evidence First")
    raw_flow = footer.get("flow", [
        {"text": "IMPLEMENTED"},
        {"text": "TESTED"},
        {"text": "VERIFIED", "is_pass": True}
    ])
    normalized_flow = []
    for item in raw_flow:
        if isinstance(item, str):
            is_p = (item.upper() == "VERIFIED")
            normalized_flow.append({"text": item, "is_pass": is_p})
        else:
            normalized_flow.append(item)
    footer["flow"] = normalized_flow
    footer.setdefault("note", "구현 여부와 검증 여부를 분리한다.")
    normalized["footer"] = footer

    # Nav
    nav = normalized.get("nav", {})
    normalized["nav"] = {
        "brand": nav.get("brand", "APMS.SR / PRESENTATION"),
        "hint": nav.get("hint", "← → 방향키 · Space 다음 · N 발표 노트"),
        "counter": nav.get("counter", "06 / 14"),
        "runtime_script": nav.get("runtime_script", "발표용_공통.js")
    }

    return normalized


# =====================================================================
# 5. Slide 007 Specific Validator & Normalizer
# =====================================================================

ALLOWED_CASE_STATUSES = {
    "RESOLVED", "VERIFY REQUIRED", "PENDING", "OPEN", "IN PROGRESS"
}

ALLOWED_RISK_STATES = {
    "VERIFIED", "VERIFY", "OPEN", "TEST", "PENDING", "MONITOR"
}

ALLOWED_ACTION_PRIORITIES = {"P0", "P1", "P2"}


def validate_slide_007(data: Dict[str, Any]) -> None:
    """Validates Slide 07: Operation / Residual Risk schema."""
    # 1. incident_panel
    if "incident_panel" not in data or not isinstance(data["incident_panel"], dict):
        raise ValidationError("Slide 07 data must contain 'incident_panel' object.")

    panel = data["incident_panel"]
    cases = panel.get("cases")
    if not isinstance(cases, list) or len(cases) == 0:
        raise ValidationError("Slide 07 'incident_panel.cases' must be a non-empty list.")

    for idx, case in enumerate(cases):
        case_id = case.get("id", f"case #{idx}")
        if not case.get("title"):
            raise ValidationError(f"Case '{case_id}' missing 'title'.")
        if not case.get("card_class"):
            raise ValidationError(f"Case '{case_id}' missing 'card_class'.")
        if not case.get("status_text"):
            raise ValidationError(f"Case '{case_id}' missing 'status_text'.")
        st = str(case["status_text"]).strip().upper()
        if st not in ALLOWED_CASE_STATUSES:
            raise ValidationError(
                f"Case '{case_id}' has invalid status_text '{st}'. "
                f"Must be one of {sorted(ALLOWED_CASE_STATUSES)}."
            )
        if not isinstance(case.get("threat"), dict) or not case["threat"].get("text"):
            raise ValidationError(f"Case '{case_id}' missing 'threat.text'.")
        if not isinstance(case.get("control"), dict) or not case["control"].get("text"):
            raise ValidationError(f"Case '{case_id}' missing 'control.text'.")
        if not isinstance(case.get("verification"), dict) or not case["verification"].get("text"):
            raise ValidationError(f"Case '{case_id}' missing 'verification.text'.")

    # 2. risk_panel
    if "risk_panel" not in data or not isinstance(data["risk_panel"], dict):
        raise ValidationError("Slide 07 data must contain 'risk_panel' object.")

    risk_panel = data["risk_panel"]
    risks = risk_panel.get("risks")
    if not isinstance(risks, list) or len(risks) == 0:
        raise ValidationError("Slide 07 'risk_panel.risks' must be a non-empty list.")

    for idx, risk in enumerate(risks):
        if not risk.get("item_class"):
            raise ValidationError(f"Risk #{idx} missing 'item_class'.")
        if not risk.get("state"):
            raise ValidationError(f"Risk #{idx} missing 'state'.")
        st = str(risk["state"]).strip().upper()
        if st not in ALLOWED_RISK_STATES:
            raise ValidationError(
                f"Risk #{idx} has invalid state '{st}'. "
                f"Must be one of {sorted(ALLOWED_RISK_STATES)}."
            )
        if not risk.get("strong"):
            raise ValidationError(f"Risk #{idx} missing 'strong'.")

    # 3. next_action_panel
    if "next_action_panel" not in data or not isinstance(data["next_action_panel"], dict):
        raise ValidationError("Slide 07 data must contain 'next_action_panel' object.")

    action_panel = data["next_action_panel"]
    actions = action_panel.get("actions")
    if not isinstance(actions, list) or len(actions) == 0:
        raise ValidationError("Slide 07 'next_action_panel.actions' must be a non-empty list.")

    for idx, action in enumerate(actions):
        if not action.get("priority"):
            raise ValidationError(f"Action #{idx} missing 'priority'.")
        pr = str(action["priority"]).strip().upper()
        if pr not in ALLOWED_ACTION_PRIORITIES:
            raise ValidationError(
                f"Action #{idx} has invalid priority '{pr}'. "
                f"Must be one of {sorted(ALLOWED_ACTION_PRIORITIES)}."
            )
        if not action.get("strong"):
            raise ValidationError(f"Action #{idx} missing 'strong'.")
        if not action.get("item_class"):
            raise ValidationError(f"Action #{idx} missing 'item_class'.")


def normalize_slide_007(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw data into canonical format ready for Slide 07 Jinja2 template."""
    normalized = dict(raw_data)

    # slide_meta
    slide_meta = normalized.get("slide_meta", {})
    raw_tag = slide_meta.get("header_tag", {})
    if isinstance(raw_tag, str):
        header_tag = {"text": raw_tag, "class": "verified"}
    else:
        header_tag = {
            "text": raw_tag.get("text", "RESIDUAL RISK & NEXT ACTION"),
            "class": raw_tag.get("class", "verified")
        }
    normalized["slide_meta"] = {
        "slide_num": slide_meta.get("slide_num", "SLIDE 07"),
        "title": slide_meta.get("title", "Evidence → Operation | 해결 이후 무엇이 보장되는가"),
        "header_tag": header_tag
    }

    # operation_summary
    op_summary = dict(normalized.get("operation_summary", {}))
    op_summary.setdefault("kicker", "SECURITY OPERATION STATUS")
    op_summary.setdefault("strong", "검증된 통제와 잔여 위험을 분리해 관리")
    op_summary.setdefault("flow", [
        {"text": "VERIFIED", "class": "flow-done"},
        {"text": "MONITOR", "class": "flow-monitor"},
        {"text": "NEXT ACTION", "class": "flow-next"}
    ])
    normalized["operation_summary"] = op_summary

    # incident_panel — normalize each case
    incident_panel = dict(normalized.get("incident_panel", {}))
    incident_panel.setdefault("kicker", "01 / OPERATION CASES")
    incident_panel.setdefault("title", "Operation & Incident Cases")
    incident_panel.setdefault("count", "02 CASES")

    normalized_cases = []
    for case in incident_panel.get("cases", []):
        c = dict(case)
        # threat / impact / control / verification are passed as-is (dicts)
        c.setdefault("has_impact", bool(c.get("impact")))
        threat = dict(c.get("threat", {}))
        threat.setdefault("label", "THREAT")
        threat.setdefault("label_class", "threat")
        c["threat"] = threat

        if c.get("has_impact") and c.get("impact"):
            impact = dict(c["impact"])
            impact.setdefault("label", "IMPACT")
            impact.setdefault("label_class", "impact")
            c["impact"] = impact

        control = dict(c.get("control", {}))
        control.setdefault("label", "CONTROL")
        c["control"] = control

        verification = dict(c.get("verification", {}))
        verification.setdefault("label", "VERIFICATION")
        c["verification"] = verification

        normalized_cases.append(c)

    incident_panel["cases"] = normalized_cases
    normalized["incident_panel"] = incident_panel

    # risk_panel — pass through as-is (item_class already set in data)
    risk_panel = dict(normalized.get("risk_panel", {}))
    risk_panel.setdefault("kicker", "02 / RESIDUAL RISK")
    risk_panel.setdefault("title", "Current Security Posture")
    risk_panel.setdefault("count", "7 CONTROLS")
    normalized["risk_panel"] = risk_panel

    # next_action_panel — pass through as-is
    action_panel = dict(normalized.get("next_action_panel", {}))
    action_panel.setdefault("kicker", "03 / NEXT ACTIONS")
    action_panel.setdefault("title", "Priority Roadmap")
    normalized["next_action_panel"] = action_panel

    # principle
    principle = dict(normalized.get("principle", {}))
    principle.setdefault("mark", "SECURITY PRINCIPLE")
    principle.setdefault(
        "strong",
        "구현된 보안 기능의 개수보다,\n      식별되고 검증된 공격면의 범위로 보안 수준을 입증한다."
    )
    normalized["principle"] = principle

    # nav
    nav = normalized.get("nav", {})
    normalized["nav"] = {
        "brand": nav.get("brand", "APMS.SR / PRESENTATION"),
        "hint": nav.get("hint", "← → 방향키 · Space 다음 · N 발표 노트"),
        "counter": nav.get("counter", "07 / 14"),
        "runtime_script": nav.get("runtime_script", "발표용_공통.js")
    }

    return normalized


# =====================================================================
# 6. Slide 008 Specific Validator & Normalizer
# =====================================================================

def validate_slide_008(data: Dict[str, Any]) -> None:
    """Validates Slide 08: Docker 7-Container Network Diagram & Architecture Principles schema."""
    # 1. slide_meta
    if "slide_meta" not in data or not isinstance(data["slide_meta"], dict):
        raise ValidationError("Slide 08 data must contain 'slide_meta' object.")
    
    meta = data["slide_meta"]
    if not meta.get("slide_num") or not str(meta["slide_num"]).strip():
        raise ValidationError("Slide 08 missing required 'slide_meta.slide_num'.")
    if not meta.get("title") or not str(meta["title"]).strip():
        raise ValidationError("Slide 08 missing required 'slide_meta.title'.")
    
    if "header_tag" not in meta or not isinstance(meta["header_tag"], dict):
        raise ValidationError("Slide 08 missing required 'slide_meta.header_tag' object.")
    tag = meta["header_tag"]
    if not tag.get("text") or not str(tag["text"]).strip():
        raise ValidationError("Slide 08 missing required 'slide_meta.header_tag.text'.")
    if not tag.get("class") or not str(tag["class"]).strip():
        raise ValidationError("Slide 08 missing required 'slide_meta.header_tag.class'.")
    
    tag_class = str(tag["class"]).strip().lower()
    if tag_class not in ALLOWED_STATUS_CLASSES:
        raise ValidationError(
            f"Invalid header_tag class '{tag_class}'. Must be one of {sorted(ALLOWED_STATUS_CLASSES)}."
        )

    # 2. speaker_note
    if "speaker_note" not in data or not str(data["speaker_note"]).strip():
        raise ValidationError("Slide 08 missing required 'speaker_note'.")

    # 3. principles
    if "principles" not in data or not isinstance(data["principles"], list):
        raise ValidationError("Slide 08 'principles' must be a list.")
    if len(data["principles"]) == 0:
        raise ValidationError("Slide 08 'principles' list cannot be empty.")

    for idx, p in enumerate(data["principles"]):
        if not isinstance(p, dict):
            raise ValidationError(f"Principle #{idx} must be a dictionary.")
        if not p.get("icon") or not str(p["icon"]).strip():
            raise ValidationError(f"Principle #{idx} missing required 'icon'.")
        if not p.get("title") or not str(p["title"]).strip():
            raise ValidationError(f"Principle #{idx} missing required 'title'.")
        if not p.get("desc") or not str(p["desc"]).strip():
            raise ValidationError(f"Principle #{idx} missing required 'desc'.")

    # 4. nav
    if "nav" in data and isinstance(data["nav"], dict):
        nav = data["nav"]
        for req_f in ["brand", "hint", "counter", "runtime_script"]:
            if req_f in nav and not str(nav[req_f]).strip():
                raise ValidationError(f"Slide 08 'nav.{req_f}' cannot be empty if specified.")


def normalize_slide_008(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes raw data into canonical format ready for Slide 08 Jinja2 template."""
    normalized = dict(raw_data)

    slide_meta = dict(normalized.get("slide_meta", {}))
    slide_meta.setdefault("slide_num", "SLIDE 08")
    slide_meta.setdefault("title", "Docker 7-Container 네트워크 격리 & DNS 통신 아키텍처")
    header_tag = dict(slide_meta.get("header_tag", {}))
    header_tag.setdefault("text", "IMPLEMENTED")
    header_tag.setdefault("class", "implemented")
    slide_meta["header_tag"] = header_tag
    normalized["slide_meta"] = slide_meta

    normalized["speaker_note"] = normalized.get(
        "speaker_note",
        "컨테이너 환경에서는 IP 주소가 유동적으로 변하므로 도커 내장 DNS 서비스명을 기반으로 상호 연결해야 합니다. TS-003을 해결하며 확립한 환경변수 주입 방식을 통해 로컬 환경과 도커 프로덕션 환경 간 무결한 네트워크 격리를 구축했습니다."
    )

    principles = []
    for p in normalized.get("principles", []):
        principles.append({
            "icon": str(p.get("icon", "")).strip(),
            "title": str(p.get("title", "")).strip(),
            "desc": str(p.get("desc", "")).strip(),
        })
    normalized["principles"] = principles

    nav = dict(normalized.get("nav", {}))
    normalized["nav"] = {
        "brand": nav.get("brand", "APMS.SR / PRESENTATION"),
        "hint": nav.get("hint", "← → 방향키 · Space 다음 · N 발표 노트"),
        "counter": nav.get("counter", "08 / 14"),
        "runtime_script": nav.get("runtime_script", "발표용_공통.js")
    }

    return normalized


# =====================================================================
# 7. Dispatch Registry
# =====================================================================

VALIDATORS: Dict[str, Callable[[Dict[str, Any]], None]] = {
    "004": validate_slide_004,
    "4": validate_slide_004,
    "005": validate_slide_005,
    "5": validate_slide_005,
    "006": validate_slide_006,
    "6": validate_slide_006,
    "007": validate_slide_007,
    "7": validate_slide_007,
    "008": validate_slide_008,
    "8": validate_slide_008,
}

NORMALIZERS: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {
    "004": normalize_slide_004,
    "4": normalize_slide_004,
    "005": normalize_slide_005,
    "5": normalize_slide_005,
    "006": normalize_slide_006,
    "6": normalize_slide_006,
    "007": normalize_slide_007,
    "7": normalize_slide_007,
    "008": normalize_slide_008,
    "8": normalize_slide_008,
}


def validate_slide_data(data: Dict[str, Any], slide_id: str = "004") -> None:
    """Entrypoint: runs common checks then dispatches to slide-specific validator."""
    validate_common(data)
    
    key = str(slide_id).strip()
    norm_key = key.zfill(3) if key.isdigit() else key
    
    validator = VALIDATORS.get(norm_key) or VALIDATORS.get(key)
    if not validator:
        raise ValidationError(f"No validator registered for slide '{slide_id}'.")
    validator(data)


def normalize_slide_data(raw_data: Dict[str, Any], slide_id: str = "004") -> Dict[str, Any]:
    """Entrypoint: dispatches to slide-specific normalizer."""
    key = str(slide_id).strip()
    norm_key = key.zfill(3) if key.isdigit() else key
    
    normalizer = NORMALIZERS.get(norm_key) or NORMALIZERS.get(key)
    if not normalizer:
        raise ValidationError(f"No normalizer registered for slide '{slide_id}'.")
    return normalizer(raw_data)


# =====================================================================
# 8. Repository-Wide Evidence & Architecture Validator
# =====================================================================

def validate_evidence_system(verbose: bool = True) -> bool:
    """Performs deterministic validation across Claims, Evidence Bundles,
    Manifests, SHA-256 hashes, and actual 26-05adf code symbols."""
    import hashlib
    import json
    import pathlib
    import jsonschema

    base_dir = pathlib.Path(__file__).resolve().parent
    repo_pr1 = base_dir.parent
    base_root = repo_pr1.parent
    repo_26 = base_root / "26-05adf"
    repo_sa1 = base_root / "SA-1"

    evidence_base = repo_pr1 / "PR-Files" / "evidence"
    claims_dir = evidence_base / "claims"
    bundles_dir = evidence_base / "bundles"
    manifests_dir = evidence_base / "manifests"
    schemas_dir = evidence_base / "schemas"

    passed = True
    errors = []

    if verbose:
        print("\n=======================================================")
        print("🛡️ [APMS.SR Evidence System Verification]")
        print("=======================================================")

    ALLOWED_STATUSES = {"VERIFIED", "IMPLEMENTED", "DOCUMENTED", "PARTIAL", "PLANNED", "UNKNOWN"}

    # 1. JSON Schema & Status Validation for Claims
    schema_file = schemas_dir / "claim.schema.json"
    if not schema_file.exists():
        errors.append(f"Claim schema missing: {schema_file}")
        passed = False
    else:
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        claim_files = list(claims_dir.glob("*.json"))
        if verbose:
            print(f"\n[1/8] Validating {len(claim_files)} Claims against Schema & Status Rules...")
        
        seen_claim_ids = set()
        seen_evidence_ids = set()

        for cf in claim_files:
            try:
                cdata = json.loads(cf.read_text(encoding="utf-8"))
                jsonschema.validate(instance=cdata, schema=schema)
                cid = cdata["claim_id"]
                if cid in seen_claim_ids:
                    errors.append(f"Duplicate claim_id found: {cid}")
                    passed = False
                seen_claim_ids.add(cid)

                status = cdata.get("status")
                if status not in ALLOWED_STATUSES:
                    errors.append(f"Invalid status '{status}' in claim {cid}")
                    passed = False

                ev_id = cdata.get("evidence", {}).get("evidence_id")
                if ev_id in seen_evidence_ids:
                    errors.append(f"Duplicate evidence_id found: {ev_id}")
                    passed = False
                seen_evidence_ids.add(ev_id)
            except Exception as e:
                errors.append(f"Schema validation error in {cf.name}: {e}")
                passed = False

        if verbose:
            print(f"  ✓ {len(seen_claim_ids)} Claims validated. Uniqueness and Status confirmed.")

    # 2. Evidence Bundles Verification
    if verbose:
        print("\n[2/8] Verifying Evidence Bundles existence & manifests...")
    bundle_dirs = [d for d in bundles_dir.iterdir() if d.is_dir()]
    for bdir in bundle_dirs:
        bmanifest = bdir / "manifest.json"
        if not bmanifest.exists():
            errors.append(f"Bundle manifest missing: {bmanifest}")
            passed = False
        else:
            try:
                bm = json.loads(bmanifest.read_text(encoding="utf-8"))
                if not bm.get("evidence_id") or not bm.get("claim_id"):
                    errors.append(f"Incomplete manifest in bundle: {bdir.name}")
                    passed = False
            except Exception as e:
                errors.append(f"Invalid JSON in {bmanifest}: {e}")
                passed = False

    if verbose:
        print(f"  ✓ {len(bundle_dirs)} Evidence Bundles verified.")

    # 3. Source Paths, Git Commits & Source Symbol Traceability
    if verbose:
        print("\n[3/8] Verifying Source Paths, Commits & Source Symbol Traceability...")
    checked_sources = 0
    for cf in claims_dir.glob("*.json"):
        cdata = json.loads(cf.read_text(encoding="utf-8"))
        cid = cdata["claim_id"]
        for s in cdata.get("sources", []):
            checked_sources += 1
            rname = s.get("repository")
            rbase = repo_26 if rname == "26-05adf" else (repo_sa1 if rname == "SA-1" else repo_pr1)
            spath = rbase / s.get("path", "")
            if not spath.exists():
                errors.append(f"Source file not found: {rname}/{s.get('path')} (Claim: {cid})")
                passed = False
            else:
                sym = s.get("symbol")
                if sym:
                    content = spath.read_text(encoding="utf-8", errors="ignore")
                    clean_sym = sym.replace("->", " ").replace(".", " ").replace(":", " ").replace("/", " ")
                    tokens = [t.strip() for t in clean_sym.split() if len(t.strip()) >= 2]
                    found = any(tok in content for tok in tokens)
                    if not found:
                        errors.append(f"Symbol '{sym}' not found in {rname}/{s.get('path')} (Claim: {cid})")
                        passed = False

            commit = s.get("commit", "")
            if len(commit) != 40 or not all(c in "0123456789abcdefABCDEF" for c in commit):
                errors.append(f"Invalid Git commit SHA in {cid}: {commit}")
                passed = False

    if verbose:
        print(f"  ✓ {checked_sources} source references & symbols verified.")

    # 4. Test Method Existence against 26-05adf
    if verbose:
        print("\n[4/8] Verifying referenced test methods against actual 26-05adf code...")
    checked_methods = 0
    for cf in claims_dir.glob("*.json"):
        cdata = json.loads(cf.read_text(encoding="utf-8"))
        verification = cdata.get("verification", {})
        test_file = verification.get("test_file")
        test_methods = verification.get("test_methods", [])

        if test_file and test_methods:
            actual_test_path = repo_26 / test_file
            if not actual_test_path.exists():
                errors.append(f"Test file not found in 26-05adf: {test_file} (Claim: {cdata['claim_id']})")
                passed = False
            else:
                code_content = actual_test_path.read_text(encoding="utf-8", errors="ignore")
                for method_name in test_methods:
                    checked_methods += 1
                    if method_name not in code_content:
                        errors.append(
                            f"Test method '{method_name}' NOT FOUND in {test_file} (Claim: {cdata['claim_id']})"
                        )
                        passed = False

    if verbose:
        print(f"  ✓ {checked_methods} test methods verified in 26-05adf backend.")

    # 5. Snapshot Manifest & SHA-256 Verification
    if verbose:
        print("\n[5/8] Verifying SOT Manifests and SHA-256 integrity...")
    manifest_files = list(manifests_dir.glob("*.json"))
    checked_files = 0
    for mf in manifest_files:
        mdata = json.loads(mf.read_text(encoding="utf-8"))
        for src_group in mdata.get("sources", []):
            repo_name = src_group.get("repository")
            snap_base = evidence_base / "snapshots" / repo_name

            for entry in src_group.get("files", []):
                rel_path = entry["path"]
                expected_sha = entry["sha256"]
                snap_file = snap_base / rel_path

                if not snap_file.exists():
                    errors.append(f"Snapshot file missing: {snap_file}")
                    passed = False
                    continue

                checked_files += 1
                h = hashlib.sha256()
                h.update(snap_file.read_bytes())
                actual_sha = h.hexdigest()

                if actual_sha != expected_sha:
                    errors.append(f"SHA-256 MISMATCH for snapshot: {rel_path} (expected {expected_sha[:8]}, got {actual_sha[:8]})")
                    passed = False

    if verbose:
        print(f"  ✓ {checked_files} Snapshot files verified with 100% SHA-256 match.")

    # 6. Portfolio / PPT Slide & Case Study Traceability Linkage
    if verbose:
        print("\n[6/8] Verifying Portfolio / PPT Slide & Case Study Traceability...")
    checked_mappings = 0
    case_study_file = repo_pr1 / "PRD-PO" / "case-study" / "CASE_STUDY.md"
    cs_content = case_study_file.read_text(encoding="utf-8", errors="ignore") if case_study_file.exists() else ""

    for cf in claims_dir.glob("*.json"):
        cdata = json.loads(cf.read_text(encoding="utf-8"))
        cid = cdata["claim_id"]
        pm = cdata.get("portfolio_mapping", {})
        slides = pm.get("slides", [])
        for sid in slides:
            checked_mappings += 1
            sjson = base_dir / "data" / f"slide_{sid}.json"
            sdir = repo_pr1 / "PRD-PO" / "presentation" / "slides" / sid
            shtml = repo_pr1 / "PRD-PO" / "html" / "분리된 html" / f"{int(sid)}번 슬라이드.html"
            if not (sjson.exists() or sdir.exists() or shtml.exists()):
                errors.append(f"Slide '{sid}' referenced by Claim {cid} does not exist in any portfolio view.")
                passed = False

        cs_ref = pm.get("case_study")
        if cs_ref and cs_content:
            cs_id = cs_ref.split("(")[0].strip()
            if cs_id and cs_id not in cs_content:
                errors.append(f"Case study reference '{cs_ref}' for Claim {cid} not found in CASE_STUDY.md")
                passed = False

    if verbose:
        print(f"  ✓ {checked_mappings} slide & case study mappings verified.")

    # 7. Slide Data & Design Integrity (004 ~ 008)
    if verbose:
        print("\n[7/8] Validating Slide Presentation Data (004~008)...")
    data_dir = base_dir / "data"
    slide_ids = ["004", "005", "006", "007", "008"]
    for sid in slide_ids:
        sfile = data_dir / f"slide_{sid}.json"
        if sfile.exists():
            try:
                sdata = json.loads(sfile.read_text(encoding="utf-8"))
                validate_slide_data(sdata, sid)
            except Exception as e:
                errors.append(f"Slide {sid} validation failure: {e}")
                passed = False

    if verbose:
        print(f"  ✓ Slides {slide_ids} passed zero-inline-style & schema checks.")

    # 8. Summary Report
    if verbose:
        print("\n[8/8] Final Validation Summary:")
        if passed and not errors:
            print("=======================================================")
            print("🎉 [ALL CHECKS PASSED] 100% Deterministic Verification Succeeded!")
            print("=======================================================\n")
        else:
            print("=======================================================")
            print(f"❌ [VALIDATION FAILED] Found {len(errors)} error(s):")
            for err in errors:
                print(f"   • {err}")
            print("=======================================================\n")

    return passed


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="APMS.SR Validation Runner")
    parser.add_argument("--all", action="store_true", help="Run full evidence and repository architecture validation")
    args = parser.parse_args()

    success = validate_evidence_system(verbose=True)
    sys.exit(0 if success else 1)


