from src.presenters.models.http import HTTPResponse
from src.infra.database import repositories as r


def handle(data: dict):

    loja_uuid = data.get('loja_uuid')
    if loja_uuid:
        precos = r.PrecoRepository.find_all(loja_uuid=loja_uuid)
        return HTTPResponse(body=precos)

    return HTTPResponse()
