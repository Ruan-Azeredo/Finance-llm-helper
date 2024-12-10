from peewee import SqliteDatabase, IntegrityError
import pytest

from models import Transaction, User

def setupTestDatabase():
    test_db = SqliteDatabase(':memory:')
    Transaction._meta.database = test_db
    User._meta.database = test_db

    return test_db

def test_create_user_model():

    test_db = setupTestDatabase()
    
    test_db.connect()
    
    test_db.create_tables([User, Transaction])

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
    assert transaction.amount == '12,34'
    assert transaction.memo == 'password'

    # transaction.user_id automatically get the User, to get just the id, use transaction.user_id_id
    assert transaction.user_id_id == user.id

def test_create_transaction_with_nonexistent_user():

    test_db = setupTestDatabase()
    
    test_db.connect()
    
    test_db.create_tables([User, Transaction])
    
    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Transaction.create(
            user_id = 1,
            amount = '12.34',
            date = '2024-12-09',
            memo = 'Test memo'
        )

    assert 'Registro não encontrado: Usuario com id 1 nao encontrado' in str(error.value)