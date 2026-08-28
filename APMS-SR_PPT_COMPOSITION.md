# APMS.SR Portfolio Presentation Deck Composition (14 Slides)

- **Document ID:** APMS-SR-PPT-COMP-01
- **Target Repository:** `PR-1A1`
- **Output Artifact:** `PRD-PO/html/ppt.html`
- **Design Paradigm:** Dark Engineering Minimalist, High Visual Density, Single Thesis per Slide, 5-10s Cognitive Absorption

---

## 1. 14-Slide Story Arc Overview

```text
[ Problem & Context ]
  Slide 01: Title / Engineering Profile & Zero-Hallucination Protocol
  Slide 02: Problem & Architectural Goal (무상태 인증의 보안 딜레마)
       │
[ Architecture & Design ]
  Slide 03: Full System Architecture & Container Topology (7 Containers)
  Slide 04: Security Architecture Before / After (단순 JWT vs 3중 보안 계층)
  Slide 05: JWT / RTR / Blacklist Core Sequence Flow
       │
[ Implementation & Verification ]
  Slide 06: Security Verification (10 Test Suites 100% Pass & Code Evidence)
  Slide 07: Incident Analysis (3 Real Failures Before/After & 6-Step TS)
  Slide 08: Docker 7-Container Network Isolation & DNS Resolution
  Slide 09: MySQL vs Redis Role & Storage Strategy Comparison
  Slide 10: Performance Metric Hero & k6 70 VU Benchmark (5~7차 실측치)
       │
[ Observability & Process ]
  Slide 11: Observability Pipeline (Actuator → Prometheus → VictoriaMetrics → Grafana [PARTIAL])
  Slide 12: AI-Assisted Engineering Workflow (SA-1 8-Stage Lifecycle)
       │
[ Synthesis & Boundary ]
  Slide 13: Claim-to-Evidence Traceability Matrix (엔지니어링 주장-증거 맵핑)
  Slide 14: FACT vs ROADMAP (검증 완료 사실과 계획 로드맵의 엄격한 분리)
```

---

## 2. Slide-by-Slide Specifications

---

### Slide 01: Title / Cover
- **Slide Title:** Backend & Infrastructure Engineering Portfolio
- **Subtitle:** Stateless JWT + RTR + Redis Blacklist 실시간 세션 제어 및 k6 부하 검증 기반 백엔드 시스템
- **Engineering Thesis:** "프레임워크 원리 이해부터 컨테이너 인프라 격리, 부하 검증, 장애 해결, AI 워크플로우 통제까지 전 주기를 관통하는 엔지니어링 포트폴리오"
- **Meta Cards:**
  - Application Source: `26-05adf` (Branch: `feature/auth@0603@1401`)
  - AI Process Source: `SA-1` (Branch: `main`)
  - Target & Evidence Workspace: `PR-1A1`
  - Protocol: `[SOURCE OF TRUTH VERIFIED]` Zero-Hallucination
- **Visual Structure:** Dark Hero Layout with glowing pulse badge, metadata grid, and clear navigation hints.
- **Speaker Note:**
  > "반갑습니다. 백엔드 및 인프라 엔지니어링 포트폴리오 발표를 시작하겠습니다. 본 발표는 26-05adf 애플리케이션 저장소와 SA-1 AI 프로세스 저장소의 실측 팩트만을 근거로 작성되었으며, 단 하나의 허위 수치 없이 모든 주장이 테스트와 코드로 증명된 사실만을 전달합니다."

---

### Slide 02: Problem & Architectural Goal
- **Slide Title:** Problem & Goal: 무상태(Stateless) 인증의 보안 딜레마
- **Core Dilemma:** 무상태 JWT는 확장성이 뛰어나지만, **'즉시 세션 무효화 불가'**와 **'토큰 탈취 시 Replay Attack 취약성'**이라는 태생적 한계를 지님.
- **Three Core Engineering Challenges:**
  1. **Token Revocation Gap:** 로그아웃 후에도 만료 시간까지 Access Token이 유효함.
  2. **Replay Attack Vulnerability:** 긴 유효기간의 Refresh Token이 탈취될 경우 장기간 비인가 접근 가능.
  3. **Container Isolation Pitfall:** Docker 환경 내 컨테이너 간 localhost 바인딩 실패 및 네트워크 고립.
- **Resolution Strategy Flow:**
  `Problem (무상태의 한계)` ➔ `Decision (RTR + In-Memory Blacklist)` ➔ `Implementation (Spring Security + Redis)` ➔ `Verification (JUnit 10종 + k6)` ➔ `Result (5.64ms / 0% Error)`
- **Visual Structure:** 3-Column Problem Cards + Horizontal Engineering Solution Flow.
- **Speaker Note:**
  > "JWT 기반 인증은 서버의 세션 저장 부담을 덜어주지만, 발급된 토큰을 중간에 무효화할 수 없다는 치명적인 보안 맹점이 있습니다. 저희는 RTR과 Redis Blacklist를 결합하여 무상태의 확장성을 해치지 않으면서도 실시간 세션 통제력을 확보하는 아키텍처를 수립했습니다."

---

### Slide 03: Full System Architecture & Container Topology
- **Slide Title:** System Architecture: 7-Container Topology & Port Isolation
- **Core Message:** Nginx 단일 진입점을 통한 외부 포트 최소화 및 Docker 내부 브리지 네트워크 격리
- **Container Registry & Port Specification:**
  - `Nginx (Port 80)`: 외부 유일 진입점 (Public Gateway), 정적 SPA 서빙 및 `/api/*` 리버스 프록시 `[IMPLEMENTED]`
  - `Spring Boot App (Port 8080)`: 내부 브리지 격리, Spring Security 6, JJWT, JPA `[IMPLEMENTED]`
  - `MySQL 8.0 (Port 3306, 호스트 3307)`: 영속 RDBMS, Flyway V1~V5 스키마 형상 관리 `[IMPLEMENTED]`
  - `Redis 7.0 (Port 6379)`: In-Memory Token & TTL Cache Store `[IMPLEMENTED]`
  - `Prometheus (Port 9090)`: `/actuator/prometheus` 메트릭 스크랩 `[IMPLEMENTED]`
  - `VictoriaMetrics (Port 8428)`: 시계열 데이터 영속화 스토리지 `[IMPLEMENTED]`
  - `Grafana (Port 3000)`: 모니터링 대시보드 `[IMPLEMENTED / PARTIAL]`
- **Visual Structure:** Detailed Pure SVG/CSS Architecture Topology Diagram with Network Boundary box, Port labels, and Traffic Arrows.
- **Speaker Note:**
  > "전체 시스템은 7개의 도커 컨테이너로 구성됩니다. 외부로는 Nginx 포트 80만 노출되며, 모든 백엔드와 스토리지, 모니터링 스택은 도커 내부 브리지 네트워크로 격리되어 보안성과 가용성을 동시에 달성했습니다."

---

### Slide 04: Security Architecture Before / After
- **Slide Title:** Security Architecture: Simple JWT vs 3-Layer Defense
- **Comparison Breakdown:**
  - **BEFORE (Simple JWT):**
    - Stateless Only (서버 제어 불가)
    - 로그아웃 후에도 Access Token 잔여 시간 동안 API 호출 가능
    - Refresh Token 고정 ➔ 탈취 시 7일간 지속 공격 노출
    - 인가 모델 미흡 (단순 Role 체크)
  - **AFTER (3-Layer Defense System):**
    - `Layer 1: Access Token (1h)` Header Bearer 전송 + 무상태 인가
    - `Layer 2: Refresh Token Rotation (7d)` HttpOnly Cookie + Redis rt:<userId> JTI 1회용 소진 + Replay Attack 즉시 차단 `[VERIFIED]`
    - `Layer 3: Redis Blacklist` 로그아웃 시 bl:<token> 잔여 TTL 저장 + 인가 필터 즉시 거부 `[VERIFIED]`
    - `Layer 4: M:N RBAC` User-Role-Permission 다대다 세부 인가 통제 `[VERIFIED]`
- **Visual Structure:** Split Before/After Box Comparison + Security Layer Stack Diagram.
- **Speaker Note:**
  > "단순 JWT 구조에서는 토큰이 탈취되면 서버가 대처할 방법이 없습니다. 이를 해결하기 위해 1회용 Refresh Token Rotation과 로그아웃 즉시 잔여 수명만큼만 메모리에 등재하는 Redis Blacklist를 도입하여 무상태 인증에 실시간 제어력을 부여했습니다."

---

### Slide 05: JWT / RTR / Blacklist Core Sequence Flow
- **Slide Title:** Security Flow: Authentication, Rotation & Revocation Lifecycle
- **Step-by-Step Flow:**
  1. **Login:** Client ➔ Server 인증 성공 시 Access Token(Header) + Refresh Token(Cookie, Redis `rt:user1` 저장) 발급
  2. **API Access:** Bearer Access Token으로 `/api/*` 요청 ➔ JwtAuthenticationFilter 검증 및 SecurityContext 주입
  3. **RTR Refresh:** Access 만료 시 `/api/auth/refresh` 호출 ➔ 기존 JTI 검증 후 즉시 Redis에서 삭제 ➔ 신규 JTI 쌍 동시 발급
  4. **Replay Attack Block:** 이미 소진된 구버전 JTI로 재요청 ➔ Redis 불일치 감지 ➔ 즉시 401 `INVALID_REFRESH_TOKEN` 반환 및 세션 파기 `[VERIFIED]`
  5. **Logout Blacklist:** `/api/auth/logout` 호출 ➔ Access Token의 잔여 TTL을 계산하여 `bl:<token>`으로 Redis 적재 ➔ 이후 요청 시 인가 필터에서 차단 `[VERIFIED]`
- **Visual Structure:** Pure CSS/SVG Swimlane Sequence Diagram (Client / Nginx / Spring Boot / Redis).
- **Speaker Note:**
  > "토큰 라이프사이클의 핵심은 RTR 재발급 시 기존 토큰이 즉시 무효화된다는 점입니다. 공격자가 가로챈 구버전 토큰으로 접근할 경우 서버는 즉시 401 에러를 반환하고 세션을 종료시킵니다. 로그아웃 또한 잔여 TTL만큼만 블랙리스트를 유지하여 메모리 낭비를 원천 차단합니다."

---

### Slide 06: Security Verification (10 Test Suites 100% Pass)
- **Slide Title:** Security Verification: 10 Core Test Suites & Code Evidence
- **Hero Banner:** 10 / 10 Test Suites 100% PASS `[VERIFIED]`
- **Top 3 Verified Evidence Deep-Dives:**
  1. **`SecurityIntegrationTest.java` (RTR Replay Attack 차단 검증):**
     - 소진된 Refresh Token 재사용 시 `mockMvc`를 통해 HTTP 401 Unauthorized 및 `INVALID_REFRESH_TOKEN` 에러 코드 반환 검증 완료.
  2. **`TokenBlacklistServiceTest.java` (블랙리스트 즉시 차단 검증):**
     - 로그아웃된 Access Token에 잔여 TTL(1800s)을 부여하여 Redis 적재 후 `isBlacklisted()` 판정 True 검증 완료.
  3. **`RbacSecurityIntegrationTest.java` (권한별 403 Forbidden 인가 검증):**
     - `ROLE_USER` 권한 계정으로 관리자 전용 엔드포인트 접근 시 403 Forbidden 차단 검증 완료.
- **Summary Grid (7 Additional Suites):**
  `AuthControllerTest`, `AuthServiceTest`, `JwtAuthenticationFilterTest`, `RefreshTokenRepositoryTest`, `PermissionIntegrationTest`, `RolePermissionIntegrationTest`, `MenuSecurityIntegrationTest` (ALL PASS)
- **Visual Structure:** 3 Featured Code/Assertion Cards + 7-Badge Verification Grid.
- **Speaker Note:**
  > "설계된 보안 기능은 10개의 단위 및 통합 테스트 스위트를 통해 100% 검증되었습니다. 특히 RTR 토큰 재사용 공격 차단과 로그아웃 토큰의 블랙리스트 필터링, 그리고 RBAC 권한 분기는 실제 MockMvc 통합 테스트로 무결성을 입증했습니다."

---

### Slide 07: Incident Analysis (3 Real Failures Before/After)
- **Slide Title:** Incident Troubleshooting: TS 6-Step Standard Root Cause Resolution
- **Standard Process:** `Symptom ➔ Impact ➔ Diagnosis ➔ Root Cause ➔ Resolution ➔ Prevention`
- **3 Real Incidents Resolved:**
  - **[TS-01-REDIS] Redis 다운 시 Lettuce 커맨드 타임아웃 60초 블로킹 `[VERIFIED]`**
    - *Root Cause:* Lettuce 기본 타임아웃 60초 미설정 및 스레드 고갈
    - *Resolution:* `application.yml`에 `timeout: 2000ms` 단축 및 503 `REDIS_UNAVAILABLE` 명확한 예외 반환
  - **[TS-001] JWT Refresh 실패 시 클라이언트-서버 간 401 무한 루프 `[VERIFIED]`**
    - *Root Cause:* 토큰 갱신 401 실패 시 Axios 인터셉터 내 탈출 조건(Exit Condition) 누락
    - *Resolution:* 갱신 실패 시 즉시 인증 상태를 초기화하고 로그인 화면으로 리다이렉트하는 탈출 로직 구현
  - **[TS-003] Docker Compose 내 Redis localhost 바인딩 연결 거부 `[VERIFIED]`**
    - *Root Cause:* 컨테이너 격리 환경에서 `localhost`는 컨테이너 자신(루프백)을 가리키는 문제
    - *Resolution:* `application.yml`을 `${SPRING_REDIS_HOST:localhost}`로 환경변수화하고 Docker 서비스명(`redis`) 주입
- **Visual Structure:** 3-Column Before/After Incident Cards with Log Snippets and Configuration Diff.
- **Speaker Note:**
  > "실제 개발 과정에서 발생한 세 가지 핵심 장애를 TS 표준 6단계 프로세스로 해결했습니다. Redis 다운 시 60초간 블로킹되던 문제를 2초 타임아웃으로 격리했고, 클라이언트의 무한 401 루프를 차단했으며, 도커 컨테이너 격리로 인한 호스트 바인딩 이슈를 환경변수 기반 아키텍처로 정상화했습니다."

---

### Slide 08: Docker 7-Container Network Isolation & DNS Resolution
- **Slide Title:** Infrastructure: Network Isolation & Service Name DNS
- **Core Facts:**
  - Bridge Network 내에서 컨테이너 간 통신은 IP가 아닌 Docker 내장 DNS(`backend`, `mysql`, `redis` 등)로 해결
  - 외부 호스트 노출 포트 최소화 (Only 80 Public Gateway, MySQL 3307은 개발 디버깅 전용)
  - 12-Factor App 원칙 준수: 환경변수를 통한 환경 격리
- **Network Traffic Matrix:**
  - Client ➔ Nginx: Port 80 (Public)
  - Nginx ➔ Backend: `http://backend:8080/api/` (Docker Internal)
  - Backend ➔ MySQL: `jdbc:mysql://mysql:3306/demo` (Docker Internal)
  - Backend ➔ Redis: `redis:6379` (Docker Internal)
  - Prometheus ➔ Backend: `http://backend:8080/actuator/prometheus` (Docker Internal)
- **Visual Structure:** Container Isolation Diagram with Docker Bridge boundaries and internal DNS routes.
- **Speaker Note:**
  > "컨테이너 환경에서는 IP 주소가 유동적으로 변하므로 도커 내장 DNS 서비스명을 기반으로 상호 연결해야 합니다. TS-003을 해결하며 확립한 환경변수 주입 방식을 통해 로컬 환경과 도커 프로덕션 환경 간 무결한 네트워크 격리를 구축했습니다."

---

### Slide 09: MySQL vs Redis Role & Storage Strategy Comparison
- **Slide Title:** Data Architecture: Persistent RDBMS vs In-Memory Session
- **Storage Tiering Decision:**
  - **MySQL 8.0 (영속 데이터 및 정규화 스키마):**
    - 영속성 보장 (ACID 트랜잭션)
    - Flyway V1~V5 기반 버전 관리 (`users`, `roles`, `permissions`, `menus`)
    - User ↔ Role ↔ Permission 다대다 정규화 매핑
  - **Redis 7.0 (In-Memory 고속 세션 & TTL 캐시):**
    - 고속 메모리 I/O (Sub-millisecond)
    - Key-Value 구조 (`rt:<userId>`: JTI, `bl:<token>`: logout)
    - 자동 만료 메커니즘 (TTL 7일 / 잔여 Access Token TTL)
- **Visual Structure:** Side-by-Side Architectural Comparison Table with Data Flow Icons.
- **Speaker Note:**
  > "영속적인 비즈니스 도메인 데이터와 정규화된 권한 모델은 MySQL과 Flyway로 엄격히 통제하고, 밀리초 단위의 고속 조회가 필요한 RTR 토큰과 블랙리스트는 Redis의 TTL 기능을 활용하여 분리했습니다. 이로써 RDBMS 부하를 최소화하면서도 고속 인증을 달성했습니다."

---

### Slide 10: Performance Metric Hero & k6 70 VU Benchmark
- **Slide Title:** Performance Benchmark: k6 70 VU Stress Test Verification
- **Immutable Fact Metrics (70 VU / 1 Minute / 3-Run Average):**
  - **Virtual Users:** `70 VUs` `[VERIFIED]`
  - **Average Latency:** `5.64 ms` (`avg < 20ms` 임계치 대비 71.8% 여유) `[VERIFIED]`
  - **P95 Latency:** `9.98 ms` (`p(95) < 50ms` 임계치 대비 80.0% 여유) `[VERIFIED]`
  - **Throughput:** `463 req/s` (총 27,000+ Requests 처리) `[VERIFIED]`
  - **Error Rate:** `0.00%` (0 Failures, `rate < 1%` 임계치 통과) `[VERIFIED]`
- **3-Run Measured Benchmark Data:**
  - Run 5 (1m): Avg 4.73ms | P95 8.77ms | 469 req/s | Error 0.00%
  - Run 6 (1m): Avg 6.01ms | P95 10.61ms | 457 req/s | Error 0.00%
  - Run 7 (1m): Avg 6.18ms | P95 10.57ms | 465 req/s | Error 0.00%
- **Load Scenario Flow:**
  `Login (/api/auth/login)` ➔ `Me Info (/api/users/me)` ➔ `Menus (/api/menus)` ➔ `Token Refresh (/api/auth/refresh)`
- **Visual Structure:** 4 Metric Hero Cards + Run 5~7 Comparison Table + Threshold Compliance Gauges.
- **Speaker Note:**
  > "k6 부하 테스트 결과, 70명의 가상 사용자가 1분간 지속적으로 요청을 주입하는 환경에서 평균 응답속도 5.64ms, P95 9.98ms, 초당 463건의 처리량을 기록했습니다. 모든 차수에서 에러율 0.00%로 설정된 성능 임계치를 완벽히 충족했습니다."

---

### Slide 11: Observability Pipeline (PARTIAL)
- **Slide Title:** Observability Pipeline: Metrics Collection & Status Transparency
- **Status Classification:** `[IMPLEMENTED]` (Prometheus / VictoriaMetrics) / `[PARTIAL]` (Grafana Dashboard)
- **Pipeline Architecture:**
  - `Spring Boot Actuator` ➔ Micrometer 메트릭 노출 (`/actuator/prometheus`) `[VERIFIED]`
  - `Prometheus (Port 9090)` ➔ 15s 주기 풀링 스크랩 `[IMPLEMENTED]`
  - `VictoriaMetrics (Port 8428)` ➔ Prometheus Remote Write 영속화 `[IMPLEMENTED]`
  - `Grafana (Port 3000)` ➔ DataSource 연결 및 대시보드 시각화 `[PARTIAL]`
- **Strict Guardrail Note:**
  > Grafana 대시보드 연동은 구현되어 있으나, 실시간 알람 및 정밀 모니터링 체계는 완전 검증이 아니므로 `[PARTIAL]` 상태로 투명하게 공개합니다.
- **Visual Structure:** Horizontal Pipeline Flow Diagram + Verified vs Partial Status Cards.
- **Speaker Note:**
  > "애플리케이션의 헬스체크와 메트릭은 Actuator와 Prometheus, VictoriaMetrics 시계열 DB로 수집됩니다. k6 부하 중에도 JVM Heap과 DB 커넥션 풀이 안정적으로 유지됨을 확인했습니다. 다만 Grafana 대시보드는 현재 구성 단계이므로 '부분 구현(PARTIAL)'으로 명확히 구분합니다."

---

### Slide 12: AI-Assisted Engineering Workflow (SA-1)
- **Slide Title:** AI Engineering Governance: SA-1 Controlled 8-Stage Lifecycle
- **Core Thesis:** "AI를 맹목적으로 신뢰하는 것이 아닌, 개발자의 통제 하에 둔 엔지니어링 도구로 활용"
- **8-Stage Lifecycle Workflow:**
  1. `Requirement`: 명확한 태스크 정의
  2. `Context Reading`: 아키텍처 및 기존 코드 컨벤션 분석
  3. `Planning`: 변경 파일 목록 및 단계별 계획 수립
  4. `Agent Delegation`: 최소 단위 정밀 코드 변경 위임
  5. `Verification`: JUnit 10종 및 k6 부하 검증 수행
  6. `Human Review`: 개발자의 최종 코드 승인
  7. `Documentation`: `changelogs/` 변경 이력 의무 동기화
  8. `Deployment`: 컨테이너 빌드 및 옵저버빌리티 관측
- **Key Policies:** `Zero-Chatter Policy` (미사여구 배제, diff 중심) / `Documentation-First`
- **Visual Structure:** 8-Step Circular/Horizontal Pipeline Process Diagram + Governance Policy Highlights.
- **Speaker Note:**
  > "SA-1 리포지토리의 거버넌스 규칙에 따라 AI Agent를 개발 프로세스에 통합했습니다. 요구사항 분석부터 검증, 문서화까지 8단계 라이프사이클을 거치며, AI가 작성한 코드는 반드시 JUnit과 k6 테스트를 거쳐 개발자의 승인 하에만 반영됩니다."

---

### Slide 13: Claim-to-Evidence Traceability Matrix
- **Slide Title:** Verification Matrix: Direct Claim-to-Evidence Mapping
- **Traceability Mapping:**
  - **[Security]** RTR 토큰 재발급 및 탈취 방어 ➔ `AuthService.java` ➔ `SecurityIntegrationTest.java` (`[VERIFIED]`)
  - **[Security]** 로그아웃 즉시 Blacklist 등록 ➔ `TokenBlacklistService.java` ➔ `TokenBlacklistServiceTest.java` (`[VERIFIED]`)
  - **[RBAC]** User-Role-Permission 다대다 인가 ➔ `UserAuthorityService.java` ➔ `RbacSecurityIntegrationTest.java` (`[VERIFIED]`)
  - **[Performance]** 70 VU 시 평균 5.64ms, P95 9.98ms, 0% Error ➔ `k6/scenarios/load.test.js` ➔ k6 실행 결과 리포트 (`[VERIFIED]`)
  - **[Infrastructure]** Nginx 단일 진입점 및 도커 네트워크 격리 ➔ `nginx/default.conf`, `docker-compose.yml` ➔ TS-003 패치 검증 (`[VERIFIED]`)
  - **[Incident]** Redis 다운 시 2s 타임아웃 차단 ➔ `application.yml` ➔ `TS-01-REDIS` 장애 보고서 (`[VERIFIED]`)
- **Visual Structure:** Interactive-style Claim ➔ Code ➔ Test ➔ Status Mapping Table with Visual Connectors.
- **Speaker Note:**
  > "본 포트폴리오에서 제시하는 모든 보안, 성능, 인프라 주장은 소스 코드의 구현 위치와 이를 검증한 자동화 테스트 파일로 1:1 맵핑됩니다. 증거가 없는 주장은 일체 포함하지 않았습니다."

---

### Slide 14: FACT vs ROADMAP (Strict Boundary)
- **Slide Title:** Architectural Boundary: Verified FACT vs Future ROADMAP
- **Clear Two-Column Separation:**
  - **LEFT COLUMN: VERIFIED FACT (현재 검증 완료된 엔지니어링 자산)**
    - Stateless JWT + RTR + Redis Blacklist 실시간 세션 통제 `[VERIFIED]`
    - M:N RBAC 다계층 권한 인가 모델 `[VERIFIED]`
    - Docker Compose 7개 컨테이너 네트워크 격리 `[IMPLEMENTED]`
    - k6 70 VU 동시 부하 평균 5.64ms, 에러 0.00% `[VERIFIED]`
    - JUnit 10개 핵심 테스트 스위트 100% Pass `[VERIFIED]`
    - 3대 핵심 장애 TS 표준 6단계 해결 `[VERIFIED]`
  - **RIGHT COLUMN: FUTURE ROADMAP (미구현 계획 과제 - 과장 금지)**
    - `[PLANNED]` JPA N+1 쿼리 최적화 정량 벤치마크 측정
    - `[PLANNED]` Apache Kafka / RabbitMQ 비동기 메시지 큐 파이프라인
    - `[PLANNED]` Redis Cluster 분산 캐시 및 다중화
    - `[PLANNED]` OWASP ZAP 모의 침투 보안 테스트 파이프라인
    - `[PLANNED]` Kubernetes 클러스터 오케스트레이션 및 HPA
    - `[PLANNED]` SSL/TLS Production 인증서 (HTTPS) 적용
    - `[PLANNED]` 1,000+ VU 분산 부하 테스트
- **Visual Structure:** Solid Border (Verified Fact, Green Accent) vs Dashed Border (Roadmap, Amber Accent) Split Screen.
- **Speaker Note:**
  > "마지막으로 구현 완료된 사실과 향후 계획을 명확히 분리합니다. 70 VU 부하 환경과 보안 메커니즘은 완벽히 검증되었으며, JPA N+1 정량 벤치마크나 분산 메시지 큐, 쿠버네티스 등은 다음 단계의 로드맵으로 관리하고 있습니다. 경청해 주셔서 감사합니다."
