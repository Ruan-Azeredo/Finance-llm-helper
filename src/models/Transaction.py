from peewee import CharField, DateTimeField, ForeignKeyField, DoesNotExist, FloatField, IntegerField
from datetime import datetime
import uuid
from copy import deepcopy

from .BaseModel import BaseModel
from models import User
from database import db
from .handles import handle_values, handle_database_error
from utils import validate_transaction_input

class Transaction(BaseModel):
    id = CharField(unique = True, primary_key = True)
    date = IntegerField() #timestamp
    direction = CharField(default = "expense")
    amount = FloatField()
    memo = CharField()
    user_id = ForeignKeyField(User, field='id', backref='transactions', on_delete='CASCADE')
    tag = CharField(default = None, null = True)
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'transactions'

    def __str__(self):
        return f'Transaction: {self.id}, {self.date}, {self.amount}, {self.memo}, {self.tag}, {self.user_id}'
    
    def formatAmountToString(amount: float) -> str:
        return f"{abs(amount):.2f}".replace('.', ',')

    def formatAmountToFloat(amount: str) -> float:
        return float(amount.replace(',', '.'))
    
    def formatTimestampToDateStr(timestamp: int) -> str:
        """
        Converte um timestamp para o formato dd/mm/aaaa.

        :param timestamp: Timestamp em segundos.
        :return: Data no formato dd/mm/aaaa.
        """
        data = datetime.fromtimestamp(timestamp)
        return data.strftime("%d/%m/%Y")



    def formatDateStrToTimestamp(data: str) -> int:
        """
        Converte uma data no formato dd/mm/aaaa para timestamp.

        :param data: Data no formato dd/mm/aaaa.
        :return: Timestamp correspondente em segundos.
        """
        try:
            data_formatada = datetime.strptime(data, "%d/%m/%Y")
            return int(data_formatada.timestamp())
        except ValueError:
            raise ValueError("Formato de data inválido. Use dd/mm/aaaa.")

    def formatTransactionToClient(self) -> 'Transaction':
        formatedTrasaction = deepcopy(self)
        formatedTrasaction.amount = self.formatAmountToString(formatedTrasaction.amount)
        formatedTrasaction.date = self.formatTimestampToDateStr(formatedTrasaction.date)

        return formatedTrasaction

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

        if 'amount' in values:
            values['amount'] = Transaction.formatAmountToFloat(values['amount'])

        if 'date' in values:
            values['date'] = Transaction.formatDateStrToTimestamp(values['date'])

        created_transaction = super(Transaction, Transaction).create(**values)

        return created_transaction
    
    @handle_database_error
    def update(self, **kwargs) -> None:

        validate_transaction_input(kwargs)

        if 'user_id' in kwargs:
            raise Exception("O campo 'user_id' não pode ser alterado")

        values = handle_values(kwargs)

        if 'amount' in values:
            values['amount'] = Transaction.formatAmountToFloat(values['amount'])

        if 'date' in values:
            values['date'] = Transaction.formatDateStrToTimestamp(values['date'])

        super(Transaction, self).update(**values)

    @handle_database_error
    def get_transactions_by_user_id(user_id: int) -> list['Transaction']:

        try:
            User.get_by_id(user_id)
        except Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        return Transaction.select().where(Transaction.user_id == user_id)
    
    @handle_database_error
    def update_tag(self, tag: str) -> None:
        self.update(tag = tag)
    