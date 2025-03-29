import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.server import app
from models import User, Transaction, Month
from testUtils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser
from utils import formatDateStrToTimestamp, formatTimestampToDateStr

client_test = TestClient(app)

#----------------------------------------------------------- as admin
@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, is_admin = True, models = [User, Transaction,] )
async def test_get_all_transactions_e2e_as_admin(authenticated_client: TestClient):

    response = authenticated_client.get('/transaction/ops')

    print(response.json())
    assert response.status_code == 200
#------------------------------------------------------------ as free
@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_transaction_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "date": "12/03/2024",
        "memo": "memo",
        "direction": "expense"
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    print(response.json())

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/03/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "expense"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_get_user_transactions_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    response = authenticated_client.get(f'/transaction/from-user/{user.id}')

    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_get_user_transactions_with_time_range_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    response = authenticated_client.get(f'/transaction/from-user/{user.id}?start_date={formatDateStrToTimestamp("12/11/2024")}&end_date={formatDateStrToTimestamp("19/11/2024")}')

    assert response.status_code == 200

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_update_transaction_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "date": "12/03/2024",
        "memo": "memo",
        "direction": "income"
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/03/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "income"

    update_transaction_data = {
        "amount": "32,34"
    }

    update_response = authenticated_client.put(f"/transaction/ops/{response.json()['transaction']['id']}", json = update_transaction_data)

    print(update_response.json())
    assert update_response.status_code == 200
    assert update_response.json()['message'] == "Transação atualizada"
    assert update_response.json()['transaction']['user_id'] == user.id
    assert update_response.json()['transaction']['amount'] == '32,34'
    assert update_response.json()['transaction']['date'] == "12/03/2024"
    assert update_response.json()['transaction']['memo'] == "memo"
    assert update_response.json()['transaction']['direction'] == "income"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_delete_transaction_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "type": "expense",
        "date": "12/03/2024",
        "memo": "memo",
        "direction": "income"
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/03/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "income"

    delete_response = authenticated_client.delete(f'/transaction/ops/{response.json()["transaction"]["id"]}')

    assert delete_response.status_code == 200
    assert delete_response.json()['message'] == "Transação deletada"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_get_transaction_from_other_user_e2e_as_free(authenticated_client: TestClient):

    response = authenticated_client.get('/transaction/from-user/12')

    assert response.status_code == 403
    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_get_all_transactions_from_other_user_e2e_as_free(authenticated_client: TestClient):

    response = authenticated_client.get('/transaction/ops')

    assert response.status_code == 403
    assert response.json()['detail'] == 'Acesso negado: nível de permissão insuficiente'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_get_transactions_from_other_user_e2e_as_free(authenticated_client: TestClient):

    response = authenticated_client.get('/transaction/from-user/12')

    assert response.status_code == 403
    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_update_transaction_not_found_e2e_as_free(authenticated_client: TestClient):

    response = authenticated_client.put('/transaction/ops/12')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Transação nao encontrada'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_delete_transaction_not_found_e2e_as_free(authenticated_client: TestClient):

    response = authenticated_client.delete('/transaction/ops/12')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Transação nao encontrada'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_update_transaction_from_other_user_e2e_as_free(authenticated_client: TestClient):

    User.create(
        id = 12,
        email = "email",
        name = "name",
        password = "password"
    )

    transaction = Transaction.create(
        user_id = 12,
        amount = "12,34",
        memo = "hsdjagf",
        date = "12/02/2024",
        direction = "expense"
    )

    update_transaction_data = {
        "amount": "32,34"
    }

    response = authenticated_client.put(f'/transaction/ops/{transaction.id}', json = update_transaction_data)

    print(response.json())
    assert response.status_code == 403
    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseFileWithTables(client_test = client_test, models = [User, Transaction, Month])
async def test_delete_transaction_from_other_user_e2e_as_free(authenticated_client: TestClient):

    User.create(
        id = 12,
        email = "email",
        name = "name",
        password = "password"
    )

    transaction = Transaction.create(
        user_id = 12,
        amount = "12,34",
        memo = "hsdjagf",
        date = "12/03/2024",
        direction = "expense"
    )

    response = authenticated_client.delete(f'/transaction/ops/{transaction.id}')

    assert response.status_code == 403
    assert response.json()['detail'] == 'Acesso negado: não possui permissão para acessar esse dados de outro usuário'

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_many_transactions_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "date": "12/03/2024",
        "memo": "memo",
        "direction": "expense"
    }

    many_transaction_data =[
        transaction_data,
        transaction_data,
        transaction_data,
        transaction_data
    ]

    response = authenticated_client.post(f'/transaction/create-many-transactions/{user.id}', json = many_transaction_data)
    
    print(response.json())

    assert response.status_code == 201
    assert response.json()['message'] == "Transações criadas"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_transaction_with_direction_default_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "date": "12/03/2024",
        "memo": "memo",
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    print(response.json())

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/03/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "expense"

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_transaction_and_create_month_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "date": "12/03/2024",
        "memo": "memo",
        "direction": "expense"
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    print(response.json())

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/03/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "expense"

    months: list[Month] = Month.get_months_by_user_id(user.id)

    print(formatTimestampToDateStr(months[0].date))
    assert months[0] is not None
    assert months[0].user_id_id == user.id
    assert months[0].balance_diff == 0
    assert months[0].date == formatDateStrToTimestamp("01/03/2024")

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_transaction_and_create_month_e2e_as_free_with_month_already_created(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    Month.create(
        balance_diff = 0,
        date = formatDateStrToTimestamp("01/03/2024"),
        user_id = user.id,
    )

    months: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months) == 1
    assert months[0].user_id_id == user.id
    assert months[0].balance_diff == 0
    assert months[0].date == formatDateStrToTimestamp("01/03/2024")

    transaction_data = {
        "amount": "12,34",
        "date": "12/03/2024",
        "memo": "memo",
        "direction": "expense"
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/03/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "expense"

    months_after_create_transaction: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months_after_create_transaction) == 1
    assert months_after_create_transaction[0].user_id_id == user.id
    assert months_after_create_transaction[0].balance_diff == 0
    assert months_after_create_transaction[0].date == formatDateStrToTimestamp("01/03/2024")

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_many_transactions_and_create_months_e2e_as_free(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    many_transaction_data = []

    for i in range(10):
        transaction_data = {
            "amount": f"1{i},34",
            "date": f"1{i}/03/2024",
            "memo": f"memo {i}",
            "direction": "expense"
        }

        many_transaction_data.append(transaction_data)

    response = authenticated_client.post(f'/transaction/create-many-transactions/{user.id}', json = many_transaction_data)
    
    print(response.json())

    assert response.status_code == 201
    assert response.json()['message'] == "Transações criadas"

    months: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months) == 1

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_create_many_transactions_and_create_months_e2e_as_free_with_month_already_created(authenticated_client: TestClient, user_credentials):

    user: User = User.get_user_by_email(user_credentials['email'])

    Month.create(
        user_id = user.id,
        balance_diff = "12,34",
        date = formatDateStrToTimestamp("01/03/2024")
    )

    many_transaction_data = []

    for i in range(10):
        transaction_data = {
            "amount": f"1{i},34",
            "date": f"1{i}/03/2024",
            "memo": f"memo {i}",
            "direction": "expense"
        }

        many_transaction_data.append(transaction_data)

    response = authenticated_client.post(f'/transaction/create-many-transactions/{user.id}', json = many_transaction_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Transações criadas"

    months: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months) == 1

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Transaction, Month])
async def test_update_transaction_and_update_months_e2e_as_free(authenticated_client: TestClient, user_credentials):    

    user: User = User.get_user_by_email(user_credentials['email'])

    transaction_data = {
        "amount": "12,34",
        "date": "12/02/2024",
        "memo": "memo",
        "direction": "expense"
    }

    response = authenticated_client.post(f'/transaction/ops/{user.id}', json = transaction_data)

    assert response.status_code == 201
    assert response.json()['message'] == "Transação criada"
    assert response.json()['transaction']['user_id'] == user.id 
    assert response.json()['transaction']['amount'] == '12,34'
    assert response.json()['transaction']['date'] == "12/02/2024"
    assert response.json()['transaction']['memo'] == "memo"
    assert response.json()['transaction']['direction'] == "expense"

    months: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months) == 1
    assert months[0].user_id_id == user.id
    assert months[0].balance_diff == 0
    assert months[0].date == formatDateStrToTimestamp("01/02/2024")


    update_transaction_data = {
        "amount": "12,34",
        "date": "12/04/2024",
        "memo": "memo",
        "direction": "income"
    }

    update_response = authenticated_client.put(f'/transaction/ops/{response.json()["transaction"]["id"]}', json = update_transaction_data)

    assert update_response.status_code == 200
    assert update_response.json()['message'] == "Transação atualizada"
    assert update_response.json()['transaction']['user_id'] == user.id
    assert update_response.json()['transaction']['amount'] == '12,34'
    assert update_response.json()['transaction']['date'] == "12/04/2024"
    assert update_response.json()['transaction']['memo'] == "memo"
    assert update_response.json()['transaction']['direction'] == "income"

    months_after_update_transaction: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months_after_update_transaction) == 2
    assert months_after_update_transaction[0].user_id_id == user.id
    assert months_after_update_transaction[0].balance_diff == 0
    assert months_after_update_transaction[0].date == formatDateStrToTimestamp("01/02/2024")
    assert months_after_update_transaction[1].user_id_id == user.id
    assert months_after_update_transaction[1].balance_diff == 0
    assert months_after_update_transaction[1].date == formatDateStrToTimestamp("01/04/2024")
    