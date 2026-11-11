# Template de API RESTful (FastAPI + SQLite) - Monolito (Projeto A3)

> ✅ **Branch `multicamadas`:** esta branch já contém a refatoração em camadas (`main.py`, `repository.py`, `models.py`, `database.py`). O que foi feito está documentado em **[DOCUMENTACAO.md](DOCUMENTACAO.md)**. Para executar: `uv sync` e depois `uv run uvicorn main:app --reload`.

> 💡 **AVISO IMPORTANTE:** Este repositório contém a estrutura base desenvolvida para o **Projeto A3** em formato **monolítico**. Todo o ciclo de vida da aplicação — conexão com o banco, estruturação de dados e roteamento — está concentrado em um único arquivo (`main.py`). Ao final deste documento, há um guia prático de como evoluir esta base para o **Projeto A4**, adotando uma arquitetura em múltiplas camadas.

Esta é uma API educacional desenvolvida em Python com o framework **FastAPI** e banco de dados relacional **SQLite**. Ela atende aos requisitos iniciais de persistência de dados e documentação automática, servindo como backend para integração com a UC de Usabilidade.

## 🛠 Tecnologias e Pré-requisitos

* **Python 3.8+**
* **uv** (Gerenciador de pacotes e projetos ultrarrápido para Python)
* **FastAPI** (Framework web de alta performance)
* **Uvicorn** (Servidor web ASGI)
* **SQLite** (Banco de dados relacional nativo do Python)

## ⚙️ Como configurar e executar (usando `uv`)

1. Clone este repositório para o seu ambiente local (ou abra no GitHub Codespaces).
2. No terminal, dentro da pasta do projeto, instale o **uv**
```bash
pip install uv
```
3. No terminal, dentro da pasta do projeto, inicialize o ambiente com o **uv** (isso criará o `pyproject.toml` e preparará o ambiente virtual isolado):
   ```bash
   uv init
   ```
4. Adicione as dependências do projeto. O **uv** fará o download e a instalação em frações de segundo:
   ```bash
   uv add fastapi uvicorn
   ```
5. Inicie o servidor local da API utilizando o comando `run` do **uv**:
   ```bash
   uv run uvicorn main:app --reload
   ```
   *(Na primeira execução, o banco de dados será criado automaticamente na mesma pasta).*

6. O servidor estará rodando em: `http://127.0.0.1:8000`

## 📖 Documentação e Testes (Swagger UI)

A API possui documentação interativa gerada automaticamente. Você não precisa de ferramentas externas como Postman ou Insomnia para testar as rotas.

Com o servidor em execução, acesse no navegador:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

## 🚀 Resumo dos Endpoints Disponíveis

A API implementa o CRUD completo. Todos os endpoints estão definidos no arquivo `main.py`:

* **POST `/registros`**: Cria um novo registro no banco (Status `201 Created` ou `400 Bad Request`).
* **GET `/registros`**: Retorna a lista com todos os registros salvos (Status `200 OK`).
* **GET `/registros/{id}`**: Busca os detalhes de um registro específico (Status `200 OK` ou `404 Not Found`).
* **PUT `/registros/{id}`**: Atualiza os dados de um registro existente (Status `200 OK` ou `404 Not Found`).
* **DELETE `/registros/{id}`**: Exclui um registro do banco de dados (Status `200 OK` ou `404 Not Found`).

---

## 🏗️ Guia de Evolução: Do Monolito (A3) para Múltiplas Camadas (A4)

Manter todo o código em um único arquivo (`main.py`) é excelente para o aprendizado inicial e testes rápidos, mas torna a manutenção difícil conforme o sistema cresce. 

Para o **Projeto A4**, o grupo deverá refatorar este monolito em uma **arquitetura de múltiplas camadas**. Siga estes passos para organizar a casa:

1. **Isole o Banco de Dados (`database.py`)**
   * Crie um novo arquivo chamado `database.py`.
   * Mova para ele toda a lógica de conexão com o SQLite (a criação da `engine`, do `cursor` ou a configuração do ORM que estiverem usando) e a função que cria as tabelas iniciais.
   * *Analogia:* Este será o almoxarifado exclusivo do seu sistema.

2. **Separe os Contratos de Dados (`models.py`)**
   * Crie um arquivo `models.py`.
   * Recorte do seu `main.py` todas as classes que herdam de `BaseModel` do Pydantic (como `RegistroCreate`, `RegistroResponse`, etc.) e cole neste novo arquivo.
   * *Analogia:* Este arquivo será o setor de controle de qualidade, ditando o que pode entrar ou sair do sistema.

3. **Limpe as Rotas (`main.py`)**
   * O seu `main.py` agora deve ficar muito mais limpo.
   * Mantenha apenas a inicialização do FastAPI (`app = FastAPI()`) e as funções de rota (os `@app.get`, `@app.post`, etc.).
   * No topo do `main.py`, importe os módulos que você acabou de criar:
     ```python
     from database import conectar_banco, criar_tabelas
     from models import RegistroCreate, RegistroResponse
     ```

Após essa divisão, seu código estará preparado para escalar, integrando facilmente novas funcionalidades de segurança, como um proxy reverso Nginx, de forma totalmente estruturada e profissional.
