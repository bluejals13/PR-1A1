# PR-Files: Technical Documentation & Evidence Repository

## 1. Overview & Responsibility
`PR-Files/`는 **단일 진실 공급원(Source of Truth)**인 `26-05adf` (Branch: `feature/auth@0603@1401`) 및 `SA-1`의 실제 코드, 설정, 테스트, 로그로부터 도출된 **기술 명세(Specification), 검증 명세(Verification), 성능 지표(Performance), 트러블슈팅(Troubleshooting), 증거(Evidence)**를 체계적으로 관리하는 공간입니다.

이 폴더의 모든 문서는 **대외 공개/발표용 요약이 아닌, 엔지니어링 수준의 사실적 증거와 구현 세부사항**을 다룹니다.

---

## 2. Directory Structure & Responsibilities

```
PR-Files/
├── evidence/              # 사실관계 스냅샷 및 Claim-to-Evidence 추적성 매트릭스
│   ├── SOURCE_OF_TRUTH_SNAPSHOT.md
│   └── README.md
├── architecture/          # 시스템 전체, 백엔드, 인프라, 보안 토폴로지 명세
│   └── README.md
├── specification/         # API 규격, JWT/Redis 세션 정책, RBAC 권한 매트릭스, DB 스키마
│   └── README.md
├── verification/          # 단위/통합/보안 테스트 검증 결과 및 테스트 스위트 매핑
│   └── README.md
├── performance/           # k6 부하 테스트 시나리오, 실측 수치, 모니터링 메트릭 분석
│   └── README.md
├── troubleshooting/       # TS 표준 6단계 기반 장애 분석 및 해결 보고서
│   └── README.md
└── ai-workflow/           # SA-1 기반 AI-Assisted Engineering Workflow 및 커맨드 규격
    └── README.md
```

---

## 3. Core Principles
1. **Zero-Hallucination:** 가공되거나 임의로 창작된 수치/기능을 일체 기록하지 않음.
2. **Traceability:** 모든 주장은 소스 파일명, 라인, 테스트 케이스, 로그 출력 결과와 직접 연결됨.
3. **State Tagging:** 모든 기술 항목에 `[IMPLEMENTED]`, `[VERIFIED]`, `[DOCUMENTED]`, `[PLANNED]`, `[UNKNOWN]` 태그 명시.
4. **Standard 6-Step TS:** 장애 문서는 반드시 `Symptom -> Impact -> Diagnosis -> Root Cause -> Resolution -> Prevention` 준수.
