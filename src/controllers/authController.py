from fastapi import APIRouter, HTTPException
from auth import verify_password, create_access_token
from models import User

router = APIRouter()

class UserInput:
    email: str
    password: str


@router.post("/login")
async def login(user_input: UserInput):
    user = User.get_user_by_email(user_input.email)

    if not user or not verify_password(user_input.password, user.password):
        raise HTTPException(status_code = 400, detail = "Email ou senha inválidos")

    access_token = create_access_token(data = {"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}