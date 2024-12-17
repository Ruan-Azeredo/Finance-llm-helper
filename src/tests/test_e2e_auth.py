import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from datetime import timedelta
import os

from src.server import app
from models import User
from auth import Security

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
async def test_access_to_protected_route():

    User.create(
        name = 'test1',
        email = 'test1',
        password = 'test1'
    )

    response = client.get('/user/protected-route')

    assert response.json()['detail'] == "Erro ao obter token"
    assert response.status_code == 401

    response = client.post('/auth/login', json={"email": "test1", "password": "test1"})

    assert response.status_code == 200

    resp = response.json()

    assert resp["access_token"]["token"] != None
    assert resp["access_token"]["token_type"] == "bearer"


    response = client.get('/user/protected-route', headers={"Authorization": f"Bearer {resp['access_token']["token"]}"})

    print('resp.json', response.json())
    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_access_to_protected_route_with_invalid_token():

    response = client.get('/user/protected-route', headers={"Authorization": "Bearer invalid_token"})

    assert response.json()["detail"] == "Token inválido"
    assert response.status_code == 401

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_access_to_protected_route_without_token():

    response = client.get('/user/protected-route')

    assert response.json()["detail"] == "Erro ao obter token"
    assert response.status_code == 401

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_access_to_protected_route_with_expired_token():

    User.create(
        name = 'test2',
        email = 'test2',
        password = 'test2'
    )

    response = client.post('/auth/login', json={"email": "test2", "password": "test2"})

    assert response.status_code == 200

    resp = response.json()

    assert resp["access_token"]["token"] != None
    assert resp["access_token"]["token_type"] == "bearer"

    expired_token = Security.create_jwt_token({"sub": "test2"}, type="access", expires_delta=timedelta(seconds=-10))

    response = client.get('/user/protected-route', headers={"Authorization": f"Bearer {expired_token}"})

    assert response.json()["detail"] == "Token expirado"
    assert response.status_code == 401

""" 
async def test_request_access_token_with_refresh_token():

async def test_request_access_token_with_invalid_refresh_token():

async def test_request_access_token_without_refresh_token():

async def test_request_access_token_with_expired_refresh_token():
"""