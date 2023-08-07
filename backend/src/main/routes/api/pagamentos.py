from typing import Annotated
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Depends,
    Query,
)
from src.main import security
from src.schemas import Loja, Pagamento
from src.infra.database.repository import Repository
from src.infra.database.manager import DatabaseConnectionManager


current_user = Annotated[Loja, Depends(security.current_user)]
NotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Pagamento não encontrado"
)

router = APIRouter(
    prefix="/pagamentos",
    tags=["Pagamentos"]
)


@router.get("/")
async def requisitar_pagamentos():
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pagamento, connection=connection)
        results = await repository.find_all()

    return results


@router.get("/{uuid}")
async def requisitar_pagamento(
    uuid: Annotated[
        str, Path(title="O uuid do pagamento a fazer get")
    ]
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pagamento, connection=connection)
        result = await repository.find_one(uuid=uuid)

        if result is None:
            raise NotFoundException

    return result


@router.post("/", status_code=201)
async def cadastrar_pagamentos(
    pagamento: Pagamento
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pagamento, connection=connection)
        try:
            uuid = await repository.save(pagamento)
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_pagamento_put(
    pagamento_Data: Pagamento,
    uuid: Annotated[
        str, Path(title="O uuid do pagemento a fazer put")
    ],
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pagamento, connection=connection)
        pagamento = await repository.find_one(uuid=uuid)
        if pagamento is None:
            raise NotFoundException

    num_rows_affected = await repository.update(
        pagamento,
        pagamento_Data.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_pagamento_patch(
    pagamentoData: Pagamento,
    uuid: Annotated[
        str, Path(title="O uuid do pagamento a fazer patch")
    ]
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pagamento, connection=connection)
        pagamento = await repository.find_one(uuid=uuid)
        if pagamento is None:
            raise NotFoundException

    num_rows_affected = await repository.update(
        pagamento,
        pagamentoData.model_dump()  # type: ignore
    )

    return {'num_rows_affected': num_rows_affected}


@router.delete("/{uuid}")
async def remover_pagamento(
    uuid: Annotated[
        str, Path(title="O uuid do pagemento a fazer delete")
    ]
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pagamento, connection=connection)
        try:
            itens_removed = await repository.delete_from_uuid(uuid=uuid)
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
