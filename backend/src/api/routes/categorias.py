from typing import Annotated, Optional, Dict, List
from src.infra.database_postgres.repository import Repository
from src.exceptions import NotFoundException
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Query,
    Request,
    Depends,
    Query
)
from src.api.security import oauth2_scheme, AuthService
from src.domain.models import CategoriaProdutos, CategoriasProdutos
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.get("/")
async def requisitar_categorias(
    connection: ConnectionDependency,
    nome: Optional[str] = Query(None),
    loja_uuid: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(1),
) -> CategoriasProdutos:

    repository = Repository(CategoriaProdutos, connection)

    kwargs = {}
    if nome is not None:
        kwargs["nome"] = nome
    if loja_uuid is not None:
        kwargs["loja_uuid"] = loja_uuid

    results: List[CategoriaProdutos] = await repository.find_all(**kwargs)
    paginate = Paginador(results, offset, limit)

    return CategoriasProdutos(**paginate.get_response())


@router.get("/{uuid}")
async def requisitar_categoria(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid da categoria a fazer get")],
    nome: Optional[str] = Query(None)
) -> CategoriaProdutos:

    repository = Repository(CategoriaProdutos, connection)
    kwargs = {}
    if nome is not None:
        kwargs["nome"] = nome

    result: Optional[CategoriaProdutos] = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Categoria não encontrada")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_categorias(
    connection: ConnectionDependency,
    categoria: CategoriaProdutos,
    token: Annotated[str, Depends(oauth2_scheme)],
) -> Dict[str, str]:

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa

    repository = Repository(CategoriaProdutos, connection)
    try:
        uuid = await repository.save(categoria)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.patch("/{uuid}")
async def atualizar_categoria_patch(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid da categoria a fazer patch")],
):
    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    return {}


@router.put("/{uuid}")
async def atualizar_categoria_put(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    itemData: CategoriaProdutos,
    uuid: Annotated[str, Path(title="O uuid da categoria a fazer put")],
) -> Dict[str, int]:

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa

    repository = Repository(CategoriaProdutos, connection)
    try:
        categoria = await repository.find_one(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    if categoria is None:
        raise NotFoundException("Categoria não encontrada")

    num_rows_affected = await repository.update(
        categoria, itemData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_categoria(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid da categoria a fazer delete")],
) -> Dict[str, int]:

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(CategoriaProdutos, connection)
    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
