import httpx
import json
from src.domain.models import Produto
from contextlib import suppress


with suppress(ModuleNotFoundError, ImportError):
    from src.qt.windows import MainWindow  # noqa


class ProdutosModel:
    def __init__(self, window: "MainWindow"):
        self.window = window
        self.loja_uuid = window.loja_uuid
        self.token = window.token
        self.data = self.getData()
        self.nomes = [item.nome for item in self.data]

    def refresh(self):
        self.data = self.getData()

    def getFromNome(self, nome: str):
        for item in self.data:
            if item.nome == nome:
                return item

    def getData(self):
        response = httpx.get(
            "http://localhost:8000/produtos/",
            headers={"Authorization": f"Bearer {self.token}"},
            params={"loja_uuid": self.loja_uuid},
        )
        responseJson = json.loads(response.text)
        return [Produto(**produtoData) for produtoData in responseJson]
