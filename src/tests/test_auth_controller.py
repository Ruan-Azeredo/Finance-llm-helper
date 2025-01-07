from models import User
from src.controllers.authController import login
from schemas import LoginInput
from testUtils import db_session

import pytest
from peewee import SqliteDatabase
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_login(db_session):

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

    resp = await login(user_input)

    assert resp["access_token"]["token"] != None
    assert resp["access_token"]["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_failed_to_login(db_session):
    
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
