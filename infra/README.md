# Infraestrutura - Docker

Este diretório contém a configuração da infraestrutura baseada em Docker.

## Build da Imagem

Para buildar a imagem base (firewall-base):

```bash
docker build -f infra/Dockerfile -t firewall-base .
```

## Rodar um container

Para executar um container interativo:

```bash
docker run -it --rm firewall-base bash
```

## Verificar instalações

### Verificar Python
```bash
docker run --rm firewall-base python --version
```

### Verificar tcpdump
```bash
docker run --rm firewall-base tcpdump --version
```

### Verificar scapy
```bash
docker run --rm firewall-base python -c "import scapy; print(f'scapy: {scapy.__version__}')"
```

## Ferramentas instaladas (Requirements do Issue #02)

- **Python 3.10** (slim)
- **tcpdump** — captura de pacotes
- **tshark** — análise de protocolos
- **iproute2** — gerenciamento de rede
- **net-tools** — utilitários de rede
- **gcc / g++** — compiladores (para packages com extensões C)
- **libcap2-bin** — gerenciamento de capacidades (para tcpdump sem root)
- **scapy** — biblioteca Python para manipulação de pacotes
- **chromium / chromium-driver** — navegador headless para automação e geração de tráfego sintético
- **selenium** — framework de automação de navegador (Issue #08)
- **fonts-liberation / fonts-noto** — fontes para renderização correta de páginas

## Teste do Navegador Headless (Issue #08)

Para validar o funcionamento do Selenium com Chromium no container `app_client`:

```bash
# 1. Subir os containers do laboratório
docker compose -f infra/docker-compose.yml up -d --build

# 2. Executar o teste de sanidade do browser dentro do app_client
docker exec -it app_client python3 -m src.collector.test_browser_headless

# 3. (Opcional) Testar com URL personalizada
docker exec -it app_client python3 -m src.collector.test_browser_headless https://google.com
```

## Notas

- Use `!volumes/` no `.gitignore` para permitir que arquivos sejam salvos em volumes persistentes.
- O `tcpdump` é configurado com capacidades (`cap_net_raw,cap_net_admin`) para rodar sem privilégios totais.
- O container `app_client` possui `shm_size: 1g` configurado para evitar esgotamento de `/dev/shm` durante navegações complexas.
