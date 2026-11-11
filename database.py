"""Camada de banco de dados: conexão com o SQLite e criação das tabelas."""
import sqlite3

DB_PATH = "banco_a3.db"


def conectar_banco():
    """Abre uma conexão com o banco (o arquivo é criado se não existir)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn


def criar_tabelas():
    """Cria as tabelas iniciais caso ainda não existam."""
    conn = conectar_banco()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            ativo BOOLEAN DEFAULT TRUE
        )
    ''')
    conn.commit()
    conn.close()
