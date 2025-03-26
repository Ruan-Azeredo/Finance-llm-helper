import pytest

from models import Month, User
from testUtils import db_session
from utils import formatDateStrToTimestamp

def test_create_month_model(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('01/03/2025'),
        user_id = user.id
    )

    month: Month = Month.from_id(1)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == formatDateStrToTimestamp('01/03/2025')

def test_get_month_by_timestamp_date_and_user(db_session):
    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Month.create(
        date = formatDateStrToTimestamp('01/03/2025'),
        user_id = user.id
    )

    month: Month = Month.get_month_by_timestamp_date_and_user(formatDateStrToTimestamp('01/03/2025'), user.id)

    assert month.balance_diff == 0
    assert month.user_id_id == user.id
    assert month.date == formatDateStrToTimestamp('01/03/2025')

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
    assert updated_month.date == formatDateStrToTimestamp('01/03/2025')

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