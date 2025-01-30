from fastapi import APIRouter, Depends, HTTPException, status, Request, Path
from typing import Optional
from fastapi.responses import JSONResponse
from functools import wraps
from pydantic import BaseModel

from models import User
from schemas import UserCRUDInput
from .utilsController import *

user_router = APIRouter()

user_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])
user_router_admin = APIRouter(dependencies = [Depends(verify_admin_access_user)])

@user_router_admin.get("/ops")
async def get_users():

    users: list[User] = User.all()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"users": [user.to_dict() for user in users]}
    )

@user_router_auth.get("/ops/{user_id}")
async def get_user(user_id: int):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "Usuário não encontrado")
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"user": user.to_dict()}
    )

@user_router.post("/ops")
async def create_user(user_input: UserCRUDInput):

    user = User.create(
        **user_input.to_dict()
    )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Usuário criado", "user": user.to_dict()}
    )

@user_router_auth.put("/ops/{user_id}")
async def update_user(user_id: int, user_input: UserCRUDInput):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "Usuário não encontrado")
    
    user.update(
        **user_input.to_dict()
    )

    updated_user = User.from_id(user_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Usuário atualizado", "user": updated_user.to_dict()}
    )

@user_router_auth.delete("/ops/{user_id}")
async def delete_user(*, user_id: int):

    user = User.from_id(user_id)

    if not user:
        raise HTTPException(status_code = 404, detail = "Usuário não encontrado")
    
    user.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Usuário deletado"}
    )

@user_router_auth.get("/protected-route")
async def protected_route(current_user: User = Depends(User.get_current_user)):
    if current_user is None:
        raise HTTPException(status_code = 401, detail = "Not authenticated")
    return f'Hello {current_user.name}, this route is protected'

user_router.include_router(user_router_auth)
user_router.include_router(user_router_admin)