from src.infra.cache import RedisService
import asyncio


async def main():
    async with RedisService(db=0) as service:
        await service.set(key='ola', value='múndo')
        value = await service.get('ola')
        print(value)


asyncio.run(main())
