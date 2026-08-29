# Agent Standard Operating Procedure (SOP) & Document System Governance

- **Target Repository:** `PR-1A1`
- **Version:** 2.0.0
- **Last Updated:** 2026-08-29
- **Status:** ACTIVE & ENFORCED

---

## 1. Project Identity & Positioning

- **Identity:** Java/Spring 기반 백엔드를 구축하고, 컨테이너/인프라/운영 환경(Nginx, CI/CD, Observability)까지 연결하여 이해하는 엔지니어의 포트폴리오 공간.
- **Track Separation:**
  - **Track A (Foundation):** Java, Maven, IoC/DI 컨테이너 직접 구현(`MySpringFW`)을 통한 프레임워크 원리 학습.
  - **Track B (Advanced):** `26-05adf`, `SA-1` 기반 Spring Boot, Security, Redis(Token Rotation), Docker, k6 부하 테스트 실무.

---

## 2. Strict Guardrails (Zero-Hallucination)

포트폴리오 문서 및 시스템 검증 시 다음 **실측 팩트 데이터만** 사용하며, 임의로 수치를 창조하거나 추측하지 않는다.
- **Performance Metrics (k6 실측치):** 70 VUs, 1 min, Avg Response 5.64ms, P95 9.98ms, Throughput 463 req/s, Error Rate 0.00% (`docs/performance/k6-load-test.md` 5~7차 평균)
- **Security Features:** JWT Access Token(1h, Bearer), Refresh Token(7d, HttpOnly Cookie), Refresh Token Rotation(Lua Script), Redis Blacklist(잔여 TTL), RBAC(User-Role-Permission M:N)
- **Infra Features:** Docker Compose (8개 서비스), Nginx Reverse Proxy (Port 80 단일 진입점), Prometheus + VictoriaMetrics + Grafana Agent
- **Unverified/Planned (구현되지 않음 - Roadmap [PLANNED] 표기):** JPA N+1 정량 벤치마크 수치, EXPLAIN 쿼리 튜닝 실측, Message Queue (Kafka/RabbitMQ), Redis Cluster 다중화

---

## 3. AI-Assisted Engineering Workflow

에이전트는 요구사항을 수신하면 다음 5단계 순서로만 작업한다:
1. **ANALYZE:** 관련 Repository Context 및 기존 코드를 읽고 영향도 분석.
2. **PLAN:** 수정/작성할 파일 목록과 예상 결과를 개발자에게 제시 후 승인 대기.
3. **IMPLEMENT:** 승인된 범위 내에서만 최소한의 안전한 코드 변경.
4. **VERIFY:** 단위 테스트(JUnit) 및 부하 테스트(k6) 결과를 통해 기능 및 무결성 검증.
5. **DOCUMENT:** 검증 완료 후 Git Commit 메시지 작성 및 TS(Troubleshooting) 문서 업데이트.

---

## 4. Documentation Standard (Troubleshooting)

모든 장애 해결 문서(TS)는 다음 6단계 구조를 엄격히 따른다:
1. **Symptom (현상)**
2. **Impact (영향 범위)**
3. **Diagnosis (진단 과정 및 로그 확인)**
4. **Root Cause (근본 원인)**
5. **Resolution (해결 방법 - 실제 코드/설정 변경 내역)**
6. **Prevention (재발 방지 대책)**
- **주요 실측 장애 기록:** `TS-01-REDIS` (Redis Lettuce 2s 타임아웃 단축 및 503 격리), `TS-001` (JWT Refresh 갱신 실패 시 401 무한 루프 탈출), `TS-003` (Docker Compose 환경 내 Redis localhost 바인딩 해결)

---

## 5. Document System Change Governance (14 Core Principles)

본 거버넌스는 `26-05adf`(Source of Truth) 및 `SA-1`(Knowledge)의 변경 사항이 발생할 때 `PR-1A1` 문서 시스템의 무결성을 유지하고 불필요한 전체 재빌드를 방지하기 위한 절대 원칙입니다.

```text
[ Git Diff (최초 입력) ] ──► [ Change Level 판정 (C0~C5) ] ──► [ relations.yaml 그래프 탐색 ]
                                                                       │
┌──────────────────────────────────────────────────────────────────────┴─────────────────────────────────┐
│                                                                                                        │
▼                                                                                                        ▼
[ 영향받은 대상만 STALE 전이 ]                                                             [ 비영향 영역 100% 보존 ]
│                                                                                          (수정/재생성 절대 금지)
▼
[ Selective Revalidation (Evidence/Claim 재검증) ]
│
├── PASS (일치) ────────► [ FRESH 승격 ] ──► [ Selective Render (HTML 갱신) ]
├── CONFLICT (충돌) ────► [ INVALID 격리 ] (FRESH 승격 절대 금지)
└── NO PROOF (근거부족) ─► [ UNVERIFIED / PLANNED 유지 ] (추측 보완 금지)
```

### 14 Core Rules:

1. **최초 입력 원칙:** 모든 PR 및 변경 검증의 최초 입력은 반드시 `git diff`로 한다.
2. **보조 정보 원칙:** Changelog, Phase 번호, 기존 PPT/HTML은 변경 영향도를 판정하는 보조 정보로만 사용하며, Source of Truth로 취급하지 않는다.
3. **실질 영향도 기반 Level 판정:** 변경된 파일의 확장자나 종류만으로 단순 결정하지 않고, 실제 변경 내용이 기존 Claim, Evidence, Contract, Architecture에 미치는 실질적 영향을 기준으로 최종 Change Level(C0~C5)을 판정한다.
4. **의존성 그래프 탐색:** `registry/relations.yaml`을 조회하여 `Changed Source ➔ Affected Domain ➔ Affected Evidence ➔ Affected Document`의 의존성 그래프를 정확히 탐색한다.
5. **비영향 영역 격리 보존:** 변경 영향 그래프에 포함되지 않은 Domain, Evidence, Document는 절대 수정하거나 재생성하지 않는다.
6. **선택적 STALE 전이:** 변경 영향이 확인된 Document 및 Claim만 `STALE` 상태로 전환한다.
7. **선택적 재검증 (Selective Revalidation):** `STALE`로 전환된 항목에 대해서만 선별적 재검증을 수행한다.
8. **상태 결정 엄격성:** 재검증 결과에 따라 `FRESH`(검증 완료), `INVALID`(원천 충돌), `UNVERIFIED`(근거 부족) 상태를 결정한다.
9. **불변 Evidence 보존 (Case A):** 기존 Claim의 단순 문장 수정이나 설명 보완 시에는 Evidence를 임의로 재생성하거나 변경하지 않는다.
10. **새로운 사실 추가 검증 (Case B):** 새로운 사실이나 기술적 주장이 추가된 경우에만 `Claim ➔ Evidence ➔ Source` 연결을 새롭게 검증하고 등록한다.
11. **추측 보완 절대 금지:** 검증되지 않은 사실이나 실측 수치가 없는 주장은 임의의 추측으로 보완하지 않고 `UNVERIFIED` 또는 `[PLANNED]` 상태로 유지한다.
12. **선택적 렌더링 (Selective Render):** 검증이 완료되어 `FRESH`로 확정된 영향 문서에 대해서만 필요한 경우 렌더러를 호출하여 HTML을 갱신한다.
13. **일괄 재생성 금지:** 새로운 Phase가 시작되었거나 새 Changelog가 추가되었다는 이유만으로 전체 Portfolio를 재검증하거나 전체 HTML을 일괄 재생성하지 않는다.
14. **충돌 문서 불승격:** `26-05adf`의 실제 코드, 테스트, 설정과 모순되거나 충돌하는 문서는 절대 `FRESH` 상태로 승격하지 않고 `INVALID`로 처리한다.

---

## 6. System Matrix & Vocabulary Alignment

본 거버넌스는 다음 레지스트리 및 정책 문서와 100% 동일한 용어와 상태 체계를 공유합니다:

- **Change Levels:** `CHANGE_POLICY.md` (C0: Cosmetic/Doc Only, C1: Evidence Addition, C2: Internal Implementation, C3: Behavioral/Contract, C4: Architecture Change, C5: Source of Truth/Boundary)
- **Document Lifecycle States:** `documents.yaml` (`FRESH`, `STALE`, `INVALID`, `UNVERIFIED`)
- **Evidence Verification States:** `evidence.yaml` (`VERIFIED`, `IMPLEMENTED`, `DOCUMENTED`, `PARTIAL`, `PLANNED`, `NOT_FOUND`)
- **Dependency Graph:** `relations.yaml` (Path Pattern ➔ Level ➔ Domains ➔ Evidences ➔ Documents)
- **Template Contracts:** `templates/contracts/` (`LONGFORM`, `FEATURE`, `TECHNICAL`, `SLIDE`, `EVIDENCE`)
