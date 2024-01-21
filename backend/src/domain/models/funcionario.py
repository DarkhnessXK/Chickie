from pydantic import BaseModel
from typing import Optional, List


class Funcionario(BaseModel):
    __tablename__ = "funcionarios"
    loja_uuid: str
    cargo: str
    nome: str
    username: str
    email: str
    celular: str

    password_hash: Optional[str] = None
    telefone: Optional[str] = None
    password: Optional[str] = None
    uuid: Optional[str] = None


###############


class Funcionarios(BaseModel):
    payload: List[Funcionario]
    limit: int
    offset: int
    length: int
