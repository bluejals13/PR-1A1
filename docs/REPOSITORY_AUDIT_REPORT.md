# 3-Repository Portfolio & Evidence Architecture Audit Report

- **Audit Date:** 2026-09-05
- **Auditor:** Senior Software Architect & Portfolio Engineer (Antigravity Agent)
- **Target Repositories:**
  1. `26-05adf` (BUILD / Source of Truth for Application Implementation)
  2. `SA-1` (PROCESS / Source of Truth for Engineering Workflow & Decisions)
  3. `PR-1A1` (PROOF / Source of Truth for Evidence, Verification & Presentation)
- **Workspace Root:** `C:/Users/bluej/Desktop/my2`
- **Audit Phase:** Phase 1 (READ-ONLY AUDIT & COMPREHENSIVE ARCHITECTURE REPORT)
- **Status:** COMPLETED — PENDING USER APPROVAL FOR REFACTORING EXECUTION

---

## Executive Summary

본 감사는 3개 Git 저장소(`26-05adf`, `SA-1`, `PR-1A1`)가 독립적인 프로젝트처럼 분절되어 발생한 **문서 중복, 잘못된 테스트 참조, 코드-문서 불일치, 불변 스냅샷 부재** 문제를 발굴하고, 이를 하나의 유기적인 엔지니어링 스토리인 **`BUILD (26-05adf) ➔ PROCESS (SA-1) ➔ PROOF (PR-1A1)`** 파이프라인으로 통합 재구성하기 위한 종합 진단 보고서입니다.

현재 상태는 다음과 같습니다:
1. **BUILD (`26-05adf`):** Spring Boot 3.3.2, Java 17, React 18, Redis 7, MySQL 8, Nginx, k6 부하 테스트 및 15개 핵심 테스트가 완비된 견고한 구현체이나, 문서화 과정에서 일부 경로 및 버전 오차가 존재합니다.
2. **PROCESS (`SA-1`):** 8단계 AI 라이프사이클과 의사결정 기록(Why)이 우수하게 관리되고 있으나, `26-05adf` 문서와의 불필요한 중복 및 동기화 지연이 발생하고 있습니다.
3. **PROOF (`PR-1A1`):** 고품질의 발표자료 및 포트폴리오를 보유하고 있으나, 테스트 메서드명 가공(Hallucination), Commit SHA 미고정 스냅샷, 이중 렌더러 혼재 등 아키텍처적 부채를 안고 있습니다.

---

## 1. 세 Repository 구조 및 메타데이터

### 1.1 Repository Metadata Summary

| 항목 | `26-05adf` (BUILD) | `SA-1` (PROCESS) | `PR-1A1` (PROOF) |
| :--- | :--- | :--- | :--- |
| **Role** | Application Implementation | Engineering Process & Decisions | Evidence, Verification & Presentation |
| **Git Remote** | `https://github.com/bluejals13/26-05adf.git` | `https://github.com/bluejals13/SA-1.git` | `https://github.com/bluejals13/PR-1A1.git` |
| **Current Branch** | `feature/auth@0603@1401` | `main` | `main` |
| **Current HEAD SHA** | `9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f` | `4a734a8edd8b670f8d29dc2a42a978ca3877a25f` | `c9f88722ad196ef7918240ab1faaaba4a8f64676` |
| **Latest Commit** | `chore: ignore Gradle build cache` | `리드미.md :` | `JinJa2 의 적용` |
| **Working Tree** | Clean | Clean | Clean |
| **Primary Languages** | Java 17, TypeScript, SQL, Shell | Markdown, JSON | Python 3, HTML/CSS, JavaScript, YAML, Markdown |

---

### 1.2 `26-05adf` (BUILD) 세부 구조 및 구성 요소

```text
26-05adf/
├── backend/                              # Spring Boot 3.3.2 (Java 17, Gradle 8.14.4)
│   ├── src/main/java/com/example/demo/
│   │   ├── audit/                        # AuditAdminController, AuditService, Audit Entity
│   │   ├── auth/
│   │   │   ├── jwt/JwtProvider.java      # JJWT 0.11.5 기반 Access/Refresh 토큰 파싱 및 생성
│   │   │   └── security/                 # AuthController, AuthService, SecurityConfig,
│   │   │                                 # JwtAuthenticationFilter, RefreshTokenRepository(Lua),
│   │   │                                 # TokenBlacklistService, UserAuthorityService
│   │   ├── common/                       # ApiResponse, GlobalExceptionHandler
│   │   ├── iam/                          # User, Role, Permission, Menu 관리 도메인
│   │   └── monitoring/                   # BodyLoggingFilter, RequestLog, MonitorApiController
│   ├── src/main/resources/
│   │   ├── application.yaml              # Spring Boot 및 Lettuce 타임아웃(2000ms) 설정
│   │   └── db/migration/                 # Flyway 마이그레이션 V1 ~ V5
│   └── src/test/java/com/example/demo/   # 15개 단위/통합 테스트 클래스 (JUnit 5, Mockito, MockMvc)
├── frontend/                             # React 18, Vite, TypeScript
│   └── src/
│       ├── api/http.ts                   # Axios 인스턴스, Single-Flight Refresh, 401 탈출 조건
│       ├── auth/auth.bootstrap.ts        # 앱 마운트 시 FOUC 방지 및 토큰 복구
│       ├── store/auth.store.ts           # Zustand 기반 인증 상태 스토어
│       └── pages/, components/, queries/ # TanStack Query, ProtectedRoute, UI 컴포넌트
├── k6/                                   # 부하 테스트 시나리오 (load, stress, spike, soak, admin)
├── monitoring/                           # prometheus.yml, agent.yaml
├── nginx/                                # default.conf (Port 80 Reverse Proxy), Dockerfile
├── docker-compose.yml                    # 10개 컨테이너 서비스 정의 (Nginx, App, MySQL, Redis 등)
└── docs/                                 # 아키텍처, 퀵스타트, 컨벤션, 부하테스트, 장애보고서
```

---

### 1.3 `SA-1` (PROCESS) 세부 구조 및 구성 요소

```text
SA-1/
├── README.md                             # 지식 저장소 정의 및 3-Repository 데이터 흐름
├── architecture/
│   ├── 01_Architecture_and_Ports.md      # 시스템 토폴로지 및 포트 명세 (26-05adf docs와 중복)
│   └── 02_Quick_Start.md                 # 퀵 스타트 가이드 (26-05adf docs와 부분 중복)
├── changelogs/                           # Phase별 의사결정(Why) 및 트레이드오프 기록
│   ├── phase1_backend/                   # 1-1 ~ 1-5 (DTO 분리, JWT/Redis, 예외처리, JPA N+1, 문서화)
│   └── phase2_frontend/                  # 2-1 (Zustand 인증 및 Single-Flight)
├── conventions/
│   ├── 03_Backend_Conventions.md         # 백엔드 코딩 규칙 (26-05adf docs와 중복)
│   ├── 04_Agent_Commands.md              # AI 에이전트 협업 커맨드
│   └── rules.md                          # 문서 작성 5대 원칙 (26-05adf docs와 중복)
└── pkm&infra/
    ├── PKM/새 텍스트 문서.txt            # 임시 링크 메모 (정리 필요)
    └── infra/Dash보드.json               # Grafana 대시보드 JSON 템플릿
```

---

### 1.4 `PR-1A1` (PROOF) 세부 구조 및 구성 요소

```text
PR-1A1/
├── PR-Files/                             # 기술 및 검증 명세 문서
│   ├── evidence/                         # SOURCE_OF_TRUTH_SNAPSHOT.md
│   ├── architecture/                     # ARCHITECTURE_SPEC.md
│   ├── specification/                    # AUTH_AND_SECURITY_SPEC.md
│   ├── verification/                     # SECURITY_VERIFICATION_REPORT.md, DATA_LAYER_VERIFICATION.md
│   ├── performance/                      # K6_LOAD_TEST_REPORT.md
│   ├── troubleshooting/                  # TS-01, TS-001, TS-003 장애 보고서
│   └── ai-workflow/                      # AI_WORKFLOW_SPEC.md
├── PRD-PO/                               # 발표 및 포트폴리오 산출물
│   ├── presentation/                     # 15개 슬라이드 소스, 스타일, 웹 뷰어
│   ├── html/                             # 단일/분리 HTML 슬라이드 (1~14), ppt.pptx
│   └── case-study/                       # 핵심 문제해결 사례 연구 (CASE_STUDY.md)
├── registry/                             # 의존성 및 검증 메타데이터 (YAML)
│   ├── evidence.yaml                     # 증거 레지스트리 (실제 코드와 불일치 다수 발견)
│   ├── relations.yaml                    # 도메인-증거-문서 의존성 그래프
│   └── documents.yaml                    # 산출 문서 메타데이터
├── automation/                           # Python 기반 슬라이드 자동화 프레임워크 (Jinja2, DOM 분석)
├── renderer/                             # Node.js 기반 정적 사이트 렌더러 (구버전 파이프라인)
├── system/                               # 거버넌스 규약 (CHANGE_POLICY.md, DOMAINS.md 등)
└── docs/                                 # 자동화 설계 문서 및 본 보고서 위치
```

---

## 2. 각 Repository의 역할 및 Source of Truth 경계

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ENGINEERING TRUTH                              │
├───────────────────────┬─────────────────────────────┬───────────────────────┤
│       26-05adf        │            SA-1             │        PR-1A1         │
│        [BUILD]        │          [PROCESS]          │        [PROOF]        │
├───────────────────────┼─────────────────────────────┼───────────────────────┤
│ • Application Code    │ • Architecture Decisions    │ • Immutable Snapshots │
│ • Automated Tests     │ • Trade-off Analysis (Why)  │ • Evidence Registry   │
│ • Docker & Nginx Infra│ • Phase Changelogs          │ • Claims & Matrix     │
│ • Migration SQL       │ • AI Governance Rules       │ • Case Studies        │
│ • Load Test Scripts   │ • Agent Prompt Conventions  │ • Presentation Deck   │
│ • Runtime Executable  │ • Engineering Decisions     │ • Portfolio Web/HTML  │
└───────────────────────┴─────────────────────────────┴───────────────────────┘
```

1. **`26-05adf` = Application Source of Truth:**
   - 런타임에서 실제 빌드·실행·테스트되는 코드와 인프라의 단일 원본.
   - **원칙:** 어떤 문서나 포트폴리오도 `26-05adf`에 없는 코드를 구현된 것처럼 기술할 수 없습니다.
2. **`SA-1` = Engineering Process Source of Truth:**
   - 기술적 의사결정의 배경(Why), 대안 비교, AI 에이전트 거버넌스 및 컨벤션의 단일 원본.
   - **원칙:** 구현된 기능의 설계 의도와 엔지니어링 협업 과정은 `SA-1`에서 파생됩니다.
3. **`PR-1A1` = Evidence & Portfolio Source of Truth:**
   - 위 두 저장소로부터 추출된 팩트의 불변 스냅샷(Snapshot)을 보관하고, 이를 바탕으로 검증(Verification), 주장(Claim), 발표(Presentation), 포트폴리오(HTML)를 생산하는 공간.
   - **원칙:** `PR-1A1`은 원본 저장소를 대체하지 않으며, 특정 Commit SHA 시점의 증거만을 영속화합니다.

---

## 3. 기존 Evidence 구조 분석

- **현황:** `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` 단일 마크다운 파일에 팩트 요약과 추적성 표가 작성되어 있음.
- **결함:**
  1. **Commit SHA 미고정:** 브랜치명(`feature/auth@0603@1401`)만 표기되어 있어 브랜치 포인터 이동 시 재현 불가능.
  2. **기계 판독성 부재:** 순수 마크다운으로 작성되어 자동화 스크립트(`validate.py`)에 의한 Schema 검증 불가.
  3. **소스 스냅샷 부재:** 원본 파일의 내용이나 SHA-256 해시가 저장되지 않아 외부 원본 저장소 유실 시 증거 증명력 상실.

---

## 4. 기존 Claim 구조 분석

- **현황:**
  - `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`: 도메인별 텍스트 매트릭스 (ID 없음)
  - `APMS-SR_CLAIM_VERIFICATION.md`: 1~29번 순번 체계
  - `registry/evidence.yaml`: `ev-auth-rtr`, `ev-perf-70vu` 체계
  - `Evidence Ledger v1.0.md`: `E-001` ~ `E-025` 체계
- **결함:** Claim ID 체계가 4개 문서에서 제각각 파편화되어 상호 링크 및 자동화된 유효성 검사가 불가능함.

---

## 5. 기존 Verification 구조 분석

- **5대 상태 정책:** `[VERIFIED]`, `[IMPLEMENTED]`, `[DOCUMENTED]`, `[PLANNED]`, `[UNKNOWN]`
- **적용 현황:**
  - JUnit 테스트가 실제로 통과하는 핵심 보안/인가 기능은 `[VERIFIED]`로 분류됨.
  - k6 부하 테스트 70 VU 실측치(평균 5.64ms, 0% 에러)는 `[VERIFIED]`로 분류됨.
- **결함:**
  - `evidence.yaml` 및 검증 리포트에 적힌 테스트 메서드명이 실제 소스코드와 불일치함.
  - 대시보드 표출 등 일부 실측되지 않은 항목에 대해 엄격한 증거 로그가 누락됨.

---

## 6. 중복 문서 현황

| 파일명 | 저장소 A | 저장소 B | 일치율 | 분석 및 조치 방안 |
| :--- | :--- | :--- | :---: | :--- |
| `01_Architecture_and_Ports.md` | `26-05adf/docs` | `SA-1/architecture` | **100%** | 완전 중복. SA-1을 원본으로 두고 26-05adf는 링킹 처리 권장 |
| `02_Quick_Start.md` | `26-05adf/docs` | `SA-1/architecture` | **85%** | 26-05adf에 최근 Gradle 커맨드 추가됨. SA-1 동기화 필요 |
| `03_Backend_Conventions.md` | `26-05adf/docs` | `SA-1/conventions` | **100%** | 완전 중복. SA-1을 원본으로 확립 |
| `rules.md` | `26-05adf/docs` | `SA-1/conventions` | **100%** | 완전 중복. SA-1을 거버넌스 원본으로 확립 |
| `05_Agent_Commands.md` / `04_Agent_Commands.md` | `26-05adf/docs` | `SA-1/conventions` | **95%** | 파일명 넘버링 불일치 및 미세 차이. SA-1 기준으로 통일 |
| `ppt.pptx` vs `presentation.pptx` | `PR-1A1/PRD-PO/html` | `PR-1A1/PRD-PO/html` | **100%** | 3.35MB 대용량 동일 바이너리 중복. presentation.pptx 삭제 권장 |

---

## 7. 누락된 Evidence (Implemented but Unverified)

1. **JPA @EntityGraph 쿼리 최적화:**
   - `UserRepository.java`에 `@EntityGraph` 적용 완료 (`[IMPLEMENTED]`).
   - 그러나 적용 전/후 쿼리 수 비교 실측 로그 및 벤치마크 데이터 부재 (`[PLANNED]`로 명확히 표기 필요).
2. **Frontend bootstrapAuth & Single-Flight:**
   - `auth.bootstrap.ts` 및 `http.ts` 구현 완료 (`[IMPLEMENTED]`).
   - Vitest / Jest 단위 테스트 코드 부재.
3. **Grafana 대시보드 실시간 표출:**
   - JSON 템플릿과 Docker Compose 설정은 존재하나, 실시간 지표 알람 검증 증거 부재 (`[PARTIAL]` 유지 필요).
4. **Loki / Promtail 로깅 파이프라인:**
   - `docker-compose.yml`에 주석 처리되어 실행되지 않음 (`[PLANNED]`로 격리 필수).

---

## 8. 잘못 연결된 Evidence 및 실제 코드-문서 불일치 전수 조사

---

### [FACT-DISCREPANCY-01] 빌드 시스템 및 의존성 버전 오류

```text
[FACT]
26-05adf/backend/build.gradle:
- line 3: id 'org.springframework.boot' version '3.3.2'
- line 26: implementation 'io.jsonwebtoken:jjwt-api:0.11.5'
- 빌드 도구는 Gradle (build.gradle)이며, pom.xml은 존재하지 않음.

[OBSERVATION]
- PR-1A1/PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md line 28: "JJWT (0.12.x)"로 잘못 기재됨.
- PR-1A1/APMS-SR_CLAIM_VERIFICATION.md line 55: "backend/pom.xml (micrometer)"로 잘못 기재됨.

[IMPLICATION]
실제 코드베이스의 기술 스택을 정확히 파악하지 못하고 임의 작성한 것으로 오해받을 수 있음.

[RECOMMENDATION]
PR-1A1의 모든 스펙 및 검증 문서에서 빌드 도구를 Gradle로, JJWT 버전을 0.11.5로 전수 수정.

[CONFIDENCE]
HIGH (build.gradle 소스 직접 확인)
```

---

### [FACT-DISCREPANCY-02] 패키지 경로 및 클래스명 불일치

```text
[FACT]
26-05adf/backend/src/main/java/com/example/demo/:
- com.example.demo.auth.jwt.JwtProvider.java (JwtTokenProvider 아님)
- com.example.demo.auth.security.AuthService.java (auth.service 아님)
- com.example.demo.auth.security.TokenBlacklistService.java (auth.service 아님)
- com.example.demo.iam.user.domain.User.java (iam.entity 아님)

[OBSERVATION]
- PR-1A1/PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md:
  - com.example.demo.auth.security.JwtTokenProvider (클래스명 오기)
  - com.example.demo.auth.service.AuthService (패키지명 오기)
  - com.example.demo.auth.service.TokenBlacklistService (패키지명 오기)
  - com.example.demo.iam.entity.* (패키지명 오기)
- PR-1A1/PRD-PO/case-study/CASE_STUDY.md line 54:
  - backend/src/main/java/com/example/demo/auth/service/TokenBlacklistService.java

[IMPLICATION]
실제 자바 패키지 구조와 맞지 않는 레퍼런스로 인해 코드 링크 유효성 검사 실패.

[RECOMMENDATION]
정규 패키지 경로(com.example.demo.auth.jwt, com.example.demo.auth.security)로 전수 교체.

[CONFIDENCE]
HIGH (실제 파일 경로 확인 완료)
```

---

### [FACT-DISCREPANCY-03] 테스트 메서드명 날조(Hallucination) 및 한국어 메서드명 누락

```text
[FACT]
26-05adf/backend/src/test/java/:
- RefreshTokenRepositoryTest.java 실제 메서드:
  saveRefreshToken, deleteRefreshToken, rotateSuccess, rotateFail, rotateNull
- TokenBlacklistServiceTest.java 실제 메서드:
  blacklistSuccess, blacklistIgnoreInvalidInput, blacklistThrowsRedisUnavailableExceptionWhenRedisFails, isBlacklistedReturnsTrue, isBlacklistedReturnsFalse, isBlacklistedReturnsFalseForNullOrBlank, isBlacklistedThrowsRedisUnavailableExceptionWhenRedisFails
- RbacSecurityIntegrationTest.java 실제 메서드:
  adminCanAssignPermissions, normalUserCannotAssignPermissions, unauthenticatedUserCannotAssignPermissions
- MenuSecurityIntegrationTest.java 실제 메서드:
  MENU_READ_권한이_있으면_메뉴를_조회할_수_있다, MENU_READ_권한이_없으면_메뉴_조회가_거부된다, 인증된_사용자라도_MENU_READ가_없으면_403이다

[OBSERVATION]
- PR-1A1/registry/evidence.yaml line 17-19:
  - rotate_Success_ShouldReturnTrueAndSetNewJti (날조됨)
  - rotate_Fail_WhenCurrentJtiMismatch (날조됨)
  - rotate_Fail_WhenKeyDoesNotExist (날조됨)
- PR-1A1/registry/evidence.yaml line 34-35:
  - addToBlacklist_ShouldSetRedisKeyWithTtl (날조됨)
  - isBlacklisted_ShouldReturnTrue_WhenTokenExists (날조됨)
- PR-1A1/registry/evidence.yaml line 66-67:
  - accessAdminEndpoint_WithoutRole_Returns403 (날조됨)
  - accessAdminEndpoint_WithRole_Returns200 (날조됨)

[IMPLICATION]
존재하지 않는 가상의 테스트 메서드명을 Evidence Registry에 등록하여 Zero-Hallucination 원칙 위배.

[RECOMMENDATION]
evidence.yaml의 test_methods 목록을 실제 소스코드의 @Test 선언 메서드명과 100% 일치하도록 정정.

[CONFIDENCE]
HIGH (JUnit 소스코드 전수 검사 완료)
```

---

### [FACT-DISCREPANCY-04] Case Study 내 가공된 코드 스니펫

```text
[FACT]
26-05adf TokenBlacklistService.java:
- private final RedisTemplate<String, String> redisTemplate;
- private static final String BLACKLIST_KEY_PREFIX = "blacklist:";

[OBSERVATION]
PR-1A1/PRD-PO/case-study/CASE_STUDY.md line 59-60:
- private final StringRedisTemplate redisTemplate;
- private static final String BLACKLIST_PREFIX = "bl:";

[IMPLICATION]
실제 동작하는 코드와 케이스 스터디 상의 코드가 달라 구현 사실성 훼손.

[RECOMMENDATION]
CASE_STUDY.md의 코드 블록을 실제 구현 스니펫으로 교체.

[CONFIDENCE]
HIGH (소스코드 직접 대조)
```

---

## 9. 개선이 필요한 구조적 결함

1. **이중 렌더링 파이프라인의 공존:**
   - Node.js 기반 `renderer/`와 Python 기반 `automation/`이 분리되어 유지보수 혼선 유발. Python `automation/`으로 일원화 필요.
2. **Immutable 증거와 Human Editable 영역의 혼재:**
   - `PR-Files/evidence/` 내에 불변 스냅샷과 사람이 수정 가능한 영역이 구분되어 있지 않음.
   - `work/` 디렉터리를 신설하여 초안/리뷰/태스크와 불변 증거를 물리적으로 분리 필요.
3. **슬라이드 분절 불일치:**
   - `PRD-PO/presentation/slides/`는 15개 슬라이드(`001` ~ `015`)인 반면, `PRD-PO/html/분리된 html/`은 14개 슬라이드(`1` ~ `14`)로 구성되어 불일치.

---

## 10. 제안하는 최종 Directory Tree

```text
PR-1A1/
├── .agents/
│   └── agents/                           # 특화 서브에이전트 역할 정의
├── automation/                           # 통합 검증 및 슬라이드 빌드 파이프라인
│   ├── validate.py                       # 종합 유효성 검증 (Schema, Hash, SHA, Code Link)
│   ├── build.py                          # Jinja2 슬라이드 렌더러
│   ├── data/                             # 정규화된 슬라이드 JSON 데이터
│   ├── templates/                        # Jinja2 HTML 템플릿 (.html.j2)
│   └── tests/                            # 자동화 회귀 테스트 스위트 (pytest)
├── docs/                                 # 아키텍처 및 거버넌스 공식 문서
│   ├── REPOSITORY_AUDIT_REPORT.md        # [본 감사 보고서]
│   ├── EVIDENCE_ARCHITECTURE.md          # 증거 시스템 구조 및 생명주기
│   ├── SOURCE_OF_TRUTH_POLICY.md         # 단일 진실 원천 정책
│   ├── CLAIM_POLICY.md                   # 클레임 작성 및 승격 규약
│   ├── TRACEABILITY.md                   # 크로스 저장소 추적성 맵
│   ├── MANUAL_WORKFLOW.md                # 수동 작업자 워크플로우 가이드
│   ├── VERIFICATION_POLICY.md            # 검증 상태 판정 기준
│   └── REPOSITORY_RELATIONSHIP.md        # 3개 저장소 간 관계 정의
├── PR-Files/
│   ├── evidence/                         # [IMMUTABLE] 불변 증거 영역
│   │   ├── SOURCE_OF_TRUTH_SNAPSHOT.md   # 마크다운 종합 스냅샷
│   │   ├── SOURCE_OF_TRUTH_SNAPSHOT.json # 기계 판독형 메타데이터
│   │   ├── schemas/                      # claim.schema.json, evidence.schema.json
│   │   ├── manifests/                    # SOT-2026-09-05-001.json (Git SHA, SHA-256)
│   │   ├── snapshots/                    # 26-05adf, SA-1 핵심 소스 스냅샷 복사본
│   │   ├── claims/                       # CLM-SEC-001 ~ CLM-AI-001 (JSON Claims)
│   │   └── bundles/                      # EV-SEC-001 ~ EV-AI-001 (Evidence Bundles)
│   ├── architecture/                     # ARCHITECTURE_SPEC.md
│   ├── specification/                    # AUTH_AND_SECURITY_SPEC.md
│   ├── verification/                     # SECURITY_VERIFICATION_REPORT.md, DATA_LAYER_VERIFICATION.md
│   ├── performance/                      # K6_LOAD_TEST_REPORT.md
│   ├── troubleshooting/                  # TS-01-REDIS, TS-001-JWT, TS-003-DOCKER
│   └── ai-workflow/                      # AI_WORKFLOW_SPEC.md
├── PRD-PO/                               # [DERIVED] 최종 포트폴리오 산출물
│   ├── case-study/                       # CASE_STUDY.md (실제 코드와 100% 일치)
│   ├── html/                             # Web Portfolio & Presentation
│   │   ├── ppt.html
│   │   ├── ppt.pptx                      # 단일 정규 PPTX 바이너리
│   │   └── 분리된 html/
│   └── presentation/                     # 웹 슬라이드 시스템
├── work/                                 # [HUMAN EDITABLE] 사람 작업 및 검토 영역
│   ├── tasks/                            # 작업 진행 상태
│   ├── reviews/                          # 코드/문서 검토 피드백
│   └── drafts/                           # 초안 문서
├── AGENTS.md                             # 에이전트 거버넌스 규칙
├── README.md                             # 저장소 메인 인덱스
└── .gitignore
```

---

## 11. 파일별 이동 / 생성 / 수정 계획

| 저장소 | 대상 파일 / 경로 | 작업 구분 | 사유 및 상세 내용 |
| :--- | :--- | :---: | :--- |
| `PR-1A1` | `docs/REPOSITORY_AUDIT_REPORT.md` | **생성** | [본 파일] 감사 종합 보고서 작성 완료 |
| `PR-1A1` | `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.json` | **생성** | Git Commit SHA 고정 및 기계 판독형 SOT 메타데이터 구축 |
| `PR-1A1` | `PR-Files/evidence/manifests/SOT-2026-09-05-001.json` | **생성** | 파일별 SHA-256 해시가 기록된 불변 매니페스트 |
| `PR-1A1` | `PR-Files/evidence/claims/*.json` | **생성** | CLM-SEC-001 등 25개 핵심 엔지니어링 Claim 정규화 |
| `PR-1A1` | `PR-Files/evidence/bundles/EV-*/` | **생성** | 핵심 Claim별 증거 번들(소스, 테스트, 결과 로그) 구축 |
| `PR-1A1` | `work/{tasks,reviews,drafts}/` | **생성** | Immutable 증거와 분리된 인간 작업 영역 구축 |
| `PR-1A1` | `docs/EVIDENCE_ARCHITECTURE.md` 등 7종 정책서 | **생성** | Phase 13 거버넌스 및 정책 문서화 |
| `PR-1A1` | `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` | **수정** | Commit SHA 고정, 패키지 경로/JJWT 버전 오류 정정 |
| `PR-1A1` | `registry/evidence.yaml` | **수정** | JUnit 실제 메서드명(rotateSuccess 등)과 100% 일치 동기화 |
| `PR-1A1` | `PRD-PO/case-study/CASE_STUDY.md` | **수정** | 가공된 코드 스니펫을 실제 26-05adf 구현 코드로 교체 |
| `PR-1A1` | `APMS-SR_CLAIM_VERIFICATION.md` | **이동/통합** | 루트에서 `PR-Files/verification/` 하위로 이동 또는 SOT와 통합 |
| `PR-1A1` | `APMS-SR_PPT_COMPOSITION.md` | **이동** | 루트에서 `PRD-PO/presentation/` 하위로 이동 |
| `PR-1A1` | `PRD-PO/html/presentation.pptx` | **삭제** | `ppt.pptx`와 100% 동일한 3.35MB 바이너리 중복 제거 |
| `PR-1A1` | `automation/validate.py` | **수정/확장** | JSON Schema, SHA-256, Git Commit, Claim 링크 검증 로직 추가 |
| `SA-1` | `architecture/02_Quick_Start.md` | **수정** | `26-05adf`의 최근 Gradle 커맨드 변경점 동기화 |
| `SA-1` | `pkm&infra/PKM/새 텍스트 문서.txt` | **정리** | 불필요한 깨진 텍스트 파일 정리 및 정규 마크다운 변환 |
| `26-05adf` | `Readme.md` | **수정** | line 30의 깨진 링크(`docs/단순 설치.md` -> `docs/05_Installation.md`) 수정 |

---

## 12. 변경하지 말아야 할 파일 (Immutable Preservation List)

다음 파일들은 원본의 역사성, 기준 지문(Baseline), 또는 핵심 구현이므로 **절대 삭제하거나 임의로 내용을 변형해서는 안 됩니다.**

1. `26-05adf`의 모든 소스 코드 및 테스트 파일 (`backend/src/**`, `frontend/src/**`, `k6/**`)
2. `26-05adf/docker-compose.yml`, `backend/build.gradle`
3. `SA-1/changelogs/phase1_backend/**`, `phase2_frontend/**` (의사결정 역사 기록)
4. `PR-1A1/PRD-PO/html/분리된 html/*.original.html` (DOM 지문 원본)
5. `PR-1A1/rendered/_golden/*.golden.html` (골든 테스트 기준 파일)
6. `PR-1A1/design-system/**` (디자인 토큰 및 CSS)

---

## 13. 위험 요소 및 대응 방안

| 위험 요소 (Risk) | 영향도 | 발생 시나리오 | 대응 방안 (Mitigation) |
| :--- | :---: | :--- | :--- |
| **상대 경로 참조 단절** | High | 마크다운 문서나 슬라이드 이동 시 이미지/CSS 링크 깨짐 | 모든 파일 이동 전 `ripgrep`으로 링크 참조 전수 조사 및 상대 경로 일괄 보정 |
| **자동화 렌더링 회귀** | High | `automation/validate.py` 변경 시 기존 슬라이드 빌드 깨짐 | `automation/tests/test_parity.py` 및 `test_build.py` 선행 통과 검증 |
| **대용량 Git Diff 발생** | Medium | 바이너리 파일 커밋 또는 대량 포맷팅 변경 시 추적 어려움 | Git diff를 최소화하고, 바이너리 변경은 분리 커밋하며, 텍스트 diff 중심 작업 |
| **코드-문서 재불일치** | Medium | 향후 `26-05adf` 코드 수정 시 `PR-1A1`이 뒤처짐 | Git Commit SHA를 강제하는 Snapshot Manifest 체계로 버전 고정 |

---

## 14. 예상되는 Git Diff 요약

- **`26-05adf`:** `Readme.md` 내 깨진 링크 1줄 수정 (최소 diff)
- **`SA-1`:** `architecture/02_Quick_Start.md` 퀵스타트 명령어 동기화, `pkm&infra` 불필요 파일 정리
- **`PR-1A1`:**
  - `docs/REPOSITORY_AUDIT_REPORT.md` (신규 생성)
  - `PR-Files/evidence/` (manifests, claims, bundles 신규 생성, snapshot 수정)
  - `registry/evidence.yaml`, `PRD-PO/case-study/CASE_STUDY.md` (실제 코드와 일치하도록 수정)
  - `work/` (신규 작업 디렉터리 생성)
  - `automation/validate.py` (검증 로직 확장)
  - `PRD-PO/html/presentation.pptx` (중복 바이너리 삭제)

---

## 15. 최종 검증 방법 (Final Validation Plan)

리팩토링 완료 후 다음 검증을 자동으로 수행하여 100% 무결성을 증명합니다.

1. **Python 통합 검증 스크립트 실행:**
   ```bash
   py PR-1A1/automation/validate.py --all
   ```
   - JSON Schema 유효성 (Claim, Evidence, Manifest)
   - SHA-256 해시 무결성 검증 (스냅샷 파일 vs 원본)
   - Git Commit SHA 실재 여부 검증
   - Claim ID 중복 및 누락 검사
   - 테스트 클래스 및 메서드 실재 여부 검사 (26-05adf 코드베이스 스캔)
   - 마크다운 및 HTML 링크 유효성 검사
2. **슬라이드 구조 일치성 테스트 (Parity Test):**
   ```bash
   py -m pytest PR-1A1/automation/tests/test_parity.py
   ```
3. **Git Diff 무결성 확인:**
   ```bash
   git status && git diff --stat
   ```

---
*End of Audit Report.*
