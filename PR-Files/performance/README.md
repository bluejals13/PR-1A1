# Performance Testing & Metrics (`PR-Files/performance`)

## 1. Purpose (목적)
k6 기반 실제 동시 부하 테스트를 통해 측정된 처리량(Throughput), 응답 지연 시간(Latency Avg/P95), 에러율(Error Rate) 등의 정량적 엔지니어링 실측 데이터와 성능 한계 검증 보고서를 관리합니다.

## 2. Input / Source (원천 데이터)
- **k6 테스트 스크립트:**
  - `26-05adf/k6/scenarios/load.test.js`
  - `26-05adf/k6/scenarios/stress.test.js`
  - `26-05adf/k6/scenarios/spike.test.js`
  - `26-05adf/k6/scenarios/soak.test.js`
  - `26-05adf/k6/config/thresholds.js`
- **원천 성능 보고서:**
  - `26-05adf/docs/performance/k6-load-test.md`

## 3. Output (산출물)
- **`K6_LOAD_TEST_REPORT.md`**: 70 VU 동시 부하 테스트 실측치 및 성능 임계치 통과 보고서

## 4. Strict Fact Metrics (절대 임의 수정 금지)
포트폴리오 및 기술 문서 작성 시 반드시 아래 실측된 사실 데이터만을 사용합니다.

| 지표 (Metric) | 실측값 (Fact) | 판정 기준 (Threshold) | 판정 |
| :--- | :--- | :--- | :---: |
| **Virtual Users (VU)** | **70 VUs** | 70 VUs 부하 주입 | PASS |
| **Test Duration** | **1 minute (60s)** | 60초 지속 부하 | PASS |
| **Throughput (req/s)** | **463 req/s** | - | Fact |
| **Average Latency** | **5.64 ms** | `p(95) < 50ms` | PASS |
| **P95 Latency** | **9.98 ms** | `p(95) < 50ms` | PASS |
| **Error Rate** | **0.00% (0 errors)** | `rate < 1%` | PASS |

## 5. What belongs here (포함되는 자료)
- k6 부하/스트레스/스파이크/소크 테스트 시나리오 및 실행 매개변수
- 실측 성능 지표 (Throughput, Latency, Error Rate, Resource Usage)
- 성능 임계치(Threshold) 충족 여부 및 병목 구간 분석 데이터

## 6. What does NOT belong here (포함되지 않는 자료)
- 실측되지 않은 가상의 성능 추정치나 "초당 수만 건 처리"와 같은 과장된 주장
- 기능 단위/통합 테스트 코드 및 합격 여부 (-> `verification/` 영역)
- 발표용 슬라이드 HTML / CSS / 디자인 요소 (-> `PRD-PO/` 영역)

## 7. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO/presentation/slides/001/`의 `70 VU / 5.64ms Avg [VERIFIED]` 지표와 `slides/002/`, `source/08_PERFORMANCE.md`의 성능 섹션은 오직 본 디렉터리의 실측치만을 인용합니다.
- `PR-Files/performance`는 사실 데이터의 원천이며, `PRD-PO`는 이 수치를 시각화하여 평가자에게 직관적으로 전달하는 발표물입니다.
