from peewee import DoesNotExist
from fastapi import APIRouter, HTTPException

from auth import create_access_token, verify_password
from models import User
from schemas import LoginInput

auth_router = APIRouter()

email_or_password_invalid = HTTPException(status_code = 400, detail = "Email ou senha inválido")

@auth_router.post("/login")
async def login(user_input: LoginInput):
    try:
        user = User.get_user_by_email(user_input.email)
    except DoesNotExist:
        raise email_or_password_invalid

    if not user or not verify_password(
        plain_password = user_input.password,
        hashed_password = user.password
    ):
        raise email_or_password_invalid

    access_token = create_access_token(data = {"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}