import pytest
from datetime import datetime

from models import Month, User, Transaction
from testUtils import db_session
from utils import formatDateStrToTimestamp

# test dependencies
def monthToTimestamp(month: str, year: int = 2025):
    month_number = datetime.strptime(month[:3], '%b').month
    return formatDateStrToTimestamp(f'01/{month_number:02d}/{year}')

def test_create_month_model(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = monthToTimestamp('Mar'),
        user_id = user.id
    )

    month: Month = Month.from_id(1)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('Mar')

def test_get_month_by_timestamp_date_and_user(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = monthToTimestamp('Mar'),
        user_id = user.id
    )

    month: Month = Month.get_month_by_timestamp_date_and_user(monthToTimestamp('Mar'), user.id)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('Mar')

def test_get_month_by_timestamp_date_and_user_not_found_date(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('21/03/2025'),
        user_id = user.id
    )

    with pytest.raises(Exception) as error:
    
        Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/03/2025'), user.id)

        print(error.value)
        assert error.value.args[0] == f"Mes com data 01/03/2025 nao encontrado"

def test_get_months_by_user_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('21/03/2025'),
        user_id = user.id
    )

    Month.create(
        date = formatDateStrToTimestamp('21/04/2025'),
        user_id = user.id
    )

    months: list[Month] = Month.get_months_by_user_id(user.id)

    assert len(months) == 2

def test_update_month_model(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('21/03/2025'),
        user_id = user.id
    )

    Month.update(
        id = 1,
        balance_diff = 100
    )

    updated_month: Month = Month.from_id(1)
    assert updated_month.balance_diff == 100
    assert updated_month.user_id_id == user.id
    assert updated_month.date == monthToTimestamp('Mar')

def test_verify_and_create(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.verify_and_create(formatDateStrToTimestamp('21/03/2025'), user.id)
    
    month: Month = Month.get_month_by_timestamp_date_and_user(monthToTimestamp('Mar'), user.id)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('Mar')

    Month.verify_and_create(formatDateStrToTimestamp('28/03/2025'), user.id)

    month: Month = Month.get_month_by_timestamp_date_and_user(monthToTimestamp('Mar'), user.id)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('Mar')

    total_user_months = Month.get_months_by_user_id(user.id)

    assert len(total_user_months) == 1

    Month.verify_and_create(formatDateStrToTimestamp('03/04/2025'), user.id)

    total_user_months = Month.get_months_by_user_id(user.id)

    assert len(total_user_months) == 2

    assert total_user_months[0].date == monthToTimestamp('Mar')
    assert total_user_months[1].date == monthToTimestamp('Apr')

    assert total_user_months[0].balance_diff == 0
    assert total_user_months[1].balance_diff == 0

    # Test balance_diff logical

    Transaction.create(
        date = '14/04/2025',
        memo = 'description',
        amount = '134,50',
        user_id = user.id
    )

    Transaction.create(
        date = '21/04/2025',
        memo = 'description',
        amount = '10,00',
        user_id = user.id
    )

    Month.verify_and_create(formatDateStrToTimestamp('05/05/2025'), user.id)
    month: Month = Month.get_month_by_timestamp_date_and_user(monthToTimestamp('May'), user.id)

    assert month.balance_diff == 144.50
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('May')

    # Should not update balance_diff from created month

    Month.verify_and_create(formatDateStrToTimestamp('10/05/2025'), user.id)
    month: Month = Month.get_month_by_timestamp_date_and_user(monthToTimestamp('May'), user.id)

    assert month.balance_diff == 144.50
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('May')

    Month.verify_and_create(formatDateStrToTimestamp('10/04/2025'), user.id)
    month: Month = Month.get_month_by_timestamp_date_and_user(monthToTimestamp('Apr'), user.id)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == monthToTimestamp('Apr')

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

def test_create_month_model_with_invalid_date(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
    
        Month.create(
            date = formatDateStrToTimestamp('21/13/2025'),
            user_id = user.id
        )

        print(error.value)
        assert error.value.args[0] == f"Data invalida"

def test_create_month_model_with_invalid_user_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
    
        Month.create(
            date = formatDateStrToTimestamp('21/03/2025'),
            user_id = user.id + 1
        )

        print(error.value)
        assert error.value.args[0] == f"Usuário nao encontrado"

def test_update_month_model_with_invalid_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:

        Month.update(
            id = 1,
            balance_diff = '100'
        )

        print(error.value)
        assert error.value.args[0] == f"Mes com id 1 nao encontrado"

def test_update_month_model_with_invalid_balance_diff(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('21/03/2025'),
        user_id = user.id
    )

    with pytest.raises(Exception) as error:
        Month.update(
            id = 1,
            balance_diff = 'invalid'
        )
        print(error.value)
        assert error.value.args[0] == f"Valor invalido para campo balance_diff"

def test_update_month_model_with_invalid_date(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('21/03/2025'),
        user_id = user.id
    )

    with pytest.raises(Exception) as error:
        Month.update(
            id = 1,
            date = 'invalid'
        )
        print(error.value)
        assert error.value.args[0] == f"Data invalida"

def test_update_month_model_with_user_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
            date = formatDateStrToTimestamp('21/03/2025'),
        user_id = user.id
    )

    with pytest.raises(Exception) as error:
        Month.update(
            id = 1,
            user_id = user.id
        )
        print(error.value)
        assert error.value.args[0] == f"O campo 'user_id' nao pode ser alterado"

def test_get_month_by_user_id_with_invalid_user_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Month.get_month_by_user_id(user.id + 1)
        print(error.value)
        assert error.value.args[0] == f"Mes com user_id {user.id + 1} nao encontrado"

def test_get_month_by_timestamp_date_and_user_with_invalid_user_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('21/03/2025'), user.id + 1)
        print(error.value)
        assert error.value.args[0] == f"Mes com user_id {user.id + 1} nao encontrado"


def test_get_month_by_timestamp_date_and_user_with_invalid_date(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('21/13/2025'), user.id)
        print(error.value)
        assert error.value.args[0] == f"Mes com data 21/13/2025 nao encontrado"


def test_verify_and_create_with_invalid_date(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Month.verify_and_create(formatDateStrToTimestamp('21/13/2025'), user.id)
        print(error.value)
        assert error.value.args[0] == f"Data invalida"

def test_verify_and_create_with_invalid_user_id(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Month.verify_and_create(formatDateStrToTimestamp('21/03/2025'), user.id + 1)
        print(error.value)
        assert error.value.args[0] == f"Usuário nao encontrado"