# 05. Core Backend Implementation & DB Governance

## What
Java 17 불변 Record DTO를 통한 계층 분리, `ApiResponse<T>` 통일 포맷 및 `GlobalExceptionHandler`, Flyway V1~V5를 통한 데이터베이스 DDL 버전 관리 체계.

## Why
- Entity의 외부 노출 방지, 영속성 컨텍스트 부수 효과 차단 및 캡슐화 강화.
- 클라이언트-서버 간 일관된 응답/에러 규격 수립으로 프론트엔드 통신 안정성 제고.
- `ddl-auto: update` 사용 위험성을 배제하고 다중 환경 간 스키마 일치 및 이력 추적 보장.

## How
- **불변 Record DTO:** 요청/응답 객체에 Java 17 `record` 키워드를 적용하여 얕은 복사/수정 차단.
- **통일 응답 규격:** `ApiResponse<T>(boolean success, T data, String message, String errorCode)` 래퍼 구조.
- **중앙화된 예외 처리:** `@RestControllerAdvice` 기반 `GlobalExceptionHandler`에서 비즈니스 예외 및 보안 예외 표준화.
- **Flyway 스키마 거버넌스:**
  - `V1__init_schema.sql` (기본 DDL)
  - `V2__init_authority_schema.sql` (인가 스키마)
  - `V3__init_common_schema.sql` (공통 엔티티)
  - `V4__insert_permissions.sql` (권한 시드)
  - `V5__insert_test_users.sql` (테스트 사용자 시드)

## Evidence
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md` Section 2.3 & 3.2
- `26-05adf/backend/src/main/java/com/example/demo/common/response/ApiResponse.java`
- `26-05adf/backend/src/main/java/com/example/demo/common/exception/GlobalExceptionHandler.java`
- `26-05adf/backend/src/main/resources/db/migration/` (V1~V5 SQL)

## Result
- DTO 캡슐화 및 계층 분리 무결성 검증 `[IMPLEMENTED]`
- Flyway V1~V5 자동 마이그레이션 정상 실행 확인 `[IMPLEMENTED]` `[VERIFIED]`

## Status
`[IMPLEMENTED]` `[VERIFIED]` `[DOCUMENTED]`

## Source
- `26-05adf` (`feature/auth@0603@1401`)
- `PR-Files/specification/AUTH_AND_SECURITY_SPEC.md`

## Presentation Use
- **Slide 04:** Backend Clean Architecture & DTO Isolation (계층 분리 및 공통 규격)
- **Slide 08:** Database Schema & Migration Governance (Flyway 형상 관리)
