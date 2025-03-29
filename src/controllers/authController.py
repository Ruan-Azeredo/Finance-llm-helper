from peewee import DoesNotExist
from fastapi import APIRouter, HTTPException, Request, status, Depends
import secrets
import time

from auth import Security
from models import User
from schemas import LoginInput, ResetPassword, ForgotPassword
from .utilsController import *
from services import SendPasswordResetEmail

auth_router = APIRouter()

auth_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])

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

    access_token = Security.create_jwt_token(data = {"sub": user.email}, type = "access")
    refresh_token = Security.create_jwt_token(data = {"sub": user.email}, type = "refresh")

    return {
        "access_token": { "token": access_token, "token_type": "bearer" },
        "refresh_token": { "token": refresh_token, "token_type": "bearer" }
    }

@auth_router.get("/get-access-token")
async def get_access_token(request: Request):

    try:
        auth_header = request.headers.get("Authorization")
        if auth_header is None or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Token inválido"
            )
        
        token = auth_header.split(" ")[1]
        payload = Security.validate_token(token = token, type = "refresh")
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Token inválido"
            )
        
        print('payload', payload)

        if payload:
            access_token = Security.create_jwt_token(data = {"sub": email}, type = "access")
            return {"access_token": access_token, "token_type": "bearer"}
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = str(error)
        )
    
# Simulando um banco de dados para armazenar tokens de redefinição de senha temporariamente
password_reset_tokens = {}

@auth_router.post("/forgot-password")
async def forgot_password(forgot_password: ForgotPassword):
    try:
        User.get_user_by_email(forgot_password.email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Gerar token único de redefinição de senha
    reset_token = secrets.token_hex(32)
    password_reset_tokens[forgot_password.email] = {"token": reset_token, "expires": time.time() + 3600}  # Expira em 1 hora

    # Enviar e-mail com link de redefinição de senha
    SendPasswordResetEmail(forgot_password.email, reset_token)

    return {"message": "E-mail de recuperação enviado!"}


@auth_router.post("/reset-password")
async def reset_password(reset_password: ResetPassword):

    try:
        User.get_user_by_email(reset_password.email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verificar se o token é válido
    if reset_password.email not in password_reset_tokens or password_reset_tokens[reset_password.email]["token"] != reset_password.token:
        raise HTTPException(status_code=400, detail="Token inválido ou expirado")

    if time.time() > password_reset_tokens[reset_password.email]["expires"]:
        raise HTTPException(status_code=400, detail="Token expirado")

    try:
        user: User = User.get_user_by_email(reset_password.email)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Atualizar a senha do usuário
    user = User.get_user_by_email(reset_password.email)
    user.update(password = reset_password.new_password)

    # Remover o token após o uso
    del password_reset_tokens[reset_password.email]

    return {"message": "Senha redefinida com sucesso!"}
    
auth_router.include_router(auth_router_auth)