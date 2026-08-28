# Troubleshooting & Incident Analysis (`PR-Files/troubleshooting`)

## 1. Responsibility
본 디렉터리는 시스템 개발 및 운영 중 발생한 장애, 병목 현상, 예외 상황에 대한 체계적인 원인 분석 및 재발 방지 기록을 다룹니다.

## 2. 6-Step Standard Documentation Rule
모든 트러블슈팅 문서는 다음 6단계를 엄격히 따릅니다:
1. **Symptom (현상):** 장애의 외적 징후 및 오류 증상
2. **Impact (영향 범위):** 비즈니스/사용자 영향도 수준 (Critical, High, Medium, Low)
3. **Diagnosis (진단 및 재현):** 탐지 방법, 재현 절차, 서버 에러 로그
4. **Root Cause (근본 원인):** 코드, 설정, 인프라 상의 기술적 원인 규명
5. **Resolution (해결 방법):** 실제 코드/설정 변경 내역 및 패치 내용
6. **Prevention (재발 방지 대책):** 모니터링 알람, 타임아웃 방어, 테스트 케이스 추가

## 3. Verified Incident Registry
- **[TS-01-REDIS] Redis 장애 시 커맨드 타임아웃 및 세션/인증 장애 대응**
  - Source: `26-05adf/docs/troubleshooting/01-redis-failure.md`
  - Status: `[VERIFIED]` `[DOCUMENTED]`
- **[TS-001] JWT Refresh 무한 루프 이슈** (AGENTS.md 등록)
  - Status: `[DOCUMENTED]`
- **[TS-003] Docker 환경 내 Redis localhost 바인딩 문제** (AGENTS.md 등록)
  - Status: `[DOCUMENTED]`
