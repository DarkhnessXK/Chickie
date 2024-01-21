from typing import Annotated
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
from src.api.security import oauth2_scheme
from typing import Optional
from src.domain.models import Funcionario
from src.infra.database_postgres.repository import Repository
from src.api.security import AuthService
from src.misc import Paginador  # noqa
from src.dependencies import ConnectionDependency


router = APIRouter(prefix="/funcionarios", tags=["Funcionários"])


@router.get("/")
async def requisitar_funcionarios(
    connection: ConnectionDependency,
    loja_uuid: Optional[str] = Query(None),
    limit: int = Query(0),
    offset: int = Query(1),
):

    repository = Repository(Funcionario, connection=connection)
    kwargs = {}
    if loja_uuid is not None:
        kwargs["loja_uuid"] = loja_uuid

    results = await repository.find_all(**kwargs)

    return results


@router.get("/{uuid}")
async def requisitar_funcionario(
    connection: ConnectionDependency,
    uuid: Annotated[str, Path(title="O uuid do funcionário a fazer get")]
):

    repository = Repository(Funcionario, connection=connection)
    result = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Funcionario não encontrado")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_funcionarios(
    connection: ConnectionDependency,
    funcionario: Funcionario,
    token: Annotated[str, Depends(oauth2_scheme)],
):

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Funcionario, connection=connection)
    try:
        uuid = await repository.save(funcionario)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_funcionario_put(
    connection: ConnectionDependency,
    funcionarioData: Funcionario,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do funcionario a fazer put")]
):

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Funcionario, connection=connection)
    funcionario = await repository.find_one(uuid=uuid)
    if funcionario is None:
        raise NotFoundException("Funcionario não encontrado")

    num_rows_affected = await repository.update(
        funcionario, funcionarioData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.patch("/{uuid}")
async def atualizar_funcionario_patch(
    connection: ConnectionDependency,
    funcionarioData: Funcionario,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do funcionario a fazer patch")],
):

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Funcionario, connection=connection)

    funcionario = await repository.find_one(uuid=uuid)
    if funcionario is None:
        raise NotFoundException("Funcionario não encontrado")

    num_rows_affected = await repository.update(
        funcionario, funcionarioData.model_dump()  # type: ignore
    )

    return {"num_rows_affected": num_rows_affected}


@router.delete("/{uuid}")
async def remover_funcionario(
    connection: ConnectionDependency,
    token: Annotated[str, Depends(oauth2_scheme)],
    uuid: Annotated[str, Path(title="O uuid do funcionario a fazer delete")],
):

    auth_service = AuthService(connection)
    loja = await auth_service.current_company(token)  # noqa
    repository = Repository(Funcionario, connection=connection)
    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
