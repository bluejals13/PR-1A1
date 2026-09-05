# [Case Study] 무상태 JWT의 한계를 극복한 실시간 토큰 제어 및 컨테이너 기반 백엔드 시스템 구축

- **Document ID:** CS-ENGINEERING-01
- **Domain:** Backend Architecture, Security (JWT/RTR/Redis), Container Infra & Performance
- **Source of Truth:**
  - Application: `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
  - AI Process: `https://github.com/bluejals13/SA-1` (Branch: `main`)
  - Evidence Base: `PR-1A1/PR-Files/`
- **Status Classification:** `[VERIFIED]` `[IMPLEMENTED]` `[DOCUMENTED]` `[PLANNED]`

---

## 1. Problem (문제 정의)
웹 애플리케이션 서비스에서 전통적인 세션 기반 인증은 서버의 메모리 부하와 수평 확장(Scale-out) 시 세션 동기화(Sticky Session 또는 Session Clustering) 문제를 야기합니다. 이를 해결하기 위해 무상태(Stateless) JWT를 도입하지만, JWT는 다음과 같은 심각한 보안 및 운영상의 한계를 가집니다:

1. **토큰 탈취(Replay Attack) 방어 불가:** Access Token이나 Refresh Token이 네트워크 구간 또는 XSS/CSRF를 통해 탈취될 경우, 토큰 만료 전까지 서버는 탈취 사실을 인지하거나 차단할 수 없습니다.
2. **즉시 로그아웃(Instant Revocation)의 한계:** Stateless 토큰은 클라이언트에서 토큰을 삭제하더라도 이미 발급된 토큰의 서명 자체는 여전히 유효하므로, 서버 레벨에서의 즉각적인 세션 종료가 불가능합니다.
3. **분산 컨테이너 환경의 안정성 위협:** Docker 격리 환경에서 외부 Nginx 단일 진입점, Spring Boot 런타임, Redis 및 MySQL 간의 포트 바인딩 및 의존성 장애가 발생할 경우, 장애 전파(Cascading Failure)로 시스템 전체가 블로킹될 위험이 존재합니다.

---

## 2. Context & Constraints (배경 맥락 및 제약 조건)
본 프로젝트(`26-05adf`)는 다음과 같은 기술적 제약과 요구사항 하에서 설계되었습니다:

- **런타임 및 프레임워크:** Java 17, Spring Boot 3.3.2, Spring Security 6, Spring Data JPA, MySQL 8.0, Redis 7.0
- **컨테이너 오케스트레이션:** Docker Compose 기반 7개 서비스(Nginx, Backend, MySQL, Redis, Prometheus, VictoriaMetrics, Grafana)의 로컬 및 단일 호스트 격리 운영
- **성능 및 지연시간 제약:** 동시 70 가상 사용자(VU) 부하 환경에서 P95 응답 지연시간 50ms 미만, 에러율 1% 미만 유지 필수
- **엔지니어링 거버넌스 (`SA-1`):** 코드 변경 전 `task_progress.md` 정의, 작업 완료 후 `changelogs/` 의무 기록, 모든 기능은 10종의 자동화 단위/통합 테스트를 100% 통과해야 커밋 허용

---

## 3. Technical Decision & Trade-off Analysis (설계 및 의사결정)

### 3.1 토큰 이원화 및 수명주기 설계 (Stateless Access + Stateful Refresh)
- **대안 1: 순수 Stateless JWT (Access Token 30분 + Refresh Token 14일)**
  - *단점:* 토큰 탈취 시 14일간 무방비 노출, 로그아웃 불가.
- **대안 2: 완전 RDBMS 세션 관리**
  - *단점:* 모든 API 호출마다 RDBMS I/O가 발생하여 Throughput 저하 및 DB 커넥션 풀 고갈.
- **최종 선택: [Access Token (1h, Stateless) + RTR Refresh Token (7d, Redis) + Redis Blacklist]**
  - *장점:* 일반 API 요청은 DB/Redis 조회 없이 JWT 서명만 검증하여 고성능(P95 9.98ms)을 유지하고, 갱신 및 로그아웃 시에만 Redis 인메모리를 활용하여 완벽한 세션 제어 달성.

### 3.2 Refresh Token Rotation (RTR) 및 Replay Attack 방어 메커니즘
- 토큰 재발급(`/api/auth/refresh`) 시 Redis에 적재된 UUID JTI(JWT ID)를 대조하고, 일치 시 **기존 JTI를 즉시 파기한 후 신규 Access Token 및 Refresh Token을 동시 발급**.
- 만약 탈취자가 이전 JTI를 재사용하여 토큰을 갱신하려 하면, Redis에 해당 JTI가 존재하지 않으므로 즉시 `401 INVALID_REFRESH_TOKEN`을 반환하고 사용자 세션을 강제 무효화.

### 3.3 M:N RBAC 인가 계층 정규화
- 단순 역할(`ROLE_USER`, `ROLE_ADMIN`) 문자열 비교가 아닌, `User -> Role -> Permission` M:N 다대다 매핑 구조를 구축하여 엔드포인트별 세부 인가(Method Security & Security Filter) 적용.

---

## 4. Implementation (핵심 구현)

### 4.1 Redis 기반 Token Blacklist 구현
- **Source:** `backend/src/main/java/com/example/demo/auth/security/TokenBlacklistService.java`
- **Commit:** `9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f`
```java
@Slf4j
@Service
@RequiredArgsConstructor
public class TokenBlacklistService {

    private static final String BLACKLIST_KEY_PREFIX = "blacklist:";
    private final RedisTemplate<String, String> redisTemplate;

    public void blacklist(String jti, long expirationMillis) {
        if (jti == null || jti.isBlank() || expirationMillis <= 0) {
            return;
        }

        try {
            redisTemplate.opsForValue().set(
                    buildKey(jti),
                    "1",
                    Duration.ofMillis(expirationMillis)
            );
            log.debug("Blacklisted token registered. jti={}, ttlMs={}", jti, expirationMillis);
        } catch (DataAccessException e) {
            log.error("Failed to register token to Redis blacklist. jti={}", jti, e);
            throw new RedisUnavailableException("Redis is unavailable for blacklist registration", e);
        }
    }

    public boolean isBlacklisted(String jti) {
        if (jti == null || jti.isBlank()) {
            return false;
        }

        try {
            return Boolean.TRUE.equals(
                    redisTemplate.hasKey(buildKey(jti))
            );
        } catch (DataAccessException e) {
            log.error("Failed to check Redis blacklist. jti={}", jti, e);
            throw new RedisUnavailableException("Redis is unavailable for blacklist check", e);
        }
    }

    private String buildKey(String jti) {
        return BLACKLIST_KEY_PREFIX + jti;
    }
}
```

### 4.2 Nginx Reverse Proxy 및 Docker Compose 네트워크 구성
- **Source:** `26-05adf/docker-compose.yml`, `nginx/default.conf`
- Nginx를 호스트 유일의 외부 노출 포트(80)로 설정하고, `/api/*` 요청만 백엔드 컨테이너(`backend:8080`)로 프록시 패스.
- Spring Boot의 Redis 호스트는 `SPRING_REDIS_HOST: redis` 환경변수로 주입하여 컨테이너 DNS 바인딩 보장.

---

## 5. Verification & Testing (검증 및 테스트)

### 5.1 10종 핵심 자동화 테스트 스위트 (100% Pass)
- `AuthControllerTest.java` / `AuthServiceTest.java`: 로그인/재발급 DTO 및 비즈니스 검증 `[VERIFIED]`
- `JwtAuthenticationFilterTest.java`: Header 내 Bearer 파싱 및 SecurityContext 주입 검증 `[VERIFIED]`
- `RefreshTokenRepositoryTest.java`: Redis JTI TTL 및 Key-Value 적재 무결성 검증 `[VERIFIED]`
- `SecurityIntegrationTest.java`: RTR 토큰 재발급 후 구버전 토큰 재사용 차단 검증 `[VERIFIED]`
- `TokenBlacklistServiceTest.java`: 로그아웃된 Access Token 인가 필터 차단 검증 `[VERIFIED]`
- `RbacSecurityIntegrationTest.java` / `PermissionIntegrationTest.java`: RBAC 403 차단 검증 `[VERIFIED]`

### 5.2 k6 부하 및 스트레스 테스트 실측 검증
- **Source:** `26-05adf/docs/performance/k6-load-test.md` Section 3.2
- **조건:** 70 VU 동시 부하, 1분(60s) 지속 측정, 3회 반복
- **실측 지표:**
  - 5차 Run: Avg 4.73ms | P95 8.77ms | 469 req/s | Error 0.00%
  - 6차 Run: Avg 6.01ms | P95 10.61ms | 457 req/s | Error 0.00%
  - 7차 Run: Avg 6.18ms | P95 10.57ms | 465 req/s | Error 0.00%
  - **3회 산술 평균 Fact:** **Avg 5.64 ms, P95 9.98 ms, Throughput 463 req/s, Error Rate 0.00%** (모든 Threshold 통과).

---

## 6. Real-World Incident Troubleshooting (장애 분석 및 복구)

### 6.1 TS-01-REDIS: Redis 장애 시 커맨드 타임아웃 및 블로킹 해결
- **Symptom:** Redis 다운 시 백엔드 API가 최대 1분간 응답하지 않고 프론트엔드 흰 화면 발생.
- **Resolution:** 장애 분석 보고서(`01-redis-failure.md`) 기반 Lettuce 타임아웃 단축(2초) 정책을 수립하고, 백엔드 `JwtAuthenticationFilter` 및 `TokenBlacklistService`에서 `RedisUnavailableException` 발생 시 503 Service Unavailable로 신속 격리하여 서블릿 스레드 풀 고갈을 방어 `[VERIFIED]`.

### 6.2 TS-001: JWT Refresh Token 갱신 실패 시 무한 루프 이슈
- **Symptom:** 토큰 만료 후 클라이언트 인터셉터와 서버 간 초당 수십 회 401 재요청 무한 루프 발생.
- **Root Cause:** 401 수신 시 무조건 재발급을 시도하고 실패 시 탈출 조건(Exit Condition)이 누락됨.
- **Resolution:** Single Flight 토큰 재발급 패턴 구축 및 401 시 즉시 로컬 세션 파기 및 로그인 리다이렉트 `[VERIFIED]`.

### 6.3 TS-003: Docker Compose 환경 내 Redis localhost 바인딩 실패
- **Symptom:** 컨테이너 구동 시 `Connection refused: localhost/127.0.0.1:6379` 발생.
- **Root Cause:** 컨테이너 내부에서 `localhost`는 컨테이너 자신(Loopback)을 가리키는 고립 문제.
- **Resolution:** `docker-compose.yml`의 `SPRING_REDIS_HOST: redis` 주입 및 `application.yaml`의 `${SPRING_REDIS_HOST:localhost}` 프로파일 분리 `[VERIFIED]`.

---

## 7. Result & Impact (성과 및 결과)
1. **보안 무결성 확보:** 무상태 JWT의 확장성을 살리면서도 RTR과 Redis Blacklist를 통해 재사용 공격 차단 및 즉시 로그아웃 100% 구현 `[VERIFIED]`.
2. **고성능 저지연 증명:** 70 VU 동시 부하 상황에서 3회 평균 P95 9.98ms, 처리량 463 req/s, 오류율 0.00% 달성 `[VERIFIED]`.
3. **인프라 안정성 및 복원력:** Nginx 단일 진입점을 통한 포트 격리 및 Redis 타임아웃 2초 방어를 통해 장애 전파 차단 `[VERIFIED]`.
4. **엔지니어링 프로세스 혁신:** SA-1 거버넌스 기반의 Documentation-First AI 협업 라이프사이클을 통해 변경 이력과 테스트 무결성 완벽 유지 `[DOCUMENTED]`.

---

## 8. Limitations & Next Steps (한계점 및 향후 로드맵)

### 8.1 현재 시스템의 트레이드오프 및 한계
- 단일 Nginx 및 단일 Spring Boot 인스턴스로 구성되어 있어, 1,000+ VU 이상의 대규모 트래픽 분산을 위한 L7 로드밸런서(ALB) 및 오토스케일링은 미적용 상태임.
- 코드 상의 N+1 방지 로직(`@EntityGraph`)은 적용되었으나, 쿼리 수 비교 전/후 벤치마크 실측 수치는 아직 미보유.

### 8.2 Next Steps (`[PLANNED]` 과제)
- **JPA N+1 쿼리 최적화 실측 벤치마크:** Batch Size 및 Fetch Join 적용 전/후 실행 쿼리 수 및 힙 메모리 정밀 측정 `[PLANNED]`.
- **비동기 메시지 큐 (Message Queue):** 이벤트 급증 시 부하 분산을 위한 Apache Kafka / RabbitMQ 파이프라인 도입 `[PLANNED]`.
- **프론트엔드 상태 캐싱 고도화:** React Query staleTime/gcTime 정책 수립 및 Route Guard 깜빡임 방지 최적화 (Phase 2-2, 2-3) `[PLANNED]`.
- **클라우드 보안 및 SSL 자동화:** AWS KMS / HashiCorp Vault 기반 Secret 주입 및 Let's Encrypt TLS 자동화 `[PLANNED]`.
- **대규모 분산 부하 테스트:** 1,000+ VU 분산 환경 k6 부하 테스트 수행 `[PLANNED]`.
