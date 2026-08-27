# Presentation Deck Specification (`PRD-PO/presentation`)

## 1. Goal
- 면접 및 기술 발표를 위한 **12~15페이지 분량의 핵심 압축 기술 발표자료** 제작
- 3~5분 발표에 최적화된 시각적/논리적 구조 확립

## 2. 15-Page Blueprint (표준 목차 구성안)

| Page | Title / Topic | Core Message / Evidence Source | Status |
| :---: | :--- | :--- | :---: |
| **01** | **Engineering Identity** | 백엔드 설계부터 인프라/옵저버빌리티까지 연결하는 엔지니어 | `[DOCUMENTED]` |
| **02** | **Problem Definition & Goal** | 대규모 권한 관리 및 세션 무효화 제어의 한계 극복 | `[DOCUMENTED]` |
| **03** | **System Architecture** | Nginx 단일 진입점, Spring Boot, MySQL, Redis, 모니터링 토폴로지 | `[IMPLEMENTED]` |
| **04** | **Backend Architecture** | 레이어드 아키텍처, Record DTO, ApiResponse, Global Exception | `[IMPLEMENTED]` |
| **05** | **Authentication: JWT & Redis** | Stateless Access Token + HttpOnly RTR Refresh Token + Blacklist | `[VERIFIED]` |
| **06** | **Authorization: RBAC & Permission** | User-Role-Permission M:N 권한 모델 및 Security 인가 필터링 | `[VERIFIED]` |
| **07** | **Domain & DB Schema Migration** | Flyway V1~V5 기반 점진적 스키마 진화 및 정합성 보장 | `[IMPLEMENTED]` |
| **08** | **Infrastructure & Containerization** | Docker Compose 멀티 컨테이너 격리 및 Nginx Reverse Proxy 라우팅 | `[IMPLEMENTED]` |
| **09** | **CI/CD & Operational Flow** | 빌드 자동화 및 환경 분리, 운영 안정성 확보 | `[DOCUMENTED]` |
| **10** | **Testing & Security Verification** | 10종 이상의 단위/통합 보안 테스트 스위트 검증 | `[VERIFIED]` |
| **11** | **Performance & Observability** | k6 70 VU 실측 (Avg 5.64ms, P95 9.98ms, 0% Error), Prometheus/Grafana | `[VERIFIED]` |
| **12** | **Troubleshooting** | TS-01 Redis 장애 시 커맨드 타임아웃 단축(1분->2초) 및 방어 해결 | `[DOCUMENTED]` |
| **13** | **AI-Assisted Workflow** | SA-1 기반 프롬프트 규격화, Documentation-First, 정밀 검증 파이프라인 | `[DOCUMENTED]` |
| **14** | **Lessons Learned & Limitations** | 분산 환경에서의 트레이드오프 및 한계점 인식 | `[DOCUMENTED]` |
| **15** | **Engineering Roadmap** | N+1 쿼리 최적화 실측, 비동기 MQ 도입 등 계획 과제 | `[PLANNED]` |

## 3. Slide Production Guideline
각 슬라이드는 다음 형식을 갖춥니다:
```text
[Header] 슬라이드 번호 및 명확한 1개 핵심 테제
[Problem] 해결하고자 한 구체적 난제
[Decision & Implementation] 기술적 선택과 구현 근거
[Verification & Result] 실제 검증된 수치 및 산출물
[Source Reference] PR-Files 내 증거 파일 링크
```
