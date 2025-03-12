from peewee import CharField, DateTimeField, ForeignKeyField, DoesNotExist, FloatField, IntegerField
from datetime import datetime
import uuid
from copy import deepcopy

from .BaseModel import BaseModel
from models import User
from database import db
from .handles import handle_values, handle_database_error
from utils import validate_transaction_input, formatAmountToString, formatTimestampToDateStr, formatDateStrToTimestamp, formatAmountToFloat

class Transaction(BaseModel):
    id = CharField(unique = True, primary_key = True)
    date = IntegerField() #timestamp
    direction = CharField(default = "expense")
    amount = FloatField()
    memo = CharField()
    user_id = ForeignKeyField(User, field='id', backref='transactions', on_delete='CASCADE')
    category = CharField(default = None, null = True)
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'transactions'

    def __str__(self):
        return f'Transaction: {self.id}, {self.date}, {self.amount}, {self.memo}, {self.category}, {self.user_id}'
    
    def formatedAmount(self) -> str:
        formatedTrasaction = deepcopy(self)
        print(formatedTrasaction)
        return formatAmountToString(formatedTrasaction.amount)
    
    def formatedDate(self) -> str:
        formatedTrasaction = deepcopy(self)
        return formatTimestampToDateStr(formatedTrasaction.date)

    def formatedTransactionToClient(self) -> 'Transaction':
        formatedTrasaction = deepcopy(self)
        formatedTrasaction.amount = formatAmountToString(formatedTrasaction.amount)
        formatedTrasaction.date = formatTimestampToDateStr(formatedTrasaction.date)

        return formatedTrasaction
    
    def _prepareFormatsToDb(values: dict) -> dict:
        if 'amount' in values:
            values['amount'] = formatAmountToFloat(values['amount'])

        if 'date' in values:
            values['date'] = formatDateStrToTimestamp(values['date'])

        return values

    @handle_database_error
    def create(user_id: int, **kwargs) -> 'Transaction':

        validate_transaction_input(kwargs)

        try:
            User.get_by_id(user_id) 
        except Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        def _defineId():
            return str(uuid.uuid4()) + '|' + str(user_id)

        kwargs.setdefault('id', _defineId())

        values = handle_values(kwargs)
        values['user_id'] = user_id

        values = Transaction._prepareFormatsToDb(values)

        created_transaction = super(Transaction, Transaction).create(**values)

        return created_transaction
    
    @handle_database_error
    def update(self, **kwargs) -> None:

        validate_transaction_input(kwargs)

        if 'user_id' in kwargs:
            raise Exception("O campo 'user_id' não pode ser alterado")

        values = handle_values(kwargs)

        values = Transaction._prepareFormatsToDb(values)

        super(Transaction, self).update(**values)

    @handle_database_error
    def get_transactions_by_user_id(user_id: int, start_date: int = None, end_date: int = None) -> list['Transaction']:

        try:
            User.get_by_id(user_id)
        except Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        if start_date and end_date:
            transactions = Transaction.select().where(Transaction.user_id == user_id, Transaction.date >= start_date, Transaction.date <= end_date)
        elif start_date:
            transactions = Transaction.select().where(Transaction.user_id == user_id, Transaction.date >= start_date)
        elif end_date:
            transactions = Transaction.select().where(Transaction.user_id == user_id, Transaction.date <= end_date)
        else:
            transactions = Transaction.select().where(Transaction.user_id == user_id)

        return transactions.order_by(Transaction.date.asc())
    
    @handle_database_error
    def update_category(self, category: str) -> None:
        self.update(category = category)
    