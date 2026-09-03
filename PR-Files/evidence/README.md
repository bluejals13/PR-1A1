# Evidence & Traceability (`PR-Files/evidence`)

## 1. Purpose (목적)
무엇이 실제 사실(Fact)이고 무엇이 검증되었는지를 증명하는 최상위 단일 진실 스냅샷과 주장-증거 추적성 매트릭스(Traceability Matrix)를 관리합니다.

## 2. Input / Source (원천 데이터)
- `26-05adf` 애플리케이션 전체 소스 코드, 설정 파일, Git 커밋 이력
- `SA-1` 엔지니어링 프로세스 및 변경 관리 로그

## 3. Output (산출물)
- **`SOURCE_OF_TRUTH_SNAPSHOT.md`**: 구현, 검증, 문서화 상태의 기준 스냅샷 및 팩트 베이스

## 4. What belongs here (포함되는 자료)
- 소스 코드와 테스트 결과에서 직접 도출된 사실 스냅샷
- 각 기능의 5대 상태 분류 (`[VERIFIED]`, `[IMPLEMENTED]`, `[DOCUMENTED]`, `[PLANNED]`, `[UNKNOWN]`)
- 주장(Claim)과 실제 파일 경로를 연결하는 추적성 매트릭스

## 5. What does NOT belong here (포함되지 않는 자료)
- 발표용 슬라이드 HTML / CSS / 디자인 요소
- 정량적 근거가 없는 추상적인 설명 문구
- 검증되지 않은 가상의 기능이나 수치

## 6. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO`의 모든 슬라이드, 웹 포트폴리오, 케이스 스터디는 반드시 본 디렉터리의 `SOURCE_OF_TRUTH_SNAPSHOT.md`에 등록된 사실만을 인용하여 작성됩니다.
- 본 디렉터리에 등록되지 않은 내용은 `PRD-PO`에서 사실로 표현할 수 없습니다.
