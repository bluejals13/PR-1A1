# Verification Specifications (`PR-Files/verification`)

## 1. Responsibility
본 디렉터리는 시스템의 무결성을 증명하는 테스트 스위트, 보안 검증 시나리오, 통합 테스트 결과를 다룹니다.

## 2. Source of Truth Mapping
- **Test Code Source (`backend/src/test/java/`):**
  - `auth/security/AuthControllerTest.java`
  - `auth/security/AuthServiceTest.java`
  - `auth/security/JwtAuthenticationFilterTest.java`
  - `auth/security/RefreshTokenRepositoryTest.java`
  - `auth/security/SecurityIntegrationTest.java`
  - `auth/security/TokenBlacklistServiceTest.java`
  - `iam/rbac/RbacSecurityIntegrationTest.java`
  - `iam/permission/PermissionIntegrationTest.java`
  - `iam/role/RolePermissionIntegrationTest.java`
  - `menu/MenuSecurityIntegrationTest.java`
- **Documentation Source:**
  - `26-05adf/docs/testing/security-tests.md`

## 3. Verification Matrix Overview
- **인증 무결성:** 만료된 토큰 거부, 변조된 토큰 거부, JTI 불일치 시 401 반환 검증
- **RTR 검증:** 갱신 시 기존 Refresh Token 무효화 및 신규 발급 검증
- **Blacklist 검증:** 로그아웃된 Access Token 재호출 차단 검증
- **RBAC 인가 검증:** 권한 없는 사용자의 엔드포인트 접근 시 403 Forbidden 검증
