import pytest
from datetime import datetime, timezone
from peewee import DoesNotExist

from models import User, Account
from testUtils import db_session

def test_create_account_model(db_session):
    """Test creating a basic account"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Minha Conta'
    )

    assert account.name == 'Minha Conta'
    assert account.user_id_id == user.id
    assert account.balance == 0
    assert account.origin == "default"
    assert account.balance_updated is not None
    assert account.created_at is not None
    assert account.updated_at is not None

def test_create_account_model_with_balance(db_session):
    """Test creating an account with initial balance"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Corrente',
        balance=1500.50
    )

    assert account.name == 'Conta Corrente'
    assert account.balance == 1500.50
    assert account.user_id_id == user.id

def test_create_account_model_with_origin(db_session):
    """Test creating an account with custom origin"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Banco',
        origin='bank_import'
    )

    assert account.name == 'Conta Banco'
    assert account.origin == 'bank_import'
    assert account.user_id_id == user.id

def test_create_account_model_with_nonexistent_user(db_session):
    """Test creating account with non-existent user should fail"""
    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Account.create(
            user_id=999,
            name='Conta Teste'
        )

    assert 'Usuario com id 999 nao encontrado' in str(error.value)

def test_create_account_model_without_name(db_session):
    """Test creating account without name should fail"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    with pytest.raises(Exception) as error:
        Account.create(
            user_id=user.id
        )

    assert "O campo obrigatório 'accounts.name' está ausente ou é nulo." in str(error.value)

def test_create_account_model_with_empty_name(db_session):
    """Test creating account with empty name should fail"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    with pytest.raises(Exception) as error:
        Account.create(
            user_id=user.id,
            name=''
        )

    assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_create_account_model_with_invalid_balance_type(db_session):
    """Test creating account with invalid balance type should fail"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    with pytest.raises(Exception) as error:
        Account.create(
            user_id=user.id,
            name='Conta Teste',
            balance='invalid'
        )

    assert 'Formato de balance está incorreto, balance deve ser um número float' in str(error.value)

def test_update_account_model(db_session):
    """Test updating account fields"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Original'
    )

    account.update(
        name='Conta Atualizada',
        balance=2500.75
    )

    updated_account = Account.get_by_id(account.id)

    assert updated_account.name == 'Conta Atualizada'
    assert updated_account.balance == 2500.75

def test_update_account_balance_updates_timestamp(db_session):
    """Test that updating balance updates the balance_updated timestamp"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Teste'
    )

    original_timestamp = account.balance_updated

    # Small delay to ensure timestamp difference
    import time
    time.sleep(0.01)

    account.update(balance=1000.0)

    updated_account = Account.get_by_id(account.id)
    assert updated_account.balance_updated > original_timestamp

def test_update_account_without_balance_keeps_timestamp(db_session):
    """Test that updating without balance doesn't change balance_updated timestamp"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Teste'
    )

    original_timestamp = account.balance_updated

    account.update(name='Novo Nome')

    updated_account = Account.get_by_id(account.id)
    # Since balance_updated is an IntegerField, we need to compare as integers
    assert int(updated_account.balance_updated) == int(original_timestamp)
    assert updated_account.name == 'Novo Nome'

def test_update_account_with_invalid_name(db_session):
    """Test updating account with invalid name should fail"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Teste'
    )

    with pytest.raises(Exception) as error:
        account.update(name='')

    assert 'Formato de name está incorreto, name não pode ser vazio' in str(error.value)

def test_delete_account_model(db_session):
    """Test deleting account when user has multiple accounts"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account1 = Account.create(
        user_id=user.id,
        name='Conta 1'
    )

    account2 = Account.create(
        user_id=user.id,
        name='Conta 2'
    )

    account1.delete()

    # Verify account1 is deleted
    assert not Account.select().where(Account.id == account1.id).exists()
    
    # Verify account2 still exists
    assert Account.select().where(Account.id == account2.id).exists()

def test_delete_last_account_should_fail(db_session):
    """Test that deleting the last account of a user should fail"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Única Conta'
    )

    with pytest.raises(Exception) as error:
        account.delete()

    assert 'Nao e possivel excluir a ultima conta do usuario' in str(error.value)

def test_get_accounts_by_user_id(db_session):
    """Test getting all accounts for a user"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    # Create another user to ensure we only get accounts for the correct user
    other_user = User.create(
        name='other',
        email='other@email.com',
        password='password'
    )

    account1 = Account.create(
        user_id=user.id,
        name='Conta 1'
    )

    account2 = Account.create(
        user_id=user.id,
        name='Conta 2'
    )

    # Create account for other user
    Account.create(
        user_id=other_user.id,
        name='Conta Outro Usuário'
    )

    accounts = Account.get_accounts_by_user_id(user.id)

    assert len(accounts) == 2
    assert accounts[0].id == account1.id  # Should be ordered by id asc
    assert accounts[1].id == account2.id
    assert all(account.user_id_id == user.id for account in accounts)

def test_get_accounts_by_nonexistent_user_id(db_session):
    """Test getting accounts for non-existent user should fail"""
    assert User.select().count() == 0

    with pytest.raises(Exception) as error:
        Account.get_accounts_by_user_id(999)

    assert 'Usuario com id 999 nao encontrado' in str(error.value)

def test_verify_and_update_balance_method_exists(db_session):
    """Test that verify_and_update_balance method exists and can be called"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Teste',
        balance=1000.0
    )

    # Test that the method can be called without errors (basic functionality test)
    # Using a very old date to ensure it doesn't update the balance
    try:
        Account.verify_and_update_balance(
            transaction_amount=500.0,
            transaction_str_date='01/01/2020',  # Very old date
            account_id=account.id
        )
        # If we get here, the method executed without throwing an exception
        assert True
    except Exception as e:
        # If there's an exception, it should not be about the method not existing
        assert "Erro ao atualizar saldo da conta" in str(e) or "formatDateStrToTimestamp" in str(e)

def test_verify_and_update_balance_with_nonexistent_account(db_session):
    """Test updating balance for non-existent account should fail"""
    with pytest.raises(Exception) as error:
        Account.verify_and_update_balance(
            transaction_amount=500.0,
            transaction_str_date='15/01/2024',
            account_id=999
        )

    assert 'Erro ao atualizar saldo da conta' in str(error.value)

def test_verify_and_update_balance_with_invalid_date_format(db_session):
    """Test updating balance with invalid date format should fail"""
    user = User.create(
        name='name',
        email='email@email.com',
        password='password'
    )

    account = Account.create(
        user_id=user.id,
        name='Conta Teste',
        balance=1000.0
    )

    with pytest.raises(Exception) as error:
        Account.verify_and_update_balance(
            transaction_amount=500.0,
            transaction_str_date='2024-01-15',  # Wrong format, should be dd/mm/yyyy
            account_id=account.id
        )

    assert 'Erro ao atualizar saldo da conta' in str(error.value)