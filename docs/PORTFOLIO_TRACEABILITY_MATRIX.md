# Portfolio Traceability Matrix

**Project:** APMS.SR — Authentication & Security Portfolio  
**Repository:** PR-1A1 (Evidence Base)  
**Source Repository:** 26-05adf (commit `9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f`, branch `feature/auth@0603@1401`)  
**AI Workflow Repository:** SA-1 (commit `4a734a8edd8b670f8d29dc2a42a978ca3877a25f`, branch `main`)  
**Last Updated:** 2026-09-05  
**Status:** FINAL QA PASS

> 💡 **Human-Friendly Explanation Guides:**
> - [PORTFOLIO_HUMAN_GUIDE.md](PORTFOLIO_HUMAN_GUIDE.md): 개발자가 스스로 이해하고 설명하기 위한 역할 중심 개인용 가이드북
> - [INTERVIEW_EXPLANATION_MAP.md](INTERVIEW_EXPLANATION_MAP.md): 30초 / 1분 / 2분 면접 질의응답 지도

---

## 1. Traceability Coverage Summary

| Domain | Claims | Evidence IDs | Status |
|--------|--------|-------------|--------|
| SECURITY (JWT/RTR/Blacklist) | CLM-SEC-001, CLM-SEC-002, CLM-SEC-003 | ev-auth-jwt-filter, ev-auth-rtr, ev-auth-blacklist | VERIFIED |
| RBAC | CLM-RBAC-001, CLM-RBAC-002 | ev-rbac-security, ev-menu-security | VERIFIED |
| PERFORMANCE | CLM-PERF-001 | ev-perf-70vu, ev-perf-50vu | VERIFIED |
| INFRASTRUCTURE | CLM-INFRA-001 | ev-infra-nginx | IMPLEMENTED |
| INCIDENT / TS | CLM-TS-001, CLM-TS-002 | ev-ts-redis-timeout, ev-ts-jwt-loop, ev-ts-docker-redis | DOCUMENTED |
| AI PROCESS | CLM-AI-001 | ev-ai-process (SA-1 changelogs) | DOCUMENTED |
| DATA / JPA | — | ev-db-flyway, ev-jpa-entitygraph | IMPLEMENTED |
| FRONTEND AUTH | — | ev-fe-bootstrap, ev-fe-single-flight | IMPLEMENTED |

---

## 2. Full Traceability Matrix

### 2.1 Security Domain — JWT / RTR / Redis Blacklist

| Slide | Claim ID | Claim (요약) | Evidence ID | Source (repo/path) | Test Method | Test Result | Status |
|-------|----------|-------------|-------------|-------------------|-------------|-------------|--------|
| 005 | CLM-SEC-001 | Stateless JWT Access Token (1h) — Bearer Header 파싱으로 API 접근 제어 | ev-auth-jwt-filter | `26-05adf/backend/.../JwtAuthenticationFilter.java` | `validAccessTokenSetsSecurityContext`, `nonAccessTokenReturnsUnauthorized` | PASS | **VERIFIED** |
| 005 | CLM-SEC-001 | JWT Payload: userId, roles, permissions 포함, JJWT HMAC-SHA256 | ev-auth-jwt-filter | `26-05adf/backend/.../JwtProvider.java` | `validAccessTokenSetsSecurityContext` | PASS | **VERIFIED** |
| 006 | CLM-SEC-002 | Refresh Token Rotation (RTR) — Lua Script 기반 JTI 원자적 교체, 구버전 즉시 401 | ev-auth-rtr | `26-05adf/backend/.../RefreshTokenRepositoryTest.java` | `rotateSuccess`, `rotateFail`, `rotateNull` | PASS | **VERIFIED** |
| 006 | CLM-SEC-003 | 로그아웃 시 Access Token → Redis Blacklist 등록, 즉시 접근 차단 | ev-auth-blacklist | `26-05adf/backend/.../TokenBlacklistServiceTest.java` | `blacklistSuccess`, `isBlacklistedReturnsTrue`, `blacklistThrowsRedisUnavailableException` | PASS | **VERIFIED** |

### 2.2 RBAC Domain

| Slide | Claim ID | Claim (요약) | Evidence ID | Source (repo/path) | Test Method | Test Result | Status |
|-------|----------|-------------|-------------|-------------------|-------------|-------------|--------|
| 007 | CLM-RBAC-001 | User-Role-Permission M:N 다단계 매핑 — 미권한 Admin 엔드포인트 접근 시 403 Forbidden | ev-rbac-security | `26-05adf/backend/.../RbacSecurityIntegrationTest.java` | `adminCanAssignPermissions`, `normalUserCannotAssignPermissions`, `unauthenticatedUserCannotAssignPermissions` | PASS | **VERIFIED** |
| 007 | CLM-RBAC-002 | Role 기반 메뉴 권한(MENU_READ) 동적 적용 — 미권한 시 403 반환 | ev-menu-security | `26-05adf/backend/.../MenuSecurityIntegrationTest.java` | `MENU_READ_권한이_있으면_메뉴를_조회할_수_있다`, `MENU_READ_권한이_없으면_메뉴_조회가_거부된다` | PASS | **VERIFIED** |

### 2.3 Performance Domain

| Slide | Claim ID | Claim (요약) | Evidence ID | Source (repo/path) | Metric | Threshold | Result | Status |
|-------|----------|-------------|-------------|-------------------|--------|-----------|--------|--------|
| 001, 010 | CLM-PERF-001 | 70 VU 1분 부하 (3회 평균): Avg 5.64ms, P95 9.98ms, 463 req/s, Error 0.00% | ev-perf-70vu | `26-05adf/docs/performance/k6-load-test.md` Section 3.2 | avg_latency=5.64ms, p95=9.98ms, rps=463, err=0.00% | p95<50ms, avg<20ms, err<1% | ALL PASS | **VERIFIED** |
| 010 | — | 50 VU 2분 지속 부하: 워밍업 후 Avg 24.30ms, P95 39.16ms, 최대 2,046 req/s | ev-perf-50vu | `26-05adf/docs/performance/k6-load-test.md` | avg=24.30ms, p95=39.16ms, rps=2046 | p95<50ms | PASS | **VERIFIED** |

### 2.4 Infrastructure Domain

| Slide | Claim ID | Claim (요약) | Evidence ID | Source (repo/path) | Verification | Status |
|-------|----------|-------------|-------------|-------------------|-------------|--------|
| 001, 003 | CLM-INFRA-001 | Nginx 단일 외부 진입점(Port 80) — Backend(8080)/DB/Redis 네트워크 격리, 리버스 프록시 라우팅 | ev-infra-nginx | `26-05adf/nginx/default.conf`, `docker-compose.yml` | Docker Compose 7서비스 토폴로지 확인, Nginx 설정 검증 | **IMPLEMENTED** |
| 003 | — | Docker Compose 7 Services: Nginx, Backend, MySQL(3307:3306), Redis(6379 내부), Prometheus(9090), VictoriaMetrics(8428), Grafana(3000) | ev-infra-nginx | `26-05adf/docker-compose.yml` | 서비스 정의 및 네트워크 격리 확인 | **IMPLEMENTED** |

### 2.5 Incident / Troubleshooting Domain

| Slide | Claim ID | Claim (요약) | Evidence ID | Source (repo/path) | Test Method | Result | Status |
|-------|----------|-------------|-------------|-------------------|-------------|--------|--------|
| 011, 013 | CLM-TS-001 | Redis 장애 시 RedisUnavailableException → 503 격리; Lettuce 커맨드 타임아웃 2초 정책 수립 | ev-ts-redis-timeout | `26-05adf/backend/.../JwtAuthenticationFilterTest.java` | `redisUnavailableReturns503` | PASS | **VERIFIED** |
| 011 | CLM-TS-002 | 토큰 갱신 실패(401) 시 클라이언트 인터셉터에서 즉시 세션 초기화 → 무한 루프 차단 | ev-ts-jwt-loop | `26-05adf/frontend/src/api/http.ts` | 코드 로직 검증 (refreshPromise Single-Flight) | IMPLEMENTED | **VERIFIED** |
| 011 | — | TS-003: Docker 환경 Redis localhost 바인딩 실패 → SPRING_REDIS_HOST 환경변수 분리 | ev-ts-docker-redis | `26-05adf/docker-compose.yml`, `application.yaml` | 컨테이너 DNS 바인딩 검증 | IMPLEMENTED | **VERIFIED** |

### 2.6 AI Process Domain

| Slide | Claim ID | Claim (요약) | Evidence ID | Source (repo/path) | Verification | Status |
|-------|----------|-------------|-------------|-------------------|-------------|--------|
| 012 | CLM-AI-001 | SA-1 8단계 AI 제어 라이프사이클 — Zero-Chatter 거버넌스로 AI 제안→엔지니어 결정→구현→검증 체계 관리 | ev-ai-process | `SA-1/conventions/rules.md`, `SA-1/changelogs/phase1_backend/1-2_jwt_redis_optimization.md` | SA-1 Commit History & Changelog Audit | **DOCUMENTED** |

### 2.7 Data / JPA Domain (미Claim, Evidence만 존재)

| Slide | Evidence ID | 설명 | Source | Status |
|-------|-------------|------|--------|--------|
| 008 | ev-db-flyway | Flyway V1~V5 마이그레이션 (init_schema → insert_test_users) | `26-05adf/backend/src/main/resources/db/migration/` | **IMPLEMENTED** |
| — | ev-jpa-entitygraph | `@EntityGraph` Fetch Join으로 User-Role-Permission 1쿼리 일괄 조회, N+1 방지 | `26-05adf/backend/.../UserRepository.java` | **IMPLEMENTED** |
| — | ev-obs-prometheus | Prometheus 15초 주기 `/actuator/prometheus` 스크레이프 | `26-05adf/monitoring/prometheus.yml` | **VERIFIED** |

### 2.8 Frontend Auth Domain (미Claim, Evidence만 존재)

| Slide | Evidence ID | 설명 | Source | Status |
|-------|-------------|------|--------|--------|
| — | ev-fe-bootstrap | 앱 마운트 시 `bootstrapAuth` 게이트웨이로 Refresh Token 검증 → FOUC/토큰 증발 방지 | `26-05adf/frontend/src/auth/auth.bootstrap.ts` | **IMPLEMENTED** |
| — | ev-fe-single-flight | 동시 401 발생 시 `refreshPromise` 싱글톤으로 갱신 요청 1개로 병합 | `26-05adf/frontend/src/api/http.ts` | **IMPLEMENTED** |

---

## 3. Presentation Slide ↔ Claim Coverage Map

| Slide # | Title | Claim ID(s) | Evidence ID(s) | Coverage |
|---------|-------|-------------|----------------|----------|
| 001 | Project Identity & Architecture Overview | CLM-PERF-001, CLM-INFRA-001 | ev-perf-70vu, ev-infra-nginx | ✅ FULL |
| 002 | Core Engineering Challenges & Objectives | CLM-SEC-001~003, CLM-INFRA-001 | ev-auth-jwt-filter, ev-infra-nginx | ✅ FULL |
| 003 | System & Container Topology | CLM-INFRA-001 | ev-infra-nginx | ✅ FULL |
| 004 | Backend Clean Architecture & DTO Isolation | — | (코드 구조, IMPLEMENTED) | ⚠️ PARTIAL (no formal Claim) |
| 005 | Authentication Architecture (JWT & Lifecycles) | CLM-SEC-001 | ev-auth-jwt-filter | ✅ FULL |
| 006 | Advanced Token Security (RTR & Redis Blacklist) | CLM-SEC-002, CLM-SEC-003 | ev-auth-rtr, ev-auth-blacklist | ✅ FULL |
| 007 | Authorization & RBAC Multi-Tier Hierarchy | CLM-RBAC-001, CLM-RBAC-002 | ev-rbac-security, ev-menu-security | ✅ FULL |
| 008 | Database Schema & Migration Governance | — | ev-db-flyway | ⚠️ PARTIAL (no formal Claim) |
| 009 | Automated Security & Integration Verification | CLM-SEC-001~003, CLM-RBAC-001~002 | ev-auth-jwt-filter, ev-auth-rtr, ev-auth-blacklist, ev-rbac-security, ev-menu-security | ✅ FULL |
| 010 | Performance & Stress Testing (k6 Benchmarks) | CLM-PERF-001 | ev-perf-70vu, ev-perf-50vu | ✅ FULL |
| 011 | Real-World Incident Troubleshooting | CLM-TS-001, CLM-TS-002 | ev-ts-redis-timeout, ev-ts-jwt-loop, ev-ts-docker-redis | ✅ FULL |
| 012 | Controlled AI Workflow (SA-1 Governance) | CLM-AI-001 | SA-1 changelogs | ✅ FULL |
| 013 | Architectural Decisions & Trade-offs | CLM-SEC-001~003, CLM-TS-001 | ev-auth-jwt-filter, ev-ts-redis-timeout | ✅ FULL |
| 014 | System Limitations & Future Roadmap | — | (PLANNED, 의도적 미Claim) | ✅ CORRECT (PLANNED 격리) |
| 015 | Conclusion & Engineering Identity | ALL | ALL | ✅ FULL |

> **주의:** Slide 004(Clean Architecture)와 Slide 008(Flyway)는 핵심 기술 주장이 아닌 구현 설명 슬라이드로, 공식 Claim이 없음. 과장된 검증 주장 없이 `[IMPLEMENTED]`로만 표기 — **의도적 설계**.

---

## 4. Unverified / PLANNED Isolation

아래 항목은 의도적으로 VERIFIED 상태에서 제외되며, 인터뷰에서 "미보유" 사실을 명확히 답변해야 한다.

| Evidence ID | 내용 | 상태 | 이유 |
|-------------|------|------|------|
| unev-jpa-n1-benchmark | JPA N+1 Fetch Join 전후 쿼리 수 비교 측정치 | PLANNED | 코드 최적화는 완료, before/after 벤치마크 수치 미보유 |
| unev-grafana-live-dashboard | Grafana 실시간 대시보드 스크린샷 및 알람 증거 | PARTIAL | Grafana 컨테이너 설정 존재, 라이브 스크린샷 미확보 |
| unev-k6-raw-log-file | k6 CLI 실행 원본 stdout 로그 파일 | NOT_FOUND | docs/performance/k6-load-test.md 에 결과 기록됨 (원본 파일 별도 보관 없음) |

---

## 5. AI Process Traceability (SA-1 → 26-05adf → PR-1A1)

```
SA-1 (거버넌스 정의)
  └── conventions/rules.md          ← Zero-Chatter, Documentation-First 원칙 정의
  └── changelogs/phase1_backend/    ← 각 Phase 구현 결정 기록
       ├── 1-2_jwt_redis_optimization.md  (JWT+Redis 설계 결정)
       ├── 1-4_jpa_n1_query_optimization.md (EntityGraph 결정)
       └── phase2_frontend/
           └── 2-1_zustand_auth_optimization.md (Frontend Auth 결정)

26-05adf (구현)
  └── commit 9e6ef83d  ← 실제 코드 구현 (JwtProvider, JwtAuthenticationFilter,
                          TokenBlacklistService, RefreshTokenRepository 등)
  └── test/            ← JUnit5 단위/통합 테스트 10종 (100% PASS)
  └── docs/performance/ ← k6 결과 문서

PR-1A1 (포트폴리오 증거)
  └── PR-Files/evidence/claims/   ← 10개 Claim JSON
  └── registry/evidence.yaml      ← Evidence Registry
  └── PRD-PO/case-study/          ← CASE_STUDY.md (공학적 결정 기록)
  └── PRD-PO/presentation/        ← 15-Slide Presentation
  └── docs/PORTFOLIO_TRACEABILITY_MATRIX.md (본 문서)
```

**AI 제안 → 엔지니어 결정 구조 유지 원칙:**
- AI가 제안한 모든 코드 변경은 `task_progress.md`에 사전 정의 후 승인
- 구현 완료 후 JUnit / k6 검증이 100% 통과해야 커밋 허용
- 결과는 `SA-1/changelogs/`에 엔지니어가 직접 기록
- AI가 모든 결정을 한 것처럼 표현하지 않음 — AI는 도구, 결정은 엔지니어

---

## 6. Claim Status Legend

| Status | 의미 |
|--------|------|
| **VERIFIED** | 자동화 테스트 (JUnit / k6) 로 수치 검증 완료 |
| **IMPLEMENTED** | 코드/설정 존재 확인, 자동화 테스트 없음 |
| **DOCUMENTED** | 설계 문서/거버넌스 기록으로 추적, 자동화 검증 없음 |
| **PLANNED** | 계획만 존재, 미구현/미측정 — 인터뷰에서 명확히 구분 |
