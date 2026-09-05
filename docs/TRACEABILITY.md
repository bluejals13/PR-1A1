# End-to-End Traceability Matrix

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED

---

## 1. 전체 추적성 그래프 (Traceability Chain)

```text
SA-1 (Why)
   │
   ▼
26-05adf (Build & Test)
   │
   ▼
PR-1A1 Snapshot & Bundle (Proof)
   │
   ▼
Claim Registry (CLM-*)
   │
   ▼
Presentation Slide / Portfolio Case Study
```

---

## 2. 도메인별 추적성 매트릭스

| Claim ID | Domain | SA-1 Decision | 26-05adf Implementation | 26-05adf Test | Evidence Bundle | Portfolio Artifact | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **CLM-SEC-001** | SECURITY | `1-2_jwt_redis_optimization.md` | `JwtProvider.java`, `JwtAuthenticationFilter.java` | `JwtAuthenticationFilterTest.java` | `EV-SEC-001` | Slide 04, 05, 06 | `[VERIFIED]` |
| **CLM-SEC-002** | SECURITY | `1-2_jwt_redis_optimization.md` | `RefreshTokenRepository.java` (Lua Script) | `RefreshTokenRepositoryTest.java` | `EV-SEC-002` | Slide 05, CS Section 3.2 | `[VERIFIED]` |
| **CLM-SEC-003** | SECURITY | `1-2_jwt_redis_optimization.md` | `TokenBlacklistService.java` | `TokenBlacklistServiceTest.java` | `EV-SEC-003` | Slide 05, CS Section 4.1 | `[VERIFIED]` |
| **CLM-RBAC-001** | RBAC | `03_Backend_Conventions.md` | `UserAuthorityService.java`, `V2__init_authority_schema.sql` | `RbacSecurityIntegrationTest.java` | `EV-RBAC-001` | Slide 04, 06 | `[VERIFIED]` |
| **CLM-RBAC-002** | RBAC | `01_Architecture_and_Ports.md` | `MenuAdminController.java` | `MenuSecurityIntegrationTest.java` | `EV-RBAC-002` | Slide 04, 06 | `[VERIFIED]` |
| **CLM-PERF-001** | PERFORMANCE| `docs/performance/k6-load-test.md` | `k6/scenarios/load.test.js`, `thresholds.js` | k6 70 VU Benchmark Report (3 runs) | `EV-PERF-001` | Slide 01, 10 | `[VERIFIED]` |
| **CLM-INFRA-001**| INFRA | `01_Architecture_and_Ports.md` | `nginx/default.conf`, `docker-compose.yml` | Container Routing & Isolation | `EV-INFRA-001` | Slide 03, 08 | `[IMPLEMENTED]` |
| **CLM-TS-001** | INCIDENT | `01-redis-failure.md` | `application.yaml` (lettuce timeout 2000ms) | `TokenBlacklistServiceTest.java` | `EV-TS-001` | Slide 07, TS-01 | `[VERIFIED]` |
| **CLM-TS-002** | INCIDENT | `TS-001_JWT_REFRESH_LOOP.md` | `frontend/src/api/http.ts` | `SecurityIntegrationTest.java` | `EV-TS-002` | Slide 07, TS-001 | `[VERIFIED]` |
| **CLM-AI-001** | AI_PROCESS | `conventions/rules.md`, `changelogs/` | SA-1 8-Stage Lifecycle & Conventions | Audit & Git Log Trace | `EV-AI-001` | Slide 12 | `[DOCUMENTED]` |
