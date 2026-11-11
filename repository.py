"""Camada de acesso a dados: todas as consultas SQL da entidade Registro.

As rotas não escrevem SQL; elas chamam estas funções.
"""
from database import conectar_banco
from models import RegistroCreate


def listar() -> list[dict]:
    conn = conectar_banco()
    linhas = conn.execute("SELECT * FROM registros").fetchall()
    conn.close()
    return [dict(linha) for linha in linhas]


def buscar_por_id(registro_id: int) -> dict | None:
    conn = conectar_banco()
    linha = conn.execute("SELECT * FROM registros WHERE id = ?", (registro_id,)).fetchone()
    conn.close()
    return dict(linha) if linha else None


def criar(registro: RegistroCreate) -> dict:
    conn = conectar_banco()
    cursor = conn.execute(
        "INSERT INTO registros (titulo, descricao, ativo) VALUES (?, ?, ?)",
        (registro.titulo, registro.descricao, registro.ativo),
    )
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()
    return {**registro.model_dump(), "id": novo_id}


def atualizar(registro_id: int, registro: RegistroCreate) -> dict:
    conn = conectar_banco()
    conn.execute(
        "UPDATE registros SET titulo = ?, descricao = ?, ativo = ? WHERE id = ?",
        (registro.titulo, registro.descricao, registro.ativo, registro_id),
    )
    conn.commit()
    conn.close()
    return {**registro.model_dump(), "id": registro_id}


def deletar(registro_id: int) -> None:
    conn = conectar_banco()
    conn.execute("DELETE FROM registros WHERE id = ?", (registro_id,))
    conn.commit()
    conn.close()
