from models import User
from auth import Security
from testUtils import db_session

import pytest
from peewee import PostgresqlDatabase


def test_create_access_token(db_session):
    token = Security.create_jwt_token(data={"sub": "test"}, type="access")
    assert token
    assert isinstance(token, str)

def test_verify_password(db_session):

    hashes_pass = Security.encrypt_password("password")

    assert Security.verify_password(plain_password = "password", hashed_password = hashes_pass)
    assert not Security.verify_password(plain_password = "password1", hashed_password = hashes_pass)

def test_get_current_user(db_session):


    with pytest.raises(Exception) as error:
        token = Security.create_jwt_token(data={"sub": "test"})
        user = User.get_current_user(token)

        assert user is None
    
    assert "Email inválido" in str(error.value)
    
    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    token = Security.create_jwt_token(data={"sub": "email@email.com"})
    user = User.get_current_user(token)
    
    assert user