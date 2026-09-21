# Custom AI Kubernetes Lab

Локална AI платформа с open-weight модели, която се изгражда постепенно като production-like DevOps лаборатория.

## Цели

- self-hosted model serving без платени API calls;
- Kubernetes, Helm, networking, storage и scheduling;
- GPU workloads с NVIDIA RTX 3080;
- observability, security и CI/CD;
- RAG върху локални документи и code repositories;
- подготовка за миграция от локална среда към AWS/EKS.

## Текущо състояние

- WSL2 Ubuntu: работи;
- Docker Engine: работи;
- NVIDIA RTX 3080: 10 GiB VRAM;
- Docker GPU passthrough: валидиран с `nvidia/cuda` контейнер;
- Kubernetes: 3-node `kind` cluster `ai-lab`;
- Kubernetes nodes: 1 control-plane + 2 workers;
- Kubernetes system pods и local-path storage: работят;
- тестов Deployment: успешно schedule-нат върху worker node;
- GPU passthrough към `kind` nodes: все още не е конфигуриран.

## Архитектура по етапи

```text
Client / Aider / VS Code
          |
          v
    Ingress / API
          |
          v
    Model Serving ---- Persistent Volume
          |
          v
      GPU / CPU

Documents --> Embeddings --> Vector DB --> RAG API
```

## План на лабораторията

1. Валидиране на WSL, Docker, GPU и Kubernetes средата.
2. Kubernetes базови workloads: Deployment, Service, probes и resources.
3. Helm chart за AI платформата.
4. GPU-enabled локален Kubernetes runtime и NVIDIA device plugin.
5. Model serving с quantized 7B–8B coding модел.
6. OpenAI-compatible API и streaming responses.
7. Persistent model cache и управление на storage.
8. RAG с embeddings и vector database.
9. Observability с Prometheus, Grafana и логове.
10. Security: RBAC, Secrets, NetworkPolicy и non-root containers.
11. CI/CD, image scanning и reproducible deployments.
12. Документация и migration path към EKS.

## Работен принцип

Всяка значима стъпка се добавя като отделен commit с проверим резултат, команда за възпроизвеждане и кратка документация.

