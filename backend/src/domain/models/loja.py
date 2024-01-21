from pydantic import BaseModel
from typing import Optional, List
from src.domain.models import EnderecoLoja
import base64
import bcrypt


class LojaGET(BaseModel):
    __tablename__ = "lojas"
    nome: str
    username: str
    email: str
    celular: str
    uuid: str
    endereco: EnderecoLoja
    telefone: Optional[str] = None
    imagem_cadastro: Optional[str] = None
    horarios_de_funcionamento: Optional[str] = None


class Lojas(BaseModel):
    __tablename__ = "lojas"
    limit: int
    offset: int
    payload: List[LojaGET]
    length: int


class Loja(BaseModel):
    __tablename__ = "lojas"
    nome: str
    username: str
    email: str
    celular: str
    password_hash: str

    telefone: Optional[str] = None
    password: Optional[str] = None
    uuid: Optional[str] = None
    ativo: Optional[bool] = True
    passou_pelo_primeiro_acesso: Optional[bool] = False
    horarios_de_funcionamento: Optional[str] = None

    def authenticate(self, senha_loja: str) -> bool:
        if self.password_hash is None:
            raise

        hash_bytes = base64.b64decode(self.password_hash.encode("utf-8"))
        return bcrypt.checkpw(senha_loja.encode("utf-8"), hash_bytes)


class LojaPUT(BaseModel):

    email: str
    telefone: str
    celular: str

    nome: str
    username: str

    uf: str
    cep: str
    cidade: str
    logradouro: str
    bairro: str
    numero: str
    complemento: str

    horarios_de_funcionamento: Optional[str] = None
