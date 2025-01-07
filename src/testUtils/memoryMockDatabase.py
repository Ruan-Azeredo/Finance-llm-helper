from peewee import SqliteDatabase
import pytest

from models import models

@pytest.fixture(scope="function")
def db_session():
    """
    Configura o banco de dados em memória antes de cada teste. Utiliz SQLITE para isso.
    
    - Importante referenciar 'db_session' como argumento nos testes!
    """

    test_db = SqliteDatabase(":memory:")

    for model in models:
        model._meta.database = test_db

    test_db.connect()
    test_db.create_tables(models)

    yield test_db

    test_db.drop_tables(models)
    test_db.close()

@pytest.fixture(scope="function")
def test_db():
    """
    #Cria o banco de dados em memória para testes estruturais sobre o banco.
    """

    test_db = SqliteDatabase(":memory:")

    for model in models:
        model._meta.database = test_db

    yield test_db

    test_db.drop_tables(models)
    test_db.close()
