from peewee import PostgresqlDatabase
import pytest

from models import User
from auth import Security
from testUtils import db_session

def test_create_user_model(db_session):
    
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    assert user.__str__() == 'User: 1, name, email@email.com, free'
    assert Security.verify_password(plain_password = 'password', hashed_password = user.password)

def test_create_user_model_with_id(db_session):
    
    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    assert user.__str__() == 'User: 1, name, email@email.com, free'
    assert Security.verify_password(plain_password = 'password', hashed_password = user.password)

def test_create_user_model_with_existing_email(db_session):

    User.create(
        name = 'Ruan',
        email = 'email@email.com',
        password = '1234'
    )
    
    with pytest.raises(Exception) as error:
        User.create(
            name = 'name',
            email = 'email@email.com',
            password = 'password'
        )
    
    assert 'Chave duplicada: email já existente' in str(error.value)

def test_create_user_model_with_existing_id(db_session):

    User.create(
        id = 1,
        name = 'Ruan',
        email = 'email@email.com',
        password = '1234'
    )   
    
    with pytest.raises(Exception) as error:
        User.create(
            id = 1,
            name = 'name',
            email = 'email@email.com',
            password = 'password'
        )
    
    assert 'Chave duplicada: id já existente' in str(error.value)

def test_get_user_model(db_session):
    
    User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user_from_db: User = User.from_id(id = 1)
    
    assert user_from_db.__str__() == 'User: 1, name, email@email.com, free'
    assert user_from_db.name == 'name'
    assert user_from_db.email == 'email@email.com'
    assert Security.verify_password(plain_password = 'password', hashed_password = user_from_db.password)

def test_get_all_users_model(db_session):
    
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

    users_from_db: User = User.all()
    
    assert len(users_from_db) == 2
    assert users_from_db[0].__str__() == 'User: 1, name, email@email.com, free'
    assert users_from_db[1].__str__() == 'User: 2, name, email@gmail.com, free'

def test_update_user_model(db_session):
    
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

    user: User = User.select().where(User.id == 1).get()
    
    assert user.__str__() == 'User: 1, Ruan, email@email.com, free'
    assert user.name == 'Ruan'

def test_update_few_fields_user_model(db_session):
    
    user: User = User.create(
        id = 12,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.update(
        name = 'Ruan',
    )

    user = User.select().where(User.id == 12).get()
    
    assert user.__str__() == 'User: 12, Ruan, email@email.com, free'

def test_delete_user_model(db_session):
    
    user: User = User.create(
        id = 12,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.delete()
    
    assert not User.select().where(User.id == 12).exists()