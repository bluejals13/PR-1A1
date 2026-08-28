# Architecture Specifications (`PR-Files/architecture`)

## 1. Responsibility
본 디렉터리는 시스템 전체의 구조적 설계, 컴포넌트 간 상호작용, 네트워크 토폴로지, 인프라 배치를 다룹니다.

## 2. Source of Truth Mapping
- **Source Files:**
  - `26-05adf/docs/01_Architecture_and_Ports.md`
  - `26-05adf/docker-compose.yml`
  - `26-05adf/nginx/default.conf`
  - `SA-1/architecture/01_Architecture_and_Ports.md`

## 3. Key Components
1. **Reverse Proxy (Nginx, Port 80):** SPA 정적 라우팅 및 `/api/*` 리버스 프록시 단일 진입점 `[IMPLEMENTED]`
2. **Backend API (Spring Boot 3.3.2, Port 8080):** Spring Security 6, JWT, RESTful API `[IMPLEMENTED]`
3. **Database (MySQL 8.0, Port 3306):** Flyway 기반 스키마 마이그레이션 `[IMPLEMENTED]`
4. **Cache & In-Memory Store (Redis 7.0, Port 6379):** RTR JTI 관리 및 Token Blacklist `[IMPLEMENTED]`
5. **Observability Stack:** Prometheus (9090), VictoriaMetrics (8428), Grafana (3000) `[IMPLEMENTED]`

## 4. Documentation Standard
- 아키텍처 다이어그램(Mermaid) 필수 포함
- 포트 매핑 및 네트워크 격리 정책 명시
- 데이터 플로우(Data Flow) 및 의존성 방향 명확화
