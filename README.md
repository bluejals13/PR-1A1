# 🛡️ PR-1A1: Engineering Evidence & Verification System (PROOF)

> **BUILD (26-05adf) ➔ PROCESS (SA-1) ➔ PROOF (PR-1A1)**  
> **"우리가 실제로 구현하고(BUILD), 체계적으로 설계했으며(PROCESS), 완벽하게 검증했음(PROOF)을 증명하는 엔지니어링 증거 시스템"**

본 저장소(`PR-1A1`)는 원본 애플리케이션 저장소(`26-05adf`)와 AI 엔지니어링 프로세스 저장소(`SA-1`)의 단일 진실 공급원(Source of Truth)을 고정된 Git Commit SHA 단위로 스냅샷하여, **결정론적 증거(Evidence), 엔지니어링 주장(Claim), 자동화 검증(Verification), 그리고 최종 포트폴리오 산출물(Presentation Deck / Case Study)**을 생산·관리하는 공식 증거 시스템(Engineering Evidence System)입니다.

---

## 1. 3-Repository Unified Engineering Architecture

```text
========================================================================================
[ 26-05adf ] BUILD (Source of Truth for Application Implementation)
  Git Commit: 9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f | Branch: feature/auth@0603@1401
  - 실제 구현 소스 (Spring Boot 3.3.2, Java 17, Gradle 8.14.4, JJWT 0.11.5, React 18)
  - 15개 단위/통합 JUnit 테스트 및 k6 70 VU 실측 부하 테스트 (Avg 5.64ms, Error 0.00%)
  - Nginx Port 80 단일 진입점 및 Docker Compose 컨테이너 인프라
=======================================│================================================
                                       │ (Engineering Decisions & Workflow)
                                       ▼
[ SA-1 ] PROCESS (Source of Truth for Engineering Process)
  Git Commit: 4a734a8edd8b670f8d29dc2a42a978ca3877a25f | Branch: main
  - 기술적 의사결정의 배경 (Why) 및 대안 비교 분석 (Phase 1 ~ Phase 2 Changelogs)
  - 8단계 AI 엔지니어링 라이프사이클 및 Zero-Chatter 거버넌스 규칙
  - 백엔드/프론트엔드 컨벤션 및 Grafana 대시보드 템플릿
=======================================│================================================
                                       │ (Commit SHA Pinned Snapshot & Fact Extraction)
                                       ▼
[ PR-1A1 ] PROOF (Source of Truth for Evidence, Verification & Presentation)
  Git Commit: c9f88722ad196ef7918240ab1faaaba4a8f64676 | Branch: main
  - 불변 스냅샷 (manifests, snapshots, bundles) 및 SHA-256 무결성 보존
  - 기계 판독형 Claim 레지스트리 (CLM-SEC-001 등 JSON Schema 기반)
  - 14~15개 기술 발표 슬라이드 (Jinja2 HTML Deck) 및 사실 기반 Case Study
  - 자동화 검증 엔진 (python automation/validate.py --all)
========================================================================================
```

---

## 2. Directory Structure & Responsibilities

```text
PR-1A1/
├── PR-Files/                             # [IMMUTABLE EVIDENCE & SPECIFICATION]
│   ├── evidence/                         # 불변 증거 영역 (수동 편집 절대 금지)
│   │   ├── SOURCE_OF_TRUTH_SNAPSHOT.md   # 통합 스냅샷 인덱스 및 매트릭스
│   │   ├── SOURCE_OF_TRUTH_SNAPSHOT.json # 기계 판독형 SOT 메타데이터
│   │   ├── schemas/                      # claim.schema.json, evidence.schema.json
│   │   ├── manifests/                    # SOT-2026-09-05-001.json (SHA-256 해시 매니페스트)
│   │   ├── snapshots/                    # 26-05adf, SA-1 핵심 소스 스냅샷 보관소
│   │   ├── claims/                       # CLM-*.json 정규화된 Claim 레지스트리
│   │   └── bundles/                      # EV-*/ 핵심 증거 번들 (소스, 테스트, 로그)
│   ├── architecture/                     # ARCHITECTURE_SPEC.md
│   ├── specification/                    # AUTH_AND_SECURITY_SPEC.md
│   ├── verification/                     # SECURITY_VERIFICATION_REPORT.md, DATA_LAYER_VERIFICATION.md
│   ├── performance/                      # K6_LOAD_TEST_REPORT.md
│   ├── troubleshooting/                  # TS-01-REDIS, TS-001-JWT, TS-003-DOCKER
│   └── ai-workflow/                      # AI_WORKFLOW_SPEC.md
│
├── PRD-PO/                               # [DERIVED PORTFOLIO & PRESENTATION]
│   ├── case-study/                       # 사실 기반 엔지니어링 문제해결 사례 (CASE_STUDY.md)
│   ├── html/                             # Web Portfolio & 16:9 Presentation (ppt.html, ppt.pptx)
│   │   └── 분리된 html/                  # Jinja2 자동화 렌더링된 슬라이드 HTML
│   └── presentation/                     # 웹 슬라이드 뷰어 및 소스 마크다운
│
├── work/                                 # [HUMAN EDITABLE] 인간 작업 및 검토 영역
│   ├── tasks/                            # 태스크 진행 상태
│   ├── reviews/                          # 코드/문서 리뷰 피드백
│   ├── decisions/                        # 수동 의사결정 기록
│   └── drafts/                           # 슬라이드/문서 초안
│
├── automation/                           # [VALIDATION & RENDERING AUTOMATION]
│   ├── validate.py                       # 원클릭 통합 검증 엔진 (Schema, Hash, Code Link)
│   ├── build.py                          # Jinja2 슬라이드 렌더러
│   ├── data/                             # 슬라이드별 JSON 데이터
│   ├── templates/                        # Jinja2 HTML 템플릿 (.html.j2)
│   └── tests/                            # 50개 자동화 회귀 테스트 스위트 (100% Pass)
│
├── docs/                                 # 거버넌스, 정책 및 감사 보고서
│   ├── REPOSITORY_AUDIT_REPORT.md        # 리팩토링 사전 감사 보고서
│   ├── REPOSITORY_REFACTORING_REPORT.md  # 리팩토링 완료 최종 보고서
│   ├── PIPELINE_CONSOLIDATION_REPORT.md  # 파이프라인 분석 및 통합 보고서
│   ├── EVIDENCE_ARCHITECTURE.md          # 증거 아키텍처 규격
│   ├── SOURCE_OF_TRUTH_POLICY.md         # 단일 진실 공급원 정책
│   ├── CLAIM_POLICY.md                   # 클레임 작성 및 승격 규약
│   ├── TRACEABILITY.md                   # 엔드-투-엔드 추적성 매트릭스
│   ├── MANUAL_WORKFLOW.md                # 작업자 매뉴얼 가이드
│   ├── VERIFICATION_POLICY.md            # 5대 검증 상태 판정 기준
│   └── REPOSITORY_RELATIONSHIP.md        # 3개 저장소 간 관계 정의
│
├── AGENTS.md                             # AI 에이전트 거버넌스 및 Zero-Hallucination 규칙
└── README.md                             # [본 파일]
```

---

## 3. 원클릭 자동화 검증 (Deterministic Verification)

AI 환각이나 수동 문서 오차 없이, 모든 주장(Claim), 스냅샷 파일(SHA-256), 실제 JUnit 테스트 메서드의 존재 여부를 100% 결정론적으로 자동 검증합니다:

```bash
# 전체 증거 시스템 무결성 검증 (Schema, Hash, Code Symbol, Slide Data)
py automation/validate.py --all

# 슬라이드 렌더링 회귀 테스트 (50개 테스트 100% Pass)
py -m unittest discover -s automation/tests
```

---

## 4. 5대 검증 상태 체계 (Verification Protocol)

- **`[VERIFIED]`**: JUnit 테스트 및 k6 부하 테스트 실측 결과가 완비된 항목
- **`[IMPLEMENTED]`**: 실제 구현 코드가 존재하나 검증 수치가 없는 항목
- **`[DOCUMENTED]`**: 공식 기술 문서 및 SA-1 의사결정 기록에 명시된 항목
- **`[PARTIAL]`**: 구현은 되었으나 실시간 표출/검증이 부분적인 항목 (Grafana 등)
- **`[PLANNED]`**: 향후 로드맵으로 계획된 항목 (JPA 쿼리 벤치마크, Kafka 도입 등)
