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

    users = User.all()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"users": [user.to_dict()for user in users]}
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

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "User created", "user": user.to_dict()}
    )

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