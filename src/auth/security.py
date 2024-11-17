import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from .config import JWT_SECRET, JWT_ALGORITHM, JWT_ACCESS_TOKEN_EXPIRE_MINUTES

class Security:

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt_password(password: str) -> str:
        return Security.pwd_context.hash(password)

    def verify_password(plain_password, hashed_password) -> bool:
        return Security.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt