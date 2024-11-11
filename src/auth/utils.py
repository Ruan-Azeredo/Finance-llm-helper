from auth import JWT_SECRET, JWT_ALGORITHM
from models import User

from fastapi import Depends, HTTPException, status, Request
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWTError

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Não foi possivel validar as credenciais",
    headers={"WWW-Authenticate": "Bearer"},
)

class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except Exception:
            raise credentials_exception

oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

    except PyJWTError:
        raise credentials_exception
    
    user = User.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user