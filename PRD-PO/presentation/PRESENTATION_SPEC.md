# Presentation Specification: Backend & Infrastructure Portfolio Deck

- **Document ID:** SPEC-PRES-01
- **Target Audience:** 백엔드/인프라 테크 리드, 시니어 개발자, 기술 면접관, 프로젝트 평가자
- **Slide Count:** 15 Slides (1 Slide, 1 Core Message Principle)
- **Source of Truth Base:**
  - `PRD-PO/presentation/source/01_PROJECT_OVERVIEW.md` ~ `11_LIMITATIONS_AND_ROADMAP.md`
  - `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`

---

## 1. Presentation Goal & Story Arc

### 1.1 Goal
본 발표자료는 단순한 기능 나열이나 라이브러리 조합을 소개하는 것이 아니라, **"백엔드 핵심 메커니즘을 설계하고, 컨테이너 인프라에서 격리 실행하며, 자동화 테스트 및 실측 부하 검증을 수행하고, 실측 장애를 6단계로 분석하며, 통제된 AI 프로세스를 활용하는 신뢰할 수 있는 엔지니어링 역량"**을 증명하는 데 목적이 있습니다.

### 1.2 Narrative Story Arc
```text
Problem (도전 과제)
 ➔ Solution (해결 방안)
   ➔ Architecture (시스템 및 포트 격리)
     ➔ Implementation (클린 코드 & DB 거버넌스)
       ➔ Security (JWT / RTR / Redis Blacklist / RBAC)
         ➔ Verification (10종 자동화 테스트)
           ➔ Performance (k6 70 VU 실측치)
             ➔ Engineering Decision & Troubleshooting (장애 분석 및 트레이드오프)
               ➔ AI Workflow (SA-1 통제 프로세스)
                 ➔ Limitations & Roadmap (한계와 로드맵)
```

---

## 2. Core Messages

1. **보안과 성능의 균형 (Security & Performance Balance):**
   Stateless JWT의 고성능(P95 9.98ms)을 유지하면서도, RTR(Refresh Token Rotation)과 Redis Blacklist를 결합하여 토큰 탈취 방어 및 안정적인 실시간 세션 통제력을 확보했습니다.
2. **실측 기반의 무결성 검증 (Empirical Verification):**
   주관적 주장을 배제하고 10종의 자동화 단위/통합 테스트와 k6 70 VU 부하 테스트(평균 5.64ms, 에러율 0.00%)를 통해 기계적으로 검증된 사실만을 제시합니다.
3. **장애 분석 및 통제된 엔지니어링 프로세스 (Resilience & Controlled AI):**
   실제 발생한 3건의 장애를 6단계 표준(Symptom~Prevention)으로 근본 해결하였으며, SA-1 거버넌스 하에 AI를 개발자의 엄격한 통제 도구로 통합했습니다.

---

## 3. Slide Plan (15 Slides Blueprint)

### Slide 01: Project Identity & Architecture Overview
- **Purpose:** 프로젝트의 정체성, 핵심 기술 스택, 엔지니어링 포지셔닝을 명확히 전달.
- **Key Message:** 단순 API 구현을 넘어 인증/인가, 컨테이너 인프라, 부하 검증, AI 거버넌스를 통합 구축한 백엔드 시스템.
- **Required Evidence:** `01_PROJECT_OVERVIEW.md`, `SOURCE_OF_TRUTH_SNAPSHOT.md`
- **Visual Recommendation:** 4대 핵심 축(Security, Infra, Verification, AI Process)을 보여주는 깔끔한 4-Card 레이아웃.
- **Content:**
  - Tech Stack: Java 17, Spring Boot 3.3, Security 6, Redis 7, MySQL 8, Docker, Nginx, Prometheus, k6
  - 4대 엔지니어링 영역: Stateless/Stateful 하이브리드 보안, 7개 컨테이너 포트 격리, k6 70 VU 실측 검증, SA-1 AI 거버넌스
- **Speaker Intent:** 프로젝트의 전체적인 스코프와 공학적 깊이를 1분 내로 스캐닝할 수 있도록 브리핑.
- **Status:** `[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

---

### Slide 02: Core Engineering Challenges & Objectives
- **Purpose:** 시스템을 설계하며 해결하고자 한 3대 핵심 엔지니어링 난제 정의.
- **Key Message:** 무상태성을 유지하면서도 즉각적인 토큰 탈취 방어와 컨테이너 환경의 네트워크 안정성을 확보한다.
- **Required Evidence:** `02_PROBLEM_AND_SOLUTION.md`
- **Visual Recommendation:** 3개의 Problem vs Solution 대칭 비교 카드.
- **Content:**
  - Challenge 1: JWT 무상태성과 즉시 세션 무효화의 딜레마 ➔ Access Token(1h) + RTR + Redis Blacklist
  - Challenge 2: 무분별한 포트 노출 및 공격 표면 ➔ Nginx Port 80 단일 진입점 및 내부 격리
  - Challenge 3: 환경 간 DDL/바인딩 불일치 ➔ Flyway V1~V5 & Docker 환경변수 주입
- **Speaker Intent:** 왜 이 아키텍처를 선택했는지에 대한 엔지니어링적 당위성 설명.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

---

### Slide 03: System & Container Topology
- **Purpose:** Nginx 단일 진입점과 7개 도커 서비스의 네트워크 격리 구조 시각화.
- **Key Message:** 오직 Nginx 80 포트만을 외부에 노출하고 모든 내부 컴포넌트는 격리된 브리지 네트워크로 보호한다.
- **Required Evidence:** `03_ARCHITECTURE.md`, `ARCHITECTURE_SPEC.md`
- **Visual Recommendation:** Nginx Gateway ➔ 내부 Docker Network (App, DB, Redis, Observability) 토폴로지 다이어그램.
- **Content:**
  - Public Gateway: Nginx (Port 80) ➔ Static SPA 서빙 & `/api/*` 프록시 라우팅
  - Internal Network: Spring Boot (8080), MySQL (3306), Redis (6379)
  - Observability Pipeline: Prometheus (9090) ➔ VictoriaMetrics (8428) ➔ Grafana (3000)
- **Speaker Intent:** 네트워크 레벨에서 보안과 모니터링이 어떻게 구조화되었는지 전달.
- **Status:** `[IMPLEMENTED]` `[VERIFIED]`

---

### Slide 04: Backend Clean Architecture & DTO Isolation
- **Purpose:** 불변 Record DTO를 통한 엔티티 캡슐화 및 통일된 API 응답 규격 제시.
- **Key Message:** Entity의 외부 직접 노출을 차단하고 통일된 응답/예외 래퍼로 통신 안정성을 보장한다.
- **Required Evidence:** `05_CORE_IMPLEMENTATION.md`
- **Visual Recommendation:** Controller ➔ Service ➔ Repository 계층 분리 다이어그램 및 `ApiResponse<T>` 구조 박스.
- **Content:**
  - Java 17 `record` 불변 DTO: 불변성 보장 및 얕은 복사 부수 효과 방지
  - `ApiResponse<T>`: `success`, `data`, `message`, `errorCode` 표준 규격
  - `@RestControllerAdvice`: 비즈니스/보안 예외의 중앙 집중식 핸들링
- **Speaker Intent:** 코드 레벨에서의 기본기, 유지보수성, 캡슐화 원칙 준수를 입증.
- **Status:** `[IMPLEMENTED]` `[DOCUMENTED]`

---

### Slide 05: Authentication Architecture (JWT & Lifecycles)
- **Purpose:** 이원화된 JWT 수명주기 및 전송 채널 격리 메커니즘 설명.
- **Key Message:** Access Token(1시간)과 Refresh Token(7일)을 분리하고 전송 채널을 물리적으로 격리하여 XSS 공격을 방어한다.
- **Required Evidence:** `04_AUTH_AND_RBAC.md`, `AUTH_AND_SECURITY_SPEC.md`
- **Visual Recommendation:** Access Token(Header) vs Refresh Token(Cookie) 전송 경로 및 수명주기 다이어그램.
- **Content:**
  - Access Token: 1시간, HTTP Authorization Header (`Bearer`), JJWT HMAC-SHA256 Payload
  - Refresh Token: 7일, `HttpOnly` / `Secure` / `SameSite=Strict` Cookie 전송, UUID JTI 식별
- **Speaker Intent:** 토큰 저장 및 전송 방식의 보안 고려사항을 논리적으로 설명.
- **Status:** `[IMPLEMENTED]` `[VERIFIED]`

---

### Slide 06: Advanced Token Security (RTR & Redis Blacklist)
- **Purpose:** Refresh Token Rotation 및 Redis Blacklist의 동작 메커니즘 증명.
- **Key Message:** 1회용 JTI 검증으로 재사용 공격을 방어하고, 잔여 TTL 블랙리스트로 즉시 로그아웃 무효화를 달성한다.
- **Required Evidence:** `04_AUTH_AND_RBAC.md`, `06_SECURITY.md`
- **Visual Recommendation:** RTR 시퀀스 다이어그램 (토큰 갱신 시 JTI 교체 및 탈취 토큰 차단 흐름).
- **Content:**
  - Refresh Token Rotation (RTR): `/api/auth/refresh` 호출 시 기존 JTI 즉시 삭제 ➔ 신규 세트 발급 ➔ 구버전 재사용 시 401 차단
  - Redis Token Blacklist: `/api/auth/logout` 시 Access Token의 잔여 TTL 동안 `bl:<token>` 등록 ➔ 즉시 인가 거부
- **Speaker Intent:** Stateless와 Stateful의 장점을 결합한 고도화된 토큰 라이프사이클 통제력 강조.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

---

### Slide 07: Authorization & RBAC Multi-Tier Hierarchy
- **Purpose:** User-Role-Permission M:N 정규화 모델 및 Spring Security 인가 파이프라인 제시.
- **Key Message:** 거친 Role 제어를 넘어 세부 Permission 단위까지 정규화된 M:N RBAC 인가 모델을 구축했다.
- **Required Evidence:** `04_AUTH_AND_RBAC.md`, `AUTH_AND_SECURITY_SPEC.md`
- **Visual Recommendation:** Users ➔ UserRoles ➔ Roles ➔ RolePermissions ➔ Permissions ERD 구조도.
- **Content:**
  - DB 정규화: `users`, `roles`, `permissions`, `user_roles`, `role_permissions`, `menus`, `role_menus`
  - Spring Security Filter Chain: `UserAuthorityService`를 통한 세부 엔드포인트 접근 인가 (권한 부재 시 403 Forbidden)
- **Speaker Intent:** 엔터프라이즈 환경에서 확장 가능한 인가 아키텍처 설계 역량 증명.
- **Status:** `[IMPLEMENTED]` `[VERIFIED]`

---

### Slide 08: Database Schema & Migration Governance (Flyway)
- **Purpose:** Flyway를 통한 데이터베이스 DDL 형상 관리 및 버전 통제 프로세스 설명.
- **Key Message:** JPA validate 모드와 Flyway V1~V5 마이그레이션으로 환경 간 스키마 일관성을 100% 보장한다.
- **Required Evidence:** `05_CORE_IMPLEMENTATION.md`
- **Visual Recommendation:** V1(Init) ➔ V2(Auth) ➔ V3(Common) ➔ V4(Perm) ➔ V5(Test User) 타임라인 스텝 바.
- **Content:**
  - `spring.jpa.hibernate.ddl-auto=validate` 정책으로 예기치 못한 DDL 변경 방지
  - 5단계 Flyway 스키마 이력 관리 및 테스트 데이터 시딩 자동화
- **Speaker Intent:** 데이터 무결성과 형상 관리에 대한 엔지니어링 원칙 제시.
- **Status:** `[IMPLEMENTED]` `[VERIFIED]`

---

### Slide 09: Automated Security & Integration Verification
- **Purpose:** 10종의 핵심 자동화 테스트 스위트 및 보안 차단 시나리오 검증 결과 제시.
- **Key Message:** 10종의 단위/통합 테스트를 통해 비인가 및 탈취 시나리오 방어를 기계적으로 100% 검증했다.
- **Required Evidence:** `07_TESTING.md`, `SECURITY_VERIFICATION_REPORT.md`
- **Visual Recommendation:** 10종 테스트 클래스 매핑 테이블 및 Pass Rate 100% 뱃지.
- **Content:**
  - Auth Core 6종: `AuthControllerTest`, `AuthServiceTest`, `JwtAuthenticationFilterTest`, `RefreshTokenRepositoryTest`, `SecurityIntegrationTest`, `TokenBlacklistServiceTest`
  - RBAC 4종: `RbacSecurityIntegrationTest`, `PermissionIntegrationTest`, `RolePermissionIntegrationTest`, `MenuSecurityIntegrationTest`
  - 주요 검증: RTR Replay Attack 401 차단, Blacklist 필터 거부, Role별 403 Forbidden
- **Speaker Intent:** 코드의 신뢰성을 자동화된 테스트로 입증하는 습관 강조.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

---

### Slide 10: Performance Validation (k6 Benchmarks)
- **Purpose:** k6 70 VU 스트레스 부하 테스트 실측 지표 및 임계치 충족 결과 보고.
- **Key Message:** 정의된 부하 조건(70 VU, 1분)에서 평균 5.64ms, P95 9.98ms, 에러율 0.00%를 실측 검증했다.
- **Required Evidence:** `08_PERFORMANCE.md`, `K6_LOAD_TEST_REPORT.md`
- **Metrics (Fact Base):**
  - VUs: **70 VUs**
  - Duration: **1 minute (60s)**
  - Throughput: **463 req/s**
  - Average Latency: **5.64 ms**
  - P95 Latency: **9.98 ms** (`p(95) < 50ms` 임계치 통과)
  - Error Rate: **0.00% (0 errors)** (`rate < 1%` 임계치 통과)
- **Visual Recommendation:** 4개 대형 KPI 숫자 카드 (463 req/s, 5.64ms Avg, 9.98ms P95, 0.00% Error) + k6 시나리오 흐름.
- **Content:**
  - 실사용자 시나리오 (로그인 ➔ 조회 ➔ 인가 메뉴 ➔ 토큰 갱신)
  - 5~7차 3회 스트레스 테스트 산술 평균 지표
- **Speaker Intent:** "SLA 보장" 등의 과장을 피하고, "정의된 테스트 조건에서 목표 성능과 안정성을 검증했다"는 객관적 사실 전달.
- **Status:** `[VERIFIED]`

---

### Slide 11: Real-World Incident Troubleshooting (TS 6-Step)
- **Purpose:** 실측 장애 3건에 대한 6단계 표준(Symptom~Prevention) 분석 및 해결 내역 제시.
- **Key Message:** 장애를 단순 패치하지 않고 6단계 표준 프레임워크로 근본 원인을 진단하여 재발을 방지했다.
- **Required Evidence:** `09_TROUBLESHOOTING.md`, `TS-01-REDIS_TIMEOUT.md`, `TS-001_*.md`, `TS-003_*.md`
- **Visual Recommendation:** 3개 장애 카드 (Symptom ➔ Root Cause ➔ Resolution ➔ Result).
- **Content:**
  - TS-01-REDIS: Redis 다운 시 60초 블로킹 ➔ Lettuce 타임아웃 2초 단축 및 503 핸들링
  - TS-001: JWT Refresh 401 무한 루프 ➔ 클라이언트 탈출 조건(Exit Condition) 및 즉시 세션 초기화
  - TS-003: Docker 환경 내 Redis localhost 바인딩 실패 ➔ Docker 네트워크 서비스명 환경변수 분리
- **Speaker Intent:** 장애 상황에서의 침착한 분석력과 시스템 복원력 설계 역량 어필.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

---

### Slide 12: Controlled AI Workflow (SA-1 Governance)
- **Purpose:** AI 에이전트를 개발자의 통제 하에 통합한 8단계 엔지니어링 라이프사이클 소개.
- **Key Message:** AI를 맹목적으로 신뢰하지 않고, 엄격한 컨벤션과 테스트 게이트로 통제하는 AI 협업 프로세스를 정립했다.
- **Required Evidence:** `10_AI_WORKFLOW.md`, `AI_WORKFLOW_SPEC.md`
- **Visual Recommendation:** 8-Stage Pipeline 다이어그램 (`Requirement` ➔ `Context` ➔ `Planning` ➔ `Delegation` ➔ `Verification` ➔ `Review` ➔ `Docs` ➔ `Deploy`).
- **Content:**
  - Zero-Chatter Policy: 장황한 텍스트 배제, diff 및 코드 변경 중심 정밀 협업
  - Documentation-First Policy: `task_progress.md` 계획 수립 및 `changelogs/` 동기화 의무
  - Human Gatekeeper: AI 생성 코드는 JUnit/k6 100% 통과 후 개발자 최종 승인 커밋
- **Speaker Intent:** 최신 AI 도구를 무분별하게 쓰는 것이 아니라 공학적 거버넌스로 통제하는 현대적 개발자 역량 입증.
- **Status:** `[DOCUMENTED]` `[VERIFIED]`

---

### Slide 13: Architectural Decisions & Technical Trade-offs
- **Purpose:** 주요 설계 의사결정에서의 트레이드오프 분석 및 최적점 도출 과정 설명.
- **Key Message:** 완벽한 아키텍처는 없으며, 시스템 요구사항에 맞는 현실적인 엔지니어링 트레이드오프를 도출했다.
- **Required Evidence:** `04_AUTH_AND_RBAC.md`, `09_TROUBLESHOOTING.md`
- **Visual Recommendation:** 2개의 Trade-off 비교 저울 다이어그램.
- **Content:**
  - Trade-off 1: 무상태(Stateless) 확장성 vs 실시간 즉시 세션 제어 ➔ Access Token 무상태 유지 + 로그아웃 시만 Redis Blacklist 조회
  - Trade-off 2: Redis 외부 의존성 결합 vs 시스템 복원력 ➔ Lettuce 커맨드 타임아웃 2초 강제 및 503 Fallback 분리
- **Speaker Intent:** 아키텍처 결정의 배경과 기술적 성숙도 제시.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`

---

### Slide 14: System Limitations & Future Roadmap (PLANNED)
- **Purpose:** 현재 시스템의 한계점을 투명하게 공개하고 사실(Fact)과 계획(Plan)을 엄격히 분리한 로드맵 제시.
- **Key Message:** 현재 한계를 객관적으로 인지하고, 사실과 계획을 명확히 분리하여 지속 가능한 발전 방향을 수립했다.
- **Required Evidence:** `11_LIMITATIONS_AND_ROADMAP.md`, `SOURCE_OF_TRUTH_SNAPSHOT.md`
- **Visual Recommendation:** Current Limitations(Left) vs Future Roadmap `[PLANNED]`(Right) 2단 분할 레이아웃.
- **Content:**
  - Current Limitations: 단일 노드 컨테이너 환경, JPA N+1 정밀 쿼리 벤치마크 미보유
  - Future Roadmap (`[PLANNED]`):
    - JPA N+1 쿼리 최적화 전/후 실측 벤치마크
    - Message Queue (Kafka/RabbitMQ) 비동기 파이프라인
    - Redis Cluster 분산 고가용성 구성
    - Vault/KMS 및 HTTPS TLS 인증서 적용
- **Speaker Intent:** 정직하고 신뢰할 수 있는 엔지니어로서의 태도 전달.
- **Status:** `[PLANNED]` `[DOCUMENTED]`

---

### Slide 15: Conclusion & Engineering Identity
- **Purpose:** 프로젝트 핵심 성과 요약 및 엔지니어로서의 아이덴티티 확립.
- **Key Message:** "프레임워크의 원리를 이해하고, 백엔드를 설계하며, 인프라에서 실행하고, 검증과 장애 분석으로 증명하는 엔지니어"
- **Required Evidence:** `01_PROJECT_OVERVIEW.md`, `PORTFOLIO_PRESENTATION.md`
- **Visual Recommendation:** 4대 성과 요약 카드 (Security, Performance, Incident, AI Process) + 엔지니어링 슬로건.
- **Content:**
  - 검증 완료된 성과 요약 (100% Test Pass, 5.64ms Latency, 0% Error, 3건 TS 완결)
  - 엔지니어링 가치관: 사실과 증거 기반의 소프트웨어 엔지니어링
  - Source Repositories & Traceability 링크
- **Speaker Intent:** 강렬하고 전문적인 인상을 남기며 발표 마무리.
- **Status:** `[VERIFIED]` `[DOCUMENTED]`
