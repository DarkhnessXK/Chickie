from pydantic import BaseModel
from typing import Optional, List


class CategoriaProdutos(BaseModel):
    __tablename__ = "categorias_de_produtos"
    nome: str
    descricao: str
    loja_uuid: str

    uuid: Optional[str] = None


class CategoriasProdutos(BaseModel):
    payload: List[CategoriaProdutos]
    limit: int
    offset: int
    length: int
