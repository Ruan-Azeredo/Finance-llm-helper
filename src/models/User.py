from peewee import CharField, IntegerField, DateTimeField, IntegrityError, DoesNotExist
from datetime import datetime
from typing import Callable, Any

from models import BaseModel
from database import db

def handle_database_error(method: Callable[..., Any]) -> Callable[..., Any] | None:
    def wrapper(*args, **kwargs):

        unique_fields = ['id', 'email']

        try:
            return method(*args, **kwargs)
        except IntegrityError as error:
            if 'UNIQUE constraint failed' in str(error):
                for field in unique_fields:
                    if field in str(error):
                        raise Exception(f"Chave duplicada: {field} já existente")
            else:
                raise Exception(f"Erro interno de integridade: {error}")
        except Exception as error:
            raise Exception(f"Erro interno: {error}")
    return wrapper

class User(BaseModel):
    id = IntegerField(unique = True, primary_key = True)
    name = CharField()
    email = CharField(unique = True)
    password = CharField()
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'users'


    def __str__(self) -> str:

        return f'User: {self.id}, {self.name}, {self.email}'
    
    @handle_database_error
    def create(**kwargs) -> 'User':

        if 'password' in kwargs:
            kwargs['password'] = hash(kwargs['password'])

        return super(User, User).create(**kwargs)
    
    @handle_database_error
    def update(self, **kwargs) -> None:

        if 'password' in kwargs:
            kwargs['password'] = hash(kwargs['password'])

        super(User, self).update(**kwargs)

    def get_user_by_email(email: str) -> 'User':
        try:
            return User.get(User.email == email)
        except DoesNotExist:
            raise DoesNotExist(f"Email inválido")
        except Exception as error:
            raise Exception(f"Não foi possivel identificar o usuario atravez deste email: {error}")
        