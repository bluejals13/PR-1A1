# APMS.SR Presentation Automation Architecture

## 1. 개요 (Overview)

APMS.SR 프레젠테이션 자동화 시스템은 HTML 기반의 정밀 발표 슬라이드를 **분석(Analyze) ➔ 스캐폴딩(Scaffold) ➔ 사람 검토(Human Review) ➔ 유효성 검증(Validate) ➔ 정규화(Normalize) ➔ 렌더러 추상화(Renderer) ➔ 구조적 일치성 검증(Parity)**을 통해 결정론적(deterministic)으로 생성·관리하는 Python 기반 자동화 프레임워크입니다.

기존의 단순 `JSON ➔ Jinja2 ➔ HTML` 직접 변환 방식을 탈피하여, 원본 HTML의 DOM 트리와 런타임 의존성을 체계적으로 분석하고 렌더링 엔진을 프레임워크로부터 분리한 다계층 아키텍처를 구현합니다.

---

## 2. 전체 아키텍처 파이프라인 (Pipeline Architecture)

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. ORIGINAL PRESENTATION HTML                               │
│    PRD-PO/html/분리된 html/{num}번 슬라이드.html             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. DOM ANALYZER ENGINE (automation/analyze/)                │
│    ├── HTMLAnalyzer          : 표준 HTMLParser 기반 DOM 트리│
│    ├── ContentDetector       : 콘텐츠 후보 및 반복 구조 탐지│
│    ├── DependencyAnalyzer    : CSS, JS 및 런타임 ID 계약 추출│
│    └── StructureFingerprint  : 원본 DOM 지문(Baseline) 생성 │
└──────────────────────────────┬──────────────────────────────┘
                               │ create_slide.py
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. SCAFFOLD ARTIFACTS (With Review Notice)                  │
│    ├── automation/data/slide_{id}.json                      │
│    ├── automation/templates/slide_{id}.html.j2              │
│    └── automation/dist/baseline_slide_{id}.json             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
               ┌──────────────────────────────┐
               │   ⚠️  HUMAN REVIEW REQUIRED  │
               │  - 도메인 필드명 결정        │
               │  - 의미론적 상태(Enum) 확인  │
               │  - Template 변수 바인딩 검토 │
               │  - Validator/Normalizer 작성 │
               └──────────────┬───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. ORCHESTRATION & VALIDATION (automation/build.py)          │
│    ├── Common Validation     : FORBIDDEN_DESIGN_KEYS 차단   │
│    ├── Slide Validator       : validate_slide_{id}() 검증   │
│    └── Slide Normalizer      : normalize_slide_{id}() 정규화│
└──────────────────────────────┬──────────────────────────────┘
                               │ Context
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. RENDERER ABSTRACTION (automation/render/)                │
│    ┌──────────────────────────────────────────────────┐     │
│    │ Renderer (Abstract Base Class)                   │     │
│    └────────────────────────┬─────────────────────────┘     │
│                             │ implements                    │
│    ┌────────────────────────▼─────────────────────────┐     │
│    │ JinjaRenderer (Jinja2 Implementation)            │     │
│    │  - Environment & FileSystemLoader                │     │
│    │  - autoescape=True (HTML/XML Safe)               │     │
│    │  - trim_blocks=True, lstrip_blocks=True          │     │
│    └──────────────────────────────────────────────────┘     │
└──────────────────────────────┬──────────────────────────────┘
                               │ Rendered String
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. GENERATED PRESENTATION SLIDES                            │
│    ├── Primary Target  : PRD-PO/html/분리된 html/*.html     │
│    └── Secondary Target: automation/dist/*.html             │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. VERIFICATION & REGRESSION (automation/tests/)            │
│    ├── test_parity.py  : StructureFingerprint.compare()     │
│    ├── test_build.py   : Renderer & Orchestration 검증      │
│    └── test_poc.py     : 런타임 계약 및 데이터 치환 회귀    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 프레임워크 계층과 Renderer 추상화

Jinja2는 자동화 프레임워크 자체의 추상화가 아니며, 프레임워크에 플러그인되는 **현재 선택된 렌더러 구현체**입니다.

```text
Automation Framework (Orchestration & Workflow)
      │
      ▼
Renderer (Abstract Interface: render(template, context, template_dir))
      │
      ▼
JinjaRenderer (Jinja2 Specific Adapter)
      │
      ▼
Jinja2 Library (Underlying Templating Engine)
```

### 계층별 책임 정의

| 계층 | 대상 모듈 | 역할 및 책임 |
|---|---|---|
| **Automation Framework** | `automation/build.py`<br>`automation/create_slide.py` | 슬라이드 생성 스캐폴딩, 전체 워크플로우 조율(Orchestration), 입출력 경로 계산 |
| **Analyzer Layer** | `automation/analyze/` | 원본 HTML DOM 트리 파싱, 텍스트 후보 탐지, 자산 의존성 추출, 구조 지문 생성 |
| **Validation Layer** | `automation/validate.py` | 디자인 키 유입 차단(`check_no_inline_design`), 슬라이드 스키마 무결성 검증, 상태 정규화 |
| **Renderer Interface** | `automation/render/renderer.py` | 템플릿 엔진 독립성을 보장하는 추상 기반 클래스 (`Renderer`) |
| **JinjaRenderer** | `automation/render/jinja_renderer.py` | Jinja2 환경 구성, 안전한 autoescape 설정, 템플릿 로딩 및 렌더링 에러(`RenderError`) 캡슐화 |
| **Visual Layer** | `PRD-PO/html/분리된 html/*.css` | 타이포그래피, 컬러, 그리드 레이아웃 (자동화에 맞추기 위한 CSS 수정 100% 금지) |
| **Runtime Script** | `PRD-PO/html/분리된 html/발표용_공통.js` | 슬라이드 전환, 네비게이션, 스피커 노트 토글 (불변 계약) |

---

## 4. Source of Truth (진실 소스) 및 인간 검토 원칙

```text
[Original HTML] ──> [Analyzer] ──> [Scaffold JSON & Template]
                                              │
                                              ▼
                                   [HUMAN REVIEW REQUIRED]
                                              │
                                              ▼
                              [Reviewed Data Model: slide_{id}.json] <=== Single Source of Truth
                                              │
                                              ▼
                                 [Generated Presentation HTML]       <=== Generated Artifact
```

> [!IMPORTANT]
> **자동 분석과 의미 확정은 엄격히 분리됩니다.**  
> `create_slide.py`는 원본 HTML을 파싱하여 텍스트 위치와 반복 노드를 탐지할 뿐, "98%"라는 텍스트를 보고 임의로 `"success_rate": "98%"`와 같이 도메인 필드명을 자동 확정하지 않습니다.  
> 인간 엔지니어가 스캐폴드를 검토하고 비즈니스 필드를 명명한 뒤에만 프로덕션 빌드로 승격됩니다.

---

## 5. CLI 명령어 명세

### 1) 슬라이드 스캐폴드 생성 (`create_slide.py`)
```bash

cd C:\Users\bluej\Desktop\my2\PR-1A1\automation

# 1. 8번 슬라이드 실제 빌드
& "C:\Users\bluej\AppData\Local\Programs\Python\Python312\python.exe" .\build.py --slide 008

# 2. 전체 Regression 테스트
& "C:\Users\bluej\AppData\Local\Programs\Python\Python312\python.exe" -m unittest discover .\tests -v

# 3. 008 전용 테스트
& "C:\Users\bluej\AppData\Local\Programs\Python\Python312\python.exe" -m unittest .\tests\test_slide_008.py -v

# 기본 사용법 (PRD-PO/html/분리된 html/{num}번 슬라이드.html 자동 탐색)
python automation/create_slide.py --slide 008

# 기존 파일이 존재할 때 강제 재생성
python automation/create_slide.py --slide 008 --force

# 원본 파일 경로 직접 지정
python automation/create_slide.py --input "path/to/source.html" --slide 008
```

### 2) 슬라이드 빌드 (`build.py`)
```bash
# 단일 슬라이드 빌드 (기본 경로 자동 매핑)
python automation/build.py --slide 004
python automation/build.py --slide 005
python automation/build.py --slide 006
python automation/build.py --slide 007

# 유효성 검증만 수행 (파일 쓰기 없음)
python automation/build.py --slide 006 --validate-only

# 커스텀 데이터 및 출력 경로 지정
python automation/build.py --slide 004 --data path/to/custom.json --output path/to/out.html
```

### 3) 단위 및 회귀 테스트 (`unittest`)
```bash
# 전체 테스트 실행 (32개 테스트)
python -m unittest discover automation/tests -v

# 개별 테스트 모듈 실행
python -m unittest automation/tests/test_build.py -v
python -m unittest automation/tests/test_parity.py -v
python -m unittest automation/tests/test_poc.py -v
```

> [!NOTE]
> `--all` (전체 일괄 빌드) 및 `--watch` 옵션은 현재 구현되어 있지 않으며, 향후 필요 시 추가 가능한 확장 항목입니다.

---

## 6. Dist 정책 명확화

- **Primary Output**: `PRD-PO/html/분리된 html/{num}번 슬라이드.html`  
  동일 디렉터리의 `{num}번 슬라이드.css`, `발표용_공통.css`, `발표용_공통.js`와 상대경로로 즉시 결합되어 완전한 브라우저 화면을 구성합니다.
- **Secondary Output (`automation/dist/`)**:  
  자동화 빌드 보조 산출물, 구조 핑거프린트 베이스라인(`baseline_slide_{id}.json`), 단위 테스트 임시 결과물이 격리되는 작업 공간입니다.  
  **`automation/dist/`는 독립 배포(Standalone Deployment) 번들이 아닙니다.**
