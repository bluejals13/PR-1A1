# 04. Authentication & RBAC Authorization

## What
Stateless JWT 이원화 수명주기 관리, Redis 기반 Refresh Token Rotation(RTR), Token Blacklist, 그리고 정규화된 M:N 구조의 RBAC(Role-Based Access Control) 권한 인가 체계.

## Why
- Access Token의 탈취 위협을 줄이면서도 사용자에게 매끄러운 세션 연장 경험 제공.
- 세분화된 리소스 및 API 엔드포인트에 대한 역할/권한별 접근 제어를 체계화.
- 다계층 권한(User-Role-Permission-Menu)을 통해 기업용 애플리케이션 수준의 인가 거버넌스 달성.

## How
- **Token Lifecycle:**
  - **Access Token:** 1시간 (3,600,000 ms), Header `Authorization: Bearer <token>` 전달, JJWT Payload에 userId, roles, permissions 포함.
  - **Refresh Token:** 7일 (604,800,000 ms), HttpOnly/Secure Cookie 전달, UUID JTI 기반 식별 및 Redis 적재 (`auth:refresh:user:<userId>`).
  - **RTR (Refresh Token Rotation):** 재발급 시 기존 JTI 즉시 무효화 및 새 JTI 발급. 소진된 구버전 토큰 재시도 시 즉시 401 반환.
  - **Token Blacklist:** 로그아웃 시 Access Token의 잔여 TTL 동안 Redis(`blacklist:<jti>`)에 등록하여 즉시 차단.
- **RBAC Data Model:**
  - `users` (N:M) `roles` (N:M) `permissions` 및 `roles` (N:M) `menus` 정규화 테이블 구조.
  - Spring Security Custom Filter 및 `UserAuthorityService`를 통한 엔드포인트 인가 검증.

## Evidence
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 2.1 & 2.2
- `26-05adf/backend/src/main/java/com/example/demo/auth/jwt/JwtProvider.java`
- `26-05adf/backend/src/main/java/com/example/demo/auth/security/AuthService.java`
- `26-05adf/backend/src/main/java/com/example/demo/auth/security/UserAuthorityService.java`

## Result
- 토큰 탈취 Replay Attack 시나리오 100% 방어 및 401 차단 `[VERIFIED]`
- 로그아웃 토큰의 즉시 인가 거부 확인 `[VERIFIED]`
- `ROLE_ADMIN` vs `ROLE_USER` 권한별 403 Forbidden 정상 인가 분기 검증 `[VERIFIED]`

## Status
`[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md`

## Presentation Use
- **Slide 05:** Authentication Architecture (JWT 수명주기 & 전송 분리)
- **Slide 06:** Advanced Token Security (RTR & Redis Blacklist)
- **Slide 07:** Authorization & RBAC Multi-Tier Hierarchy (권한 계층 구조)
