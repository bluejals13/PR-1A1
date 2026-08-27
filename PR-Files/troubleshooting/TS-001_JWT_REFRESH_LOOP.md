# [TS-001] JWT Refresh Token 갱신 실패 시 무한 루프 이슈

- **Incident ID:** TS-001
- **Domain:** Authentication & Client-Server Interceptor
- **Status:** `[VERIFIED]` `[DOCUMENTED]`
- **Related Repository:** `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
- **Registered Context:** `AGENTS.md` 장애 기록 TS-001

---

## 1. Symptom (현상)
- Refresh Token이 만료되었거나 이미 RTR로 소진된 상태에서 API 요청 시, 클라이언트의 HTTP 인터셉터가 토큰 갱신(`/api/auth/refresh`)을 시도하고, 갱신 실패 후 다시 원래 요청을 재시도하여 무한 HTTP 재시도 루프가 발생하는 현상.

---

## 2. Impact (영향 범위)
- **심각도:** High
- **영향:** 클라이언트 브라우저 과부하(CPU 점유율 상승) 및 서버에 불필요한 401 에러 요청 폭증.

---

## 3. Diagnosis (진단 및 로그)
- **네트워크 로그:** 동일한 엔드포인트와 `/api/auth/refresh` 간의 401 Unauthorized 요청이 초당 수십 회 연속 발생.
- **클라이언트 코드 분석:** Axios/Fetch 인터셉터에서 401 수신 시 무조건 갱신 로직을 호출하고, 갱신 실패에 대한 최종 탈출(Exit Condition)이 누락되어 있음을 확인.

---

## 4. Root Cause (근본 원인)
1. **인터셉터 탈출 조건 부재:** 토큰 갱신 요청 자체에서 401이 발생했을 때 재시도 큐를 비우고 세션을 종료하는 로직이 결여됨.
2. **RTR JTI 즉시 무효화 타이밍:** 구버전 Refresh Token으로 요청 시 서버는 즉시 무효화 응답을 반환하나 클라이언트가 상태를 초기화하지 못함.

---

## 5. Resolution (해결 방법)
- **클라이언트 인터셉터 플래그 및 탈출 조건 추가:**
  - 토큰 갱신 시도 중 발생한 401 오류는 재시도하지 않고 즉시 사용자 로컬 인증 상태 초기화 및 로그인 페이지로 리다이렉트.
- **서버 에러 코드 명확화:**
  - RTR 위반 또는 만료 시 `INVALID_REFRESH_TOKEN` 에러 코드를 명확히 반환하여 클라이언트가 즉시 로그아웃 처리하도록 유도.

---

## 6. Prevention (재발 방지 대책)
- **통합 테스트 검증:** 만료/소진된 Refresh Token 요청 시 재시도 없이 1회 실패 후 세션 종료 검증 (`SecurityIntegrationTest.java`) `[VERIFIED]`.
- **E2E 시나리오 테스트:** 브라우저 환경에서 토큰 만료 시 로그인 페이지 정상 리다이렉트 확인 `[VERIFIED]`.
