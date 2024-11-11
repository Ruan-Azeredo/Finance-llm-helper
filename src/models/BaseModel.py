from peewee import Model, DoesNotExist, OperationalError, IntegrityError, IntegerField
from typing import Type, TypeVar, List, Callable
from datetime import datetime

from database import db

T = TypeVar('T', bound='BaseModel')

def handle_database_error(method: Callable[..., T]) -> Callable[..., T] | None:
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except OperationalError as error:
            if 'no such table' in str(error):
                existent_tables = args[0]._meta.database.get_tables()
                raise Exception(f"Tabela '{args[0]._meta.table_name}' não existe, as unicas tabelas existentes são: {existent_tables}")
            else:
                raise Exception(f"Erro interno: {error}")
        except DoesNotExist:
            return None
        except IntegrityError as error:
            raise IntegrityError(error.args[0])
        except Exception as error:
            raise Exception(f"Erro interno: {error}")
    return wrapper

class BaseModel(Model):
    class Meta: 
        database = db

    def to_dict(cls: Type[T]) -> dict:
        data = {}
        for field in cls._meta.sorted_fields:
            value = getattr(cls, field.name)

            if isinstance(value, datetime):
                data[field.name] = value.isoformat()
            else:
                data[field.name] = value
        return data
    
    @classmethod
    @handle_database_error
    def all(cls: Type[T]) -> List[T]:
        return list(cls.select())

    @classmethod
    @handle_database_error
    def from_id(cls: Type[T], id: int) -> T:
        return cls.get(cls.id == id)

    @classmethod
    @handle_database_error
    def create(cls: Type[T], **kwargs) -> T:
        return super().create(**kwargs)

    @handle_database_error
    def update(self: T, **kwargs) -> None:
        super(BaseModel, self).update(**kwargs).where(self.__class__.id == self.id).execute()

    @handle_database_error
    def delete(self: T) -> None:
        super(BaseModel, self).delete().where(self.__class__.id == self.id).execute() 