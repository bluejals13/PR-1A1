# PR-1A1 Presentation System & Input Package

본 디렉터리(`PRD-PO/presentation/`)는 `PR-Files/`에 축적된 검증된 엔지니어링 증거(Evidence)를 기반으로, **독립형 웹 슬라이드 제작 및 조립 런타임(Presentation System)**과 **Gemini Canvas / Google Slides 프레젠테이션 입력 패키지**를 통합 관리하는 공간입니다.

---

## 1. 핵심 아키텍처 원칙 (Core Principles)

> **"Slide = 독립적인 작은 Web Page"**

1. **Slide의 완전한 독립성:** 각 슬라이드는 독립된 디렉터리(`slides/001/`, `slides/002/`, ...) 내에서 `index.html`과 `style.css`를 소유하며, 브라우저에서 단독으로 열려도 정상 작동합니다.
2. **과도한 Component화 금지:** 모든 슬라이드에 획일적인 Layout을 강제하지 않습니다. 슬라이드마다 서로 다른 Layout, Grid, Diagram, Content Density를 가질 수 있습니다.
3. **최소한의 공통화 (Design System & Runtime Only):** 
   - `common/css/`: 16:9 Viewport, Reset, Variables (Color/Font), Typography, Base Utilities
   - `common/js/`: 네비게이션(키보드/버튼), 슬라이드 번호/프로그레스, 스피커 노트 동기화, 전체화면(F), 인쇄/내보내기
4. **Builder / Runtime의 명확한 책임 분리:**
   - Builder / Runtime은 슬라이드 발견, 순서 연결, 네비게이션, 공통 UI만 제공하며, 슬라이드 내부 레이아웃을 결정하지 않습니다.
5. **Evidence와 Slide의 분리:**
   - `PR-Files` = 엔지니어링 사실과 증거 (Source of Truth)
   - `PRD-PO/presentation` = 사실을 사람이 효과적으로 이해하도록 표현하는 결과물

---

## 2. 디렉터리 구조 (Directory Structure)

```text
PRD-PO/presentation/
├── README.md                          # [본 문서] 프레젠테이션 시스템 안내 및 가이드
├── manifest.json                      # 슬라이드 순서 및 등록 메타데이터
├── index.html                         # 프레젠테이션 진입점 (Launcher & Index)
│
├── common/                            # 공통 디자인 시스템 및 런타임
│   ├── css/
│   │   ├── reset.css                  # 기본 CSS 리셋
│   │   ├── variables.css              # 컬러 팔레트, 폰트, 16:9 뷰포트 토큰
│   │   ├── typography.css             # 타이포그래피, 코드, 태그 스타일
│   │   └── common.css                 # 뷰포트 셸, 네비게이션 바, 스피커 패널
│   ├── js/
│   │   ├── presentation.js            # 네비게이션, 키보드 단축키, 스피커 노트 런타임
│   │   └── export.js                  # PDF / 인쇄 내보내기 헬퍼
│   └── assets/                        # 공통 정적 에셋
│
├── slides/                            # 독립 슬라이드 제작 공간
│   ├── 001/                           # Slide 001: Project Identity & Architecture
│   │   ├── index.html
│   │   └── style.css
│   ├── 002/                           # Slide 002: Stateless Security Dilemma & Decision
│   │   ├── index.html
│   │   └── style.css
│   └── 003/                           # Slide 003: System & Container Topology
│       ├── index.html
│       └── style.css
│
├── source/                            # 15-Slide 팩트 데이터 마크다운 패키지 (Gemini Canvas용)
│   ├── 01_PROJECT_OVERVIEW.md
│   ├── 02_PROBLEM_AND_SOLUTION.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_AUTH_AND_RBAC.md
│   ├── 05_CORE_IMPLEMENTATION.md
│   ├── 06_SECURITY.md
│   ├── 07_TESTING.md
│   ├── 08_PERFORMANCE.md
│   ├── 09_TROUBLESHOOTING.md
│   ├── 10_AI_WORKFLOW.md
│   └── 11_LIMITATIONS_AND_ROADMAP.md
│
├── PRESENTATION_SPEC.md               # 15개 슬라이드 상세 설계 명세서 (Slide Blueprint)
├── GEMINI_CANVAS_PROMPT.md            # Gemini Canvas 실행용 완성형 표준 프롬프트
└── PORTFOLIO_PRESENTATION.md          # 검증 완료된 전체 발표 마스터 스크립트
```

---

## 3. 프레젠테이션 실행 및 조작 가이드

### 3.1 슬라이드 단독 실행 (Standalone Mode)
브라우저에서 임의의 슬라이드 파일을 직접 엽니다:
```text
PRD-PO/presentation/slides/001/index.html
PRD-PO/presentation/slides/002/index.html
PRD-PO/presentation/slides/003/index.html
```
각 슬라이드는 독립된 스타일과 레이아웃으로 즉시 렌더링되며, 하단 네비게이션 및 단축키를 통해 이전/다음 슬라이드로 부드럽게 이동합니다.

### 3.2 전체 프레젠테이션 실행 (Launcher Mode)
```text
PRD-PO/presentation/index.html
```
- 실행 시 등록된 첫 번째 슬라이드(`slides/001/index.html`)로 자동 연결되며, 슬라이드 바로가기 인덱스를 제공합니다.

### 3.3 키보드 조작 단축키 (Keyboard Shortcuts)
| 키 (Key) | 기능 (Action) |
| :--- | :--- |
| `←` / `PageUp` | 이전 슬라이드 이동 |
| `→` / `Space` / `PageDown` | 다음 슬라이드 이동 |
| `Home` | 첫 번째 슬라이드(`001`)로 이동 |
| `End` | 마지막 슬라이드로 이동 |
| `N` / `n` | 발표자 노트(Speaker Notes) 패널 열기 / 닫기 |
| `F` / `f` | 전체화면 모드(Fullscreen) 토글 |
| `ESC` | 발표자 노트 닫기 |

---

## 4. 슬라이드 등록 및 신규 추가 워크플로우

### 4.1 신규 슬라이드 추가 단계
1. `slides/` 하위에 3자리 번호 폴더 생성 (예: `slides/004/`)
2. `index.html`과 `style.css` 작성:
   - `<link rel="stylesheet" href="../../common/css/reset.css">`
   - `<link rel="stylesheet" href="../../common/css/variables.css">`
   - `<link rel="stylesheet" href="../../common/css/typography.css">`
   - `<link rel="stylesheet" href="../../common/css/common.css">`
   - `<link rel="stylesheet" href="style.css">`
   - `<body class="presentation-mode" data-slide="004" data-slide-index="4">`
   - 스크립트: `<script src="../../common/js/presentation.js"></script>`
3. `manifest.json`에 슬라이드 ID 등록:
```json
{
  "slides": [
    "001",
    "002",
    "003",
    "004"
  ]
}
```

---

## 5. 15-Slide 마스터 설계 체계 (Slide Blueprint)

| Slide | 슬라이드 제목 | 주요 주제 및 핵심 메시지 | 참조 Source 파일 | 상태 |
| :---: | :--- | :--- | :--- | :---: |
| **01** | **Project Identity & Architecture Overview** | 백엔드 설계부터 인프라, 부하 검증, AI 프로세스를 통합한 시스템 | `01_PROJECT_OVERVIEW.md` | `[IMPLEMENTED]`<br>`[VERIFIED]` |
| **02** | **Core Engineering Challenges & Objectives** | 무상태성을 유지하면서도 즉각적인 토큰 탈취 방어 및 포트 격리 달성 | `02_PROBLEM_AND_SOLUTION.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **03** | **System & Container Topology** | Nginx 단일 진입점(Port 80) 및 7개 도커 서비스 내부 브리지 네트워크 격리 | `03_ARCHITECTURE.md` | `[IMPLEMENTED]`<br>`[VERIFIED]` |
| **04** | **Backend Clean Architecture & DTO Isolation** | Java 17 불변 Record DTO를 통한 엔티티 캡슐화 및 통일된 ApiResponse | `05_CORE_IMPLEMENTATION.md` | `[IMPLEMENTED]`<br>`[DOCUMENTED]` |
| **05** | **Authentication Architecture (JWT & Lifecycles)** | Access Token(1시간, Header)과 Refresh Token(7일, HttpOnly Cookie) 전송 분리 | `04_AUTH_AND_RBAC.md` | `[IMPLEMENTED]`<br>`[VERIFIED]` |
| **06** | **Advanced Token Security (RTR & Redis Blacklist)** | 1회용 JTI 검증으로 재사용 공격 방어 및 잔여 TTL 블랙리스트 즉시 무효화 | `04_AUTH_AND_RBAC.md`<br>`06_SECURITY.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **07** | **Authorization & RBAC Multi-Tier Hierarchy** | User-Role-Permission M:N 정규화 모델 및 Spring Security 세부 인가 필터링 | `04_AUTH_AND_RBAC.md` | `[IMPLEMENTED]`<br>`[VERIFIED]` |
| **08** | **Database Schema & Migration Governance (Flyway)** | `ddl-auto: validate` 및 Flyway V1~V5 마이그레이션을 통한 스키마 형상 통제 | `05_CORE_IMPLEMENTATION.md` | `[IMPLEMENTED]`<br>`[VERIFIED]` |
| **09** | **Automated Security & Integration Verification** | 10종의 핵심 JUnit 자동화 단위/통합 테스트 스위트를 통한 보안 로직 무결성 검증 (100% Pass) | `07_TESTING.md`<br>`06_SECURITY.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **10** | **Performance Validation (k6 Benchmarks)** | k6 70 VU 동시 부하 실측 결과 (Avg 5.64ms, P95 9.98ms, 463 req/s, Error 0.00%) | `08_PERFORMANCE.md` | `[VERIFIED]` |
| **11** | **Real-World Incident Troubleshooting (TS 6-Step)** | TS 표준 6단계 프레임워크 기반 실측 장애 3건 (Redis, JWT Loop, Docker) 근본 원인 해결 | `09_TROUBLESHOOTING.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **12** | **Controlled AI Workflow (SA-1 Governance)** | AI를 맹목적으로 믿지 않고 엄격한 컨벤션과 테스트로 통제하는 8단계 라이프사이클 | `10_AI_WORKFLOW.md` | `[DOCUMENTED]`<br>`[VERIFIED]` |
| **13** | **Architectural Decisions & Technical Trade-offs** | 무상태성 vs 세션 제어, Redis 외부 의존성 결합 vs 시스템 복원력 최적점 도출 | `04_AUTH_AND_RBAC.md`<br>`09_TROUBLESHOOTING.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **14** | **System Limitations & Future Roadmap (PLANNED)** | 현재 시스템 한계 인정 및 사실과 계획을 엄격히 분리한 `[PLANNED]` 로드맵 | `11_LIMITATIONS_AND_ROADMAP.md` | `[PLANNED]`<br>`[DOCUMENTED]` |
| **15** | **Conclusion & Engineering Identity** | 원리를 이해하고, 인프라에서 실행하며, 검증과 장애 분석으로 증명하는 엔지니어 | `01_PROJECT_OVERVIEW.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |

---

## 6. Source of Truth & Zero-Hallucination 거버넌스 정책

1. **5대 상태 태그 체계:** `[VERIFIED]`, `[IMPLEMENTED]`, `[DOCUMENTED]`, `[PLANNED]`, `[UNKNOWN]`
2. **성능 실측 불변치 (Strict Performance Facts):**
   - `70 VUs`, `1 minute (60s)`, Throughput `463 req/s`, Latency Avg `5.64 ms`, P95 `9.98 ms`, Error Rate `0.00%`
3. **금지 표현 방지:** "완벽한 보안", "무한 확장" 등의 과장 표현을 엄금하고 실측된 사실과 격리된 로드맵(`[PLANNED]`)으로만 서술.
