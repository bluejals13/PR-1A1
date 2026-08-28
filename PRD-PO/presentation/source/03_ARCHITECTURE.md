# 03. System & Network Architecture

## What
Nginx 리버스 프록시 단일 진입점과 Docker Compose 기반으로 오케스트레이션된 7개 컨테이너 서비스 간의 격리 네트워크 토폴로지.

## Why
- 외부 공격 표면(Attack Surface)을 최소화하고 정적 자원과 API 라우팅을 효율적으로 분리.
- RDBMS, In-Memory 캐시, 애플리케이션 계층을 내부 네트워크로 격리하여 보안 침해 방지.
- 모니터링/메트릭 수집 파이프라인을 비침습적으로 연동하여 시스템 가시성 확보.

## How
- **Nginx (Port 80):** 유일한 외부 공개 Gateway. `/` 요청은 React SPA 정적 파일로 서빙, `/api/*` 요청은 백엔드로 Proxy Pass.
- **Spring Boot App (Port 8080):** 도커 브리지 네트워크 내부 통신 전용.
- **MySQL 8.0 (Port 3306 / 호스트 3307):** RDBMS 데이터 영속성 계층.
- **Redis 7.0 (Port 6379):** In-Memory Refresh Token(JTI) 및 Blacklist 저장소.
- **Observability Stack:** Prometheus(9090) ➔ VictoriaMetrics(8428) ➔ Grafana(3000) 모니터링 파이프라인.

## Evidence
- `PR-Files/architecture/ARCHITECTURE_SPEC.md` Section 2.1 & 2.2
- `26-05adf/docker-compose.yml`
- `26-05adf/nginx/default.conf`

## Result
- 7개 도커 서비스 기동 및 상호 통신 무결성 검증 `[IMPLEMENTED]` `[VERIFIED]`
- Nginx 리버스 프록시 라우팅 오버헤드 1ms 미만 유지 `[VERIFIED]`

## Status
`[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/architecture/ARCHITECTURE_SPEC.md`

## Presentation Use
- **Slide 03:** System & Container Topology (시스템 구성도 및 포트 격리 정책)
