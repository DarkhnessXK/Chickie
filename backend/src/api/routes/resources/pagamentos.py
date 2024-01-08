from typing import Annotated, List, Dict, Optional
from src.infra.database_postgres.repository import Repository
from src.exceptions import NotFoundException
from fastapi import (  # noqa
    APIRouter,
    HTTPException,
    status,
    Path,
    Query
)
from src.models import Pagamento
from src.dependencies.connection_dependency import connection_dependency

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.get("/")
async def requisitar_pagamentos(
    connection: connection_dependency,
    loja_uuid: Optional[str] = Query(None)
) -> List[Pagamento]:
    """
    Requisita pagamentos cadastrados na plataforma.

    Args:
        loja_uuid (Optional[str]): O uuid da loja, caso necessário.

    Returns:
        list[Pagamento]: Lista de pagamentos encontrados.
    """
    repository = Repository(Pagamento, connection=connection)

    kwargs = {}
    if loja_uuid is not None:
        kwargs["loja_uuid"] = loja_uuid

    results: List[Pagamento] = await repository.find_all(**kwargs)

    return results


@router.get("/{uuid}")
async def requisitar_pagamento(
    connection: connection_dependency,
    uuid: Annotated[str, Path(title="O uuid do pagamento a fazer get")]
) -> Pagamento:
    """
    Busca um pagamento pelo seu uuid.

    Args:
        uuid (str): O uuid do pagamento a ser buscado.

    Returns:
        Pagamento: O pagamento encontrado.

    Raises:
        HTTPException: Se o pagamento não for encontrado.
    """
    repository = Repository(Pagamento, connection=connection)

    result: Optional[Pagamento] = await repository.find_one(uuid=uuid)
    if result is None:
        raise NotFoundException("Pagamento não encontrado")

    return result


@router.post("/", status_code=status.HTTP_201_CREATED)
async def cadastrar_pagamentos(
    connection: connection_dependency,
    pagamento: Pagamento
) -> Dict[str, str]:
    """
    Cadastra um novo pagamento na plataforma.

    Args:
        pagamento (Pagamento): Os detalhes do pagamento a ser cadastrado.

    Returns:
        dict: Um dicionário contendo o uuid do pagamento cadastrado.

    Raises:
        HTTPException: Se ocorrer um erro durante o cadastro.
    """
    repository = Repository(Pagamento, connection=connection)

    try:
        uuid = await repository.save(pagamento)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"uuid": uuid}


@router.put("/{uuid}")
async def atualizar_pagamento_put(
    pagamento_Data: Pagamento,
    connection: connection_dependency,
    uuid: Annotated[str, Path(title="O uuid do pagemento a fazer put")],
) -> Dict[str, int]:
    """
    Atualiza um pagamento utilizando o método HTTP PUT.

    Args:
        pagamento_Data (Pagamento): Os novos dados do pagamento.
        uuid (str): O uuid do pagamento a ser atualizado.

    Returns:
        dict: Um dicionário contendo o número de
        linhas afetadas na atualização.

    Raises:
        HTTPException: Se o pagamento não for encontrado.
    """
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
    pagamentoData: Pagamento,
    connection: connection_dependency,
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
    connection: connection_dependency,
    uuid: Annotated[str, Path(title="O uuid do pagemento a fazer delete")]
) -> Dict[str, int]:
    """
    Remove um pagamento pelo seu uuid.

    Args:
        uuid (str): O uuid do pagamento a ser removido.

    Returns:
        dict: Um dicionário contendo o número de itens removidos.

    Raises:
        HTTPException: Se ocorrer um erro durante a remoção.
    """
    repository = Repository(Pagamento, connection=connection)

    try:
        itens_removed = await repository.delete_from_uuid(uuid=uuid)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"itens_removed": itens_removed}
