from pydantic import BaseModel
from typing import Optional, List


class EnderecoLoja(BaseModel):
    __tablename__ = "enderecos_lojas"
    uf: str
    cidade: str
    logradouro: str
    numero: str
    bairro: str
    loja_uuid: str

    cep: Optional[str] = None
    complemento: Optional[str] = None
    uuid: Optional[str] = None


class EnderecoUsuario(BaseModel):
    __tablename__ = "enderecos_usuarios"
    uf: str
    cidade: str
    logradouro: str
    numero: str
    bairro: str
    usuario_uuid: str

    cep: Optional[str] = None
    complemento: Optional[str] = None
    uuid: Optional[str] = None


class EnderecoEntrega(BaseModel):
    __tablename__ = "enderecos_entregas"
    uf: str
    cidade: str
    logradouro: str
    numero: str
    bairro: str

    cep: Optional[str] = None
    complemento: Optional[str] = None
    uuid: Optional[str] = None
    pedido_uuid: Optional[str] = None


###########

class EnderecosLoja(BaseModel):
    payload: List[EnderecoLoja]
    limit: int
    offset: int
    length: int


class EnderecosEntrega(BaseModel):
    payload: List[EnderecoEntrega]
    limit: int
    offset: int
    length: int


class EnderecosUsuario(BaseModel):
    payload: List[EnderecoUsuario]
    limit: int
    offset: int
    length: int
