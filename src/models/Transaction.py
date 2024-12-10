from peewee import CharField, DateTimeField, ForeignKeyField, DoesNotExist
from datetime import datetime
import uuid

from .BaseModel import BaseModel
from models import User
from database import db
from  .utils import handle_values, handle_database_error

class Transaction(BaseModel):
    id = CharField(unique = True, primary_key = True)
    date = CharField()
    amount = CharField()
    memo = CharField()
    user_id = ForeignKeyField(User, field='id', backref='transactions', on_delete='CASCADE')
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'transactions'

    def __str__(self):
        return f'Transaction: {self.id}, {self.date}, {self.amount}, {self.memo}, {self.user_id}'

    @handle_database_error
    def create(user_id: int, **kwargs) -> 'Transaction':

        try:
            User.get_by_id(user_id)
        except Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        def _defineId():
            return str(uuid.uuid4()) + '|' + str(user_id)

        kwargs.setdefault('id', _defineId())

        values = handle_values(kwargs)
        values['user_id'] = user_id

        return super(Transaction, Transaction).create(**values)