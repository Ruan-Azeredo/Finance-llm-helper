from models import User
from src.controllers.userController import get_users, get_user, create_user, update_user, delete_user
from schemas import UserCRUDInput
from testUtils import test_db, db_session

import pytest
from fastapi import HTTPException
import json

def test_user_table_exists(test_db):

    print(test_db)

    test_db.create_tables([User])
    
    assert test_db.table_exists('users') == True

@pytest.mark.asyncio
async def test_get_users(test_db):

    test_db.create_tables([User])

    response = await get_users()

    response_body_json = json.loads(response.body)

    assert test_db.table_exists('users') == True
    assert response_body_json == {"users": []}

@pytest.mark.asyncio
async def test_create_user(db_session):

    user_data = UserCRUDInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    response = await create_user(user_input = user_data)

    response_body_json = json.loads(response.body)

    assert response_body_json["message"] == "Usuário criado"
    assert response_body_json["user"]["name"] == "Ruan"
    assert response_body_json["user"]["email"] == "ruan@gmail.com"

@pytest.mark.asyncio
async def test_get_user(db_session):

    user_data = UserCRUDInput(
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
async def test_update_user(db_session):

    user_data = UserCRUDInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await create_user(user_input = user_data)

    update_user_data = UserCRUDInput(
        name = "Ruan Azeredo",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await update_user(user_id = 1, user_input = update_user_data)

    response = await get_user(user_id = 1)

    response_body_json = json.loads(response.body)

    assert response_body_json["user"]["name"] == "Ruan Azeredo"

@pytest.mark.asyncio
async def test_user_not_found(db_session):

    with pytest.raises(HTTPException) as error:
        await get_user(user_id = 1)

    assert error.value.detail == "Usuário não encontrado"
    assert error.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_user(db_session):

    user_data = UserCRUDInput(
        name = "Ruan",
        email = "ruan@gmail.com",
        password = "1234"
    )

    await create_user(user_input = user_data)

    response = await delete_user(user_id = 1)

    response_body_json = json.loads(response.body)

    with pytest.raises(HTTPException) as error:
        await get_user(user_id = 1)

    assert response_body_json["message"] == "Usuário deletado"
    assert error.value.detail == "Usuário não encontrado"
    assert error.value.status_code == 404

@pytest.mark.asyncio
async def test_delete_user_not_found(db_session):

    with pytest.raises(HTTPException) as error:
        await delete_user(user_id = 1)

    assert error.value.detail == "Usuário não encontrado"
    assert error.value.status_code == 404

@pytest.mark.asyncio
async def test_update_user_not_found(db_session):

    update_user_data = UserCRUDInput(
        name = "Ruan Azeredo",
        email = "ruan@gmail.com",
        password = "1234"
    )

    with pytest.raises(HTTPException) as error:
        await update_user(user_id = 1, user_input = update_user_data)

    assert error.value.detail == "Usuário não encontrado"
    assert error.value.status_code == 404