from fastapi.testclient import TestClient
from config import settings as s
from src.domain.models import Loja
from faker import Faker

f = Faker()

categoria_nome = f.word()


def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_loja(loja: Loja):
    assert loja.nome == s.LOJA_NOME


def test_loja_login(client: TestClient):
    response = client.post(
        "/loja/login",
        data={"username": s.LOJA_USERNAME, "password": s.LOJA_SENHA},
    )

    assert response.status_code == 200
