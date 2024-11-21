from fastapi import HTTPException, status, Request
from typing import Optional
from fastapi.security import OAuth2PasswordBearer

class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except Exception as error:
            print(f"Erro ao obter token: {error}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Erro ao obter token",
                headers={"WWW-Authenticate": "Bearer"},
            )

oauth2_scheme = CustomOAuth2PasswordBearer(tokenUrl="login")
