# AI-Assisted Engineering Workflow (`PR-Files/ai-workflow`)

## 1. Responsibility
본 디렉터리는 `SA-1`을 단일 진실 공급원으로 삼아, 단순 코딩 보조가 아닌 **컨텍스트 분석, 정밀 계획, 에이전트 위임, 검증, 변경 기록이 통합된 AI 협업 엔지니어링 프로세스**를 문서화합니다.

## 2. Source of Truth Mapping
- **Source Files:**
  - `SA-1/README.md` (Zero-Chatter, Documentation First, Architecture Enforcement)
  - `SA-1/conventions/04_Agent_Commands.md` (표준 프롬프트 명령어 세트)
  - `SA-1/conventions/rules.md` (문서 작성 5대 원칙)
  - `SA-1/changelogs/` (Phase별 변경 로그 구조)

## 3. Engineering Workflow Lifecycle
```text
Requirement (요구사항 정의)
  └── Context Reading (규약 및 기존 코드 분석)
        └── Analysis & Planning (작업 분할 및 사전 검토)
              └── Agent Delegation (최소 단위 안전한 코드 수정)
                    └── Verification (JUnit / k6 검증)
                          └── Human Review (개발자 최종 승인)
                                └── Documentation (Changelog 및 규약 동기화)
```

## 4. Key Rules
- **Zero-Chatter Policy:** 불필요한 서론/사과 제거, diff 중심 간결한 변경 제공
- **Documentation-First Policy:** 코드 수정 완료 시 `changelogs/` 내 마크다운 로그 의무 작성
- **Standard Commands:** Task&Log, Code Review, Docs Sync, Troubleshooting 표준 커맨드 체계
