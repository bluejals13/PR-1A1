# Source of Truth Snapshot & Traceability Matrix

- **Snapshot Version:** 1.2.0
- **Snapshot Date:** 2026-09-05
- **Primary Source 1 (Application):** `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`, Commit: `9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f`)
- **Primary Source 2 (AI Agent / Process):** `https://github.com/bluejals13/SA-1` (Branch: `main`, Commit: `4a734a8edd8b670f8d29dc2a42a978ca3877a25f`)
- **Target Workspace:** `https://github.com/bluejals13/PR-1A1` (Branch: `main`, Commit: `c9f88722ad196ef7918240ab1faaaba4a8f64676`)

---

## 1. Status Classification Protocol (5대 상태 정의)

본 저장소(`PR-1A1`)에서 가공 및 참조되는 모든 기술 항목은 아래 5대 상태 분류를 엄격히 준수합니다.

| 상태 태그 | 정의 | 판정 및 적용 기준 |
| :--- | :--- | :--- |
| `[VERIFIED]` | 자동화 테스트나 부하 테스트, 실행 로그로 동작과 수치가 검증 완료된 상태 | JUnit 테스트 통과 확인, k6 실행 결과치 실측 확인 |
| `[IMPLEMENTED]` | 코드가 실제로 작성되어 저장소에 존재하나 검증 수치가 없는 상태 | `26-05adf` 내 소스 코드(.java, .ts, .sql, .yml 등) 파일 확인 |
| `[DOCUMENTED]` | 아키텍처, 설계 컨벤션, 장애 보고서 등 공식 기술 문서에 명시된 상태 | `docs/`, `changelogs/` 내 마크다운 기술 문서 확인 |
| `[PLANNED]` | 향후 개선 예정으로 계획된 상태 (Roadmap) | `task_progress.md` 미완료 항목 또는 향후 로드맵 항목 |
| `[UNKNOWN]` | 현재 소스 코드 및 문서에서 확인되지 않은 상태 | **추측 금지**, 확인 전까지 포트폴리오 인용 절대 불가 |

---

## 2. Source of Truth 실측 팩트 요약 (Fact Base)

### 2.1 Backend & Security Architecture (`26-05adf`)
- **프레임워크 & 런타임:** Java 17, Spring Boot 3.3.2, Gradle 8.14.4, Spring Security 6, Spring Data JPA, JJWT (0.11.5), Flyway, MySQL 8.0, Redis 7.0 `[IMPLEMENTED]`
- **인증 (Authentication):**
  - Stateless JWT Access Token (유효시간: 1시간, Header `Authorization: Bearer <token>` 전달) `[IMPLEMENTED]` `[VERIFIED]`
  - Refresh Token (유효시간: 7일, HttpOnly Secure Cookie 전달, UUID JTI 기반 고유 식별) `[IMPLEMENTED]` `[VERIFIED]`
  - Refresh Token Rotation (RTR): 토큰 재발급 시 기존 JTI 즉시 무효화 및 신규 JTI Redis 적재 `[IMPLEMENTED]` `[VERIFIED]`
  - Token Blacklist: 로그아웃 요청 시 Access Token의 잔여 TTL 동안 Redis Blacklist에 등록하여 즉시 무효화 `[IMPLEMENTED]` `[VERIFIED]`
- **인가 (Authorization & RBAC):**
  - `User - Role - Permission` M:N 다대다 매핑 구조 `[IMPLEMENTED]` `[VERIFIED]`
  - DB Schema (Flyway V1~V5): `V1__init_schema.sql` ~ `V5__insert_test_users.sql` (`users`, `roles`, `permissions`, `user_roles`, `role_permissions`, `menus`, `role_menus`) `[IMPLEMENTED]`
  - Spring Security Custom Provider 및 `UserAuthorityService`를 통한 세부 엔드포인트 권한 인가 필터링 `[IMPLEMENTED]` `[VERIFIED]`
- **응답 및 예외 처리 규격:**
  - Record 기반 불변 DTO 구조 `[IMPLEMENTED]`
  - `ApiResponse<T>` 통일 포맷 및 `GlobalExceptionHandler` 적용 `[IMPLEMENTED]` `[DOCUMENTED]`

---

### 2.2 Performance & Verification Metrics (`26-05adf`)
- **k6 부하 테스트 실측 불변 지표 (Fact - `docs/performance/k6-load-test.md` 70 VU 3회 평균):**
  - **Virtual Users (VU):** `70 VUs` `[VERIFIED]`
  - **Test Duration:** `1 minute (60s)` 지속 부하 `[VERIFIED]`
  - **Throughput:** `463 req/s` `[VERIFIED]`
  - **Average Latency:** `5.64 ms` `[VERIFIED]`
  - **P95 Latency:** `9.98 ms` (`p(95) < 50ms` 임계치 통과) `[VERIFIED]`
  - **Error Rate:** `0.00%` (총 0건 에러, `rate < 1%` 임계치 통과) `[VERIFIED]`
- **부하 시나리오 구성:** `load.test.js`, `stress.test.js`, `spike.test.js`, `soak.test.js`, `read.flow.js`, `user.flow.js`, `admin-flow.js` `[IMPLEMENTED]`
- **자동화 테스트 스위트 (10종 핵심 테스트):**
  - `AuthControllerTest`, `AuthServiceTest`, `JwtAuthenticationFilterTest`, `RefreshTokenRepositoryTest`, `SecurityIntegrationTest`, `TokenBlacklistServiceTest` `[VERIFIED]`
  - `RbacSecurityIntegrationTest`, `PermissionIntegrationTest`, `RolePermissionIntegrationTest`, `MenuSecurityIntegrationTest` `[VERIFIED]`

---

### 2.3 Infrastructure & Observability (`26-05adf`)
- **Container Topology (Docker Compose):**
  - `Nginx` (Port 80): 정적 자원 서빙 및 `/api/*` 리버스 프록시 단일 진입점 `[IMPLEMENTED]`
  - `Spring Boot App` (Port 8080): 내부 통신 격리 `[IMPLEMENTED]`
  - `MySQL 8.0` (Port 3306, 호스트 3307): RDBMS `[IMPLEMENTED]`
  - `Redis 7.0` (Port 6379): In-Memory Token & Cache Store `[IMPLEMENTED]`
  - `Prometheus` (Port 9090) / `VictoriaMetrics` (Port 8428) / `Grafana` (Port 3000): 메트릭 수집 및 시각화 `[IMPLEMENTED]` `[DOCUMENTED]`

---

### 2.4 Troubleshooting Registry (장애 해결 실측 내역)
모든 트러블슈팅 사례는 TS 표준 6단계 (`Symptom → Impact → Diagnosis → Root Cause → Resolution → Prevention`)로 관리됩니다.

1. **[TS-01-REDIS] Redis 장애 시 Lettuce 커맨드 타임아웃 지연 및 프론트엔드 블로킹**
   - **Symptom:** Redis 컨테이너 다운 시 커맨드 1분 블로킹 발생 및 프론트엔드 흰 화면(Blank Screen) 노출 `[DOCUMENTED]`
   - **Root Cause:** Redis 기본 커맨드 타임아웃 미설정(기본 1분) 및 토큰 검증 필터 블로킹 `[DOCUMENTED]`
   - **Resolution:** Lettuce 커맨드 타임아웃을 2초로 단축, Redis 접근 예외 처리 래핑, 프론트엔드 Error Boundary 보강 `[VERIFIED]` `[DOCUMENTED]`
2. **[TS-001] JWT Refresh 무한 루프 이슈**
   - **Symptom:** Refresh Token 갱신 요청 실패 시 클라이언트 인터셉터와 서버 간 무한 재시도 루프 발생 `[DOCUMENTED]`
   - **Root Cause:** 재발급 실패(401) 응답에 대한 클라이언트 재시도 탈출 조건 미비 및 RTR JTI 즉시 만료 처리 타이밍 이슈 `[DOCUMENTED]`
   - **Resolution:** 토큰 갱신 실패 시 즉시 쿠키 및 인증 상태를 초기화하고 로그인 페이지로 리다이렉트하는 탈출 조건 구현 `[VERIFIED]` `[DOCUMENTED]`
3. **[TS-003] Docker 환경 내 Redis localhost 바인딩 문제**
   - **Symptom:** Docker Compose 환경에서 Spring Boot가 Redis 컨테이너(`localhost:6379`)에 연결하지 못하고 커넥션 거부 발생 `[DOCUMENTED]`
   - **Root Cause:** 컨테이너 격리 환경에서 `localhost`는 컨테이너 자신을 가리키므로, Docker Network 서비스명(`redis`)을 지정해야 함 `[DOCUMENTED]`
   - **Resolution:** Spring Boot `application.yaml`의 Redis host 설정을 환경변수 기반(`SPRING_REDIS_HOST: redis`)으로 분리 `[VERIFIED]` `[DOCUMENTED]`

---

### 2.5 AI-Assisted Engineering Workflow (`SA-1`)
- **Zero-Chatter Policy:** 서론/미사여구 배제, diff 및 코드 변경 중심 정밀 협업 `[DOCUMENTED]`
- **Documentation-First Policy:** 코드 변경 전후 `task_progress.md` 및 `changelogs/` 동기화 의무화 `[DOCUMENTED]`
- **AI 엔지니어링 8단계 라이프사이클:**
  ```text
  Requirement ➔ Context Reading ➔ Analysis & Planning ➔ Agent Delegation ➔ Verification (JUnit/k6) ➔ Human Review ➔ Documentation
  ```
- **표준 프롬프트 커맨드 세트:** Task&Log, Code Review, Docs Sync, Troubleshooting `[DOCUMENTED]`

---

### 2.6 Planned / Unverified (절대 구현 완료로 표기 금지)
- **JPA N+1 쿼리 최적화 세부 벤치마크 수치:** 계획 과제 `[PLANNED]`
- **Message Queue (Kafka / RabbitMQ) 비동기 처리 도입:** 미구현 `[PLANNED]`
- **분산 캐시 클러스터링 및 다중 노드 레플리케이션:** 미구현 `[PLANNED]`

---

### 3. Claim-to-Evidence Traceability Matrix (추적성 매트릭스)

| Claim ID | 영역 (Domain) | 엔지니어링 주장 (Claim) | 소스 구현 위치 (Implementation) | 검증 테스트/증거 (Verification) | 상태 |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **CLM-SEC-001** | Security | Access Token 1시간 만료, Header Bearer 전송 | `com.example.demo.auth.jwt.JwtProvider` | `JwtAuthenticationFilterTest.java` | `[VERIFIED]` |
| **CLM-SEC-002** | Security | Refresh Token 7일 만료, RTR 적용 및 JTI Redis 저장 | `com.example.demo.auth.security.RefreshTokenRepository` | `RefreshTokenRepositoryTest.java` | `[VERIFIED]` |
| **CLM-SEC-003** | Security | 로그아웃 시 Access Token Redis Blacklist 등록 | `com.example.demo.auth.security.TokenBlacklistService` | `TokenBlacklistServiceTest.java` | `[VERIFIED]` |
| **CLM-RBAC-001** | RBAC | User-Role-Permission M:N 권한 계층 모델 | `com.example.demo.iam.*.domain.*`, Flyway `V1~V5__*.sql` | `RbacSecurityIntegrationTest.java` | `[VERIFIED]` |
| **CLM-PERF-001** | Performance | 70 VUs 동시 부하 시 평균 5.64ms, P95 9.98ms, 0% Error | `k6/scenarios/load.test.js`, `thresholds.js` | k6 실행 결과 리포트 (`docs/performance/`) | `[VERIFIED]` |
| **CLM-INFRA-001**| Infra | Nginx Reverse Proxy 단일 진입점 및 포트 격리 | `docker-compose.yml`, `nginx/default.conf` | Docker Compose 서비스 기동 및 라우팅 | `[IMPLEMENTED]` |
| **CLM-TS-001**   | Incident | Redis 단절 시 커맨드 타임아웃 2초 단축 및 방어 | Spring Data Redis 설정 (`application.yaml`) | `TS-01-REDIS` 장애 보고서 및 회복 검증 | `[VERIFIED]` |
| **CLM-TS-002**   | Incident | JWT Refresh 실패 시 무한 루프 차단 | 클라이언트 API 인터셉터 (`frontend/src/api/http.ts`) | `TS-001` 장애 분석 및 예외 핸들링 검증 | `[VERIFIED]` |
| **CLM-TS-003**   | Incident | Docker 네트워크 내 서비스명 기반 Redis 바인딩 | `docker-compose.yml` (`SPRING_REDIS_HOST: redis`) | `TS-003` 컨테이너 간 통신 검증 | `[VERIFIED]` |
| **CLM-AI-001**   | AI Workflow | 8단계 AI 협업 프로세스 및 Zero-Chatter | `SA-1/conventions/rules.md`, `changelogs/` | `SA-1` 변경 이력 및 커맨드 규격서 | `[DOCUMENTED]` |
| **CLM-ROAD-001** | Roadmap | N+1 쿼리 정량 벤치마크 및 Message Queue 도입 | 미구현 (계획 과제) | `task_progress.md` 로드맵 | `[PLANNED]` |
