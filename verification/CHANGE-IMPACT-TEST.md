# Change Impact Simulation & Boundary Revalidation Test Report

- **Document ID:** VERIF-CHANGE-IMPACT-01
- **Target Repository:** `PR-1A1`
- **Execution Date:** 2026-08-29
- **Protocol:** CHANGE_POLICY.md (C0 to C5 Levels)
- **Status:** ALL TESTS PASSED

---

## 1. Core Principles Verified

1. **Selective Revalidation:** 새 소스 커밋이나 변경이 발생해도 전체 Repository를 재검증하지 않고, 변경 경로 ➔ Domain ➔ Evidence ➔ Document 의존성 그래프를 추적하여 영향받는 범위만 재검증/재렌더링함.
2. **Separation of Concerns:** `Revalidation`(Evidence/Fact 유효성 재검사)과 `Rerender`(HTML 파일 재생성)를 독립된 의사결정으로 분리.
3. **No Phantom Evidence:** 기존 Claim의 단순 문장 수정(Case A)에는 새 Evidence를 만들지 않으며, 새로운 사실 추가(Case B)에 대해서만 Evidence를 등록하되 실측 근거가 없으면 `[PLANNED]`로 격리.

---

## 2. 4-Case Impact Test Execution Matrix

| Test ID | Simulated Change Scenario | Expected Level | Detected Level | Affected Domains | Affected Evidences | Affected Documents | Revalidate Evidence? | Rerender HTML? | Status |
|:---|:---|:---:|:---:|:---|:---|:---|:---:|:---:|:---:|
| **TEST-01** | `design-system/tokens/colors.css` 색상/토큰 하나 변경 | **C1** | **C1** | `None` | `None` | `all-templates` (스타일) | **NO** | **YES** | **PASS** |
| **TEST-02** | `content/domains/auth/apms-auth.yaml` 기존 Claim 문장 한 줄 수정 | **C2** | **C2** | `DOM-AUTH` | `None` (기존 유지) | `apms-auth` | **NO** | **YES** | **PASS** |
| **TEST-03** | `JwtAuthenticationFilter.java` 자바 백엔드 로직 수정 | **C4** | **C4** | `DOM-AUTH` | `ev-auth-jwt-filter`, `ev-auth-blacklist`, `ev-auth-rtr` | `apms-auth`, `apms-presentation` | **YES** | **YES** | **PASS** |
| **TEST-04** | `docker-compose.yml` 및 `system/BOUNDARY.md` 인프라 구조 변경 | **C5** | **C5** | `DOM-AUTH`, `DOM-INFRA` | `ev-infra-nginx`, `ev-ts-docker-redis` | `apms-infrastructure`, `apms-auth`, `apms-presentation` | **YES** | **YES** | **PASS** |

---

## 3. Test Case Analysis & Takeaways

### TEST-01 (C1: Presentation Change)
- **결과:** CSS 수정 시 소스 코드나 Evidence는 전혀 변경되지 않았으므로 Evidence Revalidation을 생략하고 렌더러만 호출하여 불필요한 빌드 시간을 최소화함.

### TEST-02 (C2: Content / Copy Change)
- **결과:** Claim 문장의 설명 보완 시 새 Evidence를 생성하지 않고 기존 `ev-auth-*` ID의 유효성만 확인한 후 `apms-auth` 관련 템플릿만 갱신.

### TEST-03 (C4: Implementation Change)
- **결과:** Java 소스 코드 변경 시 `relations.yaml`의 패스 패턴 매핑에 따라 `DOM-AUTH`를 감지하고, `ev-auth-jwt-filter`에 대한 JUnit 재실행 액션을 도출함. `DOM-RBAC`, `DOM-DATA` 등 무관한 도메인은 완벽히 보호됨.

### TEST-04 (C5: Structural / Architecture Change)
- **결과:** Docker 및 Boundary 변경 시 무조건 전체를 다시 쓰는 것이 아니라, `DOM-AUTH`와 `DOM-INFRA` 2개 영향 도메인과 `apms-infrastructure`, `apms-auth` 문서만을 타겟으로 계산하여 갱신 범위를 엄격히 제어함.

---

## 4. Conclusion

본 테스트를 통해 `PR-1A1` 시스템이 향후 `26-05adf`의 지속적인 개발 및 변경에 대해 **"EVERY CHANGE ➔ DETECT IMPACT ➔ UPDATE ONLY WHAT IS AFFECTED"** 원칙에 따라 안정적으로 동작함이 입증되었습니다.
