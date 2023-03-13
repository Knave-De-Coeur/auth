from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, validator

app = FastAPI()


class UserIn(BaseModel):
    username: str
    email: EmailStr
    age: int
    first_name: str | None = None
    last_name: str | None = None
    password: str

    @validator('password')
    def is_password_empty(cls, v):
        if v == "":
            raise ValueError("should not be empty")
        return v


class UserOut(BaseModel):
    def __int__(self, first_name, last_name, username, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None


def password_hasher(raw_password: str):
    return "supersecret" + raw_password


def generate_hashed_password(user_in: UserIn):
    hashed_password = password_hasher(user_in.password)
    print("successfully generated password!")
    user_with_pass = UserOut(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        username=user_in.username,
        email=user_in.email,
        password=hashed_password
    )

    return user_with_pass
