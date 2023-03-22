from app.classes import auth_service as auth
import asyncio
import sys
import uvicorn

service = auth.AuthService()
service.setup_api()


async def app():

    task1 = asyncio.create_task(service.connect_to_nats())
    await task1

    task2 = asyncio.create_task(service.set_up_subscriptions())
    await task2


if __name__ == '__main__':
    try:
        asyncio.run(app())
        # TODO fix subscription response
        uvicorn.run(service, host="127.0.0.1", port=8000, log_level="info")
    except Exception as e:
        print(e)
        sys.exit(0)

