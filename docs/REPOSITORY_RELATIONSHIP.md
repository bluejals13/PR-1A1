# 3-Repository Relationship & Governance Blueprint

- **Version:** 2.0.0
- **Last Updated:** 2026-09-05
- **Status:** ACTIVE & ENFORCED

---

## 1. The Unified Engineering Narrative

3개의 Git 저장소는 독립된 파편이 아닌, 하나의 엔지니어링 스토리로 완결됩니다.

```text
26-05adf (BUILD)    SA-1 (PROCESS)    PR-1A1 (PROOF)
 실제 시스템 구현   ──► 어떻게 설계했는가 ──► 어떻게 검증했는가
```

---

## 2. 저장소별 데이터 흐름 및 상호작용

```text
[ 26-05adf ] (BUILD)
  ├── 런타임 코드베이스 (Spring Boot, Java 17, React, Nginx)
  ├── 15개 단위/통합 테스트 스위트
  └── k6 70 VU 실측 부하 테스트
         │
         ▼ (엔지니어링 의사결정 및 AI 라이프사이클)
[ SA-1 ] (PROCESS)
  ├── 8단계 AI 라이프사이클 거버넌스
  ├── 기술 도입 배경(Why) 및 트레이드오프 분석
  └── Phase 1 / Phase 2 엔지니어링 Changelog
         │
         ▼ (Commit SHA Pinned 불변 스냅샷 & 증거 가공)
[ PR-1A1 ] (PROOF)
  ├── 불변 증거 스냅샷 (manifests, snapshots, bundles)
  ├── 기계 판독형 Claim 레지스트리 (CLM-*)
  ├── 14~15개 기술 발표 슬라이드 (Jinja2 HTML Deck)
  └── 사실 기반 엔지니어링 Case Study
```

---

## 3. 원본 보존 및 동기화 수칙

1. `26-05adf`와 `SA-1`은 상위 Source of Truth로 기능하며, `PR-1A1`의 작업 중에는 원본을 임의 변경하지 않습니다.
2. 모든 검증 및 증거 추출은 고정된 Git Commit SHA(`26-05adf`: `9e6ef83d`, `SA-1`: `4a734a8e`)를 기준으로 수행됩니다.
3. 원본 저장소의 변경이 발생할 경우, `SOT-YYYY-MM-DD-XXX.json` 신규 매니페스트를 발행하여 버전별 정합성을 지속 보장합니다.
