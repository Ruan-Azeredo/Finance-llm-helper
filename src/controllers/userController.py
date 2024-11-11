from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Callable
from datetime import datetime
import json

from auth import get_current_user
from models import User

class UserInput(BaseModel):
    name: str
    email: str
    password: str

user_router = APIRouter()

@user_router.get("/ops")
async def get_users():

    def model_to_dict(user: User) -> dict:
        user_dict = {}

        for name, value in user.__data__.items():
            if isinstance(value, datetime):
                user_dict[name] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                user_dict[name] = value
            print('n: ', name, value, type(value))

        print('user_dict: ', user_dict)
        return user_dict

    users = User.all()
    users_data_1 = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            # Adicione outros campos conforme necessário
        }
        for user in users
    ]

    users_data = []

    #print('type users_data_1: ', [type(user) for user in users_data_1] , 'type users_data: ', [type(user) for user in users_data])

    for user in users:
        #print('type(model_to_dict(user))', type(model_to_dict(user)))
        users_data.append(model_to_dict(user))

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"users": users_data}
    )

@user_router.get("/ops/{user_id}")
async def get_user(user_id: int):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"user": user.to_dict()}
    )

@user_router.post("/ops")
async def create_user(user_input: UserInput):

    user = User.create(
        name = user_input.name,
        email = user_input.email,
        password = user_input.password
    )

    json_user = json.dumps(user.to_dict())

    """ print(json_user)

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "User created", "user": json_user}
    ) """

    return {
        "message": "User created",
        "user": user.to_dict()
    }

@user_router.put("/ops/{user_id}")
async def update_user(user_id: int, user_input: UserInput):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.update(
        name = user_input.name,
        email = user_input.email,
        password = user_input.password
    )

    updated_user = User.from_id(user_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "User updated", "user": updated_user.to_dict()}
    )

@user_router.delete("/ops/{user_id}")
async def delete_user(user_id: int):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found")
    
    user.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "User deleted"}
    )

@user_router.get("/protected-route")
async def protected_route(current_user: User = Depends(get_current_user)):
    if current_user is None:
        raise HTTPException(status_code = 401, detail = "Not authenticated")
    return f'Hello {current_user.name}, this route is protected'