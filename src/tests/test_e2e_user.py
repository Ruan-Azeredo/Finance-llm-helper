import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
import os

from src.server import app
from models import User

client = TestClient(app)

@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    test_db = SqliteDatabase('test.db')
    # Configuração do banco de dados
    User._meta.database = test_db
    test_db.connect()
    test_db.create_tables([User])
    yield
    # Teardown - Fecha a conexão e remove o arquivo do banco de dados
    test_db.drop_tables([User])
    test_db.close()
    if os.path.exists('test.db'):
        os.remove('test.db')

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_create_user_e2e():

    user_data = {
        "name": "Ruan",
        "email": "ruan@gmail",
        "password": "1234"
    }

    response = client.post('/user/ops', json = user_data)

    assert response.status_code == 200
    assert response.json()['message'] == "User created"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan@gmail"

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_get_user_e2e():

    user_data = {
        "name": "Ruan",
        "email": "ruan11@gmail",
        "password": "1234"
    }

    response = client.post('/user/ops', json = user_data)

    assert response.status_code == 200
    assert response.json()['message'] == "User created"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan11@gmail"

    response = client.get(f'/user/ops/{response.json()["user"]["id"]}')

    assert response.status_code == 200
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan11@gmail"

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_update_user_e2e():

    user_data = {
        "name": "Ruan",
        "email": "ruan22@gmail",
        "password": "1234"
    }

    response = client.post('/user/ops', json = user_data)

    assert response.status_code == 200
    assert response.json()['message'] == "User created"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan22@gmail"

    update_user_data = {
        "name": "Ruan Azeredo",
        "email": "ruan22@gmail",
        "password": "1234"
    }

    response = client.put(f'/user/ops/{response.json()["user"]["id"]}', json = update_user_data)

    assert response.status_code == 200
    assert response.json()['message'] == "User updated"
    assert response.json()['user']['name'] == "Ruan Azeredo"
    assert response.json()['user']['email'] == "ruan22@gmail"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_delete_user_e2e():

    user_data = {
        "name": "Ruan",
        "email": "ruan33@gmail",
        "password": "1234"
    }

    response = client.post('/user/ops', json = user_data)

    assert response.status_code == 200
    assert response.json()['message'] == "User created"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan33@gmail"

    response = client.delete(f'/user/ops/{response.json()["user"]["id"]}')

    assert response.status_code == 200
    assert response.json()['message'] == "User deleted"
