# Arquitetura do Banco de Dados - Firewall Inteligente

## Visão Geral

O banco de dados PostgreSQL foi modelado para suportar:
- **Gestão de Listas** (Whitelist/Blacklist)
- **Auditoria** (Rastreamento de quem fez o quê e quando)
- **Feedback Loop** (Sistema de tickets para revisão de falsos positivos)
- **Logs de Tráfego** (Alta performance para escrita em tempo real)

## Diagrama ER Simplificado

```
┌─────────────────────────────────────────────────────────────────┐
│                           SISTEMA                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐         ┌──────────────────┐                 │
│  │    users     │ ◄───────│ filtering_rules  │                 │
│  │              │         │  (Whitelist +    │                 │
│  │ • id (PK)    │         │   Blacklist)     │                 │
│  │ • username   │         │                  │                 │
│  │ • role       │         │ • id (PK)        │                 │
│  │ • password   │         │ • target (IP)    │                 │
│  │ • is_active  │         │ • action (ALLOW/ │                 │
│  │ • created_at │         │           DENY)  │                 │
│  └──────────────┘         │ • created_by (FK)                  │
│         │                 │ • created_at     │                 │
│         │                 │ • is_active      │                 │
│         │                 └──────────────────┘                 │
│         │                                                      │
│         └───────────────────────────┬───────────────────────┐  │
│                                     │                       │  │
│                    ┌────────────────────────────┐            │  │
│                    │   review_requests          │            │  │
│                    │  (Feedback Loop)           │            │  │
│                    │                            │            │  │
│                    │ • id (PK)                  │            │  │
│                    │ • traffic_log_id (FK) ────┼────┐       │  │
│                    │ • reporter_email           │    │       │  │
│                    │ • reason                   │    │       │  │
│                    │ • status (PENDING/...)     │    │       │  │
│                    │ • resolved_by (FK) ───────┘    │       │  │
│                    │ • resolved_at              │    │       │  │
│                    │ • created_at               │    │       │  │
│                    └────────────────────────────┘    │       │  │
│                                                       │       │  │
│                                          ┌────────────▼─┐    │  │
│                                          │traffic_logs  │    │  │
│                                          │              │    │  │
│                                          │ • id (PK)    │    │  │
│                                          │ • src_ip     │    │  │
│                                          │ • dst_ip     │    │  │
│                                          │ • port       │    │  │
│                                          │ • verdict    │◄───┘  │
│                                          │ • confidence │       │
│                                          │ • timestamp  │       │
│                                          └──────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Tabelas Detalhadas

### 1. `users` - Controle de Acesso

Armazena usuários e moderadores do sistema.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | Integer | PK | Identificador único |
| `username` | String(50) | UNIQUE, NOT NULL | Nome de usuário para login |
| `email` | String(100) | UNIQUE, NOT NULL | Email do usuário |
| `password_hash` | String(255) | NOT NULL | Hash da senha |
| `role` | Enum | NOT NULL | `admin` ou `moderator` |
| `is_active` | Boolean | DEFAULT TRUE | Controla acesso ativo/inativo |
| `created_at` | DateTime | DEFAULT now() | Timestamp de criação |

**FK Referenciadas:** 
- `filtering_rules.created_by`
- `review_requests.resolved_by`

---

### 2. `filtering_rules` - Gestão de Listas

Unifica Whitelist (ALLOW) e Blacklist (DENY) em uma única tabela para simplificar queries.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | Integer | PK | Identificador único |
| `target` | String(255) | UNIQUE, NOT NULL, INDEX | IP ou domínio (ex: `192.168.1.1`, `bet365.com`) |
| `target_type` | Enum | NOT NULL | `ip`, `domain`, ou `subnet` |
| `action` | Enum | NOT NULL | `allow` (Whitelist) ou `deny` (Blacklist) |
| `reason` | Text | NULL | Justificativa (ex: "Site corporativo", "Aposta detectada") |
| `created_by` | Integer | FK → users.id | Quem criou a regra (auditoria) |
| `created_at` | DateTime | DEFAULT now() | Timestamp |
| `is_active` | Boolean | DEFAULT TRUE | Regra ativa/inativa |

**Índices:**
- `target` (para buscas rápidas em tempo real)

**Exemplo de Query (Motor do Firewall):**
```sql
SELECT action FROM filtering_rules
WHERE target = '192.168.1.100' AND is_active = true
LIMIT 1;
```

---

### 3. `traffic_logs` - Histórico de Tráfego

Registra **todas as requisições** de tráfego de rede. Sem Foreign Keys restritivas para não desacelerar a escrita.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | Integer | PK | Identificador único |
| `source_ip` | String(50) | NOT NULL, INDEX | IP de origem (máquina da rede) |
| `destination_ip` | String(50) | NOT NULL, INDEX | IP destino (site acessado) |
| `destination_domain` | String(255) | NULL | Domínio (ex: `bet365.com`, resolvido via DNS reverse) |
| `port` | Integer | NOT NULL | Porta de destino (80, 443, etc.) |
| `verdict` | Enum | NOT NULL | `allowed_by_rule`, `denied_by_rule`, `allowed_by_ai`, `denied_by_ai` |
| `confidence_score` | Float | NULL | Score da IA (0.0 a 1.0) se `verdict` foi definido por IA |
| `timestamp` | DateTime | DEFAULT now(), INDEX | Quando foi capturado |

**Índices:**
- `source_ip`, `destination_ip` (para achar logs do mesmo cliente/servidor)
- `verdict` (para relatórios)
- `timestamp` (para paginação/histórico)

**Nota:** Sem FK para `filtering_rules` para não causar locks de leitura em alta concorrência.

---

### 4. `review_requests` - Feedback Loop (Issue #46)

Representa tickets de "Falsos Positivos" abertos por usuários.

| Campo | Tipo | Restrições | Descrição |
|-------|------|------------|-----------|
| `id` | Integer | PK | Identificador único |
| `traffic_log_id` | Integer | FK → traffic_logs.id | Qual log que gerou a reclamação |
| `reporter_email` | String(100) | NULL | Email de quem reclamou (opcional, pode vir de formulário) |
| `reason` | Text | NOT NULL | "Este site é da minha faculdade, foi bloqueado erroneamente" |
| `status` | Enum | DEFAULT PENDING | `pending`, `approved`, `rejected` |
| `resolved_by` | Integer | FK → users.id (NULL) | Moderador que fechou o ticket |
| `resolved_at` | DateTime | NULL | Quando foi resolvido |
| `created_at` | DateTime | DEFAULT now() | Quando foi criado |

**Fluxo:**
1. Usuário vê IP/domínio bloqueado → Abre review request
2. Moderador vê fila de `review_requests` com `status = PENDING`
3. Moderador aprova → Nova regra criada em `filtering_rules` (ALLOW) + `review_requests.status = APPROVED`
4. Moderador rejeita → `review_requests.status = REJECTED` (sem criar regra)

---

## Enumerações (Enums)

### `UserRole`
- `admin` — Acesso total
- `moderator` — Pode gerenciar listas e review requests

### `RuleAction`
- `allow` — Whitelist (passa)
- `deny` — Blacklist (bloqueia)

### `TargetType`
- `ip` — Endereço IP individual
- `domain` — Domínio (ex: `bet365.com`)
- `subnet` — Range de IPs (ex: `192.168.0.0/24`)

### `Verdict`
- `allowed_by_rule` — Passou por estar em Whitelist
- `denied_by_rule` — Bloqueado por estar em Blacklist
- `allowed_by_ai` — IA classificou como benigno
- `denied_by_ai` — IA classificou como aposta

### `ReviewStatus`
- `pending` — Aguardando análise do moderador
- `approved` — Falso positivo confirmado, regra criada
- `rejected` — Rejeição (mantém bloqueio)

---

## Estratégia de Índices para Performance

```sql
-- Buscas de regras em tempo real (crítico para firewall)
CREATE INDEX idx_filtering_rules_target ON filtering_rules(target);
CREATE INDEX idx_filtering_rules_active ON filtering_rules(is_active);

-- Buscas de logs por IP
CREATE INDEX idx_traffic_logs_src_ip ON traffic_logs(source_ip);
CREATE INDEX idx_traffic_logs_dst_ip ON traffic_logs(destination_ip);
CREATE INDEX idx_traffic_logs_verdict ON traffic_logs(verdict);
CREATE INDEX idx_traffic_logs_timestamp ON traffic_logs(timestamp DESC);

-- Buscas de review requests
CREATE INDEX idx_review_requests_status ON review_requests(status);
CREATE INDEX idx_review_requests_created ON review_requests(created_at);
```

---

## Conexão com SQLAlchemy

Veja [`src/engine/database.py`](../src/engine/database.py) para as definições ORM.

**Exemplo de uso:**

```python
from sqlalchemy.orm import Session
from src.engine.database import FilteringRule, SessionLocal

# Inserir regra
db = SessionLocal()
rule = FilteringRule(
    target="bet365.com",
    target_type="domain",
    action="deny",
    reason="Aposta confirmada pela IA",
    created_by=1
)
db.add(rule)
db.commit()
db.close()

# Buscar regra (firewall)
db = SessionLocal()
rule = db.query(FilteringRule).filter_by(target="192.168.1.1").first()
print(f"Ação: {rule.action.value}")  # 'deny' ou 'allow'
```

---

## Próximas Etapas

1. **Issue #42-44:** Implementar CRUD (Create, Read, Update, Delete) para `filtering_rules`.
2. **Issue #44:** CLI de administração para gerenciar regras.
3. **Issue #45:** "Hot Reload" — recarregar regras sem parar o firewall.
4. **Docker Compose:** Adicionar serviço PostgreSQL com volumes persistentes.

---

## Referências

- **RFC 5735**: IPv4 Special-Use Address Blocks
- **IANA**: Port Numbers
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [PostgreSQL Enums](https://www.postgresql.org/docs/current/datatype-enum.html)
