# Architecture Specifications (`PR-Files/architecture`)

## 1. Purpose (목적)
시스템의 네트워크 토폴로지, 단일 진입점(Reverse Proxy), 백엔드 및 데이터/스토리지 컨테이너 격리, 옵저버빌리티 파이프라인의 구조적 설계와 연결 관계를 기술적으로 명세합니다.

## 2. Input / Source (원천 데이터)
- `26-05adf/docker-compose.yml` (7개 컨테이너 서비스 정의)
- `26-05adf/nginx/default.conf` (Port 80 리버스 프록시 설정)
- `26-05adf/docs/01_Architecture_and_Ports.md`

## 3. Output (산출물)
- **`ARCHITECTURE_SPEC.md`**: 시스템 및 네트워크 토폴로지 아키텍처 상세 기술 명세서

## 4. What belongs here (포함되는 자료)
- Nginx 리버스 프록시 단일 진입점(Port 80) 및 라우팅 규칙
- Docker 브리지 네트워크 격리 정책 및 포트 매핑 규격
- Spring Boot, MySQL, Redis, Prometheus, VictoriaMetrics, Grafana 간 연결 다이어그램 및 데이터 플로우

## 5. What does NOT belong here (포함되지 않는 자료)
- 발표용 스타일링/시각 효과가 적용된 프레젠테이션 SVG/HTML
- 비즈니스 도메인별 세부 Java 코드 구현
- 미구현된 분산 아키텍처를 구현된 것처럼 기술하는 내용

## 6. Relationship with PRD-PO (PRD-PO와의 관계)
- `PRD-PO/presentation/slides/003/`의 컨테이너 토폴로지 다이어그램과 `PRD-PO/presentation/source/03_ARCHITECTURE.md`는 본 디렉터리의 아키텍처 명세를 1:1로 참조하여 시각화 및 발표용으로 가공됩니다.
