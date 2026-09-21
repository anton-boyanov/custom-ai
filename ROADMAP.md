# Lab Roadmap

## Milestone 0 — Environment validation

Статус: завършен.

- WSL2 Ubuntu работи.
- Docker Engine работи.
- `nvidia-smi` работи в WSL.
- Docker контейнер с `--gpus all` вижда RTX 3080.
- Създаден е `kind` cluster `ai-lab`.
- Клъстерът има control-plane и два worker nodes.
- CoreDNS, kindnet и local-path storage са в работещо състояние.
- Тестовият nginx Deployment е стартиран върху `ai-lab-worker2`.
- Потвърдено е, че текущите `kind` nodes нямат GPU passthrough.

## Milestone 1 — Kubernetes application baseline

Статус: започнат.

- [x] Namespace `ai-platform`.
- [x] Deployment с nginx тестов workload.
- [x] Service към Deployment-а.
- [ ] Port-forward тест.
- [ ] Resource requests и limits.
- [ ] Readiness и liveness probes.
- [ ] Declarative manifests вместо imperative commands.

## Milestone 2 — Helm

Предстои:

- [ ] `charts/ai-platform` chart.
- [ ] values за image, resources, replicas и storage.
- [ ] `helm lint`.
- [ ] install, upgrade и rollback.

## Milestone 3 — GPU model serving

Предстои:

- [ ] Избор на GPU-enabled local runtime.
- [ ] NVIDIA device plugin.
- [ ] GPU resource discovery в Kubernetes.
- [ ] Quantized 7B–8B coding model.
- [ ] Ollama или vLLM.
- [ ] API smoke test.

## Milestone 4 — Production practices

- [ ] Observability.
- [ ] Security hardening.
- [ ] CI/CD.
- [ ] Image scanning.
- [ ] Failure and recovery exercises.
- [ ] EKS migration notes.

