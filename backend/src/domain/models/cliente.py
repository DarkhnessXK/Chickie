from pydantic import BaseModel
from typing import Optional


class Cliente(BaseModel):
    __tablename__ = "clientes"

    usuario_uuid: str
    loja_uuid: str
    uuid: Optional[str] = None


class ClientePOST(BaseModel):
    __tablename__ = "clientes"

    usuario_uuid: str
    loja_uuid: str
