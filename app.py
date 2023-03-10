from fastapi import FastAPI
import re

app = FastAPI()


def simple_format(*args):
    s = re.sub(r'%(\d+)', r'{\1}', args[0])
    return s.format(*args[1:])


def print_hi(name):
    return simple_format(f'Hi, {name}')


@app.get("/")
async def root():
    name = print_hi("Alexander")
    return {"message": name}
