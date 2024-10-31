from peewee import SqliteDatabase

from models import User

def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    User._meta.database = test_db

    return test_db

def test_create_user_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    user = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    assert user.__str__() == 'User: 1, name, email@email.com'
    assert user.password == hash('password')

def test_get_user_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user_from_db = User.fromId(id = 1)
    
    assert user_from_db.__str__() == 'User: 1, name, email@email.com'
    assert user_from_db.name == 'name'
    assert user_from_db.email == 'email@email.com'
    assert int(user_from_db.password) == hash('password')

def test_get_all_users_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    User.create(
        id = 2,
        name = 'name',
        email = 'email@gmail.com',
        password = 'password'
    )

    users_from_db = User.all()
    
    assert len(users_from_db) == 2
    assert users_from_db[0].__str__() == 'User: 1, name, email@email.com'
    assert users_from_db[1].__str__() == 'User: 2, name, email@gmail.com'

def test_update_user_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    user = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.update(
        id = 1,
        name = 'Ruan',
        email = 'email@email.com',
        password = 'password'
    )

    user = User.select().where(User.id == 1).get()
    
    assert user.__str__() == 'User: 1, Ruan, email@email.com'
    assert user.name == 'Ruan'

def test_update_few_fields_user_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    user = User.create(
        id = 12,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.update(
        name = 'Ruan',
    )

    user = User.select().where(User.id == 12).get()
    
    assert user.__str__() == 'User: 12, Ruan, email@email.com'

def test_delete_user_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    user = User.create(
        id = 12,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.delete()
    
    assert not User.select().where(User.id == 12).exists()