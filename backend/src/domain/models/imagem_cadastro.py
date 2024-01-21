from pydantic import BaseModel


class LojaUpdateImageCadastro(BaseModel):
    bytes_base64: str
    filename: str
