from pydantic import BaseModel
from typing import Optional


class Entregador(BaseModel):
    __tablename__ = "entregadores"
    nome: str
    celular: str
    veiculo: str
    placa_veiculo: str
    loja_uuid: str

    telefone: Optional[str] = None
    email: Optional[str] = None
    uuid: Optional[str] = None
