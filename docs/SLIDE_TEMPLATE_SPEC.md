# Slide Template Specification

## 1. 핵심 설계 원칙 (Core Principles)

### 1 Slide = 1 Independent Template
각 슬라이드는 반드시 **독립된 전용 Jinja2 템플릿 파일**(`automation/templates/slide_{id}.html.j2`)로 관리되어야 합니다.

```text
[ALLOWED]
├── automation/templates/slide_004.html.j2
├── automation/templates/slide_005.html.j2
├── automation/templates/slide_006.html.j2
└── automation/templates/slide_007.html.j2

[FORBIDDEN]
├── UniversalSlide.html.j2
├── BaseSlide.html.j2
├── GenericSlide.html.j2
└── UniversalTemplate.j2
```

### 계층별 역할 분담 (Layer Responsibilities)
- **JSON**: 순수 데이터 및 의미론적 상태 정의 (디자인 속성 완전 배제)
- **Python**: 입력 데이터 유효성 검증(Validate), 정규화(Normalize), 빌드 오케스트레이션(Build Orchestration)
- **Jinja2**: HTML DOM 구조 렌더링 (비즈니스 로직 및 스타일 연산 금지)
- **CSS**: 시각적 디자인, 타이포그래피, 반응형 레이아웃 (자동화를 위한 변경 절대 금지)
- **JS**: 브라우저 발표 런타임 네비게이션, 스피커 노트 토글 (불변 계약)

### 왜 공통 베이스 템플릿(BaseSlide)을 만들지 않는가?
1. **슬라이드별 고유 레이아웃 보존**: Slide 04는 Threat Matrix(테이블), Slide 05는 Response Flow(트랙 그리드), Slide 06은 Evidence Table 및 Load Test 메트릭, Slide 07은 Incident Case 및 Residual Risk 패널입니다. 각 슬라이드의 시각적·구조적 목적이 완전히 상이합니다.
2. **과도한 템플릿 복잡도 방지**: 범용 템플릿을 도입할 경우, 수십 개의 `{% if slide_type == 'table' %}` 같은 복잡한 조건 분기가 Jinja2 안으로 들어가게 되어 템플릿의 가독성과 유지보수성이 급격히 저하됩니다.
3. **디자인 및 DOM 회귀(Regression) 격리**: 한 슬라이드의 템플릿을 수정할 때 다른 슬라이드에 예기치 않은 부작용(Side Effect)이 전파되는 것을 원천 차단합니다.

---

## 2. Jinja2 템플릿 작성 규칙

Jinja2는 오직 **데이터를 받아 HTML DOM으로 렌더링하는 역할**만 수행합니다.

### 허용되는 패턴 (Allowed)
- 변수 치환: `{{ item.title }}`, `{{ slide_meta.slide_num }}`
- 단순 컬렉션 순회: `{% for item in items %} ... {% endfor %}`
- 존재 여부에 따른 조건부 DOM 노출: `{% if item.has_impact %} ... {% endif %}`
- 루프 인덱스 보조: `{% if not loop.first %}<b>→</b>{% endif %}`

### 엄격히 금지되는 패턴 (Forbidden)
- **비즈니스 로직 및 상태 연산**: 템플릿 안에서 점수, 합계, 판정 결과를 직접 계산하는 행위 금지 (모두 Python `validate.py`의 Normalizer에서 계산 완료 후 주입).
- **상태의 임의 승격**: 증거가 없는 항목을 `{% if ... %} VERIFIED {% endif %}`로 변환하는 행위 금지.
- **인라인 스타일(Inline Style) 삽입**: `<div style="color: red; margin: 10px;">` 같은 인라인 스타일 작성 금지.
- **동적 CSS 클래스 조립**: 템플릿 내부에서 문자열 연산으로 복잡한 클래스를 조합하지 말고, Normalizer가 제공하는 정규화된 클래스명을 그대로 바인딩.

---

## 3. 프레젠테이션 런타임 DOM 계약 (Runtime Contract)

모든 슬라이드 템플릿은 `PRD-PO/html/분리된 html/발표용_공통.js` 및 `발표용_공통.css`와의 상호작용을 위해 다음 런타임 DOM 규격을 반드시 준수해야 합니다.

### 필수 태그 및 속성 구조
```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APMS.SR - Slide {id}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{num}번 슬라이드.css">
  <link rel="stylesheet" href="발표용_공통.css">
</head>
<body class="presentation-mode" data-slide="{num}">

  <!-- 1. 프로그레스 바 -->
  <div id="presentation-progress"></div>

  <!-- 2. 메인 뷰포트 -->
  <main id="presentation-viewport">
    <section class="slide slide-{id}" id="slide-{id}"{% if speaker_note %} data-speaker-note="{{ speaker_note }}"{% endif %}>
      <!-- 슬라이드 고유 DOM 구조 -->
    </section>
  </main>

  <!-- 3. 발표자 노트 패널 (고정 ID) -->
  <div id="speaker-panel">
    <div class="speaker-head">
      <span>Speaker Notes</span>
      <button id="speaker-close" aria-label="발표 노트 닫기">✕</button>
    </div>
    <div id="speaker-text"></div>
  </div>

  <!-- 4. 프레젠테이션 네비게이션 (고정 ID) -->
  <nav id="presentation-nav" aria-label="발표 네비게이션">
    <div class="presentation-nav-left">
      <span class="presentation-brand">{{ nav.brand }}</span>
      <span class="presentation-hint">{{ nav.hint }}</span>
    </div>

    <div class="presentation-nav-right">
      <button class="presentation-btn" id="prev-btn" aria-label="이전 슬라이드">‹</button>
      <span id="presentation-counter">{{ nav.counter }}</span>
      <button class="presentation-btn" id="next-btn" aria-label="다음 슬라이드">›</button>
      <button id="speaker-toggle">SPEAKER</button>
    </div>
  </nav>

  <!-- 5. 런타임 스크립트 상대경로 링크 -->
  <script src="{{ nav.runtime_script }}"></script>
</body>
</html>
```

### 필수 ID 목록 (ID Parity Check Targets)
| ID | 요소 설명 | 런타임 바인딩 동작 (`발표용_공통.js`) |
|---|---|---|
| `presentation-progress` | 상단 진행 상태 바 | 슬라이드 진행률 너비(`width: %`) 갱신 |
| `presentation-viewport` | 슬라이드 메인 컨테이너 | 뷰포트 높이 및 반응형 제어 |
| `slide-{id}` | 개별 슬라이드 섹션 | `data-speaker-note` 추출 |
| `speaker-panel` | 발표자 노트 팝업 | 토글 시 `.visible` 클래스 추가/제거 |
| `speaker-close` | 발표자 노트 닫기 버튼 | 클릭 시 패널 닫기 |
| `speaker-text` | 발표자 노트 텍스트 컨테이너 | 현재 슬라이드의 발표 노트 텍스트 주입 |
| `speaker-toggle` | 네비게이션 내 SPEAKER 버튼 | 클릭 시 발표자 노트 토글 |
| `presentation-nav` | 하단 네비게이션 바 | 전체 네비게이션 영역 |
| `prev-btn` | 이전 슬라이드 버튼 | 클릭 시 이전 슬라이드 HTML로 이동, 1번 슬라이드 시 `disabled` |
| `next-btn` | 다음 슬라이드 버튼 | 클릭 시 다음 슬라이드 HTML로 이동, 마지막 슬라이드 시 `disabled` |
| `presentation-counter` | 슬라이드 번호 카운터 | `currentSlide / totalSlides` 텍스트 주입 |

---

## 4. DOM Parity 및 Class 일치성 표준

템플릿 변환 시 원본 수작업 HTML과의 **완전한 계층 및 클래스 일치성(1:1 Parity)**을 유지해야 합니다.

1. **태그 계층 보존**:
   - 원본 HTML에서 `<section>` > `<header>` > `<div>` 구조였다면 템플릿에서도 동일한 깊이와 태그 종류를 유지합니다. 불필요한 래퍼 `<div>`를 임의로 추가하거나 제거하지 마십시오.
2. **시각적 상태 클래스 분리**:
   - 상태에 따른 스타일링 클래스(예: `resolved`, `verify`, `risk-done`, `risk-critical`, `p0`, `p1`, `status-pass`, `status-pending`)는 반드시 Python Normalizer가 정규화한 변수를 통해 렌더링합니다.
3. **접근성(A11y) 속성 보존**:
   - `aria-label`, `role` 등 원본에 있던 접근성 관련 속성을 빠짐없이 유지합니다.
