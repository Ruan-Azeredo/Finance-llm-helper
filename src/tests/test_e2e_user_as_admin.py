import pytest
from fastapi.testclient import TestClient

from utils import setupDatabaseFileWithTables
from src.server import app

client_test = TestClient(app)

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, is_admin = True)
async def test_create_user_e2e(authenticated_client: TestClient):

    user_data = {
        "name": "Ruan",
        "email": "ruan@gmail",
        "password": "1234",
    }

    response = authenticated_client.post('/user/ops', json = user_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan@gmail"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, is_admin = True)
async def test_get_user_e2e(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan11@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/ops', json = user_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan11@gmail"

    response = authenticated_client.get(f'/user/ops/{response.json()["user"]["id"]}')
    print(response.json())

    assert response.status_code == 200
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan11@gmail"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, is_admin = True)
async def test_update_user_e2e(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan22@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/ops', json = user_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan22@gmail"

    update_user_data = {
        "name": "Ruan Azeredo",
        "email": "ruan22@gmail",
        "password": "1234"
    }

    response = authenticated_client.put(f'/user/ops/{response.json()["user"]["id"]}', json = update_user_data)

    assert response.status_code == 200
    assert response.json()['message'] == "Usuário atualizado"
    assert response.json()['user']['name'] == "Ruan Azeredo"
    assert response.json()['user']['email'] == "ruan22@gmail"


@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, is_admin = True)
async def test_delete_user_e2e(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan33@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/ops', json = user_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan33@gmail"


    response = authenticated_client.delete(f'/user/ops/{response.json()["user"]["id"]}')
    
    assert response.status_code == 200
    assert response.json()['message'] == "Usuário deletado"
