# Technical Specifications (`PR-Files/specification`)

## 1. Responsibility
본 디렉터리는 시스템의 상세 기술 명세를 다룹니다:
- JWT & Redis 토큰 수명 주기 및 제어 명세
- RBAC (Role-Based Access Control) 권한 체계 및 메뉴-퍼미션 매핑 명세
- RESTful API 및 전역 응답/예외 규격
- 데이터베이스 스키마 및 Flyway 마이그레이션 이력 명세

## 2. Source of Truth Mapping
- **Backend Source:**
  - `backend/src/main/java/com/example/demo/auth/` (JWT, Security, Token, Filter)
  - `backend/src/main/java/com/example/demo/iam/` (User, Role, Permission, Menu)
  - `backend/src/main/resources/db/migration/` (V1~V5 SQL)
  - `26-05adf/docs/reference/security.md`
  - `26-05adf/docs/03_Backend_Conventions.md`

## 3. Specification Items
| 영역 | 핵심 명세 | 상태 |
| :--- | :--- | :--- |
| **Authentication** | Access Token (1h, Header), Refresh Token (7d, HttpOnly Cookie, RTR, JTI) | `[IMPLEMENTED]` `[VERIFIED]` |
| **Blacklist** | 로그아웃 토큰 Redis 적재 (남은 TTL 적용) | `[IMPLEMENTED]` `[VERIFIED]` |
| **Authorization** | `User -> Role -> Permission` M:N RBAC 구조, 계층별 접근 제어 | `[IMPLEMENTED]` `[VERIFIED]` |
| **Response** | Record 기반 DTO, `ApiResponse<T>`, `GlobalExceptionHandler` | `[IMPLEMENTED]` `[DOCUMENTED]` |
| **Database** | MySQL 8.0, Flyway V1~V5 마이그레이션 스키마 | `[IMPLEMENTED]` `[DOCUMENTED]` |
