import asyncio
from fastapi import FastAPI
from nats.aio.client import Client as Nats, Msg as Msg, Subscription as Sub, Awaitable as Awaitable, Type as Type
import signal
from app.routers import users, home
from typing import Any
import json


class AuthService(FastAPI):
    nc = Nats | None
    sub = Sub | None
    shutdown = bool
    # loop = asyncio.get_event_loop()

    def __init__(self, **extra: Any):
        super().__init__(**extra)
        self.nc = Nats()
        self.sub = None
        self.shutdown = False

        # Handles graceful shutdown
        # signal.signal(signal.SIGINT, self.exit_graceful)
        # signal.signal(signal.SIGTERM, self.exit_graceful)

    # def exit_graceful(self, signum, frame):
    #     print('Received:', signum, ": ", frame)
    #     self.shutdown = True

    async def connect_to_nats(self):
        await self.nc.connect("nats://127.0.0.1:4222")

    async def set_up_subscriptions(self):
        async def response_handle(msg):
            m = json.loads(msg.data.decode())
            # self.nc.msgs.append(message)
            return await self.nc.publish(m.reply, b'secretpassword')

        self.sub = await self.nc.subscribe("auth.generate.password", cb=response_handle)

    async def process_request(self, m=Type[Msg]) -> Awaitable[None] | None:
        print(f"Received a message on '{m.subject} {m.reply}': {m.data.decode()}")
        return await self.nc.publish(m.reply, b'secretpassword')

    async def run(self):
        print("running App, awaiting messages: ")

        while True:
            await asyncio.sleep(1)

    def setup_api(self):
        self.include_router(home.home_router)
        self.include_router(users.user_router)

    async def stop(self):
        # Remove interest in subscription.
        await self.nc.flush()
        print("nats conn terminating...")
        # Terminate connection to NATS.
        await self.nc.drain()

