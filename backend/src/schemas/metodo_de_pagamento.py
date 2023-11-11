from pydantic import BaseModel
from typing import Optional


class MetodoDePagamento(BaseModel):
    __tablename__ = "metodos_pagamento"
    loja_uuid: str
    nome: str
    descricao: str
    uuid: Optional[str] = None

    class Config:
        json_schema_extra = {
            'example': {
                'loja_uuid': 'str',
                'nome': 'str',
                'descricao': 'str'
            }
        }
