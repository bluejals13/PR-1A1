# PR-1A1: Portfolio & Technical Documentation Processing Repository

본 저장소(`PR-1A1`)는 원본 애플리케이션 저장소(`26-05adf`)와 AI 개발 프로세스 저장소(`SA-1`)의 단일 진실 공급원(Source of Truth)을 기반으로, **포트폴리오(발표자료/웹) 및 기술/검증 명세 문서를 가공·생산하는 저장소**입니다.

---

## 1. Source of Truth Architecture

```text
[ Source 1: Application Repository ]
  https://github.com/bluejals13/26-05adf (Branch: feature/auth@0603@1401)
  - 실제 코드 (Spring Boot 3.3, Java 17, React, MySQL, Redis, Nginx)
  - 실제 설정 / Flyway 스키마 / Docker Compose
  - JUnit 단위·통합 보안 테스트 / k6 부하 테스트 스크립트 및 결과

[ Source 2: AI & Process Repository ]
  https://github.com/bluejals13/SA-1 (Branch: main)
  - AI-Assisted Engineering Workflow 및 프롬프트 규약
  - 문서화 5대 원칙 및 Phase별 Changelog

                   ▼ (Fact Extraction & Traceability)

[ Target: PR-1A1 (Current Repository) ]
  ├── PRD-PO/    (발표자료 / 웹 포트폴리오 / 케이스 스터디 가공 공간)
  └── PR-Files/  (엔지니어링 명세 / 검증 / 성능 팩트 / 장애 분석 보관 공간)
```

---

## 2. Directory Structure & Responsibilities

```
PR-1A1/
├── PRD-PO/                               # Public-Facing Portfolio & Presentation
│   ├── presentation/                     # 12~15페이지 기술 발표자료 슬라이드 및 원고
│   ├── html/                             # Fact 기반 Web Portfolio
│   ├── case-study/                       # 핵심 엔지니어링 문제해결 사례 (8단계 구조)
│   └── README.md
│
├── PR-Files/                             # Technical Specification & Evidence
│   ├── evidence/                         # 사실관계 스냅샷 및 Traceability Matrix
│   ├── architecture/                     # 시스템 및 네트워크 토폴로지 명세
│   ├── specification/                    # JWT/Redis, RBAC, API, DB 스키마 명세
│   ├── verification/                     # 테스트 스위트 및 보안 검증 명세
│   ├── performance/                      # k6 70 VU 실측치 및 성능 분석 보고서
│   ├── troubleshooting/                  # TS 6단계 표준 장애 분석 및 해결 내역
│   ├── ai-workflow/                      # SA-1 기반 AI 협업 엔지니어링 프로세스
│   └── README.md
│
├── AGENTS.md                             # Agent 작업 원칙 및 Zero-Hallucination 가이드라인
├── .cursorrules                          # IDE 코딩 및 문서화 컨벤션
└── README.md                             # 저장소 메인 인덱스
```

---

## 3. Strict Documentation Rules (Zero-Hallucination)
1. **Fact First:** `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`에 검증된 사실만을 기록합니다.
2. **State Tagging:** 모든 기술 항목에 `[IMPLEMENTED]`, `[VERIFIED]`, `[DOCUMENTED]`, `[PLANNED]`, `[UNKNOWN]` 태그를 표기합니다.
3. **8-Step Case Study Flow:** `Problem → Context → Decision → Implementation → Verification → Result → Limitation → Next Step`
4. **6-Step Troubleshooting Flow:** `Symptom → Impact → Diagnosis → Root Cause → Resolution → Prevention`
