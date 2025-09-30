import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.server import app
from models import User, Account, Category
from testUtils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser

client_test = TestClient(app)

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Account, Category])
async def test_create_user_e2e_and_verify_default_account(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/create-user-default-properties', json = user_data)
    print(response.json())
    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan@gmail"
    assert response.json()['categories'][0]['name'] == "Alimentação"
    assert response.json()['categories'][0]['color'] == 0
    assert response.json()['accounts'][0]['name'] == "Minha Conta"
    assert response.json()['accounts'][0]['balance'] == 0
    assert response.json()['accounts'][0]['origin'] == "default"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Account, Category])
async def test_create_user_e2e_and_try_to_delete_last_account(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/create-user-default-properties', json = user_data)
    
    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan@gmail"
    assert response.json()['categories'][0]['name'] == "Alimentação"
    assert response.json()['categories'][0]['color'] == 0
    assert response.json()['accounts'][0]['name'] == "Minha Conta"
    assert response.json()['accounts'][0]['balance'] == 0
    assert response.json()['accounts'][0]['origin'] == "default"

    login_reponse = authenticated_client.post("/auth/login", json = user_data)
    print(login_reponse.json())
    authenticated_client.headers.update({"Authorization": f"Bearer {login_reponse.json()['access_token']['token']}"})

    delete_response = authenticated_client.delete(f"/account/ops/{response.json()['accounts'][0]['id']}")
    print(delete_response.json())

    assert delete_response.status_code == 500
    assert delete_response.json()['detail'].__contains__("Nao e possivel excluir a ultima conta do usuario")

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Account, Category])
async def test_create_user_e2e_and_update_balance(authenticated_client):

    user_data = {
        "name": "Ruan",
        "email": "ruan@gmail",
        "password": "1234"
    }

    response = authenticated_client.post('/user/create-user-default-properties', json = user_data)
    
    assert response.status_code == 201
    assert response.json()['message'] == "Usuário criado"
    assert response.json()['user']['name'] == "Ruan"
    assert response.json()['user']['email'] == "ruan@gmail"
    assert response.json()['categories'][0]['name'] == "Alimentação"
    assert response.json()['categories'][0]['color'] == 0
    assert response.json()['accounts'][0]['name'] == "Minha Conta"
    assert response.json()['accounts'][0]['balance'] == 0
    assert response.json()['accounts'][0]['origin'] == "default"

    login_reponse = authenticated_client.post("/auth/login", json = user_data)
    print(login_reponse.json())
    authenticated_client.headers.update({"Authorization": f"Bearer {login_reponse.json()['access_token']['token']}"})

    update_response = authenticated_client.put(f"/account/ops/{response.json()['accounts'][0]['id']}", json = {
        "balance": "1000,00",
    })
    print(update_response.json())

    assert update_response.status_code == 200
    assert update_response.json()['message'] == "Conta atualizada"
    assert update_response.json()['account']['balance'] == "1000,00"
    assert update_response.json()['account']['origin'] == "default"
    assert update_response.json()['account']['name'] == "Minha Conta"

