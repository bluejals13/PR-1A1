# Source of Truth Policy & Governance

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED

---

## 1. 단일 진실 공급원 (Single Source of Truth) 원칙

3개 저장소는 각기 고유한 영역의 Source of Truth(SOT)로 동작하며, 상호 침범하지 않습니다.

```text
26-05adf = Application Source of Truth (BUILD)
SA-1      = Engineering Process Source of Truth (PROCESS)
PR-1A1    = Evidence, Verification & Presentation Source of Truth (PROOF)
```

---

## 2. 저장소별 권한과 책임

### 2.1 `26-05adf` (BUILD)
- **책임:** 실행 가능한 애플리케이션 코드, 설정, 인프라, 테스트 코드의 단일 원본.
- **불변 원칙:** `PR-1A1`이나 `SA-1`의 작업으로 인해 `26-05adf`의 코드를 임의로 수정할 수 없습니다.
- **버전 고정:** `PR-1A1`은 브랜치명이 아닌 고정된 Git Commit SHA(`9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f`)를 기준으로 사실관계를 검증합니다.

### 2.2 `SA-1` (PROCESS)
- **책임:** 시스템 설계 의도(Why), 기술 도입 대안 비교, Phase별 변경 내역, AI 에이전트 협업 거버넌스 규칙의 단일 원본.
- **불변 원칙:** `26-05adf`의 코드가 변경되었을 때, 그 배경 설명과 트레이드오프는 `SA-1`에 기록됩니다.

### 2.3 `PR-1A1` (PROOF)
- **책임:** 앞선 두 저장소의 사실관계를 증명하는 증거(Evidence), 주장(Claim), 검증(Verification), 발표자료(Presentation), 포트폴리오(HTML)의 단일 원본.
- **불변 원칙:** `PR-1A1`은 원본 저장소를 대체하지 않으며, Snapshot과 Manifest를 통해 기준 시점의 증거를 보존합니다.

---

## 3. 위반 시 처리 규정 (Conflict Resolution)
1. 문서 내용과 실제 코드가 충돌할 경우, 항상 **`26-05adf`의 실제 코드가 우선**합니다.
2. 실제 코드에 없는 기능은 문서에 적혀 있더라도 `[UNKNOWN]` 또는 `[PLANNED]`로 강등되며, 절대 `[IMPLEMENTED]`나 `[VERIFIED]`로 표기할 수 없습니다.
