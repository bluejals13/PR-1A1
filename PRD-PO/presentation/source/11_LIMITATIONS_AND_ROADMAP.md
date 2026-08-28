# 11. Limitations & Future Roadmap

## What
현재 구현된 시스템의 아키텍처적 한계점을 객관적으로 인정하고, 사실(Fact)과 계획(Plan)을 엄격히 분리하여 향후 해결할 엔지니어링 로드맵.

## Why
- 엔지니어링의 신뢰성은 "할 수 있는 것과 아직 하지 않은 것"을 명확히 구분하는 데서 출발하기 때문.
- 미구현된 기능을 구현 완료로 과장(Hallucination)하지 않고, 공학적 타당성에 기반한 발전 방향을 제시.

## Current Limitations (현재 시스템 한계)
1. **단일 노드 인프라:** 단일 Docker Compose 인스턴스 구성으로, 1,000+ VU 이상의 대규모 트래픽에 대응하는 L7 오토스케일링 미적용.
2. **JPA N+1 쿼리 실측 데이터 부재:** 배치 사이즈 및 Fetch Join 설계는 존재하나, 쿼리 수 비교 정밀 벤치마크 데이터는 아직 미보유.
3. **완전 자율 배포 미적용:** 현재 CI/CD는 개발자의 수동 승인(Human-in-the-loop)을 필수로 진행.

## Future Roadmap (`[PLANNED]` 과제)
1. **JPA N+1 쿼리 최적화 실측 벤치마크:** Batch Size 및 Fetch Join 적용 전/후 실행 쿼리 수 및 힙 메모리 정밀 측정 `[PLANNED]`
2. **비동기 메시지 큐 (Message Queue):** 대용량 트래픽 이벤트 분산을 위한 Kafka / RabbitMQ 파이프라인 도입 `[PLANNED]`
3. **분산 캐시 클러스터링:** Redis Sentinel / Cluster 다중 노드 고가용성 구성 `[PLANNED]`
4. **클라우드 보안 및 TLS:** Production 환경 HashiCorp Vault / AWS KMS 연동 및 Let's Encrypt TLS 인증서 적용 `[PLANNED]`

## Evidence
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md` Section 2.6
- `26-05adf/task_progress.md`

## Result
- 검증 완료된 기능(`[VERIFIED]`)과 향후 계획 과제(`[PLANNED]`)의 엄격한 분리 관리 달성 `[DOCUMENTED]`

## Status
`[PLANNED]` `[DOCUMENTED]`

## Source
- `PR-Files/evidence/SOURCE_OF_TRUTH_SNAPSHOT.md`
- `26-05adf/task_progress.md`

## Presentation Use
- **Slide 14:** System Limitations & Future Roadmap (한계와 로드맵)
- **Slide 15:** Conclusion (지속 가능한 성장 방향)
