ARG K3S_TAG=v1.35.5-k3s1
ARG CUDA_TAG=12.8.1-base-ubuntu24.04

FROM rancher/k3s:${K3S_TAG} AS k3s

FROM nvidia/cuda:${CUDA_TAG}

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       curl \
       gnupg \
    && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
       | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
    && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
       | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
       > /etc/apt/sources.list.d/nvidia-container-toolkit.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends nvidia-container-toolkit \
    && nvidia-ctk runtime configure --runtime=containerd \
    && mkdir -p /var/lib/rancher/k3s/agent/etc/containerd \
    && mkdir -p /var/lib/rancher/k3s/agent/etc/containerd \
    && rm -rf /var/lib/apt/lists/*

COPY --from=k3s /bin /bin
COPY --from=k3s /etc /etc

ENV PATH="/var/lib/rancher/k3s/data/cni:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/bin/aux"
ENV CRI_CONFIG_FILE="/var/lib/rancher/k3s/agent/etc/crictl.yaml"

VOLUME ["/var/lib/kubelet", "/var/lib/rancher/k3s", "/var/lib/cni", "/var/log"]

ENTRYPOINT ["/bin/k3s"]
CMD ["agent"]
