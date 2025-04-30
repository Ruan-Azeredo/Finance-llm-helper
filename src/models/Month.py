import peewee as pw
from peewee import DateTimeField, ForeignKeyField, DoesNotExist, FloatField, IntegerField, AutoField
from datetime import datetime
from copy import deepcopy

from .BaseModel import BaseModel
from models import User, Transaction
from database import db
from .handles import handle_values, handle_database_error
from utils import validate_month_input, formatAmountToFloat, formatAmountToString, formatTimestampToDateStr, get_start_and_end_of_month_by_date

class Month(BaseModel):
    id = AutoField(unique = True, primary_key = True)
    date = IntegerField(null = False) #timestamp
    balance_diff = FloatField(default = 0)
    income = FloatField(default = 0, null = True)
    expense = FloatField(default = 0, null = True)
    user_id = ForeignKeyField(User, field='id', backref='months', on_delete='CASCADE')
    created_at = DateTimeField(default = datetime.now())
    updated_at = DateTimeField(default = datetime.now())

    class Meta:
        database = db
        table_name = 'months'

    def _prepareFormatsToDb(values: dict) -> dict:
        if 'balance_diff' in values:
            values['balance_diff'] = formatAmountToFloat(values['balance_diff'])

        return values
    
    def formatedMonthToClient(self) -> 'Month':
        formatedMonth = deepcopy(self)
        return formatedMonth

    @handle_database_error
    def create(user_id: int, **kwargs) -> 'Month':
        
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")
        
        validate_month_input(kwargs)
        values = handle_values(kwargs)
        values['user_id'] = user_id

        return super(Month, Month).create(**values)
    
    @handle_database_error
    def update(self, **kwargs) -> None:
        validate_month_input(kwargs)

        if 'user_id' in kwargs:
            raise Exception("O campo 'user_id' não pode ser alterado")

        values = handle_values(kwargs)

        values = Month._prepareFormatsToDb(values)

        super(Month, self).update(**values)

    # non used yet
    @handle_database_error
    def get_months_by_user_id(user_id: int, max_date_timestamp: int | None = None, min_date_timestamp: int | None = None) -> list['Month']:
        
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")
        
        if max_date_timestamp == None and min_date_timestamp == None:
            return Month.select().where(Month.user_id == user_id).order_by(Month.date.desc())
        elif max_date_timestamp == None:
            return Month.select().where(Month.user_id == user_id, Month.date >= min_date_timestamp).order_by(Month.date.desc())
        elif min_date_timestamp == None:
            return Month.select().where(Month.user_id == user_id, Month.date <= max_date_timestamp).order_by(Month.date.desc())
        else:
            return Month.select().where(Month.user_id == user_id, Month.date >= min_date_timestamp, Month.date <= max_date_timestamp).order_by(Month.date.desc())
        
    @handle_database_error
    def get_last_month_until_date(date: int, user_id: int) -> 'Month':
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")

        try:
            return Month.select().where(Month.user_id == user_id, Month.date <= date).order_by(Month.date.desc()).first()
        except DoesNotExist:
            raise DoesNotExist(f"Mes com data menor do que {formatTimestampToDateStr(date)} nao encontrado para o usuario com id {user_id}")
    
    @handle_database_error
    def get_month_by_timestamp_date_and_user(date: float, user_id: int) -> 'Month':
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")
        
        try:
            return Month.select().where((Month.user_id == user_id) & (Month.date == date)).get()
        except DoesNotExist:
            raise DoesNotExist(f"Mes com data {formatTimestampToDateStr(date)} nao encontrado")
    
    # --------------------------------- verify / create month ---------------------------------------------------------------------------

    def _find_months_to_update_by_date(transaction_date: int, user_id) -> int:
       
        start_of_month, start_of_next_month = get_start_and_end_of_month_by_date(transaction_date)

        months_to_update = Month.select().where(Month.user_id == user_id).where(Month.date >= start_of_month, Month.date < start_of_next_month)

        return months_to_update
    
    def _scan_months_and_get_balance_diff_reference(month_date: int, user_id: int) -> 'Month':

        # closest next month
        closest_month = Month.select().where(Month.user_id == user_id, Month.date > month_date).order_by(Month.date.asc()).first()

        if closest_month:
            balance_diff_reference = closest_month.balance_diff
        else:
            # closest previous month
            closest_month = Month.select().where(Month.user_id == user_id, Month.date < month_date).order_by(Month.date.desc()).first()

            if not closest_month:
                return None
            
            transactions: list[Transaction] = Transaction.select(Transaction.amount, Transaction.direction).where(
                Transaction.user_id == user_id,
                Transaction.date >= closest_month.date,
                Transaction.date < month_date
            )

            transactions_sum = Transaction.sum_transactions_amount(transactions)

            balance_diff_reference = closest_month.balance_diff + transactions_sum

        return balance_diff_reference
    
    @handle_database_error
    def verify_and_create(transaction_date: int, user_id: int) -> None:
        
        months_to_update = Month._find_months_to_update_by_date(transaction_date, user_id)

        start_of_month, _ = get_start_and_end_of_month_by_date(transaction_date)

        if months_to_update.count() == 0:

            balance_diff_reference = Month._scan_months_and_get_balance_diff_reference(start_of_month, user_id)

            if balance_diff_reference == None:
                print("Month reference not found")
                balance_diff = 0
            else:
                balance_diff = balance_diff_reference

            Month.create(user_id = user_id, date = start_of_month, balance_diff = balance_diff)


        