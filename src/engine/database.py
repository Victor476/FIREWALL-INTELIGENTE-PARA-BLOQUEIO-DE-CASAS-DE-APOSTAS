import sqlite3
import os
from pathlib import Path

# Configura o caminho do DB para a pasta volumes montada no docker
DB_DIR = Path(__file__).resolve().parent.parent.parent / "volumes" / "db"
DB_PATH = DB_DIR / "firewall.db"

def init_db():
    \"\"\"Inicializa o banco de dados e cria as tabelas necessárias se não existirem.\"\"\"
    # Garante que o diretório existe
    DB_DIR.mkdir(parents=True, exist_ok=True)
    
    # Conecta (ou cria) o banco
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Tabela 1: Whitelist (Domínios e IPs permitidos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_domain TEXT UNIQUE NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            reason TEXT
        )
    ''')
    
    # Tabela 2: Blacklist (Domínios e IPs bloqueados manualmente ou pela IA)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blacklist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_domain TEXT UNIQUE NOT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT -- ex: 'MANUAL', 'AI_ENGINE'
        )
    ''')
    
    # Tabela 3: Logs de Auditoria e Vereditos (Atende RNF08/RNF07)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_ip TEXT NOT NULL,
            target_domain TEXT NOT NULL,
            votes TEXT, -- Guardará distribuição. Ex: '[1, 1, 0]'
            action TEXT NOT NULL -- Ex: 'DROP', 'ALLOW'
        )
    ''')
    
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    init_db()
    print(f"Banco de dados inicializado com sucesso em: {DB_PATH}")
