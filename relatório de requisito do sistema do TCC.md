1. Requisitos Funcionais (RF)
Grupo A: Aquisição e Processamento de Dados
RF01 - Automação de Coleta: O sistema deve possuir um módulo de automação (Selenium/Playwright) para navegar em domínios de apostas e controle, gerando tráfego sintético para o dataset.
RF02 - Sniffing Passivo: O sistema deve realizar a captura de pacotes brutos (formato PCAP) sem interferir na integridade do payload original durante a fase de treino.
RF03 - Extração de Atributos (Feature Extraction): O sistema deve converter PCAPs em fluxos bidirecionais, extraindo no mínimo 20 metadados estatísticos (ex: IAT, Packet Length, Flow Duration).
RF04 - Redução de Dimensionalidade: O sistema deve aplicar o algoritmo de Incerteza Simétrica (SU) para selecionar automaticamente o subconjunto de atributos com maior ganho de informação.
Grupo B: Inteligência e Votação
RF05 - Treinamento de Modelos: O sistema deve permitir o treinamento isolado de Random Forest, XGBoost e Regressão Logística.
RF06 - Persistência de Modelos: O sistema deve exportar os modelos treinados em formatos serializados (.pkl ou .joblib) para carregamento rápido no motor de inferência.
RF07 - Lógica de Votação (Hard Voting): O motor de decisão deve implementar um algoritmo de consenso onde o veredito positivo requer a concordância de $\geq 2$ classificadores.
Grupo C: Operação e Governança
RF08 - Integração com Kernel (Netfilter): O sistema deve interagir com o subsistema iptables/nftables para inserir e remover regras de bloqueio dinamicamente.
RF09 - Gestão de Whitelist/Blacklist: O sistema deve prover operações de CRUD (Criar, Ler, Atualizar, Deletar) para endereços IP e domínios em listas de exceção.
RF10 - Interface Administrativa (CLI): O sistema deve disponibilizar comandos via terminal para consulta de status, limpeza de cache e atualização manual de listas.
RF11 - Feedback Loop: O sistema deve permitir que um administrador marque um bloqueio como "Falso Positivo", movendo o IP automaticamente para a Whitelist.

2. Requisitos Não Funcionais (RNF)
Grupo D: Performance e Eficiência
RNF01 - Latência Crítica (Real-time): O tempo total de processamento (Extração + Inferência + Bloqueio) não deve exceder 200ms por fluxo inicial.
RNF02 - Restrição de Memória RAM: O motor de execução (incluindo os modelos carregados) não deve consumir mais de 512MB de memória RAM em regime estável.
RNF03 - Carga de CPU: O uso de CPU durante a inferência não deve causar starvation (fome de recursos) em processos críticos do host, mantendo-se abaixo de 60% em hardware de 1 core.
RNF04 - Vazão de Classificação: O sistema deve ser capaz de classificar pelo menos 50 novos fluxos por segundo sem enfileiramento excessivo.
Grupo E: Confiabilidade e Arquitetura
RNF05 - Isolamento via Docker: Todos os módulos (Coleta, IA, Gateway) devem ser executados em containers isolados, comunicando-se apenas via redes virtuais internas.
RNF06 - Disponibilidade: O sistema deve prever um mecanismo de "Failsafe": caso o motor de IA falhe ou trave, o tráfego deve continuar fluindo (ou ser bloqueado por padrão), conforme configuração administrativa.
RNF07 - Persistência de Dados: As listas de governança e os logs de auditoria devem ser armazenados em volumes persistentes, sobrevivendo ao reinício dos containers.
RNF08 - Interpretabilidade de Log: Cada entrada de log de bloqueio deve conter o carimbo de tempo, o IP de origem, o domínio suspeito e a distribuição exata dos votos (ex: [1, 1, 0]).
