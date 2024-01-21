from typing import Annotated
from src.exceptions import NotFoundException
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Request,
    Query
)
from src.domain.models import AvaliacaoDeLoja
from src.infra.database_postgres.repository import Repository
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/avaliacoes_loja", tags=["Avaliações de Lojas"])


@router.get("/")
async def requisitar_avaliacoes_loja(
    connection: ConnectionDependency,
    limit: int = Query(0),
    offset: int = Query(1),
):

    repository = Repository(AvaliacaoDeLoja, connection=connection)
    results = await repository.find_all()

    return results


@router.get("/{uuid}")
async def requisitar_avaliacao_loja(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid da avaliação fazer get")]
):

    repository = Repository(AvaliacaoDeLoja, connection=connection)
    result = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("avaliacoes_lojanão encontrado")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_avaliacao_loja(
    connection: ConnectionDependency,
    avaliacao: AvaliacaoDeLoja,
):

    repository = Repository(AvaliacaoDeLoja, connection=connection)
    try:
        uuid = await repository.save(avaliacao)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_avaliacao_loja_put(
    connection: ConnectionDependency,
    avaliacao_loja_data: AvaliacaoDeLoja,
    uuid: Annotated[str, Path(title="O uuid do avaliacoes_lojaa fazer put")],
):

    repository = Repository(AvaliacaoDeLoja, connection=connection)
    avaliacao = await repository.find_one(uuid=uuid)
    if avaliacao is None:
        raise NotFoundException("Avaliacao de Loja não encontrada")

    num_rows_affected = await repository.update(
        avaliacao, avaliacao_loja_data.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_avaliacoes_loja_patch(
    connection: ConnectionDependency,
    avaliacoes_loja_data: AvaliacaoDeLoja,
    uuid: Annotated[str, Path(title="O uuid do avaliacoes_lojaa fazer patch")],
):

    repository = Repository(AvaliacaoDeLoja, connection=connection)
    avaliacao = await repository.find_one(uuid=uuid)
    if avaliacao is None:
        raise NotFoundException("Avaliação encontrada")

    num_rows_affected = await repository.update(
        avaliacao, avaliacoes_loja_data.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_avaliacoes_loja(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid do avaliacoes_lojaa fazer delete")]
):

    repository = Repository(AvaliacaoDeLoja, connection=connection)
    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
