# Engineering Domain Classification & Traceability Matrix

- **Document ID:** APMS-SR-SYS-DOMAIN-01
- **Target Repository:** `PR-1A1`
- **Created Date:** 2026-08-29
- **Phase:** PHASE 3 — Engineering Domain Classification
- **Status:** ACTIVE

---

## 1. Overview & Classification Protocol

본 문서는 `26-05adf` (실제 구현/테스트)와 `SA-1` (엔지니어링 지식)의 실측 사실을 기반으로 `APMS.SR` 시스템의 공학적 도메인을 체계적으로 분류한 명세입니다.
모든 도메인은 **추측이나 과장 없이 실제 소스 코드, 테스트, 장애 분석 및 실측 지표가 존재하는 영역만**으로 구성됩니다.

### Status Tagging Protocol
- `[VERIFIED]`: 단위/통합 테스트 또는 실측 부하 테스트로 검증 완료된 상태.
- `[IMPLEMENTED]`: 소스 코드가 실제로 작성되어 있으나 정량 검증 지표가 분리된 상태.
- `[DOCUMENTED]`: 장애 분석, 규격서, 아키텍처 문서로 검증 체계가 수립된 상태.
- `[PARTIAL]`: 일부 인프라나 대시보드가 구성되어 있으나 실시간 검증이 부분적인 상태.
- `[PLANNED]`: 향후 로드맵 과제로 분류되어 기정사실화가 금지된 상태.

---

## 2. Classified Engineering Domains (10 Core Domains)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          APMS.SR 10 Core Domains                            │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│  1. Authentication   │  2. Authorization    │  3. Persistence (JPA/DB)      │
│  (JWT/RTR/Blacklist) │  (RBAC M:N Model)    │  (@EntityGraph / Flyway)      │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│  4. API Architecture │  5. Frontend Auth    │  6. Infrastructure & Network  │
│  (DTO/Global Handler)│  (Zustand/SingleFlgt)│  (Nginx/Docker Isolation)     │
├──────────────────────┼──────────────────────┼───────────────────────────────┤
│  7. Performance      │  8. Troubleshooting  │  9. Observability Pipeline    │
│  (k6 70 VU Benchmark)│  (TS 6-Step Defense) │  (Prometheus/Actuator)        │
├──────────────────────┴──────────────────────┴───────────────────────────────┤
│  10. Automated Testing Strategy (Unit/Integration/Security 10 Suites)       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### DOMAIN 01: Authentication (인증 및 토큰 라이프사이클)
- **Domain ID:** `DOM-AUTH`
- **책임:** 무상태(Stateless) JWT Access Token 발급, HttpOnly Secure Cookie 기반 Refresh Token Rotation(RTR), Redis In-Memory Blacklist를 통한 즉시 세션 무효화
- **26-05adf Source:**
  - `backend/src/main/java/com/example/demo/auth/jwt/JwtProvider.java`
  - `backend/src/main/java/com/example/demo/auth/security/AuthController.java`
  - `backend/src/main/java/com/example/demo/auth/security/AuthService.java`
  - `backend/src/main/java/com/example/demo/auth/security/JwtAuthenticationFilter.java`
  - `backend/src/main/java/com/example/demo/auth/security/RefreshTokenRepository.java` (Lua Script)
  - `backend/src/main/java/com/example/demo/auth/security/TokenBlacklistService.java`
- **SA-1 Knowledge:**
  - `changelogs/phase1_backend/1-2_jwt_redis_optimization.md` (JwtParser 캐싱, DataAccessException 처리, Token Type 검증 배경)
- **Verification Evidence:**
  - `backend/src/test/java/com/example/demo/auth/security/JwtAuthenticationFilterTest.java` `[VERIFIED]`
  - `backend/src/test/java/com/example/demo/auth/security/RefreshTokenRepositoryTest.java` `[VERIFIED]`
  - `backend/src/test/java/com/example/demo/auth/security/TokenBlacklistServiceTest.java` `[VERIFIED]`
  - `backend/src/test/java/com/example/demo/auth/security/SecurityIntegrationTest.java` `[VERIFIED]`
- **Document Mapping:** `apms-auth` (FEATURE, TECHNICAL, SLIDE, LONGFORM)

---

### DOMAIN 02: Authorization & RBAC (역할 기반 인가)
- **Domain ID:** `DOM-RBAC`
- **책임:** `User - Role - Permission` M:N 다대다 정규화 모델 구축 및 Spring Security 필터 체인을 통한 세부 엔드포인트 접근 제어
- **26-05adf Source:**
  - `backend/src/main/java/com/example/demo/auth/security/UserAuthorityService.java`
  - `backend/src/main/java/com/example/demo/auth/security/SecurityConfig.java`
  - `backend/src/main/java/com/example/demo/iam/user/domain/User.java`
  - `backend/src/main/java/com/example/demo/iam/role/domain/Role.java`
  - `backend/src/main/java/com/example/demo/iam/permission/domain/Permission.java`
  - `backend/src/main/java/com/example/demo/iam/menu/domain/Menu.java`
  - `backend/src/main/resources/db/migration/V2__init_authority_schema.sql`
- **SA-1 Knowledge:**
  - `architecture/01_Architecture_and_Ports.md`
- **Verification Evidence:**
  - `backend/src/test/java/com/example/demo/iam/rbac/RbacSecurityIntegrationTest.java` `[VERIFIED]`
  - `backend/src/test/java/com/example/demo/iam/permission/PermissionIntegrationTest.java` `[VERIFIED]`
  - `backend/src/test/java/com/example/demo/iam/role/RolePermissionIntegrationTest.java` `[VERIFIED]`
  - `backend/src/test/java/com/example/demo/menu/MenuSecurityIntegrationTest.java` `[VERIFIED]`
- **Document Mapping:** `apms-rbac` (FEATURE, TECHNICAL)

---

### DOMAIN 03: Persistence & Database (데이터 영속성 및 최적화)
- **Domain ID:** `DOM-DATA`
- **책임:** Flyway를 통한 DB 스키마 형상 관리, JPA `@EntityGraph` 및 JPQL `Fetch Join`을 통한 지연 로딩 최적화 및 N+1 쿼리 병목 예방
- **26-05adf Source:**
  - `backend/src/main/resources/db/migration/V1__init_schema.sql` ~ `V5__insert_test_users.sql`
  - `backend/src/main/java/com/example/demo/iam/user/repository/UserRepository.java`
  - `backend/src/main/java/com/example/demo/iam/role/repository/RoleRepository.java`
  - `backend/src/main/java/com/example/demo/iam/permission/repository/PermissionRepository.java`
  - `backend/src/main/java/com/example/demo/config/JpaConfig.java`
- **SA-1 Knowledge:**
  - `changelogs/phase1_backend/1-4_jpa_n1_query_optimization.md` (@EntityGraph 적용 결정 이유, Set<T> 기반 카테시안 곱 방지)
- **Verification Evidence:**
  - `PR-Files/verification/DATA_LAYER_VERIFICATION.md` `[DOCUMENTED]`
  - Flyway 마이그레이션 적용 및 Composite PK/FK 무결성 `[IMPLEMENTED]`
  - JPA N+1 정량 벤치마크 수치 `[PLANNED]`
- **Document Mapping:** `apms-jpa` (TECHNICAL, EVIDENCE)

---

### DOMAIN 04: Backend API Architecture (응답 및 예외 체계)
- **Domain ID:** `DOM-API`
- **책임:** 불변 Record 기반 DTO 설계, `ApiResponse<T>` 통일 응답 래퍼, `GlobalExceptionHandler` 전역 예외 처리
- **26-05adf Source:**
  - `backend/src/main/java/com/example/demo/common/dto/ApiResponse.java`
  - `backend/src/main/java/com/example/demo/common/exception/GlobalExceptionHandler.java`
  - `backend/src/main/java/com/example/demo/iam/user/dto/LoginRequest.java` 등 Record DTO
- **SA-1 Knowledge:**
  - `changelogs/phase1_backend/1-1. Entity와 DTO의 엄격한 분리.md`
  - `changelogs/phase1_backend/1-3_global_response_exception_handling.md`
  - `conventions/03_Backend_Conventions.md`
- **Verification Evidence:**
  - `backend/src/test/java/com/example/demo/auth/security/AuthControllerTest.java` `[VERIFIED]`
- **Document Mapping:** `apms-api` (TECHNICAL)

---

### DOMAIN 05: Frontend Auth & State Management (클라이언트 인증 상태)
- **Domain ID:** `DOM-FE-AUTH`
- **책임:** Zustand 기반 Access Token 상태 관리(`persist`), `bootstrapAuth` 게이트웨이 패턴(FOUC 방지), Single Flight 재발급(`refreshPromise`)
- **26-05adf Source:**
  - `frontend/src/store/auth.store.ts`
  - `frontend/src/auth/auth.bootstrap.ts`
  - `frontend/src/api/http.ts`
  - `frontend/src/App.tsx`
- **SA-1 Knowledge:**
  - `changelogs/phase2_frontend/2-1_zustand_auth_optimization.md`
- **Verification Evidence:**
  - `PR-Files/troubleshooting/TS-001_JWT_REFRESH_LOOP.md` `[DOCUMENTED]`
  - Single Flight 및 503 완화 로직 `[IMPLEMENTED]`
- **Document Mapping:** `apms-frontend-auth` (FEATURE, TECHNICAL)

---

### DOMAIN 06: Infrastructure & Network Topology (컨테이너 인프라)
- **Domain ID:** `DOM-INFRA`
- **책임:** Docker Compose 기반 8개 서비스 오케스트레이션, Nginx Reverse Proxy 단일 진입점(Port 80) 및 브리지 네트워크 격리
- **26-05adf Source:**
  - `docker-compose.yml`
  - `nginx/Dockerfile`, `nginx/default.conf`
  - `backend/Dockerfile`, `frontend/Dockerfile`
- **SA-1 Knowledge:**
  - `architecture/01_Architecture_and_Ports.md`
  - `architecture/02_Quick_Start.md`
- **Verification Evidence:**
  - `PR-Files/architecture/ARCHITECTURE_SPEC.md` `[DOCUMENTED]`
  - Nginx 라우팅 및 Docker 서비스 간 통신 `[IMPLEMENTED]`
  - depends_on / healthcheck / Rate Limiting `[PLANNED]`
- **Document Mapping:** `apms-infrastructure` (TECHNICAL)

---

### DOMAIN 07: Performance & Load Testing (부하 검증 및 지표)
- **Domain ID:** `DOM-PERF`
- **책임:** k6 기반 부하 테스트 수행, 70 VU 동시 접속 환경에서의 Throughput, Latency, Error Rate 실측 및 임계치 검증
- **26-05adf Source:**
  - `k6/scenarios/load.test.js`, `k6/scenarios/stress.test.js` 등 7종 시나리오
  - `k6/config/thresholds.js`
  - `docs/performance/k6-load-test.md`
- **SA-1 Knowledge:**
  - 인프라 부하 시나리오 규격
- **Verification Evidence:**
  - **70 VU (1m) 실측치:** Throughput `463 req/s`, Avg `5.64 ms`, P95 `9.98 ms`, Error `0.00%` `[VERIFIED]`
  - **50 VU (2m) 실측치:** Throughput `2,046 req/s`, Avg `24.30 ms`, P95 `39.16 ms`, Error `0.00%` `[VERIFIED]`
  - `PR-Files/performance/K6_LOAD_TEST_REPORT.md` `[VERIFIED]`
- **Document Mapping:** `apms-performance` (TECHNICAL, EVIDENCE)

---

### DOMAIN 08: Incident & Troubleshooting (장애 분석 및 복구)
- **Domain ID:** `DOM-INCIDENT`
- **책임:** 6단계 표준 절차(`Symptom → Impact → Diagnosis → Root Cause → Resolution → Prevention`)에 기반한 장애 대응
- **26-05adf Source / Fix:**
  - TS-01: `application.yaml` Lettuce 타임아웃 2초 단축 및 503 예외 래핑
  - TS-001: `frontend/src/api/http.ts` 재발급 401 즉시 탈출 조건 및 세션 초기화
  - TS-003: `docker-compose.yml`, `application.yaml` Redis host 환경변수(`redis:6379`) 분리
- **SA-1 Knowledge:**
  - 장애 분석 템플릿 및 재발 방지 컨벤션
- **Verification Evidence:**
  - `PR-Files/troubleshooting/TS-01-REDIS_TIMEOUT.md` `[DOCUMENTED]`
  - `PR-Files/troubleshooting/TS-001_JWT_REFRESH_LOOP.md` `[DOCUMENTED]`
  - `PR-Files/troubleshooting/TS-003_DOCKER_REDIS_BINDING.md` `[DOCUMENTED]`
- **Document Mapping:** `apms-incidents` (TECHNICAL, EVIDENCE)

---

### DOMAIN 09: Observability Pipeline (모니터링)
- **Domain ID:** `DOM-OBS`
- **책임:** Spring Boot Actuator 메트릭 노출, Prometheus + VictoriaMetrics 수집 및 Grafana 시각화 파이프라인
- **26-05adf Source:**
  - `monitoring/prometheus.yml`, `monitoring/agent.yaml`
  - `backend/src/main/java/com/example/demo/monitoring/`
  - `docker-compose.yml`
- **SA-1 Knowledge:**
  - `pkm&infra/infra/Dash보드.json`
- **Verification Evidence:**
  - `/actuator/prometheus` 엔드포인트 스크랩 `[VERIFIED]`
  - VictoriaMetrics 영속 스토리지 연동 `[IMPLEMENTED]`
  - Grafana 실시간 대시보드 검증 `[PARTIAL]` (스크린샷 증거 미확보)
- **Document Mapping:** `apms-observability` (TECHNICAL)

---

### DOMAIN 10: Automated Testing Strategy (테스트 스위트)
- **Domain ID:** `DOM-TEST`
- **책임:** 단위, 통합, 보안 인가 계층에 대한 10종 자동화 테스트 스위트 구축 및 회귀 방지
- **26-05adf Source:**
  - `backend/src/test/java/com/example/demo/auth/security/` (6 classes)
  - `backend/src/test/java/com/example/demo/iam/` (3 classes)
  - `backend/src/test/java/com/example/demo/menu/` (1 class)
- **SA-1 Knowledge:**
  - `changelogs/phase1_backend/` 테스트 통과 기록
- **Verification Evidence:**
  - `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md` `[DOCUMENTED]`
  - 10개 테스트 클래스 소스 코드 `[VERIFIED]`
- **Document Mapping:** `apms-testing` (TECHNICAL, EVIDENCE)

---

## 3. Domain-to-Document Mapping Summary

| Domain ID | Main Feature / Topic | Status | Recommended Template Types |
|:---|:---|:---:|:---|
| `DOM-AUTH` | JWT + Redis Token Lifecycle (RTR, Blacklist) | `[VERIFIED]` | `FEATURE`, `TECHNICAL`, `SLIDE`, `LONGFORM` |
| `DOM-RBAC` | User-Role-Permission M:N Authorization | `[VERIFIED]` | `FEATURE`, `TECHNICAL` |
| `DOM-DATA` | JPA @EntityGraph & Flyway Schema Integrity | `[IMPLEMENTED]` | `TECHNICAL`, `EVIDENCE` |
| `DOM-API` | Record DTO & Global Exception Handling | `[IMPLEMENTED]` | `TECHNICAL` |
| `DOM-FE-AUTH`| Zustand Store & Single Flight Refresh | `[IMPLEMENTED]` | `FEATURE`, `TECHNICAL` |
| `DOM-INFRA` | Docker 8-Service Topology & Nginx Gateway | `[IMPLEMENTED]` | `TECHNICAL` |
| `DOM-PERF` | k6 70 VU / 50 VU Benchmark Fact | `[VERIFIED]` | `TECHNICAL`, `EVIDENCE`, `SLIDE` |
| `DOM-INCIDENT`| TS-01, TS-001, TS-003 Incident Defense | `[DOCUMENTED]` | `TECHNICAL`, `EVIDENCE` |
| `DOM-OBS` | Prometheus / VictoriaMetrics Pipeline | `[PARTIAL]` | `TECHNICAL` |
| `DOM-TEST` | 10 Automated Test Suites | `[VERIFIED]` | `TECHNICAL`, `EVIDENCE` |

---

*본 도메인 분류 명세는 PHASE 4 Document Registry(`documents.yaml`, `evidence.yaml`) 구축의 기준 구조로 사용됩니다.*
