# -*- coding: utf-8 -*-
"""
Especificações detalhadas das novas Issues dos Grupos 5, 6, 7 e 8.
Baseado em:
- TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
- relatório de requisito do sistema do TCC.md
- Issues do TCC.md
"""

ISSUES_G5_G6_G7_G8 = {}

# ==============================================================================
# GRUPO 5: MOTOR DO FIREWALL E INTEGRAÇÃO (Issues #34 a #40)
# ==============================================================================

ISSUES_G5_G6_G7_G8[34] = """### **Issue #34: [Infraestrutura/Backend] Script de captura e inspeção de pacotes em tempo real**

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
python -m src.engine.live_sniffer \\
    --interface eth0 \\
    --bpf-filter "tcp or udp" \\
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
"""

ISSUES_G5_G6_G7_G8[35] = """### **Issue #35: [Backend] Módulo de extração de características de fluxo "em voo" (In-flight features)**

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
python -m src.engine.inflight_extractor \\
    --min-packets 10 \\
    --flow-timeout 30.0 \\
    --scaler-path models/production/scaler.joblib \\
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
"""

ISSUES_G5_G6_G7_G8[36] = """### **Issue #36: [Infraestrutura] Integração do script Python com o subsistema de rede (iptables)**

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
python -m src.engine.netfilter_adapter \\
    --action block \\
    --ip 198.51.100.25 \\
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
"""

ISSUES_G5_G6_G7_G8[37] = """### **Issue #37: [Backend] Implementação da lógica de decisão: Whitelist → Blacklist → Votação do Comitê**

**1. História de Usuário (User Story)**
> **Como** arquiteto do motor de firewall,
> **eu quero** implementar a esteira hierárquica e assíncrona de decisão em três camadas (1º Consulta à Whitelist em memória, 2º Consulta à Blacklist manual e 3º Inferência pelo Comitê de Votação),
> **para que** tráfego previamente conhecido seja liberado ou bloqueado instantaneamente em $< 1ms$ sem gastar ciclos de CPU da IA, acionando o comitê apenas para fluxos não catalogados (RF07, RF09 e Seção 3.1.2 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que um fluxo em voo é analisado**, **quando** o IP ou domínio de destino constar na Whitelist em memória, **então** o sistema deve emitir imediatamente o veredito `PASS` (liberado) sem acionar o pipeline de IA.
* **Dado que o destino consta na Blacklist Manual**, **quando** for detectado, **então** o sistema deve emitir imediatamente o veredito `DROP` (bloqueio estático) sem consumir inferência da IA.
* **Dado que o fluxo não consta em nenhuma lista**, **quando** o vetor de características estiver disponível pelo extrator in-flight, **então** deve ser submetido ao Comitê de Hard Voting, aplicando a regra $\\sum Votos \\ge 2 \\implies DROP$.
* **Dado que a auditoria deve registrar o caminho da decisão**, **quando** o veredito for emitido, **então** o log deve especificar a origem da decisão (`WHITELIST_BYPASS`, `BLACKLIST_STATIC` ou `ENSEMBLE_PREDICTION`) e o tempo total de decisão em milissegundos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.engine.decision_engine \\
    --ip 104.18.25.10 \\
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
"""

ISSUES_G5_G6_G7_G8[38] = """### **Issue #38: [Infraestrutura/Backend] Criação da lógica de execução do bloqueio (DROP)**

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
python -m src.engine.block_executor \\
    --ip 203.0.113.88 \\
    --port 443 \\
    --send-rst \\
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
"""

ISSUES_G5_G6_G7_G8[39] = """### **Issue #39: [Backend] Implementação de cache de IPs para otimização de performance**

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
python -m src.engine.cache_manager \\
    --action get \\
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
"""

ISSUES_G5_G6_G7_G8[40] = """### **Issue #40: [Backend] Sistema de Logging detalhado de eventos e vereditos**

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
python -m src.engine.logger_service \\
    --tail 5 \\
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
"""

# ==============================================================================
# GRUPO 6: GESTÃO DE LISTAS E MODERAÇÃO (Issues #41 a #46)
# ==============================================================================

ISSUES_G5_G6_G7_G8[41] = """### **Issue #41: [Backend] Modelagem do banco de dados local para Listas (SQLite ou JSON)**

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
python -m src.database.init_db \\
    --db-path /volumes/db/firewall.db \\
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
"""

ISSUES_G5_G6_G7_G8[42] = """### **Issue #42: [Backend] Desenvolvimento de módulo CRUD para gestão da Whitelist**

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
python -m src.database.crud_whitelist \\
    --action add \\
    --target "caixa.gov.br" \\
    --reason "Portal bancário essencial" \\
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
"""

ISSUES_G5_G6_G7_G8[43] = """### **Issue #43: [Backend] Desenvolvimento de módulo CRUD para gestão da Blacklist Manual**

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
python -m src.database.crud_blacklist \\
    --action add \\
    --target "198.51.100.99" \\
    --reason "Operador ilegal de apostas" \\
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
"""

ISSUES_G5_G6_G7_G8[44] = """### **Issue #44: [Backend/Frontend] Implementação de interface CLI para moderação administrativa**

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
"""

ISSUES_G5_G6_G7_G8[45] = """### **Issue #45: [Backend] Criação de mecanismo de "Hot Reload" das listas**

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
"""

ISSUES_G5_G6_G7_G8[46] = """### **Issue #46: [Backend] Lógica de "Feedback Loop": Adicionar falsos positivos à Whitelist via log**

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
python -m src.cli.main unblock 192.0.2.77 \\
    --whitelist \\
    --reason "Falso Positivo confirmado: Portal bancário corporativo" \\
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
"""

# ==============================================================================
# GRUPO 7: TESTES, VALIDAÇÃO E EFICIÊNCIA (Issues #47 a #54)
# ==============================================================================

ISSUES_G5_G6_G7_G8[47] = """### **Issue #47: [Backend/Infraestrutura] Teste de latência: Medição do impacto da votação no tempo de resposta**

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
python -m tests.benchmark.test_latency \\
    --scenarios A B C \\
    --samples 100 \\
    --output-json data/reports/latency_benchmark.json \\
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
"""

ISSUES_G5_G6_G7_G8[48] = """### **Issue #48: [Backend] Teste de Falsos Positivos em sites críticos**

**1. História de Usuário (User Story)**
> **Como** auditor de qualidade do projeto,
> **eu quero** conduzir testes automatizados de navegação em uma lista de 50 domínios institucionais e críticos (portais bancários, governamentais, notícias e streaming),
> **para que** possamos verificar se a taxa de falsos positivos ($FPR$) em regime dinâmico se mantém estritamente abaixo do limite de 5.0% estabelecido como critério de rejeição da hipótese (RNF06 e Seção 3.4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado que o coletor automatizado acessa 50 portais benignos críticos** (ex.: Receita Federal, Caixa, YouTube, G1, BBC), **quando** o tráfego transitar pelo gateway, **então** o sistema deve registrar a decisão de cada fluxo em tempo real.
* **Dado que nenhum desses domínios contém apostas**, **quando** calculada a taxa de Falsos Positivos ($FPR = \\frac{FP}{Total}$), **então** o resultado não deve exceder 5.0% (Seção 3.4.5 do TCC).
* **Dado qualquer falso positivo detectado durante o teste**, **quando** acionado o procedimento de moderação, **então** deve validar a atuação do Feedback Loop (#46), certificando a restauração do acesso.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m tests.benchmark.test_critical_sites \\
    --sites-file config/critical_sites.txt \\
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
"""

ISSUES_G5_G6_G7_G8[49] = """### **Issue #49: [Infraestrutura] Teste de estresse: Simulação de carga pesada e vazão**

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
python -m tests.benchmark.test_stress \\
    --rates 25 50 100 150 200 \\
    --duration-per-rate 60 \\
    --output-json docs/evaluation/stress_report.json \\
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
"""

ISSUES_G5_G6_G7_G8[50] = """### **Issue #50: [Backend] Validação da eficácia comparativa do bloqueio manual vs. bloqueio preditivo da IA**

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
python -m tests.benchmark.test_comparative_efficacy \\
    --targets-file config/new_unlisted_betting.txt \\
    --output-json docs/evaluation/comparative_efficacy_report.json \\
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
"""

ISSUES_G5_G6_G7_G8[51] = """### **Issue #51: [Infraestrutura] Teste de persistência e recuperação após reinício de container**

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
"""

ISSUES_G5_G6_G7_G8[52] = """### **Issue #52: [Infraestrutura] Benchmark de CPU: Monitoramento do uso de processamento durante a inferência**

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
python -m tests.benchmark.monitor_cpu \\
    --duration 120 \\
    --interval 0.1 \\
    --output-json docs/evaluation/cpu_benchmark_report.json \\
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
"""

ISSUES_G5_G6_G7_G8[53] = """### **Issue #53: [Infraestrutura] Benchmark de RAM: Monitoramento do footprint de memória do motor de IA**

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
python -m tests.benchmark.monitor_ram \\
    --duration 180 \\
    --output-json docs/evaluation/ram_footprint_report.json \\
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
"""

ISSUES_G5_G6_G7_G8[54] = """### **Issue #54: [Backend] Geração de matrizes de confusão e gráficos comparativos finais**

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
python -m src.visualization.generate_final_figures \\
    --reports-dir data/reports/ \\
    --evaluation-dir docs/evaluation/ \\
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
"""

# ==============================================================================
# GRUPO 8: DOCUMENTAÇÃO E FINALIZAÇÃO (Issues #55 a #58)
# ==============================================================================

ISSUES_G5_G6_G7_G8[55] = """### **Issue #55: [Infraestrutura/Backend] Refatoração do código e padronização técnica (PEP8)**

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
"""

ISSUES_G5_G6_G7_G8[56] = """### **Issue #56: [Documentação] Elaboração do README.md com manual e arquitetura**

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
"""

ISSUES_G5_G6_G7_G8[57] = """### **Issue #57: [Infraestrutura] Criação de scripts de configuração automática do laboratório**

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
"""

ISSUES_G5_G6_G7_G8[58] = """### **Issue #58: [Documentação] Consolidação final dos resultados (Relatório de Eficiência vs. Acurácia)**

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
  1. A latência média $T_{verdict}$ foi inferior a 1 segundo (atingiu $\\approx 48.6ms$ no Cenário B);
  2. A memória RAM manteve-se estável sem acionamento do OOM Killer ($< 150MB$ de pico);
  3. A taxa de Falsos Positivos em sites reais manteve-se estritamente abaixo de 5.0% ($2.0\\%$ nos testes).
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
"""
