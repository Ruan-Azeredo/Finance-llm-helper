from peewee import SqliteDatabase, Model, CharField, IntegerField, DateTimeField
from datetime import datetime

db = SqliteDatabase('database.db')

class User(Model):
    id = IntegerField(unique = True, primary_key = True)
    name = CharField()
    email = CharField(unique = True)
    password = CharField()
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'user'

    def __str__(self):
        return f'User: {self.id}, {self.name}, {self.email}'
    
    def create(**kwargs):

        if 'password' in kwargs:
            kwargs['password'] = hash(kwargs['password'])

        return super(User, User).create(**kwargs)