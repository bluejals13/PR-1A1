# 02. Problem and Solution

## What
웹 애플리케이션의 인증/인가 시스템 및 배포 환경에서 발생하는 3대 엔지니어링 난제(토큰 탈취/무효화 불가, 네트워크 무분별 노출, 개발-배포 환경 불일치)를 정의하고 이를 해결한 기술적 접근법.

## Why
- **JWT 무상태성의 딜레마:** 세션 DB 조회를 줄여 성능을 높이지만, 토큰 탈취 시 즉각적인 무효화 및 강제 로그아웃이 불가능한 보안 위험.
- **네트워크 보안 취약성:** DB/Redis 및 백엔드 포트가 외부에 노출될 경우 공격 표면(Attack Surface) 확장.
- **인프라 종속성 문제:** 로컬 환경과 컨테이너 환경 간 DNS 해석 차이로 인한 장애 발생 위험.

## How
- **보안 솔루션 (Hybrid Token Strategy):**
  - Access Token은 1시간 무상태 검증으로 고성능 유지.
  - Refresh Token은 7일 만료, UUID JTI 기반 RTR(Rotation) 및 Redis 관리로 탈취 시 재사용 차단.
  - 로그아웃 시 Access Token 잔여 수명만큼 Redis Blacklist에 등록하여 즉시 인가 차단.
- **인프라 솔루션 (Gateway & Port Isolation):**
  - 외부 공용 진입점은 Nginx(Port 80)로 단일화.
  - Spring Boot(8080), Redis(6379), MySQL(3306)은 Docker 내부 브리지 네트워크(`app-net`)로 완전 격리.
- **환경 통제 솔루션:**
  - Flyway V1~V5 DDL 마이그레이션으로 DB 형상 일관성 보장.
  - Docker Compose 환경변수 기반 동적 바인딩 주입.

## Evidence
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md`
- `PR-Files/architecture/ARCHITECTURE_SPEC.md`
- `PR-Files/troubleshooting/TS-001_JWT_REFRESH_LOOP.md`
- `PR-Files/troubleshooting/TS-003_DOCKER_REDIS_BINDING.md`

## Result
- 토큰 탈취 후 재사용 시도시 즉시 401 Unauthorized 차단 검증 `[VERIFIED]`
- Nginx 경유 외 직접적인 내부 컨테이너 포트 접근 차단 `[IMPLEMENTED]`
- DDL 환경 불일치 오류 0건 달성 `[VERIFIED]`

## Status
`[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`

## Presentation Use
- **Slide 02:** Problem & Solution Overview (도전 과제 및 기술적 해결책)
