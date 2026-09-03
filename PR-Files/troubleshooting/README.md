# Troubleshooting & Incident Analysis (`PR-Files/troubleshooting`)

## 1. Purpose (목적)
시스템 개발, 컨테이너화, 운영 검증 중 실제로 발생한 장애(Incident), 무한 루프, 포트/바인딩 충돌, 타임아웃 등의 문제를 표준 6단계 프레임워크에 맞춰 체계적으로 진단·분석하고 재발 방지책을 관리합니다.

## 2. Input / Source (원천 데이터)
- `26-05adf/docs/troubleshooting/01-redis-failure.md` (Redis 장애 시 타임아웃 및 서킷 대응)
- `26-05adf/AGENTS.md` (TS-001 JWT 루프, TS-003 Docker Redis 바인딩 이슈)
- `SA-1/changelogs/` (장애 조치 커밋 로그 및 패치 이력)

## 3. Output (산출물)
- **`TS-01-REDIS_TIMEOUT.md`**: Redis 장애 시 커맨드 타임아웃 및 세션/인증 장애 대응 보고서 `[VERIFIED]` `[DOCUMENTED]`
- **`TS-001_JWT_REFRESH_LOOP.md`**: 만료된 Refresh Token 요청 시 무한 재발급 루프 차단 보고서 `[DOCUMENTED]`
- **`TS-003_DOCKER_REDIS_BINDING.md`**: Docker 컨테이너 격리 환경 내 `localhost` 바인딩 거부 해결 보고서 `[DOCUMENTED]`

## 4. 6-Step Standard Documentation Rule (장애 분석 6대 표준)
모든 트러블슈팅 문서는 다음 6단계를 엄격히 따릅니다:
1. **Symptom (현상):** 장애의 외적 징후 및 오류 증상
2. **Impact (영향 범위):** 비즈니스/사용자 영향도 수준 (Critical, High, Medium, Low)
3. **Diagnosis (진단 및 재현):** 탐지 방법, 재현 절차, 서버 에러 로그
4. **Root Cause (근본 원인):** 코드, 설정, 인프라 상의 기술적 원인 규명
5. **Resolution (해결 방법):** 실제 코드/설정 변경 내역 및 패치 내용
6. **Prevention (재발 방지 대책):** 모니터링 알람, 타임아웃 방어, 테스트 케이스 추가

## 5. What belongs here (포함되는 자료)
- 표준 6단계 프레임워크를 엄격히 준수한 실측 장애 분석 보고서
- 장애 발생 당시의 실제 에러 로그, 스택 트레이스, 재현 커맨드
- 문제 해결을 위해 적용된 소스 코드 / 설정 변경 Diff 및 단위 테스트

## 6. What does NOT belong here (포함되지 않는 자료)
- 원인이나 해결책이 입증되지 않은 단순 추측성 메모
- 일반적인 프로그래밍 기초 튜토리얼이나 외부 라이브러리 공식 문서 복사
- 발표용 슬라이드 HTML / CSS / 디자인 요소 (-> `PRD-PO/` 영역)

## 7. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO/presentation/slides/002/`의 컨테이너 격리 딜레마, `PRD-PO/presentation/source/09_TROUBLESHOOTING.md`의 장애 사례 3건은 본 디렉터리의 실제 장애 분석 보고서(TS-01, TS-001, TS-003)를 바탕으로 구술 및 시각화됩니다.
- `PR-Files`는 장애의 기술적 진실(Raw Facts & Logs)을 증명하고, `PRD-PO`는 문제 해결 역량을 드러내는 포트폴리오 스토리로 전환합니다.
