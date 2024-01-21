from pydantic import BaseModel
from typing import Optional, List


class Pagamento(BaseModel):
    __tablename__ = "pagamentos"
    pedido_uuid: str
    metodo_pagamento_uuid: str
    uuid: Optional[str] = None


##################


class Pagamentos(BaseModel):
    payload: List[Pagamento]
    limit: int
    offset: int
    length: int
