# Repository Audit — APMS.SR Document System

- **Audit Date:** 2026-08-29
- **Auditor:** Antigravity AI Agent
- **Phase:** PHASE 1 — Full Repository Audit
- **Status:** COMPLETE (Read-only. No files modified.)

---

## Table of Contents

1. [26-05adf — Implementation Repository](#1-26-05adf--implementation-repository)
2. [SA-1 — Knowledge Repository](#2-sa-1--knowledge-repository)
3. [PR-1A1 — Presentation Repository](#3-pr-1a1--presentation-repository)
4. [Cross-Repository Relationships](#4-cross-repository-relationships)
5. [Engineering Domain Status Matrix](#5-engineering-domain-status-matrix)
6. [PPT / HTML vs Source Discrepancies](#6-ppt--html-vs-source-discrepancies)
7. [Document Candidates](#7-document-candidates)
8. [Evidence Candidates](#8-evidence-candidates)
9. [Broken Links / Invalid References](#9-broken-links--invalid-references)
10. [Reusable Structures in PR-1A1](#10-reusable-structures-in-pr-1a1)
11. [Do NOT Modify](#11-do-not-modify)
12. [PHASE 2 Plan](#12-phase-2-plan)

---

## 1. 26-05adf — Implementation Repository

### Role
Actual Development Repository. Single source of truth for all code, tests, configuration, and runtime evidence.

### Actual Directory Structure (Verified by filesystem scan)

```
26-05adf/
├── .agents/
├── .codex/
├── .cursorrules                     [1,360 bytes]
├── .env                             [410 bytes]
├── .github/
├── AGENTS.md                        [774 bytes]
├── Readme.md                        [9,329 bytes]
├── backend/
│   ├── Dockerfile
│   ├── build.gradle                 [2,094 bytes]
│   ├── settings.gradle
│   └── src/
│       ├── main/
│       │   ├── java/com/example/demo/
│       │   │   ├── DemoApplication.java
│       │   │   ├── audit/           (AuditAdminController, Audit, AuditAction, AuditRepository, AuditAdminService, AuditService)
│       │   │   ├── auth/
│       │   │   │   ├── jwt/         (JwtProvider)
│       │   │   │   └── security/    (AuthController, AuthService, CustomUserPrincipal, JwtAuthenticationFilter,
│       │   │   │                     RedisUnavailableException, RefreshTokenRepository, SecurityConfig,
│       │   │   │                     TokenBlacklistService, UserAuthorityService)
│       │   │   ├── common/
│       │   │   │   ├── dto/         (ApiResponse)
│       │   │   │   └── exception/   (DuplicateUserException, GlobalExceptionHandler, UserNotFoundException)
│       │   │   ├── config/          (JpaConfig, SecurityUtil)
│       │   │   ├── iam/
│       │   │   │   ├── admin/       (UserAdminController + DTOs + Services)
│       │   │   │   ├── menu/        (MenuAdminController, Menu, MenuRequest/Response, MenuRepository, MenuAdminService)
│       │   │   │   ├── permission/  (PermissionAdminController, Permission, PermissionRepository, PermissionAdminService)
│       │   │   │   ├── role/        (RoleAdminController, Role, RoleDtos, RoleRepository, RoleAdminService, RolePermissionService)
│       │   │   │   └── user/        (UserController, PageController, User, UserStatus, LoginRequest/Response/Result,
│       │   │   │                     MeResponse, SignupRequest, UpdatePasswordRequest, UserRepository, UserService)
│       │   │   └── monitoring/      (BodyLoggingFilter, LogStore, MonitorApiController, MonitorPageController,
│       │   │                         RequestLog, RequestLoggingFilter)
│       │   └── resources/
│       │       ├── application.properties  [604 bytes]
│       │       ├── application.yaml        [556 bytes]
│       │       └── db/migration/
│       │           ├── V1__init_schema.sql        (users, roles, menus)
│       │           ├── V2__init_authority_schema.sql  (permissions, user_roles, role_permissions)
│       │           ├── V3__init_common_schema.sql     (audit_logs)
│       │           ├── V4__insert_permissions.sql
│       │           └── V5__insert_test_users.sql
│       └── test/java/com/example/demo/
│           ├── auth/security/
│           │   ├── AuthControllerTest.java
│           │   ├── AuthServiceTest.java
│           │   ├── JwtAuthenticationFilterTest.java
│           │   ├── RefreshTokenRepositoryTest.java
│           │   ├── SecurityIntegrationTest.java
│           │   └── TokenBlacklistServiceTest.java
│           ├── iam/
│           │   ├── permission/  (PermissionAdminServiceTest, PermissionIntegrationTest, PermissionRepositoryTest)
│           │   ├── rbac/        (RbacSecurityIntegrationTest)
│           │   └── role/        (RoleAdminServiceTest, RolePermissionIntegrationTest, RolePermissionServiceTest, RoleRepositoryTest)
│           └── menu/
│               └── MenuSecurityIntegrationTest.java
├── docker-compose.yml               [3,364 bytes]
├── docs/
│   ├── 01_Architecture_and_Ports.md [6,013 bytes]
│   ├── 02_Quick_Start.md            [3,692 bytes]
│   ├── 03_Backend_Conventions.md    [6,269 bytes]
│   ├── 04_Agent_Commands.md         [1,675 bytes]
│   ├── README.md
│   ├── performance/
│   │   └── k6-load-test.md          [6,158 bytes]   <- 실측 k6 결과 기록
│   ├── reference/
│   ├── rules.md
│   ├── testing/
│   │   └── security-tests.md        [7,271 bytes]
│   └── troubleshooting/
├── frontend/
│   ├── Dockerfile
│   ├── package.json                 (React + Vite + TypeScript)
│   └── src/
│       ├── api/                     (http.ts, menu.api.ts, role.api.ts, user.api.ts)
│       ├── auth/                    (auth.bootstrap.ts, auth.keys.ts, auth.schema.ts,
│       │                             auth.service.ts, auth.storage.ts, auth.types.ts, hooks/)
│       ├── components/
│       ├── constants/
│       ├── layout/
│       ├── mutations/
│       ├── pages/
│       ├── queries/
│       ├── queryClient.ts
│       ├── store/
│       │   └── auth.store.ts        (Zustand + persist)
│       └── style/
├── k6/
│   ├── README.md                    [4,884 bytes]
│   ├── api/
│   ├── config/                      (thresholds.js 포함)
│   ├── core/
│   ├── run.js
│   ├── scenarios/
│   │   ├── admin-flow.js
│   │   ├── load.test.js
│   │   ├── read.flow.js
│   │   ├── soak.test.js
│   │   ├── spike.test.js
│   │   ├── stress.test.js
│   │   └── user.flow.js
│   └── setup.js
├── monitoring/
│   ├── agent.yaml
│   └── prometheus.yml               [486 bytes]
├── nginx/
│   ├── Dockerfile
│   └── default.conf                 [1,032 bytes]
└── task_progress.md                 [2,778 bytes]
```

### Important Files

| File | Role | Status |
|------|------|--------|
| `task_progress.md` | Phase별 작업 완료 추적 | Phase 1, 1.5, 2-1 완료. Phase 2-2, 2-3, 3-x 미완료 |
| `AGENTS.md` | AI 에이전트 규칙 (간략) | EXISTS |
| `.cursorrules` | 코드 생성 규칙 + Documentation First Policy | EXISTS |
| `Readme.md` | 전체 시스템 아키텍처 문서 | EXISTS — 컨테이너/API/Frontend 구조 포함 |
| `docker-compose.yml` | 전체 컨테이너 오케스트레이션 | EXISTS — depends_on/healthcheck 미설정 [PLANNED] |
| `docs/performance/k6-load-test.md` | k6 실측 결과 원본 | EXISTS — 7차 실행 결과 수치 포함 |
| `docs/testing/security-tests.md` | 보안 테스트 명세 | EXISTS |
| `nginx/default.conf` | Nginx 리버스 프록시 설정 | EXISTS — 보안 헤더/Rate Limiting 미설정 [PLANNED] |
| `monitoring/prometheus.yml` | Prometheus 스크랩 설정 | EXISTS |
| `db/migration/V1~V5__*.sql` | Flyway DB 스키마 | EXISTS — 5개 마이그레이션 파일 |

### Verified Capabilities

| Domain | Claim | Status | Evidence Source |
|--------|-------|--------|----------------|
| Authentication | Stateless JWT Access Token (1h, Bearer) | VERIFIED | JwtAuthenticationFilterTest.java |
| Authentication | Refresh Token (7d, HttpOnly Cookie, UUID JTI) | VERIFIED | RefreshTokenRepositoryTest.java |
| Authentication | RTR (Lua Script 원자적 교체) | VERIFIED | RefreshTokenRepositoryTest.java |
| Authentication | Token Blacklist (로그아웃 시 Redis 등록) | VERIFIED | TokenBlacklistServiceTest.java |
| Authorization | RBAC (User-Role-Permission M:N) | VERIFIED | RbacSecurityIntegrationTest.java |
| Authorization | Spring Security CustomProvider | VERIFIED | SecurityIntegrationTest.java |
| Authorization | Menu-based 권한 | VERIFIED | MenuSecurityIntegrationTest.java |
| API Design | GlobalExceptionHandler + ApiResponse<T> | IMPLEMENTED | GlobalExceptionHandler.java, ApiResponse.java |
| API Design | Record 기반 불변 DTO | IMPLEMENTED | LoginRequest.java 등 |
| Persistence | Flyway V1~V5 마이그레이션 | IMPLEMENTED | db/migration/*.sql |
| Persistence | JPA @EntityGraph + Fetch Join (N+1 방지) | IMPLEMENTED | RoleRepository.java, UserRepository.java |
| Frontend | Zustand + persist (Access Token 새로고침 보존) | IMPLEMENTED | auth.store.ts |
| Frontend | Bootstrap Auth Gateway (bootstrapAuth) | IMPLEMENTED | auth.bootstrap.ts |
| Frontend | Single Flight 재발급 (refreshPromise) | IMPLEMENTED | http.ts |
| Frontend | React Query + TanStack | IMPLEMENTED | queryClient.ts, queries/ |
| Infrastructure | Docker Compose (8개 서비스) | IMPLEMENTED | docker-compose.yml |
| Infrastructure | Nginx Reverse Proxy (Port 80) | VERIFIED | nginx/default.conf + k6 통과 |
| Infrastructure | MySQL 8.0 + Redis 7.0 역할 분리 | IMPLEMENTED | docker-compose.yml |
| Performance | 70VU: avg 5.64ms, P95 9.98ms, 463 req/s, 0% | VERIFIED | docs/performance/k6-load-test.md (5~7차) |
| Performance | 50VU: avg ~25ms, 2000+ req/s, 0% | VERIFIED | docs/performance/k6-load-test.md (2~4차) |
| Observability | Prometheus + VictoriaMetrics + Grafana Agent | IMPLEMENTED | docker-compose.yml, monitoring/ |
| Observability | Spring Actuator /actuator/prometheus | VERIFIED | prometheus.yml 스크랩 설정 |
| Observability | Grafana 대시보드 (실시간 검증) | PARTIAL | 컨테이너 설정 있음, 스크린샷 없음 |
| Audit | AuditService (감사 로그) | IMPLEMENTED | audit/ 패키지 |
| Monitoring | BodyLoggingFilter, RequestLoggingFilter | IMPLEMENTED | monitoring/ 패키지 |

### Unverified / Not Found / Planned

| Claim | Status | Note |
|-------|--------|------|
| JPA N+1 실측 벤치마크 (쿼리 수 before/after) | PLANNED | 코드 최적화 완료, 정량 수치 미측정 |
| React Query 캐싱 전략 정립 | PLANNED | task_progress Phase 2-2 미완료 |
| Protected Route 깜빡임 완전 제거 | PLANNED | task_progress Phase 2-3 미완료 |
| docker-compose depends_on + healthcheck | PLANNED | task_progress Phase 3-1 미완료 |
| Nginx 보안 헤더 + Rate Limiting | PLANNED | task_progress Phase 3-2 미완료 |
| Grafana 실시간 대시보드 스크린샷 | NOT FOUND | 증거 파일 없음 |
| k6 결과 원본 stdout 로그 파일 | NOT FOUND | 수치는 문서화됨, 원본 파일 없음 |
| Gradle 빌드 성공 로그 | NOT FOUND | changelog 언급만 있음 |
| SSL/TLS 인증서 | PLANNED | 현재 Port 80 HTTP만 운영 |
| Kafka/RabbitMQ 비동기 | PLANNED | 미구현 |
| Redis Cluster | PLANNED | 미구현 |
| OWASP ZAP 자동화 침투테스트 | PLANNED | 미구현 |
| Kubernetes / HPA | PLANNED | 미구현 |
| 1,000+ VU 분산 부하 테스트 | PLANNED | 미수행 |

### task_progress.md 요약

```
Phase 1 (Backend):    COMPLETE — 1-1 DTO, 1-2 JWT/Redis, 1-3 ApiResponse, 1-4 JPA N+1
Phase 1.5 (Docs):    COMPLETE — docs/ 3종 + guideline 저장소 동기화
Phase 2 (Frontend):  2-1 COMPLETE, 2-2 PLANNED, 2-3 PLANNED
Phase 3 (Infra):     3-1 PLANNED, 3-2 PLANNED, 3-3 PLANNED
```

---

## 2. SA-1 — Knowledge Repository

### Role
Technical Knowledge Repository. Architecture decisions, conventions, changelogs, PKM, and infra knowledge.
NOT a duplicate of 26-05adf code.

### Actual Directory Structure (Verified by filesystem scan)

```
SA-1/
├── README.md                        [1,383 bytes]   <- NOTE: .cursorrules 내용이 그대로 복사됨 (역할 혼란)
├── architecture/
│   ├── 01_Architecture_and_Ports.md [6,013 bytes]   <- 26-05adf/docs/와 동일 (중복)
│   └── 02_Quick_Start.md            [3,692 bytes]   <- 26-05adf/docs/와 동일 (중복)
├── changelogs/
│   ├── 026Y{08_26 - 09_xx}+위페이즈3끝난 날짜/   <- 빈 디렉터리 (Phase 3 미완료)
│   ├── phase1_backend/
│   │   ├── 1-1. Entity와 DTO의 엄격한 분리.md      [1,509 bytes]
│   │   ├── 1-2_jwt_redis_optimization.md            [3,645 bytes]
│   │   ├── 1-3_global_response_exception_handling.md [3,162 bytes]
│   │   ├── 1-4_jpa_n1_query_optimization.md         [4,514 bytes]
│   │   └── 1-5_core_documentation.md                [1,612 bytes]
│   ├── phase2_frontend/
│   │   └── 2-1_zustand_auth_optimization.md         [11,113 bytes]
│   └── phase3_infra/                                 <- 빈 디렉터리
├── conventions/
│   ├── 03_Backend_Conventions.md    [6,269 bytes]   <- 26-05adf/docs/와 동일 (중복)
│   ├── 04_Agent_Commands.md         [1,675 bytes]   <- 26-05adf/docs/와 동일 (중복)
│   └── rules.md                     [2,253 bytes]
└── pkm&infra/
    ├── PKM/
    │   └── 새 텍스트 문서.txt       [210 bytes]   <- 실질적으로 비어 있음 (미개발)
    └── infra/
        └── Dash보드.json            [3,722 bytes]   <- Grafana 대시보드 JSON 1개
```

### Critical Problems Discovered

**WARNING: SA-1 README.md** — `.cursorrules` 내용을 그대로 복사한 파일입니다. SA-1 Repository 자체의 역할과 목적을 설명하는 문서가 아닙니다.

**WARNING: 파일 중복** — SA-1의 `architecture/01_Architecture_and_Ports.md`, `architecture/02_Quick_Start.md`, `conventions/03_Backend_Conventions.md`, `conventions/04_Agent_Commands.md` 는 `26-05adf/docs/`의 파일과 내용이 동일합니다. SA-1이 guideline 저장소로서 동기화된 것이나, Source of Truth가 어느 쪽인지 명확하지 않습니다.

**WARNING: PKM 미개발** — `pkm&infra/PKM/새 텍스트 문서.txt`는 실질적으로 비어있습니다.

**WARNING: Phase 3 changelog 없음** — `changelogs/phase3_infra/`는 완전히 빈 디렉터리입니다.

### Important Files

| File | Role | Note |
|------|------|------|
| `changelogs/phase1_backend/1-2_jwt_redis_optimization.md` | JWT + Redis 최적화 이유, 변경 내역 | IMPORTANT — Why 중심 지식 |
| `changelogs/phase1_backend/1-4_jpa_n1_query_optimization.md` | JPA N+1 문제 분석 + @EntityGraph 결정 이유 | IMPORTANT — Why 중심 지식 |
| `changelogs/phase2_frontend/2-1_zustand_auth_optimization.md` | Frontend 인증 아키텍처 결정 이유 | IMPORTANT — Why 중심 지식 |
| `conventions/rules.md` | AI 협업 규칙, Zero-Chatter, Documentation First | EXISTS |
| `pkm&infra/infra/Dash보드.json` | Grafana 대시보드 JSON | EXISTS — 실제 사용 여부 미검증 |

### Knowledge Relationships (Changelog → Implementation)

| Changelog | 설명하는 지식 | 연결되는 26-05adf 구현 |
|-----------|-------------|----------------------|
| `1-2_jwt_redis_optimization.md` | JwtParser 캐싱, DataAccessException 처리, Token Type 검증, 이중 파싱 제거 이유 | `JwtProvider.java`, `TokenBlacklistService.java`, `JwtAuthenticationFilter.java` |
| `1-4_jpa_n1_query_optimization.md` | @EntityGraph 적용 결정 이유, LAZY vs EAGER 전략, Set<T> 사용 이유 | `RoleRepository.java`, `UserRepository.java`, `UserRoleService.java` |
| `2-1_zustand_auth_optimization.md` | Access Token 휘발 문제, bootstrapAuth 게이트웨이 패턴, Single Flight 이유 | `auth.store.ts`, `auth.bootstrap.ts`, `http.ts`, `App.tsx` |

---

## 3. PR-1A1 — Presentation Repository

### Role
Presentation / Portfolio Repository. Document Registry, templates, evidence presentation, HTML output.
References 26-05adf and SA-1. Does NOT contain actual implementation code.

### Actual Directory Structure (Verified by filesystem scan)

```
PR-1A1/
├── .agents/
├── .cursorrules                     [1,414 bytes]
├── AGENTS.md                        [2,334 bytes]
├── APMS-1.pptx                      [2,064,534 bytes]   <- 실제 PPT 파일 (2MB)
├── APMS-SR_CLAIM_VERIFICATION.md    [8,232 bytes]       <- 29개 Claim 검증 결과
├── APMS-SR_PPT_COMPOSITION.md       [21,430 bytes]      <- 14 Slide 구성 명세
├── README.md                        [3,442 bytes]
├── PRD-PO/
│   ├── README.md
│   ├── case-study/
│   │   ├── CASE_STUDY.md            [10,398 bytes]
│   │   └── README.md
│   ├── html/
│   │   ├── README.md
│   │   ├── index.html               [29,269 bytes]   <- Web Portfolio (현재 버전)
│   │   ├── ppt.html                 [88,681 bytes]   <- PPT 형식 HTML (현재 버전)
│   │   └── 이전버전ppt.html          [74,139 bytes]   <- 이전 버전 (미사용)
│   └── presentation/
│       ├── GEMINI_CANVAS_PROMPT.md
│       ├── PORTFOLIO_PRESENTATION.md [23,983 bytes]
│       ├── PRESENTATION_QA_REPORT.md
│       ├── PRESENTATION_SPEC.md
│       ├── README.md
│       └── source/
└── PR-Files/
    ├── README.md
    ├── ai-workflow/
    │   ├── AI_WORKFLOW_SPEC.md      [3,929 bytes]
    │   └── README.md
    ├── architecture/
    │   ├── ARCHITECTURE_SPEC.md     [5,349 bytes]
    │   └── README.md
    ├── evidence/
    │   ├── README.md
    │   └── SOURCE_OF_TRUTH_SNAPSHOT.md [9,891 bytes]   <- 핵심 Evidence 스냅샷
    ├── performance/
    │   ├── K6_LOAD_TEST_REPORT.md   [4,128 bytes]
    │   └── README.md
    ├── specification/
    │   ├── AUTH_AND_SECURITY_SPEC.md [6,949 bytes]
    │   └── README.md
    ├── troubleshooting/
    │   ├── README.md
    │   ├── TS-001_JWT_REFRESH_LOOP.md  [2,539 bytes]
    │   ├── TS-003_DOCKER_REDIS_BINDING.md [2,448 bytes]
    │   └── TS-01-REDIS_TIMEOUT.md   [2,617 bytes]
    └── verification/
        ├── DATA_LAYER_VERIFICATION.md [23,985 bytes]   <- 가장 상세한 Evidence 문서
        ├── README.md
        └── SECURITY_VERIFICATION_REPORT.md [5,732 bytes]
```

### Important Files

| File | Role | Note |
|------|------|------|
| `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` | 검증된 사실 스냅샷 (Fact Base) | CRITICAL — 모든 포트폴리오의 근거 기준 |
| `APMS-SR_CLAIM_VERIFICATION.md` | 29개 기술 Claim 상태 검증 결과 | CRITICAL — VERIFIED/IMPLEMENTED/PLANNED 분류 완료 |
| `APMS-SR_PPT_COMPOSITION.md` | 14 Slide 구성 명세 | Reference — HTML 생성 시 참조용 |
| `APMS-1.pptx` | 실제 PPT 파일 | Reference Artifact (Source of Truth 아님) |
| `PRD-PO/html/index.html` | 현재 Web Portfolio | 기존 산출물 (29KB) |
| `PRD-PO/html/ppt.html` | 현재 PPT 형식 HTML | 기존 산출물 (89KB) |
| `PR-Files/verification/DATA_LAYER_VERIFICATION.md` | Data Layer 상세 Evidence | IMPORTANT — Level 1~4 증거 기록 |
| `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` | Auth/Security 기술 명세 | IMPORTANT |
| `PR-Files/troubleshooting/TS-*.md` | 3개 장애 해결 기록 | EXISTS — TS-01, TS-001, TS-003 |

### Existing HTML Assessment

| File | Size | Assessment |
|------|------|------------|
| `ppt.html` | 88,681 bytes | 14 slide 구조. 단일 HTML 파일. Template 시스템 없음. |
| `index.html` | 29,269 bytes | Web Portfolio. 단일 HTML 파일. 섹션 네비게이션 있음. |
| `이전버전ppt.html` | 74,139 bytes | 이전 버전. 현재 미사용. |

**NOTE:** 기존 `ppt.html`과 `index.html`은 하드코딩된 단일 파일입니다. Document Model → Template → Renderer 구조가 없습니다. 새 Document System은 이를 대체하되, 기존 파일을 즉시 삭제하지 않습니다.

### PR-1A1 Missing Structure (현재 없는 것)

```
PR-1A1/
 system/                 <- AUDIT.md 생성 위치 (신규, 이 파일)
 registry/               <- Document Registry (없음)
 content/                <- Document Model (없음)
 templates/              <- Template System (없음)
 design-system/          <- Design System (없음)
 rendered/               <- Rendered HTML 출력 (없음)
 validation/             <- Validator (없음)
```

---

## 4. Cross-Repository Relationships

```
26-05adf                     SA-1                      PR-1A1
(Implementation)         (Knowledge Layer)         (Presentation Layer)

실제 코드           ->    "왜 이렇게 만들었는가?"    ->    "무엇을 달성했는가?"
JwtProvider.java    ->    1-2_jwt_redis_opt           ->    AUTH_AND_SECURITY_SPEC.md
RefreshTokenRepo    ->    (Lua Script 원자성 결정)    ->    SOURCE_OF_TRUTH_SNAPSHOT.md
UserRepository      ->    1-4_jpa_n1_query_opt        ->    DATA_LAYER_VERIFICATION.md
RoleRepository      ->    (@EntityGraph 결정 이유)    ->    (Document 후보 apms-jpa)
auth.store.ts       ->    2-1_zustand_auth_opt        ->    (Document 후보 apms-frontend-auth)
http.ts             ->    (Single Flight 이유)        ->    (Document 후보)
k6/scenarios/       ->    (미개발)                   ->    K6_LOAD_TEST_REPORT.md
docker-compose.yml  ->    architecture/01_Arch...     ->    ARCHITECTURE_SPEC.md
TS-01 Redis timeout ->    (미개발)                   ->    TS-01-REDIS_TIMEOUT.md
```

### 현재 Source of Truth 흐름 (실제)

```
26-05adf (Primary Source of Truth)
    |
    v
PR-1A1/PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md (스냅샷)
    |
    v
PR-1A1/APMS-SR_CLAIM_VERIFICATION.md (Claim 검증)
    |
    v
PR-1A1/PRD-PO/html/ppt.html (현재 HTML 출력)
```

**주의:** SA-1은 현재 Source of Truth 흐름에서 명확하게 연결되어 있지 않습니다. SA-1 changelogs가 PR-1A1 문서에서 참조되지 않고 있습니다.

---

## 5. Engineering Domain Status Matrix

각 항목은 실제 Repository를 직접 조사하여 판정했습니다.

| Domain | Aspect | Status | Primary Evidence |
|--------|--------|--------|-----------------|
| **Authentication** | JWT Access Token (1h, Bearer) | VERIFIED | JwtAuthenticationFilterTest.java |
| **Authentication** | Refresh Token (7d, HttpOnly Cookie) | VERIFIED | RefreshTokenRepositoryTest.java |
| **Authentication** | RTR (Lua Script 원자적 교체) | VERIFIED | RefreshTokenRepositoryTest.java |
| **Authentication** | Token Blacklist (Redis, 잔여 TTL) | VERIFIED | TokenBlacklistServiceTest.java |
| **Authentication** | Token Type 검증 (type=access) | IMPLEMENTED | JwtAuthenticationFilter.java |
| **Authorization** | RBAC (User-Role-Permission M:N) | VERIFIED | RbacSecurityIntegrationTest.java |
| **Authorization** | Spring Security CustomProvider | VERIFIED | SecurityIntegrationTest.java |
| **Authorization** | Menu-based 권한 | VERIFIED | MenuSecurityIntegrationTest.java |
| **Authorization** | OWASP 침투테스트 | PLANNED | — |
| **JWT** | JwtProvider (캐싱, 예외 세분화) | IMPLEMENTED | JwtProvider.java |
| **Redis** | Refresh Token Store | VERIFIED | RefreshTokenRepositoryTest.java |
| **Redis** | JWT Blacklist | VERIFIED | TokenBlacklistServiceTest.java |
| **Redis** | Redis 장애 내구성 (2s timeout) | VERIFIED | TS-01-REDIS_TIMEOUT.md |
| **Redis** | Redis Cluster 다중화 | PLANNED | — |
| **DTO** | Record 기반 불변 DTO | IMPLEMENTED | LoginRequest, MeResponse 등 |
| **API Response** | ApiResponse<T> 공통 포맷 | IMPLEMENTED | ApiResponse.java |
| **Exception** | GlobalExceptionHandler | IMPLEMENTED | GlobalExceptionHandler.java |
| **JPA** | @EntityGraph 활용 | IMPLEMENTED | RoleRepository, UserRepository |
| **JPA** | Fetch Join (JPQL) | IMPLEMENTED | UserRepository.findByPermissionId |
| **JPA** | N+1 방지 정량 벤치마크 수치 | PLANNED | 코드 존재, 수치 미측정 |
| **JPA** | Flyway V1~V5 마이그레이션 | IMPLEMENTED | db/migration/*.sql |
| **React** | Zustand (Access Token 상태) | IMPLEMENTED | auth.store.ts |
| **React** | React Query | IMPLEMENTED | queries/, queryClient.ts |
| **React** | Axios 인터셉터 (Single Flight) | IMPLEMENTED | http.ts |
| **React** | Protected Route 최적화 | PLANNED | task_progress Phase 2-3 |
| **Docker** | docker-compose.yml (8 services) | IMPLEMENTED | docker-compose.yml |
| **Docker** | depends_on + healthcheck | PLANNED | task_progress Phase 3-1 |
| **Nginx** | Reverse Proxy (Port 80) | VERIFIED | k6 테스트 + nginx/default.conf |
| **Nginx** | 보안 헤더 + Rate Limiting | PLANNED | task_progress Phase 3-2 |
| **DB** | MySQL 8.0 (eventdb) | IMPLEMENTED | docker-compose.yml |
| **k6** | Load/Stress/Spike/Soak Scenario | IMPLEMENTED | k6/scenarios/*.js (7종) |
| **Performance** | 70VU: 5.64ms avg, 9.98ms P95, 0% | VERIFIED | docs/performance/k6-load-test.md |
| **Performance** | 50VU: ~25ms avg, 2000 req/s | VERIFIED | docs/performance/k6-load-test.md |
| **Observability** | Prometheus + VictoriaMetrics | IMPLEMENTED | docker-compose.yml, prometheus.yml |
| **Observability** | Spring Actuator /actuator/prometheus | VERIFIED | prometheus.yml 스크랩 설정 |
| **Observability** | Grafana 대시보드 (실시간 검증) | PARTIAL | 설정 있음, 스크린샷 없음 |
| **Tests — Unit** | AuthServiceTest, AuthControllerTest | VERIFIED (파일) | test/auth/security/ |
| **Tests — Integration** | SecurityIntegrationTest, RbacSecurityIntegrationTest | VERIFIED (파일) | test/auth, test/iam |
| **Tests — Security** | TokenBlacklistServiceTest, JwtAuthenticationFilterTest | VERIFIED (파일) | test/auth/security/ |
| **Tests — Performance** | k6 시나리오 7종 | IMPLEMENTED | k6/scenarios/ |
| **Audit** | AuditService (감사 로그) | IMPLEMENTED | audit/ 패키지 |
| **Monitoring** | BodyLoggingFilter, RequestLoggingFilter | IMPLEMENTED | monitoring/ 패키지 |

---

## 6. PPT / HTML vs Source Discrepancies

### 기존 ppt.html / APMS-1.pptx에서 발견된 주의 항목

| 주장 | Source 확인 결과 | 판정 |
|------|--------------|------|
| "Lua Script 기반 1-RTT 원자적 JTI 교체" | RefreshTokenRepository.java에 Lua Script 실제 존재 | VERIFIED |
| "10 Test Suites 100% Pass" | 10개 테스트 파일 확인됨. 실행 로그 파일 미첨부 | IMPLEMENTED (실행 결과 파일 없음) |
| "Redis 장애 2초 이내 503 응답" | TS-01 문서에 기록. 실제 측정 로그 파일 없음 | DOCUMENTED |
| "Prometheus 메트릭 수집" | prometheus.yml + docker-compose.yml 확인. 스크랩 로그 없음 | IMPLEMENTED |
| "Grafana JVM 대시보드" | 컨테이너 설정만 확인. 스크린샷 없음 | PARTIAL |
| "JPA N+1 해결" | @EntityGraph 코드 존재. 정량 비교 수치 없음 | IMPLEMENTED (수치 없음) |
| k6 결과 수치 (5.64ms, 463 req/s, 0%) | docs/performance/k6-load-test.md에 기록 | VERIFIED |

### 표현 주의 항목 (과장 금지)

- `"SLA guaranteed"` → Source에서 확인되지 않음. **사용 금지.**
- `"Redis 장애 대응 완료"` → DOCUMENTED 수준. "대응 구현 완료, 장애 재현 검증 문서화" 수준으로 표현.
- `"Grafana 모니터링 완료"` → PARTIAL. "Observability 파이프라인 설정 완료, 실시간 대시보드 부분 검증" 수준으로 표현.
- k6 수치는 PPT/HTML의 기록과 Source가 일치함. 과장 없음.

---

## 7. Document Candidates

실제 Repository에 존재하는 구현 기반으로만 정의합니다. UNVERIFIED 항목 포함 금지.

| Document ID | Type | Title | Source | Readiness |
|-------------|------|-------|--------|-----------|
| `apms-auth` | FEATURE | JWT + Redis Authentication (RTR + Blacklist) | 26-05adf auth/security/ + SA-1 1-2 changelog + PR-1A1 AUTH_AND_SECURITY_SPEC | READY |
| `apms-rbac` | FEATURE | RBAC Authorization (User-Role-Permission) | 26-05adf iam/ + RbacSecurityIntegrationTest | READY |
| `apms-jpa` | TECHNICAL | JPA Query Optimization (@EntityGraph + Fetch Join) | 26-05adf iam/role,user repositories + SA-1 1-4 changelog | READY (정량 수치 없음 명시 필요) |
| `apms-api` | TECHNICAL | API Design (ApiResponse + GlobalExceptionHandler + Record DTO) | 26-05adf common/ + SA-1 1-3 changelog | READY |
| `apms-performance` | TECHNICAL | k6 Performance Verification (70VU) | 26-05adf k6/ + docs/performance/ + PR-1A1 K6_LOAD_TEST_REPORT | READY |
| `apms-infrastructure` | TECHNICAL | Docker + Nginx Infrastructure (8 containers) | 26-05adf docker-compose.yml + nginx/ + SA-1 architecture/ | READY |
| `apms-frontend-auth` | FEATURE | Frontend Auth (Zustand + bootstrapAuth + Single Flight) | 26-05adf frontend/src/auth/ + SA-1 2-1 changelog | READY |
| `apms-observability` | TECHNICAL | Observability Pipeline (Prometheus + VictoriaMetrics + Grafana) | 26-05adf monitoring/ | PARTIAL — PARTIAL 상태 명시 필요 |
| `apms-incidents` | TECHNICAL | Incident Analysis (TS-01, TS-001, TS-003) | PR-1A1 PR-Files/troubleshooting/ + 26-05adf 코드 | READY |
| `apms-overview` | LONGFORM | APMS.SR Engineering Portfolio | 위 Document 전체 기반 | AFTER OTHERS |
| `apms-presentation` | SLIDE | APMS.SR Technical Presentation (14 slides) | 위 Document 전체 기반 | AFTER OTHERS |
| `apms-audit-monitoring` | FEATURE | Audit Log + Request Monitoring | 26-05adf audit/ + monitoring/ | PARTIAL (테스트 없음) |

### Sample 1개 권장 선택

**`apms-auth` — JWT + Redis Authentication** 을 PHASE 9 Sample로 권장합니다.

이유:
- 코드, 테스트, SA-1 changelog, PR-1A1 specification이 모두 존재
- VERIFIED 수준의 Evidence가 가장 풍부
- 4개 Template (LONGFORM, FEATURE, TECHNICAL, SLIDE) 모두 적용 가능
- 프로젝트의 핵심 engineering decision을 포함 (RTR + Blacklist)

---

## 8. Evidence Candidates

실제로 존재하는 Evidence만 기록합니다. 없는 것은 NOT FOUND로 표기합니다.

| Evidence ID | Type | Claim | Source | Status |
|-------------|------|-------|--------|--------|
| `ev-auth-rtr` | TEST | RTR Lua Script 원자적 교체 | 26-05adf/test/.../RefreshTokenRepositoryTest.java | VERIFIED (파일 존재) |
| `ev-auth-blacklist` | TEST | 로그아웃 시 Blacklist 차단 | 26-05adf/test/.../TokenBlacklistServiceTest.java | VERIFIED (파일 존재) |
| `ev-auth-jwt-filter` | TEST | JWT 필터 Token Type 검증 | 26-05adf/test/.../JwtAuthenticationFilterTest.java | VERIFIED (파일 존재) |
| `ev-rbac-403` | TEST | RBAC 403 Forbidden 반환 | 26-05adf/test/.../RbacSecurityIntegrationTest.java | VERIFIED (파일 존재) |
| `ev-perf-70vu` | PERFORMANCE | 70VU: avg 5.64ms, P95 9.98ms, 463 req/s, 0% | 26-05adf/docs/performance/k6-load-test.md (5~7차) | VERIFIED (수치 문서화) |
| `ev-perf-50vu` | PERFORMANCE | 50VU: avg ~25ms, 2000+ req/s, 0% | 26-05adf/docs/performance/k6-load-test.md (2~4차) | VERIFIED (수치 문서화) |
| `ev-db-flyway` | DATABASE | V1~V5 Flyway 스키마 마이그레이션 | 26-05adf/backend/src/main/resources/db/migration/*.sql | IMPLEMENTED (파일 존재) |
| `ev-infra-nginx` | DEPLOYMENT | Nginx Port 80 단일 진입점 | 26-05adf/nginx/default.conf + docker-compose.yml | IMPLEMENTED |
| `ev-ts-redis-timeout` | LOG | Redis 장애 시 2초 이내 503 | PR-1A1/PR-Files/troubleshooting/TS-01-REDIS_TIMEOUT.md | DOCUMENTED |
| `ev-ts-jwt-loop` | LOG | JWT Refresh 무한 루프 차단 | PR-1A1/PR-Files/troubleshooting/TS-001_JWT_REFRESH_LOOP.md | DOCUMENTED |
| `ev-ts-docker-redis` | LOG | Docker 내 Redis 바인딩 해결 | PR-1A1/PR-Files/troubleshooting/TS-003_DOCKER_REDIS_BINDING.md | DOCUMENTED |
| `ev-jpa-entitygraph` | CODE | @EntityGraph N+1 방지 코드 | 26-05adf/backend/.../RoleRepository.java, UserRepository.java | IMPLEMENTED (정량 미측정) |
| `ev-frontend-bootstrap` | CODE | bootstrapAuth FOUC 제거 | 26-05adf/frontend/src/auth/auth.bootstrap.ts | IMPLEMENTED |
| `ev-grafana-dashboard` | SCREENSHOT | Grafana JVM 대시보드 시각화 | 없음 | NOT FOUND |
| `ev-k6-raw-log` | LOG | k6 원본 stdout 실행 로그 | 없음 (수치만 문서화) | NOT FOUND |
| `ev-build-test-pass` | LOG | ./gradlew test BUILD SUCCESSFUL | 없음 (changelog에 언급만) | NOT FOUND |

---

## 9. Broken Links / Invalid References

| Location | 문제 | 설명 |
|----------|------|------|
| `26-05adf/Readme.md` L17 | 링크 형식 오류 | `[URL](URL)` 패턴으로 URL이 중복 기재됨 |
| `26-05adf/Readme.md` L21 | 잘못된 경로 | `docker-compose -f dev/docker-compose.yml` — `dev/` 디렉터리 없음. 실제 경로는 root |
| `SA-1/architecture/*.md` | 중복 파일 | `26-05adf/docs/`와 내용 동일. 어느 쪽이 정본인지 불명확 |
| `PR-Files/verification/DATA_LAYER_VERIFICATION.md` | 잘못된 경로 | `dev/backend/src/...` — 실제 경로는 `backend/src/...` (`dev/` 없음) |
| `PR-1A1/PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` | 외부 링크 | Branch `feature/auth@0603@1401` 현재 유효 여부 외부 GitHub 확인 필요 |

---

## 10. Reusable Structures in PR-1A1

새 Document System 구축 시 재사용/참조 가능한 기존 자료입니다.

| Artifact | 재사용 가능한 부분 | 사용 방식 |
|----------|----------------|---------|
| `APMS-SR_CLAIM_VERIFICATION.md` | 29개 Claim-to-Evidence 매트릭스 | Document Registry의 Evidence Registry 초안으로 활용 |
| `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` | 검증된 Fact Base | 모든 Document의 Source 참조 기반 |
| `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` | Auth 기술 명세 | `apms-auth` FEATURE/TECHNICAL Document의 Source |
| `PR-Files/performance/K6_LOAD_TEST_REPORT.md` | k6 수치 + 테스트 조건 | `apms-performance` Document의 Source |
| `PR-Files/troubleshooting/TS-*.md` | 3개 장애 분석 | `apms-incidents` Document의 Source |
| `PR-Files/verification/DATA_LAYER_VERIFICATION.md` | DB + Redis Evidence (Level 1~4) | `apms-jpa` + `apms-auth` Document의 Source |
| `APMS-SR_PPT_COMPOSITION.md` | 14 Slide 구조 명세 | SLIDE Template 설계 시 참조 |
| `SA-1/changelogs/phase1_backend/1-2_*` | JWT/Redis 결정 이유 | `apms-auth` FEATURE의 "Decision" 섹션 |
| `SA-1/changelogs/phase1_backend/1-4_*` | JPA 결정 이유 | `apms-jpa` TECHNICAL의 "Decision" 섹션 |
| `SA-1/changelogs/phase2_frontend/2-1_*` | Frontend 인증 결정 이유 | `apms-frontend-auth` FEATURE의 "Decision" 섹션 |

---

## 11. Do NOT Modify

다음 파일/디렉터리는 이번 PHASE 1에서 수정하지 않았으며, 이후 작업에서도 Source of Truth 변경 없이는 임의로 수정하지 않습니다.

| Repository | Path | 이유 |
|------------|------|------|
| 26-05adf | 모든 `src/` 코드 | Source of Truth. PR-1A1에서 참조만 |
| 26-05adf | `task_progress.md` | 26-05adf 고유 작업 추적 문서 |
| 26-05adf | `docs/performance/k6-load-test.md` | Evidence Source. 수치 변경 금지 |
| SA-1 | `changelogs/phase1_backend/`, `phase2_frontend/` | Knowledge 원본. 삭제/축약 금지 |
| PR-1A1 | `APMS-SR_CLAIM_VERIFICATION.md` | 검증 결과 기록. 새 검증 없이 수정 금지 |
| PR-1A1 | `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` | Evidence 스냅샷 기준 문서 |
| PR-1A1 | `PRD-PO/html/ppt.html`, `index.html` | 기존 산출물. 새 시스템으로 대체 전 보존 |
| PR-1A1 | `APMS-1.pptx` | Reference Artifact. 수정 불필요 |

---

## 12. PHASE 2 Plan

### PHASE 2에서 할 일: SOURCE / KNOWLEDGE / PRESENTATION 경계 확정

1. **26-05adf = Implementation Source** 역할 공식 정의
   - 위치: `PR-1A1/system/BOUNDARY.md`

2. **SA-1 역할 문제 해결**
   - `SA-1/README.md` 교체: `.cursorrules` 복사본 → SA-1 역할 설명 문서
   - `SA-1/architecture/` + `26-05adf/docs/` 중복 문제 해결: Source of Truth를 26-05adf로 확정, SA-1을 참조 관계로 정리

3. **PR-1A1 Document System 기반 디렉터리 생성**
   - `PR-1A1/registry/` — Document + Evidence Registry YAML (PHASE 4)
   - `PR-1A1/content/` — Document Model (PHASE 5)
   - `PR-1A1/system/BOUNDARY.md` — 경계 확정 문서 (PHASE 2)

4. **중복 파일 처리 방침 결정**
   - SA-1/architecture/ ↔ 26-05adf/docs/ 중복 문제 → 어느 Repository가 정본인지 확정

5. **PHASE 3 Engineering Domain 목록 확정**
   - 실제 Repository 기반 최종 Domain 목록:
     - Authentication, Authorization (RBAC), Persistence (JPA), API Design, Frontend Auth, Infrastructure, Performance, Incident, Observability, Testing

---

*이 문서는 PHASE 1 Audit 결과입니다.*
*어떠한 코드, HTML, PPT, 기존 Markdown 파일도 수정하지 않았습니다.*
*생성된 파일: `PR-1A1/system/AUDIT.md` (이 파일 하나만)*
