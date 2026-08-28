# Presentation Input Package for Gemini Canvas & Google Slides

본 디렉터리(`PRD-PO/presentation/`)는 `PR-Files/`에 축적된 검증된 엔지니어링 사실(Evidence)을 기반으로, **Gemini Canvas 또는 Google Slides에서 고품질의 15페이지 기술 발표자료를 생성하기 위한 프레젠테이션 입력 패키지(Presentation Input Package)**입니다.

---

## 1. 목적 (Purpose)

- **검증된 사실 기반 발표자료 생성:** 면접관과 평가자가 직관적으로 이해할 수 있는 15페이지 분량의 기술 발표 슬라이드 및 발표 대본(Speaker Notes) 생성.
- **AI 환각(Hallucination) 원천 차단:** 사전에 검증된 사실 데이터(`source/`)와 설계 명세(`PRESENTATION_SPEC.md`)만을 AI 모델에 제공하여, 존재하지 않는 기능이나 수치가 생성되는 것을 원천 차단.
- **Google Slides / PDF 호환성:** 생성된 결과를 Google Slides나 PDF로 즉시 변환하여 활용할 수 있는 표준화된 구조 제공.

---

## 2. 디렉터리 구조 및 파일별 역할

```
PRD-PO/presentation/
├── README.md                          # [본 문서] 사용 가이드 및 거버넌스 정책
├── PRESENTATION_SPEC.md               # 15개 슬라이드 상세 설계 명세서 (Slide Plan & Visuals)
├── GEMINI_CANVAS_PROMPT.md            # Gemini Canvas 실행용 완성형 표준 프롬프트
├── PORTFOLIO_PRESENTATION.md          # 검증 완료된 전체 발표자료 마스터 스크립트
└── source/                            # Gemini Canvas 첨부용 정제 사실 데이터 패키지
    ├── 01_PROJECT_OVERVIEW.md         # 프로젝트 정체성, 4대 핵심 축, 엔지니어링 포지셔닝
    ├── 02_PROBLEM_AND_SOLUTION.md     # 직면 과제(JWT 한계, 포트 노출) 및 기술적 해결책
    ├── 03_ARCHITECTURE.md             # Nginx Gateway & 7개 Docker 서비스 토폴로지
    ├── 04_AUTH_AND_RBAC.md            # JWT, RTR, Blacklist, M:N RBAC 인가 모델
    ├── 05_CORE_IMPLEMENTATION.md      # 불변 Record DTO, ApiResponse, Flyway V1~V5
    ├── 06_SECURITY.md                 # XSS 방어, Replay Attack 방어, 보안 필터 체인
    ├── 07_TESTING.md                  # 10종 JUnit 자동화 단위/통합 테스트 스위트
    ├── 08_PERFORMANCE.md              # k6 70 VU 부하 테스트 실측치 (Avg 5.64ms, 0% Error)
    ├── 09_TROUBLESHOOTING.md          # TS 표준 6단계 실측 장애 3건 (Redis, JWT Loop, Docker)
    ├── 10_AI_WORKFLOW.md              # SA-1 8단계 AI 라이프사이클 및 거버넌스 규칙
    └── 11_LIMITATIONS_AND_ROADMAP.md  # 현재 시스템 한계 및 [PLANNED] 로드맵 과제
```

### 주요 구성요소 상세

| 파일 / 디렉터리 | 담당 역할 | 주요 내용 및 특징 |
| :--- | :--- | :--- |
| **`source/`** | 사실 데이터 패키지<br>(Fact Base) | 각 문서는 `What`, `Why`, `How`, `Evidence`, `Result`, `Status`, `Source`, `Presentation Use`의 표준 구조를 준수하여 발표자료 제작에 필요한 정보만 압축 제공. |
| **`PRESENTATION_SPEC.md`** | 슬라이드 설계 명세서<br>(Slide Blueprint) | 1번부터 15번까지의 목적(Purpose), 핵심 메시지(Key Message), 필수 인용 수치(Metrics), 시각화 권장사항(Visual Recommendation), 발표자 의도(Speaker Intent) 정의. |
| **`GEMINI_CANVAS_PROMPT.md`** | AI 실행 프롬프트<br>(Execution Command) | Gemini Canvas에 복사하여 붙여넣기만 하면 첨부된 `source/` 파일들을 기반으로 Google Slides 호환 발표자료를 생성하는 완성형 프롬프트. |
| **`PORTFOLIO_PRESENTATION.md`** | 발표 마스터 원고<br>(Master Script) | 15개 슬라이드 전체의 완성된 본문, 다이어그램 구조 및 구술 발표 스크립트(Speaker Note) 보관. |

---

## 3. 15-Slide 목차 체계 및 매핑 (Slide Blueprint)

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
| **09** | **Automated Security & Integration Verification** | 10종의 핵심 JUnit 단위/통합 테스트 스위트를 통한 보안 로직 무결성 검증 (100% Pass) | `07_TESTING.md`<br>`06_SECURITY.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **10** | **Performance Validation (k6 Benchmarks)** | k6 70 VU 동시 부하 실측 결과 (Avg 5.64ms, P95 9.98ms, 463 req/s, Error 0.00%) | `08_PERFORMANCE.md` | `[VERIFIED]` |
| **11** | **Real-World Incident Troubleshooting (TS 6-Step)** | TS 표준 6단계 프레임워크 기반 실측 장애 3건 (Redis, JWT Loop, Docker) 완벽 해결 | `09_TROUBLESHOOTING.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **12** | **Controlled AI Workflow (SA-1 Governance)** | AI를 맹목적으로 믿지 않고 엄격한 컨벤션과 테스트로 통제하는 8단계 라이프사이클 | `10_AI_WORKFLOW.md` | `[DOCUMENTED]`<br>`[VERIFIED]` |
| **13** | **Architectural Decisions & Technical Trade-offs** | 무상태성 vs 세션 제어, Redis 외부 의존성 결합 vs 시스템 복원력 최적점 도출 | `04_AUTH_AND_RBAC.md`<br>`09_TROUBLESHOOTING.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |
| **14** | **System Limitations & Future Roadmap (PLANNED)** | 현재 시스템 한계 인정 및 사실과 계획을 엄격히 분리한 `[PLANNED]` 로드맵 | `11_LIMITATIONS_AND_ROADMAP.md` | `[PLANNED]`<br>`[DOCUMENTED]` |
| **15** | **Conclusion & Engineering Identity** | 원리를 이해하고, 인프라에서 실행하며, 검증과 장애 분석으로 증명하는 엔지니어 | `01_PROJECT_OVERVIEW.md` | `[VERIFIED]`<br>`[DOCUMENTED]` |

---

## 4. Gemini Canvas 실행 가이드 (Step-by-Step Guide)

```text
[Step 1] Gemini Canvas 접속
   └─ Gemini 웹 인터페이스에서 Canvas 모드를 선택합니다.

[Step 2] Source 파일 첨부 (Attach Files)
   └─ PRD-PO/presentation/source/ 하위 11개 마크다운 파일 전체와
      PRD-PO/presentation/PRESENTATION_SPEC.md를 업로드합니다.

[Step 3] 프롬프트 실행
   └─ PRD-PO/presentation/GEMINI_CANVAS_PROMPT.md의 프롬프트 전문을
      복사하여 대화창에 입력하고 실행합니다.

[Step 4] 산출물 검토 및 내보내기
   └─ 생성된 슬라이드 레이아웃과 Speaker Notes를 검토한 후
      Google Slides 또는 PDF로 내보내어 발표를 준비합니다.
```

---

## 5. Source of Truth & Zero-Hallucination 거버넌스 정책

본 패키지를 활용하거나 수정할 때는 다음 거버넌스 정책을 엄격히 준수해야 합니다.

### 5.1 5대 상태 태그 체계 (Status Classification)
- `[VERIFIED]`: 자동화 테스트(JUnit)나 부하 테스트(k6), 실행 로그로 수치와 동작이 검증 완료된 상태.
- `[IMPLEMENTED]`: 코드가 실제로 작성되어 저장소에 존재하나 별도 실측 수치는 없는 상태.
- `[DOCUMENTED]`: 아키텍처, 설계 컨벤션, 장애 보고서 등 공식 기술 문서에 명시된 상태.
- `[PLANNED]`: 향후 개선 예정으로 계획된 상태 (Roadmap). 절대 구현 완료로 표현 금지.
- `[UNKNOWN]`: 소스 코드 및 문서에서 확인되지 않은 상태 (인용 절대 불가).

### 5.2 성능 실측 불변치 (Strict Performance Facts)
k6 부하 테스트 지표는 아래 실측 사실 데이터만 사용하며 임의로 수정하거나 추측하지 않습니다:
- **Virtual Users:** `70 VUs`
- **Duration:** `1 minute (60s)` 지속 부하 (3회 반복 산술 평균)
- **Throughput:** `463 req/s`
- **Average Latency:** `5.64 ms`
- **P95 Latency:** `9.98 ms` (`p(95) < 50ms` 임계치 통과)
- **Error Rate:** `0.00%` (총 0건 에러, `rate < 1%` 임계치 통과)

### 5.3 금지 표현 vs 권장 표현 정책
| 구분 | 절대 금지 표현 (Banned) | 권장 표현 (Allowed & Recommended) |
| :--- | :--- | :--- |
| **보안** | "완벽한 보안", "무결점 시스템", "해킹 불가능" | "토큰 탈취 방어", "다계층 인가 필터링", "즉시 세션 무효화" |
| **성능** | "업계 최고 성능", "초고속 처리", "SLA 100% 보장" | "70 VU 부하 조건에서 평균 5.64ms 실측 검증 완료" |
| **확장성** | "무한 확장 가능", "대규모 트래픽 완벽 처리" | "컨테이너 격리 구조 수립", "다중 노드 스케일아웃은 [PLANNED] 과제" |
| **구현 범위** | 미구현 기능을 구현된 것처럼 작성 | "현재 구현 범위", "향후 개선 로드맵 (`[PLANNED]`)" |

---

## 6. 자료 업데이트 및 유지보수 워크플로우

1. **새로운 구현 또는 테스트 발생 시:**
   - `26-05adf` 또는 `SA-1`의 변경 사항을 먼저 `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`에 반영합니다.
2. **`source/` 데이터 동기화:**
   - 갱신된 사실에 따라 `PRD-PO/presentation/source/` 내 해당 도메인 문서를 업데이트합니다.
3. **명세서 동기화:**
   - 슬라이드 구성이나 수치 변경 시 `PRESENTATION_SPEC.md`와 `PORTFOLIO_PRESENTATION.md`를 함께 동기화합니다.
4. **품질 점검 (Quality Gate):**
   - [ ] 모든 수치가 `SOURCE_OF_TRUTH_SNAPSHOT.md`와 일치하는가?
   - [ ] 미구현 항목이 `[PLANNED]`로 올바르게 격리되었는가?
   - [ ] 1 Slide = 1 Core Message 원칙을 유지하고 있는가?
