from peewee import DateTimeField, ForeignKeyField, DoesNotExist, FloatField, IntegerField, AutoField
from datetime import datetime

from .BaseModel import BaseModel
from models import User
from database import db
from .handles import handle_values, handle_database_error
from utils import validate_month_input

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
        values = handle_values(kwargs)
        super(Month, self).update(**values)

    @handle_database_error
    def get_months_by_user_id(user_id: int) -> list['Month']:
        
        try:
            User.get_by_id(user_id)
        except  Exception:
            raise DoesNotExist(f"Usuario com id {user_id} nao encontrado")
        
        return Month.select().where(Month.user_id == user_id)
    
    # ------------------------------------------------------------------------------------------------------------

    def find_months_to_update_by_date(transaction_date: int, user_id) -> int:
        transaction_month_number = datetime.fromtimestamp(transaction_date).month # month is 1-12
        transaction_month_year = datetime.fromtimestamp(transaction_date).year # year is 2023, 2024, etc.

        print(transaction_month_number, '/', transaction_month_year)

        start_of_month = datetime(transaction_month_year, transaction_month_number, 1).timestamp()

        if transaction_month_number == 12:
            start_of_next_month = datetime(transaction_month_year + 1, 1, 1).timestamp()
        else:
            start_of_next_month = datetime(transaction_month_year, transaction_month_number + 1, 1).timestamp()

        print("Start of month:", start_of_month)
        print("Start of next month:", start_of_next_month)

        months_to_update = Month.select().where(Month.user_id == user_id).where(Month.date >= start_of_month, Month.date < start_of_next_month)

        return months_to_update
    
    def scan_months_and_get_reference(month_date: int, user_id: int) -> 'Month':
        # closest next month
        closest_month = Month.select().where(Month.user_id == user_id, Month.date > month_date).order_by(Month.date.asc()).first()
        if not closest_month:
            # closest previous month
            closest_month = Month.select().where(Month.user_id == user_id, Month.date < month_date).order_by(Month.date.desc()).first()

        return closest_month
    
    @handle_database_error
    def adjust_balance(transactions_amount: float, transaction_date: int, user_id: int) -> None:
        
        months_to_update = Month.find_months_to_update_by_date(transaction_date, user_id)

        #repeated code
        transaction_month_number = datetime.fromtimestamp(transaction_date).month # month is 1-12
        transaction_month_year = datetime.fromtimestamp(transaction_date).year # year is 2023, 2024, etc.
        start_of_month = datetime(transaction_month_year, transaction_month_number, 1).timestamp()

        if months_to_update.count() == 0:

            month_reference = Month.scan_months_and_get_reference(start_of_month, user_id)

            if month_reference == None:
                print("Month reference not found")
                balance_diff = 0
            else:
                balance_diff = month_reference.balance_diff

            Month.create(user_id = user_id, date = start_of_month, balance_diff = balance_diff)

        print(abs(-100))


        