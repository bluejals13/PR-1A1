import json
import pathlib
import datetime

base_root = pathlib.Path("C:/Users/bluej/Desktop/my2")
repo_pr1 = base_root / "PR-1A1"
evidence_base = repo_pr1 / "PR-Files" / "evidence"

commit_26 = "9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f"
commit_sa1 = "4a734a8edd8b670f8d29dc2a42a978ca3877a25f"
now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

# 1. Schemas
schemas_dir = evidence_base / "schemas"
schemas_dir.mkdir(parents=True, exist_ok=True)

claim_schema = {
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Engineering Claim Schema",
  "type": "object",
  "required": ["claim_id", "claim", "domain", "sources", "evidence", "verification", "status"],
  "properties": {
    "claim_id": { "type": "string", "pattern": "^CLM-[A-Z]+-[0-9]{3}$" },
    "claim": { "type": "string" },
    "domain": { "type": "string" },
    "status": { "type": "string", "enum": ["VERIFIED", "IMPLEMENTED", "DOCUMENTED", "PARTIAL", "PLANNED", "UNKNOWN"] },
    "sources": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["repository", "path"],
        "properties": {
          "repository": { "type": "string" },
          "branch": { "type": "string" },
          "commit": { "type": "string" },
          "path": { "type": "string" },
          "symbol": { "type": "string" }
        }
      }
    },
    "evidence": {
      "type": "object",
      "required": ["evidence_id", "type"],
      "properties": {
        "evidence_id": { "type": "string" },
        "bundle_path": { "type": "string" },
        "type": { "type": "string" }
      }
    },
    "verification": {
      "type": "object",
      "required": ["method", "status"],
      "properties": {
        "method": { "type": "string" },
        "test_file": { "type": "string" },
        "test_methods": { "type": "array", "items": { "type": "string" } },
        "status": { "type": "string" },
        "metrics": { "type": "object" }
      }
    },
    "portfolio_mapping": {
      "type": "object",
      "properties": {
        "case_study": { "type": "string" },
        "slides": { "type": "array", "items": { "type": "string" } },
        "presentation_source": { "type": "string" }
      }
    }
  }
}

schemas_dir.joinpath("claim.schema.json").write_text(json.dumps(claim_schema, indent=2, ensure_ascii=False), encoding="utf-8")

# 2. Claims Definitions
claims_data = [
  {
    "claim_id": "CLM-SEC-001",
    "claim": "Stateless JWT Access Token (1시간 유효기간) 서명 검증 및 Bearer Header 파싱을 통해 API 접근을 제어한다.",
    "domain": "SECURITY",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/auth/jwt/JwtProvider.java",
        "symbol": "JwtProvider"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/auth/security/JwtAuthenticationFilter.java",
        "symbol": "JwtAuthenticationFilter.doFilterInternal"
      }
    ],
    "evidence": {
      "evidence_id": "EV-SEC-001",
      "bundle_path": "PR-Files/evidence/bundles/EV-SEC-001",
      "type": "TEST_AND_SOURCE"
    },
    "verification": {
      "method": "JUnit5 Mockito & Spring Security Test",
      "test_file": "backend/src/test/java/com/example/demo/auth/security/JwtAuthenticationFilterTest.java",
      "test_methods": [
        "validAccessTokenSetsSecurityContext",
        "nonAccessTokenReturnsUnauthorized",
        "blacklistedTokenReturnsUnauthorized",
        "redisUnavailableReturns503"
      ],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 3.1)",
      "slides": ["004", "005", "006"],
      "presentation_source": "04_AUTH_AND_RBAC.md"
    }
  },
  {
    "claim_id": "CLM-SEC-002",
    "claim": "Refresh Token Rotation (RTR) 적용: 재발급 시 기존 JTI를 원자적 Lua Script로 교체하여 토큰 탈취 및 재사용 공격을 방어한다.",
    "domain": "SECURITY",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/auth/security/RefreshTokenRepository.java",
        "symbol": "RefreshTokenRepository.rotate"
      }
    ],
    "evidence": {
      "evidence_id": "EV-SEC-002",
      "bundle_path": "PR-Files/evidence/bundles/EV-SEC-002",
      "type": "TEST_AND_SOURCE"
    },
    "verification": {
      "method": "JUnit5 Mockito Unit Test with DefaultRedisScript",
      "test_file": "backend/src/test/java/com/example/demo/auth/security/RefreshTokenRepositoryTest.java",
      "test_methods": [
        "rotateSuccess",
        "rotateFail",
        "rotateNull",
        "saveRefreshToken",
        "deleteRefreshToken"
      ],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 3.2)",
      "slides": ["004", "005", "006"],
      "presentation_source": "04_AUTH_AND_RBAC.md"
    }
  },
  {
    "claim_id": "CLM-SEC-003",
    "claim": "로그아웃 시 Access Token 잔여 TTL 동안 Redis Blacklist에 등록하여 즉시 접근을 차단한다.",
    "domain": "SECURITY",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/auth/security/TokenBlacklistService.java",
        "symbol": "TokenBlacklistService.blacklist"
      }
    ],
    "evidence": {
      "evidence_id": "EV-SEC-003",
      "bundle_path": "PR-Files/evidence/bundles/EV-SEC-003",
      "type": "TEST_AND_SOURCE"
    },
    "verification": {
      "method": "JUnit5 Mockito Unit Test",
      "test_file": "backend/src/test/java/com/example/demo/auth/security/TokenBlacklistServiceTest.java",
      "test_methods": [
        "blacklistSuccess",
        "isBlacklistedReturnsTrue",
        "isBlacklistedReturnsFalse",
        "blacklistThrowsRedisUnavailableExceptionWhenRedisFails"
      ],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 4.1)",
      "slides": ["004", "005", "006"],
      "presentation_source": "06_SECURITY.md"
    }
  },
  {
    "claim_id": "CLM-RBAC-001",
    "claim": "User-Role-Permission M:N 다대다 매핑 구조를 통해 인가되지 않은 엔드포인트 접근 시 403 Forbidden을 반환한다.",
    "domain": "RBAC",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/auth/security/UserAuthorityService.java",
        "symbol": "UserAuthorityService"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/resources/db/migration/V2__init_authority_schema.sql",
        "symbol": "roles, permissions, role_permissions"
      }
    ],
    "evidence": {
      "evidence_id": "EV-RBAC-001",
      "bundle_path": "PR-Files/evidence/bundles/EV-RBAC-001",
      "type": "INTEGRATION_TEST"
    },
    "verification": {
      "method": "MockMvc Integration Test",
      "test_file": "backend/src/test/java/com/example/demo/iam/rbac/RbacSecurityIntegrationTest.java",
      "test_methods": [
        "adminCanAssignPermissions",
        "normalUserCannotAssignPermissions",
        "unauthenticatedUserCannotAssignPermissions"
      ],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 3.3)",
      "slides": ["004", "006"],
      "presentation_source": "04_AUTH_AND_RBAC.md"
    }
  },
  {
    "claim_id": "CLM-RBAC-002",
    "claim": "사용자 역할(Role)에 매핑된 메뉴 권한(MENU_READ)에 따라 동적으로 메뉴 조회를 인가하고 미권한 시 403을 반환한다.",
    "domain": "RBAC",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/iam/menu/MenuAdminController.java",
        "symbol": "MenuAdminController"
      }
    ],
    "evidence": {
      "evidence_id": "EV-RBAC-002",
      "bundle_path": "PR-Files/evidence/bundles/EV-RBAC-002",
      "type": "INTEGRATION_TEST"
    },
    "verification": {
      "method": "MockMvc Security Integration Test",
      "test_file": "backend/src/test/java/com/example/demo/menu/MenuSecurityIntegrationTest.java",
      "test_methods": [
        "MENU_READ_권한이_있으면_메뉴를_조회할_수_있다",
        "MENU_READ_권한이_없으면_메뉴_조회가_거부된다",
        "인증된_사용자라도_MENU_READ가_없으면_403이다"
      ],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 3.3)",
      "slides": ["004", "006"],
      "presentation_source": "04_AUTH_AND_RBAC.md"
    }
  },
  {
    "claim_id": "CLM-PERF-001",
    "claim": "k6 부하 테스트 실측: 70 VU 동시 부하(1분 지속, 3회 평균)에서 평균 지연시간 5.64ms, P95 9.98ms, 처리량 463 req/s, 에러율 0.00%를 달성한다.",
    "domain": "PERFORMANCE",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "k6/scenarios/load.test.js",
        "symbol": "options"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "k6/config/thresholds.js",
        "symbol": "thresholds"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "docs/performance/k6-load-test.md",
        "symbol": "Section 3.2"
      }
    ],
    "evidence": {
      "evidence_id": "EV-PERF-001",
      "bundle_path": "PR-Files/evidence/bundles/EV-PERF-001",
      "type": "BENCHMARK_REPORT"
    },
    "verification": {
      "method": "k6 Automated Load Test (3 repeated runs: 5th, 6th, 7th)",
      "metrics": {
        "vus": 70,
        "duration": "1m",
        "avg_latency_ms": 5.64,
        "p95_latency_ms": 9.98,
        "throughput_rps": 463.6,
        "error_rate_pct": 0.00
      },
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 2)",
      "slides": ["001", "010"],
      "presentation_source": "08_PERFORMANCE.md"
    }
  },
  {
    "claim_id": "CLM-INFRA-001",
    "claim": "Nginx를 단일 외부 진입점(Port 80)으로 두고 내부 백엔드(8080), DB, Redis 포트를 격리하여 보안 및 리버스 프록시를 구성한다.",
    "domain": "ARCHITECTURE",
    "status": "IMPLEMENTED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "nginx/default.conf",
        "symbol": "server / upstream"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "docker-compose.yml",
        "symbol": "services.nginx"
      }
    ],
    "evidence": {
      "evidence_id": "EV-INFRA-001",
      "bundle_path": "PR-Files/evidence/bundles/EV-INFRA-001",
      "type": "CONFIGURATION"
    },
    "verification": {
      "method": "Docker Compose Topology & Nginx Proxy Validation",
      "status": "IMPLEMENTED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 4.2)",
      "slides": ["003", "008"],
      "presentation_source": "03_ARCHITECTURE.md"
    }
  },
  {
    "claim_id": "CLM-TS-001",
    "claim": "Redis 장애 시 Lettuce 커맨드 타임아웃을 기본 1분에서 2초로 단축하고 503 예외로 격리하여 스레드 풀 고갈을 방지한다.",
    "domain": "INCIDENT",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/resources/application.yaml",
        "symbol": "spring.data.redis.lettuce.command-timeout: 2000ms"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/main/java/com/example/demo/auth/security/RedisUnavailableException.java",
        "symbol": "RedisUnavailableException"
      }
    ],
    "evidence": {
      "evidence_id": "EV-TS-001",
      "bundle_path": "PR-Files/evidence/bundles/EV-TS-001",
      "type": "TROUBLESHOOTING_REPORT"
    },
    "verification": {
      "method": "Unit Test Exception Handling & Lettuce Config",
      "test_file": "backend/src/test/java/com/example/demo/auth/security/TokenBlacklistServiceTest.java",
      "test_methods": ["blacklistThrowsRedisUnavailableExceptionWhenRedisFails"],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 4.1)",
      "slides": ["007"],
      "presentation_source": "09_TROUBLESHOOTING.md"
    }
  },
  {
    "claim_id": "CLM-TS-002",
    "claim": "토큰 재발급 실패(401) 시 프론트엔드 인터셉터에서 즉시 세션을 초기화하고 무한 재시도 루프를 차단한다.",
    "domain": "INCIDENT",
    "status": "VERIFIED",
    "sources": [
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "frontend/src/api/http.ts",
        "symbol": "refreshPromise & 401 exit condition"
      },
      {
        "repository": "26-05adf",
        "branch": "feature/auth@0603@1401",
        "commit": commit_26,
        "path": "backend/src/test/java/com/example/demo/auth/security/SecurityIntegrationTest.java",
        "symbol": "unauthenticatedUserCannotAccessProtectedApi"
      }
    ],
    "evidence": {
      "evidence_id": "EV-TS-002",
      "bundle_path": "PR-Files/evidence/bundles/EV-TS-002",
      "type": "TROUBLESHOOTING_REPORT"
    },
    "verification": {
      "method": "Integration Test & Client Interceptor Single Flight",
      "test_file": "backend/src/test/java/com/example/demo/auth/security/SecurityIntegrationTest.java",
      "test_methods": ["unauthenticatedUserCannotAccessProtectedApi"],
      "status": "VERIFIED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 5)",
      "slides": ["007"],
      "presentation_source": "09_TROUBLESHOOTING.md"
    }
  },
  {
    "claim_id": "CLM-AI-001",
    "claim": "SA-1 8단계 엔지니어링 라이프사이클과 Zero-Chatter 거버넌스를 통해 AI 협업 의사결정과 변경 이력을 체계적으로 관리한다.",
    "domain": "AI_PROCESS",
    "status": "DOCUMENTED",
    "sources": [
      {
        "repository": "SA-1",
        "branch": "main",
        "commit": commit_sa1,
        "path": "conventions/rules.md",
        "symbol": "5대 원칙"
      },
      {
        "repository": "SA-1",
        "branch": "main",
        "commit": commit_sa1,
        "path": "changelogs/phase1_backend/1-2_jwt_redis_optimization.md",
        "symbol": "Phase 1-2 Changelog"
      }
    ],
    "evidence": {
      "evidence_id": "EV-AI-001",
      "bundle_path": "PR-Files/evidence/bundles/EV-AI-001",
      "type": "GOVERNANCE_SPEC"
    },
    "verification": {
      "method": "SA-1 Commit History & Changelog Audit",
      "status": "DOCUMENTED"
    },
    "portfolio_mapping": {
      "case_study": "CS-ENGINEERING-01 (Section 2)",
      "slides": ["012"],
      "presentation_source": "10_AI_WORKFLOW.md"
    }
  }
]

# Write Claim JSONs
claims_dir = evidence_base / "claims"
claims_dir.mkdir(parents=True, exist_ok=True)
for claim in claims_data:
    cid = claim["claim_id"]
    cf = claims_dir / f"{cid}.json"
    cf.write_text(json.dumps(claim, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Generated {len(claims_data)} claims in {claims_dir}")

# 3. Create Evidence Bundles
bundles_dir = evidence_base / "bundles"
bundles_dir.mkdir(parents=True, exist_ok=True)

for claim in claims_data:
    ev_id = claim["evidence"]["evidence_id"]
    bdir = bundles_dir / ev_id
    bdir.mkdir(parents=True, exist_ok=True)
    
    (bdir / "source").mkdir(exist_ok=True)
    (bdir / "documentation").mkdir(exist_ok=True)
    (bdir / "test").mkdir(exist_ok=True)
    (bdir / "result").mkdir(exist_ok=True)
    
    # Copy source / test files if exist
    for src in claim["sources"]:
        repo_name = src["repository"]
        rpath = src["path"]
        src_root = base_root / repo_name / rpath
        if src_root.exists() and src_root.is_file():
            dst = bdir / "source" / pathlib.Path(rpath).name
            dst.write_bytes(src_root.read_bytes())
            
    vtest = claim.get("verification", {}).get("test_file")
    if vtest:
        test_src = base_root / "26-05adf" / vtest
        if test_src.exists():
            dst = bdir / "test" / pathlib.Path(vtest).name
            dst.write_bytes(test_src.read_bytes())
            
    # Write manifest
    bundle_manifest = {
        "evidence_id": ev_id,
        "claim_id": claim["claim_id"],
        "domain": claim["domain"],
        "status": claim["status"],
        "captured_at": now_iso,
        "source_repository": claim["sources"][0]["repository"],
        "source_commit": claim["sources"][0].get("commit", ""),
        "verification_method": claim["verification"]["method"]
    }
    (bdir / "manifest.json").write_text(json.dumps(bundle_manifest, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Generated Evidence Bundles in {bundles_dir}")
