from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator
import bcrypt

app = FastAPI()


class User(BaseModel):
    first_name: str
    last_name: str
    age: int
    email: EmailStr
    username: str
    password: str

    @validator('password')
    def is_password_empty(cls, v):
        if v == "":
            raise ValueError("should not be empty")
        return v


def password_hasher(raw_password: str):
    return bcrypt.hashpw(raw_password, bcrypt.gensalt(12))


def generate_hashed_password(user_in: User) -> User:
    hashed_password = password_hasher(user_in.password)

    return User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        age=user_in.age,
        username=user_in.username,
        email=user_in.email,
        password=hashed_password
    )
