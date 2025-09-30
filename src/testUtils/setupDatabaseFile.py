from fastapi.testclient import TestClient
from peewee import SqliteDatabase, Model
import os
import functools
import pytest
from typing import Generator

from models import User, Account
from src.server import app

default_client = TestClient(app)

EMAIL = 'test@gmail.com'
PASSWORD = 'test'

def _createUser(is_admin: bool):
    if is_admin:
        role = 'admin'
    else:
        role = 'free'

    user = User.create(
        name = 'test',
        email = EMAIL,
        password = PASSWORD,
        role = role
    )
    
    # Create default account for the user
    default_account = Account.create(user.id, name="Minha Conta")
    user.update(default_account_id=default_account.id)
    
    return user

def _setupDb(func_name, models: list[Model] = [User, Account]):
    test_db = SqliteDatabase(f'{func_name}.db')
    for model in models:
        model._meta.database = test_db
    test_db.connect()
    test_db.create_tables(models)

    return test_db

def _deleteUserDb(test_db, func_name):
    test_db.drop_tables([User, Account])
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

    client_test.headers = {"Authorization": f"Bearer {json_resp['access_token']['token']}"}

    return client_test, { "email": EMAIL, "password": PASSWORD }

""" 
- - - - - - - Dependencia para testes e2e!!!! - - - - - - -

Essas funçoes definem um client para testes e cria um banco de dados temporario para cada test,

Utilize essa função como decorator, passando os parametros necessarios para a funcao que deseja testar

É de suma importancia a função de test receber o authenticated_client como parametro!
"""

@pytest.fixture
def setup_database_with_tables(request: pytest.FixtureRequest) -> Generator[dict[str, dict[str, TestClient | str]], None, None]:
    models: list[Model] = request.param.get('models') if request.param.get('models') else [User, Account]
    client_test = request.param.get('client_test') if request.param.get('client_test') else default_client
    is_admin = request.param.get('is_admin') if request.param.get('is_admin') else False

    test_db = _setupDb(func_name = request._pyfuncitem.name, models = models)

    authenticated_client, user_credentials = defineAuthUser(client_test = client_test, is_admin = is_admin)
    
    yield {
        "authenticated_client": authenticated_client,
        "user_credentials": user_credentials
    }

    _deleteUserDb(test_db = test_db, func_name = request._pyfuncitem.name)

        
def setupDatabaseFileWithTables(client_test: TestClient = default_client, is_admin: bool = False, models: list[Model] = [User, Account]):
    def decorator(func):
        #@functools.wraps(func) # Preserve function signature for pytest
        async def wrapper(*args, **kwargs):

            print(f"Function: {func.__name__}")
            print(f"Args: {args}")
            print(f"Kwargs Before Modification: {kwargs}")
     
            test_db = _setupDb(func_name = func.__name__, models = models)
            
            # Ensure Account is in the models list if not already there
            if Account not in models:
                models.append(Account)
                test_db.create_tables([Account])

            authenticated_client, _ = defineAuthUser(client_test = client_test, is_admin = is_admin)

            print('kwargs', kwargs)
            #if 'authenticated_client' in kwargs:
            kwargs['authenticated_client'] = authenticated_client

            try:
                return await func(*args, **kwargs)
            finally:
                _deleteUserDb(test_db = test_db, func_name = func.__name__)

        return wrapper
    return decorator

def setupDatabaseHandleLoggedUser(client_test: TestClient = default_client, is_admin: bool = False, models: list[Model] = [User, Account]):
    print('client_test', client_test)
    def decorator(func):
        #@functools.wraps(func)
        async def wrapper(*args, **kwargs):
     
            test_db = _setupDb(func_name = func.__name__, models = models)
            
            # Ensure Account is in the models list if not already there
            if Account not in models:
                models.append(Account)
                test_db.create_tables([Account])
            
            authenticated_client, user_credentials = defineAuthUser(client_test = client_test, is_admin = is_admin)


            kwargs['authenticated_client'] = authenticated_client
            kwargs['user_credentials'] = user_credentials
        
            try:
                return await func(*args, **kwargs)
            finally:
                _deleteUserDb(test_db = test_db, func_name = func.__name__)

        return wrapper
    return decorator