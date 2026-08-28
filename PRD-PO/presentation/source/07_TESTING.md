# 07. Testing Strategy & Automated Verification

## What
인증, 인가, 토큰 수명주기, 데이터 무결성을 검증하는 10종의 핵심 JUnit 5 단위 및 통합 테스트 스위트.

## Why
- 복잡한 보안 로직(RTR, Blacklist, RBAC Filter) 변경 시 회귀 버그(Regression)를 방지하고 동작의 무결성을 기계적으로 증명하기 위함.
- 수동 검증에 의존하지 않는 자동화된 품질 게이트 확보.

## How
- **Auth Core Tests:**
  - `AuthControllerTest`: 엔드포인트 HTTP 규격 및 DTO 바인딩 검증
  - `AuthServiceTest`: 비밀번호 해싱 및 토큰 생성 비즈니스 로직 단위 테스트
  - `JwtAuthenticationFilterTest`: Request Header 파싱 및 SecurityContext 주입 검증
  - `RefreshTokenRepositoryTest`: Redis JTI TTL 저장/조회/삭제 검증
  - `SecurityIntegrationTest`: Spring Security 통합 환경에서 RTR 및 Replay Attack 방어 검증
  - `TokenBlacklistServiceTest`: 로그아웃 토큰의 Redis Blacklist 차단 검증
- **RBAC & Authorization Tests:**
  - `RbacSecurityIntegrationTest`: `ROLE_ADMIN` vs `ROLE_USER` 권한별 403 차단 검증
  - `PermissionIntegrationTest`: 세부 퍼미션 부여 및 검증
  - `RolePermissionIntegrationTest`: Role-Permission M:N 매핑 무결성 검증
  - `MenuSecurityIntegrationTest`: 메뉴 인가 인터셉터 검증

## Evidence
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md` Section 2, 3, 4
- `26-05adf/backend/src/test/java/com/example/demo/auth/`
- `26-05adf/backend/src/test/java/com/example/demo/iam/`

## Result
- 10종 핵심 테스트 스위트 전원 통과 (Pass Rate: 100%) `[VERIFIED]`
- 비인가 및 변조 토큰 시나리오 방어 100% 확인 `[VERIFIED]`

## Status
`[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md`

## Presentation Use
- **Slide 09:** Automated Security & Integration Verification (테스트 전략 및 검증 매트릭스)
