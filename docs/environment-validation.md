# Environment Validation

Дата: 2026-09-21

## Host resources

- OS environment: WSL2 Ubuntu
- CPU: 12 logical processors
- Memory: 15 GiB available to WSL
- Swap: 4 GiB
- GPU: NVIDIA GeForce RTX 3080
- GPU memory: 10,240 MiB
- NVIDIA driver: 591.86
- CUDA reported by driver: 13.1

## Docker

Docker Engine работи и GPU passthrough-ът е валидиран с:

```bash
docker run --rm \
  --gpus all \
  nvidia/cuda:12.8.1-base-ubuntu24.04 \
  nvidia-smi
```

Очакваният резултат е RTX 3080 да се вижда вътре в контейнера.

## Kubernetes

Cluster: `ai-lab`

```text
ai-lab-control-plane   Ready   control-plane   v1.37.0
ai-lab-worker          Ready   <none>          v1.37.0
ai-lab-worker2         Ready   <none>          v1.37.0
```

Работещи системни компоненти:

- CoreDNS;
- kindnet;
- kube-proxy;
- kube-apiserver;
- kube-controller-manager;
- kube-scheduler;
- etcd;
- local-path-storage.

## Scheduling smoke test

Тестовият workload беше създаден в namespace `ai-platform`:

```bash
kubectl get pods -n ai-platform -o wide
```

Резултатът беше pod в `Running` състояние върху `ai-lab-worker2`.

## GPU limitation

Docker host-ът вижда GPU, но `kind` node контейнерите не са стартирани с GPU device requests:

```bash
docker inspect ai-lab-worker \
  --format '{{json .HostConfig.DeviceRequests}}'
```

Резултат: `null`.

Следователно NVIDIA device plugin не трябва да се инсталира върху текущия `kind` cluster преди да бъде конфигуриран GPU-enabled node runtime.

