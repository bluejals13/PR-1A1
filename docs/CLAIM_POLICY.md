# Engineering Claim Policy & Schema Governance

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED

---

## 1. Claim 정의 및 원칙

**Claim(엔지니어링 주장)**이란 포트폴리오, 발표자료, 이력서에 기술되는 모든 정량적·기술적 명제를 의미합니다.

### 3대 절대 원칙:
1. **No Code, No Claim:** `26-05adf`에 구현되지 않은 기능은 절대 Claim으로 등록할 수 없다.
2. **Deterministic Validation:** 모든 Claim은 자동화 검증 스크립트(`validate.py`)에 의해 실제 파일과 심볼이 확인되어야 한다.
3. **Single Identity:** 각 Claim은 정규화된 ID 체계(`CLM-DOMAIN-XXX`)를 준수해야 한다.

---

## 2. Claim ID 명명 규칙

```text
CLM-[DOMAIN]-[NUMBER:03d]
```

- `CLM-SEC-XXX`: 보안, 인증(JWT), 세션 관리, 토큰 로테이션(RTR), 블랙리스트
- `CLM-RBAC-XXX`: 사용자-역할-권한 M:N 인가 모델, 엔드포인트 보안
- `CLM-PERF-XXX`: k6 부하 테스트, Throughput, Latency, Error Rate
- `CLM-INFRA-XXX`: Nginx 리버스 프록시, Docker Compose, 네트워크 격리
- `CLM-DATA-XXX`: MySQL 스키마, Flyway 마이그레이션, JPA EntityGraph
- `CLM-OBS-XXX`: Prometheus, Actuator, VictoriaMetrics, Grafana
- `CLM-TS-XXX`: 트러블슈팅, 타임아웃 격리, 무한 루프 차단
- `CLM-AI-XXX`: AI 라이프사이클 협업 거버넌스, Zero-Chatter

---

## 3. Claim 생명주기 및 승격 규칙

```text
[ DRAFT ] ➔ [ IMPLEMENTED ] ➔ [ VERIFIED ]
    │                │
    ▼                ▼
[ PLANNED ]     [ REJECTED / INVALID ]
```

- **VERIFIED 승격 조건:**
  - 실제 테스트 파일 존재 (`test_file`)
  - 실제 실행 가능한 테스트 메서드 존재 (`test_methods`)
  - 실측 결과 지표 기록 완료 (`metrics`)
- **IMPLEMENTED 기준:**
  - 실제 코드 파일 및 심볼 존재 확인
- **DOCUMENTED 기준:**
  - 공식 기술 문서 또는 SA-1 의사결정 기록 존재 확인
- **PLANNED 격리:**
  - 구현 계획만 존재하거나 실측 지표가 없는 항목
