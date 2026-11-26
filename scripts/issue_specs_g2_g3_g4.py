# -*- coding: utf-8 -*-
"""
Especificações detalhadas das novas Issues dos Grupos 2, 3 e 4.
Baseado em:
- TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
- relatório de requisito do sistema do TCC.md
- Issues do TCC.md
"""

ISSUES_G2_G3_G4 = {}

# ==============================================================================
# GRUPO 2: COLETA E GERAÇÃO DE DADOS (Issue #16)
# ==============================================================================

ISSUES_G2_G3_G4[16] = """### **Issue #16: [Backend] Extração de Metadados Brutos: Relatório de volume e duração por captura**

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
python -m src.collector.extract_raw_metadata \\
    --input-dir data/raw \\
    --output-json data/reports/raw_metadata_report.json \\
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
"""

# ==============================================================================
# GRUPO 3: PRÉ-PROCESSAMENTO E DATASET (Issues #17 a #24)
# ==============================================================================

ISSUES_G2_G3_G4[17] = """### **Issue #17: [Backend] Extração de fluxos bi-direcionais (Conversão PCAP para CSV)**

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
python -m src.data_processing.flow_extractor \\
    --input-dir data/raw/ \\
    --output-csv data/processed/flows_extracted.csv \\
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
"""

ISSUES_G2_G3_G4[18] = """### **Issue #18: [Backend] Limpeza de dados (Remoção de valores NaN, Inf e duplicatas)**

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
python -m src.data_processing.clean_dataset \\
    --input-csv data/processed/flows_extracted.csv \\
    --output-csv data/processed/flows_cleaned.csv \\
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
"""

ISSUES_G2_G3_G4[19] = """### **Issue #19: [Backend] Rotulagem das classes (Apostas vs Benigno) e Label Encoding**

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
python -m src.data_processing.label_dataset \\
    --input-csv data/processed/flows_cleaned.csv \\
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
"""

ISSUES_G2_G3_G4[20] = """### **Issue #20: [Backend] Normalização e padronização de escalas dos dados**

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
python -m src.data_processing.scale_features \\
    --input-csv data/processed/flows_labeled.csv \\
    --output-csv data/processed/flows_scaled.csv \\
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
"""

ISSUES_G2_G3_G4[21] = """### **Issue #21: [Backend] Análise estatística exploratória inicial (EDA) do dataset**

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
python -m src.data_processing.eda_analysis \\
    --input-csv data/processed/flows_labeled.csv \\
    --output-dir docs/eda/ \\
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
"""

ISSUES_G2_G3_G4[22] = """### **Issue #22: [Backend] Balanceamento de classes via técnicas de amostragem (SMOTE)**

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
python -m src.data_processing.balance_classes \\
    --input-train-csv data/processed/train.csv \\
    --output-train-csv data/processed/train_balanced.csv \\
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
"""

ISSUES_G2_G3_G4[23] = """### **Issue #23: [Backend] Divisão do dataset em Treino, Validação e Teste**

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
python -m src.data_processing.split_dataset \\
    --input-csv data/processed/flows_scaled.csv \\
    --output-dir data/processed/ \\
    --train-ratio 0.70 \\
    --val-ratio 0.15 \\
    --test-ratio 0.15 \\
    --open-world-split \\
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
"""

ISSUES_G2_G3_G4[24] = """### **Issue #24: [Backend] Redução de dimensionalidade: Seleção de atributos mínimos via Incerteza Simétrica (SU)**

**1. História de Usuário (User Story)**
> **Como** pesquisador de sistemas embarcados do projeto,
> **eu quero** implementar o algoritmo de Incerteza Simétrica (Symmetrical Uncertainty - SU) baseado na teoria da informação para ranquear e selecionar o subconjunto ótimo e mínimo de características (top 6 a 10 atributos),
> **para que** o custo de processamento de CPU e o tempo de inferência do firewall em hardware limitado (0.5 vCPU, 512MB RAM) sejam reduzidos drasticamente sem perda sensível do poder discriminatório (RF04, RNF01, RNF03 e Seção 3.2.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o conjunto de dados de treino**, **quando** o cálculo de SU for executado para cada atributo numérico $X$ contra a classe binária $Y$, **então** o algoritmo deve calcular a entropia de Shannon individual $H(X)$, a entropia da classe $H(Y)$, a entropia conjunta $H(X, Y)$ e a Informação Mútua $I(X; Y) = H(X) + H(Y) - H(X, Y)$, derivando:
  $$SU(X, Y) = 2 \cdot \\frac{H(X) + H(Y) - H(X, Y)}{H(X) + H(Y)}$$
  garantindo que o resultado de $SU(X, Y)$ esteja rigorosamente delimitado no intervalo $[0.0, 1.0]$ (Seção 3.2.3 do TCC e RF04).
* **Dado que** variáveis contínuas exigem discretização para cálculo de entropia de Shannon, **quando** computar as probabilidades, **então** o algoritmo deve aplicar discretização adaptativa por quantis (ex.: 10 a 20 bins) preservando a distribuição de probabilidades.
* **Dado o ranking decrescente de SU**, **quando** selecionado o corte de atributos mínimos (ex.: top $k=8$), **então** os nomes dos atributos selecionados e seus respectivos coeficientes devem ser serializados em `models/selected_features.json` para guiar os modelos de ML e o extrator em voo.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.data_processing.symmetrical_uncertainty \\
    --train-csv data/processed/train_balanced.csv \\
    --top-k 8 \\
    --output-json models/selected_features.json \\
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
3. Testar a consistência do algoritmo criando uma feature sintética perfeitamente correlacionada e verificar se ela atinge $SU \approx 1.0$.
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
"""

# ==============================================================================
# GRUPO 4: PIPELINE DE MACHINE LEARNING (Issues #25 a #33)
# ==============================================================================

ISSUES_G2_G3_G4[25] = """### **Issue #25: [Backend] Implementação da Regressão Logística (Voto de Minerva/Baseline)**

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
python -m src.brain.train_logistic_regression \\
    --train-csv data/processed/train_balanced.csv \\
    --val-csv data/processed/val.csv \\
    --features-json models/selected_features.json \\
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
"""

ISSUES_G2_G3_G4[26] = """### **Issue #26: [Backend] Implementação e treinamento do classificador Random Forest**

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
python -m src.brain.train_random_forest \\
    --train-csv data/processed/train_balanced.csv \\
    --val-csv data/processed/val.csv \\
    --features-json models/selected_features.json \\
    --n-estimators 50 \\
    --max-depth 12 \\
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
"""

ISSUES_G2_G3_G4[27] = """### **Issue #27: [Backend] Implementação e treinamento do classificador XGBoost**

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
python -m src.brain.train_xgboost \\
    --train-csv data/processed/train_balanced.csv \\
    --val-csv data/processed/val.csv \\
    --features-json models/selected_features.json \\
    --n-estimators 60 \\
    --max-depth 6 \\
    --learning-rate 0.1 \\
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
"""

ISSUES_G2_G3_G4[28] = """### **Issue #28: [Backend] Implementação do Comitê de Votação Majoritária (Ensemble)**

**1. História de Usuário (User Story)**
> **Como** arquiteto de software do projeto,
> **eu quero** implementar o motor do Comitê de Decisão baseado em Votação Majoritária Rígida (*Hard Voting*), que submete paralelamente o vetor de atributos aos três modelos (Random Forest, XGBoost e Regressão Logística) e dispara veredito de bloqueio se e somente se $\\sum Votos \\ge 2$,
> **para que** a divergência estatística entre os algoritmos de Bagging, Boosting e Linear reduza a taxa de falsos positivos operacionais no firewall (RF07 e Seção 3.3 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado um vetor numérico de características de fluxo**, **quando** for submetido ao motor do comitê, **então** deve acionar os três classificadores de forma isolada, gerando os votos individuais $v_{RF}, v_{XGB}, v_{LR} \\in \\{0, 1\\}$.
* **Dado que o bloqueio em redes exige alta confiabilidade**, **quando** for agregada a soma dos votos, **então** o veredito final deve ser `1` (Aposta / Bloquear via DROP) apenas se $\\sum_{i=1}^3 v_i \\ge 2$; caso contrário, o veredito deve ser `0` (Benigno / Permitir) (Seção 3.3.2 do TCC e RF07).
* **Dado que o motor deve registrar auditoria completa**, **quando** o veredito for emitido, **então** deve retornar a distribuição exata dos votos ex.: `[1, 1, 0]`, o rótulo final e o tempo total de inferência $T_{decision}$ em microssegundos (RNF08).
* **Dado a restrição de latência crítica** (RNF01), **quando** o comitê executar uma decisão completa em hardware limitado, **então** o tempo de inferência conjunto não deve ultrapassar 15 milissegundos.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.ensemble_engine \\
    --models-dir models/ \\
    --features-json models/selected_features.json \\
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
2. Verificar se o veredito retornado é estritamente `1` apenas para $\\sum \\ge 2$.
3. Medir a latência média de 500 chamadas em lote e verificar se média $\\le 15ms$.
4. Executar os testes automatizados via `pytest tests/test_ensemble_engine.py`.

**10. Definição de Pronto (Definition of Done - DoD)**
* Classe `EnsembleEngine` implementada com tratamento robusto para entradas inválidas.
* Lógica de Hard Voting $\\sum \\ge 2$ testada para todas as 8 combinações binárias possíveis de votos.
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
"""

ISSUES_G2_G3_G4[29] = """### **Issue #29: [Backend] Tuning de hiperparâmetros (Foco em modelos "leves")**

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
python -m src.brain.tune_hyperparameters \\
    --train-csv data/processed/train_balanced.csv \\
    --val-csv data/processed/val.csv \\
    --features-json models/selected_features.json \\
    --n-trials 50 \\
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
"""

ISSUES_G2_G3_G4[30] = """### **Issue #30: [Backend] Avaliação via validação cruzada ($K$-Fold Cross Validation)**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** executar validação cruzada estratificada em $k=5$ dobras (*5-Fold Stratified Cross-Validation*) sobre cada modelo individual e sobre o Comitê de Votação,
> **para que** possamos comprovar a estabilidade estatística do sistema e validar cientificamente se o Ensemble reduz a variância das predições com significância estatística (Seção 3.4.4 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o dataset de treino completo**, **quando** a validação cruzada for executada com $k=5$ dobras estratificadas, **então** a proporção entre classes deve ser rigorosamente idêntica em todas as dobras de treino e validação.
* **Dado cada dobra processada**, **quando** calculadas as métricas de Acurácia, Precisão, Recall e F1-Score para a Regressão Logística, Random Forest, XGBoost e o Comitê Ensemble, **então** devem ser calculadas a média e o desvio padrão ($\mu \pm \sigma$) de cada técnica.
* **Dado os resultados consolidados**, **quando** realizada a comparação estatística (teste t pareado ou teste de Wilcoxon com $\alpha=0.05$), **então** deve ser verificado se a superioridade do Comitê de Votação frente ao melhor modelo individual é estatisticamente significativa e gravada em `docs/evaluation/kfold_results.json`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.cross_validation \\
    --train-csv data/processed/train_balanced.csv \\
    --features-json models/selected_features.json \\
    --k-folds 5 \\
    --output-json docs/evaluation/kfold_results.json \\
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
"""

ISSUES_G2_G3_G4[31] = """### **Issue #31: [Backend] Geração de métricas (Acurácia, F1-Score, Precisão, Recall)**

**1. História de Usuário (User Story)**
> **Como** pesquisador do projeto,
> **eu quero** calcular e consolidar as métricas definitivas de desempenho (Matriz de Confusão, Taxa de Falsos Positivos - FPR, Curva ROC e AUC) na partição independente de teste de Mundo Aberto,
> **para que** possamos comprovar a eficácia do firewall e garantir que a taxa de falsos positivos em tráfego nunca visto seja estritamente inferior a 5% (RNF06 e Seção 3.4.5 do TCC).

**2. Critérios de Aceitação (AC)**
* **Dado o Comitê Ensemble final** e a partição de teste `test_open_world.csv`, **quando** executada a avaliação de mundo aberto, **então** as métricas de Acurácia, Precisão, Recall, F1-Score Macro e AUC-ROC devem ser extraídas e tabuladas.
* **Dado que o bloqueio indevido de sites legítimos é uma falha operacional crítica** (Seção 3.4.5 do TCC), **quando** for gerada a Matriz de Confusão, **então** a taxa de Falsos Positivos ($FPR = \\frac{FP}{FP + TN}$) não deve ultrapassar o teto estipulado de 5.0%.
* **Dado a geração dos dados**, **quando** concluída a rotina, **então** deve salvar o relatório numérico em `docs/evaluation/metrics_summary.json` e gerar os gráficos da Matriz de Confusão e da Curva ROC em `docs/evaluation/roc_curve.png`.

**3. Exemplo de Requisição (Código/CLI)**
```bash
python -m src.brain.evaluate_metrics \\
    --models-dir models/ \\
    --test-csv data/processed/test_open_world.csv \\
    --output-dir docs/evaluation/
```

**4. Exemplo de Resposta (Saída esperada / Log)**
```plaintext
[INFO] Carregando partição de teste de Mundo Aberto (1,008 instâncias inéditas)...
[INFERENCE] Submetendo ao Comitê de Votação (Ensemble)...
================ MATRIZ DE CONFUSÃO (MUNDO ABERTO) ================
Verdadeiro \\ Predito | Benigno (0)  | Apostas (1)
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
"""

ISSUES_G2_G3_G4[32] = """### **Issue #32: [Backend] Exportação do modelo final treinado (pickle/joblib)**

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
python -m src.brain.export_pipeline \\
    --source-dir models/ \\
    --output-dir models/production/ \\
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
"""

ISSUES_G2_G3_G4[33] = """### **Issue #33: [Backend] Medição do tamanho em disco e memória dos modelos treinados**

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
python -m src.brain.measure_footprint \\
    --models-dir models/production/ \\
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
"""
