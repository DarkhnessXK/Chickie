from src.infra.database_postgres.repository import Repository
from typing import List, Any, Optional


class BaseService:

    repo: Repository

    async def get(self, uuid: str) -> Optional[Any]:
        return await self.repo.find_one(uuid=uuid)

    async def get_all(self, **kwargs) -> List[Any]:
        return await self.repo.find_all(**kwargs)
