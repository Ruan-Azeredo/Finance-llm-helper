from models import User
from src.controllers.authController import login
from schemas import LoginInput

import pytest
from peewee import SqliteDatabase
from fastapi import HTTPException

def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    User._meta.database = test_db

    test_db.connect()
    test_db.create_tables([User])

    return test_db

@pytest.mark.asyncio
async def test_login():
    test_db = setupTestDatabase()
    
    user = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user_input = LoginInput(
        email = 'email@email.com',
        password = 'password'
    )

    user = await login(user_input)

    assert user["access_token"] != None
    assert user["token_type"] == "bearer"

    test_db.close()

@pytest.mark.asyncio
async def test_failed_to_login():
    test_db = setupTestDatabase()
    
    User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user_input = LoginInput(
        email = 'wrong_email@email.com',
        password = 'password'
    )

    with pytest.raises(HTTPException) as error:
        await login(user_input)

    assert error.value.status_code == 400
    assert error.value.detail == 'Email ou senha inválido'

    test_db.close()