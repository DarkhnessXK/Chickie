import asyncio
from src.infra.database_postgres.repository import Repository
from src.infra.database_postgres.config import DatabaseConnectionManager
from src.domain.models import Loja, Produto
import aiofiles  # type: ignore
from src.services import ImageUploadService
import base64


async def fetch(image_name: str):
    async with aiofiles.open(image_name, 'rb') as f:
        return await f.read()


async def get_image():
    bytes_data = await fetch('image.jpg')
    bytes_data_base64 = base64.b64encode(bytes_data).decode('utf-8')

    return bytes_data_base64


async def main() -> None:
    async with DatabaseConnectionManager() as connection:
        loja_repository = Repository(Loja, connection)
        produto_repository = Repository(Produto, connection)
        lojas = await loja_repository.find_all()
        loja = lojas[0]

        service = ImageUploadService(loja)
        data = await get_image()

        service.upload_image_cadastro(data)

        produtos = await produto_repository.find_all(
            loja_uuid=loja.uuid
        )

        produto = produtos[0]

        service.upload_image_produto(
            produto=produto,
            base64_string=data
        )

        # print({'meta1': meta1, 'meta2': meta2})


if __name__ == '__main__':
    asyncio.run(main())
