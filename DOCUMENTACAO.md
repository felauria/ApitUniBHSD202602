# Documentação das modificações — branch `multicamadas`

## 1. Fork e execução do código original (branch `main`)

1. Fork do repositório `fvaladares/ApitUniBHSD202602` e clone local.
2. Ao seguir o README, dois problemas impediram a execução direta:
   - **`uvicorn` não estava no `pyproject.toml`.** Correção: `uv add uvicorn`.
   - **O README manda rodar `main:app`, mas o arquivo se chamava `App.py`.** No original é preciso usar `uv run uvicorn App:app --reload`.
3. O passo `uv init` do README não é necessário porque o `pyproject.toml` já existe.
4. Com isso a API subiu e o CRUD funcionou pelo Swagger (`/docs`).

## 2. Refatoração para multicamadas (branch `multicamadas`)

Criada a branch `multicamadas` a partir da `main`. O `App.py` monolítico foi dividido em 4 arquivos:

| Arquivo | Camada | Conteúdo |
|---|---|---|
| `database.py` | Banco de dados | `conectar_banco()` (conexão SQLite) e `criar_tabelas()` |
| `models.py` | Modelos | Classes Pydantic `RegistroBase`, `RegistroCreate`, `RegistroResponse` |
| `repository.py` | Acesso a dados | Todo o SQL do CRUD: `listar`, `buscar_por_id`, `criar`, `atualizar`, `deletar` |
| `main.py` | Rotas | `app = FastAPI()` e os endpoints. Não contém SQL; só chama o `repository` |

Fluxo de uma requisição: `main.py` (rota) → `repository.py` (SQL) → `database.py` (conexão).
Os dados de entrada e saída são validados por `models.py`.

O `App.py` foi substituído pelo `main.py`, que é o nome usado no README, então o comando `uvicorn main:app` passou a funcionar.

## 3. Ajustes adicionais

- **`uvicorn` adicionado ao `pyproject.toml`.** O `uv.lock` não é versionado; o `uv sync` gera esse arquivo automaticamente.
- **`@app.on_event("startup")` foi trocado por `lifespan`.** É a forma atual recomendada pelo FastAPI; a anterior está obsoleta.
- **Validação de título vazio (400) também no `PUT`.** Antes ela só existia no `POST`, e o `PUT` aceitava título em branco.
- **`.gitignore` criado** para não versionar `banco_a3.db`, `__pycache__/`, `.venv/` e `uv.lock`.

## 4. Como executar

```bash
pip install uv
uv sync
uv run uvicorn main:app --reload
```

Swagger: http://127.0.0.1:8000/docs

## 5. Testes realizados

Todos os endpoints foram testados com a API rodando:

| Requisição | Resultado esperado | Obtido |
|---|---|---|
| `POST /registros` válido | 201 | ✅ 201 |
| `POST /registros` com título vazio | 400 | ✅ 400 |
| `GET /registros` | 200 + lista | ✅ 200 |
| `GET /registros/1` | 200 | ✅ 200 |
| `GET /registros/99` (inexistente) | 404 | ✅ 404 |
| `PUT /registros/1` | 200 | ✅ 200 |
| `PUT /registros/99` | 404 | ✅ 404 |
| `PUT /registros/1` com título vazio | 400 | ✅ 400 |
| `DELETE /registros/1` | 200 | ✅ 200 |
| `DELETE /registros/1` de novo | 404 | ✅ 404 |
| `GET /docs` | 200 | ✅ 200 |
