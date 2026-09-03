# AI-Assisted Engineering Workflow (`PR-Files/ai-workflow`)

## 1. Purpose (목적)
`SA-1` 저장소를 단일 진실 공급원(Source of Truth)으로 삼아, 단순 코딩 보조에 머무르지 않고 **컨텍스트 분석, 정밀 계획, 에이전트 위임, 검증, 변경 기록이 통합된 통제된 AI 협업 엔지니어링 프로세스 및 거버넌스 규약**을 관리합니다.

## 2. Input / Source (원천 데이터)
- **SA-1 저장소 거버넌스 파일:**
  - `SA-1/README.md` (Zero-Chatter, Documentation First, Architecture Enforcement)
  - `SA-1/conventions/04_Agent_Commands.md` (표준 프롬프트 명령어 세트)
  - `SA-1/conventions/rules.md` (문서 작성 5대 원칙)
  - `SA-1/changelogs/` (Phase별 변경 로그 구조 및 작업 히스토리)

## 3. Output (산출물)
- **`AI_WORKFLOW_SPEC.md`**: AI 협업 엔지니어링 프로세스 및 거버넌스 기술 명세서 `[DOCUMENTED]` `[VERIFIED]`

## 4. Engineering Workflow Lifecycle (8단계 엔지니어링 라이프사이클)
```text
Requirement (요구사항 정의)
  └── Context Reading (규약 및 기존 코드 분석)
        └── Analysis & Planning (작업 분할 및 사전 검토)
              └── Agent Delegation (최소 단위 안전한 코드 수정)
                    └── Verification (JUnit / k6 검증)
                          └── Human Review (개발자 최종 승인)
                                └── Documentation (Changelog 및 규약 동기화)
```

## 5. What belongs here (포함되는 자료)
- SA-1 기반 AI 협업 8단계 라이프사이클 및 거버넌스 명세
- Zero-Chatter, Documentation-First 등 엔지니어링 원칙과 규약
- 표준 프롬프트 커맨드 세트 및 Changelog 기록 정책

## 6. What does NOT belong here (포함되지 않는 자료)
- 단순 일회성 AI 대화 로그나 구조화되지 않은 프롬프트 잡담
- 백엔드 비즈니스 로직 및 API 명세 (-> `specification/` 영역)
- 발표용 슬라이드 HTML / CSS / 디자인 요소 (-> `PRD-PO/` 영역)

## 7. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO/presentation/slides/001/`의 `AI Process Source (bluejals13/SA-1)` 카드와 `source/10_AI_WORKFLOW.md`는 본 디렉터리의 거버넌스 명세를 바탕으로 구성됩니다.
- `PR-Files`는 AI를 맹목적으로 믿지 않고 통제된 엔지니어링 도구로 활용한 증거와 규약을 기록하며, `PRD-PO`는 이를 AI 시대 엔지니어의 핵심 역량으로 제시합니다.
