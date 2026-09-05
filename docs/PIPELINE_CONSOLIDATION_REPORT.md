# Pipeline Consolidation & Analysis Report

- **Document ID:** PIPELINE-CONSOLIDATION-01
- **Date:** 2026-09-05
- **Target Repository:** `PR-1A1`
- **Scope:** `automation/` (Python) vs `renderer/` (Node.js) Architectural Analysis & Decision

---

## 1. Executive Summary

`PR-1A1` 저장소에는 현재 두 개의 독립적인 렌더링/검증 파이프라인이 공존하고 있습니다.
본 분석을 통해 두 파이프라인의 입출력, 대상 산출물, 테스트 현황, 의존성 관계를 전수 조사하였으며, **무조건적인 일방 삭제 대신 명확한 책임 분리와 장기적 통합 로드맵**을 수립하였습니다.

---

## 2. 파이프라인별 상세 분석

### 2.1 Python Pipeline (`automation/`)
- **주요 파일:** `build.py`, `validate.py`, `create_slide.py`, `render/jinja_renderer.py`
- **입력 데이터:**
  - `automation/data/slide_{id}.json` (슬라이드별 정규화된 데이터)
  - `automation/templates/slide_{id}.html.j2` (Jinja2 HTML 템플릿)
- **출력 산출물:**
  - `PRD-PO/html/분리된 html/{num}번 슬라이드.html` (16:9 프레젠테이션 슬라이드)
  - `automation/dist/{num}번 슬라이드.html`
- **검증 및 테스트:**
  - `automation/tests/`: 총 50개 테스트 (100% Pass)
  - 원본 DOM 지문(StructureFingerprint)과 렌더링 결과 간의 Parity 회귀 테스트
- **역할 및 책임:** **발표자료(Presentation Slide Deck) 자동화 엔진**

---

### 2.2 Node.js Pipeline (`renderer/`)
- **주요 파일:** `index.js`, `loader.js`, `validator.js`, `transformer.js`, `renderers/`
- **입력 데이터:**
  - `content/domains/auth/apms-auth.yaml` (도메인 명세 YAML)
  - `registry/evidence.yaml`, `registry/documents.yaml`, `registry/relations.yaml`
  - `design-system/` (CSS 토큰 및 컴포넌트)
- **출력 산출물:**
  - `rendered/longform/apms-auth.html` (상세 기술 문서)
  - `rendered/feature/apms-auth.html` (기능 소개서)
  - `rendered/technical/apms-auth.html` (기술 아키텍처 스펙)
  - `rendered/slide/apms-auth.html` (도메인 요약 슬라이드)
  - `rendered/evidence/apms-auth.html` (증거 검증 보고서)
  - `rendered/_golden/` (골든 스냅샷)
- **검증 및 테스트:**
  - `link_validator.js`, `impact_analyzer.js`
- **역할 및 책임:** **다형적 도메인 기술 문서(Polymorphic Technical Document) 생성 엔진**

---

## 3. 비교 매트릭스

| 비교 항목 | `automation/` (Python) | `renderer/` (Node.js) |
| :--- | :--- | :--- |
| **주요 런타임** | Python 3.12 (Jinja2, jsonschema, pyyaml) | Node.js v24 (Native ESM/CJS) |
| **목적 산출물** | 16:9 정밀 발표 슬라이드 HTML | 5대 관점(Longform/Feature/Tech/Slide/Evidence) HTML 문서 |
| **입력 포맷** | JSON + Jinja2 템플릿 | YAML + Model Contracts |
| **스타일링 의존** | 원본 슬라이드 CSS 및 개별 CSS | `design-system/` 통합 CSS 토큰 |
| **테스트 상태** | 50개 unittest/pytest 100% Pass | 골든 파일 기반 E2E 검증 통과 |
| **상호 의존성** | 독립적 동작 (renderer에 비의존) | 독립적 동작 (automation에 비의존) |

---

## 4. 통합 및 정비 결정 (Consolidation Decision)

1. **즉각 삭제 금지 (Preserve Both with Boundary):**
   - 두 엔진은 서로 다른 최종 산출물(슬라이드 덱 vs 도메인 5종 문서)을 생산하고 있으며, 둘 다 현재 정상 동작하고 빌드 테스트를 통과함.
   - 어느 하나를 강제로 삭제할 경우 해당 산출물(`PRD-PO/html` 또는 `rendered/`)의 갱신 파이프라인이 즉시 단절됨.
2. **명확한 책임 영역 분리 (Clear Separation of Concerns):**
   - **`automation/`** ➔ **Presentation & Slide Engine**: 포트폴리오 슬라이드 덱 렌더링 및 유효성 검증 담당.
   - **`renderer/`** ➔ **Documentation & Domain View Engine**: 도메인 YAML 기반 5종 기술 문서 렌더링 담당.
3. **통합 검증 스크립트 구축 (`automation/validate.py`):**
   - Python의 `automation/validate.py`를 최상위 Orchestrator로 확장하여, Slide 데이터뿐만 아니라 Evidence Registry, Claim Schemas, Commit SHA, Git 정합성을 모두 포괄하여 일괄 검증할 수 있도록 중앙 통제화.
