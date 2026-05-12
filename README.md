# FIREWALL INTELIGENTE PARA BLOQUEIO DE CASAS DE APOSTAS

Projeto de TCC para detecção e bloqueio de tráfego relacionado a casas de apostas.

Estrutura inicial do repositório, destinada a facilitar desenvolvimento modular (infra, coleta, ML, motor de firewall).

Como testar:

1. Clone o repositório: `git clone <url>`
2. Verifique a árvore de diretórios: `tree -a` (ou `ls -R`)
3. Crie um diretório `.venv` e rode `git status` — ele deve ser ignorado pelo `.gitignore`.

Diretórios criados (resumo):

- `infra/` — infraestrutura (Docker, compose)
- `src/collector/`, `src/brain/`, `src/engine/` — código fonte modular
- `data/raw/`, `data/processed/` — dados
- `volumes/db/`, `volumes/logs/` — pontos para volumes Docker
- `docs/` — documentação

Próximos passos: adicionar o código inicial em `src/`, configurar pipelines e montar volumes no `docker-compose`.
# FIREWALL-INTELIGENTE-PARA-BLOQUEIO-DE-CASAS-DE-APOSTAS