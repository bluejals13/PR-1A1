# Presentation Input Package for Gemini Canvas & Google Slides

본 디렉터리(`PRD-PO/presentation/`)는 `PR-Files/`에 축적된 검증된 엔지니어링 사실(Evidence)을 기반으로, **Gemini Canvas 또는 Google Slides에서 고품질의 15페이지 기술 발표자료를 생성하기 위한 입력 패키지(Input Package)**입니다.

---

## 1. 디렉터리 구조 및 파일별 역할

```
PRD-PO/presentation/
├── README.md                      # 본 가이드 문서
├── PRESENTATION_SPEC.md           # 15개 슬라이드 상세 설계 명세서 (Slide Plan & Visuals)
├── GEMINI_CANVAS_PROMPT.md        # Gemini Canvas 실행용 표준 프롬프트
├── PORTFOLIO_PRESENTATION.md      # 검증 완료된 전체 발표자료 마스터 스크립트
└── source/                        # 슬라이드별 사실 데이터 패키지 (Fact Base)
    ├── 01_PROJECT_OVERVIEW.md     # 프로젝트 정체성 및 4대 핵심 축
    ├── 02_PROBLEM_AND_SOLUTION.md # 직면 과제 및 기술적 해결책
    ├── 03_ARCHITECTURE.md         # Nginx Gateway & 7개 Docker 서비스 토폴로지
    ├── 04_AUTH_AND_RBAC.md        # JWT, RTR, Blacklist, M:N RBAC 인가
    ├── 05_CORE_IMPLEMENTATION.md  # 불변 Record DTO, ApiResponse, Flyway V1~V5
    ├── 06_SECURITY.md             # XSS, Replay Attack 방어 및 보안 필터 체인
    ├── 07_TESTING.md              # 10종 JUnit 자동화 테스트 스위트
    ├── 08_PERFORMANCE.md          # k6 70 VU 실측치 (Avg 5.64ms, 0% Error)
    ├── 09_TROUBLESHOOTING.md      # TS 6단계 실측 장애 3건 (Redis, JWT Loop, Docker)
    ├── 10_AI_WORKFLOW.md          # SA-1 8단계 AI 라이프사이클 및 거버넌스
    └── 11_LIMITATIONS_AND_ROADMAP.md # 현재 한계 및 [PLANNED] 로드맵
```

### 각 구성요소의 역할

1. **`source/` (Fact Data Package):**
   Gemini Canvas가 발표자료 생성 시 인용할 **정제된 사실 데이터** 모음입니다. 각 문서는 `What`, `Why`, `How`, `Evidence`, `Result`, `Status`, `Source` 형식으로 작성되어 환각(Hallucination)을 원천 차단합니다.
2. **`PRESENTATION_SPEC.md` (Presentation Blueprint):**
   슬라이드 1번부터 15번까지의 목적(Purpose), 핵심 메시지(Key Message), 필수 인용 수치(Metrics), 시각화 권장사항(Visual Recommendation), 발표자 의도(Speaker Intent)를 정의한 설계 문서입니다.
3. **`GEMINI_CANVAS_PROMPT.md` (Execution Command):**
   사용자가 Gemini Canvas에 복사하여 붙여넣기만 하면, 첨부된 `source/` 파일들을 기반으로 Google Slides에 즉시 적용 가능한 발표자료를 생성하도록 지시하는 완성형 프롬프트입니다.

---

## 2. Gemini Canvas 사용 방법

1. **Gemini Canvas 열기:** Gemini Advanced 웹 인터페이스에서 Canvas 모드를 활성화합니다.
2. **자료 첨부 (Attach):** `PRD-PO/presentation/source/` 폴더 내의 모든 마크다운 파일과 `PRESENTATION_SPEC.md`를 첨부합니다.
3. **프롬프트 실행:** [`GEMINI_CANVAS_PROMPT.md`](file:///C:/Users/user/Desktop/PR-1A1-main/PRD-PO/presentation/GEMINI_CANVAS_PROMPT.md)의 프롬프트 전문을 복사하여 입력창에 붙여넣고 전송합니다.
4. **결과 확인 및 Google Slides 반영:** 생성된 15페이지 슬라이드 레이아웃과 Speaker Notes를 검토하고 Google Slides 또는 PDF로 내보냅니다.

---

## 3. Source of Truth & Zero-Hallucination 정책

- **사실 기반 원칙:** 모든 수치와 주장은 `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`와 100% 일치해야 합니다.
  - k6 실측 불변치: **70 VUs, 1분, Avg 5.64ms, P95 9.98ms, Throughput 463 req/s, Error Rate 0.00%**
- **계획 사항 격리:** JPA N+1 정밀 쿼리 벤치마크, Message Queue(Kafka), Redis Cluster, Vault/TLS 등 미검증/미구현 항목은 반드시 `[PLANNED]` 태그 또는 Roadmap으로만 표기합니다.
- **금지 표현:** "완벽한 보안", "업계 최고 성능", "SLA 보장" 등 입증 불가능한 과장 표현은 절대 사용하지 않습니다.

---

## 4. 자료 업데이트 방법

1. `26-05adf` 또는 `SA-1`의 새로운 검증 결과가 발생하면, 먼저 `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`를 갱신합니다.
2. 갱신된 사실에 따라 `PRD-PO/presentation/source/` 내 해당 도메인 문서를 업데이트합니다.
3. 슬라이드 구성이 변경될 경우 `PRESENTATION_SPEC.md`의 슬라이드 번호 및 내용을 동기화합니다.
