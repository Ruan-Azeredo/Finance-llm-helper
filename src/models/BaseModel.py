from peewee import Model, DoesNotExist, OperationalError
from typing import Type, TypeVar, List, Callable
from database import db

T = TypeVar('T', bound='BaseModel')

def handle_database_error(method: Callable[..., T]) -> Callable[..., T] | None:
    def wrapper(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except OperationalError as error:
            if 'no such table' in str(error):
                raise Exception(f"Tabela {args[0]._meta.table_name} não existe")
            else:
                raise Exception(f"Erro interno: {error}")
        except DoesNotExist:
            return None
        except Exception as error:
            raise Exception(f"Erro interno: {error}")
    return wrapper

class BaseModel(Model):
    class Meta:
        database = db

    def to_dict(self) -> dict:
        return {field.name: getattr(self, field.name) for field in self._meta.sorted_fields}
    
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