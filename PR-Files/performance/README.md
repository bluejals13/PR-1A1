# Performance Testing & Metrics (`PR-Files/performance`)

## 1. Responsibility
본 디렉터리는 k6 부하 테스트 시나리오, 실측 수치, 임계치(Thresholds), 모니터링 연계 결과를 다룹니다.

## 2. Strict Fact Metrics (절대 임의 수정 금지)
포트폴리오 및 기술 문서 작성 시 반드시 아래 실측된 사실 데이터만을 사용합니다.

| 지표 (Metric) | 실측값 (Fact) | 판정 기준 (Threshold) | 판정 |
| :--- | :--- | :--- | :---: |
| **Virtual Users (VU)** | **70 VUs** | 70 VUs 부하 주입 | PASS |
| **Test Duration** | **1 minute (60s)** | 60초 지속 부하 | PASS |
| **Throughput (req/s)** | **463 req/s** | - | Fact |
| **Average Latency** | **5.64 ms** | `p(95) < 50ms` | PASS |
| **P95 Latency** | **9.98 ms** | `p(95) < 50ms` | PASS |
| **Error Rate** | **0.00% (0 errors)** | `rate < 1%` | PASS |

## 3. Source of Truth Mapping
- **Source Scripts:**
  - `26-05adf/k6/scenarios/load.test.js`
  - `26-05adf/k6/scenarios/stress.test.js`
  - `26-05adf/k6/scenarios/spike.test.js`
  - `26-05adf/k6/scenarios/soak.test.js`
  - `26-05adf/k6/config/thresholds.js`
- **Source Report:**
  - `26-05adf/docs/performance/k6-load-test.md`
