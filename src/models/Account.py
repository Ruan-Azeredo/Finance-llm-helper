from .BaseModel import BaseModel
from peewee import CharField, IntegerField, FloatField, AutoField, ForeignKeyField, DateTimeField, DoesNotExist
from datetime import datetime, timezone
from copy import deepcopy

from .handles import handle_values, handle_database_error
from database import db
from models import User
from utils import validate_account_input, formatDateStrToTimestamp, formatAmountToFloat, formatAmountToString

class Account(BaseModel):
    id = AutoField(unique = True, primary_key = True)
    name = CharField(null = False)
    user_id = ForeignKeyField(User, field = 'id', backref = 'accounts', on_delete = 'CASCADE')
    balance = FloatField(default = 0)
    balance_updated = IntegerField(default = datetime.now(timezone.utc).timestamp())
    origin = CharField(default = "default")
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'accounts'

    def formatedAccountToClient(self) -> 'Account':
        formatedAccount = deepcopy(self)
        formatedAccount.balance = formatAmountToString(formatedAccount.balance)

        return formatedAccount

    @handle_database_error
    def create(user_id: int, **kwargs) -> 'Account':
        
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        validate_account_input(kwargs)
        values = handle_values(kwargs)
        values['user_id'] = user_id

        # Convert balance from string to float if provided
        if 'balance' in values and values['balance'] is not None:
            values['balance'] = formatAmountToFloat(values['balance'])

        return super(Account, Account).create(**values)


    @handle_database_error
    def update(self, **kwargs) -> 'Account':
        validate_account_input(kwargs)
        values = handle_values(kwargs)

        # Convert balance from string to float if provided
        if 'balance' in values and values['balance'] is not None:
            values['balance'] = formatAmountToFloat(values['balance'])
            values['balance_updated'] = datetime.now(timezone.utc).timestamp()

        return super(Account, self).update(**values)

    @handle_database_error
    def delete(self) -> 'Account':

        user_accounts = Account.select().where(Account.user_id == self.user_id)

        if len(user_accounts) == 1:
            raise Exception("Nao e possivel excluir a ultima conta do usuario")

        return super(Account, self).delete()

    @handle_database_error
    def get_accounts_by_user_id(user_id: int) -> list['Account']:

        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        return Account.select().where(Account.user_id == user_id).order_by(Account.id.asc())

    @handle_database_error
    def verify_and_update_balance(transaction_amount: float, transaction_str_date: str, account_id: int) -> None:
        try:
            account: Account = Account.get_by_id(account_id)
            if account.balance_updated < formatDateStrToTimestamp(transaction_str_date):
                account.balance += transaction_amount
                account.balance_updated = datetime.now(timezone.utc).timestamp()
                account.save()
        except Exception as error:
            raise Exception(f"Erro ao atualizar saldo da conta: {error}")