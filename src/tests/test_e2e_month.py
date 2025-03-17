import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from src.server import app
from models import User, Month
from testUtils import setupDatabaseFileWithTables, setupDatabaseHandleLoggedUser
from utils import formatDateStrToTimestamp

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