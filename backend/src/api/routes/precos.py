from typing import Annotated, Optional, List, Dict
from src.infra.database_postgres.repository import Repository
from src.exceptions import NotFoundException, ConflictException
from starlette import status
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Query,
    Depends
)
from src.api.security import oauth2_scheme, AuthService
from src.domain.models import Preco
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/precos", tags=["Preços"])


@router.get("/")
async def requisitar_precos(
    connection: ConnectionDependency,
    produto_uuid: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(1),
) -> List[Preco]:

    repository = Repository(Preco, connection)
    kwargs = {}
    if produto_uuid is not None:
        kwargs["produto_uuid"] = produto_uuid

    results: List[Preco] = await repository.find_all(**kwargs)

    return results


@router.get("/{uuid}")
async def requisitar_preco(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid do preco a fazer get")]
) -> Preco:

    repository = Repository(Preco, connection)
    result: Optional[Preco] = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Preço não encontrado")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_precos(
    connection: ConnectionDependency,
    preco: Preco,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Dict[str, str]:

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Preco, connection)
    query = await repository.find_one(
        dia_da_semana=preco.dia_da_semana,
        produto_uuid=preco.produto_uuid
    )
    if query:
        raise ConflictException('Preço já cadastrado para este '
                                'produto e para este dia da semana!')
    try:
        uuid = await repository.save(preco)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.patch("/{uuid}")
async def atualizar_preco_patch(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do preco a fazer patch")]
):

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    return {}


@router.put("/{uuid}")
async def atualizar_preco_put(
    connection: ConnectionDependency,
    itemData: Preco,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do preco a fazer put")]
) -> Dict[str, int]:

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Preco, connection)
    preco = await repository.find_one(uuid=uuid)
    if preco is None:
        raise NotFoundException("Preço não encontrado")

    num_rows_affected = await repository.update(
        preco, itemData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_preco(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do preco a fazer delete")]
) -> Dict[str, int]:

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Preco, connection)

    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
