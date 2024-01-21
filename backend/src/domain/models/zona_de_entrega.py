from pydantic import BaseModel
from typing import Optional, List


class ZonaDeEntrega(BaseModel):
    __tablename__ = "zonas_de_entrega"

    cidade: str
    uf: str

    taxa_de_entrega: float
    loja_uuid: str

    bairro: Optional[str] = None
    uuid: Optional[str] = None


#######################


class ZonasDeEntrega(BaseModel):
    payload: List[ZonaDeEntrega]
    limit: int
    offset: int
    length: int
