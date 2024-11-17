from models import User
from auth import Security

import pytest
from peewee import SqliteDatabase



def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    User._meta.database = test_db

    return test_db



def test_create_access_token():
    token = Security.create_access_token(data={"sub": "test"})
    assert token
    assert isinstance(token, str)

def test_verify_password():

    hashes_pass = Security.encrypt_password("password")

    assert Security.verify_password(plain_password = "password", hashed_password = hashes_pass)
    assert not Security.verify_password(plain_password = "password1", hashed_password = hashes_pass)

def test_get_current_user():


    with pytest.raises(Exception) as error:
        token = Security.create_access_token(data={"sub": "test"})
        user = User.get_current_user(token)

        assert user is None
    
    assert "Email inválido" in str(error.value)

    test_db = setupTestDatabase()
    
    test_db.connect()
    test_db.create_tables([User])
    
    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    token = Security.create_access_token(data={"sub": "email@email.com"})
    user = User.get_current_user(token)
    
    assert user