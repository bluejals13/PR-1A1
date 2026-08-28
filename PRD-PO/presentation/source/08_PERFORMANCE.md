# 08. Performance Validation & k6 Benchmark

## What
k6 부하 테스트 도구를 활용해 70 VUs(Virtual Users) 동시 부하 환경에서 시스템 처리량, 지연시간, 안정성을 3회 반복 실측한 벤치마크 결과.

## Why
- 동시 접속 증가 시 Nginx ➔ Spring Boot ➔ Redis ➔ MySQL 간 병목 및 스레드 풀 고갈, 커넥션 누수 여부를 실측 검증하기 위함.
- "빠르다"는 주관적 주장을 배제하고 정량적 SLA/임계치 기준 검증 사실 입증.

## How
- **테스트 시나리오:** 로그인 ➔ 내 정보 조회 ➔ 인가 메뉴 조회 ➔ RTR 토큰 갱신 (실제 사용자 트래픽 플로우)
- **부하 조건:** 70 VU 동시 부하, 1분(60초) 지속 주입, 3회 반복 측정
- **설정 임계치 (Thresholds):**
  - `http_req_duration`: `['p(95)<50', 'avg<20']`
  - `http_req_failed`: `['rate<0.01']`

## Evidence
- `PR-Files/performance/K6_LOAD_TEST_REPORT.md` Section 2 & 3
- `26-05adf/k6/scenarios/load.test.js`
- `26-05adf/k6/config/thresholds.js`
- `26-05adf/docs/performance/k6-load-test.md`

## Result (Strict Fact - 3회 산술 평균)
- **Virtual Users (VU):** **70 VUs** `[VERIFIED]`
- **Test Duration:** **1 minute (60s)** `[VERIFIED]`
- **Throughput:** **463 req/s** (5차 469 + 6차 457 + 7차 465) / 3 `[VERIFIED]`
- **Average Latency:** **5.64 ms** (5차 4.73 + 6차 6.01 + 7차 6.18) / 3 `[VERIFIED]`
- **P95 Latency:** **9.98 ms** (5차 8.77 + 6차 10.61 + 7차 10.57) / 3 `[VERIFIED]`
- **Error Rate:** **0.00% (총 0건 에러)** `[VERIFIED]`
- **판정:** 모든 설정 임계치 100% PASS

## Status
`[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/performance/K6_LOAD_TEST_REPORT.md`

## Presentation Use
- **Slide 10:** Performance Validation (k6 70 VU 부하 테스트 실측 성과)
