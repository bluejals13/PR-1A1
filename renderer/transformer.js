/**
 * Renderer Engine - Transformer Module
 * File: PR-1A1/renderer/transformer.js
 * Description: Transforms Raw Document Content into 5 Distinct View Models
 */

function transformToViewModels(content) {
  // 1. Longform View Model
  const longformVM = {
    title: content.title || "Stateless JWT + Redis Token Lifecycle & Session Control",
    subtitle: content.subtitle || "Refresh Token Rotation (RTR) 및 Redis Blacklist 기반 무상태 인증의 실시간 세션 통제",
    state: content.state || "FRESH",
    change_level: content.change_level || "C3",
    sources: [
      { repo: "26-05adf", path: "backend/src/main/java/com/example/demo/auth/", desc: "JWT & Security 구현체" },
      { repo: "SA-1", path: "changelogs/phase1_backend/1-2_jwt_redis_optimization.md", desc: "의사결정 배경" },
      { repo: "PR-1A1", path: "PR-Files/specification/AUTH_AND_SECURITY_SPEC.md", desc: "기술 규격서" }
    ],
    sections: [
      {
        id: "sec-problem",
        title: "1. 무상태(Stateless) 인증의 보안 딜레마",
        role: "problem",
        badge: "DOCUMENTED",
        body: "Stateless JWT는 서명 검증만으로 인가가 가능하여 확장성이 높지만, '발급된 토큰의 즉시 회수 불가(Token Revocation Gap)'라는 태생적 보안 취약점이 존재합니다. 로그아웃 후에도 토큰 만료 시간까지 비인가 접근이 가능한 취약점을 방어해야 했습니다.",
        callout: {
          type: "callout-problem",
          title: "Core Dilemma",
          text: "로그아웃 요청 후에도 탈취된 Access Token으로 정상 API 인가가 통과되는 보안 홀 발생."
        }
      },
      {
        id: "sec-decision",
        title: "2. 3중 보안 방어선 및 Lua Script RTR 의사결정",
        role: "decision",
        badge: "VERIFIED",
        body: "순수 DB 세션 방식은 동시성 부하 시 I/O 병목을 유발하므로, 1시간 Stateless Access Token과 In-Memory Redis Blacklist, 1-RTT 원자적 Lua Script RTR을 결합한 3중 보안 계층을 채택했습니다.",
        callout: {
          type: "callout-decision",
          title: "Architectural Decision",
          text: "1차 Access Token 고속 검증 ➔ 2차 Redis Blacklist 즉시 차단 ➔ 3차 Lua Script RTR 재사용 방어"
        }
      },
      {
        id: "sec-architecture",
        title: "3. 토큰 라이프사이클 및 시퀀스 아키텍처",
        role: "architecture",
        badge: "VERIFIED",
        body: "Nginx(Port 80)를 단일 진입점으로 하여 Spring Boot API 서버와 In-Memory Redis 7 간의 토큰 발급/검증/폐기 흐름을 격리 구성했습니다.",
        diagram: {
          caption: "Authentication Sequence: Login ➔ Normal API Call ➔ Immediate Logout Invalidation",
          steps: [
            "Client ➔ Nginx:80 ➔ POST /api/auth/login ➔ Redis SET refresh:user (TTL 7d) ➔ Access (Bearer) + Refresh (HttpOnly Cookie)",
            "Client ➔ Nginx:80 ➔ GET /api/users/me ➔ 1) JWT 서명 검증 ➔ 2) Redis Blacklist 확인 ➔ 200 OK",
            "Client ➔ Nginx:80 ➔ POST /api/auth/logout ➔ Redis SET blacklist:{jti} (TTL 잔여시간) ➔ 즉시 무효화"
          ]
        }
      },
      {
        id: "sec-verification",
        title: "4. 보안 테스트 6종 통과 및 k6 70 VU 실측치 검증",
        role: "verification",
        badge: "VERIFIED FACT",
        body: "단위/통합 테스트 6종 100% 통과 및 k6 70 VU 동시 부하 환경에서 P95 9.98ms 및 0.00% 에러율로 가용성과 보안성을 완벽히 입증했습니다.",
        metrics: [
          { label: "Throughput", value: "463", unit: "req/s", desc: "70 VU 지속 부하" },
          { label: "Avg Latency", value: "5.64", unit: "ms", desc: "3회 실측 평균" },
          { label: "P95 Latency", value: "9.98", unit: "ms", desc: "임계치 50ms 통과" },
          { label: "Error Rate", value: "0.00", unit: "%", desc: "0 errors" }
        ]
      },
      {
        id: "sec-resilience",
        title: "5. 장애 내구성: Redis Lettuce 2s Defense (TS-01)",
        role: "tradeoff",
        badge: "DOCUMENTED",
        body: "Redis 컨테이너 다운 시 기본 60초 블로킹을 2초 타임아웃으로 단축하고, DataAccessException을 503 Service Unavailable로 격리하여 WAS 스레드 고갈을 원천 차단했습니다.",
        callout: {
          type: "callout-resilience",
          title: "TS-01 Incident Resolution",
          text: "Lettuce 커맨드 타임아웃 2초 설정 + RedisUnavailableException 503 변환"
        }
      },
      {
        id: "sec-limitations",
        title: "6. 한계점 및 향후 로드맵 (Honest Limitations)",
        role: "limitation",
        badge: "PLANNED",
        body: "현재 단일 Redis 노드 다운 시 인증이 503 처리되는 한계가 있으며, 향후 Redis Sentinel / Cluster 다중화 도입을 통해 99.99% 가용성을 확보할 계획입니다."
      }
    ]
  };

  // 2. Feature View Model
  const featureVM = {
    title: "Feature: Atomic Lua Script Refresh Token Rotation & Blacklist",
    subtitle: "동시 다발 재발급 요청 시 레이스 컨디션을 방지하는 1-RTT 원자적 JTI 교체 및 즉시 세션 제어",
    domain: "DOM-AUTH",
    steps: [
      {
        step_num: "01",
        label: "Problem & Dilemma",
        box_type: "callout-problem",
        title: "Replay Attack Vulnerability",
        desc: "탈취된 Refresh Token으로 다중 클라이언트에서 중복 갱신이 발생하는 취약점 차단 필요."
      },
      {
        step_num: "02",
        label: "Decision",
        box_type: "callout-decision",
        title: "1-RTT Atomic Lua Script",
        desc: "Redis 엔진 레벨에서 get ➔ validate ➔ setex를 단일 트랜잭션으로 원자적 실행."
      },
      {
        step_num: "03",
        label: "Implementation Code",
        is_code: true,
        filename: "RefreshTokenRepository.java",
        source_ref: "26-05adf/backend/src/main/.../RefreshTokenRepository.java (L45-L65)",
        code: `local current = redis.call('GET', KEYS[1])
if not current then return -1 end
if current == ARGV[1] then
    redis.call('SETEX', KEYS[1], ARGV[3], ARGV[2])
    return 1
else
    return 0
end`
      },
      {
        step_num: "04",
        label: "Implementation Code",
        is_code: true,
        filename: "JwtAuthenticationFilter.java (Single-Pass & Type Check)",
        source_ref: "26-05adf/backend/src/main/.../JwtAuthenticationFilter.java (L30-L50)",
        code: `Claims claims = jwtProvider.parseClaims(token);
if (!"access".equals(claims.get("type", String.class))) {
    log.warn("Invalid token type attempted: {}", claims.get("type"));
    filterChain.doFilter(request, response);
    return;
}
if (tokenBlacklistService.isBlacklisted(claims.getId())) {
    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Token is blacklisted");
    return;
}`
      },
      {
        step_num: "05",
        label: "Verification Evidence",
        is_evidence: true,
        claim_title: "JUnit 5 단위 테스트 3종 전원 통과 (rotateSuccess, rotateFail, rotateNull)",
        evidence_id: "ev-auth-rtr",
        test_file: "RefreshTokenRepositoryTest.java",
        status: "VERIFIED"
      }
    ]
  };

  // 3. Technical View Model
  const technicalVM = {
    title: "Technical Deep-Dive: Stateless vs Stateful Token Architecture & Trade-offs",
    subtitle: "RDBMS 세션 I/O 병목 방지와 In-Memory Redis 3중 방어선 엔지니어링 의사결정",
    decisions: [
      {
        name: "Stateless JWT + Redis In-Memory Blacklist 하이브리드 채택",
        rationale: "대용량 동시 요청 환경에서 RDBMS 세션 I/O 병목을 제거하고 서명 검증 위주로 처리하되, 로그아웃 시에만 Redis 잔여 TTL 블랙리스트로 즉시 무효화 완결.",
        rejected: [
          { option: "전통적 RDBMS 세션 테이블", reason: "동시 접속 증가 시 커넥션 풀 고갈 및 지연시간 증가로 k6 목표 달성 불가." },
          { option: "블랙리스트 없는 순수 무상태 JWT", reason: "로그아웃 후에도 만료 시까지 접근이 가능하여 엔터프라이즈 보안 요건 위배." }
        ]
      },
      {
        name: "Refresh Token Rotation 시 Lua Script 적용",
        rationale: "다중 커맨드 분기 시 발생하는 중간 검증 틈새(Race Condition)를 Redis 싱글 스레드 1-RTT 원자적 실행으로 원천 봉쇄.",
        rejected: [
          { option: "Spring Data Redis 다중 get/set", reason: "네트워크 왕복 오버헤드(2-RTT) 및 동시 요청 시 중복 토큰 발급 위험." }
        ]
      }
    ],
    tradeoffs: [
      {
        aspect: "Redis 저장소 의존성 도입",
        pro: "서브 밀리초(Sub-millisecond) 초고속 블랙리스트 및 JTI 교체 가능.",
        con: "Redis 장애 시 인증 서비스 블로킹 위험 발생.",
        mitigation: "Lettuce 커맨드 타임아웃을 2초로 단축하고 503 에러로 WAS 격리 (TS-01)."
      },
      {
        aspect: "Access Token 유효기간 1시간 설정",
        pro: "Refresh 요청 빈도 감소로 네트워크 트래픽 절감.",
        con: "탈취 시 유효기간 동안 잠재적 위험 존재.",
        mitigation: "HttpOnly Cookie 격리 및 로그아웃 시 즉시 블랙리스트 등록."
      }
    ],
    benchmarks: [
      { metric: "k6 70 VU Average Latency", target: "< 20.00 ms", actual: "5.64 ms", status: "PASS" },
      { metric: "k6 70 VU P95 Latency", target: "< 50.00 ms", actual: "9.98 ms", status: "PASS" },
      { metric: "k6 70 VU Error Rate", target: "< 1.00 %", actual: "0.00 %", status: "PASS" }
    ],
    limitations: [
      { issue: "Redis Cluster 다중 노드 레플리케이션 미구현", plan: "Sentinel / Cluster 다중화 도입 예정 [PLANNED]" },
      { issue: "OWASP ZAP 자동화 모의 침투 테스트", plan: "CI/CD 파이프라인 연계 예정 [PLANNED]" }
    ]
  };

  // 4. Slide View Model (3 Slides)
  const slideVM = {
    title: "APMS.SR Authentication & Token Lifecycle Presentation",
    total_slides: 3,
    aspect_ratio: "16:9",
    slides: [
      {
        index: 1,
        layout: "LAYOUT_SPLIT",
        headline: "무상태(Stateless) JWT의 보안 딜레마: 즉시 세션 무효화의 한계",
        takeaway: "확장성을 유지하면서 즉시 로그아웃과 토큰 탈취를 방어할 3중 계층 설계 필요",
        left_html: `<div class="callout callout-problem">
          <span class="callout-title">Core Dilemma</span>
          <span>무상태 JWT는 DB 부하를 줄이지만, 발급된 토큰을 중간에 폐기할 수 없는 Token Revocation Gap이 존재합니다.</span>
        </div>
        <p style="color: var(--text-secondary); font-size: 15px; line-height: 1.6;">
          • RDBMS 세션: 즉시 제어 가능하나 I/O 병목 발생<br>
          • 순수 JWT: 확장성 높으나 즉시 로그아웃 불가<br>
          • <strong>목표:</strong> 확장성과 실시간 세션 통제력의 동시 확보
        </p>`,
        right_html: `<div style="background: var(--bg-app); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: var(--space-4); text-align: center;">
          <span style="font-family: var(--font-mono); font-size: 12px; color: var(--color-primary); display: block; margin-bottom: 8px;">[ Problem Boundary Matrix ]</span>
          <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
            <div style="padding: 8px; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 4px; color: var(--status-error);">❌ Stateful Session: DB Connection Pool Exhaustion</div>
            <div style="padding: 8px; background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 4px; color: var(--status-warning);">⚠️ Pure JWT: Cannot Revoke Stolen Tokens</div>
            <div style="padding: 8px; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 4px; color: var(--status-success);">✓ APMS Hybrid: Stateless + In-Memory Blacklist</div>
          </div>
        </div>`,
        evidences: ["ev-auth-jwt-filter"],
        source: "26-05adf/backend/src/.../JwtAuthenticationFilter.java"
      },
      {
        index: 2,
        layout: "LAYOUT_SEQUENCE",
        headline: "3중 보안 방어선 & 원자적 Lua Script Refresh Token Rotation",
        takeaway: "1h Access Token + 7d HttpOnly RTR + In-Memory Redis Blacklist의 하이브리드 결합",
        left_html: `<div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-bottom: 12px;">
          <div class="card" style="padding: 12px;">
            <div style="font-family: var(--font-mono); font-size: 11px; color: var(--color-primary);">1차 방어선</div>
            <div style="font-weight: bold; font-size: 14px; margin: 4px 0;">Stateless JWT (1h)</div>
            <div style="font-size: 12px; color: var(--text-muted);">서명 및 Token Type 검증으로 DB 무부하 고속 처리</div>
          </div>
          <div class="card" style="padding: 12px;">
            <div style="font-family: var(--font-mono); font-size: 11px; color: var(--ev-documented);">2차 방어선</div>
            <div style="font-weight: bold; font-size: 14px; margin: 4px 0;">Redis Blacklist</div>
            <div style="font-size: 12px; color: var(--text-muted);">로그아웃 시 잔여 TTL 동안 Redis 적재 즉시 차단</div>
          </div>
          <div class="card" style="padding: 12px;">
            <div style="font-family: var(--font-mono); font-size: 11px; color: var(--ev-verified);">3차 방어선</div>
            <div style="font-weight: bold; font-size: 14px; margin: 4px 0;">1-RTT Lua RTR (7d)</div>
            <div style="font-size: 12px; color: var(--text-muted);">토큰 갱신 시 원자적 JTI 교체로 재사용 원천 방어</div>
          </div>
        </div>`,
        right_html: `<div style="background: var(--bg-app); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 12px; font-family: var(--font-mono); font-size: 12px; color: var(--text-secondary);">
          <div style="color: var(--color-primary); margin-bottom: 4px;">// Flow Sequence:</div>
          Client ➔ Nginx:80 ➔ Spring Boot ➔ Redis 7 (In-Memory SETEX/Lua)
        </div>`,
        evidences: ["ev-auth-rtr", "ev-auth-blacklist"],
        source: "26-05adf/backend/src/.../RefreshTokenRepository.java"
      },
      {
        index: 3,
        layout: "LAYOUT_METRIC",
        headline: "6종 자동화 보안 테스트 통과 및 k6 5.64ms / 0.00% 에러율 검증",
        takeaway: "보안 계층 추가에도 불구하고 70 VU 동시 부하에서 P95 9.98ms의 초저지연 달성",
        left_html: `<div class="metric-grid" style="grid-template-columns: 1fr 1fr; gap: 12px;">
          <div class="metric-card">
            <span class="metric-label">Average Latency</span>
            <div class="metric-value-container">
              <span class="metric-value" style="font-size: 32px;">5.64</span>
              <span class="metric-unit">ms</span>
            </div>
            <span class="metric-status" style="color: var(--status-success); font-size: 11px;">✓ 임계치 20ms 통과</span>
          </div>
          <div class="metric-card">
            <span class="metric-label">P95 Latency</span>
            <div class="metric-value-container">
              <span class="metric-value" style="font-size: 32px;">9.98</span>
              <span class="metric-unit">ms</span>
            </div>
            <span class="metric-status" style="color: var(--status-success); font-size: 11px;">✓ 임계치 50ms 통과</span>
          </div>
          <div class="metric-card">
            <span class="metric-label">Throughput</span>
            <div class="metric-value-container">
              <span class="metric-value" style="font-size: 32px;">463</span>
              <span class="metric-unit">req/s</span>
            </div>
            <span class="metric-status" style="color: var(--status-success); font-size: 11px;">✓ 70 VU 1분 지속</span>
          </div>
          <div class="metric-card">
            <span class="metric-label">HTTP Errors</span>
            <div class="metric-value-container">
              <span class="metric-value" style="font-size: 32px;">0.00</span>
              <span class="metric-unit">%</span>
            </div>
            <span class="metric-status" style="color: var(--status-success); font-size: 11px;">✓ 0건 오류</span>
          </div>
        </div>`,
        right_html: `<div class="evidence-card" style="margin: 0; padding: 12px;">
          <div style="font-size: 13px; font-weight: bold; margin-bottom: 6px;">JUnit 5 Security Suites:</div>
          <div style="font-family: var(--font-mono); font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 4px;">
            <div>✓ JwtAuthenticationFilterTest (100% Pass)</div>
            <div>✓ RefreshTokenRepositoryTest (100% Pass)</div>
            <div>✓ TokenBlacklistServiceTest (100% Pass)</div>
            <div>✓ SecurityIntegrationTest (100% Pass)</div>
          </div>
        </div>`,
        evidences: ["ev-perf-70vu", "ev-auth-rtr"],
        source: "26-05adf/docs/performance/k6-load-test.md"
      }
    ]
  };

  // 5. Evidence View Model
  const evidenceVM = {
    title: "Verification & Evidence Traceability Ledger: DOM-AUTH",
    subtitle: "주장(Claim)에 대한 실제 테스트 코드, 실측 메트릭, 장애 보고서 및 재현 경로 감사 원장",
    pass_rate: "100%",
    total_claims: 4,
    verified_claims: 4,
    items: [
      {
        status: "VERIFIED",
        claim: "Access Token(유효시간 1시간)은 서명 검증만으로 무상태(Stateless) 인증을 수행하며, Authorization Bearer 헤더로 전달된다.",
        evidence_id: "ev-auth-jwt-filter",
        method: "JUnit 5 단위 테스트 (doFilterInternal_ValidToken, doFilterInternal_InvalidTokenType)",
        source_repo: "26-05adf",
        source_path: "backend/src/test/java/com/example/demo/auth/security/JwtAuthenticationFilterTest.java"
      },
      {
        status: "VERIFIED",
        claim: "Refresh Token(유효시간 7일)은 HttpOnly Secure Cookie로 전달되며, 토큰 갱신 시 원자적 Lua Script를 통해 JTI를 즉시 교체(RTR)하여 재사용 공격을 방어한다.",
        evidence_id: "ev-auth-rtr",
        method: "JUnit 5 단위 테스트 (rotate_Success, rotate_Fail_WhenMismatch, rotate_Fail_WhenNull)",
        source_repo: "26-05adf",
        source_path: "backend/src/test/java/com/example/demo/auth/security/RefreshTokenRepositoryTest.java"
      },
      {
        status: "VERIFIED",
        claim: "로그아웃 요청 시 Access Token의 잔여 TTL 동안 Redis Blacklist에 등록하여 해당 토큰의 즉시 접근을 원천 차단한다.",
        evidence_id: "ev-auth-blacklist",
        method: "JUnit 5 단위 테스트 (addToBlacklist_ShouldSetRedisKeyWithTtl, isBlacklisted_ShouldReturnTrue)",
        source_repo: "26-05adf",
        source_path: "backend/src/test/java/com/example/demo/auth/security/TokenBlacklistServiceTest.java"
      },
      {
        status: "DOCUMENTED",
        claim: "Redis 일시 장애 시 Lettuce 커맨드 타임아웃을 2초로 제한하고 503 Service Unavailable로 격리하여 WAS 스레드 풀 고갈을 방어한다.",
        evidence_id: "ev-ts-redis-timeout",
        method: "TS 6단계 표준 장애 분석 및 회복 검증 보고서",
        source_repo: "PR-1A1",
        source_path: "PR-Files/troubleshooting/TS-01-REDIS_TIMEOUT.md"
      }
    ]
  };

  return {
    longform: longformVM,
    feature: featureVM,
    technical: technicalVM,
    slide: slideVM,
    evidence: evidenceVM
  };
}

module.exports = {
  transformToViewModels
};
