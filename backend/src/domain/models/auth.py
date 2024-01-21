from pydantic import BaseModel
from src.domain.models import EnderecoUsuario, LojaGET


class UserAuthData(BaseModel):
    access_token: str
    token_type: str
    nome: str
    username: str
    email: str
    endereco: EnderecoUsuario
    celular: str | None = None
    uuid: str | None = None


class LojaAuthData(BaseModel):
    access_token: str
    token_type: str
    loja: LojaGET | None = None
