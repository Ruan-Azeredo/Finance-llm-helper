from .BaseModel import BaseModel
from peewee import CharField, IntegerField, ForeignKeyField, DoesNotExist, DateTimeField, AutoField
from datetime import datetime

from .handles import handle_values, handle_database_error
from database import db
from models import User
from utils import default_users_categories, validate_category_input

class Category(BaseModel):
    id = AutoField(unique = True, primary_key = True)
    name = CharField(unique = True, null = False)
    color = IntegerField(default = 0, null = False)
    user_id = ForeignKeyField(User, field='id', backref='categories', on_delete='CASCADE')
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'categories'


    @handle_database_error
    def create(user_id: int, **kwargs) -> 'Category':

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        validate_category_input(kwargs)

        values = handle_values(kwargs)
        values['user_id'] = user_id

        return super(Category, Category).create(**values)
    
    @handle_database_error
    def update(self, **kwargs) -> None:

        validate_category_input(kwargs)

        values = handle_values(kwargs)

        super(Category, self).update(**values)

    @handle_database_error
    def delete(self) -> None:

        user_categories = Category.select().where(Category.user_id == self.user_id)

        if len(user_categories) == 1:
            raise Exception("O usuario precisa ter pelo menos uma category")

        super(Category, self).delete()

    @handle_database_error
    def get_categories_by_user_id(user_id: int) -> list['Category']:

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")


        return Category.select().where(Category.user_id == user_id)
    
    @handle_database_error
    def create_default_categories(user_id: int) -> None:

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        for category in default_users_categories:
            print("\n", category)
            Category.create(
                user_id = user_id,
                **category
            )
