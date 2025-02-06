from peewee import PostgresqlDatabase
import pytest

from models import User
from auth import Security
from testUtils import db_session
from utils import default_users_tags

def test_create_user_model(db_session):
    
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    assert user.__str__() == 'User: 1, name, email@email.com, free'
    assert Security.verify_password(plain_password = 'password', hashed_password = user.password)

def test_create_user_model_with_id(db_session):
    
    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    assert user.__str__() == 'User: 1, name, email@email.com, free'
    assert Security.verify_password(plain_password = 'password', hashed_password = user.password)

def test_create_user_model_with_existing_email(db_session):

    User.create(
        name = 'Ruan',
        email = 'email@email.com',
        password = '1234'
    )
    
    with pytest.raises(Exception) as error:
        User.create(
            name = 'name',
            email = 'email@email.com',
            password = 'password'
        )
    
    assert 'Chave duplicada: email já existente' in str(error.value)

def test_create_user_model_with_existing_id(db_session):

    User.create(
        id = 1,
        name = 'Ruan',
        email = 'email@email.com',
        password = '1234'
    )   
    
    with pytest.raises(Exception) as error:
        User.create(
            id = 1,
            name = 'name',
            email = 'email@email.com',
            password = 'password'
        )
    
    assert 'Chave duplicada: id já existente' in str(error.value)

def test_get_user_model(db_session):
    
    User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user_from_db: User = User.from_id(id = 1)
    
    assert user_from_db.__str__() == 'User: 1, name, email@email.com, free'
    assert user_from_db.name == 'name'
    assert user_from_db.email == 'email@email.com'
    assert Security.verify_password(plain_password = 'password', hashed_password = user_from_db.password)

def test_get_all_users_model(db_session):
    
    User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    User.create(
        id = 2,
        name = 'name',
        email = 'email@gmail.com',
        password = 'password'
    )

    users_from_db: User = User.all()
    
    assert len(users_from_db) == 2
    assert users_from_db[0].__str__() == 'User: 1, name, email@email.com, free'
    assert users_from_db[1].__str__() == 'User: 2, name, email@gmail.com, free'

def test_update_user_model(db_session):
    
    user = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.update(
        id = 1,
        name = 'Ruan',
        email = 'email@email.com',
        password = 'password'
    )

    user: User = User.select().where(User.id == 1).get()

    assert user.tags == default_users_tags
    
    assert user.__str__() == 'User: 1, Ruan, email@email.com, free'
    assert user.name == 'Ruan'

def test_update_few_fields_user_model(db_session):
    
    user: User = User.create(
        id = 12,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.update(
        name = 'Ruan',
    )

    user = User.select().where(User.id == 12).get()
    
    assert user.__str__() == 'User: 12, Ruan, email@email.com, free'

def test_delete_user_model(db_session):
    
    user: User = User.create(
        id = 12,
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    user.delete()
    
    assert not User.select().where(User.id == 12).exists()

def test_create_user_model_defined_tags(db_session):
    
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )
    
    assert user.tags == [
        {'name': 'tag1', 'color': 0},
        {'name': 'tag2', 'color': 1}
    ]

def test_create_user_model_defined_tags_with_invalid_color(db_session):
    
    with pytest.raises(Exception) as error:
        User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 'azul'},
            {'name': 'tag2', 'color': 1}
        ]
    )
        
    assert "Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. O tags recebido foi: " + str([{'name': 'tag1', 'color': 'azul'}, {'name': 'tag2', 'color': 1}]) in str(error.value)
        
def test_create_user_model_defined_tags_with_invalid_name(db_session):
    
    with pytest.raises(Exception) as error:
        User.create(
            name = 'name',
            email = 'email@email.com',
            password = 'password',
            tags = [
                {'name': 0, 'color': 0},
                {'name': 'tag2', 'color': 0}
            ]
        )

    assert "Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. O tags recebido foi: " + str([{'name': 0, 'color': 0}, {'name': 'tag2', 'color': 0}]) in str(error.value)

        
def test_create_user_model_defined_tags_with_empty_name(db_session):
    
    with pytest.raises(Exception) as error:
        User.create(
            name = 'name',
            email = 'email@email.com',
            password = 'password',
            tags = [
                {'name': '', 'color': 0},
                {'name': 'tag2', 'color': 0}
            ]
        )

    assert "Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. O tags recebido foi: " + str([{'name': '', 'color': 0}, {'name': 'tag2', 'color': 0}]) in str(error.value)

def test_create_user_model_defined_tags_with_repeated_name(db_session):
    
    with pytest.raises(Exception) as error:
        User.create(
            name = 'name',
            email = 'email@email.com',
            password = 'password',
            tags = [
                {'name': 'tag1', 'color': 0},
                {'name': 'tag1', 'color': 0}
            ]
        )

    assert "Formato de tags está incorreto, tags não pode ter tags duplicadas." in str(error.value)

def test_update_user_model_defined_tags(db_session):
        
    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )

    print(user, ' - ',user.name, user.tags, type(user.tags), type(user))

    user.update(
        name = 'ruan',
    )

    user_updated: User = User.get_user_by_email('email@email.com')

    print(user_updated, ' - - ',user_updated.name, user_updated.tags, type(user_updated.tags))

    assert user_updated.tags == [
        {'name': 'tag3', 'color': 0},
        {'name': 'tag4', 'color': 1}
    ]
    assert user_updated.__str__() == 'User: 1, name, email@email.com, free'

def test_update_user_model_defined_tags_with_invalid_color(db_session):
        
    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )

    with pytest.raises(Exception) as error:
        user.update(
            tags = [
                {'name': 'tag3', 'color': 0},
                {'name': 'tag4', 'color': 'azul'}
            ]
        )

    assert "Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. O tags recebido foi: " + str([{'name': 'tag3', 'color': 0}, {'name': 'tag4', 'color': 'azul'}]) in str(error.value)

def test_update_user_model_defined_tags_with_invalid_name(db_session):
        
    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )

    with pytest.raises(Exception) as error:
        user.update(
            tags = [
                {'name': 0, 'color': 0},
                {'name': 'tag4', 'color': 0}
            ]
        )

    assert "Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. O tags recebido foi: " + str([{'name': 0, 'color': 0}, {'name': 'tag4', 'color': 0}]) in str(error.value)

def test_update_user_model_defined_tags_with_empty_name(db_session):
        
    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )

    with pytest.raises(Exception) as error:
        user.update(
            tags = [
                {'name': '', 'color': 0},
                {'name': 'tag4', 'color': 0}
            ]
        )

    assert "Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. O tags recebido foi: " + str([{'name': '', 'color': 0}, {'name': 'tag4', 'color': 0}]) in str(error.value)

def test_update_user_model_defined_tags_with_repeated_name(db_session):

    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )

    with pytest.raises(Exception) as error:
        user.update(
            tags = [
                {'name': 'tag3', 'color': 0},
                {'name': 'tag3', 'color': 0}
            ]
        )

    assert "Formato de tags está incorreto, tags não pode ter tags duplicadas." in str(error.value)

def test_update_user_model_defined_tags_with_empty_list(db_session):

    user: User = User.create(
        id = 1,
        name = 'name',
        email = 'email@email.com',
        password = 'password',
        tags = [
            {'name': 'tag1', 'color': 0},
            {'name': 'tag2', 'color': 1}
        ]
    )

    with pytest.raises(Exception) as error:
        user.update(
            tags = []
        )

    assert "Formato de tags está incorreto, tags não pode ser vazio" in str(error.value)