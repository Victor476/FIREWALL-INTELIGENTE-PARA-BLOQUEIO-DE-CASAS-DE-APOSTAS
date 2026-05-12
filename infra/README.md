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

## Notas

- Use `!volumes/` no `.gitignore` para permitir que arquivos sejam salvos em volumes persistentes.
- O `tcpdump` é configurado com capacidades (`cap_net_raw,cap_net_admin`) para rodar sem privilégios totais.
- A imagem importa o projeto inteiro; adapte conforme necessário.

## Próximos passos

- **Issue #03**: Configurar `docker-compose.yml` com volumes para db e logs.
- **Issue #04+**: Adicionar serviços específicos (collector, ml_pipeline, engine).
