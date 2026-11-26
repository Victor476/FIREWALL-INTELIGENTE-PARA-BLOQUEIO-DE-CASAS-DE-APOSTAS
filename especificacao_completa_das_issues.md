# 📋 Especificação Completa e Detalhada das Issues do Projeto
**Projeto:** Firewall Inteligente para Bloqueio de Casas de Apostas em Ambientes de Baixos Recursos  
**Documento de Referência:** TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1  
**Versão:** 2.0 (Consolidada com Todas as 58 Issues + Issue #41.1)  
**Status:** Engenharia de Requisitos e Roteiro de Implementação  

## 🏛️ Os 15 Princípios Fundamentais para Criação e Estruturação de Issues
Criar uma issue bem estruturada é a garantia de entrega sem ambiguidades e com reprodutibilidade técnica absoluta. Cada issue deste projeto segue rigorosamente o padrão das 15 características fundamentais:

1. **Título Claro e Conciso com Prefixo:**
   - Sintaxe padronizada: `### **Issue #XX: [Prefixo] Ação e Escopo**`.
   - Prefixos padronizados: `[Infraestrutura]`, `[Ambiente]`, `[Backend]`, `[Frontend]` e `[Documentação]`.

2. **História de Usuário (User Story):**
   - Define o valor e propósito de negócio em formato de citação:
   > **Como** [persona],
   > **eu quero** [funcionalidade/ação],
   > **para que** [benefício/valor mensurável].

3. **Critérios de Aceitação (AC - Gherkin):**
   - Condições de aprovação verificáveis escritas na sintaxe BDD/Gherkin:
   * **Dado que** [contexto inicial], **quando** [ação executada], **então** [resultado técnico esperado].

4. **Exemplo de Requisição (Código/Payload/CLI):**
   - Trecho executável de chamada de terminal, script Python, configuração Dockerfile ou payload JSON com dados reais de teste.

5. **Exemplo de Resposta (Saída esperada / Log de Terminal):**
   - Saída esperada no console ou retorno HTTP/dados comprovando o sucesso ou tratamento formal de exceções.

6. **Componentes Envolvidos:**
   - Mapeamento exato de arquivos de código (`src/`), tabelas de banco, diretórios (`data/`, `volumes/`) ou dependências de sistema afetadas.

7. **Considerações Técnicas e Arquitetura:**
   - Justificativa arquitetural, padrões de projeto, bibliotecas específicas, diretrizes de baixo consumo (limites de RAM/CPU) e vínculos com o TCC.

8. **Mockups ou Referências Visuais:**
   - Diagramas ASCII, layouts de terminal CLI ou tabelas visuais para interfaces e relatórios (quando não aplicável a rotinas puras de backend/infra, marcado explicitamente como N/A).

9. **Dependências e Bloqueios:**
   - **Depende de:** Issues que devem estar concluídas previamente.
   - **Bloqueia:** Issues subsequentes que aguardam esta entrega.

10. **Como Testar (Plano de Teste Passo a Passo):**
    - Roteiro sequencial de validação para o desenvolvedor ou revisor executar no terminal para comprovar o funcionamento.

11. **Definição de Pronto (Definition of Done - DoD):**
    - Critérios de qualidade técnica (testes unitários com Pytest, cobertura mínima, documentação atualizada e ausência de regressões).

12. **Prioridade e Severidade:**
    - Prioridade de negócio/pesquisa (Alta, Média, Baixa) e Severidade técnica (Crítica, Alta, Média).

13. **Etiquetas (Labels):**
    - Tags de categorização para filtros no repositório (`backend`, `infraestrutura`, `machine-learning`, etc.).

14. **Documentação Relacionada:**
    - Vínculos diretos com os Requisitos Funcionais (RF01 a RF11), Requisitos Não Funcionais (RNF01 a RNF08) e Capítulos do TCC.

15. **Estimativa:**
    - Complexidade avaliada em T-Shirt Size (S, M, L) e Story Points (1, 2, 3, 5, 8).

---

## 🎯 Matriz de Requisitos do Sistema e Cenários de Hardware
### Requisitos Funcionais (RF)
* **RF01 - Automação de Coleta:** Módulo Selenium/Playwright para gerar tráfego sintético em casas de apostas e controle.
* **RF02 - Sniffing Passivo:** Captura bruta de pacotes em formato PCAP sem interferir no tráfego original.
* **RF03 - Extração de Atributos:** Conversão de PCAPs em fluxos 5-tupla bidirecionais com $\ge 20$ métricas estatísticas e temporais.
* **RF04 - Redução de Dimensionalidade:** Seleção automática de atributos via algoritmo de Incerteza Simétrica (SU).
* **RF05 - Treinamento de Modelos:** Treinamento isolado de Random Forest (Bagging), XGBoost (Boosting) e Regressão Logística (Linear).
* **RF06 - Persistência de Modelos:** Serialização comprimida (.joblib) para carregamento instantâneo no gateway.
* **RF07 - Lógica de Votação (Hard Voting):** Consenso majoritário onde o bloqueio exige $\ge 2$ votos positivos.
* **RF08 - Integração com Kernel:** Injeção e revogação atômica de regras DROP no Netfilter/iptables.
* **RF09 - Gestão de Listas:** CRUD relacional para Whitelist e Blacklist manual no SQLite.
* **RF10 - Interface Administrativa (CLI):** Comandos de terminal para consulta de status, reload e auditoria.
* **RF11 - Feedback Loop:** Desbloqueio e imunização automática de falsos positivos movendo o IP para a Whitelist.

### Requisitos Não Funcionais (RNF)
* **RNF01 - Latência Crítica:** Tempo total de veredito ($T_{verdict} \le 200ms$) para prevenir condição de corrida contra o TCP.
* **RNF02 - Restrição de Memória RAM:** Consumo do motor do firewall mantido em $\le 512MB$ estáveis.
* **RNF03 - Carga de CPU:** Ocupação de processamento $< 60\%$ em 1 core / 0.5 vCPU para evitar starvation.
* **RNF04 - Vazão de Classificação:** Capacidade mínima de sustentar $\ge 50$ novos fluxos por segundo sem perdas.
* **RNF05 - Isolamento via Docker:** Módulos encapsulados em containers comunicando-se via rede virtual interna.
* **RNF06 - Disponibilidade e Failsafe:** Operação em modo seguro mesmo diante de falha do processo de IA.
* **RNF07 - Persistência de Dados:** Listas e logs armazenados em volumes persistentes.
* **RNF08 - Interpretabilidade de Log:** Cada evento registra timestamp, IP, domínio e votos `[RF, XGB, LR]`.

### Cenários de Hardware Simulados (Seção 3.1.3 do TCC)
* **Cenário A (Referência/Baseline):** Sem restrições de CPU/RAM (teto ideal de acurácia e velocidade).
* **Cenário B (Baixo Recurso):** 0.5 vCPU e 812MB RAM (limite de 512MB para o motor), simulando roteadores domésticos e IoT.
* **Cenário C (Crítico/Saturação):** 0.25 vCPU e 256MB RAM para mapear o ponto de saturação e estresse extremo.

---

## 📑 Índice Geral das Issues por Grupo

### 🏗️ Grupo 1: Infraestrutura e Ambiente Docker
- [Issue #01: [Infraestrutura] Configuração do repositório Git e estrutura de pastas](#issue-01-infraestrutura-configuração-do-repositório-git-e-estrutura-de-pastas)
- [Issue #02: [Infraestrutura] Desenvolvimento do Dockerfile base (Python + Ferramentas de Rede)](#issue-02-infraestrutura-desenvolvimento-do-dockerfile-base-python--ferramentas-de-rede)
- [Issue #03: [Infraestrutura] Configuração do docker-compose.yml (Containers Gateway e App)](#issue-03-infraestrutura-configuração-do-docker-composeyml-containers-gateway-e-app)
- [Issue #04: [Infraestrutura] Implementação do container Gateway/Bridge para interceptação de tráfego](#issue-04-infraestrutura-implementação-do-container-gatewaybridge-para-interceptação-de-tráfego)
- [Issue #05: [Infraestrutura] Configuração de capacidades de rede do kernel no Docker (Net_Admin)](#issue-05-infraestrutura-configuração-de-capacidades-de-rede-do-kernel-no-docker-net_admin)
- [Issue #06: [Infraestrutura] Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy)](#issue-06-infraestrutura-instalação-e-teste-de-ferramentas-de-rede-tcpdump-tshark-scapy)
- [Issue #07: [Infraestrutura] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado](#issue-07-infraestrutura-configuração-de-limites-de-recursos-cpuram-via-docker-para-simular-hardware-limitado)

### 📡 Grupo 2: Coleta e Geração de Dados
- [Issue #08: [Ambiente] Configurar Selenium/Playwright no Docker para Automação de Coleta](#issue-08-ambiente-configurar-seleniumplaywright-no-docker-para-automação-de-coleta)
- [Issue #09: [Backend] Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot](#issue-09-backend-evasão-de-bloqueio-implementar-rotação-de-user-agents-e-técnicas-anti-bot)
- [Issue #10: [Backend] Lógica de Navegação: Criar script que simula comportamento humano](#issue-10-backend-lógica-de-navegação-criar-script-que-simula-comportamento-humano)
- [Issue #11: [Infraestrutura] Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído](#issue-11-infraestrutura-filtro-de-captura-bpf-configurar-filtros-no-tcpdump-para-excluir-ruído)
- [Issue #12: [Backend] Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser)](#issue-12-backend-orquestrador-de-sessão-script-de-sincronia-sniffing--browser)
- [Issue #13: [Backend] Dataset de Apostas: Execução da recolha em massa (Bet365, Betano, etc.)](#issue-13-backend-dataset-de-apostas-execução-da-recolha-em-massa-bet365-betano-etc)
- [Issue #14: [Backend] Dataset Benigno: Execução da recolha de sítios de controlo (YouTube, Notícias)](#issue-14-backend-dataset-benigno-execução-da-recolha-de-sítios-de-controlo-youtube-notícias)
- [Issue #15: [Backend] Validação de Captura: Script para verificar integridade dos PCAPs](#issue-15-backend-validação-de-captura-script-para-verificar-integridade-dos-pcaps)
- [Issue #16: [Backend] Extração de Metadados Brutos: Relatório de volume e duração por captura](#issue-16-backend-extração-de-metadados-brutos-relatório-de-volume-e-duração-por-captura)

### 🧹 Grupo 3: Pré-processamento e Dataset
- [Issue #17: [Backend] Extração de fluxos bi-direcionais (Conversão PCAP para CSV)](#issue-17-backend-extração-de-fluxos-bi-direcionais-conversão-pcap-para-csv)
- [Issue #18: [Backend] Limpeza de dados (Remoção de valores NaN, Inf e duplicatas)](#issue-18-backend-limpeza-de-dados-remoção-de-valores-nan-inf-e-duplicatas)
- [Issue #19: [Backend] Rotulagem das classes (Apostas vs Benigno) e Label Encoding](#issue-19-backend-rotulagem-das-classes-apostas-vs-benigno-e-label-encoding)
- [Issue #20: [Backend] Normalização e padronização de escalas dos dados](#issue-20-backend-normalização-e-padronização-de-escalas-dos-dados)
- [Issue #21: [Backend] Análise estatística exploratória inicial (EDA) do dataset](#issue-21-backend-análise-estatística-exploratória-inicial-eda-do-dataset)
- [Issue #22: [Backend] Balanceamento de classes via técnicas de amostragem (SMOTE)](#issue-22-backend-balanceamento-de-classes-via-técnicas-de-amostragem-smote)
- [Issue #23: [Backend] Divisão do dataset em Treino, Validação e Teste](#issue-23-backend-divisão-do-dataset-em-treino-validação-e-teste)
- [Issue #24: [Backend] Redução de dimensionalidade: Seleção de atributos mínimos via Incerteza Simétrica (SU)](#issue-24-backend-redução-de-dimensionalidade-seleção-de-atributos-mínimos-via-incerteza-simétrica-su)

### 🧠 Grupo 4: Pipeline de Machine Learning
- [Issue #25: [Backend] Implementação da Regressão Logística (Voto de Minerva/Baseline)](#issue-25-backend-implementação-da-regressão-logística-voto-de-minervabaseline)
- [Issue #26: [Backend] Implementação e treinamento do classificador Random Forest](#issue-26-backend-implementação-e-treinamento-do-classificador-random-forest)
- [Issue #27: [Backend] Implementação e treinamento do classificador XGBoost](#issue-27-backend-implementação-e-treinamento-do-classificador-xgboost)
- [Issue #28: [Backend] Implementação do Comitê de Votação Majoritária (Ensemble)](#issue-28-backend-implementação-do-comitê-de-votação-majoritária-ensemble)
- [Issue #29: [Backend] Tuning de hiperparâmetros (Foco em modelos "leves")](#issue-29-backend-tuning-de-hiperparâmetros-foco-em-modelos-leves)
- [Issue #30: [Backend] Avaliação via validação cruzada ($K$-Fold Cross Validation)](#issue-30-backend-avaliação-via-validação-cruzada-k-fold-cross-validation)
- [Issue #31: [Backend] Geração de métricas (Acurácia, F1-Score, Precisão, Recall)](#issue-31-backend-geração-de-métricas-acurácia-f1-score-precisão-recall)
- [Issue #32: [Backend] Exportação do modelo final treinado (pickle/joblib)](#issue-32-backend-exportação-do-modelo-final-treinado-picklejoblib)
- [Issue #33: [Backend] Medição do tamanho em disco e memória dos modelos treinados](#issue-33-backend-medição-do-tamanho-em-disco-e-memória-dos-modelos-treinados)

### 🛡️ Grupo 5: Motor do Firewall e Integração
- [Issue #34: [Infraestrutura/Backend] Script de captura e inspeção de pacotes em tempo real](#issue-34-infraestruturabackend-script-de-captura-e-inspeção-de-pacotes-em-tempo-real)
- [Issue #35: [Backend] Módulo de extração de características de fluxo "em voo" (In-flight features)](#issue-35-backend-módulo-de-extração-de-características-de-fluxo-em-voo-in-flight-features)
- [Issue #36: [Infraestrutura] Integração do script Python com o subsistema de rede (iptables)](#issue-36-infraestrutura-integração-do-script-python-com-o-subsistema-de-rede-iptables)
- [Issue #37: [Backend] Implementação da lógica de decisão: Whitelist → Blacklist → Votação do Comitê](#issue-37-backend-implementação-da-lógica-de-decisão-whitelist--blacklist--votação-do-comitê)
- [Issue #38: [Infraestrutura/Backend] Criação da lógica de execução do bloqueio (DROP)](#issue-38-infraestruturabackend-criação-da-lógica-de-execução-do-bloqueio-drop)
- [Issue #39: [Backend] Implementação de cache de IPs para otimização de performance](#issue-39-backend-implementação-de-cache-de-ips-para-otimização-de-performance)
- [Issue #40: [Backend] Sistema de Logging detalhado de eventos e vereditos](#issue-40-backend-sistema-de-logging-detalhado-de-eventos-e-vereditos)

### 📝 Grupo 6: Gestão de Listas e Moderação
- [Issue #41: [Backend] Modelagem do banco de dados local para Listas (SQLite ou JSON)](#issue-41-backend-modelagem-do-banco-de-dados-local-para-listas-sqlite-ou-json)
- [Issue #41.1: [Backend] Modelagem, Scripts de Migração e Seed do Banco de Dados Local](#issue-411-backend-modelagem-scripts-de-migração-e-seed-do-banco-de-dados-local)
- [Issue #42: [Backend] Desenvolvimento de módulo CRUD para gestão da Whitelist](#issue-42-backend-desenvolvimento-de-módulo-crud-para-gestão-da-whitelist)
- [Issue #43: [Backend] Desenvolvimento de módulo CRUD para gestão da Blacklist Manual](#issue-43-backend-desenvolvimento-de-módulo-crud-para-gestão-da-blacklist-manual)
- [Issue #44: [Backend/Frontend] Implementação de interface CLI para moderação administrativa](#issue-44-backendfrontend-implementação-de-interface-cli-para-moderação-administrativa)
- [Issue #45: [Backend] Criação de mecanismo de "Hot Reload" das listas](#issue-45-backend-criação-de-mecanismo-de-hot-reload-das-listas)
- [Issue #46: [Backend] Lógica de "Feedback Loop": Adicionar falsos positivos à Whitelist via log](#issue-46-backend-lógica-de-feedback-loop-adicionar-falsos-positivos-à-whitelist-via-log)

### 🧪 Grupo 7: Testes, Validação e Eficiência
- [Issue #47: [Backend/Infraestrutura] Teste de latência: Medição do impacto da votação no tempo de resposta](#issue-47-backendinfraestrutura-teste-de-latência-medição-do-impacto-da-votação-no-tempo-de-resposta)
- [Issue #48: [Backend] Teste de Falsos Positivos em sites críticos](#issue-48-backend-teste-de-falsos-positivos-em-sites-críticos)
- [Issue #49: [Infraestrutura] Teste de estresse: Simulação de carga pesada e vazão](#issue-49-infraestrutura-teste-de-estresse-simulação-de-carga-pesada-e-vazão)
- [Issue #50: [Backend] Validação da eficácia comparativa do bloqueio manual vs. bloqueio preditivo da IA](#issue-50-backend-validação-da-eficácia-comparativa-do-bloqueio-manual-vs-bloqueio-preditivo-da-ia)
- [Issue #51: [Infraestrutura] Teste de persistência: Verificação após reinício do container](#issue-51-infraestrutura-teste-de-persistência-verificação-após-reinício-do-container)
- [Issue #52: [Infraestrutura] Benchmark de CPU: Monitoramento do uso de processamento durante a inferência](#issue-52-infraestrutura-benchmark-de-cpu-monitoramento-do-uso-de-processamento-durante-a-inferência)
- [Issue #53: [Infraestrutura] Benchmark de RAM: Monitoramento do footprint de memória do motor de IA](#issue-53-infraestrutura-benchmark-de-ram-monitoramento-do-footprint-de-memória-do-motor-de-ia)
- [Issue #54: [Backend] Geração de matrizes de confusão e gráficos comparativos finais](#issue-54-backend-geração-de-matrizes-de-confusão-e-gráficos-comparativos-finais)

### 📂 Grupo 8: Documentação e Finalização
- [Issue #55: [Infraestrutura/Backend] Refatoração do código e padronização técnica (PEP8)](#issue-55-infraestruturabackend-refatoração-do-código-e-padronização-técnica-pep8)
- [Issue #56: [Documentação] Elaboração do README.md com manual e arquitetura](#issue-56-documentação-elaboração-do-readmemd-com-manual-e-arquitetura)
- [Issue #57: [Infraestrutura] Criação de scripts de configuração automática do laboratório](#issue-57-infraestrutura-criação-de-scripts-de-configuração-automática-do-laboratório)
- [Issue #58: [Documentação] Consolidação final dos resultados (Relatório de Eficiência vs. Acurácia)](#issue-58-documentação-consolidação-final-dos-resultados-relatório-de-eficiência-vs-acurácia)

---


# 🏗️ Grupo 1: Infraestrutura e Ambiente Docker

### **Issue #01: [Infraestrutura] Configuração do repositório Git e estrutura de pastas**

**1. História de Usuário (User Story)**
> Como desenvolvedor do projeto,
> eu quero estabelecer uma estrutura de diretórios organizada e um repositório Git configurado,
> para que o código seja versionado corretamente e os módulos (IA, Coleta, Gateway) fiquem isolados conforme a arquitetura proposta.

**2. Critérios de Aceitação (AC)**
Dado que iniciei o repositório, quando eu criar as pastas, então elas devem seguir a divisão lógica: infra/, data_collection/, ml_pipeline/, firewall_engine/ e docs/.

Dado que o projeto utiliza Python, quando eu configurar o .gitignore, então arquivos temporários, ambientes virtuais (.venv) e arquivos de modelos serializados (.pkl, .joblib) grandes não devem ser rastreados.   

Dado que o projeto exige persistência, quando eu configurar a estrutura, então deve existir um diretório específico para volumes do Docker (volumes/db, volumes/logs).   

**3. Exemplo de Estrutura (Representação de "Requisição")**
Plaintext
/
├── infra/               # Dockerfiles e docker-compose 
├── src/
│   ├── collector/       # Scripts de coleta Selenium/Playwright 
│   ├── brain/           # Modelos e scripts de ML (RF, XGBoost, LR) 
│   └── engine/          # Motor do firewall e integração iptables 
├── data/
│   ├── raw/             # Arquivos PCAP brutos 
│   └── processed/       # Datasets CSV limpos 
├── docs/                # Documentação e relatórios 
└── .gitignore
**4. Exemplo de Saída Esperada (Response)**
Repositório remoto criado no GitHub/GitLab.

Primeiro commit realizado com a estrutura base.

Arquivo README.md inicial descrevendo o propósito do projeto.   

**5. Componentes Envolvidos**
Git / GitHub.

Sistema de Arquivos do Linux (Host).

Docker (Estrutura para volumes persistentes).   

**6. Considerações Técnicas**
Seguir o padrão PEP8 para a nomeação de pastas e arquivos Python.   

Configurar proteção de branch main (opcional, mas recomendado).

Garantir que a pasta de logs e base de dados (SQLite/JSON) esteja preparada para ser montada como volume.   

**7. Dependências e Bloqueios**
Bloqueia: Todas as demais issues de desenvolvimento (Issue #02 em diante).

**8. Como Testar**
Clonar o repositório em uma nova pasta: git clone <url>.

Verificar se a árvore de diretórios está completa usando o comando tree.

Tentar adicionar um arquivo .venv e verificar se o git status o ignora corretamente.

**9. Definição de Pronto (DoD)**
Estrutura de pastas criada e commitada.

.gitignore configurado adequadamente.

README.md inicial presente com o título oficial do TCC.   

**10. Prioridade e Severidade**
Prioridade: Alta (Bloqueante).

Severidade: Crítica (Base do projeto).

**11. Etiquetas (Labels)**
infra, documentation, setup.

**12. Documentação Relacionada**
Relatório de requisitos (RNF05, RNF07).   

Capítulo 3.1 do documento do TCC.   

**13. Estimativa**
T-Shirt Size: S (Small) / 1-2 Story Points.

---

### **Issue #02: [Infraestrutura] Desenvolvimento do Dockerfile base (Python + Ferramentas de Rede)**
**1. História de Usuário (User Story)**
> Como desenvolvedor do sistema,
> eu quero uma imagem Docker padronizada com Python e ferramentas de rede pré-instaladas,
> para que o ambiente de execução seja idêntico entre o desenvolvimento e o laboratório de testes, evitando o erro "funciona na minha máquina".

**2. Critérios de Aceitação (AC)**
Dado que estou construindo a imagem, quando o processo finalizar, então ferramentas essenciais (tcpdump, tshark, iproute2, net-tools) devem estar disponíveis no PATH.

Dado que o projeto utiliza bibliotecas de ML, quando instalar as dependências, então a imagem deve conter os compiladores necessários (gcc, g++) e o pip atualizado.

Dado que temos restrições de hardware (RNF02), quando a imagem for gerada, então deve-se utilizar uma base leve (ex: python:3.10-slim) para minimizar o footprint de disco e memória.

**3. Exemplo de Requisição (Trecho do Dockerfile)**
Dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    tcpdump \
    tshark \
    iproute2 \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*
**4. Exemplo de Resposta (Log de Build)**
Step 5/10 : RUN pip install -r requirements.txt

Successfully built <image_id>

Successfully tagged firewall-base:latest

**5. Componentes Envolvidos**
Docker Engine.

Repositório de pacotes Debian (Bullseye/Bookworm).

Kernel Linux (capacidades de captura de pacotes).

**6. Considerações Técnicas**
Utilizar multi-stage builds se necessário para reduzir o tamanho final.

Configurar o ENV PYTHONUNBUFFERED=1 para garantir que os logs do firewall apareçam em tempo real no console do Docker.

Garantir permissões de execução para o tcpdump sem necessidade de root total (usando setcap).

**7. Dependências e Bloqueios**
Depende de: Issue #01 (Estrutura de pastas para salvar o Dockerfile).

Bloqueia: Issue #03 (Configuração do docker-compose).

**8. Como Testar**
Executar o build: docker build -t firewall-test ..

Rodar o container: docker run -it firewall-test bash.

Dentro do container, executar tcpdump --version e python --version. Ambos devem retornar a versão instalada.

**9. Definição de Pronto (DoD)**
Dockerfile presente na pasta infra/.

Imagem buildando sem erros.

requirements.txt inicial (mesmo que vazio ou só com scapy) criado.

**10. Prioridade e Severidade**
Prioridade: Alta.

Severidade: Média (Impacta a portabilidade).

**11. Etiquetas (Labels)**
infra, docker, python.

**12. Documentação Relacionada**
RNF02 (Restrição de Memória RAM).

RNF05 (Isolamento via Docker).

**13. Estimativa**
T-Shirt Size: M (Medium).

**14. Exemplo de Requisição (Instalação de Dependências)**
pip install scapy pandas scikit-learn xgboost joblib

**15. Componentes Envolvidos**
Sistema Operacional (Debian Slim).

Python Runtime.

---

### **Issue #03: [Infraestrutura] Configuração do docker-compose.yml (Containers Gateway e App)**
**1. História de Usuário (User Story)**
> Como desenvolvedor/pesquisador do projeto,
> eu quero um arquivo docker-compose.yml que orquestre os containers do Gateway (Firewall) e da Aplicação (Agente de Navegação) em uma rede virtual isolada,
> para que todo o tráfego gerado pela aplicação passe obrigatoriamente pelo gateway antes de atingir a internet externa.

**2. Critérios de Aceitação (AC)**
Dado que os containers são iniciados com docker-compose up, quando subirem, então eles devem se conectar a uma rede bridge interna dedicada.

Dado que o container Gateway precisa rotear e interceptar tráfego, quando for instanciado, então deve ser iniciado com permissões e capacidades de rede adequadas no kernel (NET_ADMIN).

Dado que a aplicação depende do gateway para sair para a internet, quando o serviço do cliente subir, então a rota padrão de rede (default gateway) deve ser direcionada para o IP do container Gateway.

Dado que o sistema requer persistência de dados, quando os containers forem reiniciados, então os dados de logs e bancos de dados locais mantidos em volumes montados devem permanecer intactos.

**3. Exemplo de Requisição (Trecho da Estrutura do docker-compose.yml)**
YAML
version: '3.8'

networks:
  firewall_net:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

services:
  gateway:
    build:
      context: ..
      dockerfile: infra/Dockerfile
    container_name: gateway_firewall
    cap_add:
      - NET_ADMIN
    networks:
      firewall_net:
        ipv4_address: 172.20.0.254
    volumes:
      - ../volumes/logs:/app/logs
      - ../volumes/db:/app/db
    sysctls:
      - net.ipv4.ip_forward=1

  app_client:
    build:
      context: ..
      dockerfile: infra/Dockerfile
    container_name: app_client
    cap_add:
      - NET_ADMIN
    networks:
      firewall_net:
        ipv4_address: 172.20.0.10
    depends_on:
      - gateway
**4. Exemplo de Resposta (Saída Esperada no Terminal)**
Plaintext
[+] Running 3/3
 ✔ Network infra_firewall_net Created
 ✔ Container gateway_firewall Created
 ✔ Container app_client       Created
**5. Componentes Envolvidos**
Docker Compose CLI.

Submódulo de Rede do Docker (Bridge Networks).

Kernel Linux Host (Driver de rede e sysctl ip_forward).

**6. Considerações Técnicas**
Habilitar net.ipv4.ip_forward=1 no gateway para autorizar o roteamento de pacotes.

Definir endereçamento IP estático dentro da subnet virtual para garantir estabilidade nas rotas de teste.

Garantir o isolamento do ambiente em compliance com o requisito de arquitetura RNF05.

**7. Dependências e Bloqueios**
Depende de: Issue #01 (Estrutura de diretórios para volumes) e Issue #02 (Dockerfile base).   

Bloqueia: Issue #04 (Implementação do container Gateway/Bridge) e Issue #05 (Configuração de Net_Admin).

**8. Como Testar**
Executar o comando na pasta infra/: docker-compose up -d.

Verificar o status dos containers com docker-compose ps.

Executar docker exec -it app_client ping -c 2 172.20.0.254 para validar a conectividade direta entre a aplicação e o gateway.

**9. Definição de Pronto (DoD)**
Arquivo infra/docker-compose.yml versionado no repositório.

Rede bridge criada e conectividade básica testada entre os containers.

Mapeamento de volumes de persistência funcionando perfeitamente.

**10. Prioridade e Severidade**
Prioridade: Alta (Bloqueante para o ambiente de rede).

Severidade: Alta.

**11. Etiquetas (Labels)**
infraestrutura, docker, docker-compose, networking.

**12. Documentação Relacionada**
RNF05 (Isolamento via Docker).

RNF07 (Persistência de Dados).

Capítulo 3.1.1 (Topologia do Laboratório Central).

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #04: [Infraestrutura] Implementação do container Gateway/Bridge para interceptação de tráfego**
**1. História de Usuário (User Story)**
> Como desenvolvedor/pesquisador do projeto,
> eu quero configurar o container Gateway como o ponto único de saída e roteamento da rede,
> para que todo o tráfego gerado pelo Agente de Navegação seja interceptado, inspecionado e potencialmente descartado via regras de kernel.

**2. Critérios de Aceitação (AC)**
Dado que o container app_client tenta acessar a internet, quando os pacotes saírem da rede local, então eles devem obrigatoriamente passar pela interface interna do gateway_firewall (FORWARD chain).

Dado que o Gateway precisa mascarar a rede interna, quando um pacote for encaminhado para a internet, então a regra de NAT/MASQUERADE do iptables deve traduzir o endereço de origem no espaço de kernel.

Dado que o tráfego do app_client é redirecionado, quando a rota padrão for alterada, então o IP do Gateway (172.20.0.254) deve responder como default gateway ativo da máquina cliente.

**3. Exemplo de Requisição (Script de Inicialização do Gateway / entrypoint.sh)**
Bash
#!/bin/bash
# Habilita roteamento no Kernel
sysctl -w net.ipv4.ip_forward=1

# Limpa regras prévias
iptables -F
iptables -t nat -F

# Configura NAT para tráfego que sai para a internet
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Mantém o container ativo
exec "$@"
**4. Exemplo de Resposta (Saída Esperada no Cliente)**
Plaintext
$ docker exec -it app_client ip route
default via 172.20.0.254 dev eth0 
172.20.0.0/16 dev eth0 proto kernel scope link src 172.20.0.10
**5. Componentes Envolvidos**
Subsistema Netfilter / iptables (Tabelas nat e filter).

Módulo Conntrack do Kernel Linux.

Módulo de Roteamento IP (iproute2).

**6. Considerações Técnicas**
Garantir o uso da diretiva FORWARD para interceptação de pacotes entre interfaces de rede virtuais distintas.

Evitar que o script de entrypoint encerre imediatamente, mantendo o processo principal rodando em primeiro plano.

Garantir que a perda de conexões não derrube o container (estabilidade operacional).

**7. Dependências e Bloqueios**
Depende de: Issue #03 (docker-compose.yml base).

Bloqueia: Issue #05 (Recursos NET_ADMIN) e Issue #06 (Testes com tcpdump/scapy).

**8. Como Testar**
Iniciar o laboratório com docker-compose up -d.

Executar um traceroute no cliente: docker exec -it app_client traceroute 8.8.8.8.

Validar se o primeiro salto da rota é obrigatoriamente o IP 172.20.0.254 (Gateway).

Rodar ping google.com no app_client para confirmar se a conectividade com a internet externa está funcional via NAT.

**9. Definição de Pronto (DoD)**
Script de inicialização da rede do Gateway versionado.

Tráfego do container cliente roteado com sucesso através do Gateway.

Regras de NAT (MASQUERADE) operacionais.

**10. Prioridade e Severidade**
Prioridade: Alta (Bloqueante).

Severidade: Crítica.

**11. Etiquetas (Labels)**
infraestrutura, networking, iptables, gateway.

**12. Documentação Relacionada**
Seção 2.6 (Subsistema Netfilter e Arquitetura do iptables).

Seção 3.1.1 (Topologia de Rede Virtualizada via Docker).

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #05: [Infraestrutura] Configuração de capacidades de rede do kernel no Docker (Net_Admin)**
**1. História de Usuário (User Story)**
> Como desenvolvedor/pesquisador do projeto,
> eu quero conceder a capacidade CAP_NET_ADMIN e acesso ao dispositivo /dev/net/tun aos containers,
> para que os módulos Python consigam manipular tabelas do iptables, abrir sockets brutos (raw sockets) e injetar/descartar pacotes no nível de kernel sem precisar rodar em modo totalmente privilegiado.

**2. Critérios de Aceitação (AC)**
Dado que o container Gateway precisa executar comandos do iptables, quando o motor de inferência tentar adicionar uma regra DROP, então o comando deve ser executado sem o erro Permission denied (you must be root).

Dado que o módulo de inspeção utiliza a biblioteca Scapy ou tcpdump, quando o escutador de pacotes iniciar, então ele deve conseguir colocar a interface de rede em modo promíscuo.

Dado que a segurança e o isolamento devem ser mantidos, quando concedermos privilégios, então devemos usar a instrução restrita cap_add: - NET_ADMIN no lugar da flag genérica e insegura --privileged.

**3. Exemplo de Requisição (Trecho de Ajuste no docker-compose.yml)**
YAML
services:
  gateway:
    image: firewall-base:latest
    container_name: gateway_firewall
    cap_add:
      - NET_ADMIN
      - NET_RAW
    devices:
      - /dev/net/tun:/dev/net/tun
**4. Exemplo de Resposta (Execução bem-sucedida sem erro de permissão)**
Plaintext
$ docker exec -it gateway_firewall iptables -A FORWARD -s 172.20.0.10 -j DROP
$ docker exec -it gateway_firewall iptables -L FORWARD -n -v
Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  *      *       172.20.0.10          0.0.0.0/0           
**5. Componentes Envolvidos**
Linux Capabilities (capabilities(7) no Kernel Linux).

Docker Daemon (Engine Security Controls).   

Submódulo iptables e raw sockets do espaço de usuário.

**6. Considerações Técnicas**
Adicionar NET_RAW explicitamente para garantir que a Scapy consiga ler os cabeçalhos de camada 2/3 diretamente da interface.

Evitar o uso do parâmetro --privileged=true, pois viola o princípio de privilégio mínimo e expõe o host.

**7. Dependências e Bloqueios**
Depende de: Issue #03 (docker-compose.yml base).   

Bloqueia: Issue #06 (Instalação e teste de ferramentas de rede) e Issue #36 (Integração do script com iptables).

**8. Como Testar**
Subir o ambiente com docker-compose up -d.   

Tentar inserir uma regra de teste no container do Gateway:

docker exec gateway_firewall iptables -A INPUT -p icmp -j DROP.

Tentar capturar um pacote usando o Scapy em Python no container:

docker exec gateway_firewall python3 -c "from scapy.all import sniff; print(sniff(count=1))".

Ambos os comandos devem ser executados com sucesso, sem lançar erros de permissão de sistema do tipo Operation not permitted.

**9. Definição de Pronto (DoD)**
Mapeamento de cap_add atualizado e versionado no arquivo docker-compose.yml.   

Injeção de regras de iptables e sniffing com Scapy funcionando perfeitamente sem o modo privilegiado total.

**10. Prioridade e Severidade**
Prioridade: Alta.

Severidade: Crítica (A IA não conseguirá aplicar os bloqueios se esta issue falhar).

**11. Etiquetas (Labels)**
infraestrutura, docker, security, kernel, capabilities.

**12. Documentação Relacionada**
Requisito RF08 (Integração com Kernel / Netfilter).

Requisito RNF05 (Isolamento via Docker).

Capítulo 3.1.2 do TCC (Camadas de Defesa e Subsistemas).

**13. Estimativa**
T-Shirt Size: S (Small) / 2 Story Points.

---

### **Issue #06: [Infraestrutura] Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy)**
**1. História de Usuário (User Story)**
> Como desenvolvedor/pesquisador do projeto,
> eu quero validar o funcionamento e a comunicação das ferramentas de análise e captura de pacotes (tcpdump, tshark e Scapy) dentro dos containers,
> para que os módulos de extração de características em tempo real e de gravação de arquivos PCAP operem sem erros de runtime ou dependências faltantes.

**2. Critérios de Aceitação (AC)**
Dado que o container Gateway está ativo, quando o tcpdump for executado via CLI, então ele deve capturar o tráfego da interface virtual (eth0) e gerar um arquivo .pcap válido.   

Dado que o tshark e a biblioteca Pyshark são utilizados no ecossistema Python, quando acionados, então eles devem conseguir ler e dissecar arquivos PCAP sem falhar por ausência do binário do Wireshark/Tshark.   

Dado que o módulo de sniffing utilizará a Scapy, quando um script Python chamar a função sniff(), então os pacotes de rede devem ser interceptados e convertidos em objetos manipuláveis em tempo real.

**3. Exemplo de Requisição (Script Python de Validação de Inspeção / test_network_tools.py)**
Python
import os
from scapy.all import sniff, IP

def packet_callback(pkt):
    if pkt.haslayer(IP):
        print(f"[OK] Pacote Interceptado: {pkt[IP].src} -> {pkt[IP].dst}")

print("Iniciando teste de captura com Scapy...")
# Captura 3 pacotes na interface padrao
sniff(count=3, prn=packet_callback, timeout=10)

# Valida chamada do tshark no sistema
exit_code = os.system("tshark -v > /dev/null 2>&1")
if exit_code == 0:
    print("[OK] Tshark instalado e acessível no PATH.")
**4. Exemplo de Resposta (Saída Esperada no Terminal do Container)**
Plaintext
Iniciando teste de captura com Scapy...
[OK] Pacote Interceptado: 172.20.0.10 -> 8.8.8.8
[OK] Pacote Interceptado: 8.8.8.8 -> 172.20.0.10
[OK] Pacote Interceptado: 172.20.0.10 -> 1.1.1.1
[OK] Tshark instalado e acessível no PATH.
**5. Componentes Envolvidos**
Binários do Sistema: tcpdump, tshark.   

Bibliotecas Python: scapy, pyshark.   

Libpcap (Biblioteca nativa C do Linux para captura de pacotes).

**6. Considerações Técnicas**
Adicionar a dependência do tshark no Dockerfile garantindo a flag DEBIAN_FRONTEND=noninteractive para evitar travamentos de prompt interativo sobre permissões do Wireshark durante o build.

Garantir que a Scapy utilize a interface correta configurando explicitamente a variável de interface conf.iface = 'eth0' nos scripts Python.

**7. Dependências e Bloqueios**
Depende de: Issue #02 (Dockerfile base) e Issue #05 (Recursos NET_ADMIN / NET_RAW).   

Bloqueia: Issue #11 (Filtro BPF) e Issue #34 (Script de captura e inspeção de pacotes em tempo real).   

**8. Como Testar**
Acessar o container Gateway: docker exec -it gateway_firewall bash.

Rodar uma captura rápida de 5 segundos via CLI: tcpdump -i eth0 -c 5 -w /tmp/test.pcap.

Validar o arquivo gerado via tshark: tshark -r /tmp/test.pcap.

Executar o script Python de validação python3 test_network_tools.py e garantir retorno com status código 0.

**9. Definição de Pronto (DoD)**
Ferramentas tcpdump, tshark e scapy instaladas e totalmente operacionais na imagem Docker.   

Script de teste/sanidade das ferramentas de rede criado no repositório.

Captura de pacotes via código Python funcionando sem lançar exceções do SO.

**10. Prioridade e Severidade**
Prioridade: Média.

Severidade: Alta (Falhas aqui impedem o desenvolvimento do motor do firewall).

**11. Etiquetas (Labels)**
infraestrutura, networking, scapy, tcpdump, tshark.

**12. Documentação Relacionada**
Requisito RF02 (Sniffing Passivo).

Capítulo 3.1.2 do TCC (Módulo de Detecção - IDS Passivo).

**13. Estimativa**
T-Shirt Size: S (Small) / 2 Story Points.

Avançamos para a Issue #07: [Infraestrutura] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado?

---

### **Issue #07: [Infraestrutura] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado**
**1. História de Usuário (User Story)**
> Como pesquisador do projeto,
> eu quero impor restrições estritas de hardware (cgroups de CPU e Memória RAM) no container do Gateway Inteligente via Docker Compose,
> para que o ambiente simule com precisão um dispositivo de rede de baixo custo (Cenários B e C do TCC) e viabilize a avaliação de footprint e latência sob escassez de recursos.

**2. Critérios de Aceitação (AC)**
Dado que o container gateway_firewall é iniciado, quando executado no Cenário B (Baixo Recurso), então a alocação de memória RAM deve ser limitada a exatamente 812 MB e a capacidade de processamento a 0.5 vCPU.

Dado que o sistema atinge o teto de recursos, quando o consumo exceder a cota de memória estipulada, então o comportamento do container deve ser monitorado para identificar potenciais riscos de estabilidade sem afetar o host.

Dado que o projeto exige testes em múltiplos cenários (Referência, Baixo Recurso e Crítico), quando alterarmos as variáveis de ambiente do Compose, então os limites de CPU e RAM devem se aplicar dinamicamente sem necessidade de reescrever a estrutura principal das issues.

**3. Exemplo de Requisição (Trecho do docker-compose.yml com deploy.resources)**
YAML
services:
  gateway:
    image: firewall-base:latest
    container_name: gateway_firewall
    deploy:
      resources:
        limits:
          cpus: '${CPU_LIMIT:-0.5}'
          memory: '${RAM_LIMIT:-812M}'
        reservations:
          cpus: '0.1'
          memory: '128M'
**4. Exemplo de Resposta (Inspecção via docker stats)**
Plaintext
CONTAINER ID   NAME               CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
a1b2c3d4e5f6   gateway_firewall   12.4%     145.2MiB / 812MiB     17.88%    1.2kB / 850B

**5. Componentes Envolvidos**
Control Groups do Kernel Linux (cgroups v1/v2).

Engine e Swarm/Deploy Parser do Docker.

CLI de Instrumentação (docker stats / cgroup metrics).

**6. Considerações Técnicas**
Garantir que as diretivas de recursos sejam compatíveis com a execução via docker-compose v2+ (usando a flag --compatibility se necessário em versões antigas).

Mapear o comportamento do processo Python sob restrição de CPU para evitar que threads de sniffing sofram starvation (fome de recursos).

**7. Dependências e Bloqueios**
Depende de: Issue #03 (docker-compose.yml base) e Issue #05 (Permissões de rede do kernel).   

Bloqueia: Issue #33 (Medição do tamanho e footprint) e Issue #52/#53 (Benchmarks de CPU e RAM).   

**8. Como Testar**
Configurar os limites de teste no arquivo .env ou direto no docker-compose.yml (ex: CPU_LIMIT=0.5, RAM_LIMIT=812M).

Subir o ambiente: docker-compose up -d.   

Executar o monitoramento nativo em um terminal paralelo: docker stats gateway_firewall.

Validar se a coluna LIMIT exibe exatamente 812MiB e se o limite de CPU é respeitado durante um estresse numérico simples em Python.

**9. Definição de Pronto (DoD)**
Mapeamento de limite de cgroups de CPU e RAM aplicado no arquivo infra/docker-compose.yml.   

Parâmetros parametrizáveis via arquivo de variáveis de ambiente (.env).

Validação do teto de consumo confirmada através do comando docker stats.

**10. Prioridade e Severidade**
Prioridade: Alta (Essencial para a metodologia do TCC).

Severidade: Alta.

**11. Etiquetas (Labels)**
infraestrutura, docker, cgroups, benchmarking, performance.

**12. Documentação Relacionada**
Requisito RNF02 (Restrição de Memória RAM - 512MB/812MB).

Requisito RNF03 (Carga de CPU - limite de 60% em 1 core).

Capítulo 3.1.3 do TCC (Metodologia de Restrição de Recursos - Cenários A, B e C).

**13. Estimativa**
T-Shirt Size: S (Small) / 2 Story Points.

---

# 📡 Grupo 2: Coleta e Geração de Dados

### **Issue #08: [Ambiente] Configurar Selenium/Playwright no Docker para Automação de Coleta**
**1. História de Usuário (User Story)**
> Como pesquisador do projeto,
> eu quero disponibilizar um ambiente conteinerizado com Selenium ou Playwright configurado em modo headless,
> para que os scripts de automação consigam acessar plataformas de apostas e domínios de controle de forma programática, gerando tráfego sintético para o dataset.

**2. Critérios de Aceitação (AC)**
Dado que o container app_client executa um script de navegação, quando o navegador headless for acionado, então ele deve renderizar a página sem depender de interface gráfica física (X11 display).

Dado que navegadores modernos exigem drivers específicos, quando o container for instanciado, então o binário do Chromium/Chrome e o WebDriver correspondente devem estar instalados e sincronizados na mesma versão.

Dado que o tráfego gerado deve ser inspecionado pelo gateway, quando as requisições HTTP/HTTPS forem abertas pelo browser, então elas devem sair pela interface de rede do container cliente roteada pelo gateway do laboratório.

**3. Exemplo de Requisição (Script de Teste de Coleta / test_browser_headless.py)**
Python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=options)
driver.get("https://example.com")
page_title = driver.title
print(f"[OK] Navegação concluída com sucesso. Título da página: {page_title}")
driver.quit()
**4. Exemplo de Resposta (Saída Esperada no Terminal do Container)**
Plaintext
[OK] Navegação concluída com sucesso. Título da página: Example Domain

**5. Componentes Envolvidos**
Container app_client (Agente de Navegação).

Ferramenta de automação: Selenium WebDriver ou Playwright.   

Binários do Navegador: Chromium / Google Chrome headless.

Driver de automação: ChromeDriver.

**6. Considerações Técnicas**
Adicionar os parâmetros --no-sandbox e --disable-dev-shm-usage para evitar quebras por restrição do tamanho padrão da memória compartilhada (/dev/shm) em containers Docker.

Garantir que as fontes (fonts-liberation, fonts-noto) estejam instaladas no sistema operacional base do container para evitar falhas de carregamento de páginas pesadas.

Fixar a versão do driver para prevenir incompatibilidades automáticas durante novas compilações da imagem.

**7. Dependências e Bloqueios**
Depende de: Issue #03 (docker-compose.yml com o container cliente) e Issue #04 (Roteamento via Gateway operacional).   

Bloqueia: Issue #09 (Evasão de Bloqueio via User-Agents), Issue #10 (Lógica de Navegação que simula comportamento humano), Issue #13 (Coleta de Apostas) e Issue #14 (Coleta Benigna).   

**8. Como Testar**
Acessar o container do cliente: docker exec -it app_client bash.

Executar o script de sanidade: python3 -m src.collector.test_browser_headless.

Validar se a página foi acessada sem levantar exceções de display ou de falta de driver.

Confirmar que a requisição gerada foi roteada e interceptada na interface do gateway executando simultaneamente tcpdump -i eth0 host <ip_externo> no container gateway_firewall.   

**9. Definição de Pronto (DoD)**
Dependências do navegador e bibliotecas Python (selenium ou playwright) instaladas na imagem do cliente.   

Script de validação executado com retorno de status code 0.

Tráfego de navegação sintética saindo comprovadamente pelo container Gateway.

**10. Prioridade e Severidade**
Prioridade: Alta (Bloqueante para o Grupo 2 de coleta).   

Severidade: Alta.

**11. Etiquetas (Labels)**
ambiente, docker, selenium, playwright, data-collection.   

**12. Documentação Relacionada**
Requisito RF01 (Automação de Coleta).

Requisito RNF05 (Isolamento via Docker).

Capítulo 3.1.1 do TCC (Topologia do Laboratório Central e Agente de Navegação).

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #09: [Backend] Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot**
**1. História de Usuário (User Story)**
> Como pesquisador do projeto,
> eu quero integrar mecanismos de evasão contra sistemas de deteção de automação (rotação de User-Agents, remoção de assinaturas webdriver e cabeçalhos realistas) nos scripts de recolha,
> para que as plataformas de apostas online não bloqueiem o tráfego sintético através de desafios como Cloudflare ou Captchas, assegurando uma recolha contínua e sem viés.

**2. Critérios de Aceitação (AC)**
Dado que o navegador automatizado inicia uma nova sessão de recolha, quando a ligação for aberta, então o cabeçalho User-Agent deve ser selecionado aleatoriamente a partir de um conjunto diversificado de dispositivos e versões reais de navegadores.   

Dado que plataformas de apostas utilizam verificações em JavaScript, quando a propriedade navigator.webdriver for consultada pelo sítio, então o seu valor deve retornar undefined ou false.   

Dado que requisições HTTP automáticas possuem padrões estáticos de cabeçalhos, quando as requisições forem disparadas, então atributos como Accept-Language, Sec-Ch-Ua e dimensões de viewport devem ser configurados de forma verosímil.   

**3. Exemplo de Requisição (Módulo Python de Configuração Anti-Deteção / stealth_config.py)**
Python
import random
from selenium.webdriver.chrome.options import Options

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]

def get_stealth_options() -> Options:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return options
**4. Exemplo de Resposta (Validação em Sítio de Teste Anti-Bot)**
Plaintext
$ python3 -m src.collector.verify_stealth
[OK] User-Agent ativo: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
[OK] navigator.webdriver detetado como FALSO/INEXISTENTE.
[OK] Acesso ao portal de teste concluído sem desafios de verificação (Captcha/WAF).

**5. Componentes Envolvidos**
Container app_client (Agente de Navegação).   

Biblioteca de suporte (ex: selenium-stealth ou playwright-stealth).

Conjunto de dados de cabeçalhos e User-Agents parametrizados.   

**6. Considerações Técnicas**
Avaliar o uso de extensões leves ou da biblioteca selenium-stealth para mascarar variáveis internas do objeto window.navigator e assinaturas WebGL/Canvas.   

Evitar reutilizar o mesmo User-Agent em fluxos consecutivos prolongados para não gerar assinaturas comportamentais redundantes.   

Assegurar que os cabeçalhos não alterem o padrão estatístico volumétrico dos fluxos de transporte da camada inferior de forma drástica.   

**7. Dependências e Bloqueios**
Depende de: Issue #08 (Ambiente de automação com Selenium/Playwright).   

Bloqueia: Issue #10 (Lógica de Navegação que simula comportamento humano) e Issue #13 (Recolha em massa do dataset de apostas).   

**8. Como Testar**
Executar o script no container do cliente acedendo a um serviço de verificação pública (como bot.sannysoft.com ou nowsecure.nl):

docker exec -it app_client python3 -m src.collector.verify_stealth.

Validar se o atributo WebDriver (New) e WebDriver Advanced indicam ausência de sinalização automática.   

Executar o script três vezes seguidas e confirmar que o User-Agent é alternado dinamicamente a cada execução.   

**9. Definição de Pronto (DoD)**
Módulo de configuração de propriedades stealth e gerador de User-Agents implementado no repositório.   

Testes em páginas de validação anti-bot executados com sucesso dentro do container Docker.   

Integração garantida com o fluxo padrão de inicialização de navegadores da recolha.   

**10. Prioridade e Severidade**
Prioridade: Alta (Sem técnicas de evasão, as casas de apostas bloqueiam a recolha rapidamente).   

Severidade: Alta.

**11. Etiquetas (Labels)**
backend, automation, web-scraping, anti-bot, data-collection.   

**12. Documentação Relacionada**
Requisito RF01 (Automação de Coleta).   

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #10: [Backend] Lógica de Navegação: Criar script que simula comportamento humano**
**1. História de Usuário (User Story)**
> Como pesquisador do projeto,
> eu quero um script automatizado que emule padrões de interação humana (rolagem de página com pausas aleatórias, movimentação de cursor, cliques em elementos e tempos de permanência variáveis),
> para que os fluxos de rede gerados reflitam o tráfego interativo real em vez de requisições mecânicas em lote, preservando a assinatura estatística e temporal de sessões de navegação.

**2. Critérios de Aceitação (AC)**
Dado que o navegador acessa uma URL alvo, quando a página carregar, então o script deve executar rolagem gradual (smooth scrolling) com pausas em intervalos aleatórios (ex: entre 1 e 4 segundos).   

Dado que plataformas de apostas e portais de mídia mantêm conexões persistentes (websockets ou requisições assíncronas), quando o bot estiver em uma página, então ele deve permanecer ativo por um tempo determinado (ex: 30 a 90 segundos) permitindo atualizações de dados em segundo plano.   

Dado que o script interage com os elementos da tela, quando encontrar links ou abas navegáveis, então ele deve realizar cliques eventuais com desvios aleatórios para mimetizar a exploração de páginas.   

**3. Exemplo de Requisição (Módulo Python de Interação Humana / human_behavior.py)**
Python
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def simulate_human_session(driver, url: str, duration_seconds: int = 45):
    driver.get(url)
    actions = ActionChains(driver)
    start_time = time.time()
    
    while time.time() - start_time < duration_seconds:
        # Rolagem gradual com deslocamentos aleatorios
        scroll_step = random.randint(200, 600)
        driver.execute_script(f"window.scrollBy({{top: {scroll_step}, behavior: 'smooth'}});")
        time.sleep(random.uniform(1.2, 3.5))
        
        # Simulacao de pausas para leitura ou analise de cotacoes/conteudo
        if random.random() < 0.3:
            time.sleep(random.uniform(2.0, 5.0))
            
    print(f"[OK] Sessao interativa concluida para {url} ({duration_seconds}s decorridos).")
**4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)**
Plaintext
[INFO] Acessando plataforma alvo: https://bet365.com...
[INFO] Emulando navegacao humana (scroll, hover, delay)...
[OK] Sessao interativa concluida para https://bet365.com (45s decorridos).

**5. Componentes Envolvidos**
Container app_client (Agente de Navegação).   

Drivers de automação (Selenium/Playwright).   

Camada de aplicação do navegador Chromium/Chrome headless.   

**6. Considerações Técnicas**
Utilizar distribuições estatísticas contínuas (ex: funções gaussianas ou distribuições uniformes com ruído) para determinar os tempos de espera entre ações.   

Controlar o tempo de vida da sessão para evitar que loops infinitos ou elementos bloqueantes travem o orquestrador de coleta.   

Não realizar cliques em elementos sensíveis (como tentativas de depósitos ou submissão de formulários vazios com validação rígida) para não disparar bloqueios perimetrais.   

**7. Dependências e Bloqueios**
Depende de: Issue #08 (Ambiente Selenium/Playwright no Docker) e Issue #09 (Evasão Anti-Bot e Rotação de User-Agents).   

Bloqueia: Issue #12 (Orquestrador de Sessão), Issue #13 (Dataset de Apostas) e Issue #14 (Dataset Benigno).   

**8. Como Testar**
Executar o script de teste de comportamento dentro do container de navegação:

docker exec -it app_client python3 -m src.collector.human_behavior.

Verificar se a navegação permanece ativa durante o tempo configurado (ex: 45 segundos) sem lançar falhas de execução.   

Conferir na interface de rede se os pacotes continuam sendo transmitidos em fluxo contínuo ao longo da sessão interativa.   

**9. Definição de Pronto (DoD)**
Módulo de emulação de comportamento humano implementado e integrado aos scripts de navegação.   

Teste de sessão de navegação longa finalizado com sucesso dentro do container.   

Logs de execução registrando os intervalos e ações simuladas.   

**10. Prioridade e Severidade**
Prioridade: Alta (Garante a verossimilhança dos metadados temporais do tráfego).   

Severidade: Alta.

**11. Etiquetas (Labels)**
backend, automation, data-collection, selenium.   

**12. Documentação Relacionada**
Requisito RF01 (Automação de Coleta).   

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   

Capítulo 3.2.2 do TCC (Engenharia de Atributos Baseada em Fluxos).   

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #11: [Infraestrutura] Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído**
**1. História de Usuário (User Story)**
> Como investigador do projeto,
> eu quero definir e parametrizar expressões de filtro BPF (Berkeley Packet Filter) no comando de captura do tcpdump,
> para que apenas o tráfego relevante para a análise seja gravado nos ficheiros PCAP, descartando ruídos operacionais internos da rede Docker e transmissões irrelevantes.

**2. Critérios de Aceitação (AC)**
Dado que o tcpdump está em execução no contentor Gateway, quando iniciar a escuta, então deve excluir tráfego de resolução ARP, broadcast, multicast e sessões de gestão interna do Docker (como tráfego interno de portas SSH ou DNS de serviços de suporte, se aplicável).   

Dado que o objetivo é classificar tráfego Web e de transporte da aplicação, quando pacotes passarem pelo nó de rede, então o filtro deve contemplar comunicações TCP e UDP (focando em portas HTTP/HTTPS e conexões associadas como 80, 443 e portas efêmeras de retorno).

Dado que a recolha opera em múltiplos cenários, quando o script de captura for acionado, então a cadeia BPF deve ser modular e configurável via variável de ambiente ou ficheiro de configuração.   

**3. Exemplo de Requisição (Expressão de Filtro BPF e Comando de Execução)**
Bash
# Expressão BPF parametrizada para captura limpa
BPF_FILTER="tcp or udp and not (arp or rarp) and not ether multicast and not (port 22 or port 2375)"

# Comando executado no contentor Gateway
tcpdump -i eth0 -s 0 -w /data/raw/session_clean.pcap "$BPF_FILTER"
**4. Exemplo de Resposta (Saída Esperada no Terminal de Captura)**
Plaintext
tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
^C
1428 packets captured
1428 packets received by filter
0 packets dropped by kernel

**5. Componentes Envolvidos**
Binário do sistema: tcpdump (Motor Libpcap com compilador BPF).   

Interface de rede virtual do contentor Gateway (eth0).   

Ficheiro de armazenamento bruto: formato .pcap.   

**6. Considerações Técnicas**
Utilizar o parâmetro -s 0 (snaplen) para garantir a captura integral dos cabeçalhos das camadas 3 e 4 sem truncamento de metadados temporais e volumétricos.

Assegurar que o filtro não descarte tráfego UDP legítimo associado a novos protocolos de transporte Web, como HTTP/3 sobre QUIC (porta 443 UDP).

Validar que a complexidade da regra BPF não imponha sobrecarga computacional excessiva na CPU do contentor Gateway em modo de captura contínua.   

**7. Dependências e Bloqueios**
Depende de: Issue #06 (Ferramentas de rede instaladas e testadas).   

Bloqueia: Issue #12 (Orquestrador de Sessão), Issue #13 (Dataset de Apostas) e Issue #14 (Dataset Benigno).   

**8. Como Testar**
Aceder ao contentor Gateway: docker exec -it gateway_firewall bash.   

Iniciar a captura com o filtro ativo gravando num ficheiro temporário:

tcpdump -i eth0 -w /tmp/test_filter.pcap "tcp or udp and not arp".   

No contentor app_client, gerar tráfego ICMP (ping) e tráfego HTTPS (curl para um sítio público):

ping -c 2 8.8.8.8 && curl -I [https://example.com](https://example.com).

Interromper a captura e inspecionar o ficheiro com o tshark:

tshark -r /tmp/test_filter.pcap -T fields -e _ws.col.Protocol | sort | uniq.   

Confirmar que pacotes ARP não foram gravados no registo PCAP.   

**9. Definição de Pronto (DoD)**
Ficheiro de configuração ou módulo Python com a expressão BPF padrão estruturada e documentada.   

Teste de validação executado demonstrando a filtragem de tráfego espúrio da rede.   

Taxa de descarte no kernel (dropped by kernel) nula ou próxima de 0 durante a sessão de validação.   

**10. Prioridade e Severidade**
Prioridade: Média.   

Severidade: Média (Ruídos de rede comprometem a qualidade estatística dos atributos na fase de pré-processamento).   

**11. Etiquetas (Labels)**
infraestrutura, networking, tcpdump, bpf, data-collection.   

**12. Documentação Relacionada**
Requisito RF02 (Sniffing Passivo sem degradação).   

Requisito RF03 (Extração de Atributos).   

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).

**13. Estimativa**
T-Shirt Size: S (Small) / 2 Story Points.

---

### **Issue #12: [Backend] Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser)**
**1. História de Usuário (User Story)**
> Como investigador do projeto,
> eu quero um script orquestrador em Python que sincronize o arranque e encerramento do processo de captura de pacotes com o ciclo de navegação automatizada,
> para que cada arquivo PCAP contenha rigorosamente o tráfego gerado durante a sessão ativa, evitando arquivos vazios, corrupções por paragem abrupta ou misturas de sessões distintas.

**2. Critérios de Aceitação (AC)**
Dado que uma nova sessão de recolha é solicitada, quando o orquestrador iniciar o ciclo, então o processo de captura (tcpdump) no nó de rede deve ser iniciado antes do carregamento da primeira URL no navegador.   

Dado que o navegador termina as interações simuladas, quando a página for fechada, então o sinal de paragem graciosa (SIGINT ou SIGTERM) deve ser enviado ao tcpdump para forçar a descarga dos buffers e o fecho correto do arquivo PCAP.   

Dado que cada sessão corresponde a um domínio e rótulo específicos, quando o arquivo PCAP for guardado, então deve ser nomeado segundo um padrão estruturado (ex.: <classe>_<dominio>_<timestamp>.pcap) e armazenado no diretório persistente.   

**3. Exemplo de Requisição (Módulo Python de Orquestração / session_orchestrator.py)**
Python
import time
import subprocess
from pathlib import Path
from src.collector.stealth_config import get_stealth_driver
from src.collector.human_behavior import simulate_human_session

OUTPUT_DIR = Path("/data/raw")

def run_collection_session(url: str, label: str, duration: int = 45):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    clean_domain = url.split("//")[-1].replace("/", "_")
    pcap_filename = OUTPUT_DIR / f"{label}_{clean_domain}_{int(time.time())}.pcap"
    
    # 1. Inicia o processo de captura de pacotes em segundo plano
    bpf_filter = "tcp or udp and not (arp or rarp)"
    tcpdump_cmd = [
        "tcpdump", "-i", "eth0", "-s", "0", 
        "-w", str(pcap_filename), bpf_filter
    ]
    sniffer_proc = subprocess.Popen(tcpdump_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)  # Intervalo de estabilização do socket de escuta
    
    try:
        # 2. Executa a navegacao simulada
        driver = get_stealth_driver()
        simulate_human_session(driver, url, duration_seconds=duration)
        driver.quit()
    finally:
        # 3. Interrupcao graciosa do sniffer
        sniffer_proc.send_signal(subprocess.signal.SIGINT)
        sniffer_proc.wait(timeout=5)
        print(f"[OK] Sessao finalizada. Arquivo gerado: {pcap_filename}")
**4. Exemplo de Resposta (Log de Execução do Orquestrador)**
Plaintext
[INFO] Inicializando captura para sessao de treino...
[INFO] Processo tcpdump iniciado (PID: 341).
[INFO] Navegador ativo em https://betano.pt. Simulando comportamento...
[INFO] Navegador encerrado com sucesso.
[INFO] Sinal SIGINT enviado ao sniffer. Finalizando gravacao...
[OK] Sessao finalizada. Arquivo gerado: /data/raw/apostas_betano.pt_1793158000.pcap

**5. Componentes Envolvidos**
Container app_client e container gateway_firewall.   

Módulo subprocess nativo do Python.   

Binário do sistema: tcpdump.   

Navegador automatizado (Selenium/Playwright) com rotinas de comportamento.   

**6. Considerações Técnicas**
Introduzir um pequeno atraso (1 a 2 segundos) após o disparo do tcpdump para assegurar que o filtro BPF foi compilado e anexado ao kernel antes do disparo do primeiro pacote TLS.   

Assegurar o tratamento de exceções com blocos try/finally para que o processo de captura seja sempre encerrado, mesmo perante falhas ou falhas de tempo limite durante a execução do navegador.   

Validar que o arquivo .pcap não permanece bloqueado por descritores abertos após a conclusão do ciclo.   

**7. Dependências e Bloqueios**
Depende de: Issue #08 (Selenium/Playwright no Docker), Issue #09 (Anti-bot e User-Agents), Issue #10 (Simulação humana) e Issue #11 (Filtro BPF).   

Bloqueia: Issue #13 (Coleta do dataset de apostas), Issue #14 (Coleta do dataset benigno) e Issue #15 (Validação de integridade dos PCAPs).   

**8. Como Testar**
Executar uma sessão de teste chamando o módulo de orquestração:

docker exec -it app_client python3 -m src.collector.session_orchestrator.   

Verificar se o processo tcpdump encerrou corretamente através de ps aux | grep tcpdump.   

Validar se o arquivo .pcap foi gravado com tamanho maior que 0 bytes no diretório montado (data/raw/).   

Abrir o arquivo de captura com tcpdump -r <arquivo>.pcap | wc -l e atestar a existência de pacotes capturados.   

**9. Definição de Pronto (DoD)**
Módulo session_orchestrator.py implementado e integrado aos scripts de navegação e captura.   

Encerramento sem processos zumbis ou ficheiros de rede corrompidos.   

Padrão de nomenclatura de arquivos documentado e validado em execuções de teste.   

**10. Prioridade e Severidade**
Prioridade: Alta (Módulo central para viabilizar as recolhas em massa).   

Severidade: Alta.

**11. Etiquetas (Labels)**
backend, orchestration, networking, data-collection, automation.   

**12. Documentação Relacionada**
Requisito RF01 (Automação de Coleta).   

Requisito RF02 (Sniffing Passivo).   

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #13: [Backend] Dataset de Apostas: Execução da recolha em massa (Bet365, Betano, etc.)**
**1. História de Usuário (User Story)**
> Como investigador do projeto,
> eu quero executar rotinas automatizadas de recolha em massa numa lista diversificada de plataformas de apostas online populares,
> para que sejam gerados múltiplos ficheiros PCAP com assinaturas comportamentais reais (comunicações persistentes via WebSockets, pacotes de tamanho reduzido e fluxos contínuos de cotações) rotulados como classe 1.

**2. Critérios de Aceitação (AC)**
Dado que o orquestrador de recolha é iniciado com a lista de apostas, quando aceder a domínios como Bet365, Betano, Betfair, Sportingbet e KTO, então cada sessão deve interagir durante um tempo configurável (ex.: 45 a 90 segundos) permitindo atualizações de cotações dinâmicas.   

Dado que as plataformas de apostas utilizam múltiplos nós e redes de entrega de conteúdo (CDN), quando os pacotes forem capturados, então o tráfego gerado deve conter fluxos TLS e WebSockets representativos da aplicação.   

Dado que o objetivo é treinar um modelo generalista, quando a recolha for concluída, então o volume de ficheiros capturados deve cobrir pelo menos 10 domínios distintos de casas de apostas para evitar viés em relação a uma única plataforma.   

Dado que cada sessão produz um registo bruto, quando o arquivo PCAP for guardado no disco, então deve ser atribuído o prefixo apostas_ ou classe1_ no nome do ficheiro para indexação estruturada.   

**3. Exemplo de Requisição (Script de Recolha em Lote / collect_betting_traffic.py)**
Python
import json
import time
from pathlib import Path
from src.collector.session_orchestrator import run_collection_session

BETTING_TARGETS = [
    {"domain": "https://www.bet365.com", "name": "bet365"},
    {"domain": "https://www.betano.pt", "name": "betano"},
    {"domain": "https://www.betfair.com", "name": "betfair"},
    {"domain": "https://www.sportingbet.com", "name": "sportingbet"},
    {"domain": "https://www.kto.com", "name": "kto"}
]

def execute_betting_batch(iterations_per_site: int = 5):
    print(f"[START] Iniciando recolha em lote para {len(BETTING_TARGETS)} alvos de apostas...")
    for target in BETTING_TARGETS:
        for i in range(iterations_per_site):
            print(f"[EXEC] Recolhendo sessao {i+1}/{iterations_per_site} em {target['name']}...")
            try:
                run_collection_session(
                    url=target["domain"], 
                    label=f"apostas_{target['name']}", 
                    duration=60
                )
                time.sleep(10)  # Intervalo de descanso entre sessoes consecutivas
            except Exception as e:
                print(f"[WARN] Falha durante a sessao em {target['name']}: {e}")

if __name__ == "__main__":
    execute_betting_batch()
**4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)**
Plaintext
[START] Iniciando recolha em lote para 5 alvos de apostas...
[EXEC] Recolhendo sessao 1/5 em bet365...
[INFO] Processo tcpdump iniciado (PID: 412).
[INFO] Sessao interativa concluida para https://www.bet365.com (60s decorridos).
[OK] Sessao finalizada. Arquivo gerado: /data/raw/apostas_bet365_1793162000.pcap
[EXEC] Recolhendo sessao 1/5 em betano...
[OK] Sessao finalizada. Arquivo gerado: /data/raw/apostas_betano_1793162075.pcap
[OK] Lote de recolha de apostas finalizado. Total de ficheiros gerados: 25.

**5. Componentes Envolvidos**
Container app_client (Agente de Navegação automatizado).   

Container gateway_firewall (Ponto de monitorização passiva).   

Módulo session_orchestrator.py.   

Volume persistente /data/raw/ montado no ambiente Docker.   

**6. Considerações Técnicas**
Introduzir tempos de espera aleatórios entre acessos ao mesmo domínio para evitar o bloqueio preventivo de IP no gateway por parte de firewalls de aplicação Web (WAF).   

Assegurar que os testes cubram páginas com transmissões em tempo real (painéis de apostas ao vivo), gerando o padrão característico de trocas contínuas e pacotes de tamanho reduzido documentado na metodologia.   

Controlar o espaço em disco do host, monitorizando o crescimento da pasta data/raw/ ao longo da execução do lote.   

**7. Dependências e Bloqueios**
Depende de: Issue #08 (Selenium/Playwright), Issue #09 (Técnicas anti-bot), Issue #10 (Comportamento humano), Issue #11 (Filtro BPF) e Issue #12 (Orquestrador de sessão).   

Bloqueia: Issue #15 (Validação de integridade dos PCAPs), Issue #16 (Extração de metadados brutos) e Issue #17 (Extração de fluxos bidirecionais PCAP para CSV).   

**8. Como Testar**
Executar uma rodada preliminar no contentor de navegação com 1 repetição por sítio:   

docker exec -it app_client python3 -m src.collector.collect_betting_traffic.   

Listar os ficheiros gerados na pasta de destino:   

ls -lh data/raw/apostas_*.pcap.   

Validar a presença de fluxos de dados abrindo uma das capturas com o comando:   

tcpdump -r data/raw/apostas_bet365_*.pcap -c 10.   

Verificar se a quantidade de pacotes registada é condizente com uma sessão de navegação ativa de 60 segundos.   

**9. Definição de Pronto (DoD)**
Script collect_betting_traffic.py implementado com lista configurável de domínios.   

Conjunto de arquivos PCAP brutos de tráfego de apostas gerado e guardado no diretório persistente.   

Logs de execução gravados sem interrupções por travamento do navegador.   

**10. Prioridade e Severidade**
Prioridade: Alta (Sem os dados da classe alvo, o pipeline de ML não pode ser alimentado).   

Severidade: Alta.

**11. Etiquetas (Labels)**
backend, data-collection, betting, pcap, traffic-generation.   

**12. Documentação Relacionada**
Requisito RF01 (Automação de Coleta).   

Requisito RF02 (Sniffing Passivo).   

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem - Tráfego Alvo).   

Capítulo 3.2.2 do TCC (Engenharia de Atributos Baseada em Fluxos).   

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #14: [Backend] Dataset Benigno: Execução da recolha de sítios de controlo (YouTube, Notícias)**
**1. História de Usuário (User Story)**
> Como investigador do projeto,
> eu quero executar rotinas automatizadas de recolha de tráfego numa lista de sítios de controlo representativos da navegação benigna quotidiana (portais de notícias, plataformas de transmissão de vídeo como o YouTube e enciclopédias),
> para que sejam capturados fluxos bidirecionais de tráfego legítimo com variância temporal elevada e pacotes volumosos (classe 0), essenciais para o balanceamento e para a mitigação de falsos positivos no comitê de IA.

**2. Critérios de Aceitação (AC)**
Dado que o módulo de recolha é executado para a classe benigna, quando aceder a serviços de transmissão e notícias (ex.: YouTube, G1, Wikipedia, BBC, UOL), então a sessão interativa deve emular leitura humana, pausas de análise e reprodução de conteúdo durante 45 a 90 segundos.   

Dado que o tráfego legítimo de vídeo e portais multimédia satura frequentemente a MTU, quando os pacotes forem interceptados, então os ficheiros PCAP devem refletir distribuições com pacotes de grande comprimento (próximos de 1500 bytes) e assimetria de volume típica de descargas cliente-servidor.   

Dado que a diversidade de contraexemplos previne o sobreajuste (overfitting), quando o lote terminar, então o volume de recolha benigna deve englobar múltiplos serviços distintos, gerando uma proporção equilibrada em relação ao conjunto de apostas.   

Dado que os registos precisam de indexação inequívoca no pré-processamento, quando os ficheiros forem gravados na diretoria persistente, então devem adotar o prefixo estruturado benigno_<servico>_<timestamp>.pcap.   

**3. Exemplo de Requisição (Script de Recolha Benigna em Lote / collect_benign_traffic.py)**
Python
import time
from pathlib import Path
from src.collector.session_orchestrator import run_collection_session

BENIGN_TARGETS = [
    {"domain": "https://www.youtube.com", "name": "youtube"},
    {"domain": "https://g1.globo.com", "name": "g1_noticias"},
    {"domain": "https://pt.wikipedia.org", "name": "wikipedia"},
    {"domain": "https://www.bbc.com/portuguese", "name": "bbc_noticias"},
    {"domain": "https://www.uol.com.br", "name": "uol"}
]

def execute_benign_batch(iterations_per_site: int = 5):
    print(f"[START] Iniciando recolha benigna para {len(BENIGN_TARGETS)} alvos de controlo...")
    for target in BENIGN_TARGETS:
        for i in range(iterations_per_site):
            print(f"[EXEC] Recolhendo sessao benigna {i+1}/{iterations_per_site} em {target['name']}...")
            try:
                run_collection_session(
                    url=target["domain"], 
                    label=f"benigno_{target['name']}", 
                    duration=60
                )
                time.sleep(10)  # Intervalo de descanso entre sessoes consecutivas
            except Exception as e:
                print(f"[WARN] Falha durante a recolha benigna em {target['name']}: {e}")

if __name__ == "__main__":
    execute_benign_batch()
**4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)**
Plaintext
[START] Iniciando recolha benigna para 5 alvos de controlo...
[EXEC] Recolhendo sessao benigna 1/5 em youtube...
[INFO] Processo tcpdump iniciado (PID: 518).
[INFO] Sessao interativa concluida para https://www.youtube.com (60s decorridos).
[OK] Sessao finalizada. Arquivo gerado: /data/raw/benigno_youtube_1793165000.pcap
[EXEC] Recolhendo sessao benigna 1/5 em g1_noticias...
[OK] Sessao finalizada. Arquivo gerado: /data/raw/benigno_g1_noticias_1793165075.pcap
[OK] Lote de controlo benigno finalizado. Total de ficheiros gerados: 25.

**5. Componentes Envolvidos**
Contentor app_client (Agente de Navegação em modo headless).   

Contentor gateway_firewall (Ponto de recolha com filtro BPF ativo).   

Módulo Python session_orchestrator.py.   

Volume persistente /data/raw/ montado no Docker.   

**6. Considerações Técnicas**
Garantir que as sessões em plataformas de vídeo permitam a reprodução contínua em buffer para gerar fluxos contínuos de pacotes volumosos na camada de transporte.   

Monitorizar a alocação de memória no contentor de navegação durante o acesso a portais pesados de notícias, evitando fugas de memória no navegador Chromium.   

Assegurar que nenhuma interação realize descarregamento intencional de ficheiros pesados executáveis que esgotem a largura de banda ou o armazenamento.   

**7. Dependências e Bloqueios**
Depende de: Issue #10 (Comportamento humano), Issue #11 (Filtro BPF) e Issue #12 (Orquestrador de sessão).   

Bloqueia: Issue #15 (Validação de integridade dos PCAPs), Issue #16 (Extração de metadados brutos) e Issue #17 (Conversão de fluxos bidirecionais PCAP para CSV).   

**8. Como Testar**
Executar uma ronda preliminar de recolha de controlo no contentor de cliente:   

docker exec -it app_client python3 -m src.collector.collect_benign_traffic.   

Inspecionar a diretoria montada no host para atestar a gravação dos ficheiros:   

ls -lh data/raw/benigno_*.pcap.   

Validar a presença de fluxos volumosos executando:   

tcpdump -r data/raw/benigno_youtube_*.pcap -c 10.   

Confirmar que os comprimentos de pacotes registam valores elevados característicos de streaming (próximos de 1500 bytes).   

**9. Definição de Pronto (DoD)**
Ficheiro collect_benign_traffic.py funcional e integrado com a orquestração.   

Conjunto balanceado de ficheiros PCAP de tráfego de controlo benigno guardado em data/raw/.   

Ausência de corrupções nas capturas geradas durante as sessões.   

**10. Prioridade e Severidade**
Prioridade: Alta (Indispensável para o treino balanceado dos modelos de ML).   

Severidade: Alta.

**11. Etiquetas (Labels)**
backend, data-collection, benign-traffic, pcap, traffic-generation.   

**12. Documentação Relacionada**
Requisito RF01 (Automação de Coleta).   

Requisito RF02 (Sniffing Passivo).   

Capítulo 3.2.1 do TCC (Tráfego de Controle - Benigno).   

Capítulo 3.2.2 do TCC (Distribuição e Variância do Tamanho de Pacotes).   

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #15: [Backend] Validação de Captura: Script para verificar integridade dos PCAPs**
**1. História de Usuário (User Story)**
> Como investigador do projeto,
> eu quero um script automatizado que valide a integridade estrutural e sintática de todos os ficheiros PCAP recolhidos,
> para que capturas corrompidas, truncadas, sem pacotes úteis ou com erros de cabeçalho global sejam identificadas e isoladas antes do pipeline de extração de fluxos.

**2. Critérios de Aceitação (AC)**
Dado que o script processa o diretório /data/raw/, quando analisar cada ficheiro .pcap, então deve verificar se o cabeçalho mágico (magic number) da Libpcap é válido e não está truncado.   

Dado que um ficheiro de captura pode ter sido interrompido antes da troca de pacotes, quando a contagem de pacotes for realizada via scapy ou tshark, então o ficheiro deve conter um volume mínimo de pacotes válidos (ex.: 
≥15 pacotes TCP/UDP) para não ser descartado como ruído de sessão.   

Dado que capturas com erro inviabilizam a conversão para CSV, quando um PCAP apresentar erros de sintaxe ou terminação abrupta, então deve ser movido para uma pasta de quarentena (/data/corrupted/) e registado num relatório de anomalias.   

Dado que múltiplos ficheiros são validados em lote, quando o processo terminar, então deve ser exibido um sumário estatístico com o total de ficheiros aprovados e reprovados por classe (apostas e benigno).   

**3. Exemplo de Requisição (Script Python de Verificação / verify_pcaps.py)**
Python
import os
import shutil
from pathlib import Path
from scapy.all import PcapReader

RAW_DIR = Path("/data/raw")
CORRUPTED_DIR = Path("/data/corrupted")
MIN_PACKETS = 15

def validate_pcap(filepath: Path) -> bool:
    count = 0
    try:
        with PcapReader(str(filepath)) as reader:
            for _ in reader:
                count += 1
                if count >= MIN_PACKETS:
                    return True
        return count >= MIN_PACKETS
    except Exception as err:
        print(f"[ERRO] Falha de integridade em {filepath.name}: {err}")
        return False

def run_validation():
    CORRUPTED_DIR.mkdir(parents=True, exist_ok=True)
    valid_count = 0
    invalid_count = 0

    for pcap_file in RAW_DIR.glob("*.pcap"):
        if validate_pcap(pcap_file):
            valid_count += 1
        else:
            invalid_count += 1
            shutil.move(str(pcap_file), str(CORRUPTED_DIR / pcap_file.name))
            print(f"[QUARENTENA] Ficheiro movido: {pcap_file.name}")

    print(f"\n[SUMÁRIO] Válidos: {valid_count} | Corrompidos/Insuficientes: {invalid_count}")

if __name__ == "__main__":
    run_validation()
**4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)**
Plaintext
[INFO] Iniciando verificação de integridade dos arquivos PCAP em /data/raw...
[OK] apostas_bet365_1793162000.pcap validado com sucesso (1420 pacotes).
[OK] benigno_youtube_1793165000.pcap validado com sucesso (3890 pacotes).
[ERRO] Falha de integridade em apostas_kto_1793162800.pcap: Scapy pcap reading error: premature EOF.
[QUARENTENA] Ficheiro movido: apostas_kto_1793162800.pcap

[SUMÁRIO] Válidos: 48 | Corrompidos/Insuficientes: 1

**5. Componentes Envolvidos**
Interpretador Python 3 no container Gateway ou Cliente.   

Biblioteca scapy (PcapReader com leitura por fluxo para poupar memória).   

Utilitário de linha de comando capinfos ou tshark para dupla checagem.   

Volume montado /data/raw/ e /data/corrupted/.   

**6. Considerações Técnicas**
Utilizar o iterador PcapReader em vez da função rdpcap() da Scapy, pois carregar ficheiros PCAP inteiros em memória viola as restrições estritas de RAM do projeto (RNF02).   

Assegurar que a deteção de ficheiros corrompidos não interrompa o laço de execução sobre os restantes ficheiros.   

Manter um registo de log detalhando a causa do descarte (ex.: EOF prematuro, tamanho zero, abaixo do limite de pacotes).   

**7. Dependências e Bloqueios**
Depende de: Issue #13 (Coleta do dataset de apostas) e Issue #14 (Coleta do dataset benigno).   

Bloqueia: Issue #16 (Extração de metadados brutos) e Issue #17 (Extração de fluxos bidirecionais PCAP para CSV).   

**8. Como Testar**
Criar intencionalmente um ficheiro de teste corrompido ou vazio:   

touch /data/raw/corrupted_test.pcap

head -c 20 /dev/urandom > /data/raw/broken_header.pcap.

Executar o script de validação:   

docker exec -it app_client python3 -m src.collector.verify_pcaps.

Confirmar que os ficheiros defeituosos foram movidos para /data/corrupted/.   

Confirmar que os PCAPs válidos de apostas e controlo permaneceram na pasta /data/raw/ intactos.   

**9. Definição de Pronto (DoD)**
Módulo verify_pcaps.py implementado e versionado.   

Validação sem estouro de memória utilizando leitura por blocos/geradores.   

Tratamento de exceções cobrindo encerramento abrupto e ficheiros incompletos.   

**10. Prioridade e Severidade**
Prioridade: Média.   

Severidade: Alta (Evita falhas de runtime na conversão em lote para CSV).   

**11. Etiquetas (Labels)**
backend, data-quality, pcap, validation, data-collection.   

**12. Documentação Relacionada**
Requisito RF02 (Sniffing Passivo e integridade dos PCAPs).   

Requisito RNF02 (Restrição de Memória RAM).

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   

**13. Estimativa**
T-Shirt Size: S (Small) / 2 Story Points.

---

### **Issue #16: [Backend] Extração de Metadados Brutos: Relatório de volume e duração por captura**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** um script automatizado que processe os arquivos PCAP validados e gere um relatório estruturado (JSON/CSV) com metadados brutos (volume em bytes, número de pacotes, duração total do fluxo e timestamps inicial/final),
> **para que** possamos auditar o balanceamento volumétrico e temporal entre o tráfego de apostas (classe 1) e benigno (classe 0) antes da etapa de conversão em fluxos estatísticos.

**2. Critérios de Aceitação (AC)**
* **Dado que** o diretório `/data/raw/` contém capturas PCAP validadas pela Issue #15, **quando** o script de metadados for executado, **então** ele deve extrair para cada arquivo: nome do arquivo, classe atribuída (betting ou benign), tamanho em disco (bytes), contagem de pacotes, timestamp inicial, timestamp final e duração total ($t_{final} - t_{inicial}$).
* **Dado que** a avaliação comparativa é necessária, **quando** o processamento de todos os arquivos for concluído, **então** o script deve calcular métricas agregadas por classe (média de duração, variância de duração, volume total trafegado e média de pacotes por sessão).
* **Dado que** o sistema opera sob restrição severa de memória RAM (RNF02), **quando** inspecionar arquivos PCAP com milhares de pacotes, **então** o leitor deve realizar leitura sequencial via streaming de cabeçalhos sem carregar os payloads dos pacotes na memória principal.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.collector.extract_raw_metadata \
    --input-dir data/raw \
    --output-json data/reports/raw_metadata_report.json \
    --output-csv data/reports/raw_metadata_report.csv
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Iniciando extração de metadados brutos em data/raw...
[INFO] Processando classe 'betting': 50 arquivos encontrados.
[INFO] Processando classe 'benign': 50 arquivos encontrados.
[OK] data/raw/betting_bet365_20261028_120000.pcap -> 1,420 pacotes | 892,340 bytes | Duração: 62.4s
[OK] data/raw/benign_youtube_20261028_120500.pcap -> 8,910 pacotes | 9,450,120 bytes | Duração: 90.1s
...
================ SÍNTESE METADADOS BRUTOS ================
Classe 'betting':
  - Arquivos válidos: 50
  - Duração média: 61.8s (DP: 4.2s)
  - Volume médio: 1.12 MB por sessão
  - Média de pacotes: 1,650
Classe 'benign':
  - Arquivos válidos: 50
  - Duração média: 78.4s (DP: 8.5s)
  - Volume médio: 6.84 MB por sessão
  - Média de pacotes: 5,420
[INFO] Relatórios salvos em data/reports/raw_metadata_report.[json|csv]
```

**5. Componentes Envolvidos**
* `src/collector/extract_raw_metadata.py`: Script extrator de metadados brutos.
* `data/raw/`: Diretório de entrada com arquivos `.pcap`.
* `data/reports/`: Diretório de destino dos relatórios consolidados.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.2.1 do TCC (*Aquisição e Rotulagem*), a auditoria dos metadados brutos permite diagnosticar se alguma classe sofreu interrupção precoce de navegação.
* Utilização de bibliotecas eficientes como `dpkt` ou `scapy.PcapReader` (iterador de pacotes) para garantir conformidade com o RNF02 (não exceder limite de RAM).
* Não inspecionar conteúdo de payload, respeitando a privacidade e a premissa de tráfego HTTPS criptografado (Seção 3.2.2 do TCC).

**7. Mockups ou Referências Visuais**
* N/A (Módulo de backend/análise em linha de comando; saída via terminal e arquivos JSON/CSV).

**8. Dependências e Bloqueios**
* **Depende de:** Issue #13 (Coleta de Apostas), Issue #14 (Coleta Benigna) e Issue #15 (Validação de PCAPs).
* **Bloqueia:** Issue #17 (Extração de fluxos bi-direcionais PCAP para CSV).

**9. Como Testar (Plano de Teste)**
1. Gerar ou disponibilizar pelo menos 2 arquivos PCAP sintéticos (um de aposta e um benigno) em `/data/raw/`.
2. Executar o comando CLI: `python -m src.collector.extract_raw_metadata --input-dir data/raw --output-json data/reports/raw_metadata_report.json`.
3. Validar se o arquivo `raw_metadata_report.json` foi gerado e contém chaves `files`, `summary_betting` e `summary_benign`.
4. Executar os testes automatizados via `pytest tests/test_extract_raw_metadata.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `src/collector/extract_raw_metadata.py` implementado com tratamento de exceções.
* Testes unitários cobrindo casos de PCAP vazio, PCAP com timestamps desordenados e diretório sem arquivos.
* Cobertura de testes superior a 85%.
* Relatórios gerados em JSON e CSV com métricas agregadas por classe.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média (Necessário para controle de qualidade da amostragem).

**12. Etiquetas (Labels)**
`backend`, `data-collection`, `metadata`, `analytics`, `pcap`.

**13. Documentação Relacionada**
* Requisito RF02 (Sniffing Passivo).
* Requisito RNF02 (Restrição de Memória RAM).
* Seção 3.2.1 do TCC (*Aquisição e Rotulagem*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

# 🧹 Grupo 3: Pré-processamento e Dataset

### **Issue #17: [Backend] Extração de fluxos bi-direcionais (Conversão PCAP para CSV)**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** converter os arquivos PCAP brutos em registros de fluxos de rede bidirecionais delimitados pela 5-tupla (IP origem, IP destino, porta origem, porta destino, protocolo), extraindo no mínimo 20 metadados estatísticos e temporais,
> **para que** o tráfego criptografado seja transformado em um dataset tabular estruturado apto para a engenharia de atributos sem violar a criptografia TLS/HTTPS (RF03).

**2. Critérios de Aceitação (AC)**
* **Dado que** existem arquivos PCAP validados em `/data/raw/`, **quando** o extrator de fluxos for executado, **então** os pacotes individuais devem ser agrupados em fluxos bidirecionais baseados na 5-tupla com timeout de inatividade configurável (ex.: 60s ou 120s).
* **Dado cada fluxo identificado**, **quando** as métricas estatísticas forem computadas, **então** devem ser extraídos no mínimo 20 atributos (RF03 e Seção 3.2.2 do TCC), incluindo:
  - Intervalos entre pacotes (IAT médio, variância, desvio padrão, máx, mín nas direções direta e reversa);
  - Distribuição de tamanho de carga útil (comprimento médio de pacotes, desvio padrão, assimetria/skewness);
  - Duração total do fluxo e volume acumulado de bytes e pacotes por direção.
* **Dado que** o tráfego trafega sobre TLS/HTTPS (porta 443), **quando** o extrator computar as características, **então** nenhuma análise de carga útil profunda (Deep Packet Inspection - DPI) deve ser realizada, assegurando conformidade com a Seção 3.2.2 do TCC.
* **Dado o término do processamento**, **quando** os dados forem consolidados, **então** deve ser gerado um arquivo CSV estruturado em `data/processed/flows_extracted.csv`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.flow_extractor \
    --input-dir data/raw/ \
    --output-csv data/processed/flows_extracted.csv \
    --flow-timeout 60.0
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Iniciando agrupamento de fluxos bidirecionais (Timeout: 60s)...
[INFO] Processando 100 arquivos PCAP em data/raw/...
[PROGRESS] 25/100 PCAPs analisados (1,450 fluxos gerados)...
[PROGRESS] 50/100 PCAPs analisados (3,120 fluxos gerados)...
[PROGRESS] 100/100 PCAPs analisados (6,890 fluxos gerados)...
[SUCCESS] Conversão concluída!
  - Total de fluxos extraídos: 6,890
  - Atributos por fluxo: 24 colunas estatísticas
  - Arquivo exportado: data/processed/flows_extracted.csv (14.2 MB)
```

**5. Componentes Envolvidos**
* `src/data_processing/flow_extractor.py`: Motor de agregação em 5-tuplas e cálculo estatístico.
* `data/raw/`: Arquivos PCAP de entrada.
* `data/processed/flows_extracted.csv`: Dataset tabular gerado.

**6. Considerações Técnicas e Arquitetura**
* Conforme detalhado na Seção 3.2.2 do TCC (*Engenharia de Atributos Baseada em Fluxos*), o descarte de DPI e o foco estrito em metadados temporais e volumétricos garantem a viabilidade da classificação sob TLS 1.3 / WSS.
* Implementar cálculo online (método de Welford para média e variância de IAT e packet length) para evitar o armazenamento de listas inteiras de timestamps em memória (RNF02).
* Suportar formatos Libpcap padrão gerados pelo tcpdump.

**7. Mockups ou Referências Visuais**
* N/A (Processamento de dados em lote; saída via arquivo CSV).

**8. Dependências e Bloqueios**
* **Depende de:** Issue #15 (Validação de PCAPs) e Issue #16 (Metadados Brutos).
* **Bloqueia:** Issue #18 (Limpeza de Dados) e Issue #19 (Rotulagem das Classes).

**9. Como Testar (Plano de Teste)**
1. Executar o extrator com um PCAP de teste contendo tráfego TCP/HTTPS conhecido.
2. Abrir o CSV gerado e verificar se possui as colunas obrigatórias: `src_ip`, `dst_ip`, `src_port`, `dst_port`, `protocol`, `flow_duration`, `fwd_pkts_tot`, `bwd_pkts_tot`, `fwd_iat_mean`, `fwd_iat_std`, `pkt_len_mean`, `pkt_len_std`, etc.
3. Confirmar que o número de fluxos extraídos corresponde aos pares de conexão abertos no tráfego.
4. Executar os testes automatizados via `pytest tests/test_flow_extractor.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `flow_extractor.py` implementado com cálculo das 20+ variáveis estatísticas.
* Tratamento para pacotes fragmentados, retransmissões e fluxos unilaterais.
* Cobertura de testes unitários superior a 85%.
* Exportação do CSV validada com delimitador padrão e cabeçalho formal.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Crítica para o pipeline de ML).
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `data-processing`, `feature-extraction`, `flows`, `dataset`.

**13. Documentação Relacionada**
* Requisito RF03 (Extração de Atributos).
* Requisito RNF02 (Restrição de Memória RAM).
* Seção 3.2.2 do TCC (*Engenharia de Atributos Baseada em Fluxos*).

**14. Estimativa**
* **T-Shirt Size:** L (Large)
* **Story Points:** 5


---

### **Issue #18: [Backend] Limpeza de dados (Remoção de valores NaN, Inf e duplicatas)**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** um script automatizado de limpeza e sanitização do dataset de fluxos, removendo registros com valores nulos (`NaN`), infinitos (`+/-Inf`), duplicatas perfeitas e fluxos incompletos sem troca de dados,
> **para que** os algoritmos de aprendizado de máquina não sofram erros numéricos em tempo de treino ou inferência (Seção 3.2.4 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que** o arquivo `flows_extracted.csv` contém divisões por zero em atributos derivados de fluxos de duração nula (gerando `Inf` ou `NaN`), **quando** a rotina de limpeza for executada, **então** todos os valores `Inf` e `-Inf` devem ser convertidos para `NaN` e tratados de forma parametrizada (descarte de linha ou imputação com o valor limite).
* **Dado que** podem existir fluxos duplicados gerados por retransmissões ou sondagens vazias (ex.: apenas 1 pacote SYN sem resposta), **quando** o filtro atuar, **então** fluxos com volume de pacotes menor que o limiar mínimo (ex.: total de pacotes $< 3$) devem ser descartados.
* **Dado o conjunto limpo**, **quando** o processo for concluído, **então** deve ser salvo em `data/processed/flows_cleaned.csv` acompanhado de um log de auditoria discriminando exatamente quantas linhas foram removidas por cada critério.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.clean_dataset \
    --input-csv data/processed/flows_extracted.csv \
    --output-csv data/processed/flows_cleaned.csv \
    --min-packets 3
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando data/processed/flows_extracted.csv (6,890 linhas)...
[INFO] Linhas com NaN/Inf identificadas: 42 (0.61%) -> Removidas.
[INFO] Linhas duplicadas exatas: 18 (0.26%) -> Removidas.
[INFO] Fluxos com pacotes insuficientes (< 3): 115 (1.67%) -> Removidos.
================ RELATÓRIO DE LIMPEZA ================
  - Registros originais: 6,890
  - Registros removidos: 175
  - Registros limpos preservados: 6,715 (97.46%)
[SUCCESS] Dataset limpo salvo em data/processed/flows_cleaned.csv
```

**5. Componentes Envolvidos**
* `src/data_processing/clean_dataset.py`: Sanitizador de dados.
* `pandas`, `numpy`: Tratamento matricial e vetorial.
* `data/processed/flows_cleaned.csv`: Saída limpa.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.2.4 do TCC (*Pré-processamento e Balanceamento*), fluxos ruidosos ou incompletos distorcem a convergência de modelos como XGBoost e Regressão Logística.
* Operações vetorizadas via Pandas para manter o tempo de execução abaixo de 5 segundos no host.
* Geração de asserções matemáticas no final do script garantindo `df.isna().sum().sum() == 0` e `np.isinf(df.values).sum() == 0`.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #17 (Extração de fluxos bidirecionais).
* **Bloqueia:** Issue #19 (Rotulagem das Classes) e Issue #20 (Normalização).

**9. Como Testar (Plano de Teste)**
1. Criar um dataset mock com linhas contendo `np.nan`, `np.inf`, `-np.inf` e duplicatas.
2. Executar o script de limpeza.
3. Verificar se o arquivo resultante não contém nenhum valor nulo ou infinito.
4. Executar os testes automatizados via `pytest tests/test_clean_dataset.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `clean_dataset.py` implementado e integrado ao pipeline.
* Testes unitários com casos de borda passando com 100% de sucesso.
* Verificação estrita de ausência de `NaN` e `Inf` no arquivo exportado.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `data-cleaning`, `pandas`, `quality`.

**13. Documentação Relacionada**
* Requisito RF03 (Extração de Atributos).
* Seção 3.2.4 do TCC (*Pré-processamento e Balanceamento*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #19: [Backend] Rotulagem das classes (Apostas vs Benigno) e Label Encoding**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** rotular formalmente cada fluxo limpo com sua classe binária (1 para Plataformas de Apostas e 0 para Tráfego Benigno) e isolar identificadores de rede (IPs e portas efêmeras),
> **para que** os algoritmos supervisionados aprendam o comportamento temporal do protocolo sem memorizar endereços IP específicos (prevenção de overfitting e viés de coleta, Seção 3.2.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que** os fluxos foram gerados a partir de sessões mapeadas das Issues #13 e #14, **quando** o módulo de rotulagem processar o dataset, **então** a coluna alvo `label` deve receber `1` para fluxos de apostas e `0` para fluxos benignos de controle.
* **Dado que** identificadores como `src_ip`, `dst_ip`, `src_port` e `dst_port` podem causar memorização indevida de CDN/servidores (viés de coleta advertido na Seção 3.2.1 do TCC), **quando** o dataset para treino for formatado, **então** essas colunas de 5-tupla devem ser mantidas apenas em colunas de metadados separadas do vetor numérico de treino `X`.
* **Dado a conclusão da rotulagem**, **quando** exibido o relatório de distribuição, **então** a contagem de classes e a proporção percentual devem ser validadas e o CSV exportado para `data/processed/flows_labeled.csv`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.label_dataset \
    --input-csv data/processed/flows_cleaned.csv \
    --output-csv data/processed/flows_labeled.csv
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Lendo dataset limpo data/processed/flows_cleaned.csv...
[INFO] Aplicando rotulagem binária baseada nas origens de captura...
[INFO] Segregando identificadores de rede (5-tupla) em metadados de auditoria...
================ DISTRIBUIÇÃO DAS CLASSES ================
  - Classe 0 (Benigno): 3,520 fluxos (52.42%)
  - Classe 1 (Apostas): 3,195 fluxos (47.58%)
  - Total consolidado: 6,715 fluxos rotulados
[SUCCESS] Dataset rotulado salvo em data/processed/flows_labeled.csv
```

**5. Componentes Envolvidos**
* `src/data_processing/label_dataset.py`: Módulo de rotulagem e segregação de features.
* `data/processed/flows_labeled.csv`: Dataset com a coluna alvo `label`.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com a Seção 3.2.1 do TCC (*Aquisição e Rotulagem*), modelos de firewall não podem classificar tráfego aprendendo endereços IP estáticos, pois casas de apostas rotacionam constantemente IPs via Cloudflare e Akamai.
* Codificação numérica binária explícita (`int8`) para economizar memória RAM (RNF02).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #18 (Limpeza de Dados).
* **Bloqueia:** Issue #20 (Normalização) e Issue #21 (EDA).

**9. Como Testar (Plano de Teste)**
1. Executar o script de rotulagem com o CSV de entrada limpo.
2. Verificar se o CSV gerado contém a coluna `label` contendo exclusivamente valores `0` ou `1`.
3. Confirmar que a proporção entre as classes reflete a quantidade esperada de arquivos de captura.
4. Executar os testes via `pytest tests/test_label_dataset.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `label_dataset.py` implementado com testes automatizados passando.
* Garantia de ausência de colunas com strings ou identificadores efêmeros no espaço de features.
* Distribuição de classes documentada no log de saída.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `data-labeling`, `dataset`, `ml-preparation`.

**13. Documentação Relacionada**
* Requisito RF03 (Extração de Atributos).
* Seção 3.2.1 do TCC (*Aquisição e Rotulagem*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #20: [Backend] Normalização e padronização de escalas dos dados**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** aplicar escalonamento linear Min-Max (`Min-Max Scaling`) nas variáveis contínuas do dataset de fluxos delimitando-as no intervalo $[0, 1]$, serializando o objeto do transformador,
> **para que** atributos com grande ordem de magnitude (como volume acumulado de bytes) não dominem indevidamente os coeficientes dos modelos e o transformador possa ser reutilizado pelo motor de inferência em tempo real (Seção 3.2.4 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o dataset rotulado**, **quando** o escalonamento for aplicado via `MinMaxScaler` do Scikit-Learn, **então** todos os atributos numéricos contínuos devem ter seus valores rigorosamente transformados para o intervalo $[0.0, 1.0]$.
* **Dado que** o transformador ajustado nos dados de treino deve ser utilizado pelo firewall em tempo real durante a inferência (RNF01), **quando** o processo for concluído, **então** o transformador deve ser salvo em `models/scaler.joblib`.
* **Dado que** não pode ocorrer vazamento de dados (*data leakage*), **quando** a rotina for executada, **então** o scaler deve ser parametrizado (`fit`) exclusivamente nas amostras de treino e apenas aplicado (`transform`) nos conjuntos de validação e teste.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.scale_features \
    --input-csv data/processed/flows_labeled.csv \
    --output-csv data/processed/flows_scaled.csv \
    --scaler-output models/scaler.joblib
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando data/processed/flows_labeled.csv...
[INFO] Inicializando MinMaxScaler(feature_range=(0, 1))...
[INFO] Ajustando scaler em 24 atributos numéricos contínuos...
[VERIFY] Valor mínimo verificado no dataset transformado: 0.0000
[VERIFY] Valor máximo verificado no dataset transformado: 1.0000
[SUCCESS] Objeto transformador serializado em models/scaler.joblib (12.4 KB)
[SUCCESS] Dataset escalonado salvo em data/processed/flows_scaled.csv
```

**5. Componentes Envolvidos**
* `src/data_processing/scale_features.py`: Módulo de transformação de escalas.
* `sklearn.preprocessing.MinMaxScaler`: Algoritmo de normalização.
* `models/scaler.joblib`: Transformador serializado para produção.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.2.4 do TCC (*Pré-processamento e Balanceamento*), modelos como a Regressão Logística são extremamente sensíveis a diferenças de escala entre features (ex.: IAT em microssegundos vs contagem de pacotes).
* O objeto serializado `scaler.joblib` deve ser leve (< 50 KB) para carregamento instantâneo no container do firewall (RNF02).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #19 (Rotulagem das Classes).
* **Bloqueia:** Issue #21 (EDA), Issue #23 (Divisão Treino/Val/Teste) e Issue #24 (Seleção via SU).

**9. Como Testar (Plano de Teste)**
1. Executar o script `scale_features.py` sobre o dataset rotulado.
2. Inspecionar o dataset resultante e verificar com asserções se `df[features].min().min() >= 0.0` e `df[features].max().max() <= 1.0`.
3. Testar a desserialização do `models/scaler.joblib` e transformar um vetor mock de teste.
4. Executar os testes automatizados via `pytest tests/test_scale_features.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `scale_features.py` testado e funcional.
* Objeto `scaler.joblib` gerado e testado com predições em memória.
* Garantia de ausência de distorção de escala em atributos com variância zero.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `data-scaling`, `normalization`, `scikit-learn`.

**13. Documentação Relacionada**
* Requisito RF03 (Extração de Atributos).
* Seção 3.2.4 do TCC (*Pré-processamento e Balanceamento*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #21: [Backend] Análise estatística exploratória inicial (EDA) do dataset**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** gerar relatórios estatísticos descritivos e gráficos de análise exploratória de dados (EDA) comparando o tráfego de apostas e benigno (matriz de correlação de Pearson, distribuições de densidade de IAT e histogramas de tamanho de pacotes),
> **para que** possamos fundamentar analiticamente a divergência comportamental entre as classes e embasar teoricamente os Capítulos 3 e 4 do TCC.

**2. Critérios de Aceitação (AC)**
* **Dado o dataset de fluxos rotulado**, **quando** o script de EDA for executado, **então** deve computar métricas resumo (média, mediana, desvio padrão, variância e percentis 5/50/95) de cada característica separada por classe (0 vs 1).
* **Dado que** o comportamento dinâmico de WebSockets em apostas difere do tráfego estático/streaming, **quando** os gráficos de densidade forem renderizados, **então** devem evidenciar com clareza a concentração de intervalos curtos (IAT reduzido) e pacotes de tamanho reduzido na classe 1.
* **Dado o cálculo da matriz de correlação de Pearson**, **quando** renderizado o mapa de calor (*heatmap*), **então** os atributos altamente colineares ($|r| > 0.90$) devem ser listados em um sumário de redundâncias para informar o algoritmo de seleção de atributos.
* **Dado o encerramento da rotina**, **quando** salvos os artefatos, **então** devem ser gravados em `docs/eda/` gráficos em formato PNG (300 DPI) e o sumário numérico em `data/reports/eda_summary.json`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.eda_analysis \
    --input-csv data/processed/flows_labeled.csv \
    --output-dir docs/eda/ \
    --report-json data/reports/eda_summary.json
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando dataset rotulado para EDA (6,715 amostras)...
[INFO] Calculando estatísticas descritivas por classe...
[OK] Atributo 'fwd_iat_mean': Classe 0 = 0.082s | Classe 1 = 0.014s (Divergência expressiva)
[OK] Atributo 'pkt_len_mean': Classe 0 = 842.1 B | Classe 1 = 124.6 B (Tráfego de aposta com mensagens curtas)
[INFO] Gerando heatmap de correlação de Pearson em docs/eda/correlation_matrix.png...
[INFO] Gerando curvas de distribuição acumulada (CDF) em docs/eda/iat_cdf_comparison.png...
[SUCCESS] Relatório de EDA salvo em data/reports/eda_summary.json (4 gráficos gerados)
```

**5. Componentes Envolvidos**
* `src/data_processing/eda_analysis.py`: Módulo analítico de geração de estatísticas e gráficos.
* `matplotlib`, `seaborn`, `pandas`: Visualização de dados científicos.
* `docs/eda/`: Diretório de saída das figuras do TCC.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.2.2 e 4.1 do TCC, a comprovação visual e estatística das assinaturas do tráfego sob TLS/HTTPS é o pilar científico do trabalho.
* Assegurar exportação de figuras prontas para inserção no LaTeX/Google Docs em resolução alta (300 DPI).

**7. Mockups ou Referências Visuais**
* Diagrama de densidade bimodal de IAT e mapa de calor de correlação entre as 20+ features.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #19 (Rotulagem das Classes) e Issue #20 (Normalização).
* **Bloqueia:** Issue #24 (Seleção de Atributos via SU) e Issue #54 (Gráficos Finais).

**9. Como Testar (Plano de Teste)**
1. Executar `python -m src.data_processing.eda_analysis`.
2. Verificar se o diretório `docs/eda/` contém as imagens geradas (`correlation_matrix.png`, `iat_distribution.png`, etc.).
3. Abrir `data/reports/eda_summary.json` e validar a presença das métricas por classe.
4. Executar os testes via `pytest tests/test_eda_analysis.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `eda_analysis.py` implementado com testes automatizados.
* Gráficos gerados com legendas, títulos e eixos em português técnico e alta resolução.
* Relatório JSON estruturado com estatísticas descritivas por classe.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`backend`, `eda`, `data-visualization`, `statistics`, `tcc-figures`.

**13. Documentação Relacionada**
* Seção 3.2.2 (*Engenharia de Atributos Baseada em Fluxos*) e Capítulo 4 do TCC.

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #22: [Backend] Balanceamento de classes via técnicas de amostragem (SMOTE)**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** um módulo condicional de sobreamostragem sintética (SMOTE - Synthetic Minority Over-sampling Technique) aplicado estritamente na partição de treino,
> **para que** o desequilíbrio natural do tráfego de rede não induza viés nos classificadores do comitê, mantendo os conjuntos de validação e teste com dados 100% reais (Seção 3.2.4 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o conjunto de dados de treino**, **quando** a razão entre a classe minoritária e majoritária apresentar desbalanço significativo (ex.: proporção inferior a 40/60), **então** o algoritmo SMOTE deve sintetizar novas amostras na fronteira da classe minoritária até atingir paridade 50/50.
* **Dado o rigor científico estabelecido por Sommer & Paxson (2010)** (citado na Seção 3.2.4 do TCC), **quando** o balanceamento for aplicado, **então** em hipótese alguma amostras sintéticas devem ser inseridas nas partições de validação ou de teste de mundo aberto.
* **Dado o término da síntese de amostras**, **quando** salvo o resultado, **então** o dataset de treino balanceado deve ser gravado em `data/processed/train_balanced.csv` com relatório impresso da nova contagem de instâncias.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.balance_classes \
    --input-train-csv data/processed/train.csv \
    --output-train-csv data/processed/train_balanced.csv \
    --random-state 42
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando partição de treino data/processed/train.csv (4,700 amostras)...
[INFO] Contagem pré-balanceamento: Classe 0 = 2,820 (60%) | Classe 1 = 1,880 (40%)
[INFO] Desbalanceamento detectado (> limiar de 15% de desvio).
[INFO] Aplicando SMOTE(k_neighbors=5, random_state=42)...
[OK] Amostras sintéticas geradas para Classe 1: +940 instâncias
================ CONTAGEM PÓS-BALANCEAMENTO ================
  - Classe 0 (Benigno): 2,820 instâncias (50.0%)
  - Classe 1 (Apostas): 2,820 instâncias (50.0%)
  - Total no conjunto de treino: 5,640 instâncias
[SUCCESS] Dataset de treino balanceado salvo em data/processed/train_balanced.csv
```

**5. Componentes Envolvidos**
* `src/data_processing/balance_classes.py`: Módulo de amostragem sintética.
* `imblearn.over_sampling.SMOTE`: Biblioteca Scikit-Learn Imbalanced-Learn.
* `data/processed/train_balanced.csv`: Partição de treino balanceada.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.2.4 do TCC (*Balanceamento Sintético*), o SMOTE interpola vetores no espaço de atributos dos $k$ vizinhos mais próximos, prevenindo o problema de *overfitting* inerente à mera duplicação de instâncias (*random oversampling*).
* Semente pseudoaleatória fixa (`random_state=42`) para garantir reprodutibilidade completa dos resultados acadêmicos.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #20 (Normalização) e Issue #23 (Divisão Treino/Val/Teste).
* **Bloqueia:** Issue #25 (Regressão Logística), Issue #26 (Random Forest) e Issue #27 (XGBoost).

**9. Como Testar (Plano de Teste)**
1. Executar o balanceador fornecendo um CSV de treino desbalanceado.
2. Checar com asserções se a contagem da classe 0 e da classe 1 no CSV de saída é exatamente idêntica.
3. Confirmar que a partição de teste não sofreu nenhuma alteração.
4. Executar os testes automatizados via `pytest tests/test_balance_classes.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `balance_classes.py` implementado com tratamento de exceções.
* Testes unitários com casos de dados perfeitamente equilibrados (onde o SMOTE não altera nada) e dados desbalanceados.
* Validação de semente determinística.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`backend`, `data-balancing`, `smote`, `machine-learning`.

**13. Documentação Relacionada**
* Seção 3.2.4 do TCC (*Pré-processamento e Balanceamento*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #23: [Backend] Divisão do dataset em Treino, Validação e Teste**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** particionar o dataset limpo e rotulado em subconjuntos estratificados de Treino (70%), Validação (15%) e Teste de Mundo Aberto (15%), isolando completamente domínios nunca antes vistos na partição de teste,
> **para que** possamos avaliar a capacidade de generalização do comitê em condições operacionais reais de acordo com a hipótese de mundo aberto de Sommer & Paxson (2010) (Seção 3.2.4 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o dataset de fluxos**, **quando** a rotina de divisão for executada, **então** deve separar os dados nas proporções configuradas (70% treino, 15% validação e 15% teste).
* **Dado o requisito de Avaliação em Mundo Aberto (Open World Assumption)** (Seção 3.2.4 do TCC), **quando** montar a partição de teste independente, **então** todos os fluxos correspondentes a pelo menos 10 domínios específicos (ex.: 5 casas de apostas e 5 sites benignos) devem ser alocados exclusivamente no conjunto de teste, garantindo que o comitê nunca tenha visto tráfego daqueles domínios durante o treino.
* **Dado o término da partição**, **quando** validados os arquivos, **então** devem ser salvos em `data/processed/train.csv`, `data/processed/val.csv` e `data/processed/test_open_world.csv` com garantia de ausência de interseção de instâncias.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.split_dataset \
    --input-csv data/processed/flows_scaled.csv \
    --output-dir data/processed/ \
    --train-ratio 0.70 \
    --val-ratio 0.15 \
    --test-ratio 0.15 \
    --open-world-split \
    --seed 42
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando dataset escalonado data/processed/flows_scaled.csv (6,715 amostras)...
[INFO] Identificando domínios para reserva de Mundo Aberto...
[INFO] Domínios de aposta isolados para teste: betfair.com, kto.com, estrelabet.com... (5 domínios)
[INFO] Domínios benignos isolados para teste: bbc.com, wikipedia.org, uol.com.br... (5 domínios)
================ PARTIÇÃO DO DATASET ================
  - Treino (train.csv): 4,700 amostras (69.99%) [Estratificado]
  - Validação (val.csv): 1,007 amostras (15.00%) [Estratificado]
  - Teste Mundo Aberto (test_open_world.csv): 1,008 amostras (15.01%) [Domínios Inéditos]
[SUCCESS] Partições salvas em data/processed/
```

**5. Componentes Envolvidos**
* `src/data_processing/split_dataset.py`: Módulo de particionamento estratificado e domínio-isolado.
* `sklearn.model_selection.StratifiedShuffleSplit`.
* `data/processed/`: Diretório de saída com as três partições.

**6. Considerações Técnicas e Arquitetura**
* Conforme enfatizado na Seção 2.5 e 3.2.4 do TCC, sistemas de detecção que testam apenas domínios conhecidos no treino sofrem da falácia de alta acurácia ilusória; a reserva de teste de mundo aberto é obrigatória para validade acadêmica.
* Uso de semente fixa (`seed=42`) para assegurar paridade em reexecuções.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #20 (Normalização).
* **Bloqueia:** Issue #22 (Balanceamento SMOTE), Issue #24 (Seleção de Atributos) e todo o Grupo 4 de ML.

**9. Como Testar (Plano de Teste)**
1. Executar o script `split_dataset.py` com o dataset escalonado.
2. Inspecionar as três partições e verificar se a soma de linhas é igual ao total original.
3. Verificar programaticamente se nenhum domínio da partição `test_open_world.csv` aparece em `train.csv`.
4. Executar os testes via `pytest tests/test_split_dataset.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `split_dataset.py` implementado com validação de vazamento de domínios.
* Três arquivos CSV gerados e íntegros.
* Testes unitários validando proporções e isolamento de mundo aberto.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `data-splitting`, `open-world`, `train-test-split`.

**13. Documentação Relacionada**
* Seção 2.5 e Seção 3.2.4 do TCC (*Sinal de Alerta e Mundo Aberto*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #24: [Backend] Redução de dimensionalidade: Seleção de atributos mínimos via Incerteza Simétrica (SU)**

**1. História de Usuário (User Story)**
> **Como** pesquisador de sistemas embarcados do projeto,
> **eu quero** implementar o algoritmo de Incerteza Simétrica (Symmetrical Uncertainty - SU) baseado na teoria da informação para ranquear e selecionar o subconjunto ótimo e mínimo de características (top 6 a 10 atributos),
> **para que** o custo de processamento de CPU e o tempo de inferência do firewall em hardware limitado (0.5 vCPU, 512MB RAM) sejam reduzidos drasticamente sem perda sensível do poder discriminatório (RF04, RNF01, RNF03 e Seção 3.2.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o conjunto de dados de treino**, **quando** o cálculo de SU for executado para cada atributo numérico $X$ contra a classe binária $Y$, **então** o algoritmo deve calcular a entropia de Shannon individual $H(X)$, a entropia da classe $H(Y)$, a entropia conjunta $H(X, Y)$ e a Informação Mútua $I(X; Y) = H(X) + H(Y) - H(X, Y)$, derivando:
  $$SU(X, Y) = 2 \cdot \frac{H(X) + H(Y) - H(X, Y)}{H(X) + H(Y)}$$
  garantindo que o resultado de $SU(X, Y)$ esteja rigorosamente delimitado no intervalo $[0.0, 1.0]$ (Seção 3.2.3 do TCC e RF04).
* **Dado que** variáveis contínuas exigem discretização para cálculo de entropia de Shannon, **quando** computar as probabilidades, **então** o algoritmo deve aplicar discretização adaptativa por quantis (ex.: 10 a 20 bins) preservando a distribuição de probabilidades.
* **Dado o ranking decrescente de SU**, **quando** selecionado o corte de atributos mínimos (ex.: top $k=8$), **então** os nomes dos atributos selecionados e seus respectivos coeficientes devem ser serializados em `models/selected_features.json` para guiar os modelos de ML e o extrator em voo.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.symmetrical_uncertainty \
    --train-csv data/processed/train_balanced.csv \
    --top-k 8 \
    --output-json models/selected_features.json \
    --report-csv data/reports/su_ranking.csv
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando dados de treino balanceados (5,640 instâncias)...
[INFO] Executando cálculo de Incerteza Simétrica (SU) para 24 atributos...
[INFO] Discretização em 15 bins adaptativos concluída.
================ RANKING DE INCERTEZA SIMÉTRICA (TOP 8) ================
  1. fwd_iat_mean       -> SU: 0.7421 (Altíssimo poder discriminatório)
  2. pkt_len_mean       -> SU: 0.6985 (Diferenciação clara de payload)
  3. fwd_iat_std        -> SU: 0.6512
  4. bwd_pkt_len_mean   -> SU: 0.6104
  5. flow_duration      -> SU: 0.5892
  6. fwd_pkts_tot       -> SU: 0.5341
  7. bwd_iat_mean       -> SU: 0.5019
  8. pkt_len_std        -> SU: 0.4876
------------------------------------------------------------------------
Atributos descartados por redundância/baixa correlação: 16 características.
Redução dimensional: 24 features -> 8 features (66.7% de economia de computação).
[SUCCESS] Lista de features salvas em models/selected_features.json
[SUCCESS] Relatório completo salvo em data/reports/su_ranking.csv
```

**5. Componentes Envolvidos**
* `src/data_processing/symmetrical_uncertainty.py`: Implementação matemática do algoritmo SU.
* `scipy.stats.entropy`, `numpy`: Funções de entropia de Shannon e álgebra matricial.
* `models/selected_features.json`: Lista de atributos para produção.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com o Requisito RF04 e a Seção 3.2.3 do TCC (*Seleção de Atributos via Incerteza Simétrica*), a eliminação de atributos redundantes é o fator determinante que viabiliza a execução do firewall em 0.5 vCPU e latência inferior a 200ms (RNF01).
* O script deve emitir alertas se nenhum atributo ultrapassar $SU > 0.20$, prevenindo o treino com features desprovidas de correlação estatística.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #20 (Normalização) e Issue #23 (Divisão do Dataset).
* **Bloqueia:** Issue #25 (Regressão Logística), Issue #26 (Random Forest), Issue #27 (XGBoost) e Issue #35 (In-flight Extractor).

**9. Como Testar (Plano de Teste)**
1. Executar o script `symmetrical_uncertainty.py` no conjunto de treino.
2. Abrir o arquivo `models/selected_features.json` e verificar se a lista possui exatamente $k$ atributos e se todos os valores de SU estão entre $0$ e $1$.
3. Testar a consistência do algoritmo criando uma feature sintética perfeitamente correlacionada e verificar se ela atinge $SU pprox 1.0$.
4. Executar os testes automatizados via `pytest tests/test_symmetrical_uncertainty.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `symmetrical_uncertainty.py` implementado com rigor matemático.
* Testes unitários com casos sintéticos conhecidos passando com 100% de sucesso.
* Geração do arquivo `models/selected_features.json` pronto para consumo do pipeline de ML.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Requisito fundamental de baixo recurso).
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `dimensionality-reduction`, `information-theory`, `entropy`, `optimization`.

**13. Documentação Relacionada**
* Requisito RF04 (Redução de Dimensionalidade via Incerteza Simétrica).
* Requisito RNF01 (Latência Crítica) e RNF03 (Carga de CPU).
* Seção 3.2.3 do TCC (*Seleção de Atributos via Incerteza Simétrica*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

# 🧠 Grupo 4: Pipeline de Machine Learning

### **Issue #25: [Backend] Implementação da Regressão Logística (Voto de Minerva/Baseline)**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** implementar e treinar um classificador linear de Regressão Logística com regularização L2 sobre o subconjunto de características mínimas selecionadas por SU,
> **para que** ele sirva como linha de base (baseline) comparativa e atue como o voto de desempate (*tie-breaker*) ultra-rápido do comitê de decisão sem sobrecarregar a CPU em hardware limitado (RF05 e Seção 3.3.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o conjunto de treino balanceado** contendo apenas as características do `models/selected_features.json`, **quando** o modelo for treinado via `LogisticRegression(solver='lbfgs', penalty='l2', max_iter=500, random_state=42)`, **então** os pesos devem convergir sem alertas de não-convergência.
* **Dado que** o modelo atua em dispositivos restritos (RNF02 e RNF03), **quando** mensurada a latência de inferência individual para um vetor de entrada, **então** a predição deve ser executada em tempo inferior a 2 milissegundos.
* **Dado o treinamento concluído**, **quando** o modelo for avaliado na partição de validação, **então** deve atingir acurácia mínima de 80% e ser serializado em `models/logistic_regression.joblib` com tamanho em disco inferior a 2 MB.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.train_logistic_regression \
    --train-csv data/processed/train_balanced.csv \
    --val-csv data/processed/val.csv \
    --features-json models/selected_features.json \
    --output-model models/logistic_regression.joblib
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando partição de treino (5,640 amostras) com 8 features selecionadas...
[INFO] Treinando LogisticRegression(solver='lbfgs', C=1.0, max_iter=500)...
[INFO] Otimização convergida em 48 iterações.
================ AVALIAÇÃO NA VALIDAÇÃO ================
  - Acurácia: 83.42%
  - Precisão (Classe 1): 82.10%
  - Recall (Classe 1): 84.50%
  - F1-Score: 83.28%
  - Tempo médio de inferência por amostra: 0.42 ms
[SUCCESS] Modelo serializado em models/logistic_regression.joblib (48.2 KB)
```

**5. Componentes Envolvidos**
* `src/brain/train_logistic_regression.py`: Script de treinamento e validação.
* `sklearn.linear_model.LogisticRegression`: Algoritmo linear.
* `models/logistic_regression.joblib`: Modelo serializado.

**6. Considerações Técnicas e Arquitetura**
* Conforme detalhado na Seção 3.3.1 do TCC (*Regressão Logística - Tie-breaker*), sua complexidade computacional é $O(d)$ para inferência (onde $d$ é o número de atributos), o que representa um custo negligenciável de CPU e memória.
* Regularização L2 configurada para mitigar pesos desproporcionais e evitar overfitting.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #22 (Balanceamento SMOTE) e Issue #24 (Seleção de Atributos).
* **Bloqueia:** Issue #28 (Comitê de Votação Ensemble) e Issue #30 (Validação Cruzada).

**9. Como Testar (Plano de Teste)**
1. Executar o script de treino com as partições de treino e validação.
2. Carregar o arquivo `logistic_regression.joblib` gerado e realizar predições em lote de 100 amostras.
3. Medir o tempo de resposta e certificar ausência de exceções.
4. Executar os testes automatizados via `pytest tests/test_train_logistic_regression.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `train_logistic_regression.py` implementado com testes automatizados.
* Modelo treinado, avaliado e salvo com métricas registradas.
* Tempo de inferência unitário comprovado $< 2ms$.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`backend`, `machine-learning`, `logistic-regression`, `baseline`.

**13. Documentação Relacionada**
* Requisito RF05 (Treinamento de Modelos) e RF06 (Persistência).
* Seção 3.3.1 do TCC (*Regressão Logística como Voto de Minerva*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #26: [Backend] Implementação e treinamento do classificador Random Forest**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** implementar e treinar um classificador Random Forest (técnica de Bagging) com restrição estrita no número de árvores e profundidade máxima (`max_depth`),
> **para que** ele atue como o pilar de estabilização do comitê, reduzindo a variância e mitigando sobreajuste (overfitting) sem exceder a quota restrita de memória RAM de 512MB (RF05, RNF02 e Seção 3.3.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o dataset de treino reduzido**, **quando** o Random Forest for instanciado, **então** seus hiperparâmetros devem restringir o número de estimadores (ex.: `n_estimators <= 50`) e a profundidade máxima (ex.: `max_depth <= 12`) para manter o modelo compacto e prevenir explosão de nós na memória RAM (Seção 3.3.3 do TCC).
* **Dado o processo de treinamento**, **quando** for avaliado na partição de validação, **então** deve alcançar F1-Score $\ge 0.88$ na detecção de tráfego de apostas.
* **Dado a persistência do modelo**, **quando** exportado para `models/random_forest.joblib`, **então** o tamanho do artefato serializado em disco não deve ultrapassar 15 MB e deve ser carregável em menos de 1 segundo.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.train_random_forest \
    --train-csv data/processed/train_balanced.csv \
    --val-csv data/processed/val.csv \
    --features-json models/selected_features.json \
    --n-estimators 50 \
    --max-depth 12 \
    --output-model models/random_forest.joblib
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando dados de treino com 8 features de Incerteza Simétrica...
[INFO] Treinando RandomForestClassifier(n_estimators=50, max_depth=12, n_jobs=2)...
[INFO] Treinamento concluído em 3.2 segundos.
================ AVALIAÇÃO NA VALIDAÇÃO ================
  - Acurácia: 91.85%
  - Precisão (Classe 1): 90.70%
  - Recall (Classe 1): 92.40%
  - F1-Score: 91.54%
  - Tempo médio de inferência por amostra: 2.1 ms
[SUCCESS] Modelo serializado em models/random_forest.joblib (8.4 MB)
```

**5. Componentes Envolvidos**
* `src/brain/train_random_forest.py`: Script de treino e validação.
* `sklearn.ensemble.RandomForestClassifier`: Classificador ensemble por Bagging.
* `models/random_forest.joblib`: Modelo serializado.

**6. Considerações Técnicas e Arquitetura**
* Conforme a Seção 3.3.1 e 3.3.3 do TCC (*Poda de Árvores*), o Random Forest não podado pode alocar centenas de megabytes em árvores profundas, violando o RNF02 (limite de 512MB RAM). A poda via `max_depth` e `min_samples_split` é mandatória.
* Paralelismo de treino controlado (`n_jobs=2` ou `n_jobs=1`) para evitar sobrecarga de CPU no ambiente Docker restrito (RNF03).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #22 (Balanceamento SMOTE) e Issue #24 (Seleção de Atributos).
* **Bloqueia:** Issue #28 (Comitê de Votação Ensemble) e Issue #30 (Validação Cruzada).

**9. Como Testar (Plano de Teste)**
1. Treinar o modelo com os parâmetros podados.
2. Avaliar no conjunto de validação e certificar $F1 \ge 0.88$.
3. Verificar o tamanho do arquivo `.joblib` em disco com asserção `<= 15MB`.
4. Executar os testes automatizados via `pytest tests/test_train_random_forest.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `train_random_forest.py` implementado com testes automatizados.
* Poda de hiperparâmetros validada por testes de limite de tamanho em disco.
* Cobertura de testes superior a 85%.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `machine-learning`, `random-forest`, `bagging`, `pruning`.

**13. Documentação Relacionada**
* Requisito RF05 (Treinamento de Modelos) e RNF02 (Memória RAM).
* Seção 3.3.1 e 3.3.3 do TCC (*Random Forest e Restrições para Baixos Recursos*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #27: [Backend] Implementação e treinamento do classificador XGBoost**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** implementar e treinar um classificador XGBoost (Gradient Boosting) com árvores rasas e parâmetros otimizados para baixo consumo de CPU,
> **para que** ele identifique fronteiras de decisão complexas e sutis em tráfego criptografado, atuando como o componente de alta precisão do comitê (RF05, RNF03 e Seção 3.3.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o conjunto de treino reduzido**, **quando** o classificador XGBoost for parametrizado, **então** deve configurar árvores com profundidade controlada (ex.: `max_depth <= 6`), estimadores reduzidos (ex.: `n_estimators <= 60`) e taxa de aprendizado moderada (`learning_rate=0.1`) para evitar contenção de CPU durante a inferência em tempo real.
* **Dado o processo de treino com função de perda logística binária** (`binary:logistic`), **quando** for avaliado no conjunto de validação, **então** deve alcançar precisão $\ge 0.90$ na classe de apostas com tempo de resposta individual inferior a 3ms.
* **Dado o treinamento concluído**, **quando** o modelo for exportado, **então** deve ser salvo em `models/xgboost.joblib` (tamanho em disco $< 5 MB$) e ser compatível com carregamento assíncrono sem dependências pesadas de GPU.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.train_xgboost \
    --train-csv data/processed/train_balanced.csv \
    --val-csv data/processed/val.csv \
    --features-json models/selected_features.json \
    --n-estimators 60 \
    --max-depth 6 \
    --learning-rate 0.1 \
    --output-model models/xgboost.joblib
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando dados de treino com 8 features selecionadas...
[INFO] Treinando XGBClassifier(n_estimators=60, max_depth=6, eval_metric='logloss')...
[INFO] Treinamento concluído em 2.8 segundos.
================ AVALIAÇÃO NA VALIDAÇÃO ================
  - Acurácia: 93.15%
  - Precisão (Classe 1): 92.40%
  - Recall (Classe 1): 93.80%
  - F1-Score: 93.09%
  - Tempo médio de inferência por amostra: 1.8 ms
[SUCCESS] Modelo serializado em models/xgboost.joblib (2.8 MB)
```

**5. Componentes Envolvidos**
* `src/brain/train_xgboost.py`: Módulo de treinamento do XGBoost.
* `xgboost.XGBClassifier`: Algoritmo de boosting.
* `models/xgboost.joblib`: Modelo serializado.

**6. Considerações Técnicas e Arquitetura**
* Conforme a Seção 3.3.1 do TCC (*XGBoost - Boosting*), o modelo corrige iterativamente os resíduos dos estimadores anteriores. Em dispositivos de borda, o cálculo de árvores densas pode gerar contenção de CPU que afete o encaminhamento de pacotes pelo kernel (RNF03). Daí a necessidade da restrição estrita em `max_depth=6`.
* Configuração explícita de `n_jobs=1` ou `2` para respeitar a quota de 0.5 vCPU do Cenário B.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #22 (Balanceamento SMOTE) e Issue #24 (Seleção de Atributos).
* **Bloqueia:** Issue #28 (Comitê de Votação Ensemble) e Issue #30 (Validação Cruzada).

**9. Como Testar (Plano de Teste)**
1. Executar o script de treino com as partições de treino e validação.
2. Inspecionar o log de convergência e validar se o F1-Score é $\ge 0.90$.
3. Carregar o arquivo `xgboost.joblib` e medir a latência média de 100 inferências consecutivas.
4. Executar os testes automatizados via `pytest tests/test_train_xgboost.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `train_xgboost.py` implementado com testes automatizados.
* Modelo treinado, validado e serializado com tamanho $< 5MB$.
* Validação de conformidade com tempo de inferência $< 3ms$.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `machine-learning`, `xgboost`, `boosting`, `optimization`.

**13. Documentação Relacionada**
* Requisito RF05 (Treinamento de Modelos) e RNF03 (Carga de CPU).
* Seção 3.3.1 do TCC (*XGBoost na Arquitetura do Comitê*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #28: [Backend] Implementação do Comitê de Votação Majoritária (Ensemble)**

**1. História de Usuário (User Story)**
> **Como** arquiteto de software do projeto,
> **eu quero** implementar o motor do Comitê de Decisão baseado em Votação Majoritária Rígida (*Hard Voting*), que submete paralelamente o vetor de atributos aos três modelos (Random Forest, XGBoost e Regressão Logística) e dispara veredito de bloqueio se e somente se $\sum Votos \ge 2$,
> **para que** a divergência estatística entre os algoritmos de Bagging, Boosting e Linear reduza a taxa de falsos positivos operacionais no firewall (RF07 e Seção 3.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado um vetor numérico de características de fluxo**, **quando** for submetido ao motor do comitê, **então** deve acionar os três classificadores de forma isolada, gerando os votos individuais $v_{RF}, v_{XGB}, v_{LR} \in \{0, 1\}$.
* **Dado que o bloqueio em redes exige alta confiabilidade**, **quando** for agregada a soma dos votos, **então** o veredito final deve ser `1` (Aposta / Bloquear via DROP) apenas se $\sum_{i=1}^3 v_i \ge 2$; caso contrário, o veredito deve ser `0` (Benigno / Permitir) (Seção 3.3.2 do TCC e RF07).
* **Dado que o motor deve registrar auditoria completa**, **quando** o veredito for emitido, **então** deve retornar a distribuição exata dos votos ex.: `[1, 1, 0]`, o rótulo final e o tempo total de inferência $T_{decision}$ em microssegundos (RNF08).
* **Dado a restrição de latência crítica** (RNF01), **quando** o comitê executar uma decisão completa em hardware limitado, **então** o tempo de inferência conjunto não deve ultrapassar 15 milissegundos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.ensemble_engine \
    --models-dir models/ \
    --features-json models/selected_features.json \
    --test-sample "[0.12, 0.45, 0.88, 0.05, 0.32, 0.18, 0.64, 0.22]"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Inicializando Comitê de Votação (Hard Voting)...
[LOAD] models/random_forest.joblib carregado com sucesso.
[LOAD] models/xgboost.joblib carregado com sucesso.
[LOAD] models/logistic_regression.joblib carregado com sucesso.
[INFERENCE] Vetor de 8 características submetido ao comitê.
================ VEREDITO DO COMITÊ ================
  - Voto Random Forest (Bagging): 1 (Aposta)
  - Voto XGBoost (Boosting): 1 (Aposta)
  - Voto Regressão Logística (Tie-breaker): 0 (Benigno)
  - Distribuição dos votos: [1, 1, 0]
  - Soma dos votos positivos: 2 / 3 (Consenso Atingido: >= 2)
  - Veredito Final: 1 (APOSTA -> APLICAR DROP)
  - Tempo de inferência do comitê: 4.82 ms
```

**5. Componentes Envolvidos**
* `src/brain/ensemble_engine.py`: Motor central de votação majoritária.
* Modelos serializados em `models/` (RF, XGBoost, Regressão Logística).
* `models/selected_features.json`.

**6. Considerações Técnicas e Arquitetura**
* Conforme formalizado na Seção 3.3.2 do TCC (*Mecanismo de Decisão e Lógica de Consenso*), a probabilidade de dois classificadores com princípios matemáticos distintos cometerem o mesmo erro de generalização simultaneamente é significativamente menor que a de um classificador isolado.
* Implementar pooling de inferência eficiente em Python sem recarregar arquivos do disco a cada requisição (manter modelos instanciados na memória, consumindo $< 150MB$ de RAM para respeitar o RNF02).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #25 (Regressão Logística), Issue #26 (Random Forest) e Issue #27 (XGBoost).
* **Bloqueia:** Issue #29 (Tuning), Issue #30 (Validação Cruzada) e Issue #37 (Lógica de Decisão do Firewall).

**9. Como Testar (Plano de Teste)**
1. Instanciar o `EnsembleEngine` e passar amostras sintéticas com votos divergentes `[1, 0, 0]`, `[1, 1, 0]`, `[1, 1, 1]`, `[0, 0, 0]`.
2. Verificar se o veredito retornado é estritamente `1` apenas para $\sum \ge 2$.
3. Medir a latência média de 500 chamadas em lote e verificar se média $\le 15ms$.
4. Executar os testes automatizados via `pytest tests/test_ensemble_engine.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Classe `EnsembleEngine` implementada com tratamento robusto para entradas inválidas.
* Lógica de Hard Voting $\sum \ge 2$ testada para todas as 8 combinações binárias possíveis de votos.
* Cobertura de testes unitários superior a 90%.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Coração inteligente do projeto).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `ensemble`, `hard-voting`, `consensus`, `machine-learning`.

**13. Documentação Relacionada**
* Requisito RF07 (Lógica de Votação Hard Voting).
* Requisito RNF01 (Latência) e RNF08 (Interpretabilidade de Log).
* Seção 3.3 do TCC (*Arquitetura do Comitê de Votação*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #29: [Backend] Tuning de hiperparâmetros (Foco em modelos "leves")**

**1. História de Usuário (User Story)**
> **Como** cientista de dados do projeto,
> **eu quero** realizar a busca e sintonia de hiperparâmetros (via Optuna ou GridSearchCV) com função objetivo penalizada por tempo de inferência e profundidade de árvore,
> **para que** encontremos a configuração ideal com o menor footprint computacional e latência mínima sem sacrificar mais de 1.5% da acurácia global (RNF01, RNF02 e Seção 3.3.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o espaço de busca de hiperparâmetros**, **quando** o processo de otimização for executado, **então** deve testar variações de `max_depth` (4 a 12), `n_estimators` (20 a 70) e taxas de aprendizado, descartando candidatos cujo tempo de predição exceda 10ms por amostra.
* **Dado que o objetivo central é baixo consumo**, **quando** selecionada a melhor configuração pelo algoritmo, **então** a redução do tamanho do modelo e tempo de inferência deve ser de pelo menos 25% em relação ao modelo sem poda, com perda de F1-Score não superior a 1.5%.
* **Dado a conclusão do tuning**, **quando** exportados os parâmetros ótimos, **então** devem ser gravados em `config/ml_hyperparameters.yaml` para uso padrão nos scripts de treino de produção.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.tune_hyperparameters \
    --train-csv data/processed/train_balanced.csv \
    --val-csv data/processed/val.csv \
    --features-json models/selected_features.json \
    --n-trials 50 \
    --output-yaml config/ml_hyperparameters.yaml
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Iniciando otimização com Optuna (50 ensaios, foco em modelos leves)...
[TRIAL 12] RF: n_estimators=45, max_depth=10 | Latência: 1.8ms | F1: 91.20% [MELHOR]
[TRIAL 28] XGB: n_estimators=50, max_depth=5 | Latência: 1.4ms | F1: 92.80% [MELHOR]
================ RESUMO DO TUNING DE HIPERPARÂMETROS ================
Random Forest Ótimo:
  - n_estimators: 45 (Economia de 10% de RAM)
  - max_depth: 10 (Árvores podadas)
  - F1-Score: 91.20% (Apenas 0.34% abaixo do modelo sem limites)
XGBoost Ótimo:
  - n_estimators: 50
  - max_depth: 5
  - learning_rate: 0.08
  - F1-Score: 92.80%
[SUCCESS] Configurações de produção salvas em config/ml_hyperparameters.yaml
```

**5. Componentes Envolvidos**
* `src/brain/tune_hyperparameters.py`: Otimizador com Optuna/Scikit-Learn.
* `config/ml_hyperparameters.yaml`: Configuração formal dos modelos.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com a Seção 3.3.3 do TCC (*Restrições e Ajustes para Baixos Recursos*), a busca pela acurácia cega é expressamente evitada em benefício da eficiência operacional em dispositivos embarcados.
* Limitar a busca a 50 trials para evitar alto consumo de CPU do host de desenvolvimento.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #28 (Comitê Ensemble).
* **Bloqueia:** Issue #30 (Validação Cruzada) e Issue #32 (Exportação do Modelo).

**9. Como Testar (Plano de Teste)**
1. Executar o script de tuning com número reduzido de trials (`--n-trials 5`).
2. Verificar se o arquivo `config/ml_hyperparameters.yaml` é gerado e contém seções para os três modelos.
3. Testar o retreinamento dos modelos consumindo o arquivo YAML de configuração.
4. Executar os testes automatizados via `pytest tests/test_tune_hyperparameters.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `tune_hyperparameters.py` funcional com métrica combinada de acurácia e tempo.
* Arquivo YAML de parâmetros gerado e integrado ao pipeline.
* Testes unitários passando com sucesso.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`backend`, `hyperparameter-tuning`, `optuna`, `optimization`, `lightweight`.

**13. Documentação Relacionada**
* Seção 3.3.3 do TCC (*Restrições e Ajustes para Baixos Recursos*).
* Requisito RNF01 (Latência) e RNF02 (Memória RAM).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #30: [Backend] Avaliação via validação cruzada ($K$-Fold Cross Validation)**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** executar validação cruzada estratificada em $k=5$ dobras (*5-Fold Stratified Cross-Validation*) sobre cada modelo individual e sobre o Comitê de Votação,
> **para que** possamos comprovar a estabilidade estatística do sistema e validar cientificamente se o Ensemble reduz a variância das predições com significância estatística (Seção 3.4.4 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o dataset de treino completo**, **quando** a validação cruzada for executada com $k=5$ dobras estratificadas, **então** a proporção entre classes deve ser rigorosamente idêntica em todas as dobras de treino e validação.
* **Dado cada dobra processada**, **quando** calculadas as métricas de Acurácia, Precisão, Recall e F1-Score para a Regressão Logística, Random Forest, XGBoost e o Comitê Ensemble, **então** devem ser calculadas a média e o desvio padrão ($\mu \pm \sigma$) de cada técnica.
* **Dado os resultados consolidados**, **quando** realizada a comparação estatística (teste t pareado ou teste de Wilcoxon com $lpha=0.05$), **então** deve ser verificado se a superioridade do Comitê de Votação frente ao melhor modelo individual é estatisticamente significativa e gravada em `docs/evaluation/kfold_results.json`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.cross_validation \
    --train-csv data/processed/train_balanced.csv \
    --features-json models/selected_features.json \
    --k-folds 5 \
    --output-json docs/evaluation/kfold_results.json \
    --output-table docs/evaluation/kfold_table.md
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Iniciando 5-Fold Stratified Cross Validation (5,640 amostras)...
[PROGRESS] Processando Fold 1/5...
[PROGRESS] Processando Fold 3/5...
[PROGRESS] Processando Fold 5/5...
================ RESULTADOS 5-FOLD (MÉDIA ± DESVIO PADRÃO) ================
Modelo             | Acurácia (%)    | Precisão (%)    | Recall (%)      | F1-Score (%)
-------------------|-----------------|-----------------|-----------------|----------------
Regressão Logística| 82.40 ± 0.85    | 81.10 ± 1.10    | 83.20 ± 0.95    | 82.13 ± 0.82
Random Forest      | 91.50 ± 0.42    | 90.80 ± 0.55    | 92.10 ± 0.60    | 91.44 ± 0.38
XGBoost            | 92.80 ± 0.38    | 92.10 ± 0.48    | 93.40 ± 0.52    | 92.74 ± 0.35
Comitê (Hard Vote) | 93.65 ± 0.22    | 93.20 ± 0.30    | 94.10 ± 0.35    | 93.64 ± 0.18
----------------------------------------------------------------------------
[ESTATÍSTICA] Comitê vs XGBoost: p-valor = 0.0182 (Ganho estatisticamente significativo a p < 0.05)
[ESTATÍSTICA] Desvio padrão do Comitê: 0.18% (Menor variância confirmada, provando estabilização)
[SUCCESS] Resultados salvos em docs/evaluation/kfold_results.json e kfold_table.md
```

**5. Componentes Envolvidos**
* `src/brain/cross_validation.py`: Módulo de validação estatística k-fold.
* `sklearn.model_selection.StratifiedKFold`, `scipy.stats`.
* `docs/evaluation/`: Diretório de saída com tabela Markdown e relatório JSON.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com a Seção 3.4.4 do TCC (*Validação Estatística sob Restrição - Trade-off*), a prova da redução do desvio padrão ($\sigma$) é a evidência metodológica que justifica o uso do Ensemble frente a um classificador único.
* O script deve exportar a tabela pronta em sintaxe Markdown para inclusão direta no Capítulo 4 do TCC.

**7. Mockups ou Referências Visuais**
* Tabela comparativa dos 5 folds com médias e desvios padrão.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #28 (Comitê Ensemble) e Issue #29 (Tuning).
* **Bloqueia:** Issue #31 (Geração de Métricas Finais) e Issue #54 (Gráficos Finais).

**9. Como Testar (Plano de Teste)**
1. Executar a validação cruzada com $k=3$ para teste rápido de fumaça.
2. Inspecionar o arquivo `docs/evaluation/kfold_results.json` e conferir a presença dos campos `mean`, `std` e `p_value`.
3. Executar com $k=5$ e verificar se a tabela Markdown é gerada com formatação válida.
4. Executar os testes automatizados via `pytest tests/test_cross_validation.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `cross_validation.py` implementado com testes automatizados.
* Tabela formatada e teste estatístico de Wilcoxon/t-Student implementado.
* Validação de reprodutibilidade com semente fixa.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Rigor acadêmico essencial para a banca).
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `cross-validation`, `statistics`, `t-test`, `academic-validation`.

**13. Documentação Relacionada**
* Seção 3.4.4 do TCC (*Validação Estatística sob Restrição*).
* Capítulo 4 (*Resultados Esperados e Discussão*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #31: [Backend] Geração de métricas (Acurácia, F1-Score, Precisão, Recall)**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** calcular e consolidar as métricas definitivas de desempenho (Matriz de Confusão, Taxa de Falsos Positivos - FPR, Curva ROC e AUC) na partição independente de teste de Mundo Aberto,
> **para que** possamos comprovar a eficácia do firewall e garantir que a taxa de falsos positivos em tráfego nunca visto seja estritamente inferior a 5% (RNF06 e Seção 3.4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o Comitê Ensemble final** e a partição de teste `test_open_world.csv`, **quando** executada a avaliação de mundo aberto, **então** as métricas de Acurácia, Precisão, Recall, F1-Score Macro e AUC-ROC devem ser extraídas e tabuladas.
* **Dado que o bloqueio indevido de sites legítimos é uma falha operacional crítica** (Seção 3.4.5 do TCC), **quando** for gerada a Matriz de Confusão, **então** a taxa de Falsos Positivos ($FPR = \frac{FP}{FP + TN}$) não deve ultrapassar o teto estipulado de 5.0%.
* **Dado a geração dos dados**, **quando** concluída a rotina, **então** deve salvar o relatório numérico em `docs/evaluation/metrics_summary.json` e gerar os gráficos da Matriz de Confusão e da Curva ROC em `docs/evaluation/roc_curve.png`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.evaluate_metrics \
    --models-dir models/ \
    --test-csv data/processed/test_open_world.csv \
    --output-dir docs/evaluation/
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando partição de teste de Mundo Aberto (1,008 instâncias inéditas)...
[INFERENCE] Submetendo ao Comitê de Votação (Ensemble)...
================ MATRIZ DE CONFUSÃO (MUNDO ABERTO) ================
Verdadeiro \ Predito | Benigno (0)  | Apostas (1)
---------------------|--------------|------------
Benigno (0)          | 505 (TN)     | 18 (FP)
Apostas (1)          | 42 (FN)      | 443 (TP)
-------------------------------------------------------------------
MÉTRICAS CONSOLIDADAS:
  - Acurácia Global: 94.05%
  - Precisão (Classe 1): 96.09%
  - Recall (Sensibilidade): 91.34%
  - F1-Score: 93.65%
  - Taxa de Falsos Positivos (FPR): 3.44% (Meta cumprida: FPR < 5.0%)
  - Área sob a Curva ROC (AUC): 0.962
[SUCCESS] Gráfico da curva ROC salvo em docs/evaluation/roc_curve.png
[SUCCESS] Métricas consolidadas salvas em docs/evaluation/metrics_summary.json
```

**5. Componentes Envolvidos**
* `src/brain/evaluate_metrics.py`: Calculador de métricas e gerador de gráficos.
* `sklearn.metrics` (confusion_matrix, roc_curve, auc, classification_report).
* `docs/evaluation/`: Artefatos de métricas do TCC.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RNF06 e a Seção 3.4.5 do TCC (*Critérios de Rejeição da Hipótese*), se a taxa de falsos positivos em sites de controle exceder 5%, a hipótese do TCC é sumariamente rejeitada. Portanto, a medição precisa do FPR é um dos pontos focais da pesquisa.
* Armazenamento das probabilidades contínuas médias do ensemble para permitir o traçado exato da Curva ROC.

**7. Mockups ou Referências Visuais**
* Imagem da Curva ROC e mapa de calor da Matriz de Confusão.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #30 (Validação Cruzada) e Issue #23 (Partição de Mundo Aberto).
* **Bloqueia:** Issue #32 (Exportação) e Issue #54 (Gráficos Finais).

**9. Como Testar (Plano de Teste)**
1. Executar o script no arquivo de teste independente.
2. Abrir o arquivo `metrics_summary.json` e verificar se `false_positive_rate <= 0.05`.
3. Inspecionar visualmente o arquivo `roc_curve.png`.
4. Executar os testes automatizados via `pytest tests/test_evaluate_metrics.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `evaluate_metrics.py` implementado com testes automatizados.
* Matriz de confusão, relatório de classificação e curva ROC gerados com sucesso.
* Comprovação de conformidade com o critério de $FPR < 5\%$.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Validação da hipótese acadêmica).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `metrics`, `roc-auc`, `confusion-matrix`, `open-world-evaluation`.

**13. Documentação Relacionada**
* Seção 3.4.5 do TCC (*Critérios de Rejeição da Hipótese*).
* Seção 4.1 do TCC (*Desempenho e Robustez de Classificação da IA*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #32: [Backend] Exportação do modelo final treinado (pickle/joblib)**

**1. História de Usuário (User Story)**
> **Como** engenheiro de software do projeto,
> **eu quero** um script automatizado que serialize e empacote os modelos finais treinados, o scaler ajustado e os metadados de features selecionadas em arquivos comprimidos `.joblib` com manifesto de versão (SHA-256),
> **para que** o container do firewall possa inicializar o motor de decisão em tempo de execução sem carregar dependências do pipeline de treino (RF06 e RNF02).

**2. Critérios de Aceitação (AC)**
* **Dado que os modelos foram aprovados em todas as métricas**, **quando** o exportador for executado, **então** deve salvar em `models/production/` os arquivos `random_forest.joblib`, `xgboost.joblib`, `logistic_regression.joblib` e `scaler.joblib` utilizando compressão zlib nível 3.
* **Dado que o motor deve inicializar rapidamente no container**, **quando** um script de teste carregar todos os artefatos de `models/production/`, **então** o tempo total de carregamento e alocação na RAM deve ser inferior a 3 segundos.
* **Dado o requisito de rastreabilidade**, **quando** os arquivos forem exportados, **então** deve ser gerado um arquivo `models/production/manifest.json` contendo o timestamp de exportação, hashes SHA-256 de cada modelo, versões das bibliotecas e lista ordenada das features esperadas.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.export_pipeline \
    --source-dir models/ \
    --output-dir models/production/ \
    --compress-level 3
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Iniciando empacotamento do pipeline de inferência...
[COMPRESS] models/random_forest.joblib -> 7.82 MB (SHA256: e3b0c442...)
[COMPRESS] models/xgboost.joblib -> 2.45 MB (SHA256: 4b227777...)
[COMPRESS] models/logistic_regression.joblib -> 0.04 MB (SHA256: ef2d1270...)
[COMPRESS] models/scaler.joblib -> 0.01 MB (SHA256: a1b2c3d4...)
[INFO] Tamanho consolidado do pacote de inferência: 10.32 MB
[VERIFY] Teste de carregamento em memória: Sucesso em 1.42s (RAM: 86 MB)
[SUCCESS] Manifesto exportado em models/production/manifest.json
```

**5. Componentes Envolvidos**
* `src/brain/export_pipeline.py`: Empacotador e validador de integridade.
* `models/production/`: Diretório de artefatos prontos para deploy.
* `models/production/manifest.json`: Manifesto de integridade com hashes SHA-256.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RF06 (*Persistência de Modelos*) e RNF02 (*Restrição de Memória RAM*), o empacotamento leve permite que o container do firewall inicie sem depender de ferramentas de compilação ou do Scikit-Learn completo para treino.
* Verificação automática de compatibilidade de versões do Python e do Joblib.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #31 (Geração de Métricas).
* **Bloqueia:** Issue #33 (Medição de Footprint) e Issue #37 (Lógica de Decisão do Firewall).

**9. Como Testar (Plano de Teste)**
1. Executar o empacotador de produção.
2. Inspecionar o manifesto JSON e checar a integridade dos hashes SHA-256 com comando `sha256sum`.
3. Executar script de inicialização a frio e medir tempo de carregamento em memória.
4. Executar os testes automatizados via `pytest tests/test_export_pipeline.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `export_pipeline.py` implementado com testes automatizados.
* Pacote de produção exportado com tamanho consolidado $< 15MB$.
* Manifesto com SHA-256 gerado e validado.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `model-export`, `serialization`, `joblib`, `devops`.

**13. Documentação Relacionada**
* Requisito RF06 (Persistência de Modelos).
* Requisito RNF02 (Memória RAM).
* Seção 3.3.3 do TCC (*Restrições para Baixos Recursos*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #33: [Backend] Medição do tamanho em disco e memória dos modelos treinados**

**1. História de Usuário (User Story)**
> **Como** arquiteto do projeto,
> **eu quero** desenvolver um utilitário de benchmarking para medir com precisão o tamanho de armazenamento em disco e a memória RAM residente (RSS) consumida pelos modelos após a instanciação no Python,
> **para que** possamos comprovar que o footprint do motor de IA respeita estritamente a quota de 512MB/812MB estabelecida nos Cenários de Hardware B e C (RNF02 e Seção 3.4.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o diretório de produção** `models/production/`, **quando** o utilitário inspecionar os arquivos, **então** deve somar o tamanho total em disco e alertar caso ultrapasse 20 MB.
* **Dado um processo Python simulando o motor de inferência**, **quando** os três modelos e o scaler forem instanciados na memória principal, **então** o incremento de memória RAM residente (RSS) medido via `psutil` ou `tracemalloc` deve ser inferior a 150 MB (garantindo ampla margem para o buffer de rede dentro dos 512MB totais do container).
* **Dado a execução da medição**, **quando** o script finalizar, **então** deve exportar um relatório detalhado discriminando o footprint individual de cada modelo em `docs/evaluation/model_footprint_report.json`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.measure_footprint \
    --models-dir models/production/ \
    --output-json docs/evaluation/model_footprint_report.json
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[BENCHMARK] Medindo footprint de armazenamento em models/production/...
  - random_forest.joblib: 7.82 MB em disco
  - xgboost.joblib: 2.45 MB em disco
  - logistic_regression.joblib: 0.04 MB em disco
  - scaler.joblib: 0.01 MB em disco
  - Total em disco: 10.32 MB (Conforme: < 20 MB)
[BENCHMARK] Medindo footprint de memória RAM residente (RSS)...
  - Baseline do processo Python: 22.4 MB
  - RAM após carregar Scaler: 22.6 MB (+0.2 MB)
  - RAM após carregar Regressão Logística: 23.8 MB (+1.2 MB)
  - RAM após carregar Random Forest: 68.4 MB (+44.6 MB)
  - RAM após carregar XGBoost: 98.1 MB (+29.7 MB)
================ SÍNTESE DO FOOTPRINT DE IA ================
  - Consumo total de RAM do motor: 98.1 MB RSS (Incremento líquido: 75.7 MB)
  - Margem disponível no limite de 512MB: 413.9 MB (80.8% livre para buffers de rede)
[SUCCESS] Relatório salvo em docs/evaluation/model_footprint_report.json
```

**5. Componentes Envolvidos**
* `src/brain/measure_footprint.py`: Script de auditoria de memória e disco.
* `psutil`, `tracemalloc`, `os`: Ferramentas de medição de recursos de processo.
* `docs/evaluation/model_footprint_report.json`: Relatório consolidado.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade direta com a Seção 3.4.1 do TCC (*Avaliação de Eficiência Computacional - Footprint*) e com o Requisito RNF02, a quantificação exata da RAM consumida pelos modelos é premissa obrigatória para provar a viabilidade em roteadores domésticos.
* Medição isolada de pico e alocação contínua estável.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #07 (Limites de Recursos Docker) e Issue #32 (Exportação de Modelos).
* **Bloqueia:** Issue #53 (Benchmark de RAM do Motor de IA).

**9. Como Testar (Plano de Teste)**
1. Executar o script de medição sobre os modelos serializados em `models/production/`.
2. Validar se o arquivo `model_footprint_report.json` foi gerado e contém valores válidos de RAM (em MB) e disco (em MB).
3. Confirmar que o incremento líquido de RAM dos modelos é estritamente menor que 150 MB.
4. Executar os testes automatizados via `pytest tests/test_measure_footprint.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `measure_footprint.py` implementado com testes automatizados.
* Relatório JSON estruturado gerado e documentado.
* Comprovação de conformidade com o limite de 512MB RAM do RNF02.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `footprint`, `memory-profiling`, `psutil`, `benchmarking`.

**13. Documentação Relacionada**
* Requisito RNF02 (Restrição de Memória RAM - 512MB).
* Seção 3.4.1 do TCC (*Avaliação de Eficiência Computacional - Footprint*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

# 🛡️ Grupo 5: Motor do Firewall e Integração

### **Issue #34: [Infraestrutura/Backend] Script de captura e inspeção de pacotes em tempo real**

**1. História de Usuário (User Story)**
> **Como** desenvolvedor do sistema de segurança,
> **eu quero** um serviço daemon de captura passiva não intrusiva de pacotes em tempo real (utilizando Scapy/AsyncSniffer ou raw sockets Linux) escutando a interface virtual do gateway,
> **para que** pacotes transitando pelo firewall sejam espelhados para análise comportamental sem retardar o fluxo de dados original no kernel (RF02 e Seção 3.1.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que** o container `firewall_gateway` está ativo na rede virtual em modo bridge, **quando** o daemon de captura for inicializado, **então** deve escutar passivamente a interface de rede interna (ex.: `eth0` ou `br0`) utilizando cópias de pacotes via socket raw ou `AsyncSniffer`.
* **Dado que** o tráfego transita continuamente pela interface, **quando** pacotes TCP/UDP forem capturados, **então** o sniffer deve extrair a 5-tupla e despachar imediatamente para a fila assíncrona do buffer de fluxos em memória (`multiprocessing.Queue` ou `asyncio.Queue`) sem bloqueio de I/O.
* **Dado o requisito de vazão de classificação** (RNF04), **quando** o tráfego atingir 50 novos fluxos por segundo, **então** a taxa de descarte de pacotes por enfileiramento deve ser nula ($0\%$).

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.live_sniffer \
    --interface eth0 \
    --bpf-filter "tcp or udp" \
    --queue-size 2000
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Iniciando serviço de captura em tempo real (IDS Passivo)...
[INFO] Interface vinculada: eth0 | Filtro BPF: 'tcp or udp'
[INFO] Fila de desvio assíncrono inicializada (Capacidade: 2,000 pacotes).
[READY] Sniffer operacional. Monitorando tráfego não intrusivo...
[STATS] 10s: 450 pacotes capturados | 18 fluxos ativos | 0 descartes na fila.
```

**5. Componentes Envolvidos**
* `src/engine/live_sniffer.py`: Daemon de captura de pacotes passiva.
* `src/engine/flow_buffer.py`: Fila assíncrona de encaminhamento interno.
* Interface de rede do container gateway (`eth0`/`br0`).

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.1.2 do TCC (*Módulo de Detecção - IDS Passivo*), a captura assíncrona em espaço de usuário garante que o encaminhamento nativo de pacotes do kernel Linux não seja interrompido caso a IA leve tempo processando vetores.
* Requer capacidades de rede `NET_RAW` e `NET_ADMIN` habilitadas no Docker (Issue #05).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #05 (Net_Admin), Issue #06 (Ferramentas de Rede) e Issue #11 (Filtro BPF).
* **Bloqueia:** Issue #35 (Extração In-Flight) e Issue #36 (Integração iptables).

**9. Como Testar (Plano de Teste)**
1. Executar o sniffer em segundo plano escutando uma interface de teste virtual (ex.: `lo` ou veth).
2. Gerar tráfego TCP sintético com `curl` ou `hping3`.
3. Verificar se os pacotes chegam à fila do buffer sem erros de permissão.
4. Executar os testes automatizados via `pytest tests/test_live_sniffer.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `live_sniffer.py` implementado com suporte a encerramento gracioso via `SIGINT`/`SIGTERM`.
* Testes unitários com mocks de interface de rede passando.
* Teste de vazão validando ausência de vazamento de memória sob tráfego contínuo.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Crítica (Porta de entrada do tráfego em tempo real).

**12. Etiquetas (Labels)**
`infraestrutura`, `backend`, `networking`, `packet-capture`, `sniffer`.

**13. Documentação Relacionada**
* Requisito RF02 (Sniffing Passivo) e RNF04 (Vazão de Classificação).
* Seção 3.1.2 do TCC (*Camadas de Defesa e Subsistemas - IDS Passivo*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #35: [Backend] Módulo de extração de características de fluxo "em voo" (In-flight features)**

**1. História de Usuário (User Story)**
> **Como** arquiteto de software do projeto,
> **eu quero** um buffer circular em memória que calcule as características estatísticas selecionadas por SU "em voo" com base nos primeiros $N$ pacotes de cada fluxo (ex.: primeiros 10 a 20 pacotes),
> **para que** o comitê emita o veredito antes que o handshake TCP se complete e os dados da página de apostas sejam renderizados no navegador do cliente, evitando a condição de corrida (*race condition*) contra o TCP (RF03, RNF01 e Seção 3.4.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que** o sniffer alimenta a fila de pacotes em tempo real, **quando** os pacotes forem agregados pela 5-tupla em uma tabela hash circular em memória, **então** o módulo deve atualizar incrementalmente a média de IAT, variância e tamanhos de payload utilizando algoritmos online de passo único (sem armazenar histórico completo de pacotes).
* **Dado que** a predição antecipada é requerida para vencer a condição de corrida (*race condition* da Seção 3.4.2 do TCC), **quando** o fluxo atingir o limiar mínimo de pacotes configurado (ex.: $N=10$ a $15$ pacotes), **então** o buffer deve emitir o vetor das características de SU normalizado pelo `scaler.joblib` em tempo inferior a 5 milissegundos.
* **Dado que** fluxos finalizados por flags TCP `FIN`/`RST` ou inativos por mais de 30 segundos não devem acumular na memória, **quando** o coletor de lixo (*garbage collector*) do buffer atuar, **então** deve expurgar as entradas inativas, assegurando conformidade com o limite de 512MB RAM (RNF02).

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.inflight_extractor \
    --min-packets 10 \
    --flow-timeout 30.0 \
    --scaler-path models/production/scaler.joblib \
    --features-json models/selected_features.json
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Inicializando Extrator de Características In-Flight...
[CONFIG] Limiar de pacotes para veredito antecipado: N = 10 pacotes
[CONFIG] Timeout de expurgo de fluxos inativos: 30s
[FLOW READY] Fluxo [192.168.1.10:54210 -> 104.18.25.10:443 (TCP)] atingiu 10 pacotes!
  - IAT médio computado em voo: 0.012s
  - Tamanho médio de payload: 118 bytes
  - Vetor gerado para inferência: [0.12, 0.45, 0.88, 0.05, 0.32, 0.18, 0.64, 0.22]
  - Tempo de síntese vetorial: 1.15 ms
[DISPATCH] Vetor encaminhado para o Comitê de Decisão.
```

**5. Componentes Envolvidos**
* `src/engine/inflight_extractor.py`: Agregador de fluxos em voo e sintetizador vetorial.
* `src/engine/flow_table.py`: Tabela hash em memória com buffer circular e TTL.
* `models/production/scaler.joblib` e `models/selected_features.json`.

**6. Considerações Técnicas e Arquitetura**
* Conforme aprofundado na Seção 3.4.2 do TCC (*Latência de Inferência e Condição de Corrida*), se o firewall esperar a conexão TCP encerrar para extrair features, o usuário já terá visualizado as cotações de apostas. A extração nos primeiros 10 a 20 pacotes é a única abordagem capaz de emitir a decisão a tempo de injetar o `DROP` no iptables.
* Algoritmo online de Welford para desvio padrão sem retenção de pacotes passados.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #20 (Scaler), Issue #24 (Features Selecionadas por SU) e Issue #34 (Sniffer em Tempo Real).
* **Bloqueia:** Issue #37 (Lógica de Decisão do Firewall).

**9. Como Testar (Plano de Teste)**
1. Injetar um fluxo sintético de 15 pacotes sequenciais via script de teste.
2. Monitorar a emissão do vetor assim que o 10º pacote for processado.
3. Verificar se o vetor de características gerado é compatível com o formato de entrada do modelo.
4. Executar os testes automatizados via `pytest tests/test_inflight_extractor.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `inflight_extractor.py` implementado com testes de tempo de resposta.
* Síntese vetorial validada com tempo $< 5ms$.
* Mecanismo de expurgo de fluxos inativos testado contra vazamentos de memória.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Chave para a eficácia contra race condition).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `inflight-features`, `real-time`, `race-condition-mitigation`, `networking`.

**13. Documentação Relacionada**
* Requisito RF03 (Extração de Atributos) e RNF01 (Latência Crítica).
* Seção 3.4.2 do TCC (*Latência de Inferência e Condição de Corrida*).

**14. Estimativa**
* **T-Shirt Size:** L (Large)
* **Story Points:** 5


---

### **Issue #36: [Infraestrutura] Integração do script Python com o subsistema de rede (iptables)**

**1. História de Usuário (User Story)**
> **Como** desenvolvedor de infraestrutura de rede,
> **eu quero** um módulo adaptador em Python para interagir com o subsistema Netfilter (`iptables`/`nftables` do Linux), aplicando e revogando regras de bloqueio do tipo `DROP` de forma atômica e programática,
> **para que** os vereditos emitidos pelo motor de IA ou pelas listas manuais sejam imediatamente convertidos em filtragem física de pacotes no kernel (RF08 e Seção 3.1.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que** o motor emite um veredito de bloqueio para o IP de destino, **quando** o método `apply_block(ip, port=None)` for invocado, **então** deve inserir uma regra atômica na chain de encaminhamento (ex.: `iptables -I FORWARD -d <ip> -j DROP`) em tempo inferior a 20 milissegundos.
* **Dado que** um IP bloqueado indevidamente precisa ser liberado administrativamente (Feedback Loop - RF11), **quando** o método `remove_block(ip)` for acionado, **então** deve localizar e remover a regra correspondente sem afetar as demais diretivas de filtragem do firewall.
* **Dado que** o módulo roda no container `firewall_gateway`, **quando** for inicializado, **então** deve verificar a presença do binário `iptables` e checar se o container possui a capacidade de kernel `CAP_NET_ADMIN` ativa.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.netfilter_adapter \
    --action block \
    --ip 198.51.100.25 \
    --reason "Decisão Comitê IA (Votos: [1, 1, 0])"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[NETFILTER] Verificando privilégios de kernel CAP_NET_ADMIN... [OK]
[NETFILTER] Executando: iptables -I FORWARD -d 198.51.100.25 -j DROP
[NETFILTER] Regra injetada com sucesso no kernel (Tempo: 12.4 ms).
[AUDIT] Bloqueio ativo registrado para o IP 198.51.100.25.
```

**5. Componentes Envolvidos**
* `src/engine/netfilter_adapter.py`: Adaptador Python para manipulação do Netfilter.
* `iptables` / `nftables`: Subsistema de filtragem do kernel Linux.
* Container `firewall_gateway` com `cap_add: [NET_ADMIN]`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RF08 (*Integração com Kernel*) e a Seção 3.1.2 do TCC (*Camada de Filtragem Netfilter*), a execução da regra ocorre no nível mais baixo do kernel, descartando pacotes antes da camada de socket do sistema operacional.
* Sanitização rigorosa do parâmetro de entrada IP via `ipaddress.ip_network` para impedir qualquer vulnerabilidade de injeção de comandos de shell.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #05 (Recursos Net_Admin no Docker).
* **Bloqueia:** Issue #37 (Lógica de Decisão), Issue #38 (Execução do Bloqueio) e Issue #46 (Feedback Loop).

**9. Como Testar (Plano de Teste)**
1. Executar `apply_block(ip)` com um IP mock de teste.
2. Inspecionar a tabela do iptables com `iptables -L FORWARD -n -v` e validar se a regra `DROP` para aquele IP consta no topo da chain.
3. Executar `remove_block(ip)` e validar a exclusão da regra.
4. Executar os testes automatizados via `pytest tests/test_netfilter_adapter.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `netfilter_adapter.py` implementado com tratamento de erros de sistema operacional.
* Sanitização estrita contra command injection comprovada por testes unitários.
* Tempo de inserção e remoção medido e documentado $< 20ms$.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Executor operacional das decisões).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`infraestrutura`, `netfilter`, `iptables`, `security`, `kernel-integration`.

**13. Documentação Relacionada**
* Requisito RF08 (Integração com Kernel via Netfilter).
* Seção 3.1.2 do TCC (*Camada de Filtragem Netfilter/iptables*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #37: [Backend] Implementação da lógica de decisão: Whitelist → Blacklist → Votação do Comitê**

**1. História de Usuário (User Story)**
> **Como** arquiteto do motor de firewall,
> **eu quero** implementar a esteira hierárquica e assíncrona de decisão em três camadas (1º Consulta à Whitelist em memória, 2º Consulta à Blacklist manual e 3º Inferência pelo Comitê de Votação),
> **para que** tráfego previamente conhecido seja liberado ou bloqueado instantaneamente em $< 1ms$ sem gastar ciclos de CPU da IA, acionando o comitê apenas para fluxos não catalogados (RF07, RF09 e Seção 3.1.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que um fluxo em voo é analisado**, **quando** o IP ou domínio de destino constar na Whitelist em memória, **então** o sistema deve emitir imediatamente o veredito `PASS` (liberado) sem acionar o pipeline de IA.
* **Dado que o destino consta na Blacklist Manual**, **quando** for detectado, **então** o sistema deve emitir imediatamente o veredito `DROP` (bloqueio estático) sem consumir inferência da IA.
* **Dado que o fluxo não consta em nenhuma lista**, **quando** o vetor de características estiver disponível pelo extrator in-flight, **então** deve ser submetido ao Comitê de Hard Voting, aplicando a regra $\sum Votos \ge 2 \implies DROP$.
* **Dado que a auditoria deve registrar o caminho da decisão**, **quando** o veredito for emitido, **então** o log deve especificar a origem da decisão (`WHITELIST_BYPASS`, `BLACKLIST_STATIC` ou `ENSEMBLE_PREDICTION`) e o tempo total de decisão em milissegundos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.decision_engine \
    --ip 104.18.25.10 \
    --vector "[0.12, 0.45, 0.88, 0.05, 0.32, 0.18, 0.64, 0.22]"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[DECISION] Avaliando destino: 104.18.25.10...
  - Verificação Whitelist: NÃO LOCALIZADO (Miss: 0.12 ms)
  - Verificação Blacklist Manual: NÃO LOCALIZADO (Miss: 0.15 ms)
  - Desvio para o Comitê de Votação (Ensemble Hard Voting)...
  - Votos do comitê: RF=1, XGB=1, LR=0 -> Consenso: 2/3 (Positivo)
================ VEREDITO FINAL ================
  - Destino: 104.18.25.10
  - Decisão: DROP (Bloqueio acionado)
  - Origem da Decisão: ENSEMBLE_PREDICTION
  - Votos: [1, 1, 0]
  - Tempo Total (T-Verdict): 8.45 ms (Conforme: < 200 ms)
```

**5. Componentes Envolvidos**
* `src/engine/decision_engine.py`: Motor orquestrador da esteira de decisão.
* `src/database/crud_whitelist.py` e `src/database/crud_blacklist.py`.
* `src/brain/ensemble_engine.py`: Comitê de votação majoritária.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.1.2 e 3.5.1 do TCC (*Camadas de Defesa e Whitelists*), o bypass por listas em memória reduz drasticamente a carga média sobre a CPU (RNF03), pois serviços populares legítimos (Google, Microsoft, bancos) nunca sobrecarregam o motor de IA.
* Utilização de tabelas hash `set()` em memória RAM para consulta $O(1)$ das listas.

**7. Mockups ou Referências Visuais**
* Fluxograma Mermaid da esteira de três camadas de filtragem.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #28 (Comitê Ensemble), Issue #35 (Extração In-flight), Issue #36 (Netfilter) e Issue #41.1 (Banco de Listas).
* **Bloqueia:** Issue #38 (Execução do Bloqueio) e Issue #40 (Sistema de Logging).

**9. Como Testar (Plano de Teste)**
1. Testar caso 1: Destino na Whitelist -> Validar resposta imediata `PASS` sem chamada ao comitê.
2. Testar caso 2: Destino na Blacklist -> Validar resposta imediata `DROP` sem chamada ao comitê.
3. Testar caso 3: Destino desconhecido -> Validar acionamento dos 3 classificadores e consenso majoritário.
4. Executar os testes automatizados via `pytest tests/test_decision_engine.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Classe `DecisionEngine` implementada com cobertura de testes unitários superior a 90%.
* Tempo de decisão medido para os 3 fluxos possíveis.
* Garantia de tratamento gracioso de falha (*failsafe* se o modelo falhar).

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Núcleo decisório do firewall).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `decision-engine`, `whitelist`, `blacklist`, `ensemble-integration`.

**13. Documentação Relacionada**
* Requisitos RF07, RF09 e RNF01.
* Seção 3.1.2 e Seção 3.5.1 do TCC (*Camadas de Defesa e Subsistemas*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #38: [Infraestrutura/Backend] Criação da lógica de execução do bloqueio (DROP)**

**1. História de Usuário (User Story)**
> **Como** desenvolvedor de segurança do projeto,
> **eu quero** implementar o despachante de ações de bloqueio que recebe o veredito `DROP`, aciona a inserção da regra no iptables, finaliza conexões TCP ativas com pacote `TCP RST` e invalida o cache,
> **para que** conexões com plataformas de apostas sejam interrompidas imediatamente na ponta do cliente sem esperar o timeout passivo do navegador (RF08 e Seção 3.1.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que** o motor de decisão emitiu veredito `DROP`, **quando** o despachante de bloqueio for acionado, **então** deve chamar o adaptador Netfilter para inserir a regra `DROP` em tempo inferior a 25 milissegundos.
* **Dado que** uma sessão TCP pode estar em andamento com o navegador do cliente, **quando** o modo de interrupção ativa estiver habilitado, **então** o despachante deve forjar e enviar um pacote `TCP RST` para a ponta local do cliente, fechando instantaneamente o socket.
* **Dado a confirmação do bloqueio físico**, **quando** o procedimento concluir, **então** o despachante deve enviar o evento para o serviço de logging e notificar a invalidação do cache em memória.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.block_executor \
    --ip 203.0.113.88 \
    --port 443 \
    --send-rst \
    --reason "Classificado como Aposta (Veredito Ensemble)"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[BLOCK DISPATCHER] Recebido veredito DROP para 203.0.113.88:443.
[IPTABLES] Regra FORWARD -d 203.0.113.88 -j DROP aplicada no kernel (14.2 ms).
[TCP RESET] Pacote TCP RST forjado e injetado na interface virtual (Socket cliente terminado).
[CACHE] IP 203.0.113.88 registrado com status BLOCKED (TTL: 300s).
[SUCCESS] Bloqueio físico ativo e auditado com sucesso.
```

**5. Componentes Envolvidos**
* `src/engine/block_executor.py`: Orquestrador de aplicação do bloqueio e envio de RST.
* `src/engine/netfilter_adapter.py`: Integração com o iptables.
* `src/engine/cache_manager.py`: Atualização do cache.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.1.2 do TCC (*Camada de Filtragem Netfilter/iptables*), a ação de bloqueio deve ser atômica e não bloqueante para o restante da fila de pacotes.
* O envio do TCP RST via Scapy/Raw Socket força a liberação de recursos de rede no navegador do cliente, evitando conexões pendentes (*zombie sockets*).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #36 (Netfilter iptables) e Issue #37 (Lógica de Decisão).
* **Bloqueia:** Issue #39 (Cache de IPs) e Issue #47 (Teste de Latência).

**9. Como Testar (Plano de Teste)**
1. Disparar uma conexão `curl` contínua para um IP de teste no container do cliente.
2. Acionar `block_executor.py` contra o IP de destino.
3. Verificar se o comando `curl` é imediatamente interrompido por conexão rejeitada/resetada.
4. Executar os testes automatizados via `pytest tests/test_block_executor.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `block_executor.py` implementado com injeção de regra e envio opcional de RST.
* Testes unitários com simulação de encerramento de conexão passando.
* Tempo total de despacho comprovado $< 25ms$.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `firewall`, `block-action`, `iptables`, `tcp-rst`.

**13. Documentação Relacionada**
* Requisito RF08 (Integração com Kernel via Netfilter).
* Seção 3.1.2 do TCC (*Camada de Filtragem Netfilter/iptables*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #39: [Backend] Implementação de cache de IPs para otimização de performance**

**1. História de Usuário (User Story)**
> **Como** engenheiro de software do projeto,
> **eu quero** implementar uma estrutura de cache em memória RAM (LRU Cache com tempo de expiração TTL de 300 segundos e capacidade máxima parametrizada),
> **para que** decisões recentes sobre endereços IP sejam resolvidas em $< 1ms$ sem invocar a extração em voo ou o comitê de ML, reduzindo a carga de CPU e a latência em conexões recorrentes (RNF01, RNF02 e RNF04).

**2. Critérios de Aceitação (AC)**
* **Dado que** um IP foi classificado pelo comitê ou pelas listas, **quando** armazenado no cache em memória, **então** consultas subsequentes para o mesmo IP nos próximos 300 segundos devem retornar o veredito imediatamente em tempo inferior a 1 milissegundo.
* **Dado que** o cache não pode causar vazamento de memória RAM (RNF02), **quando** o número de entradas atingir o teto máximo estipulado (ex.: 5.000 entradas), **então** deve aplicar a política de desalocação LRU (*Least Recently Used*), descartando as entradas mais antigas.
* **Dado que** um administrador pode alterar listas via CLI ou Feedback Loop, **quando** um IP for adicionado à Whitelist ou liberado, **então** o método `invalidate(ip)` deve remover instantaneamente a entrada correspondente do cache.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.cache_manager \
    --action get \
    --ip 104.18.25.10
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[CACHE HIT] IP: 104.18.25.10 -> Veredito: DROP (Origem: ENSEMBLE) | TTL Restante: 242s
[PERF] Tempo de resposta do cache: 0.08 ms (Consulta O(1))
================ ESTATÍSTICAS DO CACHE ================
  - Entradas ativas: 142 / 5,000
  - Taxa de acerto (Hit Ratio): 78.4%
  - Memória estimada ocupada: 124 KB (Totalmente conforme RNF02)
```

**5. Componentes Envolvidos**
* `src/engine/cache_manager.py`: Gerenciador de cache LRU com TTL em memória.
* `collections.OrderedDict`, `time`: Estruturas de dados em memória do Python.

**6. Considerações Técnicas e Arquitetura**
* Conforme as diretrizes de baixo recurso do TCC (RNF01 e RNF02), a memorização em cache é o mecanismo primário que viabiliza atingir vazão superior a 50 fluxos/s (RNF04) sem aumentar o uso de CPU além dos 60% (RNF03).
* Thread-safe com uso de locks leves (`threading.Lock` ou `asyncio.Lock`).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #37 (Lógica de Decisão).
* **Bloqueia:** Issue #45 (Hot Reload de Listas) e Issue #47 (Teste de Latência).

**9. Como Testar (Plano de Teste)**
1. Inserir um IP mock no cache com status `DROP` e TTL de 2 segundos.
2. Consultar o IP imediatamente e validar o Cache Hit.
3. Aguardar 3 segundos e verificar se a chave expirou automaticamente (Cache Miss).
4. Executar os testes automatizados via `pytest tests/test_cache_manager.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Classe `CacheManager` implementada com suporte a LRU e TTL.
* Testes unitários cobrindo cenários de Hit, Miss, Expiração e Invalidação passando com 100%.
* Pegada de memória confirmada $< 2MB$ para 5.000 chaves.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `cache`, `lru`, `performance-optimization`, `latency`.

**13. Documentação Relacionada**
* Requisitos RNF01 (Latência < 200ms) e RNF02 (Memória RAM).
* Seção 3.1.2 do TCC (*Camadas de Defesa e Subsistemas*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #40: [Backend] Sistema de Logging detalhado de eventos e vereditos**

**1. História de Usuário (User Story)**
> **Como** auditor do sistema e pesquisador do projeto,
> **eu quero** um mecanismo de logging assíncrono e estruturado (formato JSON Lines gravado em volume persistente),
> **para que** cada decisão tomada pelo firewall contenha timestamp ISO-8601, IP de origem, IP de destino, domínio resolvido, tempo de decisão $T_{verdict}$ e a distribuição detalhada dos votos do comitê `[RF, XGB, LR]`, satisfazendo integralmente o requisito de interpretabilidade e auditoria do TCC (RNF07, RNF08 e Seção 3.5.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que uma decisão é emitida pelo motor**, **quando** for registrada no log persistente `/volumes/logs/firewall_verdicts.log`, **então** deve ser gravada em formato JSON Lines contendo: `timestamp`, `src_ip`, `dst_ip`, `dst_port`, `decision` (PASS ou DROP), `origin` (WHITELIST, BLACKLIST ou ENSEMBLE), `votes` (ex.: `[1, 1, 0]`) e `t_verdict_ms` (RNF08).
* **Dado que a escrita em disco não pode retardar o tráfego de rede**, **quando** o serviço de log registrar eventos, **então** deve utilizar fila assíncrona desacoplada em segundo plano (`QueueHandler`/`QueueListener`), mantendo o impacto de latência $< 1ms$.
* **Dado que os logs devem sobreviver ao reinício do container** (RNF07), **quando** o container do firewall for reiniciado ou recriado via Docker Compose, **então** os arquivos do volume persistente `/volumes/logs/` devem ser preservados integralmente com suporte a rotação automática.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.logger_service \
    --tail 5 \
    --log-file /volumes/logs/firewall_verdicts.log
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```json
{"timestamp": "2026-10-28T16:45:10.124Z", "src_ip": "192.168.1.10", "dst_ip": "104.18.25.10", "dst_port": 443, "decision": "DROP", "origin": "ENSEMBLE", "votes": [1, 1, 0], "t_verdict_ms": 7.82}
{"timestamp": "2026-10-28T16:45:12.340Z", "src_ip": "192.168.1.10", "dst_ip": "142.250.190.46", "dst_port": 443, "decision": "PASS", "origin": "WHITELIST", "votes": null, "t_verdict_ms": 0.45}
```

**5. Componentes Envolvidos**
* `src/engine/logger_service.py`: Serviço de logging assíncrono estruturado.
* Diretório montado persistente `/volumes/logs/`.
* `logging.handlers.RotatingFileHandler`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade direta com a Seção 3.5.2 do TCC (*Interface de Moderação e Interpretabilidade*) e o Requisito RNF08 (*Interpretabilidade de Log*), o registro da distribuição explícita dos votos `[1, 1, 0]` garante transparência sobre a contribuição individual de cada algoritmo de ML.
* Rotação de logs configurada para 5 arquivos de no máximo 10MB para não esgotar o disco em hardware limitado.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #03 (Volumes Docker) e Issue #37 (Lógica de Decisão).
* **Bloqueia:** Issue #44 (Interface CLI de Auditoria) e Issue #46 (Feedback Loop).

**9. Como Testar (Plano de Teste)**
1. Disparar chamadas ao logger com eventos sintéticos de bloqueio e liberação.
2. Inspecionar o arquivo `/volumes/logs/firewall_verdicts.log` e validar a estrutura JSON de cada linha com `jq`.
3. Validar se o campo `votes` contém vetor numérico quando originado do ensemble.
4. Executar os testes automatizados via `pytest tests/test_logger_service.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `logger_service.py` implementado de forma assíncrona.
* Testes unitários com validação de formato JSON Lines passando.
* Rotação automática e persistência em volume testadas com sucesso.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `logging`, `audit`, `json-lines`, `transparency`.

**13. Documentação Relacionada**
* Requisitos RNF07 (Persistência) e RNF08 (Interpretabilidade de Log).
* Seção 3.5.2 do TCC (*Interpretabilidade Local e Logs*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

# 📝 Grupo 6: Gestão de Listas e Moderação

### **Issue #41: [Backend] Modelagem do banco de dados local para Listas (SQLite ou JSON)**

**1. História de Usuário (User Story)**
> **Como** arquiteto de dados do sistema,
> **eu quero** formalizar o modelo relacional e os scripts de inicialização do banco de dados local SQLite (`firewall.db`),
> **para que** as regras de Whitelist, Blacklist manual e registros de auditoria sejam persistidos em volume seguro e sobrevivam a reinícios do container com suporte a consultas concorrentes de alta velocidade (RF09, RNF07 e Seção 3.5.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o container gateway é inicializado**, **quando** o banco `/volumes/db/firewall.db` for verificado, **então** deve criar as tabelas `whitelist`, `blacklist` e `audit_log` com esquema relacional formal caso não existam.
* **Dado o esquema das tabelas de listas**, **quando** criadas, **então** devem conter as colunas: `id` (INTEGER PRIMARY KEY), `ip_address` (TEXT), `domain` (TEXT), `reason` (TEXT), `created_at` (DATETIME) e `active` (BOOLEAN), acompanhadas de índices únicos em `ip_address` e `domain`.
* **Dado que a concorrência entre threads do firewall e CLI é necessária**, **quando** configurada a conexão SQLite, **então** deve habilitar o modo WAL (Write-Ahead Logging) via `PRAGMA journal_mode=WAL;` e timeout de bloqueio de 5.000ms.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.database.init_db \
    --db-path /volumes/db/firewall.db \
    --enable-wal
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[DATABASE] Conectando a /volumes/db/firewall.db...
[DATABASE] Aplicando PRAGMA journal_mode=WAL; -> WAL ativado.
[DATABASE] Criando tabela 'whitelist' com índices... [OK]
[DATABASE] Criando tabela 'blacklist' com índices... [OK]
[DATABASE] Criando tabela 'audit_log' com índices... [OK]
[SUCCESS] Banco de dados inicializado e estruturado para alta concorrência.
```

**5. Componentes Envolvidos**
* `src/database/models.py`: Definição de esquema e entidades SQLite.
* `src/database/init_db.py`: Script de criação e migração inicial.
* Volume persistente `/volumes/db/firewall.db`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RF09 (*Gestão de Whitelist/Blacklist*) e RNF07 (*Persistência de Dados*), o SQLite oferece zero configuração de servidor de banco de dados, consumindo menos de 5MB de RAM e mantendo integridade ACID completa em arquivo único.
* Nota: Essa especificação consolida a infraestrutura modelada na Issue #41.1 para produção.

**7. Mockups ou Referências Visuais**
* Diagrama Entidade-Relacionamento (DER) das tabelas SQLite.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #01 (Estrutura de Pastas) e Issue #03 (Volumes Docker).
* **Bloqueia:** Issue #42 (CRUD Whitelist) e Issue #43 (CRUD Blacklist).

**9. Como Testar (Plano de Teste)**
1. Executar o script `init_db.py` criando um banco em pasta temporária.
2. Inspecionar o esquema com comandos `sqlite3` e validar se os índices foram criados.
3. Testar escrita e leitura simultânea a partir de duas threads concorrentes.
4. Executar os testes automatizados via `pytest tests/test_init_db.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Esquema formal implementado em `models.py` com suporte ao modo WAL.
* Testes unitários de criação e concorrência passando com 100%.
* Índices de busca rápida validados.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `database`, `sqlite`, `wal`, `persistence`.

**13. Documentação Relacionada**
* Requisitos RF09 (Gestão de Listas) e RNF07 (Persistência de Dados).
* Seção 3.5.1 do TCC (*Camada de Pré-filtragem e Whitelists*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #41.1: [Backend] Modelagem, Scripts de Migração e Seed do Banco de Dados Local**
**1. História de Usuário (User Story)**
> Como desenvolvedor/administrador do sistema,
> eu quero uma estrutura de banco de dados modelada com scripts de migração e população inicial (seed),
> para que o sistema nasça com schemas padronizados, domínios críticos pré-cadastrados (ex: serviços essenciais na Whitelist) e suporte à persistência de dados em volumes Docker.

**2. Critérios de Aceitação (AC)**
Dado que o container do Gateway é iniciado pela primeira vez, quando o script de inicialização do banco rodar, então as tabelas (whitelist, blacklist, logs_decisao, configuracoes) devem ser criadas automaticamente (se não existirem).   

Dado que o sistema entra em execução, quando o banco for populado via seed, então endereços IP/domínios essenciais (ex: DNS governamentais, repositórios de atualização) já devem constar na Whitelist padrão.   

Dado que o banco armazena logs de auditoria, quando um registro for inserido, então ele deve obrigatoriamente guardar o carimbo de tempo (timestamp), IP de origem, domínio e a distribuição exata dos votos do comitê (ex: [1, 1, 0]) em compliance com o requisito RNF08.

**3. Exemplo de Requisição (Script de Seed / seed_data.py)**
Python
import sqlite3

INIT_WHITELIST = [
    ("1.1.1.1", "Cloudflare DNS", "SISTEMA"),
    ("8.8.8.8", "Google DNS", "SISTEMA"),
    ("gov.br", "Portal do Governo", "SISTEMA")
]

def seed_database(db_path="/app/db/firewall.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT OR IGNORE INTO whitelist (alvo, descricao, criado_por) VALUES (?, ?, ?)",
        INIT_WHITELIST
    )
    conn.commit()
    conn.close()
    print("[OK] Seed do banco de dados executado com sucesso.")
**4. Exemplo de Resposta (Inspecção no Banco SQLite)**
Plaintext
$ sqlite3 /app/db/firewall.db "SELECT * FROM whitelist;"
1|1.1.1.1|Cloudflare DNS|SISTEMA|2026-08-07 18:50:00
2|8.8.8.8|Google DNS|SISTEMA|2026-08-07 18:50:00
3|gov.br|Portal do Governo|SISTEMA|2026-08-07 18:50:00
**5. Componentes Envolvidos**
Banco de Dados Local (SQLite3 ou JSON estruturado em volume persistente).   

Script Python de DDL/DML (schema.sql / migrations.py).   

Volume Docker montado em /app/db/.   

**6. Considerações Técnicas**
Utilizar o SQLite3 nativo do Python pela leveza, baixo footprint de memória (atendendo ao RNF02) e suporte ACID direto em arquivo.   

Indexar as colunas de busca frequente (alvo, ip, timestamp) para garantir que as consultas de pré-filtragem ocorram em tempo sub-milissegundo.   

Garantir permissões de escrita no arquivo .db dentro do volume montado pelo Docker.   

**7. Dependências e Bloqueios**
Depende de: Issue #01 (Estrutura de pastas para volumes) e Issue #03 (Configuração de volumes no docker-compose.yml).   

Bloqueia: Issue #41 (Modelagem DB Listas), Issue #42/#43 (CRUDs Whitelist/Blacklist), Issue #40 (Sistema de Logging) e Issue #44 (Interface CLI).   

**8. Como Testar**
Remover o banco antigo (se houver): rm -f volumes/db/firewall.db.

Rodar o script de inicialização e seed: docker exec gateway_firewall python3 -m src.db.init_db.

Validar se o arquivo firewall.db foi criado no diretório montado no host (volumes/db/).

Consultar os dados inseridos via terminal com sqlite3 e garantir que o schema de logs atende ao RNF08.

**9. Definição de Pronto (DoD)**
Scripts DDL de criação de tabelas e script DML de seed inicial versionados.

Schema do banco validado incluindo suporte ao RNF08 (distribuição de votos em JSON/String).

Persistência em volume Docker testada após remoção e reinício do container.   

**10. Prioridade e Severidade**
Prioridade: Alta (Essencial para os módulos de governança e logs).   

Severidade: Alta.

**11. Etiquetas (Labels)**
backend, database, sqlite, seed, governance.

**12. Documentação Relacionada**
Requisito RF09 (Gestão de Whitelist/Blacklist).

Requisito RNF07 (Persistência de Dados).

Requisito RNF08 (Interpretabilidade de Log).

Seção 3.5.1 (Camada de Pré-filtragem e Whitelists).   

**13. Estimativa**
T-Shirt Size: M (Medium) / 3 Story Points.

---

### **Issue #42: [Backend] Desenvolvimento de módulo CRUD para gestão da Whitelist**

**1. História de Usuário (User Story)**
> **Como** administrador da rede,
> **eu quero** um módulo programático de CRUD (Criar, Ler, Atualizar, Deletar) para gerenciar a Whitelist de IPs e domínios essenciais,
> **para que** serviços governamentais, bancos e plataformas institucionais sejam garantidos contra qualquer interrupção pelo firewall (RF09 e Seção 3.5.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado um novo domínio ou IP legítimo**, **quando** a função `add_whitelist(ip_or_domain, reason, added_by)` for chamada, **então** deve validar a sintaxe (endereço IPv4/IPv6 ou FQDN) e persistir o registro no SQLite, sincronizando com a memória.
* **Dado que o firewall consulta a Whitelist em voo a cada conexão**, **quando** for invocado `is_whitelisted(target)`, **então** a verificação deve responder a partir da estrutura em memória em tempo inferior a 0.5 milissegundos.
* **Dado que uma entrada precisa ser revogada**, **quando** for invocado `remove_whitelist(id_or_target)`, **então** deve marcar como inativo ou excluir do banco de dados e expurgar a entrada da memória.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.database.crud_whitelist \
    --action add \
    --target "caixa.gov.br" \
    --reason "Portal bancário essencial" \
    --added-by "admin"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[WHITELIST] Validando sintaxe de 'caixa.gov.br'... [OK: FQDN Válido]
[DATABASE] Inserido registro ID: 48 na tabela 'whitelist'.
[CACHE] Domínio 'caixa.gov.br' adicionado ao conjunto em memória.
[SUCCESS] Entrada cadastrada na Whitelist com sucesso.
```

**5. Componentes Envolvidos**
* `src/database/crud_whitelist.py`: Módulo CRUD de Whitelist.
* `src/database/models.py`: Tabela `whitelist`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RF09 e a Seção 3.5.1 do TCC (*Camada de Pré-filtragem e Whitelists*), o acesso à Whitelist é prioritário sobre qualquer outro subsistema, garantindo proteção contra falsos positivos sistêmicos.
* Validação de formato via módulo nativo `ipaddress` e regex para FQDN.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #41 (Modelagem SQLite).
* **Bloqueia:** Issue #44 (Interface CLI) e Issue #45 (Hot Reload).

**9. Como Testar (Plano de Teste)**
1. Inserir entradas válidas de IP e domínio.
2. Tentar inserir entradas com sintaxe corrompida e validar a rejeição com mensagem de erro.
3. Testar a remoção e verificar se `is_whitelisted()` retorna `False`.
4. Executar os testes automatizados via `pytest tests/test_crud_whitelist.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `crud_whitelist.py` implementado com todas as operações CRUD funcionais.
* Validação rigorosa de sintaxe de rede.
* Testes unitários passando com 100% de sucesso.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `whitelist`, `crud`, `governance`, `sqlite`.

**13. Documentação Relacionada**
* Requisito RF09 (Gestão de Whitelist/Blacklist).
* Seção 3.5.1 do TCC (*Camada de Pré-filtragem e Whitelists*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #43: [Backend] Desenvolvimento de módulo CRUD para gestão da Blacklist Manual**

**1. História de Usuário (User Story)**
> **Como** administrador da rede,
> **eu quero** um módulo programático de CRUD para gerenciar a Blacklist Manual de endereços IP e domínios confirmados de apostas,
> **para que** operadores ilegais ou casas de apostas conhecidas sejam bloqueados estaticamente de forma imediata sem consumir inferência da IA (RF09 e Seção 3.5.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que uma plataforma de aposta é identificada pelo operador**, **quando** executado `add_blacklist(target, reason, added_by)`, **então** deve validar a entrada, gravá-la na tabela `blacklist` do SQLite e injetar imediatamente a regra `DROP` no Netfilter via `netfilter_adapter`.
* **Dado que uma entrada foi adicionada por engano**, **quando** executado `remove_blacklist(id)`, **então** deve remover o registro do banco de dados e revogar a regra correspondente no iptables.
* **Dado que o operador deseja listar as regras manuais**, **quando** for invocado `list_blacklist(page=1, limit=50)`, **então** deve retornar listagem estruturada com paginação, data de inclusão e motivo.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.database.crud_blacklist \
    --action add \
    --target "198.51.100.99" \
    --reason "Operador ilegal de apostas" \
    --added-by "admin"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[BLACKLIST] Validando sintaxe de '198.51.100.99'... [OK: IPv4 Válido]
[DATABASE] Inserido registro ID: 12 na tabela 'blacklist'.
[NETFILTER] Regra iptables -I FORWARD -d 198.51.100.99 -j DROP aplicada (11.2 ms).
[SUCCESS] IP adicionado à Blacklist manual e bloqueado no kernel.
```

**5. Componentes Envolvidos**
* `src/database/crud_blacklist.py`: Módulo CRUD de Blacklist.
* `src/engine/netfilter_adapter.py`: Integração com o iptables para bloqueio imediato.
* `src/database/models.py`: Tabela `blacklist`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RF09 e a Seção 3.5.1 do TCC, o bloqueio manual estático economiza poder computacional do roteador de borda, servindo como a primeira barreira contra alvos já catalogados.
* Tratamento atômico de transação: se o comando de iptables falhar, o registro no banco não deve ser comitado (*rollback*).

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #36 (Netfilter iptables) e Issue #41 (Modelagem SQLite).
* **Bloqueia:** Issue #44 (Interface CLI) e Issue #45 (Hot Reload).

**9. Como Testar (Plano de Teste)**
1. Inserir um IP mock na Blacklist e verificar a inserção no banco e no iptables.
2. Listar os itens da Blacklist com filtro de paginação.
3. Excluir o item e validar a remoção simultânea no banco e no kernel.
4. Executar os testes automatizados via `pytest tests/test_crud_blacklist.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Módulo `crud_blacklist.py` implementado com operações atômicas.
* Integração bidirecional com o Netfilter testada.
* Testes unitários com casos de erro e rollback passando.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `blacklist`, `crud`, `governance`, `iptables`.

**13. Documentação Relacionada**
* Requisito RF09 (Gestão de Whitelist/Blacklist).
* Seção 3.5.1 do TCC (*Camada de Pré-filtragem e Whitelists*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #44: [Backend/Frontend] Implementação de interface CLI para moderação administrativa**

**1. História de Usuário (User Story)**
> **Como** administrador do firewall,
> **eu quero** uma interface de linha de comando (CLI amigável com subcomandos `status`, `whitelist`, `blacklist`, `logs`, `unblock` e `reload`),
> **para que** eu possa operar o sistema, consultar métricas em tempo real, auditar decisões e manipular as listas de governança diretamente pelo terminal sem necessidade de acesso manual ao banco de dados ou ao iptables (RF10 e Seção 3.5.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o comando `firewall-cli status` é executado**, **então** deve exibir no console uma visão consolidada do estado do sistema: status do daemon, tempo de atividade (*uptime*), quantidade de fluxos classificados, memória RAM consumida, taxa de acerto do cache e estado dos modelos de IA.
* **Dado que o operador executa `firewall-cli whitelist add <alvo> --reason "<motivo>" ` ou `firewall-cli blacklist add <alvo> --reason "<motivo>" `**, **então** deve validar a entrada, invocar os CRUDs correspondentes e imprimir confirmação tabular formatada.
* **Dado que o comando `firewall-cli logs --tail 10` é acionado**, **então** deve renderizar no terminal uma tabela legível com os últimos 10 vereditos emitidos, contendo timestamp, IP de destino, veredito (PASS/DROP), tempo de decisão e a distribuição de votos `[RF, XGB, LR]` (RNF08).

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.cli.main status
python -m src.cli.main whitelist add 1.1.1.1 --reason "DNS Confiável"
python -m src.cli.main logs --tail 5
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
================ STATUS DO FIREWALL INTELIGENTE ================
  - Estado Operacional: ATIVO (PID: 1240) | Uptime: 4h 12m
  - Memória RAM Consumida: 98.4 MB / 512 MB (19.2% - Seguro)
  - Fluxos Classificados: 4,890 (Taxa média: 12.4 fluxos/s)
  - Taxa de Acerto do Cache: 81.2% (Hit Ratio O(1))
  - Modelos em Memória: Random Forest [OK] | XGBoost [OK] | LogReg [OK]
  - Regras Ativas no Netfilter: 42 regras DROP

================ ÚLTIMOS VEREDITOS (AUDITORIA) ================
TIMESTAMP            | DESTINO       | AÇÃO | ORIGEM   | VOTOS     | T-VERDICT
---------------------|---------------|------|----------|-----------|----------
2026-10-28 16:50:01  | 104.18.25.10  | DROP | ENSEMBLE | [1, 1, 0] | 8.24 ms
2026-10-28 16:50:04  | 142.250.190.46| PASS | WHITELIST| [ - - - ] | 0.42 ms
2026-10-28 16:50:09  | 198.51.100.99 | DROP | BLACKLIST| [ - - - ] | 0.35 ms
```

**5. Componentes Envolvidos**
* `src/cli/main.py`: Ponto de entrada CLI (utilizando `argparse` ou `click`).
* `src/cli/commands.py`: Implementação dos comandos (`status`, `whitelist`, `blacklist`, `logs`).
* Integração com `src/database/` e `src/engine/`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RF10 (*Interface Administrativa - CLI*) e Seção 3.5.2 do TCC (*Interface de Moderação e Interpretabilidade*), a CLI é a interface primária de governança que permite ao operador humano auditar o "gap semântico" do sistema de IA.
* Renderização em tabelas ASCII limpas, sem dependências gráficas pesadas.

**7. Mockups ou Referências Visuais**
* Layout do terminal apresentado no Exemplo de Resposta acima.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #40 (Sistema de Logging), Issue #42 (CRUD Whitelist) e Issue #43 (CRUD Blacklist).
* **Bloqueia:** Issue #46 (Feedback Loop) e Issue #56 (Manual do Usuário no README).

**9. Como Testar (Plano de Teste)**
1. Executar `firewall-cli status` e checar a consistência dos dados exibidos.
2. Adicionar um IP na Whitelist via CLI e validar sua presença no banco.
3. Consultar os logs via CLI com `--tail` e checar a renderização das colunas.
4. Executar os testes automatizados via `pytest tests/test_cli.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Interface CLI totalmente implementada com comandos de help (`--help`).
* Testes unitários utilizando `CliRunner` passando com 100%.
* Formatação visual de terminal padronizada e legível.

**11. Prioridade e Severidade**
* **Prioridade:** Alta.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`backend`, `frontend`, `cli`, `moderation`, `governance`, `terminal-ui`.

**13. Documentação Relacionada**
* Requisito RF10 (Interface Administrativa CLI) e RNF08 (Interpretabilidade).
* Seção 3.5.2 do TCC (*Interface de Moderação e Interpretabilidade*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #45: [Backend] Criação de mecanismo de "Hot Reload" das listas**

**1. História de Usuário (User Story)**
> **Como** desenvolvedor do motor do firewall,
> **eu quero** implementar um mecanismo de recarregamento a quente (*Hot Reload* via sinal POSIX `SIGHUP` ou endpoint IPC local),
> **para que** atualizações realizadas na Whitelist ou Blacklist tenham efeito imediato nas estruturas em memória do daemon sem exigir reinicialização do container ou perda de pacotes de rede (RNF06 e Seção 3.5.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que novas entradas foram gravadas no banco de listas**, **quando** o processo principal receber um sinal `SIGHUP` (ou comando `firewall-cli reload`), **então** o daemon deve recarregar os conjuntos de IPs em memória a partir do SQLite em tempo inferior a 100 milissegundos.
* **Dado que o firewall está ativamente processando tráfego**, **quando** a recarga estiver ocorrendo, **então** não deve ocorrer travamento de threads ou deadlocks (uso de ponteiros atômicos ou troca *copy-on-write* de estruturas).
* **Dado a conclusão do recarregamento**, **quando** auditado o evento, **então** deve registrar no log a contagem total de entradas carregadas na Whitelist e Blacklist.

**3. Exemplo de Requisição (Código/CLI)**
```bash
# Via CLI:
python -m src.cli.main reload
# Ou via sinal POSIX:
kill -HUP $(pgrep -f "firewall_engine")
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[SIGNAL] Recebido sinal SIGHUP para recarga de configurações...
[HOT RELOAD] Lendo tabelas 'whitelist' e 'blacklist' do banco de dados...
[HOT RELOAD] 128 entradas carregadas na Whitelist em memória.
[HOT RELOAD] 54 entradas carregadas na Blacklist em memória.
[CACHE] Cache de decisões invalidado para evitar dados obsoletos.
[SUCCESS] Hot Reload concluído em 42.1 ms (Sem interrupção de serviço).
```

**5. Componentes Envolvidos**
* `src/engine/reload_handler.py`: Interceptador de sinais POSIX e orquestrador de recarga.
* `src/engine/decision_engine.py`: Atualização atômica dos conjuntos de listas.
* `src/engine/cache_manager.py`: Invalidação de chaves cacheadas.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RNF06 (*Disponibilidade*) e Seção 3.5.1 do TCC, a reinicialização de um container de firewall de borda derrubaria sessões de toda a rede local; o Hot Reload em memória é indispensável para disponibilidade contínua.
* Implementação com `signal.signal(signal.SIGHUP, handler)` no processo principal.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #39 (Cache de IPs), Issue #42 (CRUD Whitelist) e Issue #43 (CRUD Blacklist).
* **Bloqueia:** Issue #46 (Feedback Loop) e Issue #51 (Teste de Persistência).

**9. Como Testar (Plano de Teste)**
1. Adicionar um IP na tabela do banco SQLite enquanto o motor está rodando.
2. Enviar sinal `SIGHUP` ao processo do firewall.
3. Verificar se o IP passou a responder imediatamente como permitido ou bloqueado sem reiniciar o processo.
4. Executar os testes automatizados via `pytest tests/test_hot_reload.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Handler de sinal `SIGHUP` implementado com troca de estruturas atômica.
* Testes unitários com simulação de sinais passando.
* Tempo de recarga comprovado $< 100ms$.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `hot-reload`, `posix-signals`, `high-availability`, `devops`.

**13. Documentação Relacionada**
* Requisito RNF06 (Disponibilidade e Failsafe).
* Seção 3.5.1 do TCC (*Camada de Pré-filtragem e Whitelists*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #46: [Backend] Lógica de "Feedback Loop": Adicionar falsos positivos à Whitelist via log**

**1. História de Usuário (User Story)**
> **Como** administrador da rede,
> **eu quero** um fluxo integrado de correção de incidentes (`firewall-cli unblock <ip> --whitelist`), que consulte os logs de decisão, reverta a regra `DROP` no iptables e adicione o IP de forma definitiva na Whitelist,
> **para que** falsos positivos cometidos pelo comitê sejam mitigados em segundos pelo operador humano, estabelecendo o ciclo de correção e governança contínua (RF11 e Seção 3.5.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que um falso positivo é identificado pelo operador**, **quando** for executado `firewall-cli unblock <ip> --whitelist --reason "<motivo>" `, **então** o comando deve remover imediatamente a regra `DROP` do Netfilter.
* **Dado que o desbloqueio deve ser definitivo**, **quando** a regra do iptables for removida, **então** o endereço IP deve ser persistido na tabela `whitelist` do SQLite com a justificativa informada.
* **Dado que o motor em execução precisa reconhecer a alteração**, **quando** o desbloqueio for concluído, **então** deve invalidar a chave do cache em memória e disparar o Hot Reload das listas.
* **Dado que a ação de auditoria é mandatória**, **quando** o processo finalizar, **então** deve gravar um registro de evento `FEEDBACK_LOOP_OVERRIDE` nos logs de auditoria informando o timestamp e o usuário responsável (Seção 3.5.3 do TCC).

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.cli.main unblock 192.0.2.77 \
    --whitelist \
    --reason "Falso Positivo confirmado: Portal bancário corporativo" \
    --operator "admin_victor"
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[FEEDBACK LOOP] Processando solicitação de desbloqueio para 192.0.2.77...
[NETFILTER] Regra DROP revogada com sucesso no kernel (iptables -D FORWARD...).
[DATABASE] IP 192.0.2.77 cadastrado na Whitelist permanente (ID: 52).
[CACHE] Chave 192.0.2.77 expurgada do cache em memória.
[SIGNAL] Notificação de recarga enviada ao motor de decisão.
[AUDIT] Evento 'FEEDBACK_LOOP_OVERRIDE' registrado com sucesso.
[SUCCESS] IP desbloqueado e imunizado contra futuros falsos positivos.
```

**5. Componentes Envolvidos**
* `src/cli/commands.py`: Implementação do subcomando `unblock`.
* `src/engine/netfilter_adapter.py`: Remoção de regra no iptables.
* `src/database/crud_whitelist.py`: Inclusão na Whitelist.
* `src/engine/logger_service.py`: Auditoria do evento.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com o Requisito RF11 (*Feedback Loop*) e a Seção 3.5.3 do TCC (*Ciclo de Feedback e Correção de Erros*), admite-se metodologicamente a existência de uma margem residual de erro na IA. O Feedback Loop é o mecanismo de governança que impede que o mesmo erro se repita.
* Operação atômica entre kernel e banco de dados local.

**7. Mockups ou Referências Visuais**
* Fluxograma do Feedback Loop presente no Capítulo 3 do TCC.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #38 (Execução de Bloqueio), Issue #40 (Logging), Issue #44 (CLI) e Issue #45 (Hot Reload).
* **Bloqueia:** Issue #48 (Teste de Falsos Positivos) e Issue #50 (Eficácia Comparativa).

**9. Como Testar (Plano de Teste)**
1. Simular o bloqueio de um IP mock gerando regra no iptables.
2. Executar o comando CLI `unblock --whitelist`.
3. Validar se a regra do iptables desapareceu (`iptables -L FORWARD -n`).
4. Validar se o IP consta na Whitelist (`firewall-cli whitelist list`).
5. Executar os testes automatizados via `pytest tests/test_feedback_loop.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Comando `unblock` implementado com tratamento de exceções.
* Testes de integração simulando desbloqueio, gravação no banco e log de auditoria passando.
* Confirmação de que o IP desbloqueado não sofre nova retenção pela IA.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Garante a resiliência operacional da rede).
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `feedback-loop`, `governance`, `unblock`, `mitigation`.

**13. Documentação Relacionada**
* Requisito RF11 (Feedback Loop de Falsos Positivos).
* Seção 3.5.3 do TCC (*Ciclo de Feedback e Correção de Erros*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

# 🧪 Grupo 7: Testes, Validação e Eficiência

### **Issue #47: [Backend/Infraestrutura] Teste de latência: Medição do impacto da votação no tempo de resposta**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** executar uma suíte de medição experimental de latência para quantificar o tempo total de resposta ($T_{verdict}$), desde a captura do primeiro pacote até a aplicação do DROP no iptables,
> **para que** possamos verificar formalmente se o limite crítico de 200ms (RNF01) é cumprido sob os Cenários de Hardware A, B e C, avaliando o risco de condição de corrida (*race condition*) contra o TCP (Seção 3.4.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que 100 sessões sintéticas são enviadas através do gateway**, **quando** medido o tempo total $T_{verdict}$ (Extração de Features in-flight + Inferência Ensemble + Inserção Netfilter), **então** a média sob o Cenário B (0.5 vCPU, 812MB RAM) deve ser estritamente inferior a 200 milissegundos (RNF01).
* **Dado que conexões subsequentes recorrem ao cache em memória**, **quando** mensurada a latência de veredito no cache, **então** o tempo médio deve ser inferior a 5 milissegundos.
* **Dado os experimentos nos três cenários**, **quando** finalizada a bateria de testes, **então** deve salvar as medições em `data/reports/latency_benchmark.json` e plotar o gráfico de densidade de latência em `docs/evaluation/latency_distribution.png`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.test_latency \
    --scenarios A B C \
    --samples 100 \
    --output-json data/reports/latency_benchmark.json \
    --output-plot docs/evaluation/latency_distribution.png
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[BENCHMARK] Executando medição de latência T-Verdict (100 amostras por cenário)...
[CENÁRIO A - Sem Restrições]:
  - Latência Média: 14.2 ms (DP: 2.1 ms) | P95: 18.5 ms | P99: 22.1 ms
[CENÁRIO B - Baixo Recurso: 0.5 vCPU, 812MB RAM]:
  - Latência Média: 48.6 ms (DP: 6.4 ms) | P95: 64.2 ms | P99: 82.5 ms (Meta RNF01: < 200 ms [CUMPRIDA])
[CENÁRIO C - Crítico: 0.25 vCPU, 256MB RAM]:
  - Latência Média: 168.4 ms (DP: 24.1 ms) | P95: 215.0 ms (Ponto de saturação evidenciado)
[CACHE HIT]:
  - Latência Média: 0.85 ms (DP: 0.12 ms)
[SUCCESS] Gráfico gerado em docs/evaluation/latency_distribution.png
```

**5. Componentes Envolvidos**
* `tests/benchmark/test_latency.py`: Suíte de medição de latência em microssegundos.
* `src/engine/decision_engine.py` e `src/engine/block_executor.py`.
* `docs/evaluation/latency_distribution.png`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade direta com a Seção 3.4.2 do TCC (*Latência de Inferência e Condição de Corrida*), a demonstração quantitativa de que $T_{verdict} < 200ms$ prova que a decisão é tomada antes da transferência de dados do site de apostas.
* Uso de timers de alta resolução `time.perf_counter_ns()`.

**7. Mockups ou Referências Visuais**
* Gráfico de densidade e boxplot de latência comparando Cenários A, B e C.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #07 (Limites Docker), Issue #37 (Lógica de Decisão) e Issue #38 (Execução do Bloqueio).
* **Bloqueia:** Issue #52 (Benchmark de CPU) e Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar a suíte de latência no Cenário B configurado no Docker Compose.
2. Inspecionar o JSON de saída e conferir se `mean_latency_ms < 200.0`.
3. Inspecionar visualmente o boxplot gerado.
4. Executar os testes automatizados via `pytest tests/benchmark/test_latency.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script de benchmark de latência implementado com repetibilidade estatística.
* Relatório JSON e gráfico de alta resolução exportados com sucesso.
* Comprovação experimental do atendimento ao Requisito RNF01.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Requisito não funcional RNF01 chave).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `benchmark`, `latency`, `t-verdict`, `race-condition`, `performance`.

**13. Documentação Relacionada**
* Requisito RNF01 (Latência Crítica < 200ms).
* Seção 3.4.2 do TCC (*Latência de Inferência e Condição de Corrida*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #48: [Backend] Teste de Falsos Positivos em sites críticos**

**1. História de Usuário (User Story)**
> **Como** auditor de qualidade do projeto,
> **eu quero** conduzir testes automatizados de navegação em uma lista de 50 domínios institucionais e críticos (portais bancários, governamentais, notícias e streaming),
> **para que** possamos verificar se a taxa de falsos positivos ($FPR$) em regime dinâmico se mantém estritamente abaixo do limite de 5.0% estabelecido como critério de rejeição da hipótese (RNF06 e Seção 3.4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o coletor automatizado acessa 50 portais benignos críticos** (ex.: Receita Federal, Caixa, YouTube, G1, BBC), **quando** o tráfego transitar pelo gateway, **então** o sistema deve registrar a decisão de cada fluxo em tempo real.
* **Dado que nenhum desses domínios contém apostas**, **quando** calculada a taxa de Falsos Positivos ($FPR = \frac{FP}{Total}$), **então** o resultado não deve exceder 5.0% (Seção 3.4.5 do TCC).
* **Dado qualquer falso positivo detectado durante o teste**, **quando** acionado o procedimento de moderação, **então** deve validar a atuação do Feedback Loop (#46), certificando a restauração do acesso.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.test_critical_sites \
    --sites-file config/critical_sites.txt \
    --output-json data/reports/false_positive_report.json
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[AUDITORIA] Iniciando teste de falsos positivos em 50 portais críticos...
[PROGRESS] 10/50 sítios testados... (Gov.br, Caixa, BB: PASS)
[PROGRESS] 25/50 sítios testados... (YouTube, Wikipedia, UOL: PASS)
[PROGRESS] 50/50 sítios testados...
================ RESULTADO DE FALSOS POSITIVOS ================
  - Total de portais testados: 50
  - Sessões concluídas com sucesso (PASS): 49 (98.0%)
  - Falsos Positivos identificados: 1 (2.0%) [Portal institucional com websocket dinâmico]
  - Taxa de Falsos Positivos (FPR): 2.0% (Critério < 5.0% cumprido com sucesso!)
[FEEDBACK LOOP] Acionando imunização automática para o domínio com falso positivo... [OK]
[SUCCESS] Relatório salvo em data/reports/false_positive_report.json
```

**5. Componentes Envolvidos**
* `tests/benchmark/test_critical_sites.py`: Orquestrador de auditoria em sites críticos.
* `config/critical_sites.txt`: Lista dos 50 portais de controle.
* `src/engine/decision_engine.py` e `src/collector/collect_benign_traffic.py`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade direta com a Seção 3.4.5 do TCC (*Critérios de Rejeição da Hipótese*), uma taxa de Falso Positivo $> 5\%$ invalida a hipótese de viabilidade de firewall em baixos recursos, pois a indisponibilidade de serviços essenciais inviabilizaria sua implantação em redes reais.
* Documentação de cada falso positivo ocorrido com os respectivos votos do comitê.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #37 (Lógica de Decisão) e Issue #46 (Feedback Loop).
* **Bloqueia:** Issue #54 (Gráficos Finais) e Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar a rotina apontando para a lista de 50 domínios críticos.
2. Inspecionar o JSON de saída e certificar que `fpr <= 0.05`.
3. Validar se o Feedback Loop foi invocado para qualquer divergência.
4. Executar os testes automatizados via `pytest tests/benchmark/test_critical_sites.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `test_critical_sites.py` funcional com navegação em lote.
* Comprovação experimental de $FPR < 5.0\%$.
* Relatório JSON de auditoria gerado.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Validação direta do critério de rejeição da hipótese).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`backend`, `testing`, `false-positives`, `critical-sites`, `validation`.

**13. Documentação Relacionada**
* Requisito RNF06 (Disponibilidade).
* Seção 3.4.5 do TCC (*Critérios de Rejeição da Hipótese*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #49: [Infraestrutura] Teste de estresse: Simulação de carga pesada e vazão**

**1. História de Usuário (User Story)**
> **Como** engenheiro de infraestrutura do projeto,
> **eu quero** realizar testes de estresse injetando tráfego sintético massivo (de 50 até 200 novos fluxos por segundo com `tcpreplay` ou gerador multiprocesso),
> **para que** possamos identificar o ponto de saturação do sistema e certificar que a vazão mínima de 50 fluxos/s seja sustentada sem sobrecarregar a CPU além de 60% (RNF03, RNF04 e Seção 3.4.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o gerador de tráfego injeta 50 novos fluxos por segundo continuadamente**, **quando** o motor processar a carga, **então** a taxa de perda de pacotes por enfileiramento deve ser nula e a CPU não deve sofrer starvation (RNF04).
* **Dado o incremento escalonado da taxa até 200 fluxos/s**, **quando** o gateway atingir o limite de processamento, **então** deve mapear e registrar a curva de saturação (relação entre vazão e latência média).
* **Dado o término do teste de estresse**, **quando** consolidados os dados, **então** deve gerar o relatório em `docs/evaluation/stress_report.json` e a curva de vazão em `docs/evaluation/stress_throughput_curve.png`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.test_stress \
    --rates 25 50 100 150 200 \
    --duration-per-rate 60 \
    --output-json docs/evaluation/stress_report.json \
    --output-plot docs/evaluation/stress_throughput_curve.png
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[ESTRESSE] Iniciando bateria de saturação (Duração: 60s por taxa)...
  - Taxa 25 fluxos/s: Latência média = 32.4 ms | Descarte = 0% | CPU = 24.5%
  - Taxa 50 fluxos/s (Meta RNF04): Latência média = 48.2 ms | Descarte = 0% | CPU = 44.8% [CONFORME]
  - Taxa 100 fluxos/s: Latência média = 92.1 ms | Descarte = 0.2% | CPU = 72.1%
  - Taxa 200 fluxos/s: Latência média = 284.0 ms | Descarte = 4.8% | CPU = 98.4% (Saturação Atingida)
================ SÍNTESE DO PONTO DE SATURAÇÃO ================
  - Vazão sustentável garantida (sem perdas): 65 fluxos/s (Superior aos 50 fluxos/s do RNF04)
  - Limiar de degradação exponencial: > 120 fluxos/s
[SUCCESS] Gráfico salvo em docs/evaluation/stress_throughput_curve.png
```

**5. Componentes Envolvidos**
* `tests/benchmark/test_stress.py`: Gerador de tráfego massivo e coletor de saturação.
* `src/engine/live_sniffer.py` e `src/engine/decision_engine.py`.
* `docs/evaluation/stress_throughput_curve.png`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Seção 3.4.3 do TCC (*Teste de Estresse e Ponto de Saturação*) e com o Requisito RNF04 (*Vazão de Classificação*), a identificação do ponto de saturação é essencial para definir o dimensionamento da rede recomendada para o firewall.
* Uso de injeção assíncrona multiprocesso para não limitar o teste pela capacidade da máquina de geração.

**7. Mockups ou Referências Visuais**
* Curva de Vazão vs Latência (gráfico de saturação em S).

**8. Dependências e Bloqueios**
* **Depende de:** Issue #07 (Limites Docker), Issue #34 (Sniffer em Tempo Real) e Issue #37 (Lógica de Decisão).
* **Bloqueia:** Issue #52 (Benchmark de CPU) e Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar o teste de estresse na taxa base de 50 fluxos/s por 30 segundos.
2. Inspecionar se ocorreram perdas de pacotes na fila.
3. Testar a taxa máxima de 200 fluxos/s e verificar se o log capturou o ponto de saturação.
4. Executar os testes automatizados via `pytest tests/benchmark/test_stress.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `test_stress.py` funcional com geração de taxas variáveis.
* Comprovação de cumprimento da meta de vazão $\ge 50$ fluxos/s sem perdas (RNF04).
* Gráfico de saturação gerado em alta resolução.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`infraestrutura`, `stress-testing`, `throughput`, `saturation-point`, `benchmarking`.

**13. Documentação Relacionada**
* Requisitos RNF03 (CPU) e RNF04 (Vazão de Classificação).
* Seção 3.4.3 do TCC (*Teste de Estresse e Ponto de Saturação*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #50: [Backend] Validação da eficácia comparativa do bloqueio manual vs. bloqueio preditivo da IA**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** conduzir um experimento comparativo navegando em novas plataformas de apostas não catalogadas e domínios recém-criados (*Domain Fluxing*), contrastando o bloqueio estático por Blacklist contra a detecção comportamental do Comitê de IA,
> **para que** possamos comprovar cientificamente que o aprendizado de máquina supera a abordagem de listas tradicionais na neutralização de estratégias de evasão de casas de apostas (Seção 1.1, 2.1 e 4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado uma lista de 20 domínios inéditos de casas de apostas** (nunca cadastrados na Blacklist manual), **quando** o tráfego for inspecionado pelo gateway, **então** a Blacklist estática deve falhar em 100% dos casos, enquanto o Comitê de IA deve detectar e bloquear com taxa $\ge 85\%$.
* **Dado que casas de apostas utilizam múltiplos provedores de CDN** (Cloudflare, Fastly, Cloudfront), **quando** avaliada a predição da IA, **então** deve demonstrar que a decisão foi baseada na assinatura comportamental do tráfego (IAT e pacotes curtos) independente do IP de destino.
* **Dado a consolidação dos dados**, **quando** finalizado o experimento, **então** deve gerar a tabela comparativa em `docs/evaluation/comparative_efficacy_report.json` e `docs/evaluation/comparative_table.md`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.test_comparative_efficacy \
    --targets-file config/new_unlisted_betting.txt \
    --output-json docs/evaluation/comparative_efficacy_report.json \
    --output-table docs/evaluation/comparative_table.md
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[EXPERIMENTO] Avaliando eficácia em 20 domínios inéditos de apostas...
  - Domínio 1 (bet-novo-exemplo.com): Blacklist = PASS (Falhou) | IA = DROP (Detectou em 7.8 ms)
  - Domínio 2 (apostas-aovivo-cdn.net): Blacklist = PASS (Falhou) | IA = DROP (Detectou em 8.1 ms)
  ...
================ RESULTADO COMPARATIVO DE EFICÁCIA ================
Estratégia             | Bloqueios | Evasões | Taxa de Eficácia
-----------------------|-----------|---------|------------------
Blacklist Manual       | 0 / 20    | 20 / 20 | 0.0% (Inócua contra domínios inéditos)
Comitê IA (Hard Vote)  | 18 / 20   | 2 / 20  | 90.0% (Comprovada alta eficácia)
-------------------------------------------------------------------
[CONCLUSÃO] A IA neutralizou a evasão por troca de domínio em 90% dos casos.
[SUCCESS] Relatórios gerados em docs/evaluation/
```

**5. Componentes Envolvidos**
* `tests/benchmark/test_comparative_efficacy.py`: Script do experimento comparativo.
* `config/new_unlisted_betting.txt`: Lista de 20 domínios não catalogados.
* `src/engine/decision_engine.py`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com a Problemática (Seção 1.1) e Discussão dos Resultados (Seção 4.5 do TCC), este experimento fornece a justificativa empírica definitiva do trabalho, demonstrando que firewalls estáticos tradicionais são impotentes contra a indústria de apostas online.
* Registro de justificativa detalhada para os eventuais 2 casos não detectados.

**7. Mockups ou Referências Visuais**
* Gráfico de barras comparando taxa de bloqueio Blacklist vs IA.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #37 (Lógica de Decisão) e Issue #43 (CRUD Blacklist).
* **Bloqueia:** Issue #54 (Gráficos Finais) e Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar o experimento comparativo com alvos não cadastrados na Blacklist.
2. Conferir se a taxa de bloqueio da IA atinge pelo menos 85%.
3. Inspecionar a tabela Markdown gerada.
4. Executar os testes automatizados via `pytest tests/benchmark/test_comparative_efficacy.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `test_comparative_efficacy.py` implementado com testes automatizados.
* Tabela comparativa e relatório JSON gerados com dados empíricos.
* Comprovação da superioridade da IA frente a listas estáticas.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Valor acadêmico fundamental do TCC).
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`backend`, `comparative-analysis`, `efficacy`, `domain-fluxing`, `tcc-experiment`.

**13. Documentação Relacionada**
* Seção 1.1 (*Problemática*), Seção 2.1 e Seção 4.5 (*Plano de Discussão dos Resultados*).

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

### **Issue #51: [Infraestrutura] Teste de persistência e recuperação após reinício de container**

**1. História de Usuário (User Story)**
> **Como** engenheiro DevOps do projeto,
> **eu quero** testar o comportamento do sistema diante de reinicializações abruptas e quedas de containers (`docker compose restart firewall_gateway`),
> **para que** possamos validar que as listas no banco SQLite, o cache reconstruído e as políticas de Netfilter permaneçam íntegras e em conformidade com o princípio de Failsafe (RNF06 e RNF07).

**2. Critérios de Aceitação (AC)**
* **Dado que o banco SQLite contém 100 regras de listas**, **quando** o container `firewall_gateway` for reiniciado forçadamente via `docker kill` e `docker start`, **então** nenhum registro do banco de dados deve ser corrompido ou perdido (RNF07).
* **Dado que o firewall é religado após falha**, **quando** o daemon subir, **então** deve recarregar as políticas do banco SQLite e restaurar o estado operacional em menos de 10 segundos.
* **Dado o modo Failsafe configurado** (RNF06), **quando** o processo de IA travar intencionalmente, **então** o sistema deve garantir a política administrativa configurada (modo seguro: bypass com alerta ou bloqueio defensivo).

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.integration.test_persistence_failsafe
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[FAILSAFE TEST] Populando banco SQLite com 100 regras de teste... [OK]
[FAILSAFE TEST] Executando reinicialização abrupta do container (SIGKILL)...
[DOCKER] Container firewall_gateway parado forçadamente.
[DOCKER] Reiniciando container...
[RECOVERY] Daemon reinicializado em 4.2 segundos.
[VERIFY] Integridade do SQLite: 100 / 100 registros preservados (Modo WAL íntegro).
[VERIFY] Regras do Netfilter: Reaplicadas no kernel com sucesso.
[SUCCESS] Teste de persistência e Failsafe aprovado com 100% de conformidade.
```

**5. Componentes Envolvidos**
* `tests/integration/test_persistence_failsafe.py`: Script de teste de falha e recuperação.
* Docker Compose (`docker compose restart`).
* Volumes `/volumes/db` e `/volumes/logs`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RNF06 (*Disponibilidade e Failsafe*) e RNF07 (*Persistência de Dados*), o teste comprova que o firewall de borda é resiliente a quedas de energia no roteador sem requerer intervenção técnica.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #03 (Volumes Docker), Issue #41 (Modelagem SQLite) e Issue #45 (Hot Reload).
* **Bloqueia:** Issue #57 (Scripts de Laboratório).

**9. Como Testar (Plano de Teste)**
1. Executar o script de teste de persistência contra o container Docker ativo.
2. Inspecionar logs pós-recuperação e validar tempo de restauração $< 10s$.
3. Conferir a integridade das tabelas do banco de dados.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script de teste automatizado implementado.
* Teste de integridade de dados e restauração passando com 100%.
* Conformidade comprovada com os requisitos RNF06 e RNF07.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`infraestrutura`, `failsafe`, `persistence`, `docker`, `resilience`.

**13. Documentação Relacionada**
* Requisitos RNF06 (Disponibilidade) e RNF07 (Persistência).
* Seção 3.1.2 do TCC (*Camadas de Defesa e Subsistemas*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #52: [Infraestrutura] Benchmark de CPU: Monitoramento do uso de processamento durante a inferência**

**1. História de Usuário (User Story)**
> **Como** pesquisador de sistemas embarcados,
> **eu quero** instrumentar e registrar continuamente o uso percentual de processamento de CPU durante janelas ativas de inferência sob as cotas de 0.5 vCPU e 1 vCPU,
> **para que** possamos certificar que a inferência do Comitê de IA não cause inanição (*starvation*) e se mantenha abaixo do teto de 60% estabelecido no Requisito RNF03 (Seção 3.4.1 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o motor processa tráfego contínuo sob a restrição de 0.5 vCPU** (Cenário B), **quando** monitorado a cada 100ms via `psutil` ou métricas de cgroups do Docker, **então** o consumo médio de CPU não deve ultrapassar 60% em regime estável (RNF03).
* **Dado o pico máximo de chegadas de novos fluxos**, **quando** a inferência conjunta do ensemble ocorrer, **então** o encaminhamento básico de pacotes do kernel (`ip_forward`) não deve ser degradado por falta de ciclos de CPU.
* **Dado o término do benchmark**, **quando** consolidados os dados, **então** deve gerar o relatório em `docs/evaluation/cpu_benchmark_report.json` e o gráfico temporal de consumo em `docs/evaluation/cpu_usage_profile.png`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.monitor_cpu \
    --duration 120 \
    --interval 0.1 \
    --output-json docs/evaluation/cpu_benchmark_report.json \
    --output-plot docs/evaluation/cpu_usage_profile.png
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[CPU BENCHMARK] Monitorando cgroup do firewall_gateway por 120s (Cota: 0.5 vCPU)...
  - Consumo em repouso: 2.4% da vCPU
  - Consumo sob tráfego contínuo (50 fluxos/s): 42.8% de CPU média (Pico: 56.2%)
================ RESULTADO DE CPU (RNF03) ================
  - Média observada: 42.8% (< 60.0% do RNF03 [CONFORME])
  - Picos instantâneos: 56.2% (Sem ocorrência de starvation)
  - Latência de forwarding do kernel preservada em < 0.2 ms
[SUCCESS] Gráfico temporal gerado em docs/evaluation/cpu_usage_profile.png
```

**5. Componentes Envolvidos**
* `tests/benchmark/monitor_cpu.py`: Coletor de métricas de processamento.
* `psutil` / cgroups Linux (`/sys/fs/cgroup/cpu`).
* `docs/evaluation/cpu_usage_profile.png`.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com o Requisito RNF03 (*Carga de CPU*) e a Seção 3.4.1 do TCC (*Utilização de CPU*), o firewall de borda não pode monopolizar os ciclos de processamento de um roteador doméstico.

**7. Mockups ou Referências Visuais**
* Gráfico de linha temporal de consumo de CPU (%) ao longo do tempo.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #07 (Limites Docker), Issue #47 (Latência) e Issue #49 (Estresse).
* **Bloqueia:** Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Iniciar o monitor de CPU em paralelo com um teste de tráfego.
2. Inspecionar o JSON de saída e conferir `mean_cpu_percent < 60.0`.
3. Validar se o gráfico de perfil de CPU foi gerado.
4. Executar os testes automatizados via `pytest tests/benchmark/test_monitor_cpu.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `monitor_cpu.py` implementado com coleta de alta resolução.
* Cumprimento da meta de CPU $< 60\%$ comprovada.
* Gráfico e relatório JSON exportados com sucesso.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Alta.

**12. Etiquetas (Labels)**
`infraestrutura`, `cpu-benchmark`, `cgroups`, `performance`, `rnf03`.

**13. Documentação Relacionada**
* Requisito RNF03 (Carga de CPU < 60%).
* Seção 3.4.1 do TCC (*Utilização de CPU*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #53: [Infraestrutura] Benchmark de RAM: Monitoramento do footprint de memória do motor de IA**

**1. História de Usuário (User Story)**
> **Como** arquiteto do projeto,
> **eu quero** monitorar a alocação de memória RAM residente (RSS) do container ao longo de testes prolongados sob a cota estrita de 512MB / 812MB,
> **para que** possamos comprovar a ausência de vazamentos de memória (*memory leaks*) e certificar que o processo nunca seja terminado pelo OOM Killer do Linux (RNF02 e Seção 3.4.1 e 3.4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o container opera sob o limite rígido de 512MB RAM** (Cenário B), **quando** o consumo for medido ao longo de 180 segundos processando tráfego contínuo, **então** o uso estável de RAM não deve ultrapassar 80% da quota estabelecida (ou seja, $< 409.6 MB$).
* **Dado o processamento de mais de 10.000 pacotes consecutivos**, **quando** comparado o consumo inicial e final pós-coleta de lixo, **então** o crescimento residual de memória deve ser nulo (ausência de vazamento no buffer circular de fluxos).
* **Dado o encerramento do benchmark**, **quando** finalizada a medição, **então** deve salvar o relatório consolidado em `docs/evaluation/ram_footprint_report.json` e o gráfico de evolução da memória em `docs/evaluation/ram_evolution.png`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.monitor_ram \
    --duration 180 \
    --output-json docs/evaluation/ram_footprint_report.json \
    --output-plot docs/evaluation/ram_evolution.png
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[RAM BENCHMARK] Monitorando alocação RSS em container restrito a 512MB por 180s...
  - Alocação inicial (após carregar modelos): 98.4 MB (19.2% da cota)
  - Alocação sob carga contínua (10.000 pacotes): 142.1 MB (27.7% da cota)
  - Alocação pós-expurgo do buffer: 104.2 MB (Ausência de memory leak confirmada)
================ RESULTADO DE MEMÓRIA (RNF02) ================
  - Pico máximo de RAM: 142.1 MB (Margem de segurança de 72.3% livre)
  - Estabilidade: 100% | OOM Killer invocado: 0 vezes
[SUCCESS] Gráfico de evolução de RAM salvo em docs/evaluation/ram_evolution.png
```

**5. Componentes Envolvidos**
* `tests/benchmark/monitor_ram.py`: Monitor de memória RAM residente.
* `tracemalloc`, `psutil`.
* `docs/evaluation/ram_evolution.png`.

**6. Considerações Técnicas e Arquitetura**
* Em estrita conformidade com o Requisito RNF02 (*Restrição de Memória RAM - 512MB*) e a Seção 3.4.5 do TCC (*Critérios de Rejeição da Hipótese*), a instabilidade de memória que leve ao encerramento pelo OOM Killer é motivo para rejeição do trabalho.
* O teste contínuo valida o expurgo correto de fluxos inativos pelo coletor.

**7. Mockups ou Referências Visuais**
* Gráfico de área empilhada demonstrando consumo de RAM do daemon ao longo do tempo.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #07 (Limites Docker), Issue #33 (Tamanho de Modelos) e Issue #49 (Estresse).
* **Bloqueia:** Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar o teste de memória com geração contínua de tráfego.
2. Inspecionar o JSON de saída e certificar que `max_ram_mb < 409.6`.
3. Checar a inclinação da curva de memória pós-teste (deve ser plana).
4. Executar os testes automatizados via `pytest tests/benchmark/test_monitor_ram.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `monitor_ram.py` implementado com testes automatizados.
* Ausência comprovada de vazamentos de memória.
* Cumprimento formal da meta de memória RAM do Requisito RNF02.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`infraestrutura`, `ram-benchmark`, `memory-leak-audit`, `oom-killer-prevention`, `rnf02`.

**13. Documentação Relacionada**
* Requisito RNF02 (Restrição de Memória RAM - 512MB).
* Seção 3.4.1 e 3.4.5 do TCC (*Footprint e Rejeição da Hipótese*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #54: [Backend] Geração de matrizes de confusão e gráficos comparativos finais**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** um gerador automatizado de gráficos comparativos finais de alta resolução (Matrizes de Confusão multi-cenário, Curvas ROC consolidadas, trade-off de atributos SU vs F1 e histogramas de latência),
> **para que** todas as figuras visuais e dados tabulados dos Capítulos 3 e 4 da monografia do TCC sejam gerados com reprodutibilidade direta a partir dos logs de teste (Seção 4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado os relatórios dos testes** (#31, #47, #48, #50, #52, #53), **quando** o gerador for executado, **então** deve processar os JSONs e renderizar gráficos em formato PNG (300 DPI) e SVG vetorial no diretório `docs/figures/`.
* **Dado o requisito de análise de dimensionalidade** (Seção 4.5.1 do TCC), **quando** renderizar o gráfico de trade-off de SU, **então** deve demonstrar a evolução de F1-Score e tempo de inferência conforme a quantidade de atributos varia de 1 a 24.
* **Dado o requisito de comparação do Ensemble** (Seção 4.5.2 do TCC), **quando** plotar a comparação de modelos, **então** deve evidenciar a superioridade do Comitê frente aos modelos isolados na redução de falsos positivos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.visualization.generate_final_figures \
    --reports-dir data/reports/ \
    --evaluation-dir docs/evaluation/ \
    --output-dir docs/figures/
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[VISUALIZAÇÃO] Lendo artefatos de avaliação em docs/evaluation/...
  - Renderizado: docs/figures/fig3_matriz_confusao_mundo_aberto.png (300 DPI)
  - Renderizado: docs/figures/fig4_curva_roc_ensemble.png (300 DPI)
  - Renderizado: docs/figures/fig5_tradeoff_dimensionalidade_su.png (300 DPI)
  - Renderizado: docs/figures/fig6_latencia_cenarios_abc.png (300 DPI)
  - Renderizado: docs/figures/fig7_comparativo_modelos_isolados.png (300 DPI)
[SUCCESS] 5 figuras acadêmicas geradas e prontas para inclusão no TCC.
```

**5. Componentes Envolvidos**
* `src/visualization/generate_final_figures.py`: Gerador de artefatos visuais.
* `matplotlib`, `seaborn`: Renderização científica com tema padronizado.
* `docs/figures/`: Diretório de saída das imagens finais do TCC.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade direta com a Seção 4.5 do TCC (*Plano de Discussão e Análise dos Resultados*), as figuras sintetizam visualmente o trade-off de dimensionalidade, latência e eficácia estatística.
* Tipografia padronizada em fontes legíveis (Arial/Helvetica/DejaVu Sans) com rótulos e eixos em português formal.

**7. Mockups ou Referências Visuais**
* Galeria de 5 figuras finais do TCC.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #31 (Métricas), Issue #47 (Latência), Issue #48 (Falsos Positivos) e Issue #50 (Eficácia).
* **Bloqueia:** Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar o gerador sobre a pasta com os dados de avaliação.
2. Conferir se todas as 5 imagens foram criadas em `docs/figures/`.
3. Inspecionar visualmente o contraste, legendas e resolução.
4. Executar os testes automatizados via `pytest tests/test_generate_final_figures.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Script `generate_final_figures.py` implementado com testes automatizados.
* Todas as figuras acadêmicas geradas em 300 DPI e SVG.
* Ausência de sobreposição de textos ou legendas cortadas.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`backend`, `data-visualization`, `academic-figures`, `matplotlib`, `tcc-final`.

**13. Documentação Relacionada**
* Capítulo 4 (*Resultados Esperados*) e Seção 4.5 do TCC.

**14. Estimativa**
* **T-Shirt Size:** M (Medium)
* **Story Points:** 3


---

# 📂 Grupo 8: Documentação e Finalização

### **Issue #55: [Infraestrutura/Backend] Refatoração do código e padronização técnica (PEP8)**

**1. História de Usuário (User Story)**
> **Como** líder técnico do projeto,
> **eu quero** auditar, refatorar e padronizar toda a base de código do repositório conforme o guia de estilo PEP8 utilizando ferramentas automatizadas (Black, Flake8, isort) e type hints completos,
> **para que** o projeto atinja excelência técnica, facilidade de manutenção e rigor acadêmico para apresentação perante a banca examinadora do TCC.

**2. Critérios de Aceitação (AC)**
* **Dado todos os arquivos Python em `src/` e `tests/`**, **quando** inspecionados pelo `flake8`, **então** nenhum erro de formatação ou violação de estilo crítico deve ser detectado (taxa de conformidade 100%).
* **Dado que o projeto adota tipagem estática moderna**, **quando** executado o `mypy`, **então** as assinaturas de funções públicas dos módulos de extração, inferência e banco de dados devem conter type hints válidos.
* **Dado que o repositório deve manter integridade contínua**, **quando** executado `pytest`, **então** todos os 90+ testes automatizados da suíte devem passar com 100% de sucesso.

**3. Exemplo de Requisição (Código/CLI)**
```bash
black src/ tests/
isort src/ tests/
flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503
pytest
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[BLACK] All done! 24 files left unchanged.
[ISORT] Fixing imports in src/ and tests/... Done!
[FLAKE8] Verificação concluída: 0 erros ou avisos encontrados.
[PYTEST] =================== 92 passed in 8.42s ===================
[SUCCESS] Código 100% padronizado sob o padrão PEP8 com tipagem validada.
```

**5. Componentes Envolvidos**
* Todos os módulos em `src/` e `tests/`.
* `setup.cfg`, `pyproject.toml`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com as boas práticas de engenharia de software e a Seção 3 do TCC, a manutenibilidade do código garante que o software possa ser auditado por pesquisadores externos.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Todas as issues de desenvolvimento funcional (#01 a #54).
* **Bloqueia:** Issue #56 (README) e Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar `flake8 src/ tests/`.
2. Executar `pytest` e verificar aprovação completa.
3. Verificar a ausência de warnings críticos no terminal.

**10. Definição de Pronto (Definition of Done - DoD)**
* Zero erros de linting no Flake8.
* Tipagem estática validada.
* Suíte de testes 100% aprovada.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`refactor`, `pep8`, `code-quality`, `linting`, `typing`.

**13. Documentação Relacionada**
* Diretrizes PEP8 e arquitetura do TCC.

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #56: [Documentação] Elaboração do README.md com manual e arquitetura**

**1. História de Usuário (User Story)**
> **Como** avaliador da banca do TCC ou desenvolvedor da comunidade,
> **eu quero** um arquivo `README.md` abrangente, didático e visualmente bem estruturado na raiz do repositório,
> **para que** seja possível compreender a fundamentação do projeto, visualizar o diagrama da arquitetura Docker, clonar o projeto e executá-lo em poucos passos (Seção 1.2, 3.1 e 3.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o arquivo `README.md` na raiz**, **quando** consultado, **então** deve conter: Título oficial do TCC, Resumo da proposta, Badges de status dos testes, Diagrama arquitetural em Mermaid (Topologia Gateway ↔ Cliente), Pré-requisitos e Instruções de deploy em 1 comando via Docker Compose.
* **Dado que o usuário deseja operar o sistema**, **quando** consultar o README, **então** deve apresentar o Manual de Uso da CLI com exemplos práticos dos comandos `status`, `whitelist`, `blacklist`, `unblock` e `logs`.
* **Dado que o avaliador busca os resultados científicos**, **quando** consultar a seção de resultados, **então** deve apresentar tabela resumo com as métricas de acurácia, latência e consumo de recursos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
cat README.md | head -n 40
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```markdown
# Firewall Inteligente para Bloqueio de Casas de Apostas em Ambientes de Baixos Recursos

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
[![Docker](https://img.shields.io/badge/docker-ready-blue)]()

Um sistema proativo de classificação de tráfego de rede (NTC) criptografado sob restrição de hardware...
```

**5. Componentes Envolvidos**
* `README.md`: Documento principal do repositório.
* `docs/architecture.png`: Diagrama visual.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Capítulo 3 do TCC, a documentação pública deve permitir a reprodutibilidade integral do laboratório de testes por terceiros.

**7. Mockups ou Referências Visuais**
* Diagrama Mermaid renderizado no GitHub/GitLab.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #55 (Refatoração de Código) e Issue #44 (CLI).
* **Bloqueia:** Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Renderizar o `README.md` em visualizador Markdown e checar formatação de links, tabelas e diagramas.
2. Seguir as instruções do guia rápido em uma máquina limpa e validar se o laboratório sobe sem erros.

**10. Definição de Pronto (Definition of Done - DoD)**
* `README.md` completo com manual da CLI, arquitetura e instruções de laboratório.
* Diagrama Mermaid validado sem erros de sintaxe.
* Todos os links internos e externos testados e funcionais.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`documentation`, `readme`, `manual`, `open-source`, `tcc-presentation`.

**13. Documentação Relacionada**
* Capítulos 1, 3 e 4 do TCC.

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #57: [Infraestrutura] Criação de scripts de configuração automática do laboratório**

**1. História de Usuário (User Story)**
> **Como** pesquisador e examinador do projeto,
> **eu quero** scripts de automação (`setup_lab.sh` para Linux/macOS e `setup_lab.ps1` para Windows),
> **para que** todo o ambiente (criação de diretórios de dados, permissões de volume, migrações do SQLite com seed de dados e subida dos containers Docker) seja configurado automaticamente com um único comando.

**2. Critérios de Aceitação (AC)**
* **Dado um host com Docker instalado**, **quando** o script `./scripts/setup_lab.sh` (ou `.ps1`) for executado, **então** deve checar pré-requisitos, provisionar a árvore de diretórios `/data/` e `/volumes/` e compilar as imagens do Dockerfile base.
* **Dado que o banco de dados ainda não foi populado**, **quando** o setup rodar, **então** deve aplicar as migrações automáticas do SQLite e inserir as sementes iniciais de Whitelist e Blacklist.
* **Dado que o ambiente sobe com sucesso**, **quando** os containers estiverem em estado `healthy`, **então** deve exibir no terminal uma mensagem de boas-vindas com o comando sugerido para abrir a CLI ou iniciar a coleta.

**3. Exemplo de Requisição (Código/CLI)**
```bash
bash scripts/setup_lab.sh --build
# No Windows:
powershell -ExecutionPolicy Bypass -File scripts/setup_lab.ps1 -Build
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
================ CONFIGURAÇÃO DO LABORATÓRIO TCC ================
[CHECK] Docker Engine detectado: v26.1.0 [OK]
[CHECK] Docker Compose detectado: v2.27.0 [OK]
[DIRS] Estrutura de diretórios criada em data/ e volumes/ [OK]
[DB] Banco de dados SQLite provisionado com seed inicial [OK]
[BUILD] Construindo imagens dos containers... [OK]
[START] Inicializando containers em modo Gateway Bridge... [OK]
================ LABORATÓRIO PRONTO PARA USO ================
Para abrir a interface administrativa CLI, execute:
  docker exec -it firewall_gateway python -m src.cli.main status
```

**5. Componentes Envolvidos**
* `scripts/setup_lab.sh` e `scripts/setup_lab.ps1`.
* `docker-compose.yml`, `infra/Dockerfile.base`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade com o Requisito RNF05 (*Isolamento via Docker*) e RNF07 (*Persistência de Dados*), a automação de setup elimina erros de configuração manual do examinador.

**7. Mockups ou Referências Visuais**
* N/A.

**8. Dependências e Bloqueios**
* **Depende de:** Issue #03 (Docker Compose) e Issue #41.1 (Seed de Dados).
* **Bloqueia:** Issue #58 (Relatório Final do TCC).

**9. Como Testar (Plano de Teste)**
1. Executar o script em ambiente limpo e verificar se todos os containers sobem sem erro.
2. Conferir se o banco de dados foi criado e populado.
3. Testar a execução do comando CLI sugerido no final.

**10. Definição de Pronto (Definition of Done - DoD)**
* Scripts Bash e PowerShell implementados e testados.
* Provisionamento automático funcional em um único comando.
* Tratamento de falhas para casos em que o Docker não esteja em execução.

**11. Prioridade e Severidade**
* **Prioridade:** Média.
* **Severidade:** Média.

**12. Etiquetas (Labels)**
`infraestrutura`, `automation`, `devops`, `bash`, `powershell`, `setup`.

**13. Documentação Relacionada**
* Requisito RNF05 (Isolamento via Docker).
* Seção 3.1.1 do TCC (*Topologia do Laboratório Central*).

**14. Estimativa**
* **T-Shirt Size:** S (Small)
* **Story Points:** 2


---

### **Issue #58: [Documentação] Consolidação final dos resultados (Relatório de Eficiência vs. Acurácia)**

**1. História de Usuário (User Story)**
> **Como** autor do TCC,
> **eu quero** redigir e consolidar um relatório técnico exaustivo (`docs/relatorio_final_resultados.md`), cruzando os dados empíricos de Acurácia, F1-Score, Falsos Positivos, Latência de Veredito ($T_{verdict}$), Consumo de CPU e Footprint de RAM entre os Cenários A, B e C,
> **para que** a hipótese de viabilidade do Firewall Inteligente em Ambientes de Baixos Recursos seja formalmente comprovada e validada para compor os Capítulos 4, 4.5 e 6 da versão definitiva da monografia (Seção 4 e 4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que todos os experimentos foram concluídos**, **quando** compilados os dados, **então** o relatório deve apresentar tabelas comparativas detalhando métricas de eficácia de detecção vs consumo de hardware para os três cenários:
  - Cenário A: Referência sem limites;
  - Cenário B: Baixo Recurso (0.5 vCPU, 812MB RAM);
  - Cenário C: Crítico (0.25 vCPU, 256MB RAM).
* **Dado os critérios formais de rejeição da hipótese** (Seção 3.4.5 do TCC), **quando** confrontados com as medições experimentais, **então** o documento deve certificar que:
  1. A latência média $T_{verdict}$ foi inferior a 1 segundo (atingiu $\approx 48.6ms$ no Cenário B);
  2. A memória RAM manteve-se estável sem acionamento do OOM Killer ($< 150MB$ de pico);
  3. A taxa de Falsos Positivos em sites reais manteve-se estritamente abaixo de 5.0% ($2.0\%$ nos testes).
* **Dado o fechamento da discussão científica**, **quando** concluído o relatório, **então** deve sintetizar a análise do trade-off de dimensionalidade por Incerteza Simétrica, a justificativa da superioridade do Comitê de Votação frente a modelos individuais e as diretrizes práticas para a indústria de equipamentos de rede domésticos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
cat docs/relatorio_final_resultados.md | head -n 45
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```markdown
# Relatório Final de Consolidação: Eficiência Computacional vs. Acurácia Preditiva
**Projeto:** Firewall Inteligente para Bloqueio de Casas de Apostas em Ambientes de Baixos Recursos  
**Autor:** Victor  
**Data de Conclusão:** Outubro de 2026  

## 1. Síntese Executiva e Validação da Hipótese
A hipótese central do trabalho postulou que a combinação de redução dimensional por Incerteza Simétrica (SU)
com um comitê de decisão por Hard Voting viabilizaria a classificação de tráfego criptografado em tempo real
em dispositivos de rede de baixo custo sem comprometer a taxa de falsos positivos...
```

**5. Componentes Envolvidos**
* `docs/relatorio_final_resultados.md`: Relatório acadêmico e técnico final.
* Dados de `data/reports/` e figuras de `docs/figures/`.

**6. Considerações Técnicas e Arquitetura**
* Em conformidade direta com os Capítulos 4, 4.5 (*Plano de Discussão dos Resultados*) e 6 (*Considerações Finais*) do TCC, este relatório consolida todos os artefatos de software desenvolvidos ao longo das 58 issues em contribuição científica formal.

**7. Mockups ou Referências Visuais**
* Gráficos e tabelas integrados no documento Markdown.

**8. Dependências e Bloqueios**
* **Depende de:** Todas as issues anteriores do projeto (#01 a #57).
* **Bloqueia:** Conclusão formal e defesa do Trabalho de Conclusão de Curso (TCC).

**9. Como Testar (Plano de Teste)**
1. Conferir se todos os números citados no relatório batem exatamente com os dados dos arquivos JSON gerados pelos benchmarks.
2. Validar a revisão de texto, coesão acadêmica e citações metodológicas.

**10. Definição de Pronto (Definition of Done - DoD)**
* Relatório final completo, com todas as seções metodológicas e comparativas detalhadas.
* Confirmação formal do atendimento aos 11 Requisitos Funcionais e 8 Requisitos Não Funcionais.
* Documento revisado e pronto para submissão à banca examinadora.

**11. Prioridade e Severidade**
* **Prioridade:** Alta (Entrega máxima do projeto).
* **Severidade:** Crítica.

**12. Etiquetas (Labels)**
`documentation`, `tcc-final-report`, `academic-thesis`, `benchmarking-results`, `milestone`.

**13. Documentação Relacionada**
* Todos os Requisitos (RF01 a RF11, RNF01 a RNF08).
* Capítulos 1, 2, 3, 4, 5 e 6 da monografia do TCC.

**14. Estimativa**
* **T-Shirt Size:** L (Large)
* **Story Points:** 5


---
