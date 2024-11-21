import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from typing import Literal
from dotenv import load_dotenv
import os

from .config import (
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES, 
    JWT_REFRESH_TOKEN_EXPIRE_DAYS
)


class Security:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def encrypt_password(password: str) -> str:
        return Security.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return Security.pwd_context.verify(plain_password, hashed_password)

    def _load_env_environment():

        load_dotenv()

        JWT_ACCESS_TOKEN_SECRET = os.getenv("JWT_ACCESS_TOKEN_SECRET")
        JWT_REFRESH_TOKEN_SECRET = os.getenv("JWT_REFRESH_TOKEN_SECRET")
        JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

        if not all([JWT_ACCESS_TOKEN_SECRET, JWT_REFRESH_TOKEN_SECRET, JWT_ALGORITHM]):
            raise ValueError("Uma ou mais variáveis de ambiente não foram carregadas corretamente!")
        
        return JWT_ACCESS_TOKEN_SECRET, JWT_REFRESH_TOKEN_SECRET, JWT_ALGORITHM
    
    @staticmethod
    def create_jwt_token(data: dict, type: Literal["access", "refresh"] = "access", expires_delta: timedelta = None) -> str:
        """
        Cria um token (JWT) com dados e expiração.
        :param data: Dados a serem incluídos no token.
        :param expires_delta: Tempo de expiração. Por padrão, usa o tempo configurado.
        :return: Token JWT como string.
        """
        JWT_ACCESS_TOKEN_SECRET, JWT_REFRESH_TOKEN_SECRET, JWT_ALGORITHM = Security._load_env_environment()

        to_encode = data.copy()
        if type == "access":
            expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, JWT_ACCESS_TOKEN_SECRET, algorithm=JWT_ALGORITHM)
        elif type == "refresh":
            expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=JWT_REFRESH_TOKEN_EXPIRE_DAYS))
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_TOKEN_SECRET, algorithm=JWT_ALGORITHM)

        return encoded_jwt

    @staticmethod
    def validate_token(token: str, type: Literal["access", "refresh"] = "access") -> dict:
        """
        Valida um token JWT.
        :param token: O token a ser validado.
        :return: O payload decodificado, ou levanta um erro se inválido/expirado.
        """

        JWT_ACCESS_TOKEN_SECRET, JWT_REFRESH_TOKEN_SECRET, JWT_ALGORITHM = Security._load_env_environment()

        try:
            if type == "access":
                payload = jwt.decode(token, JWT_ACCESS_TOKEN_SECRET, algorithms=[JWT_ALGORITHM])
            elif type == "refresh":
                payload = jwt.decode(token, JWT_REFRESH_TOKEN_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            print("Erro: Token expirado")
            raise jwt.ExpiredSignatureError("Token expirado")
        except jwt.InvalidTokenError as error:
            print(f"Erro: Token inválido. Detalhes: {error}")
            raise jwt.InvalidTokenError(f"Token inválido: {error}")

