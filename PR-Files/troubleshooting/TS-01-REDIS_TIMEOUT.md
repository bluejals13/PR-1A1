# [TS-01-REDIS] Redis 장애 시 커맨드 타임아웃 및 애플리케이션 블로킹 해결

- **Incident ID:** TS-01-REDIS
- **Domain:** Incident Analysis & System Resilience
- **Status:** `[VERIFIED]` `[DOCUMENTED]`
- **Related Repository:** `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
- **Source File:** `docs/troubleshooting/01-redis-failure.md`

---

## 1. Symptom (현상)
- Redis 컨테이너가 일시적으로 다운되거나 네트워크 단절이 발생했을 때, 백엔드 API 요청이 최대 1분간 응답하지 않고 대기하는 현상이 발생함.
- 프론트엔드에서는 응답 지연으로 인해 화면이 멈추거나 흰 화면(Blank Screen)이 노출됨.

---

## 2. Impact (영향 범위)
- **심각도:** High
- **영향:** 인증 필터에서 Redis를 조회하는 모든 요청(`/api/*`)이 동반 블로킹되어 서비스 전체 가용성 저하.

---

## 3. Diagnosis (진단 및 로그)
- **로그 분석:**
  `io.lettuce.core.RedisCommandTimeoutException: Command timed out after 1 minute(s)`
- **동작 추적:** Spring Data Redis의 기본 Lettuce 커맨드 타임아웃이 60초로 설정되어 있어, Redis 장애 시 스레드가 60초간 블로킹 상태에 빠짐을 확인.

---

## 4. Root Cause (근본 원인)
1. **타임아웃 미설정:** Lettuce 클라이언트의 커맨드 타임아웃 기본값이 60초로 너무 길어 장애 전파 발생.
2. **예외 처리 부재:** Redis 연결 오류 시 비즈니스 로직 및 필터 계층에서 적절한 Fallback 또는 명확한 에러 응답 변환 로직 부재.

---

## 5. Resolution (해결 방법)

### 5.1 Lettuce 커맨드 타임아웃 2초 단축
- `application.yml`에 Lettuce 클라이언트 타임아웃 명시적 구성:
```yaml
spring:
  data:
    redis:
      timeout: 2000ms
      lettuce:
        shutdown-timeout: 2000ms
```

### 5.2 예외 핸들링 및 명확한 에러 코드 반환
- Redis 접속 실패 시 `500 INTERNAL_SERVER_ERROR` 및 `REDIS_UNAVAILABLE` 에러 코드를 `ApiResponse` 형식으로 즉시 반환하도록 방어 코드 적용.

---

## 6. Prevention (재발 방지 대책)
- **모니터링 알람:** Redis 연결 상태 및 커맨드 지연 메트릭 수집 및 임계치 초과 시 경보 설정.
- **Circuit Breaker 검토:** 향후 Redis 의존 서비스에 대한 서킷 브레이커 도입 검토 `[PLANNED]`.
- **회복 검증:** Redis 컨테이너 강제 중단 시 2초 이내 명확한 에러 응답 반환 및 복원 후 자동 재연결 검증 완료 `[VERIFIED]`.
