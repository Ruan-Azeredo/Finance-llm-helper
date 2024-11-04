from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Callable

from models import User

class UserInput(BaseModel):
    name: str
    email: str
    password: str

user_router = APIRouter()

def handle_HTTPException_error(method: Callable[..., User]) -> dict:
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except HTTPException as http_error:
            raise http_error
        except Exception as error:
            raise HTTPException(status_code = 500, detail = str(error))
    return wrapper

@user_router.get("/")
@handle_HTTPException_error
async def get_users():

    users = User.all()
    return {"users": [user.to_dict() for user in users]}


@user_router.get("/{user_id}")
@handle_HTTPException_error
async def get_user(user_id: int):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return {"user": user.to_dict()}

@user_router.post("/")
@handle_HTTPException_error
async def create_user(user_input: UserInput):

    user = User.create(
        name = user_input.name,
        email = user_input.email,
        password = user_input.password
    )

    return {"message": "User created", "user": str(user)}

@user_router.put("/{user_id}")
@handle_HTTPException_error
async def update_user(user_id: int, user_input: UserInput):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.update(
        name = user_input.name,
        email = user_input.email,
        password = user_input.password
    )

    return {"message": "User updated", "user": str(user)}

@user_router.delete("/{user_id}")
async def delete_user(user_id: int):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.delete()

    return {"message": "User deleted"}