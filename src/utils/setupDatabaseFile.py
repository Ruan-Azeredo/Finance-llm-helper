from fastapi.testclient import TestClient
from peewee import SqliteDatabase
import os

from models import User

def defineAuthUser(client: TestClient):

    User.create(
        name = 'test',
        email = 'test',
        password = 'test',
        role = 'admin'
    )

    response = client.post('/auth/login', json={
        "email": "test",
        "password": "test"
    })

    print('response: ',response.json())
    assert response.status_code == 200

    token = response.json()

    client.headers = {"Authorization": f"Bearer {token['access_token']}"}

    return client

def setupDatabaseFileWithUserTable(clienttest: TestClient):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            print('started')
            

            test_db = SqliteDatabase(f'{func.__name__}.db')
            User._meta.database = test_db
            test_db.connect()
            test_db.create_tables([User])
            client = defineAuthUser(clienttest)
            kwargs['client'] = client
            try:
                test = await func(*args, **kwargs)
                return test
            finally:
                print('ended')
                test_db.drop_tables([User])
                test_db.close()
                if os.path.exists(f'{func.__name__}.db'):
                    os.remove(f'{func.__name__}.db')
        return wrapper
    return decorator