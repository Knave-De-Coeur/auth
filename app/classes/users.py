from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator

app = FastAPI()


class UserIn(BaseModel):
    username: str
    email: EmailStr
    age: int
    first_name: str
    last_name: str
    password: str

    @validator('password')
    def is_password_empty(cls, v):
        if v == "":
            raise ValueError("should not be empty")
        return v


class UserOut(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str


def password_hasher(raw_password: str):
    return "supersecret" + raw_password


async def generate_hashed_password(user_in: UserIn) -> UserOut:
    hashed_password = password_hasher(user_in.password)
    print("successfully generated password!")
    return UserOut(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        username=user_in.username,
        email=user_in.email,
        password=hashed_password
    )
