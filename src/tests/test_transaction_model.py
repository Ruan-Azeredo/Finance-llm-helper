import pytest

from models import Transaction, User
from testUtils import db_session
from utils import formatDateStrToTimestamp, formatTimestampToDateStr

def test_create_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'password'
    )
    
    assert transaction.id != None
    assert transaction.date == 1733972400
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
            date = '12/12/2024',
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
        date = '12/12/2024',
        memo = 'password'
    )

    transaction.update(
        amount = '22,55',
        category = 'category'
    )

    updaded_transaction: Transaction = Transaction.from_id(transaction.id)

    assert updaded_transaction.category == 'category'
    assert updaded_transaction.amount == 22.55
    assert updaded_transaction.user_id_id == user.id
    assert updaded_transaction.date == 1733972400
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
        date = '12/12/2024',
        memo = 'password',
        category = 'category'
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
        date = '12/12/2024',
        memo = 'password',
        category = 'category'
    )

    transaction.update(
        category = 'null'
    )

    updaded_transaction: Transaction = Transaction.from_id(transaction.id)

    assert updaded_transaction.category == None

def test_get_transactions_by_user_id_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'password'
    )

    transactions = Transaction.get_transactions_by_user_id(user.id)

    assert len(transactions) == 1

    assert transactions[0].amount == 12.34
    assert transactions[0].date == 1733972400
    assert transactions[0].memo == 'password'
    assert transactions[0].user_id_id == user.id

    Transaction.create(
        user_id = user.id,
        amount = '44,22',
        date = '12/12/2024',
        memo = 'memo'
    )

    Transaction.create(
        user_id = user.id,
        amount = '25,87',
        date = '12/12/2024',
        memo = 'xixixi'
    )

    transactions = Transaction.get_transactions_by_user_id(user.id)

    assert len(transactions) == 3

    for transaction in transactions:
        assert transaction.user_id_id == user.id
        assert isinstance(transaction, Transaction)

    assert transactions[0].amount == 12.34
    assert transactions[0].date == 1733972400
    assert transactions[0].memo == 'password'
    assert transactions[0].user_id_id == user.id

    assert transactions[1].amount == 44.22
    assert transactions[1].date == 1733972400
    assert transactions[1].memo == 'memo'
    assert transactions[1].user_id_id == user.id

    assert transactions[2].amount == 25.87
    assert transactions[2].date == 1733972400
    assert transactions[2].memo == 'xixixi'
    assert transactions[2].user_id_id == user.id

def test_get_transactions_by_user_id_transaction_model_with_nonexistent_user_id():

    with pytest.raises(Exception) as error:
        Transaction.get_transactions_by_user_id(14)

    assert 'Usuario com id 14 nao encontrado' in str(error.value)

def test_get_transactions_by_user_id_transaction_model_with_dates_range(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    Transaction.create(
        user_id = user.id,
        amount = '44,22',
        date = '12/11/2024',
        memo = 'memo'
    )

    Transaction.create(
        user_id = user.id,
        amount = '25,87',
        date = '12/12/2024',
        memo = 'xixixi'
    )

    transactions = Transaction.get_transactions_by_user_id(user.id, start_date = formatDateStrToTimestamp('12/11/2024'), end_date = formatDateStrToTimestamp('12/12/2024'))

    assert len(transactions) == 2

    assert transactions[0].amount == 44.22
    assert formatTimestampToDateStr(transactions[0].date) == '12/11/2024'
    assert transactions[0].memo == 'memo'
    assert transactions[0].user_id_id == user.id

    assert transactions[1].amount == 25.87
    assert formatTimestampToDateStr(transactions[1].date) == '12/12/2024'
    assert transactions[1].memo == 'xixixi'
    assert transactions[1].user_id_id == user.id

    transactions = Transaction.get_transactions_by_user_id(user.id, start_date = formatDateStrToTimestamp('11/11/2024'), end_date = formatDateStrToTimestamp('11/12/2024'))

    assert len(transactions) == 1

    assert transactions[0].amount == 44.22
    assert formatTimestampToDateStr(transactions[0].date) == '12/11/2024'
    assert transactions[0].memo == 'memo'
    assert transactions[0].user_id_id == user.id

    transactions = Transaction.get_transactions_by_user_id(user.id, start_date = formatDateStrToTimestamp('09/11/2024'), end_date = formatDateStrToTimestamp('10/11/2024'))

    assert len(transactions) == 0

    Transaction.create(
        user_id = user.id,
        amount = '78,45',
        date = '14/11/2024',
        memo = 'laele'
    )

    Transaction.create(
        user_id = user.id,
        amount = '265,90',
        date = '16/12/2024',
        memo = 'ruan'
    )

    transactions = Transaction.get_transactions_by_user_id(user.id, start_date = formatDateStrToTimestamp('13/11/2024'))

    assert len(transactions) == 3

    assert transactions[0].amount == 78.45
    assert formatTimestampToDateStr(transactions[0].date) == '14/11/2024'
    assert transactions[0].memo == 'laele'
    assert transactions[0].user_id_id == user.id

    assert transactions[1].amount == 25.87
    assert formatTimestampToDateStr(transactions[1].date) == '12/12/2024'
    assert transactions[1].memo == 'xixixi'
    assert transactions[1].user_id_id == user.id

    assert transactions[2].amount == 265.90
    assert formatTimestampToDateStr(transactions[2].date) == '16/12/2024'
    assert transactions[2].memo == 'ruan'
    assert transactions[2].user_id_id == user.id

    transactions = Transaction.get_transactions_by_user_id(user.id, end_date = formatDateStrToTimestamp('14/11/2024'))

    assert len(transactions) == 2

    assert transactions[0].amount == 44.22
    assert formatTimestampToDateStr(transactions[0].date) == '12/11/2024'
    assert transactions[0].memo == 'memo'
    assert transactions[0].user_id_id == user.id

    assert transactions[1].amount == 78.45
    assert formatTimestampToDateStr(transactions[1].date) == '14/11/2024'
    assert transactions[1].memo == 'laele'
    assert transactions[1].user_id_id == user.id

def test_update_category_transaction_model(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )
    
    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'memo'
    )

    transaction.update_category('category')

    transaction_updated = Transaction.from_id(transaction.id)

    assert transaction_updated.category == 'category'  

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
            date = '12/12/2024',
            memo = 'memo'
        )

        assert 'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: 12.34' in str(error.value)

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '12,3',
            date = '12/12/2024',
            memo = 'memo'
        )
    
        assert 'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: 12,3' in str(error.value)

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '-12,35',
            date = '12/12/2024',
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
            date = '12/12/2024',
            memo = 'memo',
            direction = 'wrong'
        )

    assert 'Formato de direction está incorreto, direction deve ser "expense" ou "income". O direction recebido foi: wrong' in str(error.value)

    with pytest.raises(Exception) as other_error:
        Transaction.create(
            user_id = user.id,
            amount = '12,34',
            date = '12/12/2024',
            memo = 'memo',
            direction = 12
        )

    assert 'Formato de direction está incorreto, direction deve ser "expense" ou "income". O direction recebido foi: 12' in str(other_error.value)

def test_create_transaction_with_wrong_date_format(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = user.id,
            amount = '12,34',
            date = '12/12/24',
            memo = 'memo',
            direction = 'income'
        )

    print(error.value)
    assert 'Formato de data inválido. Use dd/mm/aaaa. O formato recebido foi: 12/12/24' in str(error.value)

## test formaters ## ------------------------------- ##

def test_format_date(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'memo',
        direction = 'income'
    )

    assert transaction.date == 1733972400

def test_format_amount(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'memo',
        direction = 'income'
    )

    assert transaction.amount == 12.34

def test_formated_amount(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'memo',
        direction = 'income'
    )

    assert transaction.amount == 12.34
    assert transaction.formatedAmount() == '12,34'

def test_formated_date(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'memo',
        direction = 'income'
    )

    assert transaction.date == 1733972400
    assert transaction.formatedDate() == '12/12/2024'
    
def test_formated_transaction_to_client(db_session):

    user: User = User.create(
        name = 'name',
        email = 'email@email.com',
        password = 'password'
    )

    transaction: Transaction = Transaction.create(
        user_id = user.id,
        amount = '12,34',
        date = '12/12/2024',
        memo = 'memo',
        direction = 'income'
    )

    assert transaction.formatedTransactionToClient().id == transaction.id
    assert transaction.formatedTransactionToClient().amount == '12,34'
    assert transaction.formatedTransactionToClient().date == '12/12/2024'
    assert transaction.formatedTransactionToClient().memo == 'memo'
    assert transaction.formatedTransactionToClient().direction == 'income'