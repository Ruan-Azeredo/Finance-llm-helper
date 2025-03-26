from peewee import DateTimeField, ForeignKeyField, DoesNotExist, FloatField, IntegerField, AutoField
from datetime import datetime
from copy import deepcopy

from .BaseModel import BaseModel
from models import User
from database import db
from .handles import handle_values, handle_database_error
from utils import validate_month_input, formatAmountToFloat, formatAmountToString, formatTimestampToDateStr

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
        formatedMonth.balance_diff = formatAmountToString(formatedMonth.balance_diff)

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
    def get_months_by_user_id(user_id: int) -> list['Month']:
        
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")
        
        return Month.select().where(Month.user_id == user_id)
    
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

    def _get_start_and_end_of_month_by_date(date: int) -> tuple[int, int]:

        transaction_month_number = datetime.fromtimestamp(date).month # month is 1-12
        transaction_month_year = datetime.fromtimestamp(date).year # year is 2023, 2024, etc.

        start_of_month = datetime(transaction_month_year, transaction_month_number, 1).timestamp()

        if transaction_month_number == 12:
            start_of_next_month = datetime(transaction_month_year + 1, 1, 1).timestamp()
        else:
            start_of_next_month = datetime(transaction_month_year, transaction_month_number + 1, 1).timestamp()

        return start_of_month, start_of_next_month

    def _find_months_to_update_by_date(transaction_date: int, user_id) -> int:
       
        start_of_month, start_of_next_month = Month._get_start_and_end_of_month_by_date(transaction_date)

        months_to_update = Month.select().where(Month.user_id == user_id).where(Month.date >= start_of_month, Month.date < start_of_next_month)

        return months_to_update
    
    def _scan_months_and_get_reference(month_date: int, user_id: int) -> 'Month':

        # closest next month
        closest_month = Month.select().where(Month.user_id == user_id, Month.date > month_date).order_by(Month.date.asc()).first()
        if not closest_month:
            # closest previous month
            closest_month = Month.select().where(Month.user_id == user_id, Month.date < month_date).order_by(Month.date.desc()).first()

        return closest_month
    
    @handle_database_error
    def verify_and_create(transaction_date: int, user_id: int) -> None:
        
        months_to_update = Month._find_months_to_update_by_date(transaction_date, user_id)

        start_of_month, _ = Month._get_start_and_end_of_month_by_date(transaction_date)

        if months_to_update.count() == 0:

            month_reference = Month._scan_months_and_get_reference(start_of_month, user_id)

            if month_reference == None:
                print("Month reference not found")
                balance_diff = 0
            else:
                balance_diff = month_reference.balance_diff

            Month.create(user_id = user_id, date = start_of_month, balance_diff = balance_diff)


        