from fastapi import APIRouter

from app.classes import users

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={500: {"description": "something went wrong"}}
)


@user_router.post("/generate-password", tags=["users"])
async def generate_pass(user: users.UserIn):
    return await users.generate_hashed_password(user)
