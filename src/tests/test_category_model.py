from models import User,Category
from testUtils import db_session
from utils import default_users_categories

import pytest

def test_create_category_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    category = Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    assert category.name == 'category'
    assert category.color == 0

    # category.user_id automatically get the User, to get just the id, use category.user_id_id
    assert category.user_id_id == user.id

def test_create_category_model_with_nonexistent_user(db_session):

    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Category.create(
            user_id = 1,
            name = 'category',
            color = 0
        )

    assert 'Registro não encontrado: Usuario com id 1 nao encontrado' in str(error.value)

def test_create_default_categories_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create_default_categories(user.id)

    assert Category.select().where(Category.user_id == user.id).count() == len(default_users_categories)

    user_categories = Category.select().where(Category.user_id == user.id)

    for category in user_categories:
        assert category.name in [category['name'] for category in default_users_categories]
        assert category.color in [category['color'] for category in default_users_categories]
        
def test_get_category_by_user_id_category_model(db_session):

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

    Category.create_default_categories(user.id)
    Category.create_default_categories(22)

    categories = Category.get_categories_by_user_id(user.id)

    assert len(categories) == len(default_users_categories)

def test_get_category_by_user_id_category_model_with_nonexistent_user(db_session):

    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Category.get_categories_by_user_id(1)

    assert 'Registro não encontrado: Usuario com id 1 nao encontrado' in str(error.value)

def test_update_category_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    category: Category = Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    category.update(
        name = 'new_category',
        color = 1
    )

    updated_category = Category.from_id(category.id)

    assert updated_category.name == 'new_category'
    assert updated_category.color == 1

def test_delete_category_model(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    category = Category.create(
        user_id = user.id,
        name = 'category2',
        color = 1
    )

    category.delete()

    assert Category.select().where(Category.user_id == user.id).count() == 1
    assert Category.from_id(category.id) is None

def test_create_category_model_with_default_color(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    category = Category.create(
        user_id = user.id,
        name = 'category'
    )

    assert category.color == 0

def test_create_category_model_with_invalid_color(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Category.create(
            user_id = user.id,
            name = 'category',
            color = 10
        )

        assert 'Formato de color está incorreto, color deve ser um número de 0 a 9' in str(error.value)

def test_create_category_model_without_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Category.create(
            user_id = user.id,
            color = 0
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_create_category_model_with_empty_str_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Category.create(
            user_id = user.id,
            name = '',
            color = 0
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_create_category_model_with_repeated_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create(
            user_id = user.id,
            name = 'category',
            color = 0
        )

    with pytest.raises(Exception) as error:
        Category.create(
            user_id = user.id,
            name = 'category',
            color = 1
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_update_category_model_with_invalid_color(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Category.update(
            color = 10
        )

        assert 'Formato de color está incorreto, color deve ser um número de 0 a 9' in str(error.value)

def test_update_category_model_without_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Category.update(
            name = 'null'
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_update_category_model_with_empty_str_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Category.update(
            name = ''
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_update_category_model_with_repeated_name(db_session):

    user = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Category.create(
        user_id = user.id,
        name = 'category',
        color = 0
    )

    Category.create(
        user_id = user.id,
        name = 'category1',
        color = 0
    )

    with pytest.raises(Exception) as error:
        Category.update(
            name = 'category'
        )

        assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

