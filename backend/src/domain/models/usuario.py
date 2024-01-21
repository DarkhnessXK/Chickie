from pydantic import BaseModel
from typing import Optional, List
from .endereco import EnderecoUsuario
import base64
import bcrypt


class UsuarioFollowEmpresaRequest(BaseModel):
    usuario_uuid: str
    loja_uuid: str
    follow: bool


class Usuario(BaseModel):

    __tablename__ = "usuarios"
    nome: str
    username: str
    email: str
    celular: str

    modo_de_cadastro: str

    telefone: Optional[str] = None
    password: Optional[str] = None
    password_hash: Optional[str] = None
    uuid: Optional[str] = None
    ativo: Optional[bool] = True
    passou_pelo_primeiro_acesso: Optional[bool] = False

    def authenticate(self, senha_usuario: str) -> bool:
        """
        Autentica a senha do usuário comparando-a com o hash armazenado.

        Args:
            senha_usuario (str): A senha fornecida pelo usuário.

        Returns:
            bool: True se a senha estiver correta, False caso contrário.
        """
        if self.password_hash is None:
            raise
        hash_bytes = base64.b64decode(self.password_hash.encode("utf-8"))
        return bcrypt.checkpw(senha_usuario.encode("utf-8"), hash_bytes)


class UsuarioGET(BaseModel):

    __tablename__ = "usuarios"
    nome: str
    username: str
    email: str
    celular: str

    modo_de_cadastro: str

    endereco: Optional[EnderecoUsuario] = None
    telefone: Optional[str] = None
    uuid: Optional[str] = None


class Usuarios(BaseModel):
    payload: List[Usuario]
    limit: int
    offset: int
    length: int
