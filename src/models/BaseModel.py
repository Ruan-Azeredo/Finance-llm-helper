from peewee import Model, DoesNotExist
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

        return list(cls.select())

    @classmethod
    def from_id(cls: Type[T], id: int) -> T:

        try:
            return cls.get(cls.id == id)
        except DoesNotExist:
            return None

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:

        return super().create(**kwargs)
  
    def update(self: T, **kwargs) -> None:

        super(BaseModel, self).update(**kwargs).where(self.__class__.id == self.id).execute()

    def delete(self: T) -> None:

        super(BaseModel, self).delete().where(self.__class__.id == self.id).execute()