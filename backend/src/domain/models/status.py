from pydantic import BaseModel
from typing import Optional, List


class Status(BaseModel):
    __tablename__ = "status"

    nome: str
    loja_uuid: str

    descricao: Optional[str] = None
    uuid: Optional[str] = None


#######


class StatusList(BaseModel):
    payload: List[Status]
    limit: int
    offset: int
    length: int
