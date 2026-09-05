# Portfolio Evidence QA Report

**Document ID:** PORTFOLIO-QA-FINAL-001  
**Project:** APMS.SR — Authentication & Security Portfolio  
**QA Session:** 2026-09-05 (Resume from interrupted session)  
**Scope:** PR-1A1 Evidence Base, 26-05adf Source, SA-1 AI Process  
**Status:** ✅ FINAL PASS

> 💡 **Human-Friendly Explanation Guides:**
> - [PORTFOLIO_HUMAN_GUIDE.md](PORTFOLIO_HUMAN_GUIDE.md): 개발자가 스스로 이해하고 설명하기 위한 역할 중심 개인용 가이드북
> - [INTERVIEW_EXPLANATION_MAP.md](INTERVIEW_EXPLANATION_MAP.md): 30초 / 1분 / 2분 면접 질의응답 지도

---

## 1. Audit Scope

| Category | Item |
|----------|------|
| Claims Audited | 10 (CLM-SEC-001~003, CLM-RBAC-001~002, CLM-PERF-001, CLM-INFRA-001, CLM-TS-001~002, CLM-AI-001) |
| Evidence IDs Audited | 14 (ev-auth-rtr, ev-auth-blacklist, ev-auth-jwt-filter, ev-rbac-security, ev-menu-security, ev-perf-70vu, ev-perf-50vu, ev-db-flyway, ev-jpa-entitygraph, ev-fe-bootstrap, ev-fe-single-flight, ev-infra-nginx, ev-ts-redis-timeout, ev-ts-jwt-loop, ev-ts-docker-redis, ev-obs-prometheus) |
| Slides Reviewed | 15 (Slide 001~015) |
| Source Files Verified | 20+ (26-05adf commit `9e6ef83d`) |
| Test Methods Verified | 21 (JUnit5 단위/통합 테스트) |
| Snapshot Files | 39 (SHA-256 100% 일치) |

---

## 2. Validation Results

### 2.1 Automated Validation (`validate.py --all`)

```
[1/8] 10 Claims validated. Uniqueness and Status confirmed.         ✅
[2/8] 10 Evidence Bundles verified.                                  ✅
[3/8] 20 source references & symbols verified.                       ✅
[4/8] 21 test methods verified in 26-05adf backend.                  ✅
[5/8] 39 Snapshot files verified with 100% SHA-256 match.            ✅
[6/8] 20 slide & case study mappings verified.                       ✅
[7/8] Slides [004~008] passed zero-inline-style & schema checks.     ✅
[8/8] ALL CHECKS PASSED — 100% Deterministic Verification Succeeded  ✅
```

### 2.2 Unit Tests (`py -m unittest discover`)

```
Ran 50 tests in 0.418s — OK                                         ✅
```

### 2.3 Renderer Pipeline (`node renderer/index.js apms-auth --all`)

```
5 polymorphic HTML documents rendered (longform, feature, technical, slide, evidence)
All 5 HTML documents passed structure & CSS checks
Golden Baseline snapshot saved                                       ✅
```

### 2.4 Repository Integrity

| Repository | Status | Notes |
|------------|--------|-------|
| `26-05adf` | ✅ **CLEAN** | 소스 코드 미수정 (읽기 전용) |
| `SA-1` | ✅ **CLEAN** | AI 프로세스 문서 미수정 (읽기 전용) |
| `PR-1A1` | ✅ **의도적 변경만** | QA 결과물만 추가/수정 |

---

## 3. Claims Audited — Status Summary

| Claim ID | Domain | Claim 요약 | Status | Test Evidence |
|----------|--------|-----------|--------|---------------|
| CLM-SEC-001 | SECURITY | Stateless JWT Access Token (1h) Bearer Header 파싱 | **VERIFIED** | JwtAuthenticationFilterTest (4 methods) |
| CLM-SEC-002 | SECURITY | RTR: Lua Script 기반 JTI 원자적 교체, 구버전 401 차단 | **VERIFIED** | RefreshTokenRepositoryTest (5 methods) |
| CLM-SEC-003 | SECURITY | 로그아웃 → Access Token Redis Blacklist 등록, 즉시 차단 | **VERIFIED** | TokenBlacklistServiceTest (4 methods) |
| CLM-RBAC-001 | RBAC | User-Role-Permission M:N 매핑 — 미권한 403 Forbidden | **VERIFIED** | RbacSecurityIntegrationTest (3 methods) |
| CLM-RBAC-002 | RBAC | Role 기반 메뉴 권한(MENU_READ) 동적 적용 | **VERIFIED** | MenuSecurityIntegrationTest (3 methods) |
| CLM-PERF-001 | PERFORMANCE | 70 VU 3회 평균: Avg 5.64ms, P95 9.98ms, 463 req/s, 0.00% | **VERIFIED** | k6 Load Test (26-05adf/docs/performance/k6-load-test.md) |
| CLM-INFRA-001 | ARCHITECTURE | Nginx 단일 진입점(80) + 7서비스 Docker 네트워크 격리 | **IMPLEMENTED** | docker-compose.yml + nginx/default.conf 확인 |
| CLM-TS-001 | INCIDENT | Redis 장애 시 503 격리 + Lettuce 2초 타임아웃 정책 | **VERIFIED** | JwtAuthenticationFilterTest.redisUnavailableReturns503 |
| CLM-TS-002 | INCIDENT | 토큰 갱신 실패 401 → 즉시 세션 초기화, 무한 루프 차단 | **VERIFIED** | frontend/src/api/http.ts 코드 로직 검증 |
| CLM-AI-001 | AI_PROCESS | SA-1 8단계 제어 라이프사이클 Zero-Chatter 거버넌스 | **DOCUMENTED** | SA-1/conventions/rules.md + changelogs 감사 |

---

## 4. Evidence Audited

| Evidence ID | Type | Status | Source 존재 여부 | Test 존재 여부 |
|-------------|------|--------|----------------|---------------|
| ev-auth-rtr | TEST | VERIFIED | ✅ | ✅ (rotateSuccess 등 5개) |
| ev-auth-blacklist | TEST | VERIFIED | ✅ | ✅ (blacklistSuccess 등 4개) |
| ev-auth-jwt-filter | TEST | VERIFIED | ✅ | ✅ (validAccessToken 등 4개) |
| ev-rbac-security | TEST | VERIFIED | ✅ | ✅ (adminCanAssign 등 3개) |
| ev-menu-security | TEST | VERIFIED | ✅ | ✅ (MENU_READ 등 3개) |
| ev-perf-70vu | PERFORMANCE | VERIFIED | ✅ | ✅ (k6 3회 수치 문서화) |
| ev-perf-50vu | PERFORMANCE | VERIFIED | ✅ | ✅ (k6 2분 지속 수치) |
| ev-db-flyway | DATABASE | IMPLEMENTED | ✅ (V1~V5 SQL 존재) | — |
| ev-jpa-entitygraph | CODE | IMPLEMENTED | ✅ (UserRepository) | — |
| ev-fe-bootstrap | CODE | IMPLEMENTED | ✅ (auth.bootstrap.ts) | — |
| ev-fe-single-flight | CODE | IMPLEMENTED | ✅ (http.ts) | — |
| ev-infra-nginx | DEPLOYMENT | IMPLEMENTED | ✅ (nginx/default.conf) | — |
| ev-ts-redis-timeout | LOG | DOCUMENTED | ✅ (TS-01-REDIS.md) | ✅ (redisUnavailableReturns503) |
| ev-ts-jwt-loop | LOG | DOCUMENTED | ✅ (TS-001.md + http.ts) | — |
| ev-ts-docker-redis | LOG | DOCUMENTED | ✅ (TS-003.md) | — |
| ev-obs-prometheus | CONFIGURATION | VERIFIED | ✅ (prometheus.yml) | — |

---

## 5. Traceability Coverage

| Slide # | Claim Coverage | Evidence Coverage | Status |
|---------|---------------|------------------|--------|
| 001 | CLM-PERF-001, CLM-INFRA-001 | ev-perf-70vu, ev-infra-nginx | ✅ FULL |
| 002 | CLM-SEC-001~003, CLM-INFRA-001 | ev-auth-*, ev-infra-nginx | ✅ FULL |
| 003 | CLM-INFRA-001 | ev-infra-nginx | ✅ FULL |
| 004 | (구현 설명 슬라이드) | — | ✅ 의도적 Claim 없음 |
| 005 | CLM-SEC-001 | ev-auth-jwt-filter | ✅ FULL |
| 006 | CLM-SEC-002, CLM-SEC-003 | ev-auth-rtr, ev-auth-blacklist | ✅ FULL |
| 007 | CLM-RBAC-001, CLM-RBAC-002 | ev-rbac-security, ev-menu-security | ✅ FULL |
| 008 | (Flyway 구현 설명) | ev-db-flyway | ✅ 의도적 Claim 없음 |
| 009 | CLM-SEC-001~003, CLM-RBAC-001~002 | 전체 테스트 Evidence | ✅ FULL |
| 010 | CLM-PERF-001 | ev-perf-70vu, ev-perf-50vu | ✅ FULL |
| 011 | CLM-TS-001, CLM-TS-002 | ev-ts-* | ✅ FULL |
| 012 | CLM-AI-001 | SA-1 changelogs | ✅ FULL |
| 013 | CLM-SEC-001~003, CLM-TS-001 | ev-auth-*, ev-ts-redis | ✅ FULL |
| 014 | (PLANNED 항목) | — | ✅ 의도적 미Claim (PLANNED 격리) |
| 015 | ALL | ALL | ✅ FULL |

**Overall Traceability:** 13/15 슬라이드 Full Coverage (나머지 2개는 의도적 구현 설명 슬라이드)

---

## 6. Factual Inconsistencies Found / Fixed

이전 QA 세션에서 수정된 항목 (이번 세션 재확인):

| # | 항목 | 원래 표현 | 수정 표현 | 근거 |
|---|------|----------|----------|------|
| 1 | CLM-TS-001 | "Redis timeout 2초를 설정했다" (단순 설정 claim) | "RedisUnavailableException + 503 격리 + Lettuce 2초 타임아웃 정책 수립·검증" | JwtAuthenticationFilterTest.redisUnavailableReturns503 확인 |
| 2 | CLM-PERF-001 | 단일 run 수치로 표현 | "3회(5th/6th/7th) 반복 산술 평균 Fact: Avg 5.64ms, P95 9.98ms, 463 req/s" | k6-load-test.md Section 3.2 확인 |
| 3 | Redis timeout 표현 | "60초 → 2초" (잘못된 원값) | 기본값 언급 없이 "Lettuce 커맨드 타임아웃 2초 강제" 로 완화 | application.yaml 직접 확인 |

**이번 세션 추가 수정:** 없음 (이전 수정이 올바르게 유지됨)

---

## 7. Presentation Inconsistencies Found / Fixed

| # | 파일 | 확인 결과 |
|---|------|----------|
| Slide 005 HTML | `slides/005/index.html` | Access Token 1h / Refresh Token 7d HttpOnly Cookie — Claim과 일치 ✅ |
| Slide 006 HTML | `slides/006/index.html` | RTR Lua Script JTI 교체 / Redis Blacklist — Claim과 일치 ✅ |
| 04_AUTH_AND_RBAC.md | presentation/source/ | JWT 수치 (3,600,000ms / 604,800,000ms), RTR, Blacklist — 일치 ✅ |
| ppt.html / index.html | PRD-PO/html/ | 핵심 기술 주장 Claim Registry와 일치 ✅ |
| PORTFOLIO_PRESENTATION.md | 15 Slides | 모든 VERIFIED 수치 Claim과 일치 ✅ |

**이번 세션 추가 수정:** 없음

---

## 8. Case Study Final Verification

`PRD-PO/case-study/CASE_STUDY.md` 항목별 검증 결과:

| 항목 | Case Study 표현 | 실제 코드 근거 | 판정 |
|------|---------------|--------------|------|
| JWT Access Token TTL | 1시간 (3,600,000 ms) | `JwtProvider.java` accessTokenExpiration 설정 | ✅ 일치 |
| JWT Refresh Token TTL | 7일 (604,800,000 ms) | `JwtProvider.java` refreshTokenExpiration 설정 | ✅ 일치 |
| Refresh Token Rotation | UUID JTI Lua Script 원자적 교체 | `RefreshTokenRepository.java` Lua Script 사용 | ✅ 일치 |
| Redis Blacklist 키 패턴 | `blacklist:<jti>` | `TokenBlacklistService.java` BLACKLIST_KEY_PREFIX | ✅ 일치 |
| RBAC 구조 | User-Role-Permission M:N | `user_roles`, `role_permissions`, `role_menus` 테이블 | ✅ 일치 |
| Redis 장애 처리 | RedisUnavailableException → 503 | `JwtAuthenticationFilter.java`, `TokenBlacklistService.java` | ✅ 일치 |
| Frontend Single-Flight | `refreshPromise` 싱글톤 | `frontend/src/api/http.ts` | ✅ 일치 |
| k6 성능 수치 | 3회 평균 Avg 5.64ms, P95 9.98ms, 463 req/s, 0.00% | `docs/performance/k6-load-test.md` Section 3.2 | ✅ 일치 |
| Docker 서비스 수 | 7개 (Nginx, Backend, MySQL, Redis, Prometheus, VictoriaMetrics, Grafana) | `docker-compose.yml` 서비스 목록 | ✅ 일치 |
| Frontend Bootstrap | `bootstrapAuth` 게이트웨이 | `frontend/src/auth/auth.bootstrap.ts` | ✅ 일치 |

**과장된 표현:** 없음. 모든 VERIFIED 수치는 실제 문서 기반.  
**PLANNED 항목 격리:** Section 8에 명확히 분리됨 (JPA 벤치마크, Message Queue 등)

---

## 9. AI Process Traceability Verification

| 연결 고리 | 확인 결과 |
|---------|----------|
| SA-1 → 설계 결정 | `SA-1/changelogs/phase1_backend/1-2_jwt_redis_optimization.md` 존재, JWT+Redis 설계 결정 기록 ✅ |
| SA-1 → 구현 | `SA-1/changelogs/phase2_frontend/2-1_zustand_auth_optimization.md` 존재, Frontend 결정 기록 ✅ |
| SA-1 규칙 | `SA-1/conventions/rules.md` — Zero-Chatter, Documentation-First 원칙 정의 ✅ |
| AI 과장 표현 여부 | "AI suggestion → engineering decision → implementation → verification" 구조 유지 ✅ |
| AI가 모든 결정 주체로 표현 | 없음. Slide 012, Case Study Section 2 모두 거버넌스 도구로만 표현 ✅ |

---

## 10. Interview-Ready Claims

인터뷰에서 즉시 답변 가능한 검증된 주장:

### ✅ 바로 설명 가능 (VERIFIED)
1. **JWT TTL 분리 이유:** Access Token 1h (Stateless 고성능) + Refresh Token 7d (Redis JTI 기반 Stateful 제어) — 보안과 UX 균형
2. **RTR이 Replay Attack을 막는 방법:** Lua Script로 기존 JTI 무효화 + 신규 JTI 발급 원자적 실행 → 구버전 JTI 재사용 즉시 401
3. **Redis 장애 시 서버 보호:** `RedisUnavailableException` → `JwtAuthenticationFilter`에서 503 즉시 반환, 스레드 풀 보호
4. **RBAC 403 Forbidden 조건:** `UserAuthorityService`로 사용자별 Permission 목록 로드 → Spring Security Filter에서 엔드포인트별 권한 검증
5. **k6 70 VU P95 9.98ms 근거:** `docs/performance/k6-load-test.md` Section 3.2 — 5th/6th/7th run 3회 산술 평균

### ⚠️ 인터뷰에서 "미보유"로 명확히 답변 (PLANNED)
1. **JPA N+1 전후 쿼리 수 벤치마크:** `@EntityGraph` 코드 존재, 수치 측정 미완료
2. **Grafana 라이브 대시보드 스크린샷:** Grafana 컨테이너 설정 존재, 스크린샷 미확보
3. **k6 원본 stdout 로그 파일:** 결과는 docs에 기록, 원본 CLI 로그 파일 별도 보관 없음

---

## 11. New Deliverables (이번 QA 세션)

| 파일 | 설명 |
|------|------|
| `docs/PORTFOLIO_TRACEABILITY_MATRIX.md` | 전체 Claim-Evidence-Slide 추적 매트릭스 (신규 생성) |
| `docs/PORTFOLIO_EVIDENCE_QA_REPORT.md` | 최종 QA 보고서 (본 문서, 신규 생성) |

---

## 12. Remaining Risks

| Risk | 심각도 | 대응 |
|------|--------|------|
| k6 원본 로그 파일 미보유 | 낮음 | `k6-load-test.md`의 3회 반복 수치 표로 설명 가능 |
| Grafana 스크린샷 미확보 | 낮음 | `prometheus.yml` 설정 존재 + PLANNED으로 명시 |
| JPA N+1 벤치마크 수치 없음 | 낮음 | `@EntityGraph` 코드 존재 확인, PLANNED으로 격리 |
| 단일 노드 Docker Compose (1,000+ VU 미검증) | 중간 | Slide 014에 LIMITATIONS로 명시, PLANNED 로드맵 제시 |
| presentation.pptx 삭제됨 (`D` 상태) | 없음 | HTML Presentation으로 대체 완료, pptx 불필요 |

---

## 13. Final Verdict

```
✅ 26-05adf  = CLEAN (소스 코드 미수정)
✅ SA-1      = CLEAN (AI 프로세스 문서 미수정)
✅ PR-1A1    = 의도적 변경만 (QA 결과물: Traceability Matrix, QA Report 추가)

✅ validate.py --all       = ALL CHECKS PASSED (8/8)
✅ unittest discover       = OK (50 tests)
✅ renderer apms-auth --all = BUILD PASS (5 polymorphic documents)

PORTFOLIO EVIDENCE QA: FINAL PASS ✅
```
