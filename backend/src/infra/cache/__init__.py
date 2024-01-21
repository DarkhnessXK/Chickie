import aioredis
from typing import TypeVar, Any, Optional
from config import settings as s  # noqa  # type: ignore
import json


T = TypeVar("T")


class RedisService:
    def __init__(self, db: int = 0):
        self.redis_db = None
        self.redis_url = str(s.REDIS_URL)
        self.db = db

    async def connect(self):
        self.redis_db = await aioredis.from_url(
            self.redis_url,
            db=self.db
        )

    async def close(self):
        if self.redis_db is None:
            raise ValueError('Necessário conectar antes')

        if self.redis_db:
            await self.redis_db.close()

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def get(self, key: str) -> Any:
        if self.redis_db is None:
            raise ValueError('Necessário conectar antes')

        value = await self.redis_db.get(key)
        if value:
            return value.decode()

    async def set(
        self,
        key: str,
        value: Any,
        key_ttl: Optional[int] = None,
    ) -> None:

        if self.redis_db is None:
            raise ValueError('Necessário conectar antes')

        value_dumped = value
        if key_ttl is None:
            key_ttl = int(s.CACHE_DEFAULT_TIMEOUT)

        await self.redis_db.setex(
            key,
            key_ttl,
            value_dumped
        )

    async def store_dict(self, key, data: dict) -> None:
        print("Armazenando dicionario ao redis")
        json_data = json.dumps(data)
        await self.set(key, json_data)

    async def get_dict(self, key) -> Optional[dict]:
        print("Armazenando dicionario ao redis")
        value = await self.get(key)
        try:
            json_data = json.loads(value.decode('utf-8'))
            return json_data
        except Exception:
            return None

    # async def dict(self) -> dict:
    #     if self.redis_db is None:
    #         raise ValueError('Necessário conectar antes')

    #     print("Retornando dicionario do redis")
    #     keys = await self.redis_db.keys("*")
    #     data = {}
    #     for key in keys:
    #         data[key.decode()] = await self.get(key)
    #     return data

    # async def delete(self, key: str) -> None:
    #     if self.redis_db is None:
    #         raise ValueError('Necessário conectar antes')

    #     print("Deletando chave do redis")
    #     await self.redis_db.delete(key)

    # async def clear(self) -> None:
    #     if self.redis_db is None:
    #         raise ValueError('Necessário conectar antes')

    #     print("Limpando cache do redis")
    #     keys = await self.redis_db.keys("*")
    #     for key in keys:
    #         await self.delete(key)


async def get_cache() -> RedisService:
    cache = RedisService(db=int(s.REDIS_DB))
    await cache.connect()
    await cache.set("hello", "world")
    return cache
