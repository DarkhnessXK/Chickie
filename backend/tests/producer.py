import asyncio
from src.services.rmq_service import RMQService
from secrets import token_urlsafe


async def main() -> None:
    messaging_service = RMQService()
    await messaging_service.send({'token': token_urlsafe(10)})


loop = asyncio.get_event_loop()

for i in range(100):
    loop.run_until_complete(main())
