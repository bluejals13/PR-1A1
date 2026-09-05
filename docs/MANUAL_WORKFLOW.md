# Manual Workflow & Operator Guide

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED

---

## 1. 개요

본 가이드는 사람이 직접 포트폴리오를 수정, 보완, 검토할 때 **불변 증거(Immutable Evidence)를 오염시키지 않고 안전하게 작업하는 표준 절차**를 정의합니다.

---

## 2. 작업 공간 분리 원칙

1. **절대 수정 금지 구역 (`PR-Files/evidence/`):**
   - `snapshots/`, `manifests/`, `bundles/`, `claims/`는 수동 편집이 금지됩니다.
   - 오직 `automation/` 스크립트를 통해서만 생성/갱신됩니다.
2. **자유 편집 허용 구역 (`work/`):**
   - `work/tasks/`: 개인 할 일 및 엔지니어링 계획
   - `work/reviews/`: AI 또는 피어 리뷰 피드백 기록
   - `work/decisions/`: 의사결정 메모 및 초안
   - `work/drafts/`: 포트폴리오 및 발표자료 작성 초안

---

## 3. 신규 Claim 추가 워크플로우

1. `26-05adf`에서 실제 코드 구현 및 테스트 작성 완료.
2. `work/drafts/`에 신규 Claim 초안 작성.
3. `automation/build_claims_and_bundles.py`에 Claim 및 Evidence 정보 등록.
4. 검증 실행:
   ```bash
   py PR-1A1/automation/validate.py --all
   ```
5. 검증 통과 시 `PR-Files/evidence/claims/`에 정식 승격 및 Git Commit.
