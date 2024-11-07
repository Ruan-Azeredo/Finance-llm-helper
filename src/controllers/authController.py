from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import verify_password, create_access_token
from models import User

auth_router = APIRouter()

class UserInput(BaseModel):
    email: str
    password: str


@auth_router.post("/login")
async def login(user_input: UserInput):
    user = User.get_user_by_email(user_input.email)

    if not user or not int(user.password) == hash(user_input.password):
        raise HTTPException(status_code = 400, detail = "Email ou senha inválidos")

    access_token = create_access_token(data = {"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}