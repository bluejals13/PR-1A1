# Source of Truth Snapshot & Traceability Matrix

- **Snapshot Date:** 2026-08-27
- **Primary Source 1 (Application):** `bluejals13/26-05adf` (Branch: `feature/auth@0603@1401`)
- **Primary Source 2 (AI Agent / Process):** `bluejals13/SA-1` (Branch: `main`)
- **Target Processing Workspace:** `bluejals13/PR-1A1`

---

## 1. Status Classification (상태 구분 기준)

PR-1A1에서 생산되는 모든 기술적 내용과 포트폴리오 문서는 다음 5가지 상태 표기를 엄격히 준수합니다.

| 상태 태그 | 정의 | 판정 기준 |
| :--- | :--- | :--- |
| `[IMPLEMENTED]` | 코드가 실제로 작성되어 저장소에 존재하는 상태 | 26-05adf 내 소스 코드(.java, .ts, .sql 등) 존재 확인 |
| `[VERIFIED]` | 자동화 테스트나 부하 테스트로 검증 완료된 상태 | JUnit 테스트 통과, k6 실행 보고서 수치 실측 확인 |
| `[DOCUMENTED]` | 아키텍처, 컨벤션, 장애 보고서 등 문서화된 상태 | docs/, changelogs/ 내 마크다운 기술 문서 존재 확인 |
| `[PLANNED]` | 향후 개선 예정으로 계획된 상태 (Roadmap) | `task_progress.md` 미완료 항목 또는 Roadmap 기술 항목 |
| `[UNKNOWN]` | 현재 소스 코드 및 문서에서 확인되지 않은 상태 | 추측 금지, 사실 확인 전까지 포트폴리오에 기술 금지 |

---

## 2. Source of Truth 실측 팩트 요약 (Fact Base)

### 2.1 Backend & Security (`26-05adf`)
- **프레임워크 및 런타임:** Java 17, Spring Boot 3.3.2, Spring Security 6, Spring Data JPA, JJWT (0.12.x), Flyway, MySQL 8.0, Redis 7.0 `[IMPLEMENTED]`
- **인증(Authentication) 메커니즘:**
  - Stateless JWT Access Token (1시간 만료, Header Authorization: Bearer 전송) `[IMPLEMENTED]` `[VERIFIED]`
  - Refresh Token (7일 만료, HttpOnly Secure Cookie 전송, UUID JTI 기반 식별) `[IMPLEMENTED]` `[VERIFIED]`
  - Refresh Token Rotation (RTR): 토큰 재발급 시 기존 JTI 무효화 및 신규 JTI Redis 적재 `[IMPLEMENTED]` `[VERIFIED]`
  - Token Blacklist: 로그아웃 시 Access Token의 잔여 TTL 동안 Redis Blacklist에 등록 `[IMPLEMENTED]` `[VERIFIED]`
- **인가(Authorization) 메커니즘 (RBAC):**
  - User - Role - Permission 다대다(M:N) 매핑 구조 `[IMPLEMENTED]` `[VERIFIED]`
  - DB Schema (Flyway V1~V5): `users`, `roles`, `permissions`, `user_roles`, `role_permissions`, `menus`, `role_menus` `[IMPLEMENTED]`
  - Spring Security Custom Provider 및 UserAuthorityService를 통한 권한 인가 필터링 `[IMPLEMENTED]` `[VERIFIED]`
- **응답 및 예외 처리 규격:**
  - Record 기반 DTO 구조 `[IMPLEMENTED]`
  - `ApiResponse<T>` 통일 포맷 및 `GlobalExceptionHandler` 적용 `[IMPLEMENTED]` `[DOCUMENTED]`

### 2.2 Performance & Verification (`26-05adf`)
- **k6 부하 테스트 실측 지표 (Fact):**
  - **Virtual Users (VU):** 70 VUs `[VERIFIED]`
  - **Duration:** 1 min `[VERIFIED]`
  - **Throughput:** 463 req/s `[VERIFIED]`
  - **Avg Latency:** 5.64 ms `[VERIFIED]`
  - **P95 Latency:** 9.98 ms `[VERIFIED]`
  - **Error Rate:** 0.00% `[VERIFIED]`
- **부하 시나리오 구성:** `load.test.js`, `stress.test.js`, `spike.test.js`, `soak.test.js`, `read.flow.js`, `user.flow.js`, `admin-flow.js` `[IMPLEMENTED]`
- **모니터링 스택:** Docker Compose 기반 Nginx, Spring Boot, MySQL, Redis, Prometheus (포트 9090), VictoriaMetrics (포트 8428), Grafana (포트 3000) `[IMPLEMENTED]` `[DOCUMENTED]`

### 2.3 Troubleshooting Incident (`26-05adf`)
- **TS-01-REDIS (Redis 장애 및 복구):**
  - 현상: Redis 컨테이너 단절 시 Lettuce 커맨드 1분 타임아웃 발생 및 프론트엔드 흰 화면(Blank Screen) 노출 `[DOCUMENTED]`
  - 근본 원인: Redis 커맨드 타임아웃 미설정 및 토큰 검증 시 Redis 블로킹, 프론트엔드 Error Boundary 부재 `[DOCUMENTED]`
  - 해결: Lettuce 타임아웃 2초 단축, Redis 예외 래핑 처리, 프론트엔드 에러 핸들링 보강 `[DOCUMENTED]`

### 2.4 AI-Assisted Engineering Workflow (`SA-1`)
- **Zero-Chatter & Context Rules:** 프롬프트 규격화 및 diff 중심 변경 관리 `[DOCUMENTED]`
- **문서화 5대 원칙:** Reference(현재기준), ADR(불변), Troubleshooting(재발방지), Roadmap(문제중심), Duplication(중복금지) `[DOCUMENTED]`
- **AI 개발 사이클:**
  1. `Context Reading` (기존 코드 및 규약 확인)
  2. `Analysis & Planning` (`task_progress.md` 기반 범위 확정)
  3. `Agent Delegation` (정밀 변경 수행)
  4. `Verification` (JUnit / k6 검증)
  5. `Changelog & Documentation` (`changelogs/phase*` 기록)

### 2.5 Planned / Unverified (절대 구현 완료로 표기 금지)
- JPA N+1 문제 해결 세부 벤치마크 실측 수치: 계획 단계 `[PLANNED]`
- Message Queue (Kafka/RabbitMQ) 비동기 처리: 미구현 `[PLANNED]`
- 분산 캐시 클러스터링: 미구현 `[PLANNED]`

---

## 3. Claim-to-Evidence Traceability Matrix

모든 포트폴리오 및 기술문서는 아래와 같은 추적성 구조를 갖추어야 합니다.

```text
[Claim (주장)]
  └── [Source (출처 저장소 및 커밋/브랜치)]
        └── [Implementation (구현 파일 및 라인)]
              └── [Verification (테스트 코드/실행 로그)]
                    └── [Result (실측 결과 및 산출물)]
```
