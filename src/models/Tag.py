from .BaseModel import BaseModel
from peewee import CharField, IntegerField, ForeignKeyField, DoesNotExist, DateTimeField
from datetime import datetime

from .handles import handle_values, handle_database_error
from database import db
from models import User
from utils import default_users_tags, validate_tag_input

class Tag(BaseModel):
    id = IntegerField(unique = True, primary_key = True)
    name = CharField(unique = True, null = False)
    color = IntegerField(default = 0, null = False)
    user_id = ForeignKeyField(User, field='id', backref='tags', on_delete='CASCADE')
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'tags'


    @handle_database_error
    def create(user_id: int, **kwargs) -> 'Tag':

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        validate_tag_input(kwargs)

        values = handle_values(kwargs)
        values['user_id'] = user_id

        return super(Tag, Tag).create(**values)
    
    @handle_database_error
    def update(self, **kwargs) -> None:

        validate_tag_input(kwargs)

        values = handle_values(kwargs)

        super(Tag, self).update(**values)

    @handle_database_error
    def delete(self) -> None:

        user_tags = Tag.select().where(Tag.user_id == self.user_id)

        if len(user_tags) == 1:
            raise Exception("O usuario precisa ter pelo menos uma tag")

        super(Tag, self).delete()

    @handle_database_error
    def get_tags_by_user_id(user_id: int) -> list['Tag']:

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")


        return Tag.select().where(Tag.user_id == user_id)
    
    @handle_database_error
    def create_default_tags(user_id: int) -> None:

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        for tag in default_users_tags:
            print("\n", tag)
            Tag.create(
                user_id = user_id,
                **tag
            )
