# Agent Standard Operating Procedure (SOP) & Project Context

## 1. Project Identity & Positioning
- **Identity:** Java/Spring 기반 백엔드를 구축하고, 컨테이너/인프라/운영 환경(Nginx, CI/CD, Observability)까지 연결하여 이해하는 엔지니어의 포트폴리오 공간.
- **Track Separation:**
  - Track A (Foundation): Java, Maven, IoC/DI 컨테이너 직접 구현(`MySpringFW`)을 통한 프레임워크 원리 학습.
  - Track B (Advanced): `26-05adf`, `SA-1` 기반 Spring Boot, Security, Redis(Token Rotation), Docker, k6 부하 테스트 실무.

## 2. Strict Guardrails (Zero-Hallucination)
포트폴리오 문서 및 시스템 검증 시 다음 **팩트 데이터만** 사용하며, 임의로 수치를 창조하지 않는다.
- **Performance Metrics (k6):** 70 VUs, 1 min, Avg Response 5.64ms, P95 9.98ms, Throughput 463 req/s, Error Rate 0%
- **Security Features:** JWT Access/Refresh Token, Redis TTL, Refresh Token Rotation, JTI Blacklist, RBAC(User-Role-Permission)
- **Infra Features:** Docker Compose, Nginx Reverse Proxy, Prometheus + Grafana + cAdvisor
- **Unverified/Planned (구현되지 않음 - Roadmap 표기):** N+1 해결, EXPLAIN 쿼리 최적화, Message Queue

## 3. AI-Assisted Engineering Workflow
에이전트는 요구사항을 수신하면 다음 순서로만 작업한다:
1. **ANALYZE:** 관련 Repository Context 및 기존 코드를 읽고 영향도 분석.
2. **PLAN:** 수정/작성할 파일 목록과 예상 결과를 개발자에게 제시 후 승인 대기.
3. **IMPLEMENT:** 승인된 범위 내에서만 최소한의 안전한 코드 변경.
4. **VERIFY:** 단위 테스트(JUnit) 및 부하 테스트(k6) 결과를 통해 기능 및 무결성 검증.
5. **DOCUMENT:** 검증 완료 후 Git Commit 메시지 작성 및 TS(Troubleshooting) 문서 업데이트.

## 4. Documentation Standard (Troubleshooting)
모든 장애 해결 문서(TS)는 다음 6단계 구조를 엄격히 따른다.
1. Symptom (현상)
2. Impact (영향 범위)
3. Diagnosis (진단 과정 및 로그 확인)
4. Root Cause (근본 원인)
5. Resolution (해결 방법 - 실제 코드/설정 변경 내역)
6. Prevention (재발 방지 대책)
- 주요 장애 기록: TS-001 (JWT Refresh 무한 루프), TS-003 (Docker 내 Redis localhost 바인딩 문제)