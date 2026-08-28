# 01. Project Overview

## What
Java 17, Spring Boot 3.3 기반의 견고한 백엔드 아키텍처에 무상태(Stateless) JWT 및 Redis 기반 RTR(Refresh Token Rotation)·블랙리스트 보안 체계를 구축하고, Docker/Nginx 인프라 격리, k6 부하 검증, SA-1 거버넌스 기반의 통제된 AI 협업 라이프사이클을 실증한 엔지니어링 프로젝트.

## Why
- 단순 CRUD 구현을 넘어 보안성, 성능, 운영 안정성, 공학적 검증 프로세스를 통합적으로 입증하기 위함.
- JWT의 고질적 한계인 "발급 후 즉시 무효화 불가" 및 "토큰 탈취 재사용 위험"을 구조적으로 해결.
- 로컬/컨테이너 배포 환경의 포트 격리 및 실측 부하 테스트를 통한 엔지니어링 신뢰성 확보.

## How
- **Core Backend:** Java 17, Spring Boot 3.3.2, Spring Security 6, Spring Data JPA, MySQL 8.0, Redis 7.0
- **Security:** JJWT (HMAC-SHA256), Redis TTL 기반 Token Blacklist, JTI 기반 RTR, User-Role-Permission M:N RBAC
- **Infra & Ops:** Docker Compose (7개 컨테이너 격리), Nginx Reverse Proxy (Port 80 단일 진입점), Prometheus, VictoriaMetrics, Grafana
- **Testing & Verification:** JUnit 5 (10종 단위/통합 테스트 스위트), k6 (70 VU 스트레스 부하 테스트)
- **Process Governance:** SA-1 기반 Documentation-First & Zero-Chatter AI 개발 워크플로우

## Evidence
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` (Fact Base 1.1.0)
- `PR-Files/architecture/ARCHITECTURE_SPEC.md`
- Source Code: `https://github.com/bluejals13/26-05adf` (`feature/auth@0603@1401`)
- AI Process: `https://github.com/bluejals13/SA-1` (`main`)

## Result
- 7개 도커 서비스 기반 컨테이너 오케스트레이션 구성 완료 `[IMPLEMENTED]`
- 10종 핵심 자동화 테스트 스위트 100% 통과 `[VERIFIED]`
- k6 70 VU 동시 부하 환경에서 평균 5.64ms 레이턴시 및 0.00% 에러율 달성 `[VERIFIED]`

## Status
`[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `SA-1` (`main`)
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`

## Presentation Use
- **Slide 01:** Title & Project Identity (핵심 엔지니어링 포지셔닝)
