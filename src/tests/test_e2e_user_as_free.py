import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.server import app
from models import User
from utils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser

client_test = TestClient(app)

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test)
async def test_create_user_e2e_as_free(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/ops', json = user_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan@gmail"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test)
async def test_get_user_e2e_as_free(authenticated_client):

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

    response: HTTPException = authenticated_client.get(f'/user/ops/{response.json()["user"]["id"]}')

    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'
    assert response.status_code == 403

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test)
async def test_update_user_e2e_as_free(authenticated_client):

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

    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'
    assert response.status_code == 403


@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test)
async def test_delete_user_e2e_as_free(authenticated_client):

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

    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'
    assert response.status_code == 403

# Test operations as free and self user

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test)
async def test_delete_self_user_e2e_as_free(authenticated_client, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    response = authenticated_client.delete(f'/user/ops/{user.id}')

    assert response.json()['message'] == "Usuário deletado"
    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test)
async def test_get_self_user_e2e_as_free(authenticated_client, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    response = authenticated_client.get(f'/user/ops/{user.id}')

    print(response.json())

    assert response.json()['user']['email'] == user_credentials['email']
    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test)
async def test_update_self_user_e2e_as_free(authenticated_client, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    get_response = authenticated_client.get(f'/user/ops/{user.id}')

    print(get_response.json())
    
    assert get_response.status_code == 200
    assert get_response.json()['user']['email'] == user_credentials['email']
    assert get_response.json()['user']['name'] != "Ruan Azeredo Gomes"

    update_user_data = {
        "name": "Ruan Azeredo Gomes"
    }

    response = authenticated_client.put(f'/user/ops/{user.id}', json = update_user_data)

    print(response.json())
    

    assert response.status_code == 200
    assert response.json()['message'] == "Usuário atualizado"
    assert response.json()['user']['name'] == "Ruan Azeredo Gomes"