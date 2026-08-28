# Gemini Canvas Presentation Generation Prompt

> **사용 방법:**
> 1. Gemini Canvas 또는 Gemini Advanced 대화창을 엽니다.
> 2. `PRD-PO/presentation/source/` 폴더 내의 마크다운 파일들(`01_PROJECT_OVERVIEW.md` ~ `11_LIMITATIONS_AND_ROADMAP.md`)과 `PRESENTATION_SPEC.md`를 첨부(Attach)합니다.
> 3. 아래의 프롬프트 전문을 복사하여 Gemini에 입력하고 실행합니다.

---

```markdown
# Role & Objective
You are an expert technical presentation designer and senior software engineering communicator.
Your task is to generate a comprehensive, highly professional, 15-slide technical presentation deck based EXCLUSIVELY on the attached source files and presentation specification.
The generated deck will be used in Google Slides / PDF format for technical interviews and architecture presentations.

---

# Input Context
The attached markdown files (`PRESENTATION_SPEC.md` and `source/01_PROJECT_OVERVIEW.md` through `source/11_LIMITATIONS_AND_ROADMAP.md`) represent the verified **Source of Truth** and evidence base for this project.

---

# Strict Rules & Zero-Hallucination Guardrails
1. **Fact Fidelity (Zero Hallucination):**
   - Use ONLY facts, architecture designs, and benchmark figures explicitly stated in the attached files.
   - Do NOT invent or estimate any metrics. (Exact Performance Facts: 70 VUs, 1 min, Avg 5.64ms, P95 9.98ms, Throughput 463 req/s, Error Rate 0.00%).
   - Do NOT add external libraries, databases, or cloud services not present in the source files.
2. **Planned Features Isolation:**
   - Any unverified or future roadmap items (e.g., JPA N+1 benchmark numbers, Message Queue/Kafka, Redis Cluster, Vault/TLS) MUST be explicitly labeled with `[PLANNED]` or placed in the Roadmap section. NEVER describe them as implemented.
3. **Banned Expressions vs Allowed Expressions:**
   - 🚫 NEVER USE: "완벽한 보안", "업계 최고 성능", "SLA 보장", "완벽하게 확장 가능", "무결점 시스템"
   - ✅ ALWAYS USE: "구현", "검증", "실측", "확인", "정의된 테스트 조건에서 검증 완료", "현재 구현 범위", "향후 개선 과제"

---

# Story Arc & Slide Structure (15 Slides)
Generate the presentation following the 15-slide blueprint from `PRESENTATION_SPEC.md`:

- **Slide 01: Project Identity & Architecture Overview** (Identity & 4 Core Pillars)
- **Slide 02: Core Engineering Challenges & Objectives** (3 Key Problems & Solutions)
- **Slide 03: System & Container Topology** (Nginx Gateway & 7 Docker Services Isolation)
- **Slide 04: Backend Clean Architecture & DTO Isolation** (Record DTO, ApiResponse, GlobalExceptionHandler)
- **Slide 05: Authentication Architecture (JWT & Lifecycles)** (1h Access Token vs 7d HttpOnly Refresh Token)
- **Slide 06: Advanced Token Security (RTR & Redis Blacklist)** (Replay Attack Defense & Instant Logout)
- **Slide 07: Authorization & RBAC Multi-Tier Hierarchy** (User-Role-Permission M:N Model & 403 Denial)
- **Slide 08: Database Schema & Migration Governance (Flyway)** (Flyway V1~V5 & validate mode)
- **Slide 09: Automated Security & Integration Verification** (10 Test Suites & 100% Pass Rate)
- **Slide 10: Performance Validation (k6 Benchmarks)** (70 VU, 463 req/s, 5.64ms Avg, 9.98ms P95, 0% Error)
- **Slide 11: Real-World Incident Troubleshooting (TS 6-Step)** (TS-01 Redis, TS-001 Loop, TS-003 Docker Binding)
- **Slide 12: Controlled AI Workflow (SA-1 Governance)** (Zero-Chatter, Documentation-First, 8-Stage Lifecycle)
- **Slide 13: Architectural Decisions & Technical Trade-offs** (Stateless vs Session, Resilience vs Coupling)
- **Slide 14: System Limitations & Future Roadmap (PLANNED)** (Current Limits vs Planned Improvements)
- **Slide 15: Conclusion & Engineering Identity** (Summary & Engineering Core Philosophy)

---

# Design & Visual Directives
1. **1 Slide = 1 Core Message:** Every slide must have a distinct, focused takeaway. Avoid text clustering.
2. **Visual Hierarchy:**
   - Architecture slides must use clear block diagrams or flowchart layouts.
   - Security/Auth flows must be presented as step-by-step visual flows or sequence cards.
   - Performance slide MUST feature large KPI highlight callouts (e.g., `463 req/s`, `5.64 ms`, `0.00% Error`).
   - Testing slide must display a clean 10-suite verification matrix/badge layout.
   - Troubleshooting slide must use a `Symptom ➔ Root Cause ➔ Resolution` comparative card structure.
   - AI Workflow slide must represent the 8-Stage Pipeline visually.
3. **Concise Content:**
   - NO long code blocks (only 3~5 line core snippets if essential).
   - NO wall of paragraphs. Use structured bullet points and visual badges (`[IMPLEMENTED]`, `[VERIFIED]`, `[PLANNED]`).
4. **Speaker Notes:**
   - Provide a concise (30~60 seconds) speaker script for every single slide under `🎙️ Speaker Note:`.

---

# Output Format
Generate the output in clean, structured Markdown ready to be transferred or rendered directly into Google Slides, including:
- `## Slide [XX]: [Title]`
- `> **Core Takeaway:** [One sentence]`
- `### Visual Layout & Structure`
- `### Slide Body (Key Points & Badges)`
- `---`
- `> 🎙️ **Speaker Note:** [Script in Korean]`
```
