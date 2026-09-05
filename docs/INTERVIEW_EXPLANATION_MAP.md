# Interview Explanation Map: 면접용 질문-답변 암기 지도

- **문서 목적:** 포트폴리오의 주요 기술적 의사결정과 검증 결과를 면접 현장에서 30초, 1분, 2분 단위로 막힘없이 말할 수 있도록 정리한 핵심 답변 지도
- **원칙:** 사실(Fact) 기반 설명, "내 프로젝트에서" 중심 어조, 검증 여부의 명확한 구분 (과장 금지)

---

## Q1. 이 프로젝트가 무엇인가요? (30초 답변)

### 🎙️ 30초 모범 답변
> "제가 진행한 프로젝트는 **Spring Boot 기반의 고신뢰성 인증/인가 및 세션 통제 시스템**입니다.  
> 단순히 로그인 API를 구현하는 것에 그치지 않고, 무상태 JWT의 한계인 **토큰 탈취 재사용 위험**과 **즉시 로그아웃 불가 문제**를 **Refresh Token Rotation과 Redis 블랙리스트**로 해결했습니다.  
> 또한 7개 컨테이너로 인프라를 격리하고, 21개 핵심 JUnit 테스트와 **k6 70 VU 부하 테스트(평균 5.64ms, 에러 0%)**를 통해 시스템의 안정성과 보안을 실측으로 증명했습니다."

- **핵심 키워드:** 무상태성, 토큰 탈취 방어(RTR), Redis Blacklist, RBAC, k6 부하 검증
- **관련 Claim:** `CLM-SEC-001`, `CLM-PERF-001`, `CLM-INFRA-001`
- **관련 Evidence:** `ev-auth-jwt-filter`, `ev-perf-70vu`, `ev-infra-nginx`
- **실제 소스:** `26-05adf/backend`, `26-05adf/docker-compose.yml`

---

## Q2. 인증(Authentication)을 어떻게 구현했나요? (1분 답변)

### 🎙️ 1분 모범 답변
> "저희 프로젝트에서는 **Access Token과 Refresh Token의 수명주기 이원화 정책**을 적용했습니다.  
> 일반 API 호출에 쓰이는 **Access Token은 1시간 유효기간**을 부여하고, HTTP Authorization 헤더로 전달받아 서버가 DB 조회 없이 무상태로 서명만 검증합니다. 덕분에 대규모 트래픽에서도 WAS 부하를 최소화할 수 있습니다.  
> 반면 세션 갱신에 쓰이는 **Refresh Token은 7일 유효기간**을 두고, XSS 스크립트 공격에 탈취되지 않도록 `HttpOnly`, `Secure`, `SameSite=Strict` 쿠키로만 격리 전송되도록 설계했습니다.  
> 토큰 파싱 필터(`JwtAuthenticationFilter`)에서는 토큰의 서명, 만료 여부, 그리고 토큰 타입 클레임을 단일 패스로 검증하여 Refresh Token으로 일반 API를 우회 호출하는 공격을 원천 차단했습니다."

- **핵심 키워드:** 수명주기 이원화 (1h vs 7d), 무상태 헤더 전송, HttpOnly Secure 쿠키, 단일 패스 검증
- **관련 Claim:** `CLM-SEC-001`
- **관련 Evidence:** `ev-auth-jwt-filter`
- **실제 소스:**
  - `backend/src/main/java/com/example/demo/auth/jwt/JwtProvider.java`
  - `backend/src/main/java/com/example/demo/auth/security/JwtAuthenticationFilter.java`
- **실제 테스트:** `JwtAuthenticationFilterTest.java` (`validAccessTokenSetsSecurityContext`, `nonAccessTokenReturnsUnauthorized`)

---

## Q3. Refresh Token Rotation (RTR)을 왜 사용했고 어떻게 동작하나요? (1~2분 답변)

### 🎙️ 1~2분 모범 답변
> "JWT 환경에서 가장 치명적인 시나리오는 **Refresh Token 탈취**입니다. 만약 탈취당하면 해커가 유효기간(7일) 동안 계속해서 정상 사용자인 척 새 토큰을 받아낼 수 있습니다.  
> 이를 방어하기 위해 **Refresh Token Rotation (RTR)** 메커니즘을 적용했습니다.  
> 사용자가 재발급을 요청할 때마다, 기존 Refresh Token을 즉시 폐기하고 완전히 새로운 JTI(고유 식별자)를 가진 새 토큰 쌍을 발급합니다.  
> 
> 저희 프로젝트에서는 Redis에 `auth:refresh:user:{userId}` 키로 현재 유효한 최신 JTI를 저장하고 관리합니다.  
> 재발급 요청이 들어오면 **Redis Lua Script**를 통해 '클라이언트가 보낸 JTI'와 'Redis에 저장된 최신 JTI'가 일치하는지 확인하고, 일치할 때만 원자적(Atomic)으로 새 JTI로 교체합니다.  
> 만약 이미 사용되어 폐기된 구버전 JTI로 재발급 요청이 오면, 시스템은 **토큰 재사용 공격(Replay Attack)**으로 판단하여 401 Unauthorized를 반환하고 즉시 해당 사용자의 세션을 강제 만료시킵니다.  
> 또한 동시성 레이스 컨디션을 방지하기 위해 프론트엔드에서도 `refreshPromise` Single-Flight 패턴을 적용해 동시 요청을 1개로 합쳤습니다."

- **핵심 키워드:** Refresh Token 탈취 방어, 일회용 JTI 교체, Redis 원자적 Lua Script, Replay Attack 차단, Single-Flight
- **관련 Claim:** `CLM-SEC-002`, `CLM-TS-002`
- **관련 Evidence:** `ev-auth-rtr`, `ev-fe-single-flight`
- **실제 소스:**
  - `backend/src/main/java/com/example/demo/auth/security/RefreshTokenRepository.java` (`rotate` 메서드)
  - `frontend/src/api/http.ts` (`refreshPromise`)
- **실제 테스트:** `RefreshTokenRepositoryTest.java` (`rotateSuccess`, `rotateFail`, `rotateNull`)

---

## Q4. Redis는 왜 사용했고 어떤 데이터를 저장했나요? (1분 답변)

### 🎙️ 1분 모범 답변
> "무상태 JWT를 쓰면서도 **실시간 세션 통제력**을 확보하기 위해 인메모리 저장소인 Redis 7.0을 도입했습니다.  
> Redis에는 크게 두 가지 인증 상태를 관리합니다.  
> 
> 첫 번째는 앞서 말씀드린 **Refresh Token의 활성 JTI**입니다. 빠른 조회가 필요하고 갱신 빈도가 높기 때문에 RDBMS 대신 Redis를 사용했습니다.  
> 두 번째는 **로그아웃된 Access Token의 블랙리스트**입니다. 사용자가 로그아웃을 눌렀을 때, 무상태 Access Token은 서버에서 강제로 지울 수 없습니다. 그래서 해당 토큰의 JTI를 Redis에 키로 등록하고, 토큰의 남은 유효시간(TTL)만큼 만료시간을 걸어둡니다.  
> 이후 들어오는 모든 API 요청은 필터에서 이 블랙리스트를 확인하여 이미 로그아웃된 토큰을 즉시 401로 튕겨냅니다. 남은 시간이 지나면 Redis가 메모리에서 키를 자동 삭제하므로 메모리 누수도 없습니다."

- **핵심 키워드:** 실시간 세션 통제, 활성 JTI 관리, 잔여 TTL 기반 블랙리스트, 자동 메모리 회수
- **관련 Claim:** `CLM-SEC-002`, `CLM-SEC-003`
- **관련 Evidence:** `ev-auth-rtr`, `ev-auth-blacklist`
- **실제 소스:**
  - `backend/src/main/java/com/example/demo/auth/security/TokenBlacklistService.java` (`blacklist`, `isBlacklisted`)
- **실제 테스트:** `TokenBlacklistServiceTest.java` (`blacklistSuccess`, `isBlacklistedReturnsTrue`, `isBlacklistedReturnsFalse`)

---

## Q5. RBAC(인가)는 어떻게 구현했나요? (1분 답변)

### 🎙️ 1분 모범 답변
> "저희 프로젝트는 **User - Role - Permission의 3계층 M:N 다대다 정규화 모델**을 구축했습니다.  
> 단순 Role 방식(예: `ROLE_ADMIN`)은 새로운 직책이나 세부 권한이 생길 때마다 Java 소스 코드를 수정해야 하는 단점이 있습니다.  
> 반면 저희는 Role과 Permission(`MENU_READ`, `USER_MANAGE`)을 분리하여, 비즈니스 로직에는 세부 기능 권한만 걸어두고 DB 설정(`role_permissions`)을 통해 역할에 권한을 유연하게 매핑할 수 있도록 했습니다.  
> 
> 사용자가 로그인하면 JWT Payload 및 `UserAuthorityService`를 통해 해당 유저의 권한 목록을 로드하고 Spring Security의 `SecurityContext`에 주입합니다.  
> 인가되지 않은 일반 유저가 관리자 API를 호출하면 Spring Security 필터 체인에서 가로채 **403 Forbidden** 응답을 일관된 JSON 포맷(`ApiResponse`)으로 반환합니다."

- **핵심 키워드:** User-Role-Permission 3계층, M:N 정규화 매핑, 동적 권한 분리, 403 Forbidden 차단
- **관련 Claim:** `CLM-RBAC-001`, `CLM-RBAC-002`
- **관련 Evidence:** `ev-rbac-security`, `ev-menu-security`
- **실제 소스:**
  - `backend/src/main/resources/db/migration/V2__init_authority_schema.sql`
  - `backend/src/main/java/com/example/demo/auth/security/UserAuthorityService.java`
  - `backend/src/main/java/com/example/demo/iam/menu/MenuAdminController.java`
- **실제 테스트:** 
  - `RbacSecurityIntegrationTest.java` (`adminCanAssignPermissions`, `normalUserCannotAssignPermissions`)
  - `MenuSecurityIntegrationTest.java` (`인증된_사용자라도_MENU_READ가_없으면_403이다`)

---

## Q6. 보안 및 기능 테스트는 무엇을 어떻게 검증했나요? (1분 답변)

### 🎙️ 1분 모범 답변
> "단순히 성공 케이스만 확인한 것이 아니라, **보안 공격 및 장애 격리 시나리오**를 중심으로 21개 핵심 JUnit5 단위/통합 테스트를 작성했습니다.  
> 
> 구체적으로 세 가지 핵심 엣지 케이스를 증명했습니다.  
> 첫째, `RefreshTokenRepositoryTest`에서 탈취된 구버전 JTI로 재발급을 시도할 때 Lua Script 판정 실패로 교체가 거부되는지 확인했습니다.  
> 둘째, `TokenBlacklistServiceTest`에서 로그아웃된 토큰이 필터에서 완벽히 401 차단되는지 검증했습니다.  
> 셋째, `RbacSecurityIntegrationTest`와 `MenuSecurityIntegrationTest`에서 일반 사용자 토큰으로 어드민 권한 부여나 미인가 메뉴 조회를 시도했을 때 403 Forbidden이 정확히 발생하는지 MockMvc로 검증했습니다.  
> 모든 핵심 테스트 스위트는 회귀 버그 없이 100% PASS 상태를 유지하고 있습니다."

- **핵심 키워드:** 공격 시나리오 검증, RTR 재사용 차단, 로그아웃 블랙리스트 차단, RBAC 403 인가 검증
- **관련 Claim:** `CLM-SEC-001~003`, `CLM-RBAC-001~002`
- **실제 테스트:**
  - `backend/src/test/java/com/example/demo/auth/security/RefreshTokenRepositoryTest.java`
  - `backend/src/test/java/com/example/demo/auth/security/TokenBlacklistServiceTest.java`
  - `backend/src/test/java/com/example/demo/iam/rbac/RbacSecurityIntegrationTest.java`
  - `backend/src/test/java/com/example/demo/menu/MenuSecurityIntegrationTest.java`

---

## Q7. 성능 부하 테스트(k6)는 어떻게 진행했고 결과는 어땠나요? (1분 답변)

### 🎙️ 1분 모범 답변
> "실제 프로덕션 환경의 부하를 모사하기 위해 k6를 사용하여 실제 비즈니스 흐름(로그인 ➔ 사용자 정보 조회 ➔ 인가 메뉴 조회 ➔ RTR 토큰 재발급)을 시나리오로 작성했습니다.  
> 피크 부하 조건인 **70 VU(가상 사용자) 동시 부하로 1분 동안 지속**하는 스트레스 테스트를 3회 반복 측정했습니다.  
> 
> 실측 결과, 3회 산술 평균 기준으로 **평균 레이턴시 5.64ms, P95 레이턴시 9.98ms, 초당 처리량 463 req/s, 에러율 0.00%**를 달성했습니다.  
> 사전에 정의했던 임계치인 P95 50ms 미만, 평균 20ms 미만, 에러율 1% 미만 기준을 모두 여유 있게 통과했습니다.  
> Access Token의 무상태 검증과 Redis를 통한 초고속 토큰 회전 덕분에 동시 요청 환경에서도 데이터베이스 병목 없이 높은 응답성을 유지함을 확인했습니다."

- **핵심 키워드:** k6 실측, 70 VU 피크 부하, 비즈니스 흐름 시나리오, 3회 평균 (Avg 5.64ms, P95 9.98ms, Error 0.00%)
- **관련 Claim:** `CLM-PERF-001`
- **관련 Evidence:** `ev-perf-70vu`
- **실제 소스:**
  - `26-05adf/k6/scenarios/load.test.js`
  - `26-05adf/k6/config/thresholds.js`
  - `26-05adf/docs/performance/k6-load-test.md`

---

## Q8. AI를 개발 과정에서 어떻게 활용했나요? (1분 답변)

### 🎙️ 1분 모범 답변
> "저는 AI를 '코드를 대신 짜주는 주체'가 아니라 **'엄격한 거버넌스 하에서 통제되는 엔지니어링 파트너'**로 활용했습니다.  
> `SA-1` 저장소에 Documentation-First 원칙과 8단계 제어 라이프사이클을 수립하여 AI와의 협업 프로세스를 통제했습니다.  
> 
> 핵심은 **'AI 제안 ➔ 개발자 검토 ➔ 채택/수정/거부 ➔ 테스트 검증'**의 4단계 피드백 루프입니다.  
> AI가 제시한 코드나 아키텍처 초안을 그대로 반영하지 않고, 보안 취약점과 성능 트레이드오프를 제가 직접 분석했습니다.  
> 예를 들어 Redis 다운 시 AI가 '보안 검증을 무시하고 통과시키자'고 제안했을 때, 보안 침해를 우려해 이를 거부하고 '타임아웃 2초 단축 후 503 에러로 안전하게 격리'하는 방식으로 제가 직접 설계를 수정했습니다.  
> 또한 AI가 작성한 모든 코드는 100% JUnit 및 k6 테스트 검증을 통과한 후에만 커밋을 허용했습니다."

- **핵심 키워드:** 통제된 협업, Documentation-First 거버넌스, 개발자의 주도적 결정(거부 및 수정), 100% 테스트 통과 원칙
- **관련 Claim:** `CLM-AI-001`
- **관련 Evidence:** `ev-ai-process`
- **실제 소스:**
  - `SA-1/conventions/rules.md`
  - `SA-1/changelogs/phase1_backend/1-2_jwt_redis_optimization.md`

---

## Q9. 프로젝트를 진행하며 겪었던 가장 어려웠던 장애와 해결 방법은? (장애 분석 답변)

### 🎙️ 1~2분 모범 답변 (선택 1: Redis 타임아웃 지연 & 503 격리 - 강력 추천)
> "가장 인상 깊었던 트러블슈팅은 **Redis 장애 발생 시 Spring Boot 서버 전체가 먹통이 되던 문제(TS-01-REDIS)**였습니다.  
> 
> 테스트 환경에서 Redis 컨테이너를 강제 중지시켰더니, 로그아웃 및 토큰 갱신 API 요청이 들어올 때마다 서버 스레드가 최대 60초 동안 블로킹되면서 Tomcat 스레드 풀이 순식간에 고갈되고 일반 조회 API까지 모두 멈춰버렸습니다.  
> 
> 원인을 분석해보니 Spring Data Redis의 기본 Lettuce 클라이언트 커맨드 타임아웃이 60초로 너무 길게 잡혀 있었습니다.  
> 저는 이를 해결하기 위해 두 가지 방어 코드를 적용했습니다.  
> 첫째, `application.yaml`에서 Redis 커맨드 타임아웃을 **2,000ms(2초)**로 대폭 단축했습니다.  
> 둘째, 타임아웃 발생 시 무한정 대기하거나 500 내부 에러를 내뿜지 않고, 전용 예외인 `RedisUnavailableException`을 발생시켜 **503 Service Unavailable**로 빠르게 실패(Fail-Fast)하도록 격리했습니다.  
> 이를 통해 Redis가 죽더라도 2초 만에 장애를 격리하고 일반 조회 서비스의 스레드 풀을 안전하게 지켜낼 수 있었습니다."

- **핵심 키워드:** TS-01-REDIS, Lettuce 60초 스레드 풀 고갈, 타임아웃 2초 단축, 503 Fail-Fast 격리
- **관련 Claim:** `CLM-TS-001`
- **관련 Evidence:** `ev-ts-redis-timeout`
- **실제 소스:**
  - `backend/src/main/java/com/example/demo/auth/security/RedisUnavailableException.java`
  - `backend/src/main/java/com/example/demo/auth/security/JwtAuthenticationFilter.java`
- **실제 테스트:** `JwtAuthenticationFilterTest.java` (`redisUnavailableReturns503`)

---

## Q10. 앞으로 시스템을 더 개선한다면 어떤 부분을 보완하고 싶나요? (한계 및 로드맵 답변)

### 🎙️ 1분 모범 답변
> "현재 시스템은 기능과 보안, 그리고 70 VU 수준의 부하에서 완벽히 검증되었지만, 대규모 분산 환경 관점에서는 명확한 한계와 개선점이 있습니다.  
> 저는 이를 거짓 없이 `PLANNED` 과제로 분리해 두었습니다.  
> 
> 첫째, **JPA N+1 최적화의 정량적 벤치마크**입니다. 현재 코드에는 `@EntityGraph`와 Fetch Join이 적용되어 있지만, 적용 전후 실행 쿼리 수와 힙 메모리 차이를 정량적으로 측정한 벤치마크 리포트를 완성할 계획입니다.  
> 둘째, **분산 환경 스케일아웃과 Redis 고가용성**입니다. 현재는 Docker 단일 노드 인프라입니다. 향후 트래픽 확장을 대비해 Nginx 상단에 L7 로드밸런서를 두고, Redis는 Sentinel 또는 Cluster 구조로 전환하여 마스터 장애 시 자동 페일오버(Failover)를 보장하도록 고도화하고 싶습니다.  
> 셋째, 프론트엔드 React Query 캐싱 고도화와 클라우드 KMS 연동을 로드맵으로 삼고 있습니다."

- **핵심 키워드:** 솔직한 한계 인정, PLANNED 명확한 분리, JPA N+1 정량 벤치마크, Redis 클러스터/Sentinel 고가용성, L7 로드밸런서
- **관련 상태:** `PLANNED` (unev-jpa-n1-benchmark, unev-grafana-live-dashboard)
- **참조 슬라이드:** Slide 014 (System Limitations & Future Roadmap)
