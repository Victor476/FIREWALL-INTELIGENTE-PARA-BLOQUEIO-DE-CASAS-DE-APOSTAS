🏗️ Grupo 1: Infraestrutura e Ambiente Docker (07 Issues)
Configuração do repositório Git e estrutura de pastas.
Desenvolvimento do Dockerfile base (Python + Ferramentas de Rede).
Configuração do docker-compose.yml (Containers Gateway e App).
Implementação do container Gateway/Bridge para interceptação de tráfego.
Configuração de capacidades de rede do kernel no Docker (Net_Admin).
Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy).
[NOVA] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado.
📡 Grupo 2: Coleta e Geração de Dados (09 Issues)
Ambiente de Automação: Configurar Selenium/Playwright no Docker.
Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot.
Lógica de Navegação: Criar script que simula comportamento humano.
Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído.
Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser).
Dataset de Apostas: Execução da coleta em massa (Bet365, Betano, etc.).
Dataset Benigno: Execução da coleta de sites de controle (YouTube, Notícias).
Validação de Captura: Script para verificar integridade dos PCAPs.
Extração de Metadados Brutos: Relatório de volume e duração por captura.
🧹 Grupo 3: Pré-processamento e Dataset (08 Issues)
Extração de fluxos bi-direcionais (Conversão PCAP para CSV).
Limpeza de dados (Remoção de valores NaN, Inf e duplicatas).
Rotulagem das classes (Apostas vs Benigno) e Label Encoding.
Normalização e padronização de escalas dos dados.
Análise estatística exploratória inicial (EDA) do dataset.
Balanceamento de classes via técnicas de amostragem (SMOTE).
Divisão do dataset em Treino, Validação e Teste.
[NOVA] Redução de dimensionalidade: Seleção de atributos mínimos para diminuir carga computacional .
🧠 Grupo 4: Pipeline de Machine Learning (09 Issues)
Implementação da Regressão Logística (Voto de Minerva/Baseline).
Implementação e treinamento do classificador Random Forest.
Implementação e treinamento do classificador XGBoost.
Implementação do Comitê de Votação Majoritária (Ensemble).
Tuning de hiperparâmetros (Foco em modelos "leves").
Avaliação via validação cruzada ($K$-Fold Cross Validation).
Geração de métricas (Acurácia, F1-Score, Precisão, Recall).
Exportação do modelo final treinado (pickle/joblib).
[NOVA] Medição do tamanho em disco e memória dos modelos treinados.

🛡️ Grupo 5: Motor do Firewall e Integração (07 Issues)
Script de captura e inspeção de pacotes em tempo real.
Módulo de extração de características de fluxo "em voo" (In-flight features).
Integração do script Python com o subsistema de rede (iptables).
Implementação da lógica de decisão: Whitelist → Blacklist → Votação do Comitê.
Criação da lógica de execução do bloqueio (DROP).
Implementação de cache de IPs para otimização de performance.
Sistema de Logging detalhado de eventos e vereditos.
📝 Grupo 6: Gestão de Listas e Moderação (06 Issues)
Modelagem do banco de dados local para Listas (SQLite ou JSON).
Desenvolvimento de módulo CRUD para gestão da Whitelist.
Desenvolvimento de módulo CRUD para gestão da Blacklist Manual.
Implementação de interface CLI para moderação administrativa.
Criação de mecanismo de "Hot Reload" das listas.
Lógica de "Feedback Loop": Adicionar falsos positivos à Whitelist via log.
🧪 Grupo 7: Testes, Validação e Eficiência (08 Issues)
Teste de latência: Medição do impacto da votação no tempo de resposta .
Teste de Falsos Positivos em sites críticos.
Teste de estresse: Simulação de carga pesada com listas extensas.
Validação da eficácia do bloqueio manual vs. bloqueio da IA.
Teste de persistência: Verificação após reinício do container.
Benchmark de CPU: Monitoramento do uso de processamento durante a inferência.
Benchmark de RAM: Monitoramento do footprint de memória do motor de IA.
Geração de matrizes de confusão e gráficos comparativos finais.
📂 Grupo 8: Documentação e Finalização (04 Issues)
Refatoração do código e padronização técnica (PEP8).
Elaboração do README.md com manual e arquitetura.
Criação de scripts de configuração automática do laboratório.
Consolidação final dos resultados (Relatório de Eficiência vs. Acurácia).

