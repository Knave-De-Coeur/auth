from app.classes import auth_service as auth
import asyncio
import sys

app = auth.AuthService()
app.setup_api()


async def main():

    _ = asyncio.gather(app.connect_to_nats(), app.set_up_subscriptions())

    while not app.shutdown:
        await app.run()

    await app.stop()
    sys.exit(0)


@app.api.get("/")
async def root():
    return {"message": "Hello Authentication service!"}
