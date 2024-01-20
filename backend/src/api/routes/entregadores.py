from typing import Annotated
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Query,
    Request,
    Depends
)
from src.api.security import oauth2_scheme
from aiopg import Connection
from typing import Optional
from src.domain.models import Entregador
from src.exceptions import NotFoundException
from src.api.security import AuthService
from src.infra.database_postgres.repository import Repository
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/entregadores", tags=["Entregadores"])


@router.get("/")
async def requisitar_entregadores(
    request: Request,
    loja_uuid: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(1),
):
    connection: Connection = request.state.connection

    repository = Repository(Entregador, connection=connection)
    kwargs = {}
    if loja_uuid is not None:
        kwargs["loja_uuid"] = loja_uuid

    results = await repository.find_all(**kwargs)

    return results


@router.get("/{uuid}")
async def requisitar_entregador(
    request: Request,
    uuid: Annotated[str, Path(title="O uuid do entregador a fazer get")]
):
    connection: Connection = request.state.connection

    repository = Repository(Entregador, connection=connection)
    result = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Entregador não encontrado")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_entregadores(
    request: Request,
    entregador: Entregador,
    token: Annotated[str, Depends(oauth2_scheme)],
):
    connection: Connection = request.state.connection
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa

    repository = Repository(Entregador, connection=connection)
    try:
        uuid = await repository.save(entregador)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_entregador_put(
    request: Request,
    entregadorData: Entregador,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do entregador a fazer put")],
):
    connection: Connection = request.state.connection
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Entregador, connection=connection)
    entregador = await repository.find_one(uuid=uuid)
    if entregador is None:
        raise NotFoundException("Entregador não encontrado")

    num_rows_affected = await repository.update(
        entregador, entregadorData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_entregador_patch(
    request: Request,
    entregadorData: Entregador,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do entregador a fazer patch")],
):

    connection: Connection = request.state.connection
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Entregador, connection=connection)

    entregador = await repository.find_one(uuid=uuid)
    if entregador is None:
        raise NotFoundException("Entregador não encontrado")

    num_rows_affected = await repository.update(
        entregador, entregadorData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_entregador(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do entregador a fazer delete")],
):

    connection: Connection = request.state.connection
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Entregador, connection=connection)
    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
