import pytest
from fastapi.testclient import TestClient
from peewee import SqliteDatabase
from datetime import timedelta
import os

from src.server import app
from models import User
from auth import create_access_token

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

    assert response.status_code == 401
    assert response.json()['detail'] == "Não foi possivel validar as credenciais"

    response = client.post('/auth/login', json={"email": "test1", "password": "test1"})

    assert response.status_code == 200

    token = response.json()

    assert token["access_token"] != None
    assert token["token_type"] == "bearer"


    response = client.get('/user/protected-route', headers={"Authorization": f"Bearer {token['access_token']}"})

    print('resp.json', response.json())
    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_access_to_protected_route_with_invalid_token():

    response = client.get('/user/protected-route', headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == 401

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_access_to_protected_route_without_token():

    response = client.get('/user/protected-route')

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

    token = response.json()

    assert token["access_token"] != None
    assert token["token_type"] == "bearer"

    expired_token = create_access_token({"sub": "test2"}, expires_delta=timedelta(seconds=-10))

    response = client.get('/user/protected-route', headers={"Authorization": f"Bearer {expired_token}"})

    assert response.status_code == 401