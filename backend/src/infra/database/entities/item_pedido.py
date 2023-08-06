from src.infra.database.entities import Base
from sqlalchemy.schema import Column as Col, ForeignKey as FK
from sqlalchemy.types import Integer as Int, Float, String as Str


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    quantidade = Col(Int)
    subtotal = Col(Float)
    produto_uuid = Col(Str(36), FK("produtos.uuid"))
    pedido_uuid = Col(Str(36), FK("pedidos.uuid"))
    loja_uuid = Col(Str(36), FK("lojas.uuid"))
