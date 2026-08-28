# Verification Specifications (`PR-Files/verification`)

## 1. Responsibility
본 디렉터리는 시스템의 무결성을 증명하는 테스트 스위트, 보안 검증 시나리오, 통합 테스트 결과 및 데이터 계층 검증 증거 장부를 다룹니다.

## 2. Core Documents
1. [`DATA_LAYER_VERIFICATION.md`](file:///C:/Users/bluej/Desktop/PR-1A1/PR-Files/verification/DATA_LAYER_VERIFICATION.md): MySQL 스키마 무결성, Redis 임시 세션 모델, Lua Atomic Rotation 1-RTT 증명, 4대 검증 레벨 매트릭스 및 런타임 CLI 가이드.
2. [`SECURITY_VERIFICATION_REPORT.md`](file:///C:/Users/bluej/Desktop/PR-1A1/PR-Files/verification/SECURITY_VERIFICATION_REPORT.md): 10종 핵심 보안 테스트 스위트 검증 보고서.

## 3. Source of Truth Mapping
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

## 4. Verification Matrix Overview
- **인증 무결성:** 만료된 토큰 거부, 변조된 토큰 거부, JTI 불일치 시 401 반환 검증
- **RTR 검증:** 갱신 시 기존 Refresh Token 무효화 및 신규 발급 검증
- **Blacklist 검증:** 로그아웃된 Access Token 재호출 차단 검증
- **RBAC 인가 검증:** 권한 없는 사용자의 엔드포인트 접근 시 403 Forbidden 검증
- **Data Layer 원자성:** Redis Lua Script를 통한 Check-Then-Act Race Condition 방어 검증

