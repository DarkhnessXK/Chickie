from pydantic import BaseModel
from typing import Optional, List


class AvaliacaoDeLoja(BaseModel):

    __tablename__ = "avaliacoes_de_loja"

    usuario_uuid: str
    loja_uuid: str
    nota: int
    descricao: str
    uuid: Optional[str] = None


class AvaliacaoDeProduto(BaseModel):

    __tablename__ = "avaliacoes_de_produtos"

    usuario_uuid: str
    loja_uuid: str
    produto_uuid: str
    nota: int
    descricao: str
    uuid: Optional[str] = None


################


class AvaliacoesDeProduto(BaseModel):
    payload: List[AvaliacaoDeProduto]
    limit: int
    offset: int
    length: int


class AvaliacoesDeLoja(BaseModel):
    payload: List[AvaliacaoDeLoja]
    limit: int
    offset: int
    length: int
