from pydantic import BaseModel
from typing import Optional, List


class MetodoDePagamento(BaseModel):
    __tablename__ = "metodos_pagamento"
    loja_uuid: str
    nome: str
    descricao: Optional[str] = None
    uuid: Optional[str] = None


#################


class MetodosDePagamento(BaseModel):
    payload: List[MetodoDePagamento]
    limit: int
    offset: int
    length: int
