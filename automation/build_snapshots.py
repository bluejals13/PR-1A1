import json
import hashlib
import pathlib
import datetime

# Root paths
base_root = pathlib.Path("C:/Users/bluej/Desktop/my2")
repo_26 = base_root / "26-05adf"
repo_sa1 = base_root / "SA-1"
repo_pr1 = base_root / "PR-1A1"

commit_26 = "9e6ef83d07cf3dc59e8625d78b70f45a5ad2613f"
commit_sa1 = "4a734a8edd8b670f8d29dc2a42a978ca3877a25f"
commit_pr1 = "c9f88722ad196ef7918240ab1faaaba4a8f64676"

now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha256_file(filepath: pathlib.Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# 1. Create work directories in PR-1A1
work_dirs = ["tasks", "reviews", "decisions", "drafts"]
for d in work_dirs:
    p = repo_pr1 / "work" / d
    p.mkdir(parents=True, exist_ok=True)
    readme = p / "README.md"
    if not readme.exists():
        readme.write_text(f"# Human Editable Work Area: {d}\n\nThis directory is dedicated for human-editable workflows, reviews, and drafts.\nIt is strictly separated from immutable evidence snapshots.\n", encoding="utf-8")

# 2. Key files to snapshot from 26-05adf
files_26 = [
    "backend/build.gradle",
    "backend/src/main/resources/application.yaml",
    "backend/src/main/java/com/example/demo/auth/jwt/JwtProvider.java",
    "backend/src/main/java/com/example/demo/auth/security/AuthService.java",
    "backend/src/main/java/com/example/demo/auth/security/RefreshTokenRepository.java",
    "backend/src/main/java/com/example/demo/auth/security/TokenBlacklistService.java",
    "backend/src/main/java/com/example/demo/auth/security/JwtAuthenticationFilter.java",
    "backend/src/main/java/com/example/demo/auth/security/SecurityConfig.java",
    "backend/src/main/java/com/example/demo/auth/security/UserAuthorityService.java",
    "backend/src/main/java/com/example/demo/common/dto/ApiResponse.java",
    "backend/src/main/java/com/example/demo/common/exception/GlobalExceptionHandler.java",
    "backend/src/main/java/com/example/demo/iam/user/repository/UserRepository.java",
    "backend/src/test/java/com/example/demo/auth/security/RefreshTokenRepositoryTest.java",
    "backend/src/test/java/com/example/demo/auth/security/TokenBlacklistServiceTest.java",
    "backend/src/test/java/com/example/demo/auth/security/JwtAuthenticationFilterTest.java",
    "backend/src/test/java/com/example/demo/auth/security/AuthControllerTest.java",
    "backend/src/test/java/com/example/demo/auth/security/AuthServiceTest.java",
    "backend/src/test/java/com/example/demo/auth/security/SecurityIntegrationTest.java",
    "backend/src/test/java/com/example/demo/iam/rbac/RbacSecurityIntegrationTest.java",
    "backend/src/test/java/com/example/demo/menu/MenuSecurityIntegrationTest.java",
    "frontend/src/api/http.ts",
    "frontend/src/auth/auth.bootstrap.ts",
    "frontend/src/store/auth.store.ts",
    "k6/scenarios/load.test.js",
    "k6/config/thresholds.js",
    "docker-compose.yml",
    "nginx/default.conf",
    "docs/performance/k6-load-test.md",
    "docs/troubleshooting/01-redis-failure.md"
]

# 3. Key files to snapshot from SA-1
files_sa1 = [
    "README.md",
    "architecture/01_Architecture_and_Ports.md",
    "architecture/02_Quick_Start.md",
    "conventions/03_Backend_Conventions.md",
    "conventions/04_Agent_Commands.md",
    "conventions/rules.md",
    "changelogs/phase1_backend/1-2_jwt_redis_optimization.md",
    "changelogs/phase1_backend/1-3_global_response_exception_handling.md",
    "changelogs/phase1_backend/1-4_jpa_n1_query_optimization.md",
    "changelogs/phase2_frontend/2-1_zustand_auth_optimization.md"
]

# 4. Manifest structure
manifest_entries_26 = []
snapshot_base_26 = repo_pr1 / "PR-Files" / "evidence" / "snapshots" / "26-05adf"
for rel in files_26:
    src_f = repo_26 / rel
    if src_f.exists():
        f_hash = sha256_file(src_f)
        manifest_entries_26.append({
            "path": rel,
            "sha256": f_hash,
            "size_bytes": src_f.stat().st_size
        })
        # copy to snapshot
        dst_f = snapshot_base_26 / rel
        dst_f.parent.mkdir(parents=True, exist_ok=True)
        dst_f.write_bytes(src_f.read_bytes())
    else:
        print(f"Warning: 26-05adf file not found: {rel}")

manifest_entries_sa1 = []
snapshot_base_sa1 = repo_pr1 / "PR-Files" / "evidence" / "snapshots" / "SA-1"
for rel in files_sa1:
    src_f = repo_sa1 / rel
    if src_f.exists():
        f_hash = sha256_file(src_f)
        manifest_entries_sa1.append({
            "path": rel,
            "sha256": f_hash,
            "size_bytes": src_f.stat().st_size
        })
        # copy to snapshot
        dst_f = snapshot_base_sa1 / rel
        dst_f.parent.mkdir(parents=True, exist_ok=True)
        dst_f.write_bytes(src_f.read_bytes())
    else:
        print(f"Warning: SA-1 file not found: {rel}")

# 5. Write manifest SOT-2026-09-05-001.json
manifest_data = {
    "manifest_id": "SOT-2026-09-05-001",
    "created_at": now_iso,
    "target_workspace": {
        "repository": "PR-1A1",
        "branch": "main",
        "commit": commit_pr1
    },
    "sources": [
        {
            "repository": "26-05adf",
            "role": "BUILD",
            "branch": "feature/auth@0603@1401",
            "commit": commit_26,
            "file_count": len(manifest_entries_26),
            "files": manifest_entries_26
        },
        {
            "repository": "SA-1",
            "role": "PROCESS",
            "branch": "main",
            "commit": commit_sa1,
            "file_count": len(manifest_entries_sa1),
            "files": manifest_entries_sa1
        }
    ]
}

manifest_file = repo_pr1 / "PR-Files" / "evidence" / "manifests" / "SOT-2026-09-05-001.json"
manifest_file.parent.mkdir(parents=True, exist_ok=True)
manifest_file.write_text(json.dumps(manifest_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Created manifest: {manifest_file}")

# 6. Write SOURCE_OF_TRUTH_SNAPSHOT.json
sot_json_data = {
    "snapshot_version": "1.2.0",
    "snapshot_date": "2026-09-05",
    "active_manifest": "SOT-2026-09-05-001",
    "repositories": {
        "build": {
            "name": "26-05adf",
            "branch": "feature/auth@0603@1401",
            "commit": commit_26,
            "url": "https://github.com/bluejals13/26-05adf.git",
            "tech_stack": {
                "java": "17",
                "spring_boot": "3.3.2",
                "gradle": "8.14.4",
                "jjwt": "0.11.5",
                "react": "18.3.1",
                "mysql": "8.0",
                "redis": "7.0",
                "nginx": "1.25"
            }
        },
        "process": {
            "name": "SA-1",
            "branch": "main",
            "commit": commit_sa1,
            "url": "https://github.com/bluejals13/SA-1.git",
            "governance": {
                "lifecycle": "8-Stage Engineering Lifecycle",
                "communication": "Zero-Chatter Policy",
                "documentation": "Documentation-First Policy"
            }
        },
        "proof": {
            "name": "PR-1A1",
            "branch": "main",
            "commit": commit_pr1,
            "url": "https://github.com/bluejals13/PR-1A1.git"
        }
    }
}

sot_json_file = repo_pr1 / "PR-Files" / "evidence" / "SOURCE_OF_TRUTH_SNAPSHOT.json"
sot_json_file.write_text(json.dumps(sot_json_data, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Created snapshot JSON: {sot_json_file}")
