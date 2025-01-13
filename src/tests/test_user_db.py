import pytest

from models import User
from testUtils import test_db

def test_user_table_exists(test_db):
    
    test_db.connect()
    test_db.create_tables([User])
    
    assert test_db.table_exists('users')

def test_user_table_not_exists(test_db):
    
    test_db.connect()
    
    assert not test_db.table_exists('users')

def test_get_all_users_when_table_not_exists(test_db):
    
    test_db.connect()

    user = User

    with pytest.raises(Exception) as error:
        user.all()
    
    assert test_db.table_exists('users') == False
    assert "Tabela 'users' não existe" in str(error.value)

def test_get_user_when_table_not_exists(test_db):
    
    test_db.connect()

    user = User

    with pytest.raises(Exception) as error:
        user.from_id(id = 1)
    
    assert test_db.table_exists('users') == False
    assert "Tabela 'users' não existe" in str(error.value)

def test_create_user_when_table_not_exists(test_db):
    
    test_db.connect()

    with pytest.raises(Exception) as error:
        User.create(
            name = 'name',
            email = 'email@email.com',
            password = 'password'
        )
    
    assert test_db.table_exists('users') == False
    assert "Tabela 'users' não existe" in str(error.value)

def test_update_user_when_table_not_exists(test_db):
    
    test_db.connect()

    user = User()

    with pytest.raises(Exception) as error:
        user.update(
            id = 1,
            name = 'name',
            email = 'email@email.com',
            password = 'password'
        )
    
    assert test_db.table_exists('users') == False
    assert "Tabela 'users' não existe" in str(error.value)

def test_delete_user_when_table_not_exists(test_db):
    
    test_db.connect()

    user = User()

    with pytest.raises(Exception) as error:
        user.delete()
    
    assert test_db.table_exists('users') == False
    assert "Tabela 'users' não existe" in str(error.value)

def test_get_user_when_user_not_exists(test_db):
    
    test_db.connect()
    test_db.create_tables([User])

    user_founded = User.from_id(id = 1)

    assert user_founded == None