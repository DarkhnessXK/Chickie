from fastapi import FastAPI
from . import (  # noqa
    info,
    categorias,
    # entregadores,
    # funcionarios,
    # metodos_de_pagamento,
    # pagamentos,
    # avaliacoes_de_lojas,
    # avaliacoes_de_produtos,
    pedidos,
    precos,
    produtos,
    status,
    usuario,
    loja
)
# from . import (  # noqa
#     zona_de_entrega,
# )


def init_app(app: FastAPI) -> None:
    app.include_router(usuario.router)
    app.include_router(loja.router)
    app.include_router(pedidos.router)
    app.include_router(precos.router)
    app.include_router(produtos.router)
    app.include_router(categorias.router)
    # router.include_router(entregadores.router)
    # router.include_router(avaliacoes_de_lojas.router)
    # router.include_router(avaliacoes_de_produtos.router)
    # router.include_router(funcionarios.router)
    # router.include_router(metodos_de_pagamento.router)
    # router.include_router(pagamentos.router)
    # router.include_router(zona_de_entrega.router)
    app.include_router(status.router)
    info.init_app(app)
