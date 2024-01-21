from typing import Annotated, List, Dict, Optional
from src.infra.database_postgres.repository import Repository
from src.exceptions import NotFoundException
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Request,
    Query,
    Depends
)
from src.domain.models import AvaliacaoDeProduto
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(
    prefix="/avaliacoes-de-produtos",
    tags=["Avaliações de produtos"]
)


@router.get("/")
async def requisitar_avaliacoes(
    connection: ConnectionDependency,
    limit: int = Query(0),
    offset: int = Query(1),
) -> List[AvaliacaoDeProduto]:

    repository = Repository(AvaliacaoDeProduto, connection)
    results: List[AvaliacaoDeProduto] = await repository.find_all()

    return results


@router.get("/{uuid}")
async def requisitar_avaliacao(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid da avaliação a fazer get")]
) -> AvaliacaoDeProduto:

    repository = Repository(AvaliacaoDeProduto, connection)

    result: Optional[AvaliacaoDeProduto] = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Avaliação não encontrada")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_avaliacoes(
    connection: ConnectionDependency,
    avaliacao: AvaliacaoDeProduto
) -> Dict[str, str]:

    repository = Repository(AvaliacaoDeProduto, connection)
    try:
        uuid = await repository.save(avaliacao)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_avaliacao_put(
    connection: ConnectionDependency,
    avaliacaoData: AvaliacaoDeProduto,
    uuid: Annotated[str, Path(title="O uuid da avaliação a fazer put")],
) -> Dict[str, int]:

    repository = Repository(AvaliacaoDeProduto, connection)
    avaliacao = await repository.find_one(uuid=uuid)
    if avaliacao is None:
        raise NotFoundException("Avaliação não encontrada")

    num_rows_affected = await repository.update(
        avaliacao, avaliacaoData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_avaliacao_patch(
    connection: ConnectionDependency,
    avaliacaoData: AvaliacaoDeProduto,
    uuid: Annotated[str, Path(title="O uuid do avaliação a fazer patch")]
) -> Dict[str, int]:

    repository = Repository(AvaliacaoDeProduto, connection)
    avaliacao = await repository.find_one(uuid=uuid)
    if avaliacao is None:
        raise NotFoundException("Avaliação não encontrada")

    num_rows_affected = await repository.update(
        avaliacao,
        avaliacaoData.model_dump()  # type: ignore
    )

    return {'num_rows_affected': num_rows_affected}


@router.delete("/{uuid}")
async def remover_avaliacao(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid da avaliação a fazer delete")]
) -> Dict[str, int]:

    repository = Repository(AvaliacaoDeProduto, connection)
    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
