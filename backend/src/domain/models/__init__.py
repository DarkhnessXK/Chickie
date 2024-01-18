from .endereco import EnderecoUsuario, EnderecoEntrega, EnderecoLoja  # noqa
from .status import Status  # noqa
from .categoria import CategoriaProdutos  # noqa
from .item_pedido import ItemPedido, ItemPedidoPOST  # noqa
from .login import Login  # noqa
from .loja import Loja, LojaGET, LojaPUT  # noqa
from .pedido import Pedido, PedidoGET, PedidoPOST, AlterarStatusPedidoPATCH   # noqa
from .preco import Preco  # noqa
from .produto import Produto, ProdutoGET, ProdutoPOST, ProdutoPUT  # noqa
from .signup import UsuarioSignUp, LojaSignUp  # noqa
from .auth import UserAuthData, LojaAuthData, LojaGET  # noqa
from .usuario import Usuario, UsuarioFollowEmpresaRequest  # noqa
from .entregador import Entregador  # noqa
from .avaliacao import AvaliacaoDeProduto, AvaliacaoDeLoja  # noqa
from .funcionario import Funcionario  # noqa
from .metodo_de_pagamento import MetodoDePagamento  # noqa
from .pagamento import Pagamento  # noqa
from .zona_de_entrega import ZonaDeEntrega  # noqa
from .cliente import Cliente, ClientePOST  # noqa
from .imagem_cadastro import LojaUpdateImageCadastro  # noqa
