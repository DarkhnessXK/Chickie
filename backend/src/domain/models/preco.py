from pydantic import BaseModel
from typing import Optional, List


class Preco(BaseModel):
    __tablename__ = "precos"
    produto_uuid: str
    valor: float
    dia_da_semana: str
    uuid: Optional[str] = None


####################


class Precos(BaseModel):
    payload: List[Preco]
    limit: int
    offset: int
    length: int
