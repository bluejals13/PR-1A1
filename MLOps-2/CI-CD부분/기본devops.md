

## 🏗️ 1. 전체 구조 (표준 실무 아키텍처)

```text
myapp/
├── backend/                 # Spring Boot API
├── frontend/                # React SPA
├── infra/
│   ├── docker/              # docker-compose + nginx + prometheus
│   └── terraform/           # AWS 인프라 (ECS 전환용)
├── .github/workflows/       # CI/CD
└── README.md
```

---

## 🌐 2. 시스템 아키텍처

```text
Browser
  ↓
Nginx (Static + Reverse Proxy)
  ├── React (static)
  └── /api → Spring Boot

Spring Boot
  ├── MySQL
  └── Redis

Observability
  ├── Prometheus (metrics)
  └── Grafana (visualization)
```

---

## ⚙️ 3. 설계 핵심 (실무 기준)

| 항목     | 기준                                |
| ------ | --------------------------------- |
| 보안     | DTO 분리 + env 분리                   |
| 배포 안정성 | healthcheck + depends_on          |
| 장애 대응  | restart always                    |
| 구조     | Controller / Service / Repository |
| 성능     | Redis 캐시                          |
| 확장     | Kafka / ECS 가능 구조                 |
| 운영     | Docker Compose 기반 초기 운영           |

---

## 🐳 4. docker-compose 핵심 구조

### ✔ 핵심 포인트

* DB 먼저 뜨고 backend 실행 (healthcheck 기반)
* backend 정상 → nginx 실행
* Redis/MySQL 안정성 체크

```yaml
backend:
  depends_on:
    mysql:
      condition: service_healthy
    redis:
      condition: service_healthy

mysql:
  healthcheck:
    test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]

redis:
  healthcheck:
    test: ["CMD", "redis-cli", "ping"]
```

---

## 🚀 5. CI/CD 구조

| 단계     | 내용                   |
| ------ | -------------------- |
| Build  | Gradle / React build |
| Test   | backend unit test    |
| Docker | image 생성             |
| Push   | GHCR / ECR           |
| Deploy | EC2 or ECS           |

---

## 📊 6. 운영 구성 요소

| 영역         | 도구                   |
| ---------- | -------------------- |
| CI/CD      | GitHub Actions       |
| Container  | Docker               |
| Registry   | GHCR / ECR           |
| Deploy     | Docker Compose → ECS |
| Infra      | Terraform            |
| Monitoring | Prometheus + Grafana |

---

## ☁️ 7. Terraform 구조

| 파일     | 역할      |
| ------ | ------- |
| vpc.tf | 네트워크    |
| ecs.tf | 서비스     |
| ecr.tf | 이미지 저장소 |
| alb.tf | 로드밸런서   |
| iam.tf | 권한      |

```text
CI → Build → Push ECR → Terraform → ECS Deploy
```

---

## 📈 8. 운영 철학

| 원칙        | 설명                  |
| --------- | ------------------- |
| 구조 고정     | CI/CD는 만들고 거의 안 건드림 |
| 분리        | build / deploy 분리   |
| 인프라 코드화   | Terraform 단일 책임     |
| stateless | 컨테이너 상태 유지 금지       |
| 자동화       | 수동 SSH 배포 금지        |

---

## 🧠 9. 핵심 요약

* docker-compose는 **로컬/초기 운영**
* ECS는 **확장 단계**
* Terraform은 **인프라 전용**
* CI/CD는 **자동화 고정 구조**
* Prometheus/Grafana는 **관측 기본 세트**

---
