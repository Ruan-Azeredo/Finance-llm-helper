import pytest

from models import Transaction, User
from testUtils import db_session

def test_create_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = 'date',
        memo = 'password'
    )
    
    assert transaction.id != None
    assert transaction.date == 'date'
    assert transaction.amount == 12.34
    assert transaction.memo == 'password'

    # transaction.user_id automatically get the User, to get just the id, use transaction.user_id_id
    assert transaction.user_id_id == user.id

def test_create_transaction_model_with_nonexistent_user(db_session):
    
    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = 1,
            amount = '12,34',
            date = '2024-12-09',
            memo = 'Test memo'
        )

    assert 'Registro não encontrado: Usuario com id 1 nao encontrado' in str(error.value)

def test_update_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = 'date',
        memo = 'password'
    )

    transaction.update(
        amount = '22,55',
        tag = 'tag'
    )

    updaded_transaction: Transaction = Transaction.from_id(transaction.id)

    assert updaded_transaction.tag == 'tag'
    assert updaded_transaction.amount == 22.55
    assert updaded_transaction.user_id_id == user.id
    assert updaded_transaction.date == 'date'
    assert updaded_transaction.memo == 'password'

def test_update_transaction_model_with_wrong_type_properties_null(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = 'date',
        memo = 'password',
        tag = 'tag'
    )

    with pytest.raises(Exception) as error:
        transaction.update(
            amount = 'null'
        )

    assert 'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: null' in str(error.value)

def test_update_transaction_model_with_right_type_properties_null(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = 'date',
        memo = 'password',
        tag = 'tag'
    )

    transaction.update(
        tag = 'null'
    )

    updaded_transaction: Transaction = Transaction.from_id(transaction.id)

    assert updaded_transaction.tag == None

def test_get_transactions_by_user_id_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = 'date',
        memo = 'password'
    )

    transactions = Transaction.get_transactions_by_user_id(user.id)

    assert len(transactions) == 1

    assert transactions[0].amount == 12.34
    assert transactions[0].date == 'date'
    assert transactions[0].memo == 'password'
    assert transactions[0].user_id_id == user.id

    Transaction.create(
        user_id = user.id,
        amount = '44,22',
        date = 'uwu',
        memo = 'memo'
    )

    Transaction.create(
        user_id = user.id,
        amount = '25,87',
        date = 'hihi',
        memo = 'xixixi'
    )

    transactions = Transaction.get_transactions_by_user_id(user.id)

    assert len(transactions) == 3

    for transaction in transactions:
        assert transaction.user_id_id == user.id
        assert isinstance(transaction, Transaction)

    assert transactions[0].amount == 12.34
    assert transactions[0].date == 'date'
    assert transactions[0].memo == 'password'
    assert transactions[0].user_id_id == user.id

    assert transactions[1].amount == 44.22
    assert transactions[1].date == 'uwu'
    assert transactions[1].memo == 'memo'
    assert transactions[1].user_id_id == user.id

    assert transactions[2].amount == 25.87
    assert transactions[2].date == 'hihi'
    assert transactions[2].memo == 'xixixi'
    assert transactions[2].user_id_id == user.id

def test_get_transactions_by_user_id_transaction_model_with_nonexistent_user_id():

    with pytest.raises(Exception) as error:
        Transaction.get_transactions_by_user_id(14)

    assert 'Usuario com id 14 nao encontrado' in str(error.value)

def test_update_tag_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = 'date',
        memo = 'memo'
    )

    transaction.update_tag('tag')

    transaction_updated = Transaction.from_id(transaction.id)

    assert transaction_updated.tag == 'tag'

def test_create_transaction_with_wrong_amount_format(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '12.34',
            date = 'date',
            memo = 'memo'
        )

        assert 'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: 12.34' in str(error.value)

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '12,3',
            date = 'date',
            memo = 'memo'
        )
    
        assert 'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: 12,3' in str(error.value)

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '-12,35',
            date = 'date',
            memo = 'memo'
        )

        assert 'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: -12,35' in str(error.value)

def test_create_transaction_with_wrong_direction_format(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '12,34',
            date = 'date',
            memo = 'memo',
            direction = 'wrong'
        )

    assert 'Formato de direction está incorreto, direction deve ser "expense" ou "income". O direction recebido foi: wrong' in str(error.value)

    with pytest.raises(Exception) as other_error:
        Transaction.create(
            user_id = user.id,
            amount = '12,34',
            date = 'date',
            memo = 'memo',
            direction = 12
        )

    assert 'Formato de direction está incorreto, direction deve ser "expense" ou "income". O direction recebido foi: 12' in str(other_error.value)