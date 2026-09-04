# Slide Automation Step-by-Step Guide

본 가이드는 새로운 HTML 슬라이드를 **분석(Analyze) ➔ 스캐폴딩(Scaffold) ➔ 사람 검토(Human Review) ➔ 유효성 검증(Validate) ➔ 렌더러(Renderer) ➔ 패리티 검증(Parity)** 절차를 거쳐 자동화 파이프라인에 통합하는 표준 작업 절차서입니다.

---

## 0. 핵심 시스템 원칙 및 아키텍처 경계

새로운 슬라이드 자동화 작업 시 아래 원칙을 반드시 준수해야 합니다.

1. **자동 분석과 의미 확정의 분리 (Human Review Required)**:
   `create_slide.py`는 원본 HTML DOM을 파싱하여 텍스트 위치와 반복 노드를 탐지할 뿐, 임의로 도메인 필드명을 확정하거나 비즈니스 의미를 추측하지 않습니다. 사람이 스캐폴드를 검토하고 필드를 명명해야 합니다.
2. **Renderer 추상화 계층 분리**:
   자동화 프레임워크(`build.py`)는 특정 템플릿 라이브러리에 직접 의존하지 않고 `Renderer` 추상 인터페이스(`render/renderer.py`)를 통해 `JinjaRenderer`를 호출합니다.
3. **CLI 중심 독립 실행 (AI Agent는 Optional)**:
   모든 자동화 작업(스캐폴드 생성, 빌드, 패리티 검증, 회귀 테스트)은 외부 AI API 없이 순수 Python CLI 명령어로 즉시 실행 가능해야 합니다. AI Agent는 필요 시 보조 도구로만 활용합니다.
4. **CSS / JS 불변 원칙 (기준선 보존)**:
   기존 `PRD-PO/html/분리된 html/*.css` 및 `발표용_공통.js`는 완전한 기준선으로 취급하며, 자동화를 이유로 단 한 줄도 수정하지 않습니다. HTML 템플릿이 기존 CSS/JS 구조를 100% 따릅니다.
5. **1 Slide = 1 Independent Template**:
   슬라이드 간 시각적·구조적 목적이 상이하므로 공통 베이스 템플릿(`UniversalSlide`, `BaseSlide`)을 만들지 않고, 각 슬라이드마다 독립 템플릿(`slide_{id}.html.j2`)을 유지합니다.
6. **`automation/dist/` 정책**:
   `dist/` 디렉터리는 빌드 보조 산출물, 구조 지문 베이스라인(`baseline_slide_{id}.json`), 테스트 임시 아티팩트 작업 공간입니다. CSS/JS 에셋이 포함되지 않으므로 **Standalone 프레젠테이션 배포 번들이 아닙니다.**

---

## 1. 실제 사용자 작업 흐름 (CLI Workflow)

```bash
# 1단계: 원본 HTML 분석 및 스캐폴드 자동 생성
python automation/create_slide.py --slide 008

# 2단계: 사람이 직접 검토 및 도메인 모델 확정 (Human Review)
#   - automation/data/slide_008.json 편집 (필드명 정의)
#   - automation/templates/slide_008.html.j2 편집 (변수 바인딩)
#   - automation/validate.py 편집 (validate_slide_008, normalize_slide_008 작성)

# 3단계: 슬라이드 빌드 실행
python automation/build.py --slide 008

# 4단계: DOM Parity 및 전체 회귀 테스트 실행
python -m unittest discover automation/tests -v
```

---

## 2. 16단계 표준 작업 절차 (Standard Procedure)

```text
[1. 원본 HTML 읽기] ──> [2. 원본 CSS 읽기] ──> [3. 공통 JS 읽기] ──> [4. DOM 트리 분석]
                                                                            │
┌───────────────────────────────────────────────────────────────────────────┘
▼
[5. Content 후보 탐색] ─> [6. JSON 스캐폴드] ─> [7. Validator 작성] ─> [8. Normalizer 작성]
                                                                                │
┌───────────────────────────────────────────────────────────────────────────────┘
▼
[9. Template 바인딩] ─> [10. Renderer 빌드] ─> [11. DOM Parity 검증] ─> [12. ID Parity 검증]
                                                                                │
┌───────────────────────────────────────────────────────────────────────────────┘
▼
[13. data-* Parity] ──> [14. CSS/JS 의존성] ──> [15. Data 치환 테스트] ─> [16. Regression]
```

### 단계별 상세 가이드

1. **원본 HTML 읽기**: `PRD-PO/html/분리된 html/{num}번 슬라이드.html`을 읽고 슬라이드 목적과 블록 구성을 파악합니다.
2. **원본 CSS 읽기**: `{num}번 슬라이드.css`, `발표용_공통.css`에서 클래스명 및 레이아웃을 확인합니다. (CSS 수정 절대 금지)
3. **공통 JS 읽기**: `발표용_공통.js`의 런타임 이벤트 대상 ID 및 `data-slide` 계약을 확인합니다.
4. **DOM 구조 분석**: `python automation/create_slide.py --slide {id}`를 실행하여 `HTMLAnalyzer`로 태그 계층과 깊이를 자동 분석합니다.
5. **Content 영역 식별**: `ContentDetector`가 추출한 텍스트 후보 및 반복 구조를 검토하여 정적 장식 태그와 동적 데이터를 분리합니다.
6. **JSON 데이터 모델 확정**: `automation/data/slide_{id}.json`에서 임시 `content_candidates`를 실제 도메인 키(`title`, `items`, `metrics`, `status` 등)로 명명합니다. (인라인 스타일 및 디자인 키 금지)
7. **Validator 작성**: `automation/validate.py`에 `validate_slide_{id}()` 함수를 추가하고 필수 키, 배열 무결성, 허용 상태값을 검증합니다.
8. **Normalizer 작성**: `automation/validate.py`에 `normalize_slide_{id}()` 함수를 추가하고 상태값을 CSS 클래스로 매핑한 뒤 디스패처에 등록합니다.
9. **Jinja2 Template 작성**: `automation/templates/slide_{id}.html.j2`에 도메인 변수를 바인딩합니다. 원본의 DOM 계층과 클래스는 100% 유지합니다.
10. **Build 실행**: `python automation/build.py --slide {id}`를 실행하여 `JinjaRenderer`를 통해 HTML을 생성합니다.
11. **DOM Parity 검증**: `StructureFingerprint.compare()` 또는 육안 검사를 통해 원본 대비 누락된 클래스나 태그가 없는지 확인합니다.
12. **ID Parity 검증**: 런타임 필수 ID(`slide-{id}`, `presentation-viewport`, `speaker-panel` 등)가 온전히 유지되었는지 확인합니다.
13. **data-* Parity 검증**: `data-slide="{num}"`과 `data-speaker-note`가 정상 주입되었는지 확인합니다.
14. **CSS/JS Dependency 검증**: `{num}번 슬라이드.css`와 `발표용_공통.js` 상대경로가 온전히 연결되었는지 확인합니다.
15. **Data Replacement 테스트**: 텍스트나 상태값을 변경한 임시 데이터로 빌드하여 템플릿 수정 없이 동적으로 렌더링되는지 확인합니다.
16. **Regression Test**: `python -m unittest discover automation/tests -v`를 실행하여 기존 슬라이드(04~07)와 신규 슬라이드 테스트가 모두 통과하는지 확인합니다.

---

## 3. 실제 Template 변환 사례 (3 Case Studies)

### Example A. Slide 04 — Threat Matrix (테이블/매트릭스 구조)

```html
<!-- 원본 HTML -->
<tr class="row-warning">
  <td>
    <div class="threat-name threat-medium">
      <span class="threat-dot"></span> BOLA <small>IDOR</small>
    </div>
  </td>
  <td><span class="scenario-text">타인의 Resource ID 변조 접근</span></td>
  <td>
    <div class="control-name">
      <strong>Object-Level Authorization</strong>
      <span>Resource Ownership 검증</span>
    </div>
  </td>
  <td class="status-cell">
    <div class="security-status-group">
      <span class="security-status implemented"><span class="status-dot"></span> IMPLEMENTED </span>
      <span class="security-status verify-required"><span class="status-dot"></span> VERIFY REQUIRED </span>
    </div>
  </td>
</tr>

<!-- slide_004.html.j2 -->
{% for item in items %}
<tr{% if item.is_warning %} class="row-warning"{% endif %}>
  <td>
    <div class="threat-name {{ item.threat_class }}">
      <span class="threat-dot"></span> {{ item.threat }}
      {% if item.threat_sub %}<small>{{ item.threat_sub }}</small>{% endif %}
    </div>
  </td>
  <td><span class="scenario-text">{{ item.scenario }}</span></td>
  <td>
    <div class="control-name">
      <strong>{{ item.control_strong }}</strong>
      <span>{{ item.control_desc }}</span>
    </div>
  </td>
  <td class="status-cell">
    <div class="security-status-group">
      {% for st in item.statuses %}
      <span class="security-status {{ st.statusClass }}">
        <span class="status-dot"></span> {{ st.status }}
      </span>
      {% endfor %}
    </div>
  </td>
</tr>
{% endfor %}
```
- **설계 포인트**: 장식 요소(`threat-dot`, `security-status-group`)는 템플릿에 두고 텍스트와 상태 라벨만 JSON으로 추출. 상태 스타일(`st.statusClass`)은 Normalizer에서 계산하여 주입.

---

### Example B. Slide 05 — Security Flow (트랙 그리드 구조)

```html
<!-- 원본 HTML -->
<article class="flow-card flow-replay">
  <header class="flow-card-header">
    <div>
      <span class="flow-kicker">02 / ATTACK</span>
      <h3>Refresh Replay</h3>
    </div>
    <span class="flow-badge danger">BLOCK</span>
  </header>
  <div class="flow-track">
    <div class="flow-step">
      <span class="step-index">01</span>
      <div><strong>Refresh Token 탈취</strong><small>공격자가 Token 확보</small></div>
    </div>
    <div class="flow-connector"></div>
    <div class="flow-control danger">
      <span class="control-label">REPLAY DETECTION</span>
      <strong>JTI 이미 사용됨?</strong>
      <small>RTR + JTI 상태 확인</small>
    </div>
  </div>
</article>

<!-- slide_005.html.j2 -->
{% for flow in flows %}
<article class="flow-card {{ flow.card_class }}">
  <header class="flow-card-header">
    <div>
      <span class="flow-kicker">{{ flow.kicker }}</span>
      <h3>{{ flow.title }}</h3>
    </div>
    <span class="flow-badge {{ flow.badge.class }}">{{ flow.badge.text }}</span>
  </header>
  <div class="flow-track">
    {% for node in flow.nodes %}
      {% if not loop.first %}<div class="flow-connector"></div>{% endif %}
      {% if node.type == 'step' %}
        <div class="flow-step">
          <span class="step-index">{{ node.index }}</span>
          <div><strong>{{ node.strong }}</strong><small>{{ node.small }}</small></div>
        </div>
      {% elif node.type == 'control' %}
        <div class="flow-control{% if node.control_class %} {{ node.control_class }}{% endif %}">
          <span class="control-label">{{ node.label }}</span>
          <strong>{{ node.strong }}</strong>
          <small>{{ node.small }}</small>
        </div>
      {% endif %}
    {% endfor %}
  </div>
</article>
{% endfor %}
```
- **설계 포인트**: `step`, `control`, `decision`, `result`의 다형성 노드를 `node.type` 분기로 안전하게 렌더링.

---

### Example C. Slide 06 — Evidence & Metrics (검증 매트릭스 및 부하 테스트)

```html
<!-- 원본 HTML -->
<tr class="status-pass">
  <td class="test-id">SEC-01</td>
  <td><strong>만료된 Access Token 사용</strong><small>Expired JWT</small></td>
  <td class="result-code">401</td>
  <td class="result-code actual">401</td>
  <td><span class="status-badge pass"><i></i> PASS</span></td>
</tr>

<!-- slide_006.html.j2 -->
{% for tc in evidence.test_cases %}
<tr class="{{ tc.row_class }}">
  <td class="test-id">{{ tc.id }}</td>
  <td><strong>{{ tc.scenario }}</strong><small>{{ tc.scenario_sub }}</small></td>
  <td class="result-code">{{ tc.expected }}</td>
  <td class="result-code {{ tc.actual_class }}">{{ tc.actual }}</td>
  <td><span class="status-badge {{ tc.badge_class }}"><i></i> {{ tc.badge_text }}</span></td>
</tr>
{% endfor %}
```
- **설계 포인트**: JSON에는 `"status": "PASS"`만 저장되고, Normalizer가 `row_class="status-pass"`, `badge_class="pass"`로 변환. 증거가 없는 SEC-05, SEC-06은 `PENDING`/`N/A`로 엄격히 보존.

---

## 4. 작업 명령서 및 체크리스트

AI Agent 또는 엔지니어가 신규 슬라이드 작업을 수행할 때 사용하는 체크리스트입니다. (AI 사용은 Optional)

```text
[NEW SLIDE AUTOMATION CHECKLIST]

[ ] 1. 원본 HTML 분석 (`create_slide.py --slide {id}`)
[ ] 2. 원본 CSS 분석 (`{num}번 슬라이드.css`, `발표용_공통.css`)
[ ] 3. 공통 JS 분석 (`발표용_공통.js`)
[ ] 4. DOM 트리 및 구조 지문 베이스라인 확인
[ ] 5. Content 후보 검토 및 정적/동적 영역 분리
[ ] 6. JSON 데이터 모델 명명 및 확정 (`slide_{id}.json`)
[ ] 7. Validator 작성 (`automation/validate.py` 내 `validate_slide_{id}`)
[ ] 8. Normalizer 작성 (`automation/validate.py` 내 `normalize_slide_{id}`)
[ ] 9. Dispatcher 등록 (`VALIDATORS`, `NORMALIZERS` 딕셔너리)
[ ] 10. 독립 Jinja2 템플릿 변수 바인딩 (`slide_{id}.html.j2`)
[ ] 11. 빌드 실행 (`python automation/build.py --slide {id}`)
[ ] 12. 생성 HTML DOM 구조 및 육안 확인
[ ] 13. CSS Class Parity 검증
[ ] 14. ID Parity 검증 (런타임 필수 ID 포함)
[ ] 15. data-* Attribute Parity 검증 (`data-slide`, `data-speaker-note`)
[ ] 16. CSS / JS 상대경로 의존성 검증
[ ] 17. Data 치환 및 상태 동적 반영 단위 테스트 작성
[ ] 18. 전체 테스트 통과 확인 (`python -m unittest discover automation/tests -v`)
[ ] 19. Git diff 확인 (CSS/JS 등 보호 대상 파일 변경 여부 무결성 확인)
```

### 3대 작업 원칙
1. **"기존 CSS를 수정해서 맞추지 말고, HTML template을 원본 DOM에 맞춰라."**  
   자동화 파이프라인 편의를 위해 기존 CSS 셀렉터나 스타일 규칙을 변경하는 것은 엄격히 금지됩니다.
2. **"증거가 없는 상태를 VERIFIED로 만들지 마라."**  
   자동화 과정에서 임의로 PENDING, VERIFY REQUIRED 상태를 VERIFIED나 PASS로 변경해서는 안 됩니다.
3. **"슬라이드 간 디자인 통일을 이유로 Universal Template을 만들지 마라."**  
   1 Slide = 1 Independent Template 원칙을 준수하고, 템플릿 간 결합도를 0으로 유지하십시오.
