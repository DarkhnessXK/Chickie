from pydantic import BaseModel
from src.domain.models import Status, EnderecoEntrega
from typing import Optional, List, Annotated
from .item_pedido import ItemPedido, ItemPedidoPOST
from datetime import datetime


isodatetime = Annotated[str, 'isotime']


class Pedido(BaseModel):
    __tablename__ = "pedidos"

    celular: str
    data_hora: isodatetime | datetime
    loja_uuid: str
    frete: float
    concluido: bool
    comentarios: str

    status_uuid: Optional[str] = None
    usuario_uuid: Optional[str] = None
    uuid: Optional[str] = None


class PedidoGET(BaseModel):
    __tablename__ = "pedidos"
    data_hora: isodatetime | datetime
    frete: float
    loja_uuid: str
    celular: str
    total: float
    comentarios: str
    usuario_uuid: Optional[str] = None
    uuid: Optional[str] = None
    status_uuid: Optional[str] = None
    status: Optional[Status] = None
    endereco: Optional[EnderecoEntrega] = None
    itens: List[ItemPedido] = []
    concluido: Optional[bool] = None


class Pedidos(BaseModel):
    __tablename__ = "pedidos"
    payload: List[PedidoGET]
    limit: int
    offset: int
    length: int


class PedidoPOST(BaseModel):

    celular: str
    data_hora: isodatetime
    endereco: EnderecoEntrega
    frete: float
    itens: List[ItemPedidoPOST]
    loja_uuid: str
    comentarios: str
    usuario_uuid: Optional[str] = None
    status_uuid: Optional[str] = None


class AlterarStatusPedidoPATCH(BaseModel):
    status_uuid: str
