import pytest
from fastapi.testclient import TestClient

from src.server import app
from models import User, Category
from testUtils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser

client = TestClient(app)

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client, is_admin = True, models = [User, Category])
async def test_get_all_categories_e2e_as_admin(authenticated_client: TestClient):

    response = authenticated_client.get('/category/ops')

    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client, models = [User, Category])
async def test_get_all_categories_e2e_as_free(authenticated_client: TestClient):

    response = authenticated_client.get('/category/ops')

    assert response.status_code == 403

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client, models = [User, Category])
async def test_create_category_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    category_data = {
        "name": "category"
    }

    response = authenticated_client.post(f'/category/ops/{user.id}', json = category_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Categoria criada"
    assert response.json()['category']['user_id'] == user.id
    assert response.json()['category']['name'] == "category"
    assert response.json()['category']['color'] == 0

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client, models = [User, Category])
async def test_create_category_defining_color_e2e_as_free(authenticated_client: TestClient, user_credentials):
    user: User = User.get_user_by_email(user_credentials['email'])

    category_data = {
        "name": "category",
        "color": 1
    }

    response = authenticated_client.post(f'/category/ops/{user.id}', json = category_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Categoria criada"
    assert response.json()['category']['user_id'] == user.id
    assert response.json()['category']['name'] == "category"
    assert response.json()['category']['color'] == 1

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client, models = [User, Category])
async def test_update_category_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    category_data = {
        "name": "category",
        "color": 1
    }

    response = authenticated_client.post(f'/category/ops/{user.id}', json = category_data)

    update_category_data = {
        "name": "new category",
        "color": 1
    }

    response = authenticated_client.put(f'/category/ops/{response.json()["category"]["id"]}', json = update_category_data)

    assert response.status_code == 200
    assert response.json()['message'] == "Categoria atualizada"
    assert response.json()['category']['user_id'] == user.id
    assert response.json()['category']['name'] == "new category"
    assert response.json()['category']['color'] == 1

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client, models = [User, Category])
async def test_delete_category_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    category_data = {
        "name": "category",
        "color": 1
    }

    category_data_2 = {
        "name": "category2",
        "color": 1
    }

    authenticated_client.post(f'/category/ops/{user.id}', json = category_data_2)
    response = authenticated_client.post(f'/category/ops/{user.id}', json = category_data)

    delete_response = authenticated_client.delete(f'/category/ops/{response.json()["category"]["id"]}')

    

    assert delete_response.status_code == 200