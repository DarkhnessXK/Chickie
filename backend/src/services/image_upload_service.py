import re
from config import settings
import base64
from typing import Any, Optional, Dict
from pydantic import BaseModel
from src.domain.models import Loja, Produto
from contextlib import suppress

import cloudinary.uploader  # type: ignore
import cloudinary.api  # type: ignore
import enum
import uuid
import os


class ImageType(enum.Enum):
    Produto = 'Produto'
    Cadastro = 'Cadastro'


class ImageUploadServiceResponse(BaseModel):
    """Response structure for image upload service."""
    data: dict
    loja_uuid: str | None = None

    __tablename__ = 'ImagemCadastroCollection'


class ImageUploadServiceBase:
    """Service for uploading, deleting, and retrieving images."""

    def __init__(self, loja: Loja):
        """Initialize Cloudinary configuration."""

        self.loja = loja

        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET
        )

    def get_image_url_by_asset_id(self, asset_id):
        query = f"resource_type:image AND asset_id={asset_id}"
        search = cloudinary.Search()
        result = search.expression(query) \
            .sort_by("public_id", "desc")\
            .max_results("1")\
            .execute()

        return result

    def delete_image_by_public_id(self, public_id: str):
        public_ids = [public_id]
        image_delete_result = cloudinary.api.delete_resources(
            public_ids, resource_type="image",
            type="upload"
        )
        print(image_delete_result)
        return image_delete_result  # type: ignore

    def safe_name(self, name: str) -> str:
        """Sanitize name to remove special characters."""

        safe_name = re.sub(r'[^a-zA-Z0-9]', '_', name)  # type: ignore
        safe_name = re.sub(r'\s+', '_', safe_name).strip('_')
        return safe_name

    def execute_query(self, query: str):
        return cloudinary.Search()\
            .expression(query)\
            .sort_by("public_id", "desc") \
            .max_results("30") \
            .execute()


class ImageUploadProdutoService(ImageUploadServiceBase):

    def upload_image_produto(
        self,
        produto: Produto,
        base64_string: str,
        filename: Optional[str] = None
    ) -> ImageUploadServiceResponse:
        bytes_data = base64.b64decode(base64_string)

        with suppress(ValueError):
            public_id = self.__get_public_id_image_produto(produto)
            self.delete_image_by_public_id(public_id)

        if filename:
            new_name = self.__get_cloud_filename(produto, filename)
            metadata_dict = cloudinary.uploader.upload(
                file=bytes_data,
                folder=self.image_produto_folder_path,
                public_id=new_name
            )
        else:
            metadata_dict = cloudinary.uploader.upload(
                file=bytes_data,
                folder=self.image_produto_folder_path
            )

        return ImageUploadServiceResponse(data=metadata_dict)

    def get_public_url_image_produto(self, produto) -> str:
        file_metadata = self.image_produto_metadata(produto)
        if file_metadata:
            asset_id = file_metadata['secure_url']
            if isinstance(asset_id, str):
                return asset_id

        raise ValueError('Nenhuma imagem encotrada!')

    def __get_public_id_image_produto(self, produto) -> str:
        file_metadata = self.image_produto_metadata(produto)
        if file_metadata:
            asset_id = file_metadata['public_id']
            if isinstance(asset_id, str):
                return asset_id

        raise ValueError('Nenhuma imagem encotrada!')

    def __get_cloud_filename(self, produto: Produto, filename: str) -> str:
        name, ext = os.path.splitext(filename)  # type: ignore
        new_filename = f"{name}_{produto.nome}_{produto.uuid}"

        web_safe_name = re.sub(
            pattern=r'[^\w\s-]',
            repl='',
            string=new_filename
        ).strip().replace(' ', '-')

        return web_safe_name

    def delete_image_produto(self, produto: Produto):
        public_id = self.__get_public_id_image_produto(produto)
        return self.delete_image_by_public_id(public_id)

    @property
    def image_produto_folder_path(self):
        dirname = self.safe_name(f'{self.loja.uuid}_{self.loja.username}')
        return (f'lojas/{dirname}/imagem_produto/')

    def image_produto_metadata(
        self, produto: Produto
    ) -> Optional[Dict[str, Any]]:

        """
        {
            'asset_id': 'f3785f1bf01146afcf32e8796f4d21a8',
            'public_id': 'folder_teste/empresa/fmla9sjviktuomuopdva',
            'format': 'jpg',
            'version': 1704084448,
            'resource_type': 'image',
            'type': 'upload',
            'created_at': '2024-01-01T04:47:28Z',
            'bytes': 55801,
            'width': 1500,
            'height': 870,
            'folder': 'folder_teste/empresa',
            'url': 'http://res.cloudinary.com/
                    ddus7rrgr/image/upload/v1704084448/folder_teste/
                    empresa/fmla9sjviktuomuopdva.jpg',
            'secure_url': 'https://res.cloudinary.com/
                    ddus7rrgr/image/upload/v1704084448/folder_teste/
                    empresa/fmla9sjviktuomuopdva.jpg'
        }
        """
        result = self.execute_query("resource_type:image")
        for image in result['resources']:
            if produto.uuid in image['public_id']:
                return image

        raise ValueError('Nenhum produto encontrado!')


class ImageUploadCadastroService(ImageUploadServiceBase):

    @property
    def public_id(self):
        result = self.execute_query("resource_type:image")
        for image in result['resources']:
            if self.loja.uuid in image['public_id']:
                return image['public_id']

        raise ValueError('Nenhum recurso encontrado!')

    def upload_image_cadastro(
        self,
        base64_string: str,
        filename: Optional[str] = None
    ) -> ImageUploadServiceResponse:
        """Upload an image to Cloudinary."""
        bytes_data: bytes = base64.b64decode(base64_string)

        if filename:
            new_name = self.__get_cloud_filename(filename)
            metadata_dict = cloudinary.uploader.upload(
                file=bytes_data,
                folder=self.image_cadastro_folder_path,
                public_id=new_name
            )
        else:
            metadata_dict = cloudinary.uploader.upload(
                file=bytes_data,
                folder=self.image_cadastro_folder_path
            )

        return ImageUploadServiceResponse(data=metadata_dict)

    def delete_image_cadastro(self):
        public_id = self.__get_public_id_image_cadastro()
        return self.delete_image_by_public_id(public_id)

    def get_public_url_image_cadastro(self) -> str:
        file_metadata = self.image_cadastro_metadata
        if file_metadata:
            public_url = file_metadata['secure_url']
            if isinstance(public_url, str):
                return public_url

        raise ValueError('Nenhuma imagem encontrada!')

    def __get_public_id_image_cadastro(self) -> str:
        file_metadata = self.image_cadastro_metadata
        if file_metadata:
            asset_id = file_metadata['public_id']
            if isinstance(asset_id, str):
                return asset_id

        raise ValueError('Nenhuma imagem encontrada!')

    def __get_cloud_filename(self, filename: str) -> str:
        name, ext = os.path.splitext(filename)  # type: ignore
        uuid_part = str(uuid.uuid4())
        new_filename = f"{name}_{self.loja.uuid or uuid_part}"

        web_safe_name = re.sub(
            pattern=r'[^\w\s-]',
            repl='',
            string=new_filename
        ).strip().replace(' ', '-')

        return web_safe_name

    @property
    def image_cadastro_folder_path(self) -> str:
        dirname = self.safe_name(f'{self.loja.username}_{self.loja.uuid}')
        return (f'lojas/{dirname}/imagem_cadastro')

    @property
    def image_cadastro_metadata(
        self
    ) -> Optional[Dict[str, Any]]:
        """
        {
            'asset_id': 'f3785f1bf01146afcf32e8796f4d21a8',
            'public_id': 'folder_teste/empresa/fmla9sjviktuomuopdva',
            'format': 'jpg',
            'version': 1704084448,
            'resource_type': 'image',
            'type': 'upload',
            'created_at': '2024-01-01T04:47:28Z',
            'bytes': 55801,
            'width': 1500,
            'height': 870,
            'folder': 'folder_teste/empresa',
            'url': 'http://res.cloudinary.com/
                    ddus7rrgr/image/upload/v1704084448/folder_teste/
                    empresa/fmla9sjviktuomuopdva.jpg',
            'secure_url': 'https://res.cloudinary.com/
                    ddus7rrgr/image/upload/v1704084448/folder_teste/
                    empresa/fmla9sjviktuomuopdva.jpg'
        }
        """
        result = self.execute_query("resource_type:image")
        for image in result['resources']:
            if self.loja.uuid in image['public_id']:
                return image

        raise ValueError('Nenhuma imagem de cadastro encontrada!')


class ImageUploadService(
    ImageUploadCadastroService,
    ImageUploadProdutoService
):
    ...
