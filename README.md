# MLOps-1
---
## Copilot은 단순 자동완성보다 “지시형”으로 써야 훨씬 강력해진다.
```bash
// express 서버에서 JWT 인증 미들웨어 작성, 에러 처리 포함
```
---
## Copilot Chat 에서
```bash
위 코드 비동기 처리 문제 있는지 봐줘
```
---
## MCP 는 AI가 외부 도구/데이터에 접근하게 해주는 인터페이스
- OpenAPI 연결 → API 호출 코드 자동 생성
- DB schema 연결 → ORM 코드 생성
---
## 확장(extension) 조합 추천
- GitHub Copilot Chat
- Prettier
- ESLint
AI 강화
- Codeium (Copilot 대체/보조)
- Continue (LLM 연결형 코딩 도구)
---
## 워크플로우 예제
```bash
# 목표
- 로그인 API 구현
- JWT 사용
- refresh token 포함
```
- Chat으로 검증
```bash
보안 문제 있는지 체크해줘
```
- 테스트 코드 자동 생성
```bash
jest 테스트 만들어줘
```
- 리팩토링 요청
```bash
확장성 있게 구조 개선해줘
```

## 주의
- Copilot을 “자동완성”이 아니라 “지시 기반 생성기”로 쓰기
- Copilot Chat으로 계속 대화하면서 코드 다듬기
- MCP로 프로젝트 context 연결하기
