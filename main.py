"""Camada de rotas: inicialização do FastAPI e endpoints HTTP."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

import repository
from database import criar_tabelas
from models import RegistroCreate, RegistroResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria a tabela automaticamente ao iniciar a API
    criar_tabelas()
    yield


app = FastAPI(
    title="API de Gerenciamento - Projeto A4 (Multicamadas)",
    description="FastAPI + SQLite organizada em camadas: rotas, repositório, modelos e banco.",
    version="2.0.0",
    lifespan=lifespan,
)


def validar_titulo(registro: RegistroCreate):
    # Requisito 5: Código 400 (Bad Request) para regra de negócio inválida
    if not registro.titulo.strip():
        raise HTTPException(status_code=400, detail="O título não pode estar em branco.")


@app.post("/registros", response_model=RegistroResponse, status_code=201)
def criar_registro(registro: RegistroCreate):
    validar_titulo(registro)
    try:
        return repository.criar(registro)
    except Exception as e:
        # Requisito 5: Código 500 (Internal Server Error)
        raise HTTPException(status_code=500, detail=f"Erro interno no banco de dados: {str(e)}")


@app.get("/registros", response_model=list[RegistroResponse], status_code=200)
def listar_registros():
    return repository.listar()


@app.get("/registros/{registro_id}", response_model=RegistroResponse, status_code=200)
def buscar_registro(registro_id: int):
    registro = repository.buscar_por_id(registro_id)
    if registro is None:
        # Requisito 5: Código 404 (Not Found)
        raise HTTPException(status_code=404, detail="Registro não encontrado.")
    return registro


@app.put("/registros/{registro_id}", response_model=RegistroResponse, status_code=200)
def atualizar_registro(registro_id: int, registro: RegistroCreate):
    validar_titulo(registro)
    if repository.buscar_por_id(registro_id) is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado para atualização.")
    try:
        return repository.atualizar(registro_id, registro)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")


@app.delete("/registros/{registro_id}", status_code=200)
def deletar_registro(registro_id: int):
    if repository.buscar_por_id(registro_id) is None:
        raise HTTPException(status_code=404, detail="Registro não encontrado para exclusão.")
    repository.deletar(registro_id)
    return {"mensagem": "Registro removido com sucesso."}
