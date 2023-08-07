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
from src.schemas import Loja, Pedido
from src.infra.database.repository import Repository
from src.infra.database.manager import DatabaseConnectionManager


current_user = Annotated[Loja, Depends(security.current_user)]
NotFoundException = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado"
)

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


@router.get("/")
async def requisitar_pedidos():
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pedido, connection=connection)
        results = await repository.find_all()

    return results


@router.get("/{uuid}")
async def requisitar_pedido(
    uuid: Annotated[str, Path(title="O uuid do pedido a fazer get")]
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pedido, connection=connection)
        result = await repository.find_one(uuid=uuid)

        if result is None:
            raise NotFoundException

    return result


@router.post("/", status_code=201)
async def cadastrar_pedidos(pedido: Pedido):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pedido, connection=connection)
        try:
            uuid = await repository.save(pedido)
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.patch("/{uuid}")
async def atualizar_pedido_patch(
    uuid: Annotated[str, Path(title="O uuid do pedido a fazer patch")],
    current_user: current_user,
):
    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_pedido_put(
    itemData: Pedido,
    current_user: current_user,
    uuid: Annotated[str, Path(title="O uuid do pedido a fazer put")],
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pedido, connection=connection)
        pedido = await repository.find_one(uuid=uuid)
        if pedido is None:
            raise NotFoundException

    num_rows_affected = await repository.update(
        pedido, itemData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_pedido(
    current_user: current_user,
    uuid: Annotated[str, Path(title="O uuid do pedido a fazer delete")]
):
    async with DatabaseConnectionManager() as connection:
        repository = Repository(Pedido, connection=connection)
        try:
            itens_removed = await repository.delete_from_uuid(uuid=uuid)
        except Exception as error:
            raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
