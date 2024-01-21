from .endereco import (  # noqa
    EnderecoUsuario,
    EnderecoEntrega,
    EnderecoLoja,
    EnderecosLoja,
    EnderecosEntrega,
    EnderecosUsuario
)
from .status import Status, StatusList  # noqa
from .categoria import CategoriaProdutos, CategoriasProdutos  # noqa
from .item_pedido import ItemPedido, ItemPedidoPOST  # noqa
from .login import Login  # noqa
from .loja import Loja, Lojas, LojaGET, LojaPUT  # noqa
from .pedido import (  # noqa
    Pedido,
    PedidoGET,
    PedidoPOST,
    Pedidos,
    AlterarStatusPedidoPATCH
)
from .preco import Preco, Precos  # noqa
from .produto import (  # noqa
    Produto,
    ProdutoGET,
    Produtos,
    ProdutoPOST,
    ProdutoPUT
)
from .signup import UsuarioSignUp, LojaSignUp  # noqa
from .auth import UserAuthData, LojaAuthData, LojaGET  # noqa
from .usuario import Usuario, Usuarios, UsuarioGET, UsuarioFollowEmpresaRequest  # noqa
from .entregador import Entregador, Entregadores  # noqa
from .avaliacao import (  # noqa
    AvaliacaoDeProduto,
    AvaliacaoDeLoja,
    AvaliacoesDeProduto,
    AvaliacoesDeLoja
)
from .funcionario import Funcionario, Funcionarios  # noqa
from .metodo_de_pagamento import MetodoDePagamento, MetodosDePagamento  # noqa
from .pagamento import Pagamento, Pagamentos  # noqa
from .zona_de_entrega import ZonaDeEntrega, ZonasDeEntrega  # noqa
from .cliente import Cliente, ClientePOST  # noqa
from .imagem_cadastro import LojaUpdateImageCadastro  # noqa
