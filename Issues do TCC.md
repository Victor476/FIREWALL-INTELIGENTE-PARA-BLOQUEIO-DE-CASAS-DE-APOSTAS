🏗️ Grupo 1: Infraestrutura e Ambiente Docker (07 Issues)

1) Configuração do repositório Git e estrutura de pastas.
2) Desenvolvimento do Dockerfile base (Python + Ferramentas de Rede).
3) Configuração do docker-compose.yml (Containers Gateway e App).
4) Implementação do container Gateway/Bridge para interceptação de tráfego.
5) Configuração de capacidades de rede do kernel no Docker (Net_Admin).
6) Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy).
7) [NOVA] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado.

📡 Grupo 2: Coleta e Geração de Dados (09 Issues)

8) Ambiente de Automação: Configurar Selenium/Playwright no Docker.
9) Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot.
10) Lógica de Navegação: Criar script que simula comportamento humano.
11) Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído.
12) Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser).
13) Dataset de Apostas: Execução da coleta em massa (Bet365, Betano, etc.).
14) Dataset Benigno: Execução da coleta de sites de controle (YouTube,Streams, Notícias).
15) Validação de Captura: Script para verificar integridade dos PCAPs.
16) Extração de Metadados Brutos: Relatório de volume e duração por captura.

🧹 Grupo 3: Pré-processamento e Dataset (08 Issues)

17) Extração de fluxos bi-direcionais (Conversão PCAP para CSV).
18) Limpeza de dados (Remoção de valores NaN, Inf e duplicatas).
19) Rotulagem das classes (Apostas vs Benigno) e Label Encoding.
20) Normalização e padronização de escalas dos dados.
21) Análise estatística exploratória inicial (EDA) do dataset.
22) Balanceamento de classes via técnicas de amostragem (SMOTE).
23) Divisão do dataset em Treino, Validação e Teste.
24) [NOVA] Redução de dimensionalidade: Seleção de atributos mínimos para diminuir carga computacional.

🧠 Grupo 4: Pipeline de Machine Learning (09 Issues)

25) Implementação da Regressão Logística (Voto de Minerva/Baseline).
26) Implementação e treinamento do classificador Random Forest.
27) Implementação e treinamento do classificador XGBoost.
28) Implementação do Comitê de Votação Majoritária (Ensemble).
29) Tuning de hiperparâmetros (Foco em modelos "leves").
30) Avaliação via validação cruzada ($K$-Fold Cross Validation).
31) Geração de métricas (Acurácia, F1-Score, Precisão, Recall).
32) Exportação do modelo final treinado (pickle/joblib).
33) [NOVA] Medição do tamanho em disco e memória dos modelos treinados.

🛡️ Grupo 5: Motor do Firewall e Integração (07 Issues)

34) Script de captura e inspeção de pacotes em tempo real.
35) Módulo de extração de características de fluxo "em voo" (In-flight features).
36) Integração do script Python com o subsistema de rede (iptables).
37) Implementação da lógica de decisão: Whitelist → Blacklist → Votação do Comitê.
38) Criação da lógica de execução do bloqueio (DROP).
39) Implementação de cache de IPs para otimização de performance.
40) Sistema de Logging detalhado de eventos e vereditos.

📝 Grupo 6: Gestão de Listas e Moderação (06 Issues)

41) Modelagem do banco de dados local para Listas (SQLite ou JSON).
42) Desenvolvimento de módulo CRUD para gestão da Whitelist.
43) Desenvolvimento de módulo CRUD para gestão da Blacklist Manual.
44) Implementação de interface CLI para moderação administrativa.
45) Criação de mecanismo de "Hot Reload" das listas.
46) Lógica de "Feedback Loop": Adicionar falsos positivos à Whitelist via log.

🧪 Grupo 7: Testes, Validação e Eficiência (08 Issues)

47) Teste de latência: Medição do impacto da votação no tempo de resposta.
48) Teste de Falsos Positivos em sites críticos.
49) Teste de estresse: Simulação de carga pesada com listas extensas.
50) Validação da eficácia do bloqueio manual vs. bloqueio da IA.
51) Teste de persistência: Verificação após reinício do container.
52) Benchmark de CPU: Monitoramento do uso de processamento durante a inferência.
53) Benchmark de RAM: Monitoramento do footprint de memória do motor de IA.
54) Geração de matrizes de confusão e gráficos comparativos finais.

📂 Grupo 8: Documentação e Finalização (04 Issues)

55) Refatoração do código e padronização técnica (PEP8).
56) Elaboração do README.md com manual e arquitetura.
57) Criação de scripts de configuração automática do laboratório.
58) Consolidação final dos resultados (Relatório de Eficiência vs. Acurácia).
