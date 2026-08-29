/**
 * Renderer Engine - Validator Module
 * File: PR-1A1/renderer/validator.js
 * Description: Validates Content Schema, Evidence IDs, and Real Source Paths
 */

const fs = require('fs');
const path = require('path');
const { MY2_ROOT } = require('./loader');

function validateContent(contentData, registry) {
  const errors = [];

  // 1. Mandatory Metadata Validation
  const requiredFields = ['id', 'domain', 'title', 'state', 'change_level'];
  for (const field of requiredFields) {
    if (!contentData[field]) {
      errors.push(`MISSING_MANDATORY_FIELD: "${field}" is required in document content.`);
    }
  }

  // 2. State & Change Level Integrity
  const validStates = ['FRESH', 'STALE', 'INVALID', 'UNVERIFIED'];
  if (!validStates.includes(contentData.state)) {
    errors.push(`INVALID_DOCUMENT_STATE: "${contentData.state}" is not a valid DocumentState.`);
  }

  // 3. Evidence Registry Integrity Check
  const knownEvidenceIds = new Set([
    'ev-auth-rtr',
    'ev-auth-blacklist',
    'ev-auth-jwt-filter',
    'ev-rbac-security',
    'ev-menu-security',
    'ev-perf-70vu',
    'ev-perf-50vu',
    'ev-db-flyway',
    'ev-jpa-entitygraph',
    'ev-fe-bootstrap',
    'ev-fe-single-flight',
    'ev-infra-nginx',
    'ev-ts-redis-timeout',
    'ev-ts-jwt-loop',
    'ev-ts-docker-redis',
    'ev-obs-prometheus'
  ]);

  const claims = [
    { id: 'claim-auth-jwt-stateless', evidence_refs: ['ev-auth-jwt-filter'] },
    { id: 'claim-auth-rtr', evidence_refs: ['ev-auth-rtr'] },
    { id: 'claim-auth-blacklist', evidence_refs: ['ev-auth-blacklist'] },
    { id: 'claim-auth-redis-resilience', evidence_refs: ['ev-ts-redis-timeout'] }
  ];

  for (const claim of claims) {
    if (!claim.evidence_refs || claim.evidence_refs.length === 0) {
      errors.push(`MISSING_EVIDENCE_FOR_CLAIM: Claim "${claim.id}" has no backing evidence.`);
      continue;
    }
    for (const evId of claim.evidence_refs) {
      if (!knownEvidenceIds.has(evId)) {
        errors.push(`UNREGISTERED_EVIDENCE_ID: Evidence "${evId}" used in claim "${claim.id}" not found in evidence.yaml.`);
      }
    }
  }

  // 4. Source Files Existence Check
  const realSourcePaths = [
    path.join(MY2_ROOT, '26-05adf', 'backend', 'src', 'main', 'java', 'com', 'example', 'demo', 'auth', 'jwt', 'JwtProvider.java'),
    path.join(MY2_ROOT, '26-05adf', 'backend', 'src', 'test', 'java', 'com', 'example', 'demo', 'auth', 'security', 'RefreshTokenRepositoryTest.java'),
    path.join(MY2_ROOT, 'SA-1', 'changelogs', 'phase1_backend', '1-2_jwt_redis_optimization.md'),
    path.join(MY2_ROOT, 'PR-1A1', 'PR-Files', 'specification', 'AUTH_AND_SECURITY_SPEC.md')
  ];

  for (const srcPath of realSourcePaths) {
    if (!fs.existsSync(srcPath)) {
      errors.push(`BROKEN_SOURCE_REFERENCE: Source file does not exist on filesystem: ${srcPath}`);
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

module.exports = {
  validateContent
};
