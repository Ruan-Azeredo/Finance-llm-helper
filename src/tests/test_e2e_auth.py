import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from datetime import timedelta
import os
import time
import pytest_mock

from src.server import app
from models import User
from auth import Security
from testUtils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser, setup_database_with_tables

not_logged_client = TestClient(app)

# @pytest.fixture(scope="session", autouse=True)
# def setup_and_teardown_database():
#     test_db = SqliteDatabase('test.db')
#     # Configuração do banco de dados
#     User._meta.database = test_db
#     test_db.connect()
#     test_db.create_tables([User])
#     yield
#     # Teardown - Fecha a conexão e remove o arquivo do banco de dados
#     test_db.drop_tables([User])
#     test_db.close()
#     if os.path.exists('test.db'):
#         os.remove('test.db')


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_access_to_protected_route(setup_database_with_tables):

    User.create(
        name = 'test1',
        email = 'test1',
        password = 'test1'
    )

    response = not_logged_client.get('/user/protected-route')

    assert response.json()['detail'] == "Erro ao obter token"
    assert response.status_code == 401

    response = not_logged_client.post('/auth/login', json={"email": "test1", "password": "test1"})

    assert response.status_code == 200

    resp = response.json()

    assert resp["access_token"]["token"] != None
    assert resp["access_token"]["token_type"] == "bearer"


    response = not_logged_client.get('/user/protected-route', headers={"Authorization": f"Bearer {resp['access_token']['token']}"})

    print('resp.json', response.json())
    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_access_to_protected_route_with_invalid_token(setup_database_with_tables):

    response = not_logged_client.get('/user/protected-route', headers={"Authorization": "Bearer invalid_token"})

    assert response.json()["detail"] == "Token inválido"
    assert response.status_code == 401

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_access_to_protected_route_without_token(setup_database_with_tables):

    response = not_logged_client.get('/user/protected-route')

    assert response.json()["detail"] == "Erro ao obter token"
    assert response.status_code == 401

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_access_to_protected_route_with_expired_token(setup_database_with_tables):

    User.create(
        name = 'test2',
        email = 'test2',
        password = 'test2'
    )

    response = not_logged_client.post('/auth/login', json={"email": "test2", "password": "test2"})

    assert response.status_code == 200

    resp = response.json()

    assert resp["access_token"]["token"] != None
    assert resp["access_token"]["token_type"] == "bearer"

    expired_token = Security.create_jwt_token({"sub": "test2"}, type="access", expires_delta=timedelta(seconds=-10))

    response = not_logged_client.get('/user/protected-route', headers={"Authorization": f"Bearer {expired_token}"})

    assert response.json()["detail"] == "Token expirado"
    assert response.status_code == 401

""" 
async def test_request_access_token_with_refresh_token():

async def test_request_access_token_with_invalid_refresh_token():

async def test_request_access_token_without_refresh_token():

async def test_request_access_token_with_expired_refresh_token():
"""

def mock_send_password_reset_email(email: str, reset_token: str):
    print(f"E-mail enviado para {email} com token {reset_token}")

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_forgot_password(setup_database_with_tables, mocker: pytest_mock.MockerFixture):

    """Testa se a solicitação de redefinição de senha funciona corretamente"""
    mocker.patch('services.SendPasswordResetEmail', mock_send_password_reset_email)

    user: User = User.create(
        name = 'name',
        email = 'email',
        password = 'password'
    )

    response = not_logged_client.post('/auth/forgot-password', json={"email": user.email})
    print('response', response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "E-mail de recuperação enviado!"

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_forgot_password_with_invalid_email(setup_database_with_tables):
    response = not_logged_client.post('/auth/forgot-password', json={"email": "invalid_email"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_reset_password(mocker: pytest_mock.MockerFixture, setup_database_with_tables):

    user: User = User.create(
        name = 'name',
        email = 'email',
        password = 'password'
    )

    """Testa se a redefinição de senha funciona corretamente"""
    # Gerar um token de teste manualmente
    reset_token = "testtoken123"
    password_reset_tokens = {}
    password_reset_tokens[user.email] = {"token": reset_token, "expires": time.time() + 3600}

    mocker.patch('controllers.authController.password_reset_tokens', password_reset_tokens)

    new_password = "NovaSenha123"
    response = not_logged_client.post("/auth/reset-password", json={
        "email": user.email,
        "token": reset_token,
        "new_password": new_password
    })

    print('response', response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "Senha redefinida com sucesso!"}

    # Verificar se a senha foi realmente alterada no banco de dados
    user: User = User.get_user_by_email(user.email)
    assert Security.verify_password(new_password, user.password)  # A senha deve ter sido alterada

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_reset_password_with_invalid_token(setup_database_with_tables):
    
    user: User = User.create(
        name = 'name',
        email = 'email',
        password = 'password'
    )

    response = not_logged_client.post("/auth/reset-password", json={
    "email": user.email,
    "token": "invalid_token",
    "new_password": "NovaSenha123"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Token inválido ou expirado"}

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_reset_password_with_invalid_email(setup_database_with_tables):

    response = not_logged_client.post("/auth/reset-password", json={
    "email": "invalid_email",
    "token": "valid_token",
    "new_password": "NovaSenha123"
    })

    assert response.status_code == 404
    assert response.json() == {"detail": "Usuário não encontrado"}

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User]}], indirect=True)
async def test_reset_password_with_expired_token(setup_database_with_tables, mocker: pytest_mock.MockerFixture):
    
    user: User = User.create(
        name = 'name',
        email = 'email',
        password = 'password'
    )

    reset_token = "testtoken123"
    password_reset_tokens = {}
    password_reset_tokens[user.email] = {"token": reset_token, "expires": time.time() - 1} # Token expirado

    mocker.patch('controllers.authController.password_reset_tokens', password_reset_tokens)


    response = not_logged_client.post("/auth/reset-password", json={
    "email": user.email,
    "token": "expired_token",
    "new_password": "NovaSenha123"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Token inválido ou expirado"}