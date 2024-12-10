from fastapi.testclient import TestClient
from peewee import SqliteDatabase
import os

from models import User

EMAIL = 'test@gmail.com'
PASSWORD = 'test'

def _createUser(is_admin: bool):
    if is_admin:
        role = 'admin'
    else:
        role = 'free'

    User.create(
        name = 'test',
        email = EMAIL,
        password = PASSWORD,
        role = role
    )

def _setupUserDb(func_name):
    test_db = SqliteDatabase(f'{func_name}.db')
    User._meta.database = test_db
    test_db.connect()
    test_db.create_tables([User])

    return test_db

def _deleteUserDb(test_db, func_name):
    test_db.drop_tables([User])
    test_db.close()
    if os.path.exists(f'{func_name}.db'):
        os.remove(f'{func_name}.db')

def defineAuthUser(client_test: TestClient, is_admin: bool):

    _createUser(is_admin = is_admin)
    
    response = client_test.post('/auth/login', json={
        "email": EMAIL,
        "password": PASSWORD
    })

    assert response.status_code == 200

    json_resp = response.json()

    client_test.headers = {"Authorization": f"Bearer {json_resp["access_token"]["token"]}"}

    return client_test, { "email": EMAIL, "password": PASSWORD }

""" 
Essa função define um client para testes e cria um banco de dados temporario para cada test,

Utilize essa função como decorator, passando os parametros necessarios para a funcao que deseja testar

É de suma importancia a função de test receber o authenticated_client como parametro!
"""

def setupDatabaseFileWithUserTable(client_test: TestClient, is_admin: bool = False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
     
            test_db = _setupUserDb(func_name = func.__name__)
            
            authenticated_client, _ = defineAuthUser(client_test = client_test, is_admin = is_admin)

            kwargs['authenticated_client'] = authenticated_client

            try:
                test = await func(*args, **kwargs)
                return test
            finally:
                _deleteUserDb(test_db = test_db, func_name = func.__name__)

        return wrapper
    return decorator

def setupDatabaseHandleLoggedUser(client_test: TestClient, is_admin: bool = False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
     
            test_db = _setupUserDb(func_name = func.__name__)
            
            authenticated_client, user_credentials = defineAuthUser(client_test = client_test, is_admin = is_admin)

            kwargs['authenticated_client'] = authenticated_client
            kwargs['user_credentials'] = user_credentials
            
            try:
                test = await func(*args, **kwargs)
                return test
            finally:
                _deleteUserDb(test_db = test_db, func_name = func.__name__)

        return wrapper
    return decorator