from typing import Annotated
from src.domain.services import LojaService, ProdutoService, PedidoService
from src.api.security import AuthService
from fastapi import Depends


from .connection_dependency import ConnectionDependency  # noqa


def get_auth_service(connection: ConnectionDependency):
    return AuthService(connection)


def get_loja_service(connection: ConnectionDependency):
    return LojaService(connection)


def get_produto_service(connection: ConnectionDependency):
    return ProdutoService(connection)


def get_pedido_service(connection: ConnectionDependency):
    return PedidoService(connection)


AuthServiceDependency = Annotated[
    AuthService, Depends(get_auth_service)
]

PedidoServiceDependency = Annotated[
    PedidoService, Depends(get_pedido_service)
]

ProdutoServiceDependency = Annotated[
    ProdutoService, Depends(get_produto_service)
]

LojaServiceDependency = Annotated[
    LojaService, Depends(get_loja_service)
]
