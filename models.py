"""Camada de modelos: contratos de dados (Pydantic) de entrada e saída da API."""
from pydantic import BaseModel


class RegistroBase(BaseModel):
    titulo: str
    descricao: str | None = None
    ativo: bool = True


class RegistroCreate(RegistroBase):
    """Dados aceitos ao criar ou atualizar um registro."""


class RegistroResponse(RegistroBase):
    """Dados devolvidos pela API (inclui o id gerado pelo banco)."""
    id: int
