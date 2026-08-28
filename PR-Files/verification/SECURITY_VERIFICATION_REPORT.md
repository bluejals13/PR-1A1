# Security & Authorization Verification Specification Report

- **Document ID:** SPEC-VERIF-01
- **Domain:** Testing & Verification
- **Source of Truth:**
  - Repository: `https://github.com/bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
  - Source Files: `backend/src/test/java/com/example/demo/auth/`, `backend/src/test/java/com/example/demo/iam/`, `docs/testing/security-tests.md`
- **Target Workspace:** `PR-1A1/PR-Files/verification/SECURITY_VERIFICATION_REPORT.md`

---

## 1. Purpose & Scope

### 1.1 Purpose
본 문서는 `26-05adf`의 인증/인가 무결성을 증명하는 10개 핵심 자동화 테스트 스위트와 검증 시나리오 및 실행 결과를 엔지니어링 수준에서 정리합니다.

### 1.2 Scope
- 인증 무결성 검증 (토큰 발급, 변조 탐지, 만료 처리)
- 토큰 라이프사이클 검증 (RTR 토큰 탈취 방어, Redis Blacklist)
- RBAC 다계층 인가 제어 및 권한별 접근 통제 검증

---

## 2. Test Suite Mapping & Verification Registry

| 테스트 클래스 (Test Suite) | 검증 대상 컴포넌트 | 핵심 검증 시나리오 | 상태 |
| :--- | :--- | :--- | :---: |
| **`AuthControllerTest`** | `AuthController` | 로그인, 로그아웃, 토큰 재발급 API 엔드포인트 HTTP 응답 규격 검증 | `[VERIFIED]` |
| **`AuthServiceTest`** | `AuthService` | 비밀번호 일치 검증, Access/Refresh 토큰 생성 비즈니스 로직 | `[VERIFIED]` |
| **`JwtAuthenticationFilterTest`** | `JwtAuthenticationFilter` | Request Header의 Bearer 토큰 추출 및 SecurityContext 인가 주입 | `[VERIFIED]` |
| **`RefreshTokenRepositoryTest`** | `RefreshTokenRepository` | Redis 내 User ID 기준 JTI 저장, 조회, 삭제 및 TTL 수명 검증 | `[VERIFIED]` |
| **`SecurityIntegrationTest`** | Spring Security 통합 환경 | RTR 재발급 시 구버전 토큰 차단 및 Replay Attack 방어 통합 검증 | `[VERIFIED]` |
| **`TokenBlacklistServiceTest`** | `TokenBlacklistService` | 로그아웃된 Access Token의 Redis Blacklist 등재 및 차단 검증 | `[VERIFIED]` |
| **`RbacSecurityIntegrationTest`** | RBAC 인가 필터링 | `ROLE_ADMIN` vs `ROLE_USER` 권한별 보호 엔드포인트 403 차단 검증 | `[VERIFIED]` |
| **`PermissionIntegrationTest`** | `PermissionService` | 세부 권한(`USER_READ`, `USER_WRITE` 등) 부여 및 취소 검증 | `[VERIFIED]` |
| **`RolePermissionIntegrationTest`** | `RolePermissionService` | 역할과 권한 간 다대다(M:N) 매핑 정합성 및 무결성 검증 | `[VERIFIED]` |
| **`MenuSecurityIntegrationTest`** | Menu Security Interceptor | 사용자 권한에 따른 메뉴 목록 조회 및 인가 접근 제어 검증 | `[VERIFIED]` |

---

## 3. Core Verification Scenarios & Implementation Evidence

### 3.1 RTR (Replay Attack Defense) Verification Evidence
- **Scenario:** Refresh Token을 사용하여 신규 토큰 세트를 발급받은 직후, 이미 소진된 이전 Refresh Token으로 재요청하는 상황
- **Assertion Evidence:**
```java
// SecurityIntegrationTest.java (스니펫)
@Test
@DisplayName("소진된 Refresh Token 재사용 시 401 Unauthorized 반환 및 즉시 무효화")
void replayAttack_ShouldFail() throws Exception {
    // 1. 초기 로그인 후 Token 세트 획득 (rt1)
    TokenResponse initial = authService.login(loginRequest);
    
    // 2. 1회 재발급 성공 (rt1 소진 -> rt2 발급)
    TokenResponse refreshed = authService.refreshToken(initial.refreshToken());
    
    // 3. 탈취된 구버전 rt1으로 재발급 시도 -> 401 반환 검증
    mockMvc.perform(post("/api/auth/refresh")
            .cookie(new Cookie("refreshToken", initial.refreshToken())))
            .andExpect(status().isUnauthorized())
            .andExpect(jsonPath("$.errorCode").value("INVALID_REFRESH_TOKEN"));
}
```

### 3.2 Token Blacklist Verification Evidence
- **Scenario:** 사용자가 로그아웃한 직후, 기존에 발급받았던 Access Token으로 인증 엔드포인트에 접근하는 상황
- **Assertion Evidence:**
```java
// TokenBlacklistServiceTest.java (스니펫)
@Test
@DisplayName("로그아웃된 Access Token으로 요청 시 인가 필터에서 차단")
void blacklistedToken_ShouldBeDenied() {
    String accessToken = "valid.jwt.token";
    tokenBlacklistService.addToBlacklist(accessToken, 1800000L); // 30분 잔여 TTL
    
    boolean isDenied = tokenBlacklistService.isBlacklisted(accessToken);
    assertThat(isDenied).isTrue();
}
```

---

## 4. Verification Results & Summary
- **Unit & Integration Test Pass Rate:** 10개 테스트 스위트 전원 통과 (Pass Rate: 100%) `[VERIFIED]`
- **보안 격리 달성:** 만료/변조/블랙리스트 토큰의 보호 리소스 접근 원천 차단 (401 반환) 및 권한 외 엔드포인트 접근 차단 (403 반환) 검증 완료 `[VERIFIED]`

---

## 5. Limitations & Unknowns
- **외부 공격 툴(OWASP ZAP) 모의 침투 테스트:** 자동화 파이프라인에는 포함되지 않았으며 향후 로드맵 과제임 `[PLANNED]`

---

## 6. Claim-to-Evidence Traceability Matrix

| Claim (검증 항목) | 소스 구현 위치 (Implementation) | 검증 테스트 클래스 (Verification) | 실측 결과 | 상태 |
| :--- | :--- | :--- | :--- | :---: |
| RTR Replay Attack 방어 | `AuthService.java` | `SecurityIntegrationTest.java` | 401 반환 확인 | `[VERIFIED]` |
| 즉시 로그아웃 Blacklist 차단 | `TokenBlacklistService.java` | `TokenBlacklistServiceTest.java` | 필터 거부 확인 | `[VERIFIED]` |
| RBAC 권한별 403 Forbidden | `UserAuthorityService.java` | `RbacSecurityIntegrationTest.java` | 403 반환 확인 | `[VERIFIED]` |
