/**
 * Renderer Engine - Change Impact Analyzer & Manifest Engine
 * File: PR-1A1/renderer/impact_analyzer.js
 * Description: Calculates change levels, affected domains, evidences, and documents based on changed file paths
 */

const path = require('path');
const { loadRegistry } = require('./loader');

function analyzeChangeImpact(changedPaths, changeDescription = '') {
  const registry = loadRegistry();
  const relations = registry.relations;

  const affectedDomains = new Set();
  const affectedEvidences = new Set();
  const affectedDocuments = new Set();
  let maxChangeLevel = 'C0';

  const levelPriority = { 'C0': 0, 'C1': 1, 'C2': 2, 'C3': 3, 'C4': 4, 'C5': 5 };

  function upgradeLevel(newLevel) {
    if (levelPriority[newLevel] > levelPriority[maxChangeLevel]) {
      maxChangeLevel = newLevel;
    }
  }

  for (const p of changedPaths) {
    const normPath = p.replace(/\\/g, '/');

    // 1. CSS / Design System only → C0 (Cosmetic / Doc Only)
    //    CHANGE_POLICY C0: 오타 수정, 문장 보완, 마크다운 포맷팅, CSS Layout 미세 조정
    if (normPath.includes('design-system/') || normPath.endsWith('.css')) {
      upgradeLevel('C0');
      affectedDocuments.add('all-templates');
      continue;
    }

    // 2. Content YAML description edit → C0 (Cosmetic / Doc Only)
    //    CHANGE_POLICY C0: 기존 Claim 설명 보완은 Cosmetic으로 분류
    if (normPath.includes('content/domains/')) {
      upgradeLevel('C0');
      if (normPath.includes('auth')) {
        affectedDomains.add('DOM-AUTH');
        affectedDocuments.add('apms-auth');
      }
      continue;
    }

    // 3. Java Auth Implementation → C3 (Behavioral / Contract)
    //    CHANGE_POLICY C3: 인증/인가 흐름 및 규칙 변경, 에러 처리 정책 변경
    //    relations.yaml: backend/src/main/java/**/auth/** → C3
    if (normPath.includes('JwtAuthenticationFilter') || normPath.includes('TokenBlacklistService') || normPath.includes('RefreshTokenRepository') || normPath.match(/backend\/src\/main\/java\/.*\/auth\//)) {
      upgradeLevel('C3');
      affectedDomains.add('DOM-AUTH');
      affectedEvidences.add('ev-auth-jwt-filter');
      affectedEvidences.add('ev-auth-blacklist');
      affectedEvidences.add('ev-auth-rtr');
      affectedDocuments.add('apms-auth');
      affectedDocuments.add('apms-presentation');
      continue;
    }

    // 4. Performance Test / k6 → C1 (Evidence Addition)
    //    CHANGE_POLICY C1: 성능 결과에 새 측정 차수 추가, 실행 로그 스냅샷 추가
    //    relations.yaml: k6/** → C1
    if (normPath.includes('k6/') || normPath.includes('k6-load-test.md')) {
      upgradeLevel('C1');
      affectedDomains.add('DOM-PERF');
      affectedEvidences.add('ev-perf-70vu');
      affectedEvidences.add('ev-perf-50vu');
      affectedDocuments.add('apms-performance');
      affectedDocuments.add('apms-presentation');
      continue;
    }

    // 5. Source of Truth / Boundary → C5 (Source of Truth / Boundary)
    //    CHANGE_POLICY C5: 저장소 간 책임 재정의, Source of Truth 정책 변경
    if (normPath.includes('system/BOUNDARY.md') || normPath.includes('architecture/01_Architecture')) {
      upgradeLevel('C5');
      affectedDomains.add('DOM-AUTH');
      affectedDomains.add('DOM-INFRA');
      affectedEvidences.add('ev-infra-nginx');
      affectedEvidences.add('ev-ts-docker-redis');
      affectedDocuments.add('apms-infrastructure');
      affectedDocuments.add('apms-auth');
      affectedDocuments.add('apms-presentation');
      continue;
    }

    // 6. Infrastructure / Architecture → C4 (Architecture Change)
    //    CHANGE_POLICY C4: 컨테이너 토폴로지 변경, Nginx 리버스 프록시 구조 변경
    //    relations.yaml: docker-compose.yml → C4, nginx/** → C4
    if (normPath.includes('docker-compose.yml')) {
      upgradeLevel('C4');
      affectedDomains.add('DOM-INFRA');
      affectedEvidences.add('ev-infra-nginx');
      affectedEvidences.add('ev-ts-docker-redis');
      affectedDocuments.add('apms-infrastructure');
      affectedDocuments.add('apms-auth');
      affectedDocuments.add('apms-presentation');
      continue;
    }

    // Fallback: Documentation or minor file → C0 (Cosmetic)
    upgradeLevel('C0');
  }

  // Determine Required Actions (aligned with CHANGE_POLICY processing protocols)
  // C0: 전체 재검증 금지 → revalidate=false, rerender=false, markStale=false
  // C1: Evidence 항목 갱신, 관련 문서 확인 → rerender=true
  // C2~C5: STALE 전이, 재검증, 렌더링 필요
  const revalidateEvidence = ['C3', 'C4', 'C5'].includes(maxChangeLevel);
  const rerenderDocuments = ['C1', 'C2', 'C3', 'C4', 'C5'].includes(maxChangeLevel);
  const markStale = ['C2', 'C3', 'C4', 'C5'].includes(maxChangeLevel);

  return {
    change_level: maxChangeLevel,
    changed_paths: changedPaths,
    description: changeDescription,
    affected_domains: Array.from(affectedDomains),
    affected_evidences: Array.from(affectedEvidences),
    affected_documents: Array.from(affectedDocuments),
    required_actions: {
      mark_stale: markStale,
      revalidate_evidence: revalidateEvidence,
      rerender_html: rerenderDocuments
    }
  };
}

module.exports = {
  analyzeChangeImpact
};
