from src.infra.database.entities import Base
from sqlalchemy.schema import Column as Col
import enum
from sqlalchemy.types import String as Str, Text, Enum


class UF(enum.Enum):
    AC = "Acre"
    AL = "Alagoas"
    AP = "Amapá"
    AM = "Amazonas"
    BA = "Bahia"
    CE = "Ceará"
    DF = "Distrito Federal"
    ES = "Espírito Santo"
    GO = "Goiás"
    MA = "Maranhão"
    MT = "Mato Grosso"
    MS = "Mato Grosso do Sul"
    MG = "Minas Gerais"
    PA = "Pará"
    PB = "Paraíba"
    PR = "Paraná"
    PE = "Pernambuco"
    PI = "Piauí"
    RJ = "Rio de Janeiro"
    RN = "Rio Grande do Norte"
    RS = "Rio Grande do Sul"
    RO = "Rondônia"
    RR = "Roraima"
    SC = "Santa Catarina"
    SP = "São Paulo"
    SE = "Sergipe"
    TO = "Tocantins"


class Endereco(Base):
    __tablename__ = "enderecos"
    uuid = Col(Str(36), unique=True, primary_key=True)
    uf = Col(Enum(UF))  # type: ignore
    cidade = Col(Text, nullable=False)
    logradouro = Col(Text, nullable=False)
    numero = Col(Text)
    complemento = Col(Text)
    bairro = Col(Text, nullable=False)
    cep = Col(Text)
