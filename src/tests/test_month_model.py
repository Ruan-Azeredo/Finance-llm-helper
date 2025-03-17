import pytest

from models import Month, User
from testUtils import db_session
from utils import formatDateStrToTimestamp

def test_verify_and_create(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.verify_and_create(formatDateStrToTimestamp('21/03/2025'), user.id)
    
    month: Month = Month.from_id(1)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == formatDateStrToTimestamp('01/03/2025')

def test_update_month_model(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    Month.verify_and_create(formatDateStrToTimestamp('21/03/2025'), user.id)

    month: Month = Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/03/2025'), user.id)

    month.update(balance_diff = '100')

    updated_month: Month = Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/03/2025'), user.id)

    assert updated_month.balance_diff == 100
    assert updated_month.user_id_id == user.id
    assert updated_month.date == formatDateStrToTimestamp('01/03/2025')


"""
handle errors, model cases when trigger errors and use cases
"""