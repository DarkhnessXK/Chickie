from fastapi.security import OAuth2PasswordRequestForm  # noqa
from .connection_dependency import ConnectionDependency  # noqa
from .service_dependencies import (  # noqa
    AuthServiceDependency,  # noqa
    PedidoServiceDependency,
    ProdutoServiceDependency,
    LojaServiceDependency
)
from .token_dependency import TokenDependency  # noqa
from .oauth2_password_request_form_dependency import (  # noqa
    Oauth2PasswordRequestFormDependency  # noqa
)
from .current_loja_dependency import CurrentLojaDependency
