# Portfolio Human Guide: 개발자를 위한 포트폴리오 설명서

- **문서 목적:** 복잡한 기술 및 검증 시스템을 개발자 본인이 직관적으로 이해하고, 면접관에게 쉽고 정확하게 설명하기 위한 개인용 가이드북
- **적용 대상 저장소:** `26-05adf` (BUILD), `SA-1` (PROCESS), `PR-1A1` (PROOF)
- **최종 발표 자료:** 15-Slide Presentation Deck & Engineering Case Study

---

## 1. 프로젝트 한 줄 설명

> **"Spring Boot 기반 인증/인가 시스템을 구현하고, JWT + Refresh Token Rotation + Redis + RBAC를 적용한 뒤 테스트와 부하 테스트로 주요 동작을 검증한 백엔드 시스템"**

이 프로젝트는 단순히 기능만 돌아가는 게시판 수준의 웹 서비스가 아닙니다.  
실제 서비스 환경에서 가장 흔히 발생하는 **토큰 탈취(Replay Attack)**, **세션 즉시 무효화 불가**, **권한 분기 복잡도**, **인메모리 캐시 장애 전파** 문제를 해결하고, 이를 자동화된 단위/통합 테스트와 부하 테스트로 **증명(Proof)**한 엔지니어링 프로젝트입니다.

---

## 2. 3개 Repository의 역할

3개의 저장소는 분리된 프로젝트가 아니라, 하나의 개발 스토리를 완성하는 3개의 기둥입니다.

```text
[BUILD]                [PROCESS]               [PROOF]                 [PORTFOLIO]
26-05adf       ──►     SA-1            ──►     PR-1A1          ──►     PPT / Case Study
실제 애플리케이션        개발 과정과 AI 판단      검증과 증거 저장소        면접관에게 설명
```

| Repository | 역할 | 쉽게 말하면 | 왜 존재하는가? (2~3문장) |
|---|---|---|---|
| **26-05adf** | **BUILD** | **내가 실제로 만든 것** | 백엔드(Spring Boot), 프론트엔드(React), 인프라(Docker/Nginx), 테스트 코드가 실제로 동작하는 본체입니다. 모든 기능 코드와 21개 이상의 JUnit 테스트, k6 부하 스크립트가 이곳에 존재합니다. |
| **SA-1** | **PROCESS** | **내가 어떻게 개발하고 판단했는가** | AI 에이전트를 개발 도구로 활용하면서 내린 기술적 의사결정과 개발 거버넌스 기록입니다. AI의 제안을 무비판적으로 수용하지 않고, 엔지니어가 어떻게 검토하고 트레이드오프를 결정했는지 보여줍니다. |
| **PR-1A1** | **PROOF** | **내가 만든 것을 어떻게 증명했는가** | 실제 코드와 테스트 결과에서 추출한 증거(Evidence)와 주장(Claim)을 연결하는 검증 시스템입니다. 면접관이 "이거 진짜 동작하나요?"라고 물었을 때 1초 만에 테스트 결과와 커밋 해시로 증명할 수 있습니다. |
| **PPT / Case Study** | **PORTFOLIO** | **면접관에게 보여주는 결과물** | 위의 세 가지를 면접관의 눈높이에 맞추어 15장의 슬라이드와 케이스 스터디로 시각화한 최종 산출물입니다. |

---

## 3. 기술 스택: 외우기 쉬운 역할 중심 정리

백과사전식 기술 나열 대신, **"무엇인가? 왜 썼는가? 내 프로젝트 어디에 썼는가?"** 3가지만 기억합니다.

```text
[Application]       Spring Boot 3.3.2 / Java 17
[Authentication]    JWT (Access Token / Refresh Token)
[Token Management]  Redis 7.0 (RTR / Blacklist)
[Authorization]     RBAC (User - Role - Permission - Menu)
[Database]          MySQL 8.0 / JPA / Flyway V1~V5
[Frontend]          React 18 / Zustand / Axios
[Infrastructure]    Docker Compose (7 Services) / Nginx (Port 80)
[Monitoring]        Prometheus / VictoriaMetrics / Grafana
[Testing]           JUnit 5 / MockMvc / k6
```

### [Application] Java 17 & Spring Boot 3.3.2
- **무엇인가?** 최신 LTS Java 언어와 엔터프라이즈 백엔드 표준 프레임워크.
- **왜 썼는가?** 불변 `record` 객체로 DTO를 안전하게 설계하고, Spring Security 6과의 강력한 보안 연계를 위해 사용했다.
- **내 프로젝트 어디에 썼는가?** 전체 백엔드 API 서버와 도메인 계층 분리 (`26-05adf/backend`).

### [Authentication] JWT (JSON Web Token)
- **무엇인가?** 서명된 토큰 안에 사용자 정보를 담는 무상태(Stateless) 인증 방식.
- **왜 썼는가?** API 요청마다 매번 DB를 조회하지 않고 서버 리소스를 아끼기 위해 사용했다.
- **내 프로젝트 어디에 썼는가?** Access Token(1시간 유효, 헤더 전송)과 Refresh Token(7일 유효, HttpOnly 쿠키 전송) 이원화 (`JwtProvider.java`, `JwtAuthenticationFilter.java`).

### [Token Management] Redis 7.0
- **무엇인가?** 메모리 기반 초고속 Key-Value 데이터베이스.
- **왜 썼는가?** 무상태 JWT의 최대 약점인 "즉시 로그아웃 불가"와 "토큰 탈취 재사용"을 초고속으로 통제하기 위해 사용했다.
- **내 프로젝트 어디에 썼는가?**
  1. Refresh Token JTI 저장 및 Rotation 원자적 검증 (`RefreshTokenRepository.java`).
  2. 로그아웃된 Access Token의 잔여 TTL 동안 즉시 차단하는 블랙리스트 (`TokenBlacklistService.java`).

### [Authorization] RBAC (역할 기반 접근 제어)
- **무엇인가?** 사용자가 가진 역할(Role)과 그 역할에 부여된 권한(Permission)을 분리하여 API 접근을 통제하는 방식.
- **왜 썼는가?** 역할만으로 통제하면 권한이 바뀔 때마다 코드를 고쳐야 하지만, 퍼미션을 분리하면 DB 설정만으로 유연하게 제어할 수 있다.
- **내 프로젝트 어디에 썼는가?** `users` - `roles` - `permissions` M:N 매핑과 Spring Security 필터 인가 (`UserAuthorityService.java`, `MenuAdminController.java`).

### [Database] MySQL 8.0 & Flyway & JPA
- **무엇인가?** 관계형 데이터베이스와 객체-관계 매핑(JPA), 그리고 DB 형상 관리 도구(Flyway).
- **왜 썼는가?** JPA `ddl-auto: update`의 위험성을 배제하고, 마이그레이션 스크립트로 스키마 변경을 안전하게 추적하기 위해 사용했다.
- **내 프로젝트 어디에 썼는가?** V1부터 V5까지의 Flyway 스크립트 관리 및 `@EntityGraph`를 통한 Fetch Join N+1 방어 (`UserRepository.java`).

### [Frontend] React 18 & Zustand & Axios
- **무엇인가?** 컴포넌트 기반 웹 프론트엔드 라이브러리와 경량 상태 관리 라이브러리.
- **왜 썼는가?** 화면 깜빡임(FOUC) 없는 인증 복원과 토큰 자동 갱신을 깔끔하게 구현하기 위해 사용했다.
- **내 프로젝트 어디에 썼는가?** 앱 실행 시 사전 인증 게이트웨이 (`auth.bootstrap.ts`)와 동시 401 요청을 1개로 합치는 `refreshPromise` Single-Flight 패턴 (`http.ts`).

### [Infrastructure] Nginx & Docker Compose (7 Services)
- **무엇인가?** 웹 리버스 프록시 서버와 컨테이너 통합 오케스트레이션 도구.
- **왜 썼는가?** 내부 포트(Spring Boot, DB, Redis)를 외부에 노출하지 않고 포트 80 하나만 열어 보안성을 확보하기 위해 사용했다.
- **내 프로젝트 어디에 썼는가?** 7개 컨테이너(Nginx, Backend, MySQL, Redis, Prometheus, VictoriaMetrics, Grafana)의 `app-net` 브리지 격리 (`nginx/default.conf`, `docker-compose.yml`).

### [Testing] JUnit 5, MockMvc & k6
- **무엇인가?** 자바 단위/통합 테스트 프레임워크와 Go 기반 현대적 부하 테스트 도구.
- **왜 썼는가?** "말뿐인 보안과 성능"이 아니라 실제 코드가 동작함을 수치로 증명하기 위해 사용했다.
- **내 프로젝트 어디에 썼는가?** 21개 핵심 JUnit 테스트 메서드와 70 VU 피크 부하 실측 벤치마크 (`k6/scenarios/load.test.js`).

---

## 4. 핵심 기술 4개를 "면접에서 설명할 수 있는 이야기"로 변환

면접관이 가장 궁금해하는 4가지 주제는 **[문제] - [선택] - [이유] - [구현] - [검증] - [결과] - [한계]** 템플릿으로 설명합니다.

---

### 이야기 1. Authentication (JWT 무상태 인증)

- **[문제]** 세션 기반 인증은 서버가 늘어나면 세션 동기화 비용이 커지고, 무상태 JWT는 토큰이 탈취되었을 때 만료 전까지 강제 회수할 수 없는 문제가 있었습니다.
- **[선택]** 토큰 수명 이원화 정책을 선택했습니다. Access Token은 1시간으로 짧게 유지하고, Refresh Token은 7일로 길게 설정했습니다.
- **[이유]** 일반 API 호출은 헤더의 Access Token만으로 서버 DB 조회 없이 초고속 무상태 처리하고, 1시간이 지나면 안전한 쿠키의 Refresh Token으로만 갱신하게 하여 성능과 보안을 모두 챙겼습니다.
- **[구현]** 
  - 서명 생성/검증: `26-05adf/backend/.../JwtProvider.java` (JJWT HMAC-SHA256)
  - 요청 필터: `26-05adf/backend/.../JwtAuthenticationFilter.java` (`doFilterInternal`)
- **[검증]** `JwtAuthenticationFilterTest.java`
  - `validAccessTokenSetsSecurityContext`: 유효한 토큰일 때 SecurityContext에 인증 정보 주입 확인.
  - `nonAccessTokenReturnsUnauthorized`: Refresh Token으로 일반 API 접근 시 401 차단 확인.
- **[결과]** 1시간 무상태 고속 인증과 토큰 오용 차단 검증 완료 (`CLM-SEC-001`, `ev-auth-jwt-filter`, **VERIFIED**).
- **[한계]** 클라우드 KMS나 비대칭키(RS256) 연동은 아직 적용하지 않았으며 대칭키(HS256) 기반으로 구현되어 있습니다.

---

### 이야기 2. Refresh Token Rotation (RTR) + Redis Blacklist

- **[문제]** 
  1. 만약 해커가 사용자의 Refresh Token을 탈취하면 7일 동안 무제한으로 새 Access Token을 뽑아낼 수 있습니다.
  2. 사용자가 로그아웃해도 기존 Access Token은 만료시간까지 유효하여 보안 구멍이 발생합니다.
- **[선택]**
  1. **RTR (Refresh Token Rotation):** 토큰을 재발급할 때마다 기존 Refresh Token을 폐기하고 완전히 새로운 토큰 세트를 발급합니다.
  2. **Redis Blacklist:** 로그아웃 시 Access Token의 남은 유효시간(TTL)만큼 Redis에 블랙리스트 키로 등록합니다.
- **[이유]** 
  - RTR을 적용하면 탈취된 구버전 토큰으로 재발급을 시도하는 순간, 서버가 "이미 사용된 토큰"임을 인지하고 즉시 세션을 폭파할 수 있습니다.
  - Redis는 TTL 만료 시 자동 삭제되므로 서버 메모리 누수 없이 즉시 로그아웃 무효화를 달성합니다.
- **[구현]**
  - Redis JTI 원자적 교체: `26-05adf/backend/.../RefreshTokenRepository.java` (`rotate` 메서드, Redis Lua Script)
  - 블랙리스트 등록/조회: `26-05adf/backend/.../TokenBlacklistService.java` (`blacklist`, `isBlacklisted`)
- **[검증]**
  - `RefreshTokenRepositoryTest.java`: `rotateSuccess`, `rotateFail` (구버전 JTI 재사용 시 교체 실패 및 차단)
  - `TokenBlacklistServiceTest.java`: `blacklistSuccess`, `isBlacklistedReturnsTrue`
- **[결과]** 탈취 토큰 재사용 100% 차단 및 즉시 로그아웃 인가 차단 확인 (`CLM-SEC-002`, `CLM-SEC-003`, **VERIFIED**).
- **[한계]** Redis 클러스터링(Multi-Node Sentinel)까지는 테스트하지 못했고 단일 Redis 인스턴스 기준으로 검증되었습니다.

---

### 이야기 3. RBAC (역할-권한 M:N 다단계 인가)

- **[문제]** 시스템이 커질수록 `ROLE_ADMIN`, `ROLE_USER` 같은 단순 역할 체크만으로는 특정 메뉴 조회나 세부 기능 접근 제어를 유연하게 처리할 수 없습니다.
- **[선택]** `User` - `Role` - `Permission` - `Menu`로 이어지는 정규화된 M:N 관계 모델을 구축했습니다.
- **[이유]** "관리자"라는 역할이 있더라도 특정 화면의 권한(`MENU_READ`, `USER_MANAGE`)만 떼어내거나 붙일 수 있도록 권한 단위를 모듈화하기 위함입니다.
- **[구현]**
  - 스키마 정의: `26-05adf/backend/.../db/migration/V2__init_authority_schema.sql`
  - 권한 로드 및 매핑: `26-05adf/backend/.../UserAuthorityService.java`
  - 메뉴 접근 제어: `26-05adf/backend/.../MenuAdminController.java`
- **[검증]**
  - `RbacSecurityIntegrationTest.java`:
    - `adminCanAssignPermissions`: 어드민 계정 권한 할당 성공 (200 OK)
    - `normalUserCannotAssignPermissions`: 일반 유저가 권한 변경 시도 시 403 Forbidden 차단
    - `unauthenticatedUserCannotAssignPermissions`: 미인증 사용자 차단
  - `MenuSecurityIntegrationTest.java`: `MENU_READ` 권한 유무에 따른 403 확인
- **[결과]** 역할과 권한의 완벽한 분리 및 미인가 요청 403 차단 검증 완료 (`CLM-RBAC-001`, `CLM-RBAC-002`, **VERIFIED**).
- **[한계]** 사용자 수가 수십만 명으로 늘어났을 때의 권한 캐싱 계층(Spring Cache / Redis 권한 캐시)은 아직 적용 전입니다.

---

### 이야기 4. Testing + Performance (테스트 및 부하 실측)

- **[문제]** "성능이 빠르다", "보안이 완벽하다"는 주장은 실제 트래픽과 자동화 검증이 없으면 면접관에게 신뢰를 줄 수 없습니다.
- **[선택]** 21개 핵심 JUnit 테스트 스위트와 k6를 활용한 70 VU 실측 부하 테스트를 직접 수행했습니다.
- **[이유]** 실제 사용자 시나리오(로그인 ➔ 조회 ➔ 토큰 재발급)를 모사하여 시스템의 한계와 병목 지점을 수치로 확인하기 위함이었습니다.
- **[구현]**
  - k6 시나리오: `26-05adf/k6/scenarios/load.test.js`
  - 임계치 설정: `26-05adf/k6/config/thresholds.js` (`p95 < 50ms`, `avg < 20ms`, `error < 1%`)
  - 실측 보고서: `26-05adf/docs/performance/k6-load-test.md`
- **[검증]** 70 VU 동시 사용자 1분 지속 스트레스 테스트를 3회 반복 측정(5차, 6차, 7차 run).
- **[결과]** 
  - **평균 응답시간 5.64ms, P95 9.98ms, 초당 처리량 463 req/s, 에러율 0.00% 달성** (`CLM-PERF-001`, **VERIFIED**).
- **[한계]**
  - JPA N+1 적용 전후 쿼리 수 비교 벤치마크는 코드는 적용했으나 정량 수치 미보유 (`PLANNED`).
  - k6 원본 터미널 stdout raw 로그 텍스트 파일은 별도 아카이빙되지 않고 결과 요약 문서만 존재 (`NOT_FOUND`).

---

## 5. JWT / RTR / Redis: 하나의 흐름으로 이해하기

인증 시스템의 핵심 동작 흐름은 다음 8단계로 깔끔하게 정리됩니다.

```text
[1. 로그인 성공]
  │  Access Token(헤더, 1h) + Refresh Token(쿠키, 7d) 동시 발급
  │  Redis에 JTI 저장 (auth:refresh:user:{userId} = UUID_A)
  ▼
[2. 일반 API 호출]
  │  JwtAuthenticationFilter가 Access Token 서명 및 만료 검증
  │  Redis 조회 없이 무상태로 즉시 통과 (빠른 속도)
  ▼
[3. 1시간 경과: Access Token 만료]
  │  클라이언트가 만료된 Access Token으로 API 호출 -> 401 Unauthorized 수신
  ▼
[4. 토큰 재발급 요청 (POST /api/auth/refresh)]
  │  클라이언트는 쿠키에 담긴 Refresh Token(UUID_A)으로 재발급 요청
  ▼
[5. RTR 원자적 교체 (RefreshTokenRepository.rotate)]
  │  Redis Lua Script 실행:
  │  "현재 Redis의 JTI가 클라이언트가 보낸 UUID_A와 일치하는가?"
  │  - 일치하면: 새 JTI(UUID_B)로 덮어쓰고 성공 반환
  │  - 불일치하면: 실패 반환 -> 401 에러 및 세션 폭파
  ▼
[6. 새 토큰 세트 전달]
  │  클라이언트에게 새 Access Token과 새 Refresh Token(UUID_B) 전달
  ▼
[7. 공격 시나리오: 탈취된 기존 Refresh Token(UUID_A)으로 해커가 재발급 요청 시]
  │  Redis에는 이미 UUID_B로 바뀌어 있음 -> Lua Script 불일치 판정
  │  서버는 즉시 401 Unauthorized 반환 -> 해커의 토큰 재사용 차단!
  ▼
[8. 로그아웃 요청 시 (POST /api/auth/logout)]
     Access Token의 잔여 시간(예: 35분 남음)을 계산하여
     Redis Blacklist에 등록 (blacklist:{jti}, TTL=35분)
     이후 해커가 해당 Access Token을 쓰더라도 JwtAuthenticationFilter에서 401 즉시 차단!
```

### 연결되는 실제 소스 파일 & 테스트

| 역할 | 실제 코드 파일 | 실제 테스트 파일 & 메서드 |
|---|---|---|
| 토큰 생성/검증 | `backend/.../JwtProvider.java` | `JwtAuthenticationFilterTest.java` (`validAccessTokenSetsSecurityContext`) |
| 요청 가로채기 | `backend/.../JwtAuthenticationFilter.java` | `JwtAuthenticationFilterTest.java` (`nonAccessTokenReturnsUnauthorized`) |
| RTR 원자적 교체 | `backend/.../RefreshTokenRepository.java` (`rotate`) | `RefreshTokenRepositoryTest.java` (`rotateSuccess`, `rotateFail`) |
| 블랙리스트 등록 | `backend/.../TokenBlacklistService.java` (`blacklist`) | `TokenBlacklistServiceTest.java` (`blacklistSuccess`, `isBlacklistedReturnsTrue`) |
| 프론트엔드 단일 비행 | `frontend/src/api/http.ts` (`refreshPromise`) | TS-001 무한 루프 탈출 조건 검증 |

---

## 6. RBAC (권한 관리): 한 번에 이해하기

### 1. 핵심 엔티티 관계
```text
[User] (사용자)
  │  (M:N) user_roles
  ▼
[Role] (역할: ROLE_ADMIN, ROLE_USER)
  │  (M:N) role_permissions
  ▼
[Permission] (세부 권한: MENU_READ, USER_MANAGE)
  │
  ▼
[Resource / API] (접근 대상: /api/admin/**, /api/menus)
```

### 2. 면접관의 5가지 핵심 질문에 대한 답변

#### Q1. 왜 Role과 Permission을 분리했습니까?
> "Role만 사용하면 '중간 관리자'처럼 권한 범위가 미묘하게 다른 직책이 생길 때마다 Java 코드에 `@PreAuthorize("hasRole('MANAGER')")`를 계속 추가해야 합니다. Role과 Permission을 분리하면, 코드에는 `@PreAuthorize("hasAuthority('MENU_READ')")`처럼 기능 단위만 걸어두고, DB 테이블에서 Role에 Permission을 붙였다 뗐다 할 수 있어 코드 수정 없이 권한 정책을 바꿀 수 있습니다."

#### Q2. 왜 M:N 다대다 관계인가요?
> "한 명의 사용자가 여러 역할(예: 일반 사용자이면서 사내 강사)을 가질 수 있고, 하나의 권한(예: `BOARD_READ`) 역시 여러 역할에 동시에 포함될 수 있기 때문에 `user_roles`와 `role_permissions`라는 중간 조인 테이블을 두어 정규화된 M:N 구조로 설계했습니다."

#### Q3. 권한이 없는 사용자는 어떻게 처리되나요?
> "Spring Security 인가 필터에서 요청한 엔드포인트의 필요 권한과 사용자의 `SecurityContext` 내 `authorities`를 비교합니다. 권한이 부족하면 즉시 `AccessDeniedHandler`가 동작하여 **403 Forbidden** 응답과 통일된 에러 JSON(`ApiResponse`)을 반환합니다."

#### Q4. 403 에러는 정확히 어디서 발생합니까?
> "`JwtAuthenticationFilter`를 통과하여 인증이 완료된 후, Spring Security의 `AuthorizationFilter`(또는 메서드 보안 AOP 프록시)에서 인가 판정이 실패할 때 발생합니다."

#### Q5. 실제 테스트에서는 어떻게 검증했습니까?
> "`RbacSecurityIntegrationTest.java`에서 `ROLE_USER` 권한을 가진 모의 유저로 어드민 전용 권한 변경 API를 호출하여 상태 코드 403이 정확히 반환되는지 MockMvc로 검증했습니다."

---

## 7. 테스트: "개수"가 아니라 "무엇을 증명했는가"

단순히 "테스트가 많다"고 하지 않고, **"보안 결함과 회귀 버그를 방어하기 위해 정확히 무엇을 검증했는가"**를 설명합니다.

| 테스트 목적 | 검증 대상 | 테스트 방법 | 실제 결과 | 소스 위치 (26-05adf) |
|---|---|---|---|---|
| **토큰 변조 방어** | 잘못된 토큰 / Refresh Token의 API 우회 | MockMvc & JwtProvider | 401 Unauthorized 반환 확인 | `JwtAuthenticationFilterTest.java`<br>`nonAccessTokenReturnsUnauthorized` |
| **RTR 재사용 방어** | 이미 사용된 Refresh Token의 재발급 시도 | Mockito & RedisScript | Lua Script 불일치 -> 401 차단 | `RefreshTokenRepositoryTest.java`<br>`rotateFail` |
| **즉시 로그아웃 보장** | 로그아웃 후 이전 Access Token 재사용 | TokenBlacklistService | Redis 조회 -> 401 차단 | `TokenBlacklistServiceTest.java`<br>`blacklistSuccess` |
| **Redis 장애 격리** | Redis 서버 다운 시 WAS 먹통 방지 | Lettuce Timeout & Filter | 2초 만에 `RedisUnavailableException` 발생 -> 503 반환 | `JwtAuthenticationFilterTest.java`<br>`redisUnavailableReturns503` |
| **RBAC 인가 차단** | 일반 유저의 어드민 엔드포인트 침범 | RbacSecurityIntegrationTest | 403 Forbidden 차단 | `RbacSecurityIntegrationTest.java`<br>`normalUserCannotAssignPermissions` |
| **메뉴 동적 인가** | 권한 없는 사용자의 메뉴 API 호출 | MenuSecurityIntegrationTest | 403 Forbidden 차단 | `MenuSecurityIntegrationTest.java`<br>`인증된_사용자라도_MENU_READ가_없으면_403이다` |
| **미인증 접근 통제** | 토큰 없는 보호 자원 접근 | SecurityIntegrationTest | 401 Unauthorized 차단 | `SecurityIntegrationTest.java`<br>`unauthenticatedUserCannotAccessProtectedApi` |

---

## 8. Performance: 과장 없는 실측 데이터 설명법

면접에서 성능을 설명할 때는 절대 "엄청 빠르다"는 추상적인 단어를 쓰지 않고, **조건과 결과**를 정확하게 말합니다.

### 1. 실측 결과 (VERIFIED Fact)
- **도구:** k6 (HTTP load testing tool)
- **시나리오:** 실제 유저 흐름 (로그인 ➔ 프로필 조회 ➔ 인가 메뉴 조회 ➔ RTR 토큰 재발급)
- **부하 조건:** 70 VU (가상 사용자) 동시 부하, 1분 지속, 총 3회 반복 측정 (5차, 6차, 7차)
- **실측 수치:**
  - **평균 응답시간 (Avg Latency):** **5.64 ms** (5차 4.73ms, 6차 6.01ms, 7차 6.18ms 평균)
  - **95% 응답시간 (P95 Latency):** **9.98 ms** (임계치 50ms 대비 압도적 통과)
  - **초당 처리량 (Throughput):** **463.6 req/s**
  - **에러율 (Error Rate):** **0.00%** (27,000건 이상의 요청 중 단 1건의 실패도 없음)

### 2. 상태 구분 (VERIFIED vs NOT VERIFIED vs PLANNED)

| 상태 | 항목 | 면접에서의 올바른 답변 태도 |
|---|---|---|
| **VERIFIED** | k6 70 VU 부하 테스트 결과 (Avg 5.64ms, P95 9.98ms, Error 0%) | "실제 k6 시나리오를 작성하여 3회 반복 측정한 실제 데이터입니다." |
| **VERIFIED** | 21개 핵심 JUnit 보안 단위/통합 테스트 | "Spring Boot 테스트 환경에서 100% 통과를 확인했습니다." |
| **PLANNED** | JPA N+1 Fetch Join 전후 쿼리 수 비교 벤치마크 | "코드 상에 `@EntityGraph`를 적용해 N+1을 방어했으나, 전후 정량 비교 벤치마크 측정 수치는 향후 과제로 계획되어 있습니다." |
| **PARTIAL** | Grafana 실시간 대시보드 | "Grafana 컨테이너 파이프라인은 연결되어 있으나, 실시간 지표 스크린샷 증거는 포트폴리오에 미포함되어 있습니다." |
| **NOT_FOUND** | k6 터미널 원본 stdout txt 로그 | "k6 실행 결과 보고서 문서는 존재하지만, 원본 터미널 텍스트 로그 파일은 별도로 저장해 두지 않았습니다." |

---

## 9. AI 활용: 주도적 엔지니어링 프로세스

면접관이 "이거 AI가 다 짜준 거 아닌가요?"라고 질문했을 때 답변할 수 있는 공식입니다.

```text
[AI의 역할]               [나의 역할]
코드 템플릿 제안   ──►   기술적 타당성 검토
트레이드오프 초안   ──►   채택, 수정, 거부 결정
                      직접 코드 구현 및 리팩터링
                      JUnit 및 k6 자동화 테스트로 증명
```

> **핵심 한 줄:** "AI를 개발 보조 도구로 적극 활용하되, 기술적 판단과 아키텍처 결정, 그리고 최종 검증은 제가 직접 수행했습니다."

### 대표 사례 1: Redis 타임아웃 장애 격리 (TS-01-REDIS)
- **상황:** Redis 컨테이너가 멈추었을 때 Spring Boot의 모든 요청 스레드가 Lettuce 기본 타임아웃인 60초 동안 대기하면서 전체 서버가 다운되는 현상 발생.
- **AI 제안:** "Redis 연결 실패 시 예외를 무시하고 인증을 통과(Bypass)시키는 Fallback 코드를 추가하자."
- **나의 엔지니어링 판단 (거부 및 수정):** "인증/인가 시스템에서 캐시 장애라고 보안 검증을 우회하면 심각한 보안 사고가 된다. 타임아웃을 2초로 대폭 줄이고(`timeout: 2000ms`), 즉시 `RedisUnavailableException`을 발생시켜 **503 Service Unavailable**로 시스템을 안전하게 격리해야 한다."
- **결과:** 스레드 풀 고갈 방어 및 안전한 장애 격리 달성.

### 대표 사례 2: JWT Refresh 무한 재시도 탈출 (TS-001)
- **상황:** 리프레시 토큰이 만료되었을 때 프론트엔드 Axios 인터셉터가 401을 받고 다시 갱신 요청을 보내며 무한 루프에 빠짐.
- **나의 엔지니어링 판단:** 동시 다발적 401 요청을 단 1회로 합치는 `refreshPromise` Single-Flight 패턴을 도입하고, 재발급 실패 시 즉시 토큰을 비우고 로그인 페이지로 이동하는 탈출 조건(Exit Condition)을 강제 적용함.

---

## 10. Evidence Architecture: 사람이 기억하기 쉬운 언어로 번역

복잡한 포트폴리오 내부 시스템 용어를 일상적인 개발자 언어로 번역합니다.

```text
전문 용어             사람 말 번역                     실제 위치
SOURCE          =    실제 동작하는 코드               26-05adf, SA-1
SNAPSHOT        =    그 당시 코드를 고정해 둔 사진      PR-1A1/PR-Files/evidence/snapshots/
EVIDENCE        =    코드와 테스트로 입증된 증거 모음   PR-1A1/PR-Files/evidence/bundles/
CLAIM           =    포트폴리오에서 내가 주장하는 문장  PR-1A1/PR-Files/evidence/claims/ (CLM-*)
WORK            =    사람이 글 쓰고 다듬는 작업대      PR-1A1/work/
VERIFICATION    =    거짓말이 없는지 검사하는 채점기    PR-1A1/automation/validate.py
FINAL ARTIFACT  =    면접관에게 보여주는 완성품        PPT, Case Study, HTML Deck
```

---

## 11. PPT 슬라이드별(001~015) 30초 설명 점검표

면접 전 각 슬라이드를 넘기며 혼자서 30초 브리핑을 연습할 수 있는 요약표입니다.

| 슬라이드 | 핵심 메시지 (1개) | 내가 30초 동안 말할 내용 | 면접관 예상 질문 | 관련 Claim & Evidence |
|---|---|---|---|---|
| **001** | 프로젝트 정체성 | "JWT 보안, 컨테이너 인프라, k6 부하 검증을 결합한 엔지니어링 백엔드 포트폴리오입니다." | 다른 프로젝트와의 차별점은? | `CLM-PERF-001`<br>`CLM-INFRA-001` |
| **002** | 핵심 공학적 과제 | "무상태의 성능을 지키면서도 실시간 로그아웃과 토큰 탈취를 어떻게 막을 것인가를 고민했습니다." | 왜 세션을 안 쓰고 JWT를 썼나? | `CLM-SEC-001~003` |
| **003** | 시스템 & 컨테이너 토폴로지 | "Docker Compose 7개 서비스를 구성하고, Nginx 80 포트만 외부에 열어 내부 네트워크를 격리했습니다." | 포트 격리를 왜 했는가? | `CLM-INFRA-001`<br>`ev-infra-nginx` |
| **004** | 클린 아키텍처 & DTO | "Java 17 불변 Record DTO로 Entity 노출을 막고 ApiResponse 규격을 통일했습니다." | Entity를 직접 반환하면 왜 안 되나? | `IMPLEMENTED` |
| **005** | 인증 아키텍처 (JWT) | "1시간 무상태 Access Token과 7일 HttpOnly Refresh Token으로 수명주기를 이원화했습니다." | 왜 쿠키에 Refresh Token을 넣었나? | `CLM-SEC-001`<br>`ev-auth-jwt-filter` |
| **006** | 고도화 보안 (RTR & Blacklist) | "Redis Lua Script 기반 RTR로 토큰 탈취를 방어하고, 잔여 TTL 블랙리스트로 즉시 로그아웃을 구현했습니다." | RTR 시 동시 요청 레이스 컨디션 해결법은? | `CLM-SEC-002`<br>`CLM-SEC-003` |
| **007** | 인가 계층 (RBAC M:N) | "User-Role-Permission M:N 모델을 통해 미인가 접근 시 403 Forbidden으로 차단합니다." | Role과 Permission을 분리한 이유는? | `CLM-RBAC-001`<br>`CLM-RBAC-002` |
| **008** | DB 형상 관리 (Flyway) | "Flyway V1~V5로 마이그레이션을 자동화하고 ddl-auto는 validate로 고정했습니다." | ddl-auto: update의 문제점은? | `ev-db-flyway` |
| **009** | 자동화 보안 검증 | "10종의 핵심 JUnit 단위/통합 테스트를 구축하여 100% 통과를 확인했습니다." | 주로 어떤 엣지 케이스를 테스트했나? | `CLM-SEC-*`<br>`CLM-RBAC-*` |
| **010** | 부하 테스트 (k6) | "70 VU 동시 부하에서 3회 평균 5.64ms 응답시간과 0% 에러율을 실측 달성했습니다." | 70 VU를 피크 부하로 선정한 기준은? | `CLM-PERF-001`<br>`ev-perf-70vu` |
| **011** | 실무 장애 해결 (TS 3건) | "Redis 2초 타임아웃 격리, 프론트 401 무한 루프 탈출, 도커 DNS 바인딩 3건을 해결했습니다." | Redis 다운 시 WAS 전체 장애를 막은 방법은? | `CLM-TS-001`<br>`CLM-TS-002` |
| **012** | 통제된 AI 협업 (SA-1) | "Documentation-First 거버넌스를 통해 AI 제안을 엔지니어가 검증하고 채택하는 프로세스를 세웠습니다." | AI가 만든 코드의 신뢰성은 어떻게 담보했나? | `CLM-AI-001`<br>`ev-ai-process` |
| **013** | 아키텍처 결정 & 트레이드오프 | "보안을 위한 Redis 도입과 성능 사이의 균형점을 2초 타임아웃과 잔여 TTL로 찾았습니다." | 시스템 설계 시 가장 크게 고민한 트레이드오프는? | `CLM-SEC-*`<br>`CLM-TS-001` |
| **014** | 시스템 한계 & 로드맵 | "단일 노드 환경의 한계를 인정하고, JPA 정량 벤치마크와 MQ 도입을 계획 과제로 격리했습니다." | 지금 아키텍처에서 1만 TPS가 오면 어떻게 할 것인가? | `PLANNED` |
| **015** | 결론 및 엔지니어링 정체성 | "설계하고, 코드로 만들고, 인프라에 띄우고, 테스트와 부하 측정으로 증명하는 백엔드 개발자입니다." | 마지막으로 하고 싶은 말 | `ALL CLAIMS` |
