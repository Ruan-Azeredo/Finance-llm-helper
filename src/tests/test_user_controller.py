from models import User
from src.controllers.userController import UserInput, get_users, get_user, create_user, update_user, delete_user

import pytest
from peewee import SqliteDatabase
from fastapi import HTTPException
import json

def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    User._meta.database = test_db

    test_db.connect()
    test_db.create_tables([User])

    return test_db

def test_user_table_exists():

    test_db = setupTestDatabase()
    
    assert test_db.table_exists('users') == True

@pytest.mark.asyncio
async def test_get_users():

    test_db = setupTestDatabase()

    response = await get_users()

    response_body_json = json.loads(response.body)

    assert test_db.table_exists('users') == True
    assert response_body_json == {"users": []}

@pytest.mark.asyncio
async def test_create_user():

    setupTestDatabase()

    user_data = UserInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    response = await create_user(user_input = user_data)

    response_body_json = json.loads(response.body)

    assert response_body_json["message"] == "User created"
    assert response_body_json["user"]["name"] == "Ruan"
    assert response_body_json["user"]["email"] == "ruan@gmail.com"

@pytest.mark.asyncio
async def test_get_user():

    setupTestDatabase()

    user_data = UserInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await create_user(user_input = user_data)

    response = await get_user(user_id = 1)

    response_body_json = json.loads(response.body)

    assert response_body_json["user"]["id"] == 1
    assert response_body_json["user"]["name"] == "Ruan"
    assert response_body_json["user"]["email"] == "ruan@gmail.com"

@pytest.mark.asyncio
async def test_update_user():

    setupTestDatabase()

    user_data = UserInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await create_user(user_input = user_data)

    update_user_data = UserInput(
        name = "Ruan Azeredo",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await update_user(user_id = 1, user_input = update_user_data)

    response = await get_user(user_id = 1)

    response_body_json = json.loads(response.body)

    assert response_body_json["user"]["name"] == "Ruan Azeredo"

@pytest.mark.asyncio
async def test_user_not_found():

    setupTestDatabase()

    with pytest.raises(HTTPException) as error:
        await get_user(user_id = 1)

    assert error.value.detail == "User not found"
    assert error.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_user():

    setupTestDatabase()

    user_data = UserInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await create_user(user_input = user_data)

    response = await delete_user(user_id = 1)

    response_body_json = json.loads(response.body)

    with pytest.raises(HTTPException) as error:
        await get_user(user_id = 1)

    assert response_body_json["message"] == "User deleted"
    assert error.value.detail == "User not found"
    assert error.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_not_found():

    setupTestDatabase()

    with pytest.raises(HTTPException) as error:
        await delete_user(user_id = 1)

    assert error.value.detail == "User not found"
    assert error.value.status_code == 404

@pytest.mark.asyncio
async def test_update_user_not_found():

    setupTestDatabase()

    update_user_data = UserInput(
        name = "Ruan Azeredo",
        email = "ruan@gmail.com",
        password = "1234"
    )

    with pytest.raises(HTTPException) as error:
        await update_user(user_id = 1, user_input = update_user_data)

    assert error.value.detail == "User not found"
    assert error.value.status_code == 404