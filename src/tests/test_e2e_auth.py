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
async def test_access_to_protected_route():

    client.post('/user/ops', json={"name": "test", "email": "test", "password": "test"})

    response = client.get('/user/protected-route')
    print('resp.json', response.json())

    assert response.status_code == 401
    assert response.json()['detail'] == "Não foi possivel validar as credenciais"

    response = client.post('/auth/login', json={"email": "test", "password": "test"})

    assert response.status_code == 200

    token = response.json()
    print(token)

    assert token["access_token"] != None
    assert token["token_type"] == "bearer"


    response = client.get('/user/protected-route', headers={"Authorization": f"Bearer {token['access_token']}"})

    print('resp.json', response.json())
    assert response.status_code == 200