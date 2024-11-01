from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models import User

class UserInput(BaseModel):
    name: str
    email: str
    password: str

user_router = APIRouter()

@user_router.get("/")
async def get_users():
    try:
        users = User.all()
        return {"users": [str(user) for user in users]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.get("/{user_id}")
async def get_user(user_id: int):
    try:
        user = User.from_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {"user": str(user)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.post("/")
async def create_user(user_input: UserInput):
    try:
        user = User.create(
            name = user_input.name,
            email = user_input.email,
            password = user_input.password
        )
        return {"message": "User created", "user": str(user)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.put("/{user_id}")
async def update_user(user_id: int, user_input: UserInput):
    try:
        user = User.from_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.update(
            name = user_input.name,
            email = user_input.email,
            password = user_input.password
        )
        return {"message": "User updated", "user": str(user)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@user_router.delete("/{user_id}")
async def delete_user(user_id: int):
    try:
        user = User.from_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.delete()
        return {"message": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))