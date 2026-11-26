# -*- coding: utf-8 -*-
"""
Script gerador da especificação completa e unificada de todas as Issues do projeto (Issues #01 a #58 + #41.1).
Lê as issues já desenvolvidas em 'issues desenvolidas.md', realiza a sanitização e padronização rigorosa
de acordo com os 15 Princípios Fundamentais e concatena com as novas issues especificadas nos módulos:
- scripts/issue_specs_g2_g3_g4.py
- scripts/issue_specs_g5_g6_g7_g8.py
Gera o artefato final: especificacao_completa_das_issues.md
"""

import os
import re
import sys
from issue_specs_g2_g3_g4 import ISSUES_G2_G3_G4
from issue_specs_g5_g6_g7_g8 import ISSUES_G5_G6_G7_G8

def clean_developed_issue(raw_text: str, issue_num_str: str) -> str:
    """
    Sanitiza uma issue extraída de 'issues desenvolidas.md':
    - Remove resíduos de exportação ([cite: ...], Google Docs, Issues do TCC, + 1, + 2)
    - Remove caudas de conversa/chatter entre as iterações
    - Padroniza o título com markdown '### **Issue #XX: [Prefixo] Título**'
    - Padroniza a formatação de seções
    """
    txt = raw_text

    # Remove citações de exportação
    txt = re.sub(r'\[cite:\s*[\d,\s]+\]', '', txt)
    txt = re.sub(r'^\s*Google Docs\s*$', '', txt, flags=re.MULTILINE)
    txt = re.sub(r'^\s*Issues do TCC\s*$', '', txt, flags=re.MULTILINE)
    txt = re.sub(r'^\s*TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1\s*$', '', txt, flags=re.MULTILINE)
    txt = re.sub(r'^\s*relatório de requisito do sistema do TCC\s*$', '', txt, flags=re.MULTILINE)
    txt = re.sub(r'^\s*\+\s*\d+\s*$', '', txt, flags=re.MULTILINE)

    # Remove caudas de diálogo de chat
    chatter_pattern = r'\n(?=(?:Podemos\s+(?:prosseguir|avançar|seguir)|Pronto\s+para|Finalizamos|Deseja\s+seguir|ta\s+agora|beleza|sim\s+cria|quando\s+for|acredito\s+que|Faz\s+total|O\s+treino\s+prático))'
    parts = re.split(chatter_pattern, txt, flags=re.IGNORECASE)
    cleaned = parts[0].strip()

    # Corrige título inicial para o padrão: ### **Issue #XX: [Prefixo] Título**
    lines = cleaned.splitlines()
    first_line = lines[0].strip()

    # Extrai prefixo e título
    m = re.search(r'Issue\s+#(\d+(?:\.\d+)?):?\s*(\[[^\]]+\])?\s*(.*)', first_line)
    if m:
        num = m.group(1)
        prefix = m.group(2) if m.group(2) else ""
        title = m.group(3).strip()

        # Ajuste específico de prefixo se ausente (ex: Issue #01)
        if not prefix:
            if num == "01":
                prefix = "[Infraestrutura]"
            elif num in ["08", "09"]:
                prefix = "[Ambiente]"
            else:
                prefix = "[Backend]"

        standard_header = f"### **Issue #{num}: {prefix} {title}**"
        lines[0] = standard_header

    # Reconstitui o texto
    rebuilt = "\n".join(lines).strip()

    # Padroniza numeração em negrito nas seções: "1. História de Usuário" -> "**1. História de Usuário (User Story)**"
    def fix_section_heading(match):
        sec_num = match.group(1)
        sec_name = match.group(2).strip()
        return f"\n**{sec_num}. {sec_name}**"

    rebuilt = re.sub(r'\n(?:###\s*)?(?:\*\*)?(\d+)\.\s+([^\n\r]+?)(?:\*\*)?\n', fix_section_heading, rebuilt)

    # Padroniza user story com blockquote se não estiver
    # Exemplo: "Como ...\neu quero ...\npara que ..."
    def format_user_story(match):
        body = match.group(1).strip()
        formatted_lines = []
        for l in body.splitlines():
            l_str = l.strip()
            if l_str:
                formatted_lines.append(f"> {l_str}")
        return f"**1. História de Usuário (User Story)**\n" + "\n".join(formatted_lines) + "\n"

    rebuilt = re.sub(
        r'\*\*1\.\s+História de Usuário[^\*]*\*\*\s*\n((?:(?!^\s*\*\*2\.).*\n)+)',
        format_user_story,
        rebuilt,
        flags=re.MULTILINE
    )

    # Limpa linhas vazias excessivas
    rebuilt = re.sub(r'\n{3,}', '\n\n', rebuilt)

    return rebuilt.strip()

def extract_all_developed_issues(raw_file_path: str):
    """
    Extrai as issues já criadas de 'issues desenvolidas.md'.
    """
    with open(raw_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    chunks = re.split(r'\n(?=Issue #\d+|###\s*\*\*Issue #\d+)', content)
    developed_issues = {}

    for c in chunks[1:]:
        m = re.search(r'Issue\s+#(\d+(?:\.\d+)?)', c)
        if m:
            key = m.group(1)
            cleaned = clean_developed_issue(c, key)
            developed_issues[key] = cleaned

    return developed_issues

def build_table_of_contents():
    """
    Gera o Sumário completo com links para as 58 issues (+ 41.1) divididas nos 8 grupos.
    """
    toc = [
        "## 📑 Índice Geral das Issues por Grupo",
        "",
        "### 🏗️ Grupo 1: Infraestrutura e Ambiente Docker",
        "- [Issue #01: [Infraestrutura] Configuração do repositório Git e estrutura de pastas](#issue-01-infraestrutura-configuração-do-repositório-git-e-estrutura-de-pastas)",
        "- [Issue #02: [Infraestrutura] Desenvolvimento do Dockerfile base (Python + Ferramentas de Rede)](#issue-02-infraestrutura-desenvolvimento-do-dockerfile-base-python--ferramentas-de-rede)",
        "- [Issue #03: [Infraestrutura] Configuração do docker-compose.yml (Containers Gateway e App)](#issue-03-infraestrutura-configuração-do-docker-composeyml-containers-gateway-e-app)",
        "- [Issue #04: [Infraestrutura] Implementação do container Gateway/Bridge para interceptação de tráfego](#issue-04-infraestrutura-implementação-do-container-gatewaybridge-para-interceptação-de-tráfego)",
        "- [Issue #05: [Infraestrutura] Configuração de capacidades de rede do kernel no Docker (Net_Admin)](#issue-05-infraestrutura-configuração-de-capacidades-de-rede-do-kernel-no-docker-net_admin)",
        "- [Issue #06: [Infraestrutura] Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy)](#issue-06-infraestrutura-instalação-e-teste-de-ferramentas-de-rede-tcpdump-tshark-scapy)",
        "- [Issue #07: [Infraestrutura] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado](#issue-07-infraestrutura-configuração-de-limites-de-recursos-cpuram-via-docker-para-simular-hardware-limitado)",
        "",
        "### 📡 Grupo 2: Coleta e Geração de Dados",
        "- [Issue #08: [Ambiente] Configurar Selenium/Playwright no Docker para Automação de Coleta](#issue-08-ambiente-configurar-seleniumplaywright-no-docker-para-automação-de-coleta)",
        "- [Issue #09: [Backend] Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot](#issue-09-backend-evasão-de-bloqueio-implementar-rotação-de-user-agents-e-técnicas-anti-bot)",
        "- [Issue #10: [Backend] Lógica de Navegação: Criar script que simula comportamento humano](#issue-10-backend-lógica-de-navegação-criar-script-que-simula-comportamento-humano)",
        "- [Issue #11: [Infraestrutura] Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído](#issue-11-infraestrutura-filtro-de-captura-bpf-configurar-filtros-no-tcpdump-para-excluir-ruído)",
        "- [Issue #12: [Backend] Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser)](#issue-12-backend-orquestrador-de-sessão-script-de-sincronia-sniffing--browser)",
        "- [Issue #13: [Backend] Dataset de Apostas: Execução da recolha em massa (Bet365, Betano, etc.)](#issue-13-backend-dataset-de-apostas-execução-da-recolha-em-massa-bet365-betano-etc)",
        "- [Issue #14: [Backend] Dataset Benigno: Execução da recolha de sítios de controlo (YouTube, Notícias)](#issue-14-backend-dataset-benigno-execução-da-recolha-de-sítios-de-controlo-youtube-notícias)",
        "- [Issue #15: [Backend] Validação de Captura: Script para verificar integridade dos PCAPs](#issue-15-backend-validação-de-captura-script-para-verificar-integridade-dos-pcaps)",
        "- [Issue #16: [Backend] Extração de Metadados Brutos: Relatório de volume e duração por captura](#issue-16-backend-extração-de-metadados-brutos-relatório-de-volume-e-duração-por-captura)",
        "",
        "### 🧹 Grupo 3: Pré-processamento e Dataset",
        "- [Issue #17: [Backend] Extração de fluxos bi-direcionais (Conversão PCAP para CSV)](#issue-17-backend-extração-de-fluxos-bi-direcionais-conversão-pcap-para-csv)",
        "- [Issue #18: [Backend] Limpeza de dados (Remoção de valores NaN, Inf e duplicatas)](#issue-18-backend-limpeza-de-dados-remoção-de-valores-nan-inf-e-duplicatas)",
        "- [Issue #19: [Backend] Rotulagem das classes (Apostas vs Benigno) e Label Encoding](#issue-19-backend-rotulagem-das-classes-apostas-vs-benigno-e-label-encoding)",
        "- [Issue #20: [Backend] Normalização e padronização de escalas dos dados](#issue-20-backend-normalização-e-padronização-de-escalas-dos-dados)",
        "- [Issue #21: [Backend] Análise estatística exploratória inicial (EDA) do dataset](#issue-21-backend-análise-estatística-exploratória-inicial-eda-do-dataset)",
        "- [Issue #22: [Backend] Balanceamento de classes via técnicas de amostragem (SMOTE)](#issue-22-backend-balanceamento-de-classes-via-técnicas-de-amostragem-smote)",
        "- [Issue #23: [Backend] Divisão do dataset em Treino, Validação e Teste](#issue-23-backend-divisão-do-dataset-em-treino-validação-e-teste)",
        "- [Issue #24: [Backend] Redução de dimensionalidade: Seleção de atributos mínimos via Incerteza Simétrica (SU)](#issue-24-backend-redução-de-dimensionalidade-seleção-de-atributos-mínimos-via-incerteza-simétrica-su)",
        "",
        "### 🧠 Grupo 4: Pipeline de Machine Learning",
        "- [Issue #25: [Backend] Implementação da Regressão Logística (Voto de Minerva/Baseline)](#issue-25-backend-implementação-da-regressão-logística-voto-de-minervabaseline)",
        "- [Issue #26: [Backend] Implementação e treinamento do classificador Random Forest](#issue-26-backend-implementação-e-treinamento-do-classificador-random-forest)",
        "- [Issue #27: [Backend] Implementação e treinamento do classificador XGBoost](#issue-27-backend-implementação-e-treinamento-do-classificador-xgboost)",
        "- [Issue #28: [Backend] Implementação do Comitê de Votação Majoritária (Ensemble)](#issue-28-backend-implementação-do-comitê-de-votação-majoritária-ensemble)",
        "- [Issue #29: [Backend] Tuning de hiperparâmetros (Foco em modelos \"leves\")](#issue-29-backend-tuning-de-hiperparâmetros-foco-em-modelos-leves)",
        "- [Issue #30: [Backend] Avaliação via validação cruzada ($K$-Fold Cross Validation)](#issue-30-backend-avaliação-via-validação-cruzada-k-fold-cross-validation)",
        "- [Issue #31: [Backend] Geração de métricas (Acurácia, F1-Score, Precisão, Recall)](#issue-31-backend-geração-de-métricas-acurácia-f1-score-precisão-recall)",
        "- [Issue #32: [Backend] Exportação do modelo final treinado (pickle/joblib)](#issue-32-backend-exportação-do-modelo-final-treinado-picklejoblib)",
        "- [Issue #33: [Backend] Medição do tamanho em disco e memória dos modelos treinados](#issue-33-backend-medição-do-tamanho-em-disco-e-memória-dos-modelos-treinados)",
        "",
        "### 🛡️ Grupo 5: Motor do Firewall e Integração",
        "- [Issue #34: [Infraestrutura/Backend] Script de captura e inspeção de pacotes em tempo real](#issue-34-infraestruturabackend-script-de-captura-e-inspeção-de-pacotes-em-tempo-real)",
        "- [Issue #35: [Backend] Módulo de extração de características de fluxo \"em voo\" (In-flight features)](#issue-35-backend-módulo-de-extração-de-características-de-fluxo-em-voo-in-flight-features)",
        "- [Issue #36: [Infraestrutura] Integração do script Python com o subsistema de rede (iptables)](#issue-36-infraestrutura-integração-do-script-python-com-o-subsistema-de-rede-iptables)",
        "- [Issue #37: [Backend] Implementação da lógica de decisão: Whitelist → Blacklist → Votação do Comitê](#issue-37-backend-implementação-da-lógica-de-decisão-whitelist--blacklist--votação-do-comitê)",
        "- [Issue #38: [Infraestrutura/Backend] Criação da lógica de execução do bloqueio (DROP)](#issue-38-infraestruturabackend-criação-da-lógica-de-execução-do-bloqueio-drop)",
        "- [Issue #39: [Backend] Implementação de cache de IPs para otimização de performance](#issue-39-backend-implementação-de-cache-de-ips-para-otimização-de-performance)",
        "- [Issue #40: [Backend] Sistema de Logging detalhado de eventos e vereditos](#issue-40-backend-sistema-de-logging-detalhado-de-eventos-e-vereditos)",
        "",
        "### 📝 Grupo 6: Gestão de Listas e Moderação",
        "- [Issue #41: [Backend] Modelagem do banco de dados local para Listas (SQLite ou JSON)](#issue-41-backend-modelagem-do-banco-de-dados-local-para-listas-sqlite-ou-json)",
        "- [Issue #41.1: [Backend] Modelagem, Scripts de Migração e Seed do Banco de Dados Local](#issue-411-backend-modelagem-scripts-de-migração-e-seed-do-banco-de-dados-local)",
        "- [Issue #42: [Backend] Desenvolvimento de módulo CRUD para gestão da Whitelist](#issue-42-backend-desenvolvimento-de-módulo-crud-para-gestão-da-whitelist)",
        "- [Issue #43: [Backend] Desenvolvimento de módulo CRUD para gestão da Blacklist Manual](#issue-43-backend-desenvolvimento-de-módulo-crud-para-gestão-da-blacklist-manual)",
        "- [Issue #44: [Backend/Frontend] Implementação de interface CLI para moderação administrativa](#issue-44-backendfrontend-implementação-de-interface-cli-para-moderação-administrativa)",
        "- [Issue #45: [Backend] Criação de mecanismo de \"Hot Reload\" das listas](#issue-45-backend-criação-de-mecanismo-de-hot-reload-das-listas)",
        "- [Issue #46: [Backend] Lógica de \"Feedback Loop\": Adicionar falsos positivos à Whitelist via log](#issue-46-backend-lógica-de-feedback-loop-adicionar-falsos-positivos-à-whitelist-via-log)",
        "",
        "### 🧪 Grupo 7: Testes, Validação e Eficiência",
        "- [Issue #47: [Backend/Infraestrutura] Teste de latência: Medição do impacto da votação no tempo de resposta](#issue-47-backendinfraestrutura-teste-de-latência-medição-do-impacto-da-votação-no-tempo-de-resposta)",
        "- [Issue #48: [Backend] Teste de Falsos Positivos em sites críticos](#issue-48-backend-teste-de-falsos-positivos-em-sites-críticos)",
        "- [Issue #49: [Infraestrutura] Teste de estresse: Simulação de carga pesada e vazão](#issue-49-infraestrutura-teste-de-estresse-simulação-de-carga-pesada-e-vazão)",
        "- [Issue #50: [Backend] Validação da eficácia comparativa do bloqueio manual vs. bloqueio preditivo da IA](#issue-50-backend-validação-da-eficácia-comparativa-do-bloqueio-manual-vs-bloqueio-preditivo-da-ia)",
        "- [Issue #51: [Infraestrutura] Teste de persistência: Verificação após reinício do container](#issue-51-infraestrutura-teste-de-persistência-verificação-após-reinício-do-container)",
        "- [Issue #52: [Infraestrutura] Benchmark de CPU: Monitoramento do uso de processamento durante a inferência](#issue-52-infraestrutura-benchmark-de-cpu-monitoramento-do-uso-de-processamento-durante-a-inferência)",
        "- [Issue #53: [Infraestrutura] Benchmark de RAM: Monitoramento do footprint de memória do motor de IA](#issue-53-infraestrutura-benchmark-de-ram-monitoramento-do-footprint-de-memória-do-motor-de-ia)",
        "- [Issue #54: [Backend] Geração de matrizes de confusão e gráficos comparativos finais](#issue-54-backend-geração-de-matrizes-de-confusão-e-gráficos-comparativos-finais)",
        "",
        "### 📂 Grupo 8: Documentação e Finalização",
        "- [Issue #55: [Infraestrutura/Backend] Refatoração do código e padronização técnica (PEP8)](#issue-55-infraestruturabackend-refatoração-do-código-e-padronização-técnica-pep8)",
        "- [Issue #56: [Documentação] Elaboração do README.md com manual e arquitetura](#issue-56-documentação-elaboração-do-readmemd-com-manual-e-arquitetura)",
        "- [Issue #57: [Infraestrutura] Criação de scripts de configuração automática do laboratório](#issue-57-infraestrutura-criação-de-scripts-de-configuração-automática-do-laboratório)",
        "- [Issue #58: [Documentação] Consolidação final dos resultados (Relatório de Eficiência vs. Acurácia)](#issue-58-documentação-consolidação-final-dos-resultados-relatório-de-eficiência-vs-acurácia)",
        "",
        "---"
    ]
    return "\n".join(toc)

def generate_document():
    workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    developed_path = os.path.join(workspace_root, "issues desenvolidas.md")
    output_path = os.path.join(workspace_root, "especificacao_completa_das_issues.md")

    print(f"Carregando issues desenvolvidas de: {developed_path}")
    developed = extract_all_developed_issues(developed_path)
    print(f"Total de issues extraídas de issues desenvolidas.md: {len(developed)}")
    print(f"Chaves encontradas: {list(developed.keys())}")

    doc = []

    # Cabeçalho do Documento
    doc.append("# 📋 Especificação Completa e Detalhada das Issues do Projeto")
    doc.append("**Projeto:** Firewall Inteligente para Bloqueio de Casas de Apostas em Ambientes de Baixos Recursos  ")
    doc.append("**Documento de Referência:** TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1  ")
    doc.append("**Versão:** 2.0 (Consolidada com Todas as 58 Issues + Issue #41.1)  ")
    doc.append("**Status:** Engenharia de Requisitos e Roteiro de Implementação  \n")

    # Os 15 Princípios Fundamentais
    doc.append("## 🏛️ Os 15 Princípios Fundamentais para Criação e Estruturação de Issues")
    doc.append("""Criar uma issue bem estruturada é a garantia de entrega sem ambiguidades e com reprodutibilidade técnica absoluta. Cada issue deste projeto segue rigorosamente o padrão das 15 características fundamentais:

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
""")
    doc.append("---\n")

    # Mapeamento de Requisitos e Cenários do TCC
    doc.append("## 🎯 Matriz de Requisitos do Sistema e Cenários de Hardware")
    doc.append("""### Requisitos Funcionais (RF)
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
""")
    doc.append("---\n")

    # Índice Geral de Navegação
    doc.append(build_table_of_contents())
    doc.append("\n")

    # GRUPO 1: Infraestrutura e Ambiente Docker (Issues #01 a #07)
    doc.append("# 🏗️ Grupo 1: Infraestrutura e Ambiente Docker\n")
    for i in range(1, 8):
        key = f"{i:02d}"
        if key in developed:
            doc.append(developed[key])
            doc.append("\n---\n")
        else:
            print(f"AVISO: Issue #{key} não encontrada em desenvolvidas!")

    # GRUPO 2: Coleta e Geração de Dados (Issues #08 a #16)
    doc.append("# 📡 Grupo 2: Coleta e Geração de Dados\n")
    for i in range(8, 16):
        key = f"{i:02d}"
        if key in developed:
            doc.append(developed[key])
            doc.append("\n---\n")
        else:
            print(f"AVISO: Issue #{key} não encontrada em desenvolvidas!")
    # Issue #16
    doc.append(ISSUES_G2_G3_G4[16])
    doc.append("\n---\n")

    # GRUPO 3: Pré-processamento e Dataset (Issues #17 a #24)
    doc.append("# 🧹 Grupo 3: Pré-processamento e Dataset\n")
    for i in range(17, 25):
        doc.append(ISSUES_G2_G3_G4[i])
        doc.append("\n---\n")

    # GRUPO 4: Pipeline de Machine Learning (Issues #25 a #33)
    doc.append("# 🧠 Grupo 4: Pipeline de Machine Learning\n")
    for i in range(25, 34):
        doc.append(ISSUES_G2_G3_G4[i])
        doc.append("\n---\n")

    # GRUPO 5: Motor do Firewall e Integração (Issues #34 a #40)
    doc.append("# 🛡️ Grupo 5: Motor do Firewall e Integração\n")
    for i in range(34, 41):
        doc.append(ISSUES_G5_G6_G7_G8[i])
        doc.append("\n---\n")

    # GRUPO 6: Gestão de Listas e Moderação (Issues #41, #41.1, #42 a #46)
    doc.append("# 📝 Grupo 6: Gestão de Listas e Moderação\n")
    # Issue #41
    doc.append(ISSUES_G5_G6_G7_G8[41])
    doc.append("\n---\n")
    # Issue #41.1 (Desenvolvida antecipadamente na discussão)
    if "41.1" in developed:
        doc.append(developed["41.1"])
        doc.append("\n---\n")
    # Issues #42 a #46
    for i in range(42, 47):
        doc.append(ISSUES_G5_G6_G7_G8[i])
        doc.append("\n---\n")

    # GRUPO 7: Testes, Validação e Eficiência (Issues #47 a #54)
    doc.append("# 🧪 Grupo 7: Testes, Validação e Eficiência\n")
    for i in range(47, 55):
        doc.append(ISSUES_G5_G6_G7_G8[i])
        doc.append("\n---\n")

    # GRUPO 8: Documentação e Finalização (Issues #55 a #58)
    doc.append("# 📂 Grupo 8: Documentação e Finalização\n")
    for i in range(55, 59):
        doc.append(ISSUES_G5_G6_G7_G8[i])
        doc.append("\n---\n")

    final_content = "\n".join(doc)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print(f"Sucesso! Arquivo gerado em: {output_path}")
    print(f"Tamanho total: {len(final_content.encode('utf-8'))} bytes")
    print(f"Total de linhas: {len(final_content.splitlines())}")

if __name__ == "__main__":
    generate_document()
