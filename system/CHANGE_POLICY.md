# Change Impact & Document Revalidation Policy

- **Document ID:** APMS-SR-SYS-CHANGE-01
- **Target Repository:** `PR-1A1`
- **Created Date:** 2026-08-29
- **Status:** ACTIVE
- **Core Principle:** "EVERY CHANGE ➔ DETECT IMPACT ➔ UPDATE ONLY WHAT IS AFFECTED" (전체 재빌드 금지, 영향도 기반 선택적 갱신)

---

## 1. Overview & Core Philosophy

새로운 개발 Phase, 기능, 커밋, Changelog가 발생할 때 전체 문서를 무조건 처음부터 다시 작성하거나 전체 Repository를 재검증하지 않습니다.
반드시 **변경 영향도(Change Impact Level: C0 ~ C5)**를 먼저 판정하고, **Registry의 의존성 관계(Dependency Graph)**를 추적하여 영향받는 단위(Domain, Evidence, Document)만 선택적으로 재검증 및 갱신합니다.

```text
[ New Commit / Changelog / Source Change ]
                   │
                   ▼
       [ 1. Determine Change Level (C0 ~ C5) ]
                   │
                   ▼
       [ 2. Identify Changed Source Path ]
                   │
                   ▼
       [ 3. Traverse Registry Relations ]
         ├── Affected Domains
         ├── Affected Evidences
         └── Affected Documents
                   │
                   ▼
       [ 4. Mark State: STALE ] (Only Affected Items)
                   │
                   ▼
       [ 5. Selective Revalidation & Lint ]
                   │
                   ▼
       [ 6. Transition State: FRESH / INVALID / UNVERIFIED ]
                   │
                   ▼
       [ 7. Selective Re-rendering (HTML) ]
```

---

## 2. Change Impact Levels (C0 ~ C5)

| Level | Classification | Example Scenarios | Processing Protocol |
|:---:|:---|:---|:---|
| **C0** | **Cosmetic / Doc Only** | • 오타 수정, 문장 보완<br>• 마크다운 포맷팅<br>• CSS Layout 미세 조정 | • Changelog 확인<br>• 영향 문서만 단순 확인<br>• **전체 재검증 금지** |
| **C1** | **Evidence Addition** | • 기존 기능에 새 단위/통합 테스트 추가<br>• 성능 결과에 새 측정 차수 추가<br>• 실행 로그 스냅샷 추가 | • 해당 Evidence 항목 갱신 (`evidence.yaml`)<br>• 해당 Document 상태 확인<br>• 관련 문서/EVIDENCE 템플릿만 검증 |
| **C2** | **Internal Implementation** | • Service/Repository 리팩토링<br>• 내부 알고리즘 최적화<br>• 쿼리 튜닝 (외부 계약 불변) | • 해당 Domain 식별<br>• 해당 Source & Evidence 확인<br>• 관련 FEATURE / TECHNICAL 검증<br>• 실제 변경점 발생 시에만 SLIDE / LONGFORM 갱신 |
| **C3** | **Behavioral / Contract** | • JWT Expiration 시간 변경<br>• API Response 필드/포맷 변경<br>• 인증/인가 흐름 및 규칙 변경<br>• 에러 처리 정책 변경 | • `Affected Domain` ➔ `Architecture` ➔ `Evidence` ➔ `SA-1 Knowledge` ➔ `FEATURE` ➔ `TECHNICAL` ➔ `SLIDE` ➔ `LONGFORM 관련 Section` 순서로 정밀 영향도 검사 |
| **C4** | **Architecture Change** | • Redis 캐싱/세션 구조 변경<br>• Nginx 리버스 프록시 구조 변경<br>• MySQL 스키마/마이그레이션 변경<br>• 컨테이너 토폴로지 변경 | • Architecture Dependency Graph 탐색<br>• 영향을 받는 모든 Domain/Evidence/Knowledge 식별<br>• 영향 문서 전체 재검증 |
| **C5** | **Source of Truth / Boundary** | • 3개 저장소 간 책임 재정의<br>• 핵심 데이터/인증 모델 전면 개편<br>• Source of Truth 정책 변경 | • 26-05adf ↔ SA-1 ↔ PR-1A1 전체 관계 재검증<br>• Registry 관계 기반 영향 범위 계산 후 재동기화 |

---

## 3. Document Lifecycle States

모든 Document, Feature, Technical Spec은 다음 4가지 상태 중 하나를 가집니다.

```text
┌─────────┐      Source Change Detected       ┌─────────┐
│  FRESH  │ ────────────────────────────────► │  STALE  │
└─────────┘                                   └────┬────┘
     ▲                                             │ Revalidation
     │                                             ▼
     │ Verified OK                  ┌──────────────────────────────┐
     └───────────────────────────── │ Verification Decision        │
                                    └──────┬────────────────┬──────┘
                                           │                │
                          Conflict with    │                │ Missing
                          Source of Truth  ▼                ▼ Evidence
                                    ┌───────────┐      ┌────────────┐
                                    │  INVALID  │      │ UNVERIFIED │
                                    └───────────┘      └────────────┘
```

- **`FRESH`:** 현재 Source of Truth 및 Evidence와 완벽히 일치하고 검증이 통과된 최신 상태.
- **`STALE`:** 연결된 Source 또는 Knowledge가 변경되어 재검증 및 diff 검토가 필요한 상태.
- **`INVALID`:** 실제 소스 코드나 런타임 결과와 내용이 명백히 충돌하거나 모순되는 상태.
- **`UNVERIFIED`:** 주장(Claim)에 대한 실제 코드/테스트/로그 근거가 결여되어 검증할 수 없는 상태.

---

## 4. Strict Governance Rules (절대 금지 및 의무 사항)

### 4.1 절대 금지 사항 (Prohibitions)
1. ❌ 새 Changelog가 추가되었다는 이유만으로 전체 Portfolio / HTML을 일괄 재생성하지 않는다.
2. ❌ 새로운 Phase가 시작되었다는 이유만으로 변경되지 않은 모든 Document를 재검증하지 않는다.
3. ❌ 변경된 파일과 무관한 Domain까지 탐색하여 문서를 수정하지 않는다.
4. ❌ 변경되지 않은 Evidence를 삭제하거나 임의로 재생성하지 않는다.
5. ❌ 소스 코드와 불일치하는 내용을 추측하여 임의로 FRESH 상태로 만들지 않는다.

### 4.2 필수 수행 절차 (Mandatory Protocol)
1. ⭕ 변경된 Source 파일의 경로를 정확히 파악한다.
2. ⭕ `relations.yaml`을 통해 해당 Source와 연결된 Domain을 식별한다.
3. ⭕ 해당 Domain과 매핑된 Evidence 항목을 식별한다.
4. ⭕ 해당 Evidence 및 Domain을 참조하는 Document만 `STALE` 상태로 전이한다.
5. ⭕ `STALE` 상태로 지정된 Document에 대해서만 선별적 재검증(Selective Revalidation)을 수행한다.
6. ⭕ 검증 결과에 따라 `FRESH`, `INVALID`, `UNVERIFIED`로 상태를 갱신한다.
7. ⭕ 최종적으로 검증이 완료된 Document에 대해서만 Renderer를 호출하여 HTML을 갱신한다.

---

## 5. Template-Specific Re-rendering Trigger Matrix

| Template Type | Re-rendering Trigger Condition (갱신 조건) | Non-Trigger Condition (비갱신 조건) |
|:---|:---|:---|
| **FEATURE** | 해당 기능의 실제 동작, 소스 로직, 예외 처리, 검증 테스트가 변경되었을 때 | 관련 없는 타 도메인 변경, 단순 오타 수정 |
| **TECHNICAL** | 아키텍처 구조, 기술 의사결정(Why), Trade-off, 벤치마크 수치가 변경되었을 때 | 내부 단순 주석 변경, UI 레이아웃 미세 조정 |
| **EVIDENCE** | 실제 테스트 클래스, 부하 테스트 실측 수치, 실행 로그가 변경되었을 때 | 문서 설명 문구 수정 |
| **SLIDE** | 발표용 핵심 메시지, 아키텍처 다이어그램, 최종 검증 수치 팩트가 변경되었을 때 | 내부 세부 메서드 리팩토링, 세부 변수명 변경 |
| **LONGFORM** | 프로젝트 전체 맥락, 문제 해결 엔지니어링 스토리, 시스템 종합 결과가 변경되었을 때 | 개별 기능의 사소한 내부 구현 변경 |

---

*본 문서는 APMS.SR 문서 시스템의 지속 가능한 유지보수를 위한 핵심 운영 정책이며, Registry 및 Validation 파이프라인의 알고리즘 기준으로 동작합니다.*
