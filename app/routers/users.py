from fastapi import APIRouter

from app.classes import users

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={500: {"description": "something went wrong"}}
)


@router.post("/generate-password", tags=["users"])
async def generate_pass(user: users.UserIn):
    return users.generate_hashed_password(user)
