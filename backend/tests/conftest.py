from config import settings as s
from fastapi.testclient import TestClient  # noqa
from src.domain.models import Loja  # noqa
import json  # noqa
import pytest  # noqa
import sys  # noqa
from src import create_app  # noqa


@pytest.fixture
def client():
    app = create_app(sys.argv)
    client = TestClient(app)
    return client


@pytest.fixture
def loja_uuid(client: TestClient):
    data = {"username": s.LOJA_USERNAME, "password": s.LOJA_SENHA}
    response = client.post("/loja/login", data=data)
    return json.loads(response.text)["uuid"]


@pytest.fixture
def loja(loja_uuid: str, client: TestClient):
    response = client.get(f"/loja/{loja_uuid}")
    return Loja(**json.loads(response.text))


@pytest.fixture
def access_token(client: TestClient):
    response = client.post(
        "/loja/login",
        data={"username": s.LOJA_USERNAME, "password": s.LOJA_SENHA},
    )
    return json.loads(response.text)["access_token"]
