# Performance Testing & k6 Benchmark Specification Report

- **Document ID:** SPEC-PERF-01
- **Domain:** Performance, Load Testing & Observability
- **Source of Truth:**
  - Repository: `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
  - Source Files: `k6/scenarios/load.test.js`, `k6/config/thresholds.js`, `docs/performance/k6-load-test.md`
- **Target Workspace:** `PR-1A1/PR-Files/performance/K6_LOAD_TEST_REPORT.md`

---

## 1. Purpose & Scope

### 1.1 Purpose
본 문서는 `26-05adf` 백엔드 시스템(Spring Boot, Nginx, Redis, MySQL)에 대해 수행된 k6 기반 부하 테스트의 실측 수치와 임계치(Thresholds) 충족 여부, 그리고 Observability 연계 결과를 공학적 사실(Fact) 기반으로 기록합니다.

### 1.2 Scope
- 70 VU 동시 부하 환경 실측 수치 및 레이턴시 분포 분석
- k6 부하 시나리오 구성 및 임계치 판정 결과
- Prometheus / Grafana 모니터링 메트릭 연동 내역
- JPA N+1 등 미검증 최적화 항목의 `[PLANNED]` 명확한 분리

---

## 2. Strict Benchmark Metrics (실측 불변 팩트)

> [!IMPORTANT]
> 본 절의 수치는 실제 k6 부하 테스트를 통해 측정된 불변의 사실 데이터입니다.

| 메트릭 (Metric) | 실측값 (Fact - 3회 평균) | 설정 임계치 (Threshold) | 판정 (Status) |
| :--- | :---: | :---: | :---: |
| **Virtual Users (VU)** | **70 VUs** | 70 VUs 지속 부하 주입 | `[VERIFIED]` PASS |
| **Test Duration** | **1 minute (60s)** | 60초 지속 측정 (3회 반복) | `[VERIFIED]` PASS |
| **Throughput** | **463 req/s** | (5차 469 + 6차 457 + 7차 465) / 3 | `[VERIFIED]` Fact |
| **Average Latency** | **5.64 ms** | `avg < 20ms` (5차 4.73 + 6차 6.01 + 7차 6.18) / 3 | `[VERIFIED]` PASS |
| **P95 Latency** | **9.98 ms** | `p(95) < 50ms` (5차 8.77 + 6차 10.61 + 7차 10.57) / 3 | `[VERIFIED]` PASS |
| **Error Rate** | **0.00% (0 errors)** | `rate < 1.0%` (전 차수 0건 에러) | `[VERIFIED]` PASS |

---

## 3. Implementation Evidence (k6 스크립트 및 설정)

### 3.1 Thresholds Configuration Evidence
- **Source File:** `26-05adf/k6/config/thresholds.js`
```javascript
export const thresholds = {
    http_req_duration: ['p(95)<50', 'avg<20'], // 95% 요청 50ms 미만, 평균 20ms 미만
    http_req_failed: ['rate<0.01'],            // 에러율 1% 미만
};
```

### 3.2 Load Test Scenario Evidence
- **Source File:** `26-05adf/k6/scenarios/load.test.js`
- **시나리오 흐름:**
  1. `/api/auth/login` (사용자 인증 및 Access/Refresh 토큰 획득)
  2. `/api/users/me` (Access Token 기반 내 정보 조회)
  3. `/api/menus` (사용자 인가 메뉴 목록 조회)
  4. `/api/auth/refresh` (RTR 토큰 갱신)

---

## 4. Verification Evidence & Observability Integration

### 4.1 Observability Correlation
- **Prometheus & VictoriaMetrics:** 부하 주입 중 JVM Heap 사용량 안정적 유지 (안정적 GC 사이클 확인), HikariCP 커넥션 풀 고갈 없음 확인 `[VERIFIED]` `[DOCUMENTED]`
- **Nginx & Network:** Nginx Reverse Proxy 경유 시 추가 오버헤드 1ms 미만 수준 유지 `[VERIFIED]`

---

## 5. Limitations & Unknowns (절대 과장 금지)
- **JPA N+1 쿼리 최적화 실측 벤치마크:** Batch Size 및 Fetch Join 적용 전후의 세부 쿼리 수 비교 벤치마크는 현재 계획 과제임 `[PLANNED]`
- **분산 대규모 트래픽 (1,000+ VU):** 현재 70 VU 단일 노드 검증 완료 상태이며, 다중 노드 스케일아웃 테스트는 미수행 `[PLANNED]`

---

## 6. Claim-to-Evidence Traceability Matrix

| Claim (성능 주장) | Source Script / Config | 검증 결과 리포트 | 상태 |
| :--- | :--- | :--- | :---: |
| 70 VU 부하 시 P95 9.98ms 및 0% 에러율 | `k6/scenarios/load.test.js` | k6 실행 요약 로그 (`docs/performance/`) | `[VERIFIED]` |
| 초당 463 req/s 처리량 달성 | `k6/scenarios/load.test.js` | k6 Throughput 측정 지표 | `[VERIFIED]` |
| Prometheus/Grafana 지표 수집 | `docker-compose.yml` | Grafana JVM 대시보드 | `[DOCUMENTED]` |
