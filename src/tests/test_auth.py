from auth import create_access_token, verify_password, get_current_user
from models import User

import pytest
from peewee import SqliteDatabase



def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    User._meta.database = test_db

    return test_db



def test_create_access_token():
    token = create_access_token(data={"sub": "test"})
    assert token
    assert isinstance(token, str)

def test_verify_password():

    hashes_pass = hash("password")
    str_hashed_pass = str(hashes_pass)

    assert verify_password(plain_password = "password", hashed_password = str_hashed_pass)
    assert not verify_password(plain_password = "password1", hashed_password = str_hashed_pass)

def test_get_current_user():


    with pytest.raises(Exception) as error:
        token = create_access_token(data={"sub": "test"})
        user = get_current_user(token)

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

    token = create_access_token(data={"sub": "email@email.com"})
    user = get_current_user(token)
    
    assert user