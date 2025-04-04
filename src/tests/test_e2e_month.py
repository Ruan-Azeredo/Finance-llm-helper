import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.server import app
from models import User, Month, Transaction
from testUtils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser, setup_database_with_tables
from utils import formatDateStrToTimestamp, formatTimestampToDateStr

client_test = TestClient(app)

@pytest.mark.e2e
@pytest.mark.asyncio
@setupDatabaseHandleLoggedUser(client_test = client_test, models = [User, Month])
async def test_update_month_e2e(authenticated_client: TestClient, user_credentials):
    user: User = User.get_user_by_email(user_credentials['email'])

    Month.verify_and_create(formatDateStrToTimestamp('06/03/2025'), user.id)

    month: Month = Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/03/2025'), user.id)

    assert month.balance_diff == 0

    response = authenticated_client.put(f'/month/ops/{month.id}', json = {
        "balance_diff": "12,34"
    })

    print(response.json())
    assert response.status_code == 200
    assert response.json()['message'] == "Month atualizado"
    assert response.json()['month']['balance_diff'] == '12,34'
    assert response.json()['month']['user_id'] == user.id
    assert response.json()['month']['date'] == formatDateStrToTimestamp('01/03/2025')

"""
handle  errors, controller errors

create tests in transactionsController.py to handle errors annd months creation especific cases
"""


@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User, Month, Transaction]}], indirect=True)
async def test_months_balance(setup_database_with_tables):

    authenticated_client = setup_database_with_tables['authenticated_client']
    user_credentials = setup_database_with_tables['user_credentials']

    user: User = User.get_user_by_email(user_credentials['email'])

    #----------------------------------------------------------------------

    # balance_diff = 0
    Month.verify_and_create(
        transaction_date = formatDateStrToTimestamp('01/03/2025'),
        user_id = user.id
    )

    month_1: Month = Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/03/2025'), user.id)
    print(month_1.balance_diff, formatTimestampToDateStr(month_1.date), ' - ', month_1.date)

    Transaction.create(
        user_id = user.id,
        amount = '10,00',
        date = '21/03/2025',
        memo = 'memo',
        direction = 'expense'
    )

    Transaction.create(
        user_id = user.id,
        amount = '25,00',
        date = '31/03/2025',
        memo = 'memo',
        direction = 'expense'
    )

    # Saldo do mes 3 de 2025 = - 35,00

    #------------------------- ----------------- ------------- -------- ---

    # balance_diff = - 35,00
    Month.verify_and_create(
        transaction_date = formatDateStrToTimestamp('01/04/2025'),
        user_id = user.id
    )

    month_2: Month = Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/04/2025'), user.id)
    print(month_2.balance_diff, formatTimestampToDateStr(month_2.date), ' - ', month_2.date)

    Transaction.create(
        user_id = user.id,
        amount = '10,00',
        date = '21/04/2025',
        memo = 'memo',
        direction = 'expense'
    )

    Transaction.create(
        user_id = user.id,
        amount = '50,00',
        date = '14/04/2025',
        memo = 'memo',
        direction = 'income'
    )

    # Saldo do mes 4 de 2025 = - 35,00 - 10,00 + 50,00 = 5,00

    # ----------------------------------------------------------------------

    response = authenticated_client.post(f'/month/require-balances/', json = {
        "timestamps": [formatDateStrToTimestamp('01/03/2025'), formatDateStrToTimestamp('01/04/2025')]
    })

    print(response.json())

    assert response.status_code == 200
    assert response.json()[str(formatDateStrToTimestamp('01/03/2025'))]['balance'] == -35.00
    assert response.json()[str(formatDateStrToTimestamp('01/04/2025'))]['balance'] == 5.00

@pytest.mark.e2e
@pytest.mark.asyncio
@pytest.mark.parametrize("setup_database_with_tables", [{"models": [User, Month, Transaction]}], indirect=True)
async def test_year_balance(setup_database_with_tables):

    authenticated_client = setup_database_with_tables['authenticated_client']
    user_credentials = setup_database_with_tables['user_credentials']

    user: User = User.get_user_by_email(user_credentials['email'])

    #----------------------------------------------------------------------

    # balance_diff = 0
    Month.verify_and_create(
        transaction_date = formatDateStrToTimestamp('01/03/2025'),
        user_id = user.id
    )

    Transaction.create(
        user_id = user.id,
        amount = '10,00',
        date = '21/03/2025',
        memo = 'memo',
        direction = 'expense'
    )

    Transaction.create(
        user_id = user.id,
        amount = '25,00',
        date = '31/03/2025',
        memo = 'memo',
        direction = 'expense'
    )

    # Saldo do mes 3 de 2025 = - 35,00

    #------------------------- ----------------- ------------- -------- ---

    # balance_diff = - 35,00
    Month.verify_and_create(
        transaction_date = formatDateStrToTimestamp('01/04/2025'),
        user_id = user.id
    )

    Transaction.create(
        user_id = user.id,
        amount = '10,00',
        date = '21/04/2025',
        memo = 'memo',
        direction = 'expense'
    )

    Transaction.create(
        user_id = user.id,
        amount = '50,00',
        date = '14/04/2025',
        memo = 'memo',
        direction = 'income'
    )

    # Saldo do mes 4 de 2025 = - 35,00 - 10,00 + 50,00 = 5,00

    # ----------------------------------------------------------------------

    # Saldo final de de 2025 = ultimo saldo do mes 4 de 2025 = 5,00

    response = authenticated_client.post(f'/month/require-balances', json = {
        "timestamps": [formatDateStrToTimestamp('01/01/2024'), formatDateStrToTimestamp('01/01/2025'), formatDateStrToTimestamp('01/01/2026')],
        "type": "years"
    })

    print(response.json())

    assert response.status_code == 200
    assert response.json()[str(formatDateStrToTimestamp('01/01/2024'))]['balance'] == 0
    assert response.json()[str(formatDateStrToTimestamp('01/01/2025'))]['balance'] == 5.00
    assert response.json()[str(formatDateStrToTimestamp('01/01/2026'))]['balance'] == 5.00
