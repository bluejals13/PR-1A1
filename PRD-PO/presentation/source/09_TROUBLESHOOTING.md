# 09. Troubleshooting & Incident Response

## What
시스템 개발 및 컨테이너 환경에서 실제로 발생한 3건의 핵심 기술 장애를 TS 표준 6단계 (`Symptom ➔ Impact ➔ Diagnosis ➔ Root Cause ➔ Resolution ➔ Prevention`) 프레임워크로 분석하고 해결한 엔지니어링 사례.

## Why
- 시스템 장애 발생 시 임기응변식 대처가 아닌, 근본 원인(Root Cause)을 정확히 진단하고 재발 방지책을 아키텍처에 내재화하기 위함.
- 엔지니어의 문제 해결 능력 및 시스템 복원력(Resilience) 설계 역량 입증.

## How & Incidents

### Case 1: [TS-01-REDIS] Redis 단절 시 커맨드 타임아웃 지연 및 프론트엔드 블로킹
- **Symptom:** Redis 컨테이너 다운 시 커맨드 60초 블로킹 발생 및 프론트엔드 흰 화면(Blank Screen) 노출.
- **Root Cause:** Lettuce 기본 타임아웃(60s) 미설정 및 토큰 검증 필터 블로킹 전파.
- **Resolution:** Lettuce 커맨드 타임아웃을 2초(`timeout: 2000ms`)로 단축, `RedisUnavailableException` 503 에러 핸들링, 프론트엔드 Error Boundary 보강.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

### Case 2: [TS-001] JWT Refresh 무한 루프 이슈
- **Symptom:** Refresh Token 갱신 실패 시 클라이언트 인터셉터와 서버 간 무한 재시도 루프 발생.
- **Root Cause:** 401 재발급 실패 응답에 대한 클라이언트 재시도 탈출 조건(Exit Condition) 결여.
- **Resolution:** Single Flight 토큰 재발급 패턴 구축 및 401 수신 시 즉시 세션 초기화 및 로그인 페이지 리다이렉트.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

### Case 3: [TS-003] Docker 환경 내 Redis localhost 바인딩 실패
- **Symptom:** Docker Compose 환경에서 Spring Boot가 `localhost:6379`로 접속 시도하여 커넥션 거부 발생.
- **Root Cause:** 컨테이너 격리 환경에서 `localhost`는 컨테이너 자신을 가리키는 네트워크 격리 특성.
- **Resolution:** Spring Boot 설정에 `${SPRING_REDIS_HOST:localhost}` 적용 및 Docker Compose에서 `SPRING_REDIS_HOST: redis` 환경변수 주입.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

## Evidence
- `PR-Files/troubleshooting/TS-01-REDIS_TIMEOUT.md`
- `PR-Files/troubleshooting/TS-001_JWT_REFRESH_LOOP.md`
- `PR-Files/troubleshooting/TS-003_DOCKER_REDIS_BINDING.md`

## Result
- Redis 단절 시 2초 이내 빠른 실패 및 503 반환 검증 완료 `[VERIFIED]`
- 토큰 갱신 실패 시 무한 루프 없이 정상 로그아웃 처리 검증 완료 `[VERIFIED]`
- 컨테이너 간 서비스명 기반 DNS 해석 및 통신 100% 정상화 `[VERIFIED]`

## Status
`[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/troubleshooting/`

## Presentation Use
- **Slide 11:** Real-World Incident Troubleshooting (장애 분석 및 해결)
- **Slide 13:** Architectural Decisions & Technical Trade-offs (시스템 복원력 설계)
