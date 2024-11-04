from peewee import Model, DoesNotExist, OperationalError
from typing import Type, TypeVar, List
from database import db

T = TypeVar('T', bound='BaseModel')

class BaseModel(Model):
    class Meta:
        database = db

    def to_dict(self) -> dict:
        return {field.name: getattr(self, field.name) for field in self._meta.sorted_fields}
    
    @classmethod
    def all(cls: Type[T]) -> List[T]:

        """ if not cls._meta.database.table_exists(cls._meta.database.table_name):
            raise Exception(f"A tabela {cls._meta.database.table_name} não existe") """

        try:
            return list(cls.select())
        
        except OperationalError as error:
            if 'no such table' in str(error):
                raise Exception(f"Tabela {cls._meta.table_name} não existe")
            else:
                raise Exception(f"Erro ao Listar o registro: {error}")
        except Exception as error:
            raise Exception(f"Erro ao listar os registros: {error}")

    @classmethod
    def from_id(cls: Type[T], id: int) -> T:

        try:
            return cls.get(cls.id == id)
        
        except OperationalError as error:
            if 'no such table' in str(error):
                raise Exception(f"Tabela {cls._meta.table_name} não existe")
            else:
                raise Exception(f"Erro ao criar o registro: {error}")
        except DoesNotExist:
            return None

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:

        try:
            return super().create(**kwargs)
        
        except OperationalError as error:
            if 'no such table' in str(error):
                raise Exception(f"Tabela {cls._meta.table_name} não existe")
            else:
                raise Exception(f"Erro ao criar o registro: {error}")
        except Exception as error:
            raise Exception(f"Erro ao criar o registro: {error}")
  
    def update(self: T, **kwargs) -> None:

        try:
            super(BaseModel, self).update(**kwargs).where(self.__class__.id == self.id).execute()

        except OperationalError as error:
            if 'no such table' in str(error):
                raise Exception(f"Tabela {self._meta.table_name} não existe")
            else:
                raise Exception(f"Erro ao atualizar o registro: {error}")
        except Exception as error:
            raise Exception(f"Erro ao atualizar o registro: {error}")

    def delete(self: T) -> None:

        try:
            super(BaseModel, self).delete().where(self.__class__.id == self.id).execute()

        except OperationalError as error:
            if 'no such table' in str(error):
                raise Exception(f"Tabela {self._meta.table_name} não existe")
            else:
                raise Exception(f"Erro ao deletar o registro: {error}")
        except Exception as error:
            raise Exception(f"Erro ao deletar o registro: {error}")    