from fastapi import APIRouter

home_router = APIRouter(
    responses={500: {"description": "something went wrong"}}
)


@home_router.get("/")
async def root():
    return {"message": "Hello Authentication service!"}