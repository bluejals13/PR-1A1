# Verification Policy & Status Protocol

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED

---

## 1. 5대 상태 분류 (Status Classification)

모든 엔지니어링 주장 및 포트폴리오 기술 항목은 아래 5대 상태 중 정확히 하나를 가져야 합니다.

| 상태 태그 | 판정 기준 | 허용 근거 |
| :--- | :--- | :--- |
| `[VERIFIED]` | 실제 자동화 테스트 또는 부하 측정 결과로 통과가 증명된 상태 | JUnit 테스트 메서드 통과 확인, k6 실측치 리포트 존재 |
| `[IMPLEMENTED]` | 코드가 실제로 작성되어 리포지토리에 존재하나 정량 검증 수치가 없는 상태 | 소스 코드 파일 및 메서드 존재 확인 |
| `[DOCUMENTED]` | 아키텍처, 설계 규격, 컨벤션, 장애 보고서 등 공식 기술 문서에 명시된 상태 | 공식 마크다운 문서 및 Changelog 확인 |
| `[PARTIAL]` | 구현 및 연동은 되었으나, 실시간성 또는 대시보드 검증이 부분적인 상태 | Grafana 대시보드 등 과장 금지 항목 |
| `[PLANNED]` | 향후 개선 예정으로 계획된 상태 (Roadmap) | task_progress.md 미완료 항목 또는 향후 로드맵 |

---

## 2. 엄격한 불일치 방지 규칙 (Zero-Hallucination)

```text
DOCUMENTED != IMPLEMENTED
IMPLEMENTED != VERIFIED
```

1. 문서에 기술되어 있다는 이유만으로 `[IMPLEMENTED]`나 `[VERIFIED]`로 승격할 수 없습니다.
2. 코드가 구현되어 있다는 이유만으로 테스트 결과 없이 `[VERIFIED]`로 승격할 수 없습니다.
3. 실측되지 않은 지표(예: JPA N+1 최적화 전후 쿼리 수 비교, Message Queue 도입)는 반드시 `[PLANNED]`로 표기하여 과장을 방지합니다.
