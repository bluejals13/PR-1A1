# Evidence Architecture Specification

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED
- **Target Repository:** `PR-1A1` (PROOF Layer)

---

## 1. Architectural Philosophy

APMS.SR 증거 아키텍처(Evidence Architecture)는 소프트웨어 엔지니어링 포트폴리오의 신뢰성을 수학적·결정론적(deterministic)으로 보장하기 위한 시스템입니다.

단순히 "이러한 코드가 있다"는 진술이나 가공된 문서 스니펫을 인용하는 대신,
**`SOURCE ➔ SNAPSHOT ➔ EVIDENCE BUNDLE ➔ CLAIM ➔ VERIFICATION ➔ PORTFOLIO`**
의 단방향 불변 체인을 강제합니다.

```text
26-05adf (BUILD)    SA-1 (PROCESS)
       │                  │
       └─────────┬────────┘
                 │ (Commit SHA Pinned Extraction)
                 ▼
       [ Immutable Snapshots ]
                 │
                 ▼
       [ Evidence Bundles ]
                 │
                 ▼
       [ Claim Registry ]
                 │
                 ▼
       [ Verification Engine ]
                 │
                 ▼
       [ Presentation & Portfolio ]
```

---

## 2. 핵심 레이어 구성

### 2.1 Immutable Snapshots (`PR-Files/evidence/snapshots/`)
- 원본 저장소(`26-05adf`, `SA-1`)의 특정 커밋 시점 소스 파일을 불변으로 보존합니다.
- 사람이 직접 수정할 수 없으며, 모든 파일은 SHA-256 해시로 매니페스트에 고정됩니다.

### 2.2 Manifests (`PR-Files/evidence/manifests/`)
- 특정 감사/릴리즈 시점의 모든 스냅샷 파일의 SHA-256 해시, 크기, 원본 커밋 SHA를 JSON으로 기록합니다.
- 예: `SOT-2026-09-05-001.json`

### 2.3 Evidence Bundles (`PR-Files/evidence/bundles/`)
- 개별 핵심 주장(Claim)을 증명하는 최소 단위 번들입니다.
- 디렉터리 구성:
  - `manifest.json`: 번들 메타데이터 및 검증 상태
  - `source/`: 원본 구현체 스냅샷
  - `documentation/`: 관련 설계 및 아키텍처 문서
  - `test/`: 증명 테스트 소스 코드
  - `result/`: 실제 실행 로그 및 결과 지표

### 2.4 Claim Registry (`PR-Files/evidence/claims/`)
- JSON Schema(`claim.schema.json`)로 검증되는 구조화된 엔지니어링 주장 파일들입니다.
- 각 Claim은 유일한 ID(`CLM-DOMAIN-XXX`)를 가집니다.

---

## 3. 물리적 작업 영역 분리 (Immutability vs Human Work)

```text
PR-Files/evidence/
├── snapshots/      <-- [IMMUTABLE] 사람이 절대 직접 수정 금지
├── manifests/      <-- [IMMUTABLE] 감사 시점에만 자동 생성
├── bundles/        <-- [IMMUTABLE] 증거 파일 불변 보존
└── claims/         <-- [IMMUTABLE] 검증 통과된 클레임 레지스트리

work/
├── tasks/          <-- [HUMAN EDITABLE] 개발/감사 태스크 추적
├── reviews/        <-- [HUMAN EDITABLE] 코드 및 아키텍처 리뷰 피드백
├── decisions/      <-- [HUMAN EDITABLE] 사람의 의사결정 메모
└── drafts/         <-- [HUMAN EDITABLE] 발표 및 문서 작성 초안
```
