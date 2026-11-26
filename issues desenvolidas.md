quais as 15 características fundamentais pra criação de issues coisas como histórias de usuarios, critérios de aceitação, Exemplo de Requisição, Exemplo de Resposta, Componentes Envolvidos, Considerações Técnicas, Como Testar, etc

Criar uma issue bem estruturada é a diferença entre uma entrega fluida e um ciclo infinito de "o que você quis dizer com isso?". Para que qualquer desenvolvedor — ou você mesmo no futuro — consiga pegar a tarefa e executá-la sem dúvidas, aqui estão as 15 características fundamentais:

1. Título Claro e Conciso
O título deve ser o "resumo do resumo". Evite "Erro no sistema" ou "Ajustar API". Prefira padrões como: [Tipo/Componente]: Ação esperada.

Exemplo: [Auth] Implementar renovação de token JWT via Refresh Token.

2. História de Usuário (User Story)
Define o valor de negócio e o propósito da tarefa. Segue o clássico template:

Como [persona], eu quero [funcionalidade], para que [valor/benefício].

3. Critérios de Aceitação (AC)
São as condições que a entrega deve cumprir para ser considerada funcional. Frequentemente escritos no formato Gherkin:

Dado que [contexto]

Quando [ação executada]

Então [resultado esperado]

4. Exemplo de Requisição (Payload)
Crucial para tarefas de Backend ou Integração. Forneça o JSON ou os parâmetros necessários.

Exemplo: POST /v1/logs { "service": "firewall", "severity": "high" }.

5. Exemplo de Resposta (Response)
O que o sistema deve retornar em cenários de sucesso (200, 201) e erro (400, 404, 500). Isso evita suposições sobre a estrutura dos dados no Frontend.

6. Componentes Envolvidos
Liste quais partes do ecossistema serão afetadas: Banco de Dados, Microserviço X, Interface Y, ou alguma infraestrutura de Cloud/DevOps específica.

7. Considerações Técnicas e Arquitetura
Aqui entra o "como" técnico. Menção a padrões de projeto, bibliotecas específicas a serem usadas, possíveis refatorações necessárias ou impactos em performance e segurança (ex: uso de criptografia).

8. Mockups ou Referências Visuais
Para tarefas de UI/UX, o link do Figma ou prints de tela são obrigatórios. Se for um ajuste de layout, um "antes vs. depois" ajuda muito na validação.

9. Dependências e Bloqueios
Identifique se esta issue depende da finalização de outra tarefa ou se ela bloqueia o trabalho de outra pessoa. Ajuda na gestão do fluxo (Kanban/Scrum).

10. Como Testar (Plano de Teste)
Um guia passo a passo para o QA ou para o desenvolvedor que fará o Code Review:

Faça login com usuário 'X'.

Tente enviar o formulário vazio.

Verifique se o log de erro foi gerado no console.

11. Definição de Pronto (Definition of Done - DoD)
Diferente dos critérios de aceitação (que são da funcionalidade), o DoD é da qualidade técnica:

Testes unitários escritos e passando.

Documentação atualizada (Swagger/README).

Código revisado por pelo menos um par.

12. Prioridade e Severidade
Prioridade: O quão rápido o negócio precisa disso.

Severidade: O impacto técnico (ex: um bug que derruba o servidor é severidade crítica).

13. Etiquetas (Labels)
Categorização para facilitar filtros e métricas. Tags como bug, feature, refactor, documentation, ou devops.

14. Documentação Relacionada
Links para documentos de requisitos, threads de discussão no Slack/Discord ou referências externas da documentação de uma API que está sendo integrada.

15. Estimativa (Story Points ou T-Shirt Sizes)
A percepção de complexidade da tarefa. Ajuda a entender se a issue é um "átomo" (pequena) ou um "épico" disfarçado que precisa ser quebrado em partes menores.

Dica Extra: Se for um Bug Report, inclua obrigatoriamente a seção "Passos para Reproduzir" e o "Comportamento Esperado vs. Comportamento Atual". Nada frustra mais um dev do que um bug que não pode ser replicado.

Acha que alguma dessas etapas costuma ser o maior "gargalo" no dia a dia de desenvolvimento que você observa?

preciso criar as issues desse sistema ai com todas essas características nas issues eu vou te pedir as issues uma por uma e vc vai escrevendo elas pra mim

Perfeito, Victor. Vamos começar a transformar o seu planejamento em tarefas executáveis, seguindo o padrão de alta qualidade que discutimos.

Para a primeira issue, utilizaremos o Grupo 1: Infraestrutura e Ambiente Docker.   
Google Docs

Issue #01: Configuração do repositório Git e estrutura de pastas    
Google Docs

1. História de Usuário (User Story)

Como desenvolvedor do projeto,
eu quero estabelecer uma estrutura de diretórios organizada e um repositório Git configurado,
para que o código seja versionado corretamente e os módulos (IA, Coleta, Gateway) fiquem isolados conforme a arquitetura proposta.   
Google Docs
+ 3

2. Critérios de Aceitação (AC)

Dado que iniciei o repositório, quando eu criar as pastas, então elas devem seguir a divisão lógica: infra/, data_collection/, ml_pipeline/, firewall_engine/ e docs/.

Dado que o projeto utiliza Python, quando eu configurar o .gitignore, então arquivos temporários, ambientes virtuais (.venv) e arquivos de modelos serializados (.pkl, .joblib) grandes não devem ser rastreados.   
Google Docs
+ 1

Dado que o projeto exige persistência, quando eu configurar a estrutura, então deve existir um diretório específico para volumes do Docker (volumes/db, volumes/logs).   
Google Docs
+ 1

3. Exemplo de Estrutura (Representação de "Requisição")

Plaintext
/
├── infra/               # Dockerfiles e docker-compose [cite: 3, 4]
├── src/
│   ├── collector/       # Scripts de coleta Selenium/Playwright [cite: 10, 69]
│   ├── brain/           # Modelos e scripts de ML (RF, XGBoost, LR) [cite: 30, 31, 29]
│   └── engine/          # Motor do firewall e integração iptables [cite: 39, 41]
├── data/
│   ├── raw/             # Arquivos PCAP brutos [cite: 20, 70]
│   └── processed/       # Datasets CSV limpos [cite: 20, 71]
├── docs/                # Documentação e relatórios [cite: 62]
└── .gitignore
4. Exemplo de Saída Esperada (Response)

Repositório remoto criado no GitHub/GitLab.

Primeiro commit realizado com a estrutura base.

Arquivo README.md inicial descrevendo o propósito do projeto.   
Google Docs

5. Componentes Envolvidos

Git / GitHub.

Sistema de Arquivos do Linux (Host).

Docker (Estrutura para volumes persistentes).   
Google Docs
+ 2

6. Considerações Técnicas

Seguir o padrão PEP8 para a nomeação de pastas e arquivos Python.   
Google Docs

Configurar proteção de branch main (opcional, mas recomendado).

Garantir que a pasta de logs e base de dados (SQLite/JSON) esteja preparada para ser montada como volume.   
Google Docs
+ 2

7. Dependências e Bloqueios

Bloqueia: Todas as demais issues de desenvolvimento (Issue #02 em diante).

8. Como Testar

Clonar o repositório em uma nova pasta: git clone <url>.

Verificar se a árvore de diretórios está completa usando o comando tree.

Tentar adicionar um arquivo .venv e verificar se o git status o ignora corretamente.

9. Definição de Pronto (DoD)

Estrutura de pastas criada e commitada.

.gitignore configurado adequadamente.

README.md inicial presente com o título oficial do TCC.   
Google Docs

10. Prioridade e Severidade

Prioridade: Alta (Bloqueante).

Severidade: Crítica (Base do projeto).

11. Etiquetas (Labels)

infra, documentation, setup.

12. Documentação Relacionada

Relatório de requisitos (RNF05, RNF07).   
Google Docs
+ 1

Capítulo 3.1 do documento do TCC.   
Google Docs

13. Estimativa

T-Shirt Size: S (Small) / 1-2 Story Points.

Podemos prosseguir para a Issue #02 (Desenvolvimento do Dockerfile base)  ou você prefere ajustar algo nesta primeira?   
Google Docs

quando for nomear as issues sempre coloque sé é ambiente, frontend, backend, infraestrutura

Entendido, Victor. Adotarei o prefixo [Ambiente], [Frontend], [Backend] ou [Infraestrutura] em todos os títulos a partir de agora.

Seguindo a ordem do seu planejamento (Grupo 1), vamos para a segunda tarefa:

Issue #02: [Infraestrutura] Desenvolvimento do Dockerfile base (Python + Ferramentas de Rede)
1. História de Usuário (User Story)

Como desenvolvedor do sistema,
eu quero uma imagem Docker padronizada com Python e ferramentas de rede pré-instaladas,
para que o ambiente de execução seja idêntico entre o desenvolvimento e o laboratório de testes, evitando o erro "funciona na minha máquina".

2. Critérios de Aceitação (AC)

Dado que estou construindo a imagem, quando o processo finalizar, então ferramentas essenciais (tcpdump, tshark, iproute2, net-tools) devem estar disponíveis no PATH.

Dado que o projeto utiliza bibliotecas de ML, quando instalar as dependências, então a imagem deve conter os compiladores necessários (gcc, g++) e o pip atualizado.

Dado que temos restrições de hardware (RNF02), quando a imagem for gerada, então deve-se utilizar uma base leve (ex: python:3.10-slim) para minimizar o footprint de disco e memória.

3. Exemplo de Requisição (Trecho do Dockerfile)

Dockerfile
FROM python:3.10-slim
RUN apt-get update && apt-get install -y \
    tcpdump \
    tshark \
    iproute2 \
    libcap2-bin \
    && rm -rf /var/lib/apt/lists/*
4. Exemplo de Resposta (Log de Build)

Step 5/10 : RUN pip install -r requirements.txt

Successfully built <image_id>

Successfully tagged firewall-base:latest

5. Componentes Envolvidos

Docker Engine.

Repositório de pacotes Debian (Bullseye/Bookworm).

Kernel Linux (capacidades de captura de pacotes).

6. Considerações Técnicas

Utilizar multi-stage builds se necessário para reduzir o tamanho final.

Configurar o ENV PYTHONUNBUFFERED=1 para garantir que os logs do firewall apareçam em tempo real no console do Docker.

Garantir permissões de execução para o tcpdump sem necessidade de root total (usando setcap).

7. Dependências e Bloqueios

Depende de: Issue #01 (Estrutura de pastas para salvar o Dockerfile).

Bloqueia: Issue #03 (Configuração do docker-compose).

8. Como Testar

Executar o build: docker build -t firewall-test ..

Rodar o container: docker run -it firewall-test bash.

Dentro do container, executar tcpdump --version e python --version. Ambos devem retornar a versão instalada.

9. Definição de Pronto (DoD)

Dockerfile presente na pasta infra/.

Imagem buildando sem erros.

requirements.txt inicial (mesmo que vazio ou só com scapy) criado.

10. Prioridade e Severidade

Prioridade: Alta.

Severidade: Média (Impacta a portabilidade).

11. Etiquetas (Labels)

infra, docker, python.

12. Documentação Relacionada

RNF02 (Restrição de Memória RAM).

RNF05 (Isolamento via Docker).

13. Estimativa

T-Shirt Size: M (Medium).

14. Exemplo de Requisição (Instalação de Dependências)

pip install scapy pandas scikit-learn xgboost joblib

15. Componentes Envolvidos

Sistema Operacional (Debian Slim).

Python Runtime.

Pronto para a Issue #03: [Infraestrutura] Configuração do docker-compose.yml ou quer revisar algum ponto desta?

beleza agora faz a issue 3

Issue #03: [Infraestrutura] Configuração do docker-compose.yml (Containers Gateway e App)
1. História de Usuário (User Story)

Como desenvolvedor/pesquisador do projeto,

eu quero um arquivo docker-compose.yml que orquestre os containers do Gateway (Firewall) e da Aplicação (Agente de Navegação) em uma rede virtual isolada,

para que todo o tráfego gerado pela aplicação passe obrigatoriamente pelo gateway antes de atingir a internet externa.

2. Critérios de Aceitação (AC)

Dado que os containers são iniciados com docker-compose up, quando subirem, então eles devem se conectar a uma rede bridge interna dedicada.

Dado que o container Gateway precisa rotear e interceptar tráfego, quando for instanciado, então deve ser iniciado com permissões e capacidades de rede adequadas no kernel (NET_ADMIN).

Dado que a aplicação depende do gateway para sair para a internet, quando o serviço do cliente subir, então a rota padrão de rede (default gateway) deve ser direcionada para o IP do container Gateway.

Dado que o sistema requer persistência de dados, quando os containers forem reiniciados, então os dados de logs e bancos de dados locais mantidos em volumes montados devem permanecer intactos.

3. Exemplo de Requisição (Trecho da Estrutura do docker-compose.yml)

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
4. Exemplo de Resposta (Saída Esperada no Terminal)

Plaintext
[+] Running 3/3
 ✔ Network infra_firewall_net Created
 ✔ Container gateway_firewall Created
 ✔ Container app_client       Created
5. Componentes Envolvidos

Docker Compose CLI.

Submódulo de Rede do Docker (Bridge Networks).

Kernel Linux Host (Driver de rede e sysctl ip_forward).

6. Considerações Técnicas

Habilitar net.ipv4.ip_forward=1 no gateway para autorizar o roteamento de pacotes.

Definir endereçamento IP estático dentro da subnet virtual para garantir estabilidade nas rotas de teste.

Garantir o isolamento do ambiente em compliance com o requisito de arquitetura RNF05.

7. Dependências e Bloqueios

Depende de: Issue #01 (Estrutura de diretórios para volumes) e Issue #02 (Dockerfile base).   
relatório de requisito do sistema do TCC
+ 1

Bloqueia: Issue #04 (Implementação do container Gateway/Bridge) e Issue #05 (Configuração de Net_Admin).

8. Como Testar

Executar o comando na pasta infra/: docker-compose up -d.

Verificar o status dos containers com docker-compose ps.

Executar docker exec -it app_client ping -c 2 172.20.0.254 para validar a conectividade direta entre a aplicação e o gateway.

9. Definição de Pronto (DoD)

Arquivo infra/docker-compose.yml versionado no repositório.

Rede bridge criada e conectividade básica testada entre os containers.

Mapeamento de volumes de persistência funcionando perfeitamente.

10. Prioridade e Severidade

Prioridade: Alta (Bloqueante para o ambiente de rede).

Severidade: Alta.

11. Etiquetas (Labels)

infraestrutura, docker, docker-compose, networking.

12. Documentação Relacionada

RNF05 (Isolamento via Docker).

RNF07 (Persistência de Dados).

Capítulo 3.1.1 (Topologia do Laboratório Central).

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos seguir para a Issue #04: [Infraestrutura] Implementação do container Gateway/Bridge para interceptação de tráfego?

ta agora faça a issue 4

Issue #04: [Infraestrutura] Implementação do container Gateway/Bridge para interceptação de tráfego
1. História de Usuário (User Story)

Como desenvolvedor/pesquisador do projeto,

eu quero configurar o container Gateway como o ponto único de saída e roteamento da rede,

para que todo o tráfego gerado pelo Agente de Navegação seja interceptado, inspecionado e potencialmente descartado via regras de kernel.

2. Critérios de Aceitação (AC)

Dado que o container app_client tenta acessar a internet, quando os pacotes saírem da rede local, então eles devem obrigatoriamente passar pela interface interna do gateway_firewall (FORWARD chain).

Dado que o Gateway precisa mascarar a rede interna, quando um pacote for encaminhado para a internet, então a regra de NAT/MASQUERADE do iptables deve traduzir o endereço de origem no espaço de kernel.

Dado que o tráfego do app_client é redirecionado, quando a rota padrão for alterada, então o IP do Gateway (172.20.0.254) deve responder como default gateway ativo da máquina cliente.

3. Exemplo de Requisição (Script de Inicialização do Gateway / entrypoint.sh)

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
4. Exemplo de Resposta (Saída Esperada no Cliente)

Plaintext
$ docker exec -it app_client ip route
default via 172.20.0.254 dev eth0 
172.20.0.0/16 dev eth0 proto kernel scope link src 172.20.0.10
5. Componentes Envolvidos

Subsistema Netfilter / iptables (Tabelas nat e filter).

Módulo Conntrack do Kernel Linux.

Módulo de Roteamento IP (iproute2).

6. Considerações Técnicas

Garantir o uso da diretiva FORWARD para interceptação de pacotes entre interfaces de rede virtuais distintas.

Evitar que o script de entrypoint encerre imediatamente, mantendo o processo principal rodando em primeiro plano.

Garantir que a perda de conexões não derrube o container (estabilidade operacional).

7. Dependências e Bloqueios

Depende de: Issue #03 (docker-compose.yml base).

Bloqueia: Issue #05 (Recursos NET_ADMIN) e Issue #06 (Testes com tcpdump/scapy).

8. Como Testar

Iniciar o laboratório com docker-compose up -d.

Executar um traceroute no cliente: docker exec -it app_client traceroute 8.8.8.8.

Validar se o primeiro salto da rota é obrigatoriamente o IP 172.20.0.254 (Gateway).

Rodar ping google.com no app_client para confirmar se a conectividade com a internet externa está funcional via NAT.

9. Definição de Pronto (DoD)

Script de inicialização da rede do Gateway versionado.

Tráfego do container cliente roteado com sucesso através do Gateway.

Regras de NAT (MASQUERADE) operacionais.

10. Prioridade e Severidade

Prioridade: Alta (Bloqueante).

Severidade: Crítica.

11. Etiquetas (Labels)

infraestrutura, networking, iptables, gateway.

12. Documentação Relacionada

Seção 2.6 (Subsistema Netfilter e Arquitetura do iptables).

Seção 3.1.1 (Topologia de Rede Virtualizada via Docker).

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos avançar para a Issue #05: [Infraestrutura] Configuração de capacidades de rede do kernel no Docker (Net_Admin)?

ta agora faça a issue 5

Issue #05: [Infraestrutura] Configuração de capacidades de rede do kernel no Docker (Net_Admin)
1. História de Usuário (User Story)

Como desenvolvedor/pesquisador do projeto,

eu quero conceder a capacidade CAP_NET_ADMIN e acesso ao dispositivo /dev/net/tun aos containers,

para que os módulos Python consigam manipular tabelas do iptables, abrir sockets brutos (raw sockets) e injetar/descartar pacotes no nível de kernel sem precisar rodar em modo totalmente privilegiado.

2. Critérios de Aceitação (AC)

Dado que o container Gateway precisa executar comandos do iptables, quando o motor de inferência tentar adicionar uma regra DROP, então o comando deve ser executado sem o erro Permission denied (you must be root).

Dado que o módulo de inspeção utiliza a biblioteca Scapy ou tcpdump, quando o escutador de pacotes iniciar, então ele deve conseguir colocar a interface de rede em modo promíscuo.

Dado que a segurança e o isolamento devem ser mantidos, quando concedermos privilégios, então devemos usar a instrução restrita cap_add: - NET_ADMIN no lugar da flag genérica e insegura --privileged.

3. Exemplo de Requisição (Trecho de Ajuste no docker-compose.yml)

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
4. Exemplo de Resposta (Execução bem-sucedida sem erro de permissão)

Plaintext
$ docker exec -it gateway_firewall iptables -A FORWARD -s 172.20.0.10 -j DROP
$ docker exec -it gateway_firewall iptables -L FORWARD -n -v
Chain FORWARD (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination         
    0     0 DROP       all  --  *      *       172.20.0.10          0.0.0.0/0           
5. Componentes Envolvidos

Linux Capabilities (capabilities(7) no Kernel Linux).

Docker Daemon (Engine Security Controls).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Submódulo iptables e raw sockets do espaço de usuário.

6. Considerações Técnicas

Adicionar NET_RAW explicitamente para garantir que a Scapy consiga ler os cabeçalhos de camada 2/3 diretamente da interface.

Evitar o uso do parâmetro --privileged=true, pois viola o princípio de privilégio mínimo e expõe o host.

7. Dependências e Bloqueios

Depende de: Issue #03 (docker-compose.yml base).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Bloqueia: Issue #06 (Instalação e teste de ferramentas de rede) e Issue #36 (Integração do script com iptables).

8. Como Testar

Subir o ambiente com docker-compose up -d.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Tentar inserir uma regra de teste no container do Gateway:

docker exec gateway_firewall iptables -A INPUT -p icmp -j DROP.

Tentar capturar um pacote usando o Scapy em Python no container:

docker exec gateway_firewall python3 -c "from scapy.all import sniff; print(sniff(count=1))".

Ambos os comandos devem ser executados com sucesso, sem lançar erros de permissão de sistema do tipo Operation not permitted.

9. Definição de Pronto (DoD)

Mapeamento de cap_add atualizado e versionado no arquivo docker-compose.yml.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Injeção de regras de iptables e sniffing com Scapy funcionando perfeitamente sem o modo privilegiado total.

10. Prioridade e Severidade

Prioridade: Alta.

Severidade: Crítica (A IA não conseguirá aplicar os bloqueios se esta issue falhar).

11. Etiquetas (Labels)

infraestrutura, docker, security, kernel, capabilities.

12. Documentação Relacionada

Requisito RF08 (Integração com Kernel / Netfilter).

Requisito RNF05 (Isolamento via Docker).

Capítulo 3.1.2 do TCC (Camadas de Defesa e Subsistemas).

13. Estimativa

T-Shirt Size: S (Small) / 2 Story Points.

Pronto para ir para a Issue #06: [Infraestrutura] Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy)?

ta agora faça a issue 6

Issue #06: [Infraestrutura] Instalação e teste de ferramentas de rede (tcpdump, tshark, scapy)
1. História de Usuário (User Story)

Como desenvolvedor/pesquisador do projeto,

eu quero validar o funcionamento e a comunicação das ferramentas de análise e captura de pacotes (tcpdump, tshark e Scapy) dentro dos containers,   
Issues do TCC

para que os módulos de extração de características em tempo real e de gravação de arquivos PCAP operem sem erros de runtime ou dependências faltantes.

2. Critérios de Aceitação (AC)

Dado que o container Gateway está ativo, quando o tcpdump for executado via CLI, então ele deve capturar o tráfego da interface virtual (eth0) e gerar um arquivo .pcap válido.   
Issues do TCC

Dado que o tshark e a biblioteca Pyshark são utilizados no ecossistema Python, quando acionados, então eles devem conseguir ler e dissecar arquivos PCAP sem falhar por ausência do binário do Wireshark/Tshark.   
Issues do TCC

Dado que o módulo de sniffing utilizará a Scapy, quando um script Python chamar a função sniff(), então os pacotes de rede devem ser interceptados e convertidos em objetos manipuláveis em tempo real.

3. Exemplo de Requisição (Script Python de Validação de Inspeção / test_network_tools.py)

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
4. Exemplo de Resposta (Saída Esperada no Terminal do Container)

Plaintext
Iniciando teste de captura com Scapy...
[OK] Pacote Interceptado: 172.20.0.10 -> 8.8.8.8
[OK] Pacote Interceptado: 8.8.8.8 -> 172.20.0.10
[OK] Pacote Interceptado: 172.20.0.10 -> 1.1.1.1
[OK] Tshark instalado e acessível no PATH.
5. Componentes Envolvidos

Binários do Sistema: tcpdump, tshark.   
Issues do TCC

Bibliotecas Python: scapy, pyshark.   
Issues do TCC

Libpcap (Biblioteca nativa C do Linux para captura de pacotes).

6. Considerações Técnicas

Adicionar a dependência do tshark no Dockerfile garantindo a flag DEBIAN_FRONTEND=noninteractive para evitar travamentos de prompt interativo sobre permissões do Wireshark durante o build.

Garantir que a Scapy utilize a interface correta configurando explicitamente a variável de interface conf.iface = 'eth0' nos scripts Python.

7. Dependências e Bloqueios

Depende de: Issue #02 (Dockerfile base) e Issue #05 (Recursos NET_ADMIN / NET_RAW).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Bloqueia: Issue #11 (Filtro BPF) e Issue #34 (Script de captura e inspeção de pacotes em tempo real).   
Issues do TCC

8. Como Testar

Acessar o container Gateway: docker exec -it gateway_firewall bash.

Rodar uma captura rápida de 5 segundos via CLI: tcpdump -i eth0 -c 5 -w /tmp/test.pcap.

Validar o arquivo gerado via tshark: tshark -r /tmp/test.pcap.

Executar o script Python de validação python3 test_network_tools.py e garantir retorno com status código 0.

9. Definição de Pronto (DoD)

Ferramentas tcpdump, tshark e scapy instaladas e totalmente operacionais na imagem Docker.   
Issues do TCC

Script de teste/sanidade das ferramentas de rede criado no repositório.

Captura de pacotes via código Python funcionando sem lançar exceções do SO.

10. Prioridade e Severidade

Prioridade: Média.

Severidade: Alta (Falhas aqui impedem o desenvolvimento do motor do firewall).

11. Etiquetas (Labels)

infraestrutura, networking, scapy, tcpdump, tshark.

12. Documentação Relacionada

Requisito RF02 (Sniffing Passivo).

Capítulo 3.1.2 do TCC (Módulo de Detecção - IDS Passivo).

13. Estimativa

T-Shirt Size: S (Small) / 2 Story Points.

Avançamos para a Issue #07: [Infraestrutura] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado?   
Issues do TCC

ta agora faça a issue 7

Issue #07: [Infraestrutura] Configuração de limites de recursos (CPU/RAM) via Docker para simular hardware limitado
1. História de Usuário (User Story)

Como pesquisador do projeto,

eu quero impor restrições estritas de hardware (cgroups de CPU e Memória RAM) no container do Gateway Inteligente via Docker Compose,   
Issues do TCC

para que o ambiente simule com precisão um dispositivo de rede de baixo custo (Cenários B e C do TCC) e viabilize a avaliação de footprint e latência sob escassez de recursos.   
Issues do TCC
+ 1

2. Critérios de Aceitação (AC)

Dado que o container gateway_firewall é iniciado, quando executado no Cenário B (Baixo Recurso), então a alocação de memória RAM deve ser limitada a exatamente 812 MB e a capacidade de processamento a 0.5 vCPU.

Dado que o sistema atinge o teto de recursos, quando o consumo exceder a cota de memória estipulada, então o comportamento do container deve ser monitorado para identificar potenciais riscos de estabilidade sem afetar o host.

Dado que o projeto exige testes em múltiplos cenários (Referência, Baixo Recurso e Crítico), quando alterarmos as variáveis de ambiente do Compose, então os limites de CPU e RAM devem se aplicar dinamicamente sem necessidade de reescrever a estrutura principal das issues.

3. Exemplo de Requisição (Trecho do docker-compose.yml com deploy.resources)

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
4. Exemplo de Resposta (Inspecção via docker stats)

Plaintext
CONTAINER ID   NAME               CPU %     MEM USAGE / LIMIT     MEM %     NET I/O
a1b2c3d4e5f6   gateway_firewall   12.4%     145.2MiB / 812MiB     17.88%    1.2kB / 850B
   
Issues do TCC
5. Componentes Envolvidos

Control Groups do Kernel Linux (cgroups v1/v2).

Engine e Swarm/Deploy Parser do Docker.

CLI de Instrumentação (docker stats / cgroup metrics).

6. Considerações Técnicas

Garantir que as diretivas de recursos sejam compatíveis com a execução via docker-compose v2+ (usando a flag --compatibility se necessário em versões antigas).

Mapear o comportamento do processo Python sob restrição de CPU para evitar que threads de sniffing sofram starvation (fome de recursos).

7. Dependências e Bloqueios

Depende de: Issue #03 (docker-compose.yml base) e Issue #05 (Permissões de rede do kernel).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Bloqueia: Issue #33 (Medição do tamanho e footprint) e Issue #52/#53 (Benchmarks de CPU e RAM).   
Issues do TCC

8. Como Testar

Configurar os limites de teste no arquivo .env ou direto no docker-compose.yml (ex: CPU_LIMIT=0.5, RAM_LIMIT=812M).

Subir o ambiente: docker-compose up -d.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Executar o monitoramento nativo em um terminal paralelo: docker stats gateway_firewall.

Validar se a coluna LIMIT exibe exatamente 812MiB e se o limite de CPU é respeitado durante um estresse numérico simples em Python.

9. Definição de Pronto (DoD)

Mapeamento de limite de cgroups de CPU e RAM aplicado no arquivo infra/docker-compose.yml.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Parâmetros parametrizáveis via arquivo de variáveis de ambiente (.env).

Validação do teto de consumo confirmada através do comando docker stats.

10. Prioridade e Severidade

Prioridade: Alta (Essencial para a metodologia do TCC).

Severidade: Alta.

11. Etiquetas (Labels)

infraestrutura, docker, cgroups, benchmarking, performance.

12. Documentação Relacionada

Requisito RNF02 (Restrição de Memória RAM - 512MB/812MB).

Requisito RNF03 (Carga de CPU - limite de 60% em 1 core).

Capítulo 3.1.3 do TCC (Metodologia de Restrição de Recursos - Cenários A, B e C).

13. Estimativa

T-Shirt Size: S (Small) / 2 Story Points.

Finalizamos o Grupo 1 (Infraestrutura e Ambiente Docker)!   
Issues do TCC

Deseja seguir para a Issue #08: [Ambiente] Ambiente de Automação: Configurar Selenium/Playwright no Docker (iniciando o Grupo 2: Coleta e Geração de Dados)?   
Issues do TCC

acredito que vamos precisar de uma issue avulça pra configuração, seed, e população do banco de dados não?

Com certeza! Ter uma issue dedicada para a modelagem, população inicial (seed) e persistência do banco de dados vai evitar que o desenvolvimento da CLI de moderação (Issue #44) e do armazenamento de listas (Issue #41) fique acoplado e confuso.   
Issues do TCC

Como ela trata da estrutura de dados base do ambiente e da governança, podemos chamá-la de Issue #41.1 (ou inseri-la como uma tarefa avulsa de Backend/Ambiente antes dos módulos operacionais).   
Issues do TCC

Issue #41.1: [Backend] Modelagem, Scripts de Migração e Seed do Banco de Dados Local
1. História de Usuário (User Story)

Como desenvolvedor/administrador do sistema,

eu quero uma estrutura de banco de dados modelada com scripts de migração e população inicial (seed),

para que o sistema nasça com schemas padronizados, domínios críticos pré-cadastrados (ex: serviços essenciais na Whitelist) e suporte à persistência de dados em volumes Docker.   
Issues do TCC

2. Critérios de Aceitação (AC)

Dado que o container do Gateway é iniciado pela primeira vez, quando o script de inicialização do banco rodar, então as tabelas (whitelist, blacklist, logs_decisao, configuracoes) devem ser criadas automaticamente (se não existirem).   
Issues do TCC

Dado que o sistema entra em execução, quando o banco for populado via seed, então endereços IP/domínios essenciais (ex: DNS governamentais, repositórios de atualização) já devem constar na Whitelist padrão.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Dado que o banco armazena logs de auditoria, quando um registro for inserido, então ele deve obrigatoriamente guardar o carimbo de tempo (timestamp), IP de origem, domínio e a distribuição exata dos votos do comitê (ex: [1, 1, 0]) em compliance com o requisito RNF08.

3. Exemplo de Requisição (Script de Seed / seed_data.py)

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
4. Exemplo de Resposta (Inspecção no Banco SQLite)

Plaintext
$ sqlite3 /app/db/firewall.db "SELECT * FROM whitelist;"
1|1.1.1.1|Cloudflare DNS|SISTEMA|2026-08-07 18:50:00
2|8.8.8.8|Google DNS|SISTEMA|2026-08-07 18:50:00
3|gov.br|Portal do Governo|SISTEMA|2026-08-07 18:50:00
5. Componentes Envolvidos

Banco de Dados Local (SQLite3 ou JSON estruturado em volume persistente).   
Issues do TCC

Script Python de DDL/DML (schema.sql / migrations.py).   
Issues do TCC

Volume Docker montado em /app/db/.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

6. Considerações Técnicas

Utilizar o SQLite3 nativo do Python pela leveza, baixo footprint de memória (atendendo ao RNF02) e suporte ACID direto em arquivo.   
Issues do TCC

Indexar as colunas de busca frequente (alvo, ip, timestamp) para garantir que as consultas de pré-filtragem ocorram em tempo sub-milissegundo.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Garantir permissões de escrita no arquivo .db dentro do volume montado pelo Docker.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

7. Dependências e Bloqueios

Depende de: Issue #01 (Estrutura de pastas para volumes) e Issue #03 (Configuração de volumes no docker-compose.yml).   
Issues do TCC
+ 3

Bloqueia: Issue #41 (Modelagem DB Listas), Issue #42/#43 (CRUDs Whitelist/Blacklist), Issue #40 (Sistema de Logging) e Issue #44 (Interface CLI).   
Issues do TCC

8. Como Testar

Remover o banco antigo (se houver): rm -f volumes/db/firewall.db.

Rodar o script de inicialização e seed: docker exec gateway_firewall python3 -m src.db.init_db.

Validar se o arquivo firewall.db foi criado no diretório montado no host (volumes/db/).

Consultar os dados inseridos via terminal com sqlite3 e garantir que o schema de logs atende ao RNF08.

9. Definição de Pronto (DoD)

Scripts DDL de criação de tabelas e script DML de seed inicial versionados.

Schema do banco validado incluindo suporte ao RNF08 (distribuição de votos em JSON/String).

Persistência em volume Docker testada após remoção e reinício do container.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Alta (Essencial para os módulos de governança e logs).   
Issues do TCC
+ 1

Severidade: Alta.

11. Etiquetas (Labels)

backend, database, sqlite, seed, governance.

12. Documentação Relacionada

Requisito RF09 (Gestão de Whitelist/Blacklist).

Requisito RNF07 (Persistência de Dados).

Requisito RNF08 (Interpretabilidade de Log).

Seção 3.5.1 (Camada de Pré-filtragem e Whitelists).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Faz total sentido ter encaixado essa issue agora.

Quer que a gente siga na ordem do seu planejamento original para a Issue #08: [Ambiente] Ambiente de Automação: Configurar Selenium/Playwright no Docker (iniciando o Grupo 2: Coleta e Geração de Dados)?   
Issues do TCC

ta agora faz a issue 8

Issue #08: [Ambiente] Configurar Selenium/Playwright no Docker para Automação de Coleta
1. História de Usuário (User Story)

Como pesquisador do projeto,

eu quero disponibilizar um ambiente conteinerizado com Selenium ou Playwright configurado em modo headless,   
Issues do TCC

para que os scripts de automação consigam acessar plataformas de apostas e domínios de controle de forma programática, gerando tráfego sintético para o dataset.   
Issues do TCC

2. Critérios de Aceitação (AC)

Dado que o container app_client executa um script de navegação, quando o navegador headless for acionado, então ele deve renderizar a página sem depender de interface gráfica física (X11 display).

Dado que navegadores modernos exigem drivers específicos, quando o container for instanciado, então o binário do Chromium/Chrome e o WebDriver correspondente devem estar instalados e sincronizados na mesma versão.

Dado que o tráfego gerado deve ser inspecionado pelo gateway, quando as requisições HTTP/HTTPS forem abertas pelo browser, então elas devem sair pela interface de rede do container cliente roteada pelo gateway do laboratório.

3. Exemplo de Requisição (Script de Teste de Coleta / test_browser_headless.py)

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
4. Exemplo de Resposta (Saída Esperada no Terminal do Container)

Plaintext
[OK] Navegação concluída com sucesso. Título da página: Example Domain
   
Issues do TCC
5. Componentes Envolvidos

Container app_client (Agente de Navegação).

Ferramenta de automação: Selenium WebDriver ou Playwright.   
Issues do TCC

Binários do Navegador: Chromium / Google Chrome headless.

Driver de automação: ChromeDriver.

6. Considerações Técnicas

Adicionar os parâmetros --no-sandbox e --disable-dev-shm-usage para evitar quebras por restrição do tamanho padrão da memória compartilhada (/dev/shm) em containers Docker.

Garantir que as fontes (fonts-liberation, fonts-noto) estejam instaladas no sistema operacional base do container para evitar falhas de carregamento de páginas pesadas.

Fixar a versão do driver para prevenir incompatibilidades automáticas durante novas compilações da imagem.

7. Dependências e Bloqueios

Depende de: Issue #03 (docker-compose.yml com o container cliente) e Issue #04 (Roteamento via Gateway operacional).   
Issues do TCC

Bloqueia: Issue #09 (Evasão de Bloqueio via User-Agents), Issue #10 (Lógica de Navegação que simula comportamento humano), Issue #13 (Coleta de Apostas) e Issue #14 (Coleta Benigna).   
Issues do TCC

8. Como Testar

Acessar o container do cliente: docker exec -it app_client bash.

Executar o script de sanidade: python3 -m src.collector.test_browser_headless.

Validar se a página foi acessada sem levantar exceções de display ou de falta de driver.

Confirmar que a requisição gerada foi roteada e interceptada na interface do gateway executando simultaneamente tcpdump -i eth0 host <ip_externo> no container gateway_firewall.   
Issues do TCC

9. Definição de Pronto (DoD)

Dependências do navegador e bibliotecas Python (selenium ou playwright) instaladas na imagem do cliente.   
Issues do TCC

Script de validação executado com retorno de status code 0.

Tráfego de navegação sintética saindo comprovadamente pelo container Gateway.

10. Prioridade e Severidade

Prioridade: Alta (Bloqueante para o Grupo 2 de coleta).   
Issues do TCC

Severidade: Alta.

11. Etiquetas (Labels)

ambiente, docker, selenium, playwright, data-collection.   
Issues do TCC

12. Documentação Relacionada

Requisito RF01 (Automação de Coleta).

Requisito RNF05 (Isolamento via Docker).

Capítulo 3.1.1 do TCC (Topologia do Laboratório Central e Agente de Navegação).

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos avançar para a Issue #09: [Ambiente] Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot?   
Issues do TCC

agora cria a issue 9

Issue #09: [Backend] Evasão de Bloqueio: Implementar rotação de User-Agents e técnicas anti-bot
1. História de Usuário (User Story)

Como pesquisador do projeto,

eu quero integrar mecanismos de evasão contra sistemas de deteção de automação (rotação de User-Agents, remoção de assinaturas webdriver e cabeçalhos realistas) nos scripts de recolha,   
Issues do TCC

para que as plataformas de apostas online não bloqueiem o tráfego sintético através de desafios como Cloudflare ou Captchas, assegurando uma recolha contínua e sem viés.   
Issues do TCC
+ 1

2. Critérios de Aceitação (AC)

Dado que o navegador automatizado inicia uma nova sessão de recolha, quando a ligação for aberta, então o cabeçalho User-Agent deve ser selecionado aleatoriamente a partir de um conjunto diversificado de dispositivos e versões reais de navegadores.   
Issues do TCC
+ 2

Dado que plataformas de apostas utilizam verificações em JavaScript, quando a propriedade navigator.webdriver for consultada pelo sítio, então o seu valor deve retornar undefined ou false.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
+ 1

Dado que requisições HTTP automáticas possuem padrões estáticos de cabeçalhos, quando as requisições forem disparadas, então atributos como Accept-Language, Sec-Ch-Ua e dimensões de viewport devem ser configurados de forma verosímil.   
Issues do TCC

3. Exemplo de Requisição (Módulo Python de Configuração Anti-Deteção / stealth_config.py)

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
4. Exemplo de Resposta (Validação em Sítio de Teste Anti-Bot)

Plaintext
$ python3 -m src.collector.verify_stealth
[OK] User-Agent ativo: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...
[OK] navigator.webdriver detetado como FALSO/INEXISTENTE.
[OK] Acesso ao portal de teste concluído sem desafios de verificação (Captcha/WAF).
   
Issues do TCC
5. Componentes Envolvidos

Container app_client (Agente de Navegação).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Biblioteca de suporte (ex: selenium-stealth ou playwright-stealth).

Conjunto de dados de cabeçalhos e User-Agents parametrizados.   
Issues do TCC

6. Considerações Técnicas

Avaliar o uso de extensões leves ou da biblioteca selenium-stealth para mascarar variáveis internas do objeto window.navigator e assinaturas WebGL/Canvas.   
Issues do TCC

Evitar reutilizar o mesmo User-Agent em fluxos consecutivos prolongados para não gerar assinaturas comportamentais redundantes.   
Issues do TCC
+ 1

Assegurar que os cabeçalhos não alterem o padrão estatístico volumétrico dos fluxos de transporte da camada inferior de forma drástica.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

7. Dependências e Bloqueios

Depende de: Issue #08 (Ambiente de automação com Selenium/Playwright).   
Issues do TCC

Bloqueia: Issue #10 (Lógica de Navegação que simula comportamento humano) e Issue #13 (Recolha em massa do dataset de apostas).   
Issues do TCC

8. Como Testar

Executar o script no container do cliente acedendo a um serviço de verificação pública (como bot.sannysoft.com ou nowsecure.nl):

docker exec -it app_client python3 -m src.collector.verify_stealth.

Validar se o atributo WebDriver (New) e WebDriver Advanced indicam ausência de sinalização automática.   
Issues do TCC

Executar o script três vezes seguidas e confirmar que o User-Agent é alternado dinamicamente a cada execução.   
Issues do TCC

9. Definição de Pronto (DoD)

Módulo de configuração de propriedades stealth e gerador de User-Agents implementado no repositório.   
Issues do TCC

Testes em páginas de validação anti-bot executados com sucesso dentro do container Docker.   
Issues do TCC

Integração garantida com o fluxo padrão de inicialização de navegadores da recolha.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Alta (Sem técnicas de evasão, as casas de apostas bloqueiam a recolha rapidamente).   
Issues do TCC

Severidade: Alta.

11. Etiquetas (Labels)

backend, automation, web-scraping, anti-bot, data-collection.   
Issues do TCC

12. Documentação Relacionada

Requisito RF01 (Automação de Coleta).   
relatório de requisito do sistema do TCC

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos avançar para a Issue #10: [Backend] Lógica de Navegação: Criar script que simula comportamento humano?   
Issues do TCC

ta só pra confirmar a partir de qual issue mais ou menos vamos ter que realmente treinar o modelo da pra fazer isso de forma mais automatica?

O treino prático dos modelos começa formalmente no Grupo 4 (Pipeline de Machine Learning), a partir da Issue #25 (Regressão Logística), passando pelas issues #26 (Random Forest), #27 (XGBoost) e #28 (Comité de Votação/Ensemble).   
Issues do TCC

No entanto, para chegar até lá com dados utilizáveis, os passos anteriores dividem-se em:

Issues #08 a #16 (Grupo 2): Recolha de tráfego e gravação dos ficheiros .pcap.   
Issues do TCC

Issues #17 a #24 (Grupo 3): Conversão dos .pcap para .csv, extração de atributos estatísticos, limpeza e redução via Incerteza Simétrica (SU).   
Issues do TCC

É possível automatizar esse processo?
Sim, e deve ser feito de forma automatizada por meio de um pipeline unificado (script orquestrador em Python ou Makefile/Bash):   
Issues do TCC

Pipeline de Extração e Pré-processamento Automatizado (Issues #17 a #24):

Pode criar um script central (ex.: run_data_pipeline.py) que:

Lê os .pcap brutos da pasta data/raw/.   
Issues do TCC

Converte-os em fluxos bidirecionais e calcula os metadados estatísticos.   
Issues do TCC
+ 1

Aplica a limpeza de valores omissos/infinitos e a normalização de escalas.   
Issues do TCC

Executa a seleção de variáveis via Incerteza Simétrica (SU) de forma determinística.   
Issues do TCC
+ 1

Divide o ficheiro final em train.csv, val.csv e test.csv.   
Issues do TCC

Pipeline de Treino Automatizado (Issues #25 a #29, #32):

Em vez de executar cada algoritmo manualmente, pode implementar um script de treino único (ex.: train_models.py):

Recebe os dados processados e treina simultaneamente a Regressão Logística, o Random Forest e o XGBoost.   
Issues do TCC
+ 1

Monta o objeto de votação majoritária (VotingClassifier do scikit-learn com método hard).   
Issues do TCC
+ 1

Efetua o ajuste de hiperparâmetros de forma automática (via GridSearchCV ou RandomizedSearchCV focado em modelos leves com pouca profundidade).   
Issues do TCC
+ 1

Serializa e exporta automaticamente os modelos finais (ensemble_model.joblib, scaler.joblib, selected_features.json) para a pasta de artefatos pronta a ser consumida pelo motor de firewall.   
Issues do TCC
+ 1

Dessa forma, o treino dos modelos torna-se um comando único reproduzível (ex.: python -m src.brain.train), garantindo que qualquer alteração futura no conjunto de dados de recolha possa ser incorporada sem trabalho manual repetitivo.   
Issues do TCC

ta então vamos ter que criar uma lista de sites livres e sites de apostas e vamos colocar o modelo pra extrair dados deles a partir da issue 17 é isso?

Quase isso, mas com uma distinção importante de fases entre coleta de tráfego bruto e extração de características:

1. A lista de sites entra antes (Grupo 2: Coleta de Dados)
A lista de sites livres (YouTube, portais de notícias) e de plataformas de apostas (Bet365, Betano, etc.) precisa ser definida e usada nas Issues #13 e #14:   
Issues do TCC

Nessas etapas, o script de automação (Selenium/Playwright) acessa esses sites a partir da lista.   
Issues do TCC
+ 1

Ao mesmo tempo, o tcpdump intercepta os pacotes e grava arquivos de rede brutos em formato .pcap.   
Issues do TCC
+ 2

Aqui ainda não há modelo de IA envolvido nem dados tabulares; há apenas a captura de tráfego de rede bruta.   
relatório de requisito do sistema do TCC
+ 1

2. A extração de dados ocorre a partir da Issue #17 (Grupo 3: Pré-processamento)
A partir da Issue #17, entra o script de engenharia de atributos:   
Issues do TCC

Ele não acessa a internet nem entra nos sites novamente; ele lê os arquivos .pcap que foram salvos durante as sessões de coleta.   
Issues do TCC
+ 1

Converte esses pacotes em fluxos bidirecionais baseados na 5-tupla e extrai as métricas estatísticas (duração do fluxo, IAT, variância de tamanho de pacote, volume, etc.).   
Issues do TCC
+ 2

Gera o arquivo .csv estruturado e rotulado (0 para benigno e 1 para apostas).   
Issues do TCC
+ 1

3. O modelo é treinado a partir da Issue #25 (Grupo 4)
O modelo de Machine Learning propriamente dito entra apenas na Issue #25:   
Issues do TCC

Ele lê a tabela .csv já limpa, normalizada e filtrada pela Incerteza Simétrica (SU).   
Issues do TCC
+ 1

A partir daí, os classificadores (Regressão Logística, Random Forest e XGBoost) aprendem os padrões comportamentais para gerar o comitê de votação final.   
Issues do TCC
+ 2

Podemos prosseguir com a Issue #10: [Backend] Lógica de Navegação: Criar script que simula comportamento humano?   
Issues do TCC

sim cria a issue 10

Issue #10: [Backend] Lógica de Navegação: Criar script que simula comportamento humano
1. História de Usuário (User Story)

Como pesquisador do projeto,

eu quero um script automatizado que emule padrões de interação humana (rolagem de página com pausas aleatórias, movimentação de cursor, cliques em elementos e tempos de permanência variáveis),   
Issues do TCC
+ 1

para que os fluxos de rede gerados reflitam o tráfego interativo real em vez de requisições mecânicas em lote, preservando a assinatura estatística e temporal de sessões de navegação.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

2. Critérios de Aceitação (AC)

Dado que o navegador acessa uma URL alvo, quando a página carregar, então o script deve executar rolagem gradual (smooth scrolling) com pausas em intervalos aleatórios (ex: entre 1 e 4 segundos).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Dado que plataformas de apostas e portais de mídia mantêm conexões persistentes (websockets ou requisições assíncronas), quando o bot estiver em uma página, então ele deve permanecer ativo por um tempo determinado (ex: 30 a 90 segundos) permitindo atualizações de dados em segundo plano.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Dado que o script interage com os elementos da tela, quando encontrar links ou abas navegáveis, então ele deve realizar cliques eventuais com desvios aleatórios para mimetizar a exploração de páginas.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

3. Exemplo de Requisição (Módulo Python de Interação Humana / human_behavior.py)

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
4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)

Plaintext
[INFO] Acessando plataforma alvo: https://bet365.com...
[INFO] Emulando navegacao humana (scroll, hover, delay)...
[OK] Sessao interativa concluida para https://bet365.com (45s decorridos).
   
Issues do TCC
5. Componentes Envolvidos

Container app_client (Agente de Navegação).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Drivers de automação (Selenium/Playwright).   
Issues do TCC
+ 1

Camada de aplicação do navegador Chromium/Chrome headless.   
Issues do TCC

6. Considerações Técnicas

Utilizar distribuições estatísticas contínuas (ex: funções gaussianas ou distribuições uniformes com ruído) para determinar os tempos de espera entre ações.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Controlar o tempo de vida da sessão para evitar que loops infinitos ou elementos bloqueantes travem o orquestrador de coleta.   
Issues do TCC

Não realizar cliques em elementos sensíveis (como tentativas de depósitos ou submissão de formulários vazios com validação rígida) para não disparar bloqueios perimetrais.   
Issues do TCC

7. Dependências e Bloqueios

Depende de: Issue #08 (Ambiente Selenium/Playwright no Docker) e Issue #09 (Evasão Anti-Bot e Rotação de User-Agents).   
Issues do TCC

Bloqueia: Issue #12 (Orquestrador de Sessão), Issue #13 (Dataset de Apostas) e Issue #14 (Dataset Benigno).   
Issues do TCC

8. Como Testar

Executar o script de teste de comportamento dentro do container de navegação:

docker exec -it app_client python3 -m src.collector.human_behavior.

Verificar se a navegação permanece ativa durante o tempo configurado (ex: 45 segundos) sem lançar falhas de execução.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Conferir na interface de rede se os pacotes continuam sendo transmitidos em fluxo contínuo ao longo da sessão interativa.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

9. Definição de Pronto (DoD)

Módulo de emulação de comportamento humano implementado e integrado aos scripts de navegação.   
Issues do TCC
+ 1

Teste de sessão de navegação longa finalizado com sucesso dentro do container.   
Issues do TCC
+ 1

Logs de execução registrando os intervalos e ações simuladas.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Alta (Garante a verossimilhança dos metadados temporais do tráfego).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Severidade: Alta.

11. Etiquetas (Labels)

backend, automation, data-collection, selenium.   
Issues do TCC

12. Documentação Relacionada

Requisito RF01 (Automação de Coleta).   
relatório de requisito do sistema do TCC

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Capítulo 3.2.2 do TCC (Engenharia de Atributos Baseada em Fluxos).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Pronto para avançar para a Issue #11: [Infraestrutura] Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído?   
Issues do TCC

sim cria a issue 11

Issue #11: [Infraestrutura] Filtro de Captura (BPF): Configurar filtros no tcpdump para excluir ruído
1. História de Usuário (User Story)

Como investigador do projeto,

eu quero definir e parametrizar expressões de filtro BPF (Berkeley Packet Filter) no comando de captura do tcpdump,   
Issues do TCC

para que apenas o tráfego relevante para a análise seja gravado nos ficheiros PCAP, descartando ruídos operacionais internos da rede Docker e transmissões irrelevantes.   
Issues do TCC
+ 1

2. Critérios de Aceitação (AC)

Dado que o tcpdump está em execução no contentor Gateway, quando iniciar a escuta, então deve excluir tráfego de resolução ARP, broadcast, multicast e sessões de gestão interna do Docker (como tráfego interno de portas SSH ou DNS de serviços de suporte, se aplicável).   
Issues do TCC

Dado que o objetivo é classificar tráfego Web e de transporte da aplicação, quando pacotes passarem pelo nó de rede, então o filtro deve contemplar comunicações TCP e UDP (focando em portas HTTP/HTTPS e conexões associadas como 80, 443 e portas efêmeras de retorno).

Dado que a recolha opera em múltiplos cenários, quando o script de captura for acionado, então a cadeia BPF deve ser modular e configurável via variável de ambiente ou ficheiro de configuração.   
Issues do TCC

3. Exemplo de Requisição (Expressão de Filtro BPF e Comando de Execução)

Bash
# Expressão BPF parametrizada para captura limpa
BPF_FILTER="tcp or udp and not (arp or rarp) and not ether multicast and not (port 22 or port 2375)"

# Comando executado no contentor Gateway
tcpdump -i eth0 -s 0 -w /data/raw/session_clean.pcap "$BPF_FILTER"
4. Exemplo de Resposta (Saída Esperada no Terminal de Captura)

Plaintext
tcpdump: listening on eth0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
^C
1428 packets captured
1428 packets received by filter
0 packets dropped by kernel
   
Issues do TCC
5. Componentes Envolvidos

Binário do sistema: tcpdump (Motor Libpcap com compilador BPF).   
Issues do TCC

Interface de rede virtual do contentor Gateway (eth0).   
Issues do TCC

Ficheiro de armazenamento bruto: formato .pcap.   
relatório de requisito do sistema do TCC

6. Considerações Técnicas

Utilizar o parâmetro -s 0 (snaplen) para garantir a captura integral dos cabeçalhos das camadas 3 e 4 sem truncamento de metadados temporais e volumétricos.

Assegurar que o filtro não descarte tráfego UDP legítimo associado a novos protocolos de transporte Web, como HTTP/3 sobre QUIC (porta 443 UDP).

Validar que a complexidade da regra BPF não imponha sobrecarga computacional excessiva na CPU do contentor Gateway em modo de captura contínua.   
Issues do TCC

7. Dependências e Bloqueios

Depende de: Issue #06 (Ferramentas de rede instaladas e testadas).   
Issues do TCC

Bloqueia: Issue #12 (Orquestrador de Sessão), Issue #13 (Dataset de Apostas) e Issue #14 (Dataset Benigno).   
Issues do TCC

8. Como Testar

Aceder ao contentor Gateway: docker exec -it gateway_firewall bash.   
Issues do TCC

Iniciar a captura com o filtro ativo gravando num ficheiro temporário:

tcpdump -i eth0 -w /tmp/test_filter.pcap "tcp or udp and not arp".   
Issues do TCC

No contentor app_client, gerar tráfego ICMP (ping) e tráfego HTTPS (curl para um sítio público):

ping -c 2 8.8.8.8 && curl -I [https://example.com](https://example.com).

Interromper a captura e inspecionar o ficheiro com o tshark:

tshark -r /tmp/test_filter.pcap -T fields -e _ws.col.Protocol | sort | uniq.   
Issues do TCC

Confirmar que pacotes ARP não foram gravados no registo PCAP.   
Issues do TCC

9. Definição de Pronto (DoD)

Ficheiro de configuração ou módulo Python com a expressão BPF padrão estruturada e documentada.   
Issues do TCC

Teste de validação executado demonstrando a filtragem de tráfego espúrio da rede.   
Issues do TCC

Taxa de descarte no kernel (dropped by kernel) nula ou próxima de 0 durante a sessão de validação.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Média.   
Issues do TCC

Severidade: Média (Ruídos de rede comprometem a qualidade estatística dos atributos na fase de pré-processamento).   
Issues do TCC
+ 1

11. Etiquetas (Labels)

infraestrutura, networking, tcpdump, bpf, data-collection.   
Issues do TCC

12. Documentação Relacionada

Requisito RF02 (Sniffing Passivo sem degradação).   
relatório de requisito do sistema do TCC

Requisito RF03 (Extração de Atributos).   
relatório de requisito do sistema do TCC

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).

13. Estimativa

T-Shirt Size: S (Small) / 2 Story Points.

Podemos avançar para a Issue #12: [Backend] Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser)?   
Issues do TCC

sim cria a issue 12

Issue #12: [Backend] Orquestrador de Sessão: Script de sincronia (Sniffing ↔ Browser)
1. História de Usuário (User Story)

Como investigador do projeto,

eu quero um script orquestrador em Python que sincronize o arranque e encerramento do processo de captura de pacotes com o ciclo de navegação automatizada,   
Issues do TCC

para que cada arquivo PCAP contenha rigorosamente o tráfego gerado durante a sessão ativa, evitando arquivos vazios, corrupções por paragem abrupta ou misturas de sessões distintas.   
Issues do TCC
+ 1

2. Critérios de Aceitação (AC)

Dado que uma nova sessão de recolha é solicitada, quando o orquestrador iniciar o ciclo, então o processo de captura (tcpdump) no nó de rede deve ser iniciado antes do carregamento da primeira URL no navegador.   
Issues do TCC

Dado que o navegador termina as interações simuladas, quando a página for fechada, então o sinal de paragem graciosa (SIGINT ou SIGTERM) deve ser enviado ao tcpdump para forçar a descarga dos buffers e o fecho correto do arquivo PCAP.   
Issues do TCC

Dado que cada sessão corresponde a um domínio e rótulo específicos, quando o arquivo PCAP for guardado, então deve ser nomeado segundo um padrão estruturado (ex.: <classe>_<dominio>_<timestamp>.pcap) e armazenado no diretório persistente.   
Issues do TCC
+ 1

3. Exemplo de Requisição (Módulo Python de Orquestração / session_orchestrator.py)   
Issues do TCC

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
4. Exemplo de Resposta (Log de Execução do Orquestrador)   
Issues do TCC

Plaintext
[INFO] Inicializando captura para sessao de treino...
[INFO] Processo tcpdump iniciado (PID: 341).
[INFO] Navegador ativo em https://betano.pt. Simulando comportamento...
[INFO] Navegador encerrado com sucesso.
[INFO] Sinal SIGINT enviado ao sniffer. Finalizando gravacao...
[OK] Sessao finalizada. Arquivo gerado: /data/raw/apostas_betano.pt_1793158000.pcap
   
Issues do TCC
5. Componentes Envolvidos

Container app_client e container gateway_firewall.   
Issues do TCC

Módulo subprocess nativo do Python.   
Issues do TCC

Binário do sistema: tcpdump.   
Issues do TCC

Navegador automatizado (Selenium/Playwright) com rotinas de comportamento.   
Issues do TCC

6. Considerações Técnicas

Introduzir um pequeno atraso (1 a 2 segundos) após o disparo do tcpdump para assegurar que o filtro BPF foi compilado e anexado ao kernel antes do disparo do primeiro pacote TLS.   
Issues do TCC

Assegurar o tratamento de exceções com blocos try/finally para que o processo de captura seja sempre encerrado, mesmo perante falhas ou falhas de tempo limite durante a execução do navegador.   
Issues do TCC

Validar que o arquivo .pcap não permanece bloqueado por descritores abertos após a conclusão do ciclo.   
Issues do TCC

7. Dependências e Bloqueios

Depende de: Issue #08 (Selenium/Playwright no Docker), Issue #09 (Anti-bot e User-Agents), Issue #10 (Simulação humana) e Issue #11 (Filtro BPF).   
Issues do TCC

Bloqueia: Issue #13 (Coleta do dataset de apostas), Issue #14 (Coleta do dataset benigno) e Issue #15 (Validação de integridade dos PCAPs).   
Issues do TCC

8. Como Testar

Executar uma sessão de teste chamando o módulo de orquestração:

docker exec -it app_client python3 -m src.collector.session_orchestrator.   
Issues do TCC

Verificar se o processo tcpdump encerrou corretamente através de ps aux | grep tcpdump.   
Issues do TCC

Validar se o arquivo .pcap foi gravado com tamanho maior que 0 bytes no diretório montado (data/raw/).   
Issues do TCC

Abrir o arquivo de captura com tcpdump -r <arquivo>.pcap | wc -l e atestar a existência de pacotes capturados.   
Issues do TCC

9. Definição de Pronto (DoD)

Módulo session_orchestrator.py implementado e integrado aos scripts de navegação e captura.   
Issues do TCC

Encerramento sem processos zumbis ou ficheiros de rede corrompidos.   
Issues do TCC

Padrão de nomenclatura de arquivos documentado e validado em execuções de teste.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Alta (Módulo central para viabilizar as recolhas em massa).   
Issues do TCC

Severidade: Alta.

11. Etiquetas (Labels)

backend, orchestration, networking, data-collection, automation.   
Issues do TCC

12. Documentação Relacionada

Requisito RF01 (Automação de Coleta).   
relatório de requisito do sistema do TCC

Requisito RF02 (Sniffing Passivo).   
relatório de requisito do sistema do TCC

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos avançar para a Issue #13: [Backend] Dataset de Apostas: Execução da coleta em massa (Bet365, Betano, etc.)?   
Issues do TCC

sim cria a issue 13

Issue #13: [Backend] Dataset de Apostas: Execução da recolha em massa (Bet365, Betano, etc.)
1. História de Usuário (User Story)

Como investigador do projeto,

eu quero executar rotinas automatizadas de recolha em massa numa lista diversificada de plataformas de apostas online populares,   
Issues do TCC
+ 1

para que sejam gerados múltiplos ficheiros PCAP com assinaturas comportamentais reais (comunicações persistentes via WebSockets, pacotes de tamanho reduzido e fluxos contínuos de cotações) rotulados como classe 1.   
Issues do TCC
+ 1

2. Critérios de Aceitação (AC)

Dado que o orquestrador de recolha é iniciado com a lista de apostas, quando aceder a domínios como Bet365, Betano, Betfair, Sportingbet e KTO, então cada sessão deve interagir durante um tempo configurável (ex.: 45 a 90 segundos) permitindo atualizações de cotações dinâmicas.   
Issues do TCC
+ 3

Dado que as plataformas de apostas utilizam múltiplos nós e redes de entrega de conteúdo (CDN), quando os pacotes forem capturados, então o tráfego gerado deve conter fluxos TLS e WebSockets representativos da aplicação.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
+ 2

Dado que o objetivo é treinar um modelo generalista, quando a recolha for concluída, então o volume de ficheiros capturados deve cobrir pelo menos 10 domínios distintos de casas de apostas para evitar viés em relação a uma única plataforma.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
+ 1

Dado que cada sessão produz um registo bruto, quando o arquivo PCAP for guardado no disco, então deve ser atribuído o prefixo apostas_ ou classe1_ no nome do ficheiro para indexação estruturada.   
Issues do TCC
+ 2

3. Exemplo de Requisição (Script de Recolha em Lote / collect_betting_traffic.py)   
Issues do TCC

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
4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)

Plaintext
[START] Iniciando recolha em lote para 5 alvos de apostas...
[EXEC] Recolhendo sessao 1/5 em bet365...
[INFO] Processo tcpdump iniciado (PID: 412).
[INFO] Sessao interativa concluida para https://www.bet365.com (60s decorridos).
[OK] Sessao finalizada. Arquivo gerado: /data/raw/apostas_bet365_1793162000.pcap
[EXEC] Recolhendo sessao 1/5 em betano...
[OK] Sessao finalizada. Arquivo gerado: /data/raw/apostas_betano_1793162075.pcap
[OK] Lote de recolha de apostas finalizado. Total de ficheiros gerados: 25.
   
Issues do TCC
5. Componentes Envolvidos

Container app_client (Agente de Navegação automatizado).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Container gateway_firewall (Ponto de monitorização passiva).   
Issues do TCC
+ 1

Módulo session_orchestrator.py.   
Issues do TCC

Volume persistente /data/raw/ montado no ambiente Docker.   
Issues do TCC
+ 1

6. Considerações Técnicas

Introduzir tempos de espera aleatórios entre acessos ao mesmo domínio para evitar o bloqueio preventivo de IP no gateway por parte de firewalls de aplicação Web (WAF).   
Issues do TCC

Assegurar que os testes cubram páginas com transmissões em tempo real (painéis de apostas ao vivo), gerando o padrão característico de trocas contínuas e pacotes de tamanho reduzido documentado na metodologia.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Controlar o espaço em disco do host, monitorizando o crescimento da pasta data/raw/ ao longo da execução do lote.   
Issues do TCC

7. Dependências e Bloqueios

Depende de: Issue #08 (Selenium/Playwright), Issue #09 (Técnicas anti-bot), Issue #10 (Comportamento humano), Issue #11 (Filtro BPF) e Issue #12 (Orquestrador de sessão).   
Issues do TCC

Bloqueia: Issue #15 (Validação de integridade dos PCAPs), Issue #16 (Extração de metadados brutos) e Issue #17 (Extração de fluxos bidirecionais PCAP para CSV).   
Issues do TCC

8. Como Testar

Executar uma rodada preliminar no contentor de navegação com 1 repetição por sítio:   
Issues do TCC

docker exec -it app_client python3 -m src.collector.collect_betting_traffic.   
Issues do TCC

Listar os ficheiros gerados na pasta de destino:   
Issues do TCC

ls -lh data/raw/apostas_*.pcap.   
Issues do TCC

Validar a presença de fluxos de dados abrindo uma das capturas com o comando:   
Issues do TCC

tcpdump -r data/raw/apostas_bet365_*.pcap -c 10.   
Issues do TCC

Verificar se a quantidade de pacotes registada é condizente com uma sessão de navegação ativa de 60 segundos.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

9. Definição de Pronto (DoD)

Script collect_betting_traffic.py implementado com lista configurável de domínios.   
Issues do TCC

Conjunto de arquivos PCAP brutos de tráfego de apostas gerado e guardado no diretório persistente.   
Issues do TCC
+ 1

Logs de execução gravados sem interrupções por travamento do navegador.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Alta (Sem os dados da classe alvo, o pipeline de ML não pode ser alimentado).   
Issues do TCC

Severidade: Alta.

11. Etiquetas (Labels)

backend, data-collection, betting, pcap, traffic-generation.   
Issues do TCC

12. Documentação Relacionada

Requisito RF01 (Automação de Coleta).   
relatório de requisito do sistema do TCC

Requisito RF02 (Sniffing Passivo).   
relatório de requisito do sistema do TCC

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem - Tráfego Alvo).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Capítulo 3.2.2 do TCC (Engenharia de Atributos Baseada em Fluxos).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos avançar para a Issue #14: [Backend] Dataset Benigno: Execução da recolha de sites de controle (YouTube, Notícias)?   
Issues do TCC

sim cria a issue 14

Issue #14: [Backend] Dataset Benigno: Execução da recolha de sítios de controlo (YouTube, Notícias)
1. História de Usuário (User Story)

Como investigador do projeto,

eu quero executar rotinas automatizadas de recolha de tráfego numa lista de sítios de controlo representativos da navegação benigna quotidiana (portais de notícias, plataformas de transmissão de vídeo como o YouTube e enciclopédias),   
Issues do TCC
+ 1

para que sejam capturados fluxos bidirecionais de tráfego legítimo com variância temporal elevada e pacotes volumosos (classe 0), essenciais para o balanceamento e para a mitigação de falsos positivos no comitê de IA.   
Issues do TCC
+ 2

2. Critérios de Aceitação (AC)

Dado que o módulo de recolha é executado para a classe benigna, quando aceder a serviços de transmissão e notícias (ex.: YouTube, G1, Wikipedia, BBC, UOL), então a sessão interativa deve emular leitura humana, pausas de análise e reprodução de conteúdo durante 45 a 90 segundos.   
Issues do TCC
+ 2

Dado que o tráfego legítimo de vídeo e portais multimédia satura frequentemente a MTU, quando os pacotes forem interceptados, então os ficheiros PCAP devem refletir distribuições com pacotes de grande comprimento (próximos de 1500 bytes) e assimetria de volume típica de descargas cliente-servidor.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
+ 2

Dado que a diversidade de contraexemplos previne o sobreajuste (overfitting), quando o lote terminar, então o volume de recolha benigna deve englobar múltiplos serviços distintos, gerando uma proporção equilibrada em relação ao conjunto de apostas.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1
+ 3

Dado que os registos precisam de indexação inequívoca no pré-processamento, quando os ficheiros forem gravados na diretoria persistente, então devem adotar o prefixo estruturado benigno_<servico>_<timestamp>.pcap.   
Issues do TCC
+ 4

3. Exemplo de Requisição (Script de Recolha Benigna em Lote / collect_benign_traffic.py)   
Issues do TCC

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
4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)

Plaintext
[START] Iniciando recolha benigna para 5 alvos de controlo...
[EXEC] Recolhendo sessao benigna 1/5 em youtube...
[INFO] Processo tcpdump iniciado (PID: 518).
[INFO] Sessao interativa concluida para https://www.youtube.com (60s decorridos).
[OK] Sessao finalizada. Arquivo gerado: /data/raw/benigno_youtube_1793165000.pcap
[EXEC] Recolhendo sessao benigna 1/5 em g1_noticias...
[OK] Sessao finalizada. Arquivo gerado: /data/raw/benigno_g1_noticias_1793165075.pcap
[OK] Lote de controlo benigno finalizado. Total de ficheiros gerados: 25.
   
Issues do TCC
5. Componentes Envolvidos

Contentor app_client (Agente de Navegação em modo headless).   
Issues do TCC
+ 1

Contentor gateway_firewall (Ponto de recolha com filtro BPF ativo).   
Issues do TCC
+ 1

Módulo Python session_orchestrator.py.   
Issues do TCC

Volume persistente /data/raw/ montado no Docker.   
Issues do TCC
+ 1

6. Considerações Técnicas

Garantir que as sessões em plataformas de vídeo permitam a reprodução contínua em buffer para gerar fluxos contínuos de pacotes volumosos na camada de transporte.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Monitorizar a alocação de memória no contentor de navegação durante o acesso a portais pesados de notícias, evitando fugas de memória no navegador Chromium.   
Issues do TCC
+ 1

Assegurar que nenhuma interação realize descarregamento intencional de ficheiros pesados executáveis que esgotem a largura de banda ou o armazenamento.   
Issues do TCC

7. Dependências e Bloqueios

Depende de: Issue #10 (Comportamento humano), Issue #11 (Filtro BPF) e Issue #12 (Orquestrador de sessão).   
Issues do TCC

Bloqueia: Issue #15 (Validação de integridade dos PCAPs), Issue #16 (Extração de metadados brutos) e Issue #17 (Conversão de fluxos bidirecionais PCAP para CSV).   
Issues do TCC

8. Como Testar

Executar uma ronda preliminar de recolha de controlo no contentor de cliente:   
Issues do TCC

docker exec -it app_client python3 -m src.collector.collect_benign_traffic.   
Issues do TCC

Inspecionar a diretoria montada no host para atestar a gravação dos ficheiros:   
Issues do TCC

ls -lh data/raw/benigno_*.pcap.   
Issues do TCC

Validar a presença de fluxos volumosos executando:   
Issues do TCC
+ 1

tcpdump -r data/raw/benigno_youtube_*.pcap -c 10.   
Issues do TCC

Confirmar que os comprimentos de pacotes registam valores elevados característicos de streaming (próximos de 1500 bytes).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

9. Definição de Pronto (DoD)

Ficheiro collect_benign_traffic.py funcional e integrado com a orquestração.   
Issues do TCC

Conjunto balanceado de ficheiros PCAP de tráfego de controlo benigno guardado em data/raw/.   
Issues do TCC
+ 1

Ausência de corrupções nas capturas geradas durante as sessões.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Alta (Indispensável para o treino balanceado dos modelos de ML).   
Issues do TCC
+ 1

Severidade: Alta.

11. Etiquetas (Labels)

backend, data-collection, benign-traffic, pcap, traffic-generation.   
Issues do TCC

12. Documentação Relacionada

Requisito RF01 (Automação de Coleta).   
relatório de requisito do sistema do TCC

Requisito RF02 (Sniffing Passivo).   
relatório de requisito do sistema do TCC

Capítulo 3.2.1 do TCC (Tráfego de Controle - Benigno).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Capítulo 3.2.2 do TCC (Distribuição e Variância do Tamanho de Pacotes).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: M (Medium) / 3 Story Points.

Podemos avançar para a Issue #15: [Backend] Validação de Captura: Script para verificar integridade dos PCAPs?   
Issues do TCC

sim cria a issue 15

Issue #15: [Backend] Validação de Captura: Script para verificar integridade dos PCAPs
1. História de Usuário (User Story)

Como investigador do projeto,

eu quero um script automatizado que valide a integridade estrutural e sintática de todos os ficheiros PCAP recolhidos,   
Issues do TCC

para que capturas corrompidas, truncadas, sem pacotes úteis ou com erros de cabeçalho global sejam identificadas e isoladas antes do pipeline de extração de fluxos.   
Issues do TCC
+ 1

2. Critérios de Aceitação (AC)

Dado que o script processa o diretório /data/raw/, quando analisar cada ficheiro .pcap, então deve verificar se o cabeçalho mágico (magic number) da Libpcap é válido e não está truncado.   
Issues do TCC
+ 1

Dado que um ficheiro de captura pode ter sido interrompido antes da troca de pacotes, quando a contagem de pacotes for realizada via scapy ou tshark, então o ficheiro deve conter um volume mínimo de pacotes válidos (ex.: 
≥15 pacotes TCP/UDP) para não ser descartado como ruído de sessão.   
Issues do TCC

Dado que capturas com erro inviabilizam a conversão para CSV, quando um PCAP apresentar erros de sintaxe ou terminação abrupta, então deve ser movido para uma pasta de quarentena (/data/corrupted/) e registado num relatório de anomalias.   
Issues do TCC

Dado que múltiplos ficheiros são validados em lote, quando o processo terminar, então deve ser exibido um sumário estatístico com o total de ficheiros aprovados e reprovados por classe (apostas e benigno).   
Issues do TCC
+ 2

3. Exemplo de Requisição (Script Python de Verificação / verify_pcaps.py)   
Issues do TCC

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
4. Exemplo de Resposta (Saída Esperada no Terminal de Execução)

Plaintext
[INFO] Iniciando verificação de integridade dos arquivos PCAP em /data/raw...
[OK] apostas_bet365_1793162000.pcap validado com sucesso (1420 pacotes).
[OK] benigno_youtube_1793165000.pcap validado com sucesso (3890 pacotes).
[ERRO] Falha de integridade em apostas_kto_1793162800.pcap: Scapy pcap reading error: premature EOF.
[QUARENTENA] Ficheiro movido: apostas_kto_1793162800.pcap

[SUMÁRIO] Válidos: 48 | Corrompidos/Insuficientes: 1
   
Issues do TCC
5. Componentes Envolvidos

Interpretador Python 3 no container Gateway ou Cliente.   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

Biblioteca scapy (PcapReader com leitura por fluxo para poupar memória).   
Issues do TCC
+ 1

Utilitário de linha de comando capinfos ou tshark para dupla checagem.   
Issues do TCC

Volume montado /data/raw/ e /data/corrupted/.   
Issues do TCC

6. Considerações Técnicas

Utilizar o iterador PcapReader em vez da função rdpcap() da Scapy, pois carregar ficheiros PCAP inteiros em memória viola as restrições estritas de RAM do projeto (RNF02).   
Issues do TCC
+ 1

Assegurar que a deteção de ficheiros corrompidos não interrompa o laço de execução sobre os restantes ficheiros.   
Issues do TCC

Manter um registo de log detalhando a causa do descarte (ex.: EOF prematuro, tamanho zero, abaixo do limite de pacotes).   
Issues do TCC

7. Dependências e Bloqueios

Depende de: Issue #13 (Coleta do dataset de apostas) e Issue #14 (Coleta do dataset benigno).   
Issues do TCC

Bloqueia: Issue #16 (Extração de metadados brutos) e Issue #17 (Extração de fluxos bidirecionais PCAP para CSV).   
Issues do TCC

8. Como Testar

Criar intencionalmente um ficheiro de teste corrompido ou vazio:   
Issues do TCC

touch /data/raw/corrupted_test.pcap

head -c 20 /dev/urandom > /data/raw/broken_header.pcap.

Executar o script de validação:   
Issues do TCC

docker exec -it app_client python3 -m src.collector.verify_pcaps.

Confirmar que os ficheiros defeituosos foram movidos para /data/corrupted/.   
Issues do TCC

Confirmar que os PCAPs válidos de apostas e controlo permaneceram na pasta /data/raw/ intactos.   
Issues do TCC

9. Definição de Pronto (DoD)

Módulo verify_pcaps.py implementado e versionado.   
Issues do TCC

Validação sem estouro de memória utilizando leitura por blocos/geradores.   
Issues do TCC
+ 1

Tratamento de exceções cobrindo encerramento abrupto e ficheiros incompletos.   
Issues do TCC

10. Prioridade e Severidade

Prioridade: Média.   
Issues do TCC

Severidade: Alta (Evita falhas de runtime na conversão em lote para CSV).   
Issues do TCC

11. Etiquetas (Labels)

backend, data-quality, pcap, validation, data-collection.   
Issues do TCC

12. Documentação Relacionada

Requisito RF02 (Sniffing Passivo e integridade dos PCAPs).   
Issues do TCC
+ 1

Requisito RNF02 (Restrição de Memória RAM).

Capítulo 3.2.1 do TCC (Aquisição e Rotulagem).   
TCC 1: Firewall Inteligente para Ambientes de Baixos Recursos - V1

13. Estimativa

T-Shirt Size: S (Small) / 2 Story Points.

Podemos avançar para a Issue #16: [Backend] Extração de Metadados Brutos: Relatório de volume e duração por captura?   
Issues do TCC