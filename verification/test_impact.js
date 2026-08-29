/**
 * Change Impact Simulation & Verification Test Suite
 * File: PR-1A1/verification/test_impact.js
 * Description: Runs 6 Change Impact Test Cases and validates expected vs actual results
 * Canonical Source: system/CHANGE_POLICY.md (C0~C5 Level Definitions)
 */

const { analyzeChangeImpact } = require('../renderer/impact_analyzer');

const testCases = [
  {
    // CHANGE_POLICY C0: Cosmetic / Doc Only (CSS Layout 미세 조정)
    id: "TEST-01",
    name: "CSS 색상/토큰 하나 변경",
    changed_paths: ["design-system/tokens/colors.css"],
    expected: {
      level: "C0",
      revalidate_evidence: false,
      rerender_html: false,
      affected_domains_count: 0
    }
  },
  {
    // CHANGE_POLICY C0: Cosmetic / Doc Only (기존 Claim 설명 보완)
    id: "TEST-02",
    name: "DOM-AUTH Content에 기존 Claim 설명 한 줄 수정",
    changed_paths: ["content/domains/auth/apms-auth.yaml"],
    expected: {
      level: "C0",
      revalidate_evidence: false,
      rerender_html: false,
      affected_documents: ["apms-auth"]
    }
  },
  {
    // CHANGE_POLICY C3: Behavioral / Contract (인증/인가 흐름 및 규칙 변경)
    id: "TEST-03",
    name: "JwtAuthenticationFilter.java 코드 변경",
    changed_paths: ["backend/src/main/java/com/example/demo/auth/security/JwtAuthenticationFilter.java"],
    expected: {
      level: "C3",
      revalidate_evidence: true,
      rerender_html: true,
      affected_domains: ["DOM-AUTH"],
      affected_evidences: ["ev-auth-jwt-filter"]
    }
  },
  {
    // CHANGE_POLICY C4: Architecture Change (컨테이너 토폴로지 변경)
    id: "TEST-04a",
    name: "docker-compose.yml 컨테이너 토폴로지 변경",
    changed_paths: ["docker-compose.yml"],
    expected: {
      level: "C4",
      revalidate_evidence: true,
      rerender_html: true,
      affected_domains: ["DOM-INFRA"],
      affected_documents: ["apms-infrastructure"]
    }
  },
  {
    // CHANGE_POLICY C5: Source of Truth / Boundary (저장소 간 책임 재정의)
    id: "TEST-04b",
    name: "인증 및 컨테이너 아키텍처 구조 변경 (Boundary 포함)",
    changed_paths: ["docker-compose.yml", "system/BOUNDARY.md"],
    expected: {
      level: "C5",
      revalidate_evidence: true,
      rerender_html: true,
      affected_domains: ["DOM-AUTH", "DOM-INFRA"],
      affected_documents: ["apms-infrastructure", "apms-auth"]
    }
  },
  {
    // CHANGE_POLICY C1: Evidence Addition (성능 결과에 새 측정 차수 추가)
    id: "TEST-05",
    name: "k6 부하 테스트 새 측정 차수 추가",
    changed_paths: ["k6/load_test_v7.js"],
    expected: {
      level: "C1",
      revalidate_evidence: false,
      rerender_html: true,
      affected_domains: ["DOM-PERF"],
      affected_evidences: ["ev-perf-70vu"]
    }
  }
];


console.log("======================================================");
console.log("🧪 [CHANGE IMPACT SIMULATION TEST SUITE]");
console.log("======================================================\n");

let allPassed = true;

for (const tc of testCases) {
  console.log(`[Running ${tc.id}] ${tc.name}`);
  const res = analyzeChangeImpact(tc.changed_paths, tc.name);

  const levelMatch = res.change_level === tc.expected.level;
  const revalMatch = res.required_actions.revalidate_evidence === tc.expected.revalidate_evidence;
  const rerenderMatch = res.required_actions.rerender_html === tc.expected.rerender_html;

  const passed = levelMatch && revalMatch && rerenderMatch;
  if (!passed) allPassed = false;

  console.log(`  - Detected Level: ${res.change_level} (Expected: ${tc.expected.level}) -> ${levelMatch ? 'PASS' : 'FAIL'}`);
  console.log(`  - Affected Domains: [${res.affected_domains.join(', ')}]`);
  console.log(`  - Affected Evidences: [${res.affected_evidences.join(', ')}]`);
  console.log(`  - Affected Documents: [${res.affected_documents.join(', ')}]`);
  console.log(`  - Actions: MarkStale=${res.required_actions.mark_stale}, Revalidate=${res.required_actions.revalidate_evidence}, Rerender=${res.required_actions.rerender_html}`);
  console.log(`  => RESULT: ${passed ? '✅ PASS' : '❌ FAIL'}\n`);
}

console.log("======================================================");
console.log(`Summary: ${allPassed ? '🎉 ALL 6 TEST CASES PASSED' : '❌ SOME TEST CASES FAILED'}`);
console.log("======================================================");

process.exit(allPassed ? 0 : 1);
