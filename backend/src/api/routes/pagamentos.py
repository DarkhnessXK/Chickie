from typing import Annotated, List, Dict, Optional
from src.infra.database_postgres.repository import Repository
from src.exceptions import NotFoundException
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Query,
    Request,
    Depends
)
from src.domain.models import Pagamento
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.get("/")
async def requisitar_pagamentos(
    connection: ConnectionDependency,
    loja_uuid: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(1),
) -> List[Pagamento]:

    repository = Repository(Pagamento, connection=connection)
    kwargs = {}
    if loja_uuid is not None:
        kwargs["loja_uuid"] = loja_uuid

    results: List[Pagamento] = await repository.find_all(**kwargs)

    return results


@router.get("/{uuid}")
async def requisitar_pagamento(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid do pagamento a fazer get")]
) -> Pagamento:

    repository = Repository(Pagamento, connection=connection)
    result: Optional[Pagamento] = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Pagamento não encontrado")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_pagamentos(
    connection: ConnectionDependency,
    pagamento: Pagamento
) -> Dict[str, str]:

    repository = Repository(Pagamento, connection=connection)
    try:
        uuid = await repository.save(pagamento)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_pagamento_put(
    connection: ConnectionDependency,
    pagamento_Data: Pagamento,
    uuid: Annotated[str, Path(title="O uuid do pagemento a fazer put")],
) -> Dict[str, int]:

    repository = Repository(Pagamento, connection=connection)
    pagamento = await repository.find_one(uuid=uuid)
    if pagamento is None:
        raise NotFoundException("Pagamento não encontrado")

    num_rows_affected = await repository.update(
        pagamento, pagamento_Data.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_pagamento_patch(
    connection: ConnectionDependency,
    pagamentoData: Pagamento,
    uuid: Annotated[str, Path(title="O uuid do pagamento a fazer patch")],
) -> Dict[str, int]:

    repository = Repository(Pagamento, connection=connection)
    pagamento = await repository.find_one(uuid=uuid)
    if pagamento is None:
        raise NotFoundException("Pagamento não encontrado")

    num_rows_affected = await repository.update(
        pagamento, pagamentoData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_pagamento(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid do pagemento a fazer delete")]
) -> Dict[str, int]:

    repository = Repository(Pagamento, connection=connection)

    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
