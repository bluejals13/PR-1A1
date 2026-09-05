# Backend & Infrastructure Engineering Portfolio Presentation

- **Presenter:** Backend & Infrastructure Engineer
- **Core Stacks:** Java 17, Spring Boot 3.3.2, Spring Security 6, Redis 7.0, MySQL 8.0, Docker Compose, Nginx, Prometheus/Grafana, k6
- **Source of Truth:**
  - Application: `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
  - AI & Workflow: `https://github.com/bluejals13/SA-1` (Branch: `main`)
  - Evidence Base: `PR-1A1/PR-Files/`
- **Slide Count:** 15 Slides (1 Slide, 1 Core Message Principle)

---

## Slide 01: Project Identity & Architecture Overview
> **핵심 테제:** 단순 API 구현을 넘어, 인증/인가 보안, 컨테이너 인프라 격리, 부하 검증 및 AI 엔지니어링 프로세스를 통합 구축한 백엔드 시스템

### 1. Problem & Challenge
- 마이크로서비스 및 웹 환경에서 보안성(토큰 탈취 방어), 확장성(Stateless 인증), 운영 안정성(컨테이너 격리 및 모니터링)을 동시에 만족하는 백엔드 아키텍처 구축 필요.

### 2. Technical Decision & Architecture
- **통합 기술 스택:** Spring Boot 3.3.2, Spring Security 6, Redis 7.0 (인메모리 세션/블랙리스트), MySQL 8.0 (Flyway V1~V5), Nginx (Reverse Proxy 단일 진입점).
- **측정 및 관측 파이프라인:** Prometheus + VictoriaMetrics + Grafana 메트릭 수집 및 k6 부하 검증 파이프라인 구축.

### 3. Verification & Result
- 7개 도커 서비스 기반 컨테이너 오케스트레이션 구성 완료 `[IMPLEMENTED]`.
- 10종 JUnit 자동화 테스트 100% 통과 및 k6 부하 테스트 검증 완료 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`
- `PR-Files/architecture/ARCHITECTURE_SPEC.md`

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "안녕하십니까. 본 프로젝트는 Java 17과 Spring Boot 3.3을 기반으로 토큰 탈취 및 재사용 방어 메커니즘을 갖춘 인증/인가 시스템을 설계하고, Nginx와 Docker Compose를 이용한 컨테이너 격리 인프라, k6를 통한 부하 검증, 그리고 SA-1 거버넌스 기반의 통제된 AI 협업 프로세스를 통해 완성한 엔지니어링 프로젝트입니다."

---

## Slide 02: Core Engineering Challenges & Objectives
> **핵심 테제:** 무상태성(Stateless)을 유지하면서도 실시간 세션 제어(로그아웃/탈취 방어)가 가능한 안전한 백엔드 시스템 구축

### 1. Problem & Challenge
- JWT는 무상태성으로 서버 부하를 줄이지만, 발급 후 즉시 무효화가 어렵고 토큰 탈취(Replay Attack)에 취약함.
- 로컬 개발 환경과 컨테이너 배포 환경 간의 네트워크 바인딩 차이로 인한 연결 실패 및 장애 전파 위험 존재.

### 2. Technical Decision & Architecture
- **JWT + RTR + Redis Blacklist 결합 구조:** Access Token(1시간)은 무상태로 검증하되, Refresh Token(7일)은 Redis JTI 기반 Rotation(RTR)으로 관리하고, 로그아웃 시 Access Token 잔여 TTL 동안 Redis Blacklist에 등록.
- **포트 격리 및 단일 진입점:** 외부에는 Nginx(Port 80)만 노출하고 애플리케이션 및 스토리지는 도커 내부 브리지 네트워크(`app-net`)로 완전 격리.

### 3. Verification & Result
- 토큰 탈취 시나리오 방어 및 즉시 차단 검증 완료 `[VERIFIED]`.
- Nginx를 통한 안전한 트래픽 라우팅 및 0% 패킷 에러 달성 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md`
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md`

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "JWT를 도입할 때 가장 큰 문제는 '토큰이 탈취되었을 때 어떻게 즉시 무효화할 것인가'입니다. 저는 무상태성의 확장성을 살리면서도, Refresh Token Rotation과 Redis Blacklist를 결합하여 안정적인 실시간 세션 통제력을 확보했습니다."

---

## Slide 03: System & Container Topology
> **핵심 테제:** Nginx 단일 진입점(Port 80)을 통한 보안 라우팅과 도커 브리지 네트워크 기반 7개 서비스 격리

### 1. Problem & Challenge
- 백엔드, DB, 캐시 등 내부 인프라 포트가 외부에 무분별하게 노출될 경우 보안 침해 및 공격 표면(Attack Surface) 증가.

### 2. Technical Decision & Architecture
- **Nginx Reverse Proxy:** 유일한 공용 진입점(Port 80)으로 설정하여 정적 자원 서빙 및 `/api/*` 요청만 백엔드(Port 8080)로 프록시 전달.
- **Docker Compose Topology (7 Services):** Nginx(80), Backend(8080 내부), MySQL(3307:3306), Redis(6379 내부), Prometheus(9090), VictoriaMetrics(8428), Grafana(3000).

### 3. Verification & Result
- `docker-compose.yml` 서비스 오케스트레이션 및 `nginx/default.conf` 라우팅 동작 검증 완료 `[IMPLEMENTED]` `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/architecture/ARCHITECTURE_SPEC.md` Section 2.1 & 2.2

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "전체 인프라는 Docker Compose를 통해 7개 컨테이너로 격리 운영됩니다. 오직 Nginx 80 포트만이 외부에 노출되며, Spring Boot 애플리케이션과 Redis, MySQL은 내부 도커 네트워크에서만 상호작용하도록 설계하여 보안성을 극대화했습니다."

---

## Slide 04: Backend Clean Architecture & DTO Isolation
> **핵심 테제:** 불변 Java Record DTO와 Entity의 엄격한 계층 분리 및 일관된 ApiResponse 규격 수립

### 1. Problem & Challenge
- Entity가 컨트롤러나 외부 API에 직접 노출될 경우 영속성 컨텍스트 의도치 않은 변경, 순환 참조 및 도메인 정보 유출 발생.

### 2. Technical Decision & Architecture
- **불변 Record DTO:** 요청/응답 객체는 Java 17 `record` 타입으로 선언하여 불변성 보장 및 캡슐화 강화.
- **통일된 응답/예외 래퍼:** `ApiResponse<T>(success, data, message, errorCode)` 통일 포맷 및 `@RestControllerAdvice` 기반 `GlobalExceptionHandler` 구축.

### 3. Verification & Result
- `task_progress.md` Phase 1-1 및 1-3 완료 검증 `[IMPLEMENTED]` `[DOCUMENTED]`.
- API 엔드포인트 응답 규격 정합성 검증 완료 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 3.2

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "계층 간 데이터 전송 시 Java 17의 불변 Record DTO를 적용해 Entity와의 결합을 완전히 끊어냈습니다. 또한 모든 API 응답을 ApiResponse 표준 포맷으로 통일하여 클라이언트와의 통신 안정성을 확보했습니다."

---

## Slide 05: Authentication Architecture (JWT & Lifecycles)
> **핵심 테제:** Access Token 1시간 + Refresh Token 7일 분리 및 전송 채널 격리를 통한 보안성 강화

### 1. Problem & Challenge
- Access Token의 수명이 길면 탈취 시 피해가 크고, 수명이 너무 짧으면 잦은 재로그인으로 사용자 경험(UX) 훼손.

### 2. Technical Decision & Architecture
- **Access Token:** 유효기간 3,600,000 ms (1시간), HTTP Request Header (`Authorization: Bearer <token>`)로 전송. JJWT(HMAC-SHA256) 기반 Payload(userId, roles, permissions) 포함.
- **Refresh Token:** 유효기간 604,800,000 ms (7일), XSS 공격 방어를 위해 `HttpOnly`, `Secure`, `SameSite=Strict` Cookie로만 전송.

### 3. Verification & Result
- 토큰 발급 및 파싱 필터링 자동화 테스트(`JwtAuthenticationFilterTest.java`) 통과 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 2.1

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "인증 수명주기는 1시간 만료의 Access Token과 7일 만료의 Refresh Token으로 이원화했습니다. Access Token은 메모리 상에서 헤더로 통신하고, Refresh Token은 XSS 공격을 방어하기 위해 HttpOnly Secure 쿠키로만 격리 전송됩니다."

---

## Slide 06: Advanced Token Security (RTR & Redis Blacklist)
> **핵심 테제:** Refresh Token Rotation(RTR)으로 재사용 공격을 방어하고, Redis Blacklist로 즉시 로그아웃 무효화 달성

### 1. Problem & Challenge
- Refresh Token이 탈취되어 재사용될 경우 무한 세션 연장 가능.
- 사용자가 로그아웃하더라도 이미 발급된 Stateless Access Token은 만료 전까지 유효한 취약점 존재.

### 2. Technical Decision & Architecture
- **Refresh Token Rotation (RTR):** 재발급 요청 시 Redis(`auth:refresh:user:<userId>`)에 저장된 UUID JTI와 일치 여부를 원자적 Lua Script로 검증하고, 검증 즉시 신규 JTI로 교체하며 신규 토큰 세트를 동시 발급. 이미 사용된 구버전 JTI로 재요청 시 즉시 401 반환 및 세션 파기.
- **Redis Token Blacklist:** 로그아웃 요청 시 Access Token JTI를 `blacklist:<jti>` 키로 등록하고 잔여 유효시간(TTL)을 만료시간으로 설정하여 즉시 인가 차단.

### 3. Verification & Result
- `SecurityIntegrationTest.java` (소진된 토큰 재사용 시 401 차단 검증 완료) `[VERIFIED]`.
- `TokenBlacklistServiceTest.java` (블랙리스트 등록 토큰 필터 차단 검증 완료) `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md` Section 3.1 & 3.2

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "핵심 보안 로직인 RTR은 토큰이 재발급될 때마다 기존 JTI를 즉시 무효화하여 토큰 탈취 후 재사용을 방어합니다. 또한 로그아웃 시 Access Token의 남은 시간만큼만 Redis Blacklist에 등록하여, 무상태 JWT 환경에서도 즉시 로그아웃 무효화를 구현했습니다."

---

## Slide 07: Authorization & RBAC Multi-Tier Hierarchy
> **핵심 테제:** User-Role-Permission M:N 정규화 모델 및 Spring Security Filter 기반 세부 리소스 인가 제어

### 1. Problem & Challenge
- 단순 Role(역할) 기반 인가만으로는 세부 기능(메뉴 조회, 데이터 수정, 관리자 권한 등)에 대한 유연한 접근 제어 한계.

### 2. Technical Decision & Architecture
- **M:N 다대다 RBAC 모델:** `users` - `user_roles` - `roles` - `role_permissions` - `permissions`, `roles` - `role_menus` - `menus` 테이블 매핑 정규화.
- **Security Interceptor & Provider:** `UserAuthorityService`를 통해 사용자별 권한 목록을 로드하고, Custom Filter에서 엔드포인트 접근 권한을 검증하여 권한 부족 시 403 Forbidden 반환.

### 3. Verification & Result
- `RbacSecurityIntegrationTest.java` (`ROLE_ADMIN` vs `ROLE_USER` 권한별 403 차단 검증 완료) `[VERIFIED]`.
- `PermissionIntegrationTest.java`, `RolePermissionIntegrationTest.java` 정합성 검증 완료 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 2.2

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "인가는 사용자-역할-퍼미션으로 이어지는 정규화된 M:N RBAC 모델을 구축했습니다. 역할 단위의 거친 제어뿐만 아니라 세부 퍼미션 단위로 Spring Security 인가 필터를 적용하여, 권한 없는 사용자의 관리자 엔드포인트 접근을 403 Forbidden으로 안전하게 차단합니다."

---

## Slide 08: Database Schema & Migration Governance (Flyway)
> **핵심 테제:** Flyway V1~V5 버전 관리 마이그레이션을 통한 무결성 보장 및 자동화된 DDL 이력 통제

### 1. Problem & Challenge
- 로컬 및 배포 환경 간 데이터베이스 DDL 불일치(`ddl-auto: update`의 위험성) 및 스키마 변경 이력 추적 누락 방지 필요.

### 2. Technical Decision & Architecture
- **Flyway 마이그레이션 적용:** `spring.jpa.hibernate.ddl-auto=validate`로 설정하고 모든 테이블 및 시드 데이터는 Flyway 스크립트로만 관리.
- **5단계 스키마 이력:**
  - `V1__init_schema.sql` (기본 DDL)
  - `V2__init_authority_schema.sql` (인가 스키마 확장)
  - `V3__init_common_schema.sql` (공통 엔티티)
  - `V4__insert_permissions.sql` (기본 권한 시드)
  - `V5__insert_test_users.sql` (테스트 사용자 시드)

### 3. Verification & Result
- Spring Boot 기동 시 Flyway V1~V5 자동 마이그레이션 및 정합성 검증 완료 `[IMPLEMENTED]` `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 2.3

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "데이터베이스 형상 관리를 위해 Flyway를 도입하여 V1부터 V5까지 체계적인 스키마 마이그레이션을 구성했습니다. JPA의 ddl-auto는 validate로 잠그고 모든 DDL 변경을 스크립트로 통제하여 환경 간 불일치를 근본적으로 제거했습니다."

---

## Slide 09: Automated Security & Integration Verification
> **핵심 테제:** 10종의 핵심 자동화 단위·통합 테스트 스위트를 구축하여 보안 및 비즈니스 로직 무결성 검증

### 1. Problem & Challenge
- 토큰 갱신, 블랙리스트, 인가 필터 등 복잡한 보안 로직 변경 시 회귀 버그(Regression) 발생 위험.

### 2. Technical Decision & Architecture
- **10종 핵심 테스트 스위트:**
  - Auth: `AuthControllerTest`, `AuthServiceTest`, `JwtAuthenticationFilterTest`, `RefreshTokenRepositoryTest`, `SecurityIntegrationTest`, `TokenBlacklistServiceTest`
  - RBAC: `RbacSecurityIntegrationTest`, `PermissionIntegrationTest`, `RolePermissionIntegrationTest`, `MenuSecurityIntegrationTest`

### 3. Verification & Result
- 10개 핵심 테스트 스위트 전원 통과 (Pass Rate 100%) `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md` Section 2 & 4

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "인증, 인가, 토큰 수명주기 전 영역에 걸쳐 10종의 단위 및 통합 테스트 스위트를 구축했습니다. MockMvc와 통합 테스트 환경을 통해 RTR 리플레이 어택과 블랙리스트 차단이 100% 정상 작동함을 자동화 검증했습니다."

---

## Slide 10: Performance & Stress Testing (k6 Benchmarks)
> **핵심 테제:** k6 기반 70 VU 피크 스트레스 3회 반복 측정 결과 평균 5.64ms 레이턴시 및 0.00% 에러율 달성

### 1. Problem & Challenge
- 동시 접속 증가 시 Nginx-Spring Boot-Redis-MySQL 간 병목 및 스레드 풀 고갈, 커넥션 누수 여부 검증 필요.

### 2. Technical Decision & Architecture
- **k6 부하 시나리오 구성:** 로그인 ➔ 내 정보 조회 ➔ 인가 메뉴 조회 ➔ RTR 토큰 갱신으로 이어지는 실제 사용자 비즈니스 흐름 반영.
- **임계치(Thresholds) 설정:** `http_req_duration: ['p(95)<50', 'avg<20']`, `http_req_failed: ['rate<0.01']`.

### 3. Verification & Result (70 VU 1분 × 3회 스트레스 테스트 실측)
- **5차 Run:** Avg 4.73ms | P95 8.77ms | 469 req/s | Error 0.00% `[VERIFIED]`
- **6차 Run:** Avg 6.01ms | P95 10.61ms | 457 req/s | Error 0.00% `[VERIFIED]`
- **7차 Run:** Avg 6.18ms | P95 10.57ms | 465 req/s | Error 0.00% `[VERIFIED]`
- **3회 산술 평균 Fact:** **Avg 5.64 ms, P95 9.98 ms, 463 req/s, Error Rate 0.00%** (모든 Threshold 통과).

### 4. Evidence Link
- `PR-Files/performance/K6_LOAD_TEST_REPORT.md`
- Source: `26-05adf/docs/performance/k6-load-test.md` Section 3.2

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "k6 부하 테스트 도구를 사용해 70 VU 동시 부하 환경에서 스트레스 테스트를 3회 반복 수행했습니다. 실측 결과 5~7차 3회 산술 평균 5.64ms의 평균 응답시간, 9.98ms의 P95 지연시간, 463 req/s 처리량을 기록하며 0.00%의 에러율을 실측 검증했습니다."

---

## Slide 11: Real-World Incident Troubleshooting (TS 6-Step)
> **핵심 테제:** 개발 및 컨테이너 환경에서 발생한 실측 장애 3건을 표준 6단계 분석으로 근본 원인 해결

### 1. TS-01-REDIS: Redis 타임아웃 지연 및 프론트엔드 블로킹
- **Root Cause:** Lettuce 기본 타임아웃 60초로 인한 스레드 고갈 및 전파.
- **Resolution:** `timeout: 2000ms`로 2초 단축 및 `RedisUnavailableException` 503 에러 핸들링 `[VERIFIED]`.

### 2. TS-001: JWT Refresh 무한 루프 이슈
- **Root Cause:** 클라이언트 인터셉터의 401 재발급 실패 시 탈출 조건(Exit Condition) 결여.
- **Resolution:** Single Flight 토큰 재발급 패턴 구축 및 401 시 즉시 세션 초기화 및 로그인 리다이렉트 `[VERIFIED]`.

### 3. TS-003: Docker 환경 내 Redis localhost 바인딩 실패
- **Root Cause:** 컨테이너 격리 환경에서 `localhost`는 컨테이너 자신을 가리키는 문제.
- **Resolution:** `application.yaml`의 `${SPRING_REDIS_HOST:localhost}` 및 `docker-compose.yml`의 `SPRING_REDIS_HOST: redis` 주입 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/troubleshooting/TS-01-REDIS_TIMEOUT.md`
- `PR-Files/troubleshooting/TS-001_JWT_REFRESH_LOOP.md`
- `PR-Files/troubleshooting/TS-003_DOCKER_REDIS_BINDING.md`

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "실제 발생했던 장애 3건을 6단계 표준(Symptom~Prevention)으로 분석하고 해결했습니다. Redis 장애 시 2초 타임아웃 방어 코드를 적용했고, 토큰 갱신 시 발생할 수 있는 무한 루프를 탈출 조건으로 차단했으며, 도커 네트워크 환경변수 주입을 통해 컨테이너 간 통신 문제를 해결했습니다."

---

## Slide 12: Controlled AI Workflow (SA-1 Governance)
> **핵심 테제:** AI를 맹목적으로 신뢰하는 것이 아니라, 엄격한 컨벤션과 테스트 검증으로 통제하는 AI 협업 프로세스

### 1. Problem & Challenge
- AI 코딩 보조 도구 사용 시 환각(Hallucination), 아키텍처 규칙 위반 및 컨텍스트 오염 발생 위험.

### 2. Technical Decision & Architecture
- **SA-1 Governance & Zero-Chatter:** 사과/미사여구를 배제하고 `diff` 중심의 정밀한 변경만 허용.
- **Documentation-First Policy:** 코드 수정 전 `task_progress.md` 정의 및 완료 후 `changelogs/` 의무 동기화.
- **8-Stage Controlled Lifecycle:** `Requirement -> Context Reading -> Planning -> Agent Delegation -> Verification (JUnit/k6) -> Human Review -> Documentation -> Deployment`.

### 3. Verification & Result
- SA-1 표준 프롬프트 커맨드 4종(`@Task&Log`, `@CodeReview`, `@DocsSync`, `@Troubleshoot`) 정립 및 적용 `[DOCUMENTED]` `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/ai-workflow/AI_WORKFLOW_SPEC.md`
- Source: `SA-1/README.md`, `SA-1/conventions/rules.md`

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "AI 에이전트를 개발에 활용할 때 가장 중요한 것은 통제력입니다. SA-1 저장소의 가이드라인에 따라 Documentation-First 원칙을 수립하고, AI가 작성한 모든 코드는 반드시 JUnit과 k6 테스트를 100% 통과한 후에만 개발자의 승인을 거쳐 커밋되도록 프로세스를 강제했습니다."

---

## Slide 13: Architectural Decisions & Technical Trade-offs
> **핵심 테제:** 보안 강화와 성능 유지 간의 현실적인 엔지니어링 트레이드오프 분석 및 최적점 도출

### 1. Trade-off 1: 무상태(Stateless) vs 실시간 즉시 무효화(Stateful)
- **결정:** Access Token은 1시간 무상태로 검증하여 DB 조회를 배제하고 처리량을 극대화하되, 로그아웃 시에만 Redis Blacklist를 조회하여 보안성과 고성능(P95 9.98ms)의 균형을 달성.

### 2. Trade-off 2: Redis 의존성 결합 vs 시스템 복원력(Resilience)
- **결정:** Redis 단절 시 전체 인증이 블로킹되는 문제를 방지하기 위해 Lettuce 커맨드 타임아웃을 2초로 강제하고 503 Fallback 에러를 즉시 반환하도록 설계.

### 3. Verification & Result
- 부하 테스트(463 req/s)와 장애 복구 시나리오를 통해 트레이드오프 설계의 유효성 검증 완료 `[VERIFIED]`.

### 4. Evidence Link
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md`
- `PR-Files/troubleshooting/TS-01-REDIS_TIMEOUT.md`

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "모든 아키텍처에는 트레이드오프가 존재합니다. 순수 JWT의 단점인 즉시 무효화 불가를 해결하기 위해 Redis Blacklist를 도입하면서도, 성능 저하를 막기 위해 잔여 TTL 방식과 2초 타임아웃 방어선을 설계하여 안정적인 엔지니어링 밸런스를 잡았습니다."

---

## Slide 14: System Limitations & Future Roadmap (PLANNED)
> **핵심 테제:** 현재 아키텍처의 한계를 명확히 인지하고, 사실(Fact)과 계획(Plan)을 엄격히 분리한 로드맵 수립

### 1. 현재 시스템 한계점 (Current Limitations)
- 단일 노드 컨테이너 환경으로 구성되어 있어 대규모 트래픽(1,000+ VU)에 대한 오토스케일링 및 L7 로드밸런서(ALB) 미적용.
- JPA N+1 최적화 코드는 존재하나, 쿼리 수 비교 실측 벤치마크 데이터는 아직 미보유.

### 2. Future Roadmap (`[PLANNED]` 과제)
- **JPA N+1 쿼리 최적화 실측 벤치마크:** Batch Size 및 Fetch Join 적용 전/후 실행 쿼리 수 및 힙 메모리 정밀 측정 `[PLANNED]`.
- **비동기 메시지 큐 (Message Queue):** 대용량 이벤트 분산을 위한 Kafka / RabbitMQ 파이프라인 도입 `[PLANNED]`.
- **프론트엔드 캐싱 고도화:** React Query staleTime/gcTime 정책 및 Route Guard 렌더링 최적화 (Phase 2-2, 2-3) `[PLANNED]`.
- **클라우드 보안:** Production 환경 HashiCorp Vault / AWS KMS 연동 및 Let's Encrypt TLS 자동화 `[PLANNED]`.

### 3. Evidence Link
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` Section 2.6
- Source: `26-05adf/task_progress.md`

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "엔지니어로서 현재 시스템의 한계를 투명하게 공개하는 것은 매우 중요합니다. 대규모 트래픽 스케일아웃, Message Queue를 통한 비동기 처리, 그리고 세부 JPA 쿼리 벤치마크 측정은 PLANNED 로드맵으로 명확히 격리하여 향후 과제로 계획하고 있습니다."

---

## Slide 15: Conclusion & Engineering Identity
> **핵심 테제:** "프레임워크의 원리를 이해하고, 백엔드를 설계하며, 인프라에서 실행하고, 검증과 장애 분석으로 증명하는 엔지니어"

### 1. Portfolio Achievements Summary
- **보안 무결성:** JWT + RTR + Redis Blacklist + RBAC M:N 체계 구축 및 10종 JUnit 테스트 100% 통과 `[VERIFIED]`.
- **성능 및 인프라:** Docker Compose 7개 서비스 격리, k6 스트레스 테스트 70 VU 평균 5.64ms, 0.00% 에러 달성 `[VERIFIED]`.
- **문제 해결 능력:** TS 표준 6단계 기반 Redis 타임아웃, 무한 루프, 도커 네트워크 장애 3건 근본 원인 분석 및 해결 `[VERIFIED]`.
- **AI 프로세스 거버넌스:** SA-1 기반 Documentation-First AI 협업 라이프사이클 정립 `[VERIFIED]`.

### 2. Next Horizon
- 계획된 로드맵을 지속적으로 검증하고, 검증된 사실만을 기록하는 신뢰성 높은 백엔드 엔지니어로 성장하겠습니다.

### 3. Evidence & Repository Matrix
- Source Application: `https://github.com/bluejals13/26-05adf` (`feature/auth@0603@1401`)
- AI & Process: `https://github.com/bluejals13/SA-1` (`main`)
- Evidence & Spec: `https://github.com/bluejals13/PR-1A1` (`main`)

---
> 🎙️ **Speaker Note (발표 스크립트):**
> "단순히 코드를 작성하는 것을 넘어, 보안과 인프라의 원리를 이해하고, 실제 부하 테스트와 장애 분석을 통해 공학적으로 증명할 수 있는 엔지니어가 되겠습니다. 경청해 주셔서 대단히 감사합니다."
