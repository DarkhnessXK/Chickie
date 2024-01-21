# from src.services.rmq_service import RMQService
# from src.tasks import main
# import asyncio


# async def start(messaging_service: RMQService) -> None:
#     await messaging_service.connect()
#     await messaging_service.start_consuming(callback=main.callback)


# async def close(messaging_service: RMQService) -> None:
#     await messaging_service.close()


# service = RMQService()
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(start(messaging_service=service))
# except KeyboardInterrupt:
#     loop.run_until_complete(close(messaging_service=service))

##############################################################################
# from src.services.rmq_service import RMQService
# import asyncio


# async def callback(channel, message, envelope, properties):
#     print(message)


# async def start(messaging_service: RMQService) -> None:
#     await messaging_service.connect()
#     await messaging_service.start_consuming(callback=callback)


# async def close(messaging_service: RMQService) -> None:
#     await messaging_service.close()


# service = RMQService()
# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(start(messaging_service=service))
# except KeyboardInterrupt:
#     loop.run_until_complete(close(messaging_service=service))


import asyncio
from config import settings as s
from src.services.rmq_service import RMQService
from aioamqp.exceptions import EmptyQueue  # type: ignore


async def main():
    async with RMQService() as service:
        await service.send({'hello': 'world'})
        await service.send({'hello': 'world'})
        await service.send({'hello': 'world'})


async def main2():
    async with RMQService() as service:

        message_properties = await service.channel.basic_get(s.RABBITMQ_QUEUE)

        if message_properties is not None:
            print(message_properties)

        message_properties = await service.channel.basic_get(s.RABBITMQ_QUEUE)

        if message_properties is not None:
            print(message_properties)

        message_properties = await service.channel.basic_get(s.RABBITMQ_QUEUE)

        if message_properties is not None:
            print(message_properties)

        message_properties = await service.channel.basic_get(s.RABBITMQ_QUEUE)

        if message_properties is not None:
            print(message_properties)


if __name__ == '__main__':
    # asyncio.run(main())
    try:
        asyncio.run(main2())
    except EmptyQueue:
        print('Fila vazia')
