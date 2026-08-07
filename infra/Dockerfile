FROM python:3.10-slim

LABEL org.opencontainers.image.title="firewall-base"
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    tcpdump \
    tshark \
    iproute2 \
    net-tools \
    iputils-ping \
    curl \
    iptables \
    libcap2-bin \
    gcc \
    g++ \
    build-essential \
    libpcap-dev \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Permitir captura com tcpdump sem exigir root (se suportado no host)
RUN if [ -f /usr/sbin/tcpdump ]; then setcap 'cap_net_raw,cap_net_admin+eip' /usr/sbin/tcpdump || true; fi

WORKDIR /app

# Copiar requirements e instalar (arquivo mínimo por enquanto)
COPY infra/requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    pip install --no-cache-dir --no-deps xgboost

# Copiar o projeto (pode ser ajustado mais tarde)
COPY . /app

CMD ["bash"]
