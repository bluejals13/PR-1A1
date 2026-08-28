# 10. AI-Assisted Engineering Workflow

## What
AI 에이전트를 맹목적으로 신뢰하는 것이 아니라, 개발자의 완벽한 통제 하에 아키텍처 컨벤션 준수, 정밀 계획, 코드 수정 위임, 엄격한 테스트 검증, 문서 동기화를 수행하는 AI 협업 엔지니어링 프로세스.

## Why
- 무분별한 AI 코딩 도구 사용으로 인한 환각(Hallucination), 컨텍스트 오염, 아키텍처 훼손을 방지.
- AI를 단순 코드 생성기가 아닌, 정밀하게 통제된 개발 생산성 파이프라인의 구성 요소로 활용하기 위함.

## How
- **Zero-Chatter Policy:** 불필요한 미사여구나 서론을 배제하고 `diff` 및 실행 결과 중심 정밀 협업.
- **Documentation-First Policy:** 코드 수정 전 `task_progress.md`에 계획을 정의하고, 작업 완료 후 `changelogs/`에 동기화 의무화.
- **8-Stage Controlled Lifecycle:**
  `Requirement ➔ Context Reading ➔ Planning ➔ Agent Delegation ➔ Verification (JUnit/k6) ➔ Human Review ➔ Documentation ➔ Deployment`
- **표준 Agent 커맨드 세트:**
  - `@Task&Log`: 작업 진행 상황 점검 및 계획 동기화
  - `@CodeReview`: Spring Security 및 컨벤션 정적 분석
  - `@DocsSync`: 코드 변경 사항 기술 문서 역반영
  - `@Troubleshoot`: 장애 발생 시 6단계 TS 표준 양식 작성

## Evidence
- `PR-Files/ai-workflow/AI_WORKFLOW_SPEC.md`
- `SA-1/README.md`
- `SA-1/conventions/rules.md`
- `SA-1/conventions/04_Agent_Commands.md`
- `SA-1/changelogs/`

## Result
- AI가 작성한 모든 코드는 JUnit 자동화 테스트 100% 통과 및 k6 부하 검증을 거쳐 `[VERIFIED]` 상태로 승격 `[VERIFIED]`
- 변경 이력 및 추적성(Traceability) 100% 동기화 달성 `[DOCUMENTED]`

## Status
`[DOCUMENTED]` `[VERIFIED]`

## Source
- `SA-1` (`main`)
- `PR-Files/ai-workflow/AI_WORKFLOW_SPEC.md`

## Presentation Use
- **Slide 12:** Controlled AI Workflow (SA-1 Governance & 8-Stage Lifecycle)
- **Slide 15:** Engineering Identity (통제된 AI 엔지니어링 역량)
