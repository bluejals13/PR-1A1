# Technical Specifications (`PR-Files/specification`)

## 1. Purpose (목적)
인증/인가, JWT/Redis 세션 수명 주기, RTR(Refresh Token Rotation), RBAC 권한 계층 모델, API 응답/예외 규격, Flyway DB 마이그레이션 규칙 등 시스템 구현 기술 명세를 체계적으로 정의합니다.

## 2. Input / Source (원천 데이터)
- `26-05adf/backend/src/main/java/com/example/demo/auth/` (JWT Provider, Security Filter, AuthService)
- `26-05adf/backend/src/main/java/com/example/demo/iam/` (User, Role, Permission Entity & Admin API)
- `26-05adf/backend/src/main/resources/db/migration/` (Flyway V1~V5 SQL 마이그레이션 스크립트)
- `26-05adf/docs/03_Backend_Conventions.md`, `docs/reference/security.md`

## 3. Output (산출물)
- **`AUTH_AND_SECURITY_SPEC.md`**: 인증/인가 및 보안 아키텍처 상세 기술 명세서

## 4. What belongs here (포함되는 자료)
- Access Token (1h, Bearer Header) 및 Refresh Token (7d, HttpOnly Cookie) 규격
- RTR 기반 1회용 JTI 검증 및 Redis 블랙리스트 잔여 TTL 명세
- `User ➔ Role ➔ Permission` M:N RBAC 인가 모델 및 메뉴 접근 제어 규격
- Record 기반 불변 DTO, `ApiResponse<T>`, Flyway 스키마 명세

## 5. What does NOT belong here (포함되지 않는 자료)
- 테스트 실행 결과 및 합격 여부 (-> `verification/` 영역)
- 부하 테스트 수치 (-> `performance/` 영역)
- 발표용 구술 스크립트 및 슬라이드 (-> `PRD-PO/` 영역)

## 6. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO/presentation/source/04_AUTH_AND_RBAC.md`, `05_CORE_IMPLEMENTATION.md`, `06_SECURITY.md` 및 슬라이드 002/005/006/007 등은 본 디렉터리의 엔지니어링 명세를 바탕으로 핵심 메시지와 시각화 요소를 구성합니다.
