from fastapi import FastAPI
import re

# from .internal import user
from .routers import users

app = FastAPI()
app.include_router(users.router)


def simple_format(*args):
    s = re.sub(r'%(\d+)', r'{\1}', args[0])
    return s.format(*args[1:])


@app.get("/")
async def root():
    return {"message": "Hello Authentication service!"}
