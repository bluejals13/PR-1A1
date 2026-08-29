# Repository Boundary & Governance Specification

- **Document ID:** APMS-SR-SYS-BOUNDARY-01
- **Target Repository:** `PR-1A1`
- **Created Date:** 2026-08-29
- **Phase:** PHASE 2 — Source / Knowledge / Presentation Boundary Definition
- **Status:** ACTIVE

---

## 1. 3-Repository Boundary Overview

본 시스템은 `my2/` 하위의 3개 저장소가 단일 프로젝트로 병합되거나 코드가 복제되지 않고, 역할에 따라 엄격히 분리되어 동작하도록 설계되었습니다.

```text
┌────────────────────────────────────────────────────────┐
│               26-05adf (Source of Truth)               │
│  - Actual Code (Java 17, Spring Boot 3.3, React, Vite) │
│  - Configuration (docker-compose, Nginx, DB, Redis)    │
│  - Tests (JUnit 5, MockMvc, SpringBootTest)            │
│  - Real Benchmarks & Runtime Evidence (k6, logs)       │
└───────────────────────────┬────────────────────────────┘
                            │
                   Implementation Facts
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               SA-1 (Knowledge Layer)                   │
│  - Architecture & Design Decisions                     │
│  - Why & Trade-offs (Changelogs with rationale)        │
│  - Engineering Conventions & Agent Workflows           │
│  - PKM & Infrastructure Knowledge                      │
└───────────────────────────┬────────────────────────────┘
                            │
             Structured Knowledge & Context
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│               PR-1A1 (Presentation Layer)              │
│  - Document Registry (documents.yaml, relations.yaml)  │
│  - Evidence Registry (evidence.yaml)                   │
│  - Template System (LONGFORM, SLIDE, FEATURE, TECH)    │
│  - Unified Design System & HTML Renderer               │
│  - Claim-to-Evidence Traceability Verification         │
└────────────────────────────────────────────────────────┘
```

---

## 2. Detailed Repository Responsibilities & Rules

### 2.1 26-05adf (Implementation Source of Truth)

- **역할:** 실제 동작하는 애플리케이션 코드 및 런타임 인프라 저장소
- **책임:**
  - 백엔드 구현 (Spring Boot 3.3, Spring Security, JPA, Flyway, JJWT, Lettuce)
  - 프론트엔드 구현 (React, TypeScript, Zustand, React Query, Vite)
  - 인프라 및 네트워크 설정 (`docker-compose.yml`, `nginx/default.conf`, `monitoring/`)
  - 자동화 테스트 및 부하 테스트 코드 (`backend/src/test/`, `k6/scenarios/`)
  - 런타임 실측 결과 보고서 (`docs/performance/k6-load-test.md`)
  - 로컬 작업 추적 (`task_progress.md`, `AGENTS.md`, `.cursorrules`)
- **금지 사항:**
  - 포트폴리오용 가공 문서/HTML을 이 저장소에 직접 생성하지 않음.
  - 검증되지 않은 코드를 완료 상태로 `task_progress.md`에 기록하지 않음.

### 2.2 SA-1 (Technical Knowledge Layer)

- **역할:** 기술 의사결정, 아키텍처 배경, 엔지니어링 지식(Why/Trade-off) 관리 저장소
- **책임:**
  - 변경 이력에 대한 엔지니어링 배경 기록 (`changelogs/phase*`)
  - 아키텍처 원칙 및 설계 근거 (`architecture/`)
  - AI 에이전트 협업 및 코드/문서화 컨벤션 (`conventions/`)
  - 인프라 지식 및 모니터링 대시보드 템플릿 (`pkm&infra/`)
- **금지 사항:**
  - 26-05adf의 실제 구현 코드 전체를 복사하여 보관하지 않음.
  - 26-05adf에 존재하지 않는 허위 구현이나 미검증 기술을 기정사실화하여 작성하지 않음.
  - `README.md`에 `.cursorrules` 단순 복사본을 방치하지 않고 저장소의 역할과 인덱스를 유지함.

### 2.3 PR-1A1 (Presentation & Portfolio Layer)

- **역할:** 검증된 팩트와 엔지니어링 지식을 사람이 읽을 수 있는 문서/웹/발표자료로 렌더링하고 무결성을 검증하는 저장소
- **책임:**
  - 엔지니어링 단위 기반 **Document Registry** (`registry/documents.yaml`)
  - 근거 추적 기반 **Evidence Registry** (`registry/evidence.yaml`)
  - 관계 정의 매트릭스 (`registry/relations.yaml`)
  - 포트폴리오 콘텐츠 모델 및 템플릿 시스템 (`templates/`)
  - 통합 디자인 시스템 (`design-system/`)
  - 템플릿 기반 HTML 렌더러 (`renderer/`)
  - 링크/팩트/경계 검증기 (`validation/`)
- **금지 사항:**
  - 26-05adf의 소스 코드를 PR-1A1 내부에 복사하여 독자적인 Source of Truth를 만들지 않음 (항상 원본 참조).
  - Evidence가 없는 주장을 `[VERIFIED]` 상태로 표시하거나 과장된 표현(SLA 보장 등)을 사용하지 않음.
  - 슬라이드 내용을 단순히 세로로 늘려 롱폼으로 만들거나, 롱폼 문장을 그대로 쪼개어 슬라이드로 만들지 않음 (Template 역할 분리 준수).

---

## 3. Source of Truth & Precedence Protocol

내용을 생성하거나 사실관계를 판단할 때의 우선순위는 다음과 같습니다:

```text
Priority 1: 26-05adf의 실제 코드, 실제 테스트, 실제 런타임 설정, 실제 실행 결과
Priority 2: 26-05adf의 실제 Evidence 파일 (k6 리포트, Flyway SQL, 테스트 클래스)
Priority 3: 26-05adf의 기술 문서 (docs/)
Priority 4: SA-1의 Architecture / Changelogs / Conventions / PKM
Priority 5: 26-05adf 및 SA-1의 README.md
Priority 6: PR-1A1의 기존 PPT 및 레거시 HTML (단순 Reference로만 취급)
```

---

## 4. Cross-Repository Duplication & Synchronization Policy

### 4.1 `26-05adf/docs/` vs `SA-1/architecture/`, `conventions/` 중복 처리
- **원칙:** 26-05adf의 `docs/`는 **실제 개발 및 로컬 실행을 위한 가이드**이며, SA-1의 문서는 **전체 시스템 관점의 아키텍처 지식 및 결정 이력**입니다.
- **정본(Source of Truth):** 실행 설정 및 포트 매핑의 실측 정본은 `26-05adf`입니다.
- **참조 규칙:** PR-1A1은 구현 및 포트 실측 팩트는 `26-05adf`를 직접 참조하고, 해당 구조를 도입한 이유(Why)와 대안 비교(Trade-off)는 `SA-1`의 changelog를 참조합니다.

### 4.2 Code Duplication Prohibition (코드 복제 금지)
- PR-1A1은 코드 스니펫을 인용할 때 파일 전체를 복제하지 않고, 필요 최소한의 핵심 로직 블록과 함께 `file:///` 또는 GitHub 상대 경로 링크를 명시합니다.

---

## 5. Traceability & Change Propagation Flow

원본의 변경 사항은 다음 흐름에 따라 검증 및 렌더링됩니다:

```text
[26-05adf 코드/테스트/설정 변경]
               │
               ▼
[SA-1 Changelog 및 의사결정 기록]
               │
               ▼
[PR-1A1 Registry 갱신 (documents.yaml, evidence.yaml)]
               │
               ▼
[PR-1A1 Validator 실행 (Link / Content / Boundary)]
               │
               ▼
[PR-1A1 Renderer 재실행 → HTML 산출물 생성]
```

---

*본 문서는 3개 저장소 간의 책임과 데이터 흐름의 기준점이며, 향후 Registry 구축 및 Template 렌더링 시 절대적 규칙으로 적용됩니다.*
