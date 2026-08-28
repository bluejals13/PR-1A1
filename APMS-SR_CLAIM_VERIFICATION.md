# APMS.SR Claim-to-Evidence Verification Report

- **Document ID:** APMS-SR-CLAIM-VERIF-01
- **Target Repository:** `PR-1A1`
- **Source of Truth Repositories:**
  - `26-05adf` (Branch: `feature/auth@0603@1401`): Backend App, Security, k6 Tests, Docker, DB Migrations
  - `SA-1` (Branch: `main`): AI Engineering Process, 8-Stage Lifecycle, Governance Rules
- **Verification Protocol:** Zero-Hallucination & Evidence-First Standard

---

## 1. Verification Classification Protocol (5대 상태 체계)

| 상태 태그 | 정의 및 기준 | 적용 원칙 |
| :--- | :--- | :--- |
| `[VERIFIED]` | 자동화 테스트(JUnit), 부하 테스트(k6), 실행 로그로 동작과 수치가 검증 완료된 항목 | 실측 수치 및 테스트 클래스 존재 필수 |
| `[IMPLEMENTED]` | 코드가 실제로 작성되어 리포지토리에 존재하나 정량 검증 수치는 없는 항목 | 소스 코드 파일 경로 확인 |
| `[DOCUMENTED]` | 아키텍처, 설계 규격, 컨벤션, 장애 보고서 등 공식 기술 문서에 명시된 항목 | 공식 마크다운 문서 확인 |
| `[PARTIAL]` | 구현 및 연동은 되었으나, 실시간성 또는 대시보드 검증이 부분적인 상태 | Grafana 대시보드 등 과장 금지 |
| `[PLANNED]` | 향후 개선 예정으로 계획된 상태 (Roadmap) | 구현 완료로 표기 절대 금지 |

---

## 2. Domain-by-Domain Claim-to-Evidence Matrix

### 2.1 Security & Authentication
| # | 엔지니어링 주장 (Claim) | 소스 구현 위치 (Implementation) | 검증 테스트 / 증거 (Verification) | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 1 | Stateless JWT Access Token (1시간 만료, Header Bearer 전송) | `com.example.demo.auth.security.JwtTokenProvider` | `JwtAuthenticationFilterTest.java` | `[VERIFIED]` |
| 2 | Refresh Token (7일 만료, HttpOnly Secure Cookie 전송, UUID JTI 기반) | `auth/security/RefreshTokenRepository.java` (`auth:refresh:user:{userId}`) | `RefreshTokenRepositoryTest.java` (save, delete) | `[VERIFIED]` |
| 3 | Refresh Token Rotation (RTR): Lua Script 기반 1-RTT 원자적 JTI 교체 | `auth/security/RefreshTokenRepository.java` (Lua Script) | `RefreshTokenRepositoryTest.java` (rotateSuccess, rotateFail, rotateNull) | `[VERIFIED]` |
| 4 | Token Blacklist: 로그아웃 시 Access Token 잔여 TTL 동안 Redis 블랙리스트 등록 | `com.example.demo.auth.service.TokenBlacklistService` | `TokenBlacklistServiceTest.java` (blacklistedToken_ShouldBeDenied) | `[VERIFIED]` |
| 5 | RBAC (User-Role-Permission M:N 다대다 매핑 인가 필터링) | `com.example.demo.iam.entity.*`, `UserAuthorityService` | `RbacSecurityIntegrationTest.java` (403 Forbidden 확인) | `[VERIFIED]` |
| 6 | Flyway V1~V5 DB 마이그레이션 및 Composite PK/FK 스키마 무결성 | `src/main/resources/db/migration/V1~V5__*.sql` (`V2__init_authority_schema.sql`) | DB 구동 및 테이블 생성 로그, FK Cascade 무결성 | `[IMPLEMENTED]` |

### 2.2 Performance & Load Testing (k6)
| # | 엔지니어링 주장 (Claim) | 소스 구현 위치 (Implementation) | 검증 테스트 / 증거 (Verification) | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 7 | 70 VUs 동시 부하 환경 1분 지속 측정 | `k6/scenarios/load.test.js` | k6 실행 요약 로그 (5~7차 실행) | `[VERIFIED]` |
| 8 | 평균 응답 시간 5.64ms (3회 평균: 4.73ms, 6.01ms, 6.18ms) | `k6/config/thresholds.js` (`avg<20`) | k6 통계 결과 리포트 (임계치 통과) | `[VERIFIED]` |
| 9 | P95 레이턴시 9.98ms (3회 평균: 8.77ms, 10.61ms, 10.57ms) | `k6/config/thresholds.js` (`p(95)<50`) | k6 통계 결과 리포트 (임계치 통과) | `[VERIFIED]` |
| 10 | 초당 처리량(Throughput) 463 req/s 달성 | `k6/scenarios/load.test.js` | k6 Throughput 집계 지표 | `[VERIFIED]` |
| 11 | 에러율 0.00% (0 errors, 임계치 `rate<1%` 통과) | `k6/config/thresholds.js` | k6 HTTP Fail 지표 (전 차수 0건) | `[VERIFIED]` |

### 2.3 Infrastructure & Network Topology
| # | 엔지니어링 주장 (Claim) | 소스 구현 위치 (Implementation) | 검증 테스트 / 증거 (Verification) | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 12 | Nginx Reverse Proxy 단일 진입점 (Port 80) 및 라우팅 | `nginx/default.conf` | k6 및 브라우저 API 프록시 호출 성공 | `[VERIFIED]` |
| 13 | Docker Compose 7개 컨테이너 오케스트레이션 및 브리지 격리 | `docker-compose.yml` | 컨테이너 서비스 기동 및 상호 통신 | `[IMPLEMENTED]` |
| 14 | MySQL 8.0 & Redis 7.0 역할 분리 (영속 스토리지 vs In-Memory) | `docker-compose.yml`, `application.yml` | Flyway 마이그레이션 & Redis TTL 연동 | `[IMPLEMENTED]` |

### 2.4 Observability Pipeline
| # | 엔지니어링 주장 (Claim) | 소스 구현 위치 (Implementation) | 검증 테스트 / 증거 (Verification) | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 15 | Prometheus 메트릭 스크랩 (`/actuator/prometheus`) | `backend/pom.xml` (micrometer), `prometheus.yml` | JVM Heap, CPU, HikariCP 메트릭 수집 확인 | `[VERIFIED]` |
| 16 | VictoriaMetrics 시계열 스토리지 영속화 | `docker-compose.yml` (victoriametrics:8428) | Prometheus Remote Write 연동 | `[IMPLEMENTED]` |
| 17 | Grafana 모니터링 대시보드 | `docker-compose.yml` (grafana:3000) | 대시보드 컨테이너 구성 (실시간 모니터링 완전 검증은 아님) | `[PARTIAL]` |

### 2.5 Incident Troubleshooting (TS 6단계)
| # | 엔지니어링 주장 (Claim) | 장애 원인 및 해결 위치 | 검증 결과 / 증거 | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 18 | TS-01-REDIS: Redis 타임아웃 60s 블로킹 ➔ 2s 단축 | `application.yml` (lettuce timeout 2000ms), 503 반환 | Redis 다운 시 2s 이내 503 응답 확인 | `[VERIFIED]` |
| 19 | TS-001: JWT Refresh 갱신 실패 시 401 무한 루프 차단 | 클라이언트 Axios 인터셉터 탈출 조건 및 상태 초기화 | 401 시 1회 시도 후 세션 종료 확인 | `[VERIFIED]` |
| 20 | TS-003: Docker 환경 내 Redis localhost 바인딩 실패 해결 | `application.yml` (`${SPRING_REDIS_HOST:localhost}`) | 컨테이너 내부 `redis:6379` DNS 해석 확인 | `[VERIFIED]` |

### 2.6 AI-Assisted Engineering Workflow
| # | 엔지니어링 주장 (Claim) | 소스 구현 위치 (Implementation) | 검증 결과 / 증거 | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 21 | SA-1 8단계 라이프사이클 통제 프로세스 | `SA-1/conventions/rules.md` | Task Reading ➔ Plan ➔ Verification 준수 | `[DOCUMENTED]` |
| 22 | Zero-Chatter & Documentation-First 거버넌스 | `SA-1/conventions/rules.md`, `changelogs/` | 마크다운 변경 이력 및 정밀 diff 협업 | `[DOCUMENTED]` |

### 2.7 Limitations & Roadmap (미구현 항목 격리)
| # | 계획 항목 (Planned Items) | 현재 상태 | 로드맵 계획 | 판정 상태 |
| :- | :--- | :--- | :--- | :---: |
| 23 | JPA N+1 쿼리 최적화 실측 벤치마크 (Batch Size/Fetch Join 정량 비교) | 미측정 | 로드맵 과제로 관리 | `[PLANNED]` |
| 24 | Message Queue (Kafka / RabbitMQ) 비동기 파이프라인 | 미구현 | 대용량 트래픽 대비 로드맵 | `[PLANNED]` |
| 25 | Redis Cluster 다중화 및 분산 캐싱 | 미구현 | 가용성 확장 로드맵 | `[PLANNED]` |
| 26 | OWASP ZAP 모의 침투 보안 테스트 자동화 | 미구현 | 파이프라인 확장 로드맵 | `[PLANNED]` |
| 27 | Kubernetes 클러스터 오케스트레이션 & HPA | 미구현 | 분산 인프라 로드맵 | `[PLANNED]` |
| 28 | SSL/TLS Production 인증서 적용 (HTTPS) | 미구현 (현재 Port 80) | 프로덕션 환경 로드맵 | `[PLANNED]` |
| 29 | 1,000+ VU 분산 부하 테스트 | 미수행 (현재 70 VU 완료) | 분산 환경 부하 로드맵 | `[PLANNED]` |

---

## 3. Fact Verification Summary

- **Total Claims:** 29 Items
- **Verified Fact (`[VERIFIED]`):** 14 Items (48.3%)
- **Implemented (`[IMPLEMENTED]`):** 5 Items (17.2%)
- **Documented (`[DOCUMENTED]`):** 2 Items (6.9%)
- **Partial (`[PARTIAL]`):** 1 Item (3.4% - Grafana)
- **Planned / Roadmap (`[PLANNED]`):** 7 Items (24.1%)

본 문서는 `PR-1A1`의 모든 포트폴리오 산출물(Presentation, HTML, Case Study)의 근거 기준 자료로 사용됩니다.
