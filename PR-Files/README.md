# PR-Files: Technical Documentation & Evidence Repository

## 1. Overview & Positioning (위치 및 역할)

`PR-Files/`는 **단일 진실 공급원(Source of Truth)**인 `26-05adf` (Branch: `feature/auth@0603@1401`) 및 `SA-1`의 실제 코드, 설정, 테스트, 로그로부터 추출된 **엔지니어링 사실(Fact), 기술 명세(Specification), 검증 증거(Evidence), 성능 실측치(Performance), 장애 분석(Troubleshooting)**을 체계적으로 보관하는 기술 증거 저장소입니다.

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. 26-05adf & SA-1 (Source of Truth)                       │
│    - 실제 백엔드 소스 코드, 설정 파일, JUnit 테스트, k6 스크립트 │
└──────────────────────────────┬──────────────────────────────┘
                               │ (Fact Extraction & Traceability)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. PR-Files (Engineering Evidence & Technical Truth)        │
│    - 사실과 근거 (무엇이 검증되었고 구현되었는가)                  │
│    - 아키텍처 토폴로지, 보안/API 명세, 실측 성능 데이터, TS 보고서│
└──────────────────────────────┬──────────────────────────────┘
                               │ (Fact-Based Content Production)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. PRD-PO (Public-Facing Output & Presentation)             │
│    - 표현 결과물 (사람/평가자가 한눈에 이해할 수 있는 발표/포트폴리오) │
│    - presentation/ (독립 슬라이드), html/ (웹 포트폴리오), case-study/│
└─────────────────────────────────────────────────────────────┘
```

> **핵심 원칙:**
> - `PR-Files` = 사실과 근거 (Source of Truth 기반 기술 명세 및 검증 증거)
> - `PRD-PO` = 그것을 사람이 이해할 수 있도록 효과적으로 표현하는 발표/웹 산출물

---

## 2. Directory Structure & Subdomain Responsibilities

```text
PR-Files/
├── README.md                      # [본 문서] PR-Files 거버넌스 및 디렉터리 안내
│
├── evidence/                      # 사실관계 스냅샷 및 Claim-to-Evidence 추적성 매트릭스
│   ├── SOURCE_OF_TRUTH_SNAPSHOT.md
│   └── README.md
│
├── architecture/                  # 시스템 네트워크 토폴로지 및 컨테이너 격리 명세
│   ├── ARCHITECTURE_SPEC.md
│   └── README.md
│
├── specification/                 # 인증/인가, JWT/Redis 세션, RBAC, DB 스키마 상세 기술 명세
│   ├── AUTH_AND_SECURITY_SPEC.md
│   └── README.md
│
├── verification/                  # 보안 테스트 스위트, 단위/통합 테스트, 데이터 계층 무결성 검증
│   ├── DATA_LAYER_VERIFICATION.md
│   ├── SECURITY_VERIFICATION_REPORT.md
│   └── README.md
│
├── performance/                   # k6 70 VU 부하 테스트 실측치 및 성능 분석 보고서
│   ├── K6_LOAD_TEST_REPORT.md
│   └── README.md
│
├── troubleshooting/               # TS 표준 6단계 프레임워크 기반 실측 장애 3건 원인 및 해결
│   ├── TS-01-REDIS_TIMEOUT.md
│   ├── TS-001_JWT_REFRESH_LOOP.md
│   ├── TS-003_DOCKER_REDIS_BINDING.md
│   └── README.md
│
└── ai-workflow/                   # SA-1 기반 AI 협업 엔지니어링 프로세스 및 작업 규약
    ├── AI_WORKFLOW_SPEC.md
    └── README.md
```

---

## 3. Core Principles & Zero-Hallucination Policy

1. **Zero-Hallucination (무환각 원칙):** 가공되거나 임의로 창작된 수치/기능을 일체 기록하지 않으며, 소스 코드/로그로 증명된 사실만 기록합니다.
2. **Traceability (추적성):** 모든 엔지니어링 주장은 실제 파일 경로, 라인 번호, 테스트 스위트와 직접 매핑됩니다.
3. **5-State Tagging (상태 명시):** 모든 기술 항목에 `[IMPLEMENTED]`, `[VERIFIED]`, `[DOCUMENTED]`, `[PLANNED]`, `[UNKNOWN]` 태그를 표기합니다.
4. **Standard 6-Step TS (장애 표준화):** 장애 보고서는 반드시 `Symptom → Impact → Diagnosis → Root Cause → Resolution → Prevention` 6단계를 엄수합니다.
