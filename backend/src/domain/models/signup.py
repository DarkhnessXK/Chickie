from pydantic import BaseModel
from typing import Optional


class UsuarioSignUp(BaseModel):

    nome: str
    username: str
    email: str
    celular: str
    password: str

    bairro: str
    cep: str
    cidade: str
    complemento: str
    logradouro: str
    numero: str
    uf: str

    modo_de_cadastro: str

    telefone: Optional[str] = None


class LojaSignUp(BaseModel):
    nome: str
    username: str
    email: str
    telefone: str
    celular: str
    password: str

    uf: str
    cep: str
    cidade: str
    logradouro: str
    bairro: str
    numero: str
    complemento: str

    horarios_de_funcionamento: Optional[str] = None
    image_filename: str | None = None
    image_bytes: str | None = None  # base64 string
