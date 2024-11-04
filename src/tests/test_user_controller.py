from src.server import app
from models import User

from peewee import SqliteDatabase
from fastapi.testclient import TestClient

client = TestClient(app)

def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    User._meta.database = test_db

    test_db.connect()
    test_db.create_tables([User])

    return test_db

def test_user_table_exists():

    test_db = setupTestDatabase()

    """ if not test_db.table_exists('user'):
        test_db.create_tables([User]) """
    
    assert test_db.table_exists('user') == True


def test_get_users():

    test_db = setupTestDatabase()

    response = client.get("/user")

    assert test_db.table_exists('user') == True
    ###assert response.status_code == 200
    assert response.json() == {"users": []}