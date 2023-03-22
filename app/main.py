from app.classes import auth_service as auth
import asyncio
import sys


async def app():
    service = auth.AuthService()
    service.setup_api()

    _ = asyncio.gather(service.connect_to_nats(), service.set_up_subscriptions())

    while not service.shutdown:
        await service.run()

    await service.stop()
    sys.exit(0)


if __name__ == '__main__':
    asyncio.run(app())

