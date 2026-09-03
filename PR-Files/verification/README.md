# Verification Specifications (`PR-Files/verification`)

## 1. Purpose (목적)
시스템의 보안, 인증/인가 무결성, 데이터 계층 원자성 및 비즈니스 규칙이 테스트 코드로 100% 입증되었음을 증명하는 검증 결과 보고서와 증거 장부를 관리합니다.

## 2. Input / Source (원천 데이터)
- `26-05adf/backend/src/test/java/` 내 10종 핵심 테스트 스위트:
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
- `26-05adf/docs/testing/security-tests.md`

## 3. Output (산출물)
- **`DATA_LAYER_VERIFICATION.md`**: MySQL 스키마 무결성, Redis 임시 세션 모델, Lua Atomic Rotation 증명 보고서
- **`SECURITY_VERIFICATION_REPORT.md`**: 10종 핵심 보안 테스트 스위트 실행 결과 및 검증 보고서

## 4. What belongs here (포함되는 자료)
- 단위 테스트 및 통합 테스트 시나리오별 검증 내역 (만료 토큰 거부, RTR 회전, Blacklist 차단, 403 Forbidden)
- Redis Lua Script 원자성 및 Race Condition 방어 검증 증거
- 테스트 실행 커맨드 및 통과율 (`100% Pass`)

## 5. What does NOT belong here (포함되지 않는 자료)
- 부하/성능 테스트 실측치 (-> `performance/` 영역)
- 장애 발생 및 조치 내역 (-> `troubleshooting/` 영역)
- 단순 기능 설명 요약 (-> `specification/` 영역)

## 6. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO/presentation/slides/001/`의 `JUnit 10종 100% Pass [VERIFIED]` 배지와 `PRD-PO/presentation/source/07_TESTING.md`는 본 디렉터리의 실제 검증 데이터를 기반으로 작성됩니다.
