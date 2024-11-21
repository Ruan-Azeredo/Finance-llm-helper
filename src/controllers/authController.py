from peewee import DoesNotExist
from fastapi import APIRouter, HTTPException, Request, status

from auth import Security
from models import User
from schemas import LoginInput

auth_router = APIRouter()


@auth_router.post("/login")
async def login(user_input: LoginInput):
    
    email_or_password_invalid = HTTPException(status_code = 400, detail = "Email ou senha inválido")
    
    try:
        user: User = User.get_user_by_email(user_input.email)
    except DoesNotExist:
        raise email_or_password_invalid

    if not user or not Security.verify_password(
        plain_password = user_input.password,
        hashed_password = user.password
    ):
        raise email_or_password_invalid

    access_token = Security.create_jwt_token(data = {"sub": user.email})
    refresh_token = Security.create_jwt_token(data = {"sub": user.email})

    return {
        "access_token": { "token": access_token, "token_type": "bearer" },
        "refresh_token": { "token": refresh_token, "token_type": "bearer" }
    }

@auth_router.get("/get-access-token")
async def get_access_token(request: Request):

    try:
        payload = Security.validate_token(token = request.headers["Authorization"], type = "refresh")
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Token inválido"
            )

        if payload:
            access_token = Security.create_jwt_token(data = {"sub": email}, type = "access")
            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = str(error)
        )
    
