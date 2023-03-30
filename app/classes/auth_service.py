import json
from typing import Any

from fastapi import FastAPI
from nats.aio.client import Client as Nats, Msg as Msg, Subscription as Sub, Awaitable as Awaitable, Type as Type

from app.classes.users import User, generate_hashed_password
from app.routers import users, home


class AuthService(FastAPI):
    nc = Nats | None
    sub = Sub | None
    shutdown = bool

    def __init__(self, **extra: Any):
        super().__init__(**extra)
        self.nc = Nats()
        self.sub = None

    async def connect_to_nats(self):
        await self.nc.connect("nats://127.0.0.1:4222")

    async def set_up_subscriptions(self):
        try:
            self.sub = await self.nc.subscribe("auth.generate.password", cb=self.generate_password)
        except Exception as e:
            print(e)
            return

    async def process_request(self, m=Type[Msg]) -> Awaitable[None] | None:
        print(f"Received a message on '{m.subject} {m.reply}': {m.data.decode()}")
        return await self.nc.publish(m.reply, b'secretpassword')

    def setup_api(self):
        self.include_router(home.home_router)
        self.include_router(users.user_router)

    async def stop(self):
        # Remove interest in subscription.
        await self.nc.flush()
        print("nats conn terminating...")
        # Terminate connection to NATS.
        await self.nc.drain()

    async def generate_password(self, m=Type[Msg]) -> Awaitable[None] | None:
        reply = m.reply
        try:
            user_raw = json.loads(m.data)
            user_in = User(**user_raw)
            user_with_hashed_pass = generate_hashed_password(user_in)
            res = user_with_hashed_pass.json()
        except Exception as e:
            print(e)
            return await self.nc.publish(reply, b'{message:"something went wrong getting message"}')
        return await self.nc.publish(reply, str.encode(res))

