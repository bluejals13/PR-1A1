# [TS-003] Docker Compose 환경 내 Redis localhost 바인딩 실패 이슈

- **Incident ID:** TS-003
- **Domain:** Infrastructure & Container Networking
- **Status:** `[VERIFIED]` `[DOCUMENTED]`
- **Related Repository:** `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
- **Registered Context:** `AGENTS.md` 장애 기록 TS-003

---

## 1. Symptom (현상)
- 로컬 개발 환경(IDE)에서는 정상 작동하던 백엔드 애플리케이션이 `docker compose up`으로 컨테이너화하여 실행할 때, Redis 연결 실패(`Connection refused`)가 발생하며 Spring Boot 기동이 실패함.

---

## 2. Impact (영향 범위)
- **심각도:** High
- **영향:** 컨테이너 기반 빌드 및 로컬 통합 환경 배포 불가.

---

## 3. Diagnosis (진단 및 로그)
- **에러 로그:**
  `io.netty.channel.AbstractChannel$AnnotatedConnectException: Connection refused: localhost/127.0.0.1:6379`
- **환경 분석:** Spring Boot `application.yml`의 Redis host가 `localhost`로 하드코딩되어 있어, Spring Boot 컨테이너 내부의 `127.0.0.1:6379`를 탐색함을 확인.

---

## 4. Root Cause (근본 원인)
- Docker 컨테이너 격리 환경에서 `localhost`는 호스트 OS나 다른 컨테이너가 아닌 **해당 컨테이너 자신(Container Loopback)**을 가리킴.
- Redis는 별도의 `redis` 컨테이너에서 구동되므로, 동일한 Docker Network 상에서는 서비스 이름인 `redis`를 호스트명으로 사용해야 함.

---

## 5. Resolution (해결 방법)

### 5.1 환경변수 기반 프로파일 분리
- `application.yaml`에 환경변수 기본값 설정 적용:
```yaml
spring:
  data:
    redis:
      host: ${SPRING_REDIS_HOST:localhost}
      port: ${SPRING_REDIS_PORT:6379}
```

### 5.2 docker-compose.yml 환경변수 주입
- `docker-compose.yml`의 backend 서비스 환경변수에 `SPRING_REDIS_HOST: redis` 명시:
```yaml
services:
  backend:
    environment:
      - SPRING_REDIS_HOST=redis
      - SPRING_REDIS_PORT=6379
```

---

## 6. Prevention (재발 방지 대책)
- **Docker Compose 기동 검증:** 컨테이너 환경에서 `backend` -> `redis:6379` DNS 해석 및 연결 성공 자동 확인 `[VERIFIED]`.
- **설정 원칙 수립:** 인프라 의존성(DB, Redis) 호스트명은 모두 환경변수 기반으로 주입하는 12-Factor App 원칙 준수 `[DOCUMENTED]`.
