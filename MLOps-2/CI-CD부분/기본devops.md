좋아, 이제 “진짜 실무 구조 문서” 스타일로 정리해줄게.

(설계도가 아니라 \*\*실제 파일 구조 + 설정 + 운영 기준 + 표 기반 설명\*\*)



\---



\# 🏗️ 1. 프로젝트 전체 구조 (실무형)



```text id="p0x9aa"

myapp/

├── backend/                          # Spring Boot

│   ├── src/main/java/...

│   ├── Dockerfile

│   ├── build.gradle

│   └── application.yml

│

├── frontend/                         # React

│   ├── src/

│   ├── dist/

│   ├── Dockerfile

│   └── nginx.conf

│

├── infra/

│   ├── terraform/                    # (나중 AWS 전환용)

│   │   ├── main.tf

│   │   ├── vpc.tf

│   │   ├── ecs.tf

│   │   └── ecr.tf

│   │

│   └── docker/

│       ├── docker-compose.yml

│       ├── nginx/

│       │   └── default.conf

│       └── prometheus/

│           └── prometheus.yml

│

├── .github/

│   └── workflows/

│       ├── ci-common.yml

│       ├── ci-backend.yml

│       └── ci-frontend.yml

│

└── README.md

```



\---



\# 🌐 2. 아키텍처 개요



```text id="a7x2qk"

\[ Browser ]

&#x20;    |

&#x20;    v

\[ Nginx (Reverse Proxy + Static Server) ]

&#x20;    |----------------------|

&#x20;    |                      |

&#x20;    v                      v

React dist (static)     /api/\*

&#x20;                          |

&#x20;                          v

&#x20;                  Spring Boot Backend

&#x20;                          |

&#x20;            -----------------------------

&#x20;            |                           |

&#x20;            v                           v

&#x20;       MySQL                      Redis Cache



Observability:

Prometheus → Metrics

Grafana → Visualization

Loki (optional) → Logs

```



\---



\# ⚙️ 3. 핵심 설계 포인트



| 관점     | 적용 내용                                              |

| ------ | -------------------------------------------------- |

| 보안     | DTO 분리, Entity 외부 노출 금지, `.env` 분리                 |

| 안정성    | Docker Healthcheck + `depends\_on: service\_healthy` |

| 운영성    | Restart Policy (`always`) 적용                       |

| 관측 가능성 | Prometheus + Grafana + Exporter                    |

| 유지보수   | Controller / Service / Repository 계층 분리            |

| 확장성    | Redis Cache + 향후 Kafka/Loki 확장 가능                  |

| 성능     | Redis 캐싱으로 DB read 감소                              |

| 배포     | Docker Compose 기반 통합 운영                            |



\---



\# 🐳 4. docker-compose (실무형 핵심)



```yaml id="c3p8qz"

version: "3.9"



services:



&#x20; nginx:

&#x20;   image: nginx:alpine

&#x20;   volumes:

&#x20;     - ./infra/docker/nginx/default.conf:/etc/nginx/conf.d/default.conf

&#x20;     - ./frontend/dist:/usr/share/nginx/html

&#x20;   ports:

&#x20;     - "80:80"

&#x20;   depends\_on:

&#x20;     backend:

&#x20;       condition: service\_healthy



&#x20; backend:

&#x20;   build: ./backend

&#x20;   environment:

&#x20;     SPRING\_PROFILES\_ACTIVE: prod

&#x20;   ports:

&#x20;     - "8080:8080"

&#x20;   depends\_on:

&#x20;     mysql:

&#x20;       condition: service\_healthy

&#x20;     redis:

&#x20;       condition: service\_healthy

&#x20;   healthcheck:

&#x20;     test: \["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]

&#x20;     interval: 10s

&#x20;     timeout: 3s

&#x20;     retries: 5



&#x20; mysql:

&#x20;   image: mysql:8

&#x20;   environment:

&#x20;     MYSQL\_ROOT\_PASSWORD: root

&#x20;     MYSQL\_DATABASE: app

&#x20;   ports:

&#x20;     - "3306:3306"

&#x20;   healthcheck:

&#x20;     test: \["CMD", "mysqladmin", "ping", "-h", "localhost"]

&#x20;     interval: 10s

&#x20;     timeout: 5s

&#x20;     retries: 5



&#x20; redis:

&#x20;   image: redis:7

&#x20;   ports:

&#x20;     - "6379:6379"

&#x20;   healthcheck:

&#x20;     test: \["CMD", "redis-cli", "ping"]

&#x20;     interval: 10s

&#x20;     timeout: 3s

&#x20;     retries: 5



&#x20; prometheus:

&#x20;   image: prom/prometheus

&#x20;   volumes:

&#x20;     - ./infra/docker/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

&#x20;   ports:

&#x20;     - "9090:9090"



&#x20; grafana:

&#x20;   image: grafana/grafana

&#x20;   ports:

&#x20;     - "3000:3000"

```



\---



\# 🚀 5. CI/CD 구조 (공통 + 분리)



\## 공통 CI



| 단계       | 내용                |

| -------- | ----------------- |

| Checkout | 코드 pull           |

| Setup    | JDK / Node 환경 구성  |

| Test     | Backend unit test |

| Lint     | 코드 품질 검사          |



\---



\## Backend CI/CD



| 단계           | 내용                        |

| ------------ | ------------------------- |

| Build        | Gradle build              |

| Docker Build | backend image 생성          |

| Push         | GHCR or ECR push          |

| Deploy       | EC2 or ECS deploy trigger |



\---



\## Frontend CI/CD



| 단계           | 내용                                |

| ------------ | --------------------------------- |

| Build        | React build                       |

| Docker Build | nginx image 생성                    |

| Push         | GHCR or ECR                       |

| Deploy       | Nginx reload or container restart |



\---



\# 📊 6. CI/CD 표 정리



| 영역            | 기술                      | 역할             |

| ------------- | ----------------------- | -------------- |

| CI            | GitHub Actions          | build/test 자동화 |

| Registry      | GHCR / ECR              | 이미지 저장         |

| Deploy (초기)   | EC2 + Docker Compose    | 간단 배포          |

| Deploy (확장)   | ECS/Fargate + Terraform | 운영 배포          |

| Infra as Code | Terraform               | AWS 인프라 관리     |



\---



\# ☁️ 7. Terraform 전환 구조 (핵심)



\## infra/terraform



| 파일     | 역할              |

| ------ | --------------- |

| vpc.tf | 네트워크 구성         |

| ecs.tf | ECS 서비스 정의      |

| ecr.tf | Docker registry |

| iam.tf | 권한 관리           |

| alb.tf | Load balancer   |



\---



\## Terraform 적용 후 구조



```text id="tf1"

GitHub Actions

&#x20;     ↓

Build Docker Image

&#x20;     ↓

Push to ECR

&#x20;     ↓

Terraform Apply

&#x20;     ↓

ECS 자동 롤링 배포

```



\---



\# 📈 8. 운영 철학 (실무 핵심)



| 원칙       | 설명                  |

| -------- | ------------------- |

| 변경 최소화   | CI/CD는 구조 고정        |

| 배포 분리    | build / deploy 분리   |

| infra 분리 | Terraform으로만 인프라 관리 |

| 상태 유지    | 컨테이너 stateless 유지   |

| 자동화 우선   | 수동 SSH 배포 제거        |



\---



\# 🧠 최종 핵심 요약



\* CI/CD는 “한 번 만들고 거의 안 건드리는 구조”가 맞음

\* GHCR/ECR은 “교체 가능한 레이어”로 설계

\* Terraform은 “배포/인프라만 담당”

\* docker-compose → ECS로 자연스럽게 확장 가능



\---



원하면 다음 단계로

👉 \*\*“이 구조 그대로 GitHub Actions 실제 production 템플릿”\*\*

👉 \*\*“Terraform ECS 완전 실전 코드 (VPC + ALB + ECR + Fargate)”\*\*



이건 진짜 실무 레벨로 이어서 만들어줄게.



