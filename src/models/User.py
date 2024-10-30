from peewee import SqliteDatabase, Model, CharField
import os
import asyncio

db = SqliteDatabase('database.db')

class UserTable(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class User(UserTable):

    def __str__(self):
        return f'User: {self.id}, {self.name}, {self.email}, {self.password}'

    async def create(self):
        UserTable.create(
            id = self.id,
            name = self.name,
            email = self.email,
            password = self.password
        )

        return self

async def ops():
    db.connect()
    db.create_tables([UserTable])

    new_user = await User(
        id = 1,
        name = 'name',
        email = 'email',
        password = 'password'
    ).create()
    print(new_user.__str__(), type(new_user))

    users: UserTable = list(UserTable.select().execute())

    for user in users:
        print(user.__str__(), type(user))
    
    
    
    
    os.remove('database.db')


asyncio.run(ops())