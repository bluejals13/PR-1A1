# 06. Security Architecture & Threat Defense

## What
XSS, Replay Attack, 토큰 위변조, 권한 우회 공격에 대응하는 다계층 보안 방어 아키텍처 및 세션 무효화 메커니즘.

## Why
- 단일 방어선(Single Point of Failure)에 의존하지 않고, 네트워크-전송-필터-저장소 전 계층에서 보안 취약점을 방어하기 위함.
- 무상태 인증 체계에서 발생할 수 있는 보안 취약점(토큰 탈취 후 악용)을 실시간으로 차단.

## How
- **XSS 방어:** 민감한 Refresh Token은 JavaScript 접근이 불가능한 `HttpOnly`, `Secure`, `SameSite=Strict` Cookie로만 전송.
- **Replay Attack 방어 (RTR):** Refresh Token 재발급 시 고유 UUID JTI를 1회용으로 검증 후 즉시 파기. 이미 사용된 JTI로 요청 시 즉시 세션 차단.
- **즉시 세션 무효화 (Blacklist TTL):** 로그아웃 시 Access Token을 Redis에 등록하고, 잔여 유효시간(TTL)만큼만 키를 보관하여 메모리 낭비 없이 즉시 인가 차단.
- **Spring Security 6 SecurityFilterChain:** `JwtAuthenticationFilter` ➔ `UsernamePasswordAuthenticationFilter` ➔ `UserAuthorityService` 순의 엄격한 인가 파이프라인.

## Evidence
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 2.1 & 3.1
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md` Section 3.1 & 3.2
- `26-05adf/backend/src/main/java/com/example/demo/auth/service/TokenBlacklistService.java`

## Result
- 토큰 탈취 재사용 시도 차단 검증 완료 (401 반환) `[VERIFIED]`
- 로그아웃 후 잔여 유효시간 내 Access Token 접근 차단 검증 완료 `[VERIFIED]`
- 비인가 리소스 접근 차단 (403 반환) 검증 완료 `[VERIFIED]`

## Status
`[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/verification/SECURITY_VERIFICATION_REPORT.md`

## Presentation Use
- **Slide 06:** Advanced Token Security (RTR & Redis Blacklist)
- **Slide 09:** Automated Security & Integration Verification
