from typing import Annotated
from src.exceptions import NotFoundException
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path
)
from src.misc import Paginador  # noqa
from src.domain.models import ZonaDeEntrega
from src.infra.database_postgres.repository import Repository
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/zonas-de-entrega", tags=["Zonas de entrega"])


@router.get("/")
async def requisitar_zonas_de_entrega(connection: ConnectionDependency):

    repository = Repository(ZonaDeEntrega, connection)
    results = await repository.find_all()

    return results


@router.get("/{uuid}")
async def requisitar_zona_de_entrega(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid da zona de entrega a fazer get")]
):

    repository = Repository(ZonaDeEntrega, connection)
    result = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Zona de entrega não encontrada")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_zonas_de_entrega(
    connection: ConnectionDependency,
    zona_de_entrega: ZonaDeEntrega
):

    repository = Repository(ZonaDeEntrega, connection)
    try:
        uuid = await repository.save(zona_de_entrega)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_zona_de_entrega_put(
    connection: ConnectionDependency,
    zona_de_entrega_Data: ZonaDeEntrega,
    uuid: Annotated[
        str, Path(title="O uuid do método de pagemento a fazer put")
    ],
):

    repository = Repository(ZonaDeEntrega, connection)
    zona_de_entrega = await repository.find_one(uuid=uuid)
    if zona_de_entrega is None:
        raise NotFoundException("Zona de entrega não encontrada")

    num_rows_affected = await repository.update(
        zona_de_entrega, zona_de_entrega_Data.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_zona_de_entrega_patch(
    connection: ConnectionDependency,
    zona_de_entregaData: ZonaDeEntrega,
    uuid: Annotated[
        str, Path(title="O uuid da zona de entrega a fazer patch")
    ],
):

    repository = Repository(ZonaDeEntrega, connection)
    zona_de_entrega = await repository.find_one(uuid=uuid)
    if zona_de_entrega is None:
        raise NotFoundException("Zona de entrega não encontrada")

    num_rows_affected = await repository.update(
        zona_de_entrega, zona_de_entregaData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_zona_de_entrega(
    connection: ConnectionDependency,
    uuid: Annotated[
        str, Path(title="O uuid do método de pagemento a fazer delete")
    ]
):

    repository = Repository(ZonaDeEntrega, connection)
    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
