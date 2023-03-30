from app.classes import auth_service as auth
import asyncio
import sys
import uvicorn

service = auth.AuthService()
service.setup_api()


async def create_webserver(port):
    server_config = uvicorn.Config(service, port=port, log_level="info")
    server = uvicorn.Server(server_config)
    await server.serve()


async def app():
    task1 = asyncio.create_task(create_webserver(8000))
    task2 = service.connect_to_nats()
    task3 = service.set_up_subscriptions()
    _ = await asyncio.gather(
            task1,
            task2,
            task3,
    )

    # terminates nats connection and flushes subscriptions
    await service.stop()


if __name__ == '__main__':
    try:
        asyncio.run(app())
    except Exception as e:
        print(e)
        sys.exit(0)

