from peewee import CharField, DateTimeField, AutoField, DoesNotExist
from datetime import datetime
from fastapi import Depends, HTTPException, status
import jwt

from .BaseModel import BaseModel
from auth import Security, oauth2_scheme
from database import db
from .handles import handle_values, handle_database_error

class User(BaseModel):
    id = AutoField(unique = True, primary_key = True)
    name = CharField()
    email = CharField(unique = True)
    password = CharField()
    role = CharField(default = "free")
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'users'


    def __str__(self) -> str:

        return f'User: {self.id}, {self.name}, {self.email}, {self.role}'
    
    def to_dict(self) -> dict:
        user = super().to_dict()
        if 'password' in user:
            del user['password']
        return user
    
    @handle_database_error
    def create(**kwargs) -> 'User':

        values = handle_values(kwargs)

        if 'password' in values:
            values['password'] = Security.encrypt_password(values['password'])

        return super(User, User).create(**values)
    
    @handle_database_error
    def update(self, **kwargs) -> None:

        values = handle_values(kwargs)

        if 'password' in values:
            values['password'] = Security.encrypt_password(values['password'])

        super(User, self).update(**values)

    def get_user_by_email(email: str) -> 'User':
        try:
            return User.get(User.email == email)
        except DoesNotExist:
            raise DoesNotExist(f"Email inválido")
        except Exception as error:
            raise Exception(f"Não foi possivel identificar o usuario atravez deste email: {error}")

    def get_current_user(token: str = Depends(oauth2_scheme)):

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possivel validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = Security.validate_token(token = token, type = "access")
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception

        except jwt.ExpiredSignatureError:
            print("Erro: Token expirado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado",
            )
        except jwt.InvalidTokenError as error:
            print(f"Erro: Token inválido. Detalhes: {error}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
            )
        except Exception as error:
            print(f"Erro inesperado: {error}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Erro interno na validação do token: {error}",
            )
        
        user = User.get_user_by_email(email)

        if user is None:
            raise credentials_exception
        
        return user
        