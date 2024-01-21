from pydantic import BaseModel
from typing import Optional


class ItemPedido(BaseModel):
    __tablename__ = "itens_pedido"
    quantidade: int
    observacoes: str
    pedido_uuid: str
    loja_uuid: str
    produto_nome: str
    produto_descricao: str
    valor: float
    uuid: Optional[str] = None


class ItemPedidoPOST(BaseModel):
    quantidade: int
    observacoes: str
    produto_uuid: str
    pedido_uuid: Optional[str] = None
    loja_uuid: Optional[str] = None
    valor: Optional[float] = 0
