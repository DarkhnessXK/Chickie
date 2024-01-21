from src.infra.database_postgres.repository import Repository
from src.domain.models import (
    Preco,
    Loja,
    Usuario,
    AvaliacaoDeLoja,
)
from aiopg.connection import Connection
from typing import Optional
from .base import BaseService
from src.misc import Paginador
from typing import TypedDict, List, Any


class PaginateOptions(TypedDict):
    limit: int
    offset: int
    payload: List[Any]


class AvaliacaoDeLojaService(BaseService):
    def __init__(
        self,
        connection: Connection,
        loja: Optional[Loja] = None
    ):
        self.model = AvaliacaoDeLoja
        self.connection = connection
        self.repo = Repository(
            model=self.model, connection=self.connection
        )
        self.user_repo = Repository(
            model=Usuario, connection=self.connection
        )
        self.preco_repo = Repository(
            model=Preco, connection=self.connection
        )
        self.loja_repo = Repository(
            model=Loja, connection=self.connection
        )
        self.loja = loja

    async def avaliacao_de_loja(self, loja: Loja) -> Optional[dict]:
        sql = """
        SELECT AVG(nota) AS media_avaliacao
        FROM Avaliacoes
        WHERE empresa_uuid = %s;
        """
        result = await self.repo.execute_and_fetch_one(sql, (loja.uuid,))
        return result

    async def buscar_lojas_por_avaliacao_acima_de(
        self,
        nota: int,
        pag_data: PaginateOptions
    ):
        avaliacoes = await self.buscar_avaliacoes_de_loja_acima_de(nota)

        lojas = []
        for avaliacao in avaliacoes:
            loja = await self.get_loja(avaliacao)
            lojas.append(loja)

        paginador = Paginador(
            data=lojas,
            offset=pag_data['offset'],
            limit=pag_data['limit']
        )
        return paginador.get_response()

    async def buscar_avaliacoes_de_loja_acima_de(
        self,
        nota: int,
    ):
        sql = """
        SELECT * FROM Avaliacoes
        GROUP BY empresa_uuid
        HAVING AVG(nota) > %s;
        """
        results = await self.repo.execute_and_fetch_all(sql, (nota,))
        avaliacoes = [
            AvaliacaoDeLoja(**result) for result in results
        ]

        [print(avaliacao) for avaliacao in avaliacoes]

        return avaliacoes

    async def get_loja(self, avaliacao: AvaliacaoDeLoja) -> Optional[Loja]:
        loja = await self.loja_repo.find_one(
            uuid=avaliacao.loja_uuid
        )
        if loja is None:
            raise

        return loja
