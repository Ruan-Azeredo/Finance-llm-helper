from models import User,Tag
from testUtils import db_session
from utils import default_users_tags

import pytest

def test_create_tag_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    tag = Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    assert tag.name == 'tag'
    assert tag.color == 0

    # tag.user_id automatically get the User, to get just the id, use tag.user_id_id
    assert tag.user_id_id == user.id

def test_create_tag_model_with_nonexistent_user(db_session):

    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Tag.create(
            user_id = 1,
            name = 'tag',
            color = 0
        )

    assert 'Registro não encontrado: Usuario com id 1 nao encontrado' in str(error.value)

def test_create_default_tags_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create_default_tags(user.id)

    assert Tag.select().where(Tag.user_id == user.id).count() == len(default_users_tags)

    user_tags = Tag.select().where(Tag.user_id == user.id)

    for tag in user_tags:
        assert tag.name in [category['name'] for category in default_users_tags]
        assert tag.color in [category['color'] for category in default_users_tags]
        
def test_get_tag_by_user_id_tag_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    User.create(
        id = 22,
        name = 'othername',
        email = 'otheremail@email.com',
        password = 'password'
    )

    Tag.create_default_tags(user.id)
    Tag.create_default_tags(22)

    tags = Tag.get_tags_by_user_id(user.id)

    assert len(tags) == len(default_users_tags)

def test_get_tag_by_user_id_tag_model_with_nonexistent_user(db_session):

    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Tag.get_tags_by_user_id(1)

    assert 'Registro não encontrado: Usuario com id 1 nao encontrado' in str(error.value)

def test_update_tag_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    tag: Tag = Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    tag.update(
        name = 'new_tag',
        color = 1
    )

    updated_tag = Tag.from_id(tag.id)

    assert updated_tag.name == 'new_tag'
    assert updated_tag.color == 1

def test_delete_tag_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    tag = Tag.create(
        user_id = user.id,
        name = 'tag2',
        color = 1
    )

    tag.delete()

    assert Tag.select().where(Tag.user_id == user.id).count() == 1
    assert Tag.from_id(tag.id) is None

def test_create_tag_model_with_default_color(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    tag = Tag.create(
        user_id = user.id,
        name = 'tag'
    )

    assert tag.color == 0

def test_create_tag_model_with_invalid_color(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Tag.create(
            user_id = user.id,
            name = 'tag',
            color = 10
        )

        assert 'Formato de color está incorreto, color deve ser um número de 0 a 9' in str(error.value)

def test_create_tag_model_without_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Tag.create(
            user_id = user.id,
            color = 0
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_create_tag_model_with_empty_str_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Tag.create(
            user_id = user.id,
            name = '',
            color = 0
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_create_tag_model_with_repeated_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create(
            user_id = user.id,
            name = 'tag',
            color = 0
        )

    with pytest.raises(Exception) as error:
        Tag.create(
            user_id = user.id,
            name = 'tag',
            color = 1
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_update_tag_model_with_invalid_color(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Tag.update(
            color = 10
        )

        assert 'Formato de color está incorreto, color deve ser um número de 0 a 9' in str(error.value)

def test_update_tag_model_without_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Tag.update(
            name = 'null'
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_update_tag_model_with_empty_str_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Tag.update(
            name = ''
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_update_tag_model_with_repeated_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Tag.create(
        user_id = user.id,
        name = 'tag',
        color = 0
    )

    Tag.create(
        user_id = user.id,
        name = 'tag1',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Tag.update(
            name = 'tag'
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

