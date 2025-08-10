from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from peewee import DoesNotExist

from models import Month, User, Transaction 
from schemas import MonthCRUDInput, RequestBalancesInput
from .utilsController import *
from utils import get_start_and_end_of_month_by_date, get_start_and_end_of_year_by_date, formatTimestampToDateStr

month_router = APIRouter()

month_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])
month_router_auth_by_month = APIRouter(dependencies = [Depends(verify_only_self_access_month)])
month_router_admin = APIRouter(dependencies = [Depends(verify_admin_access_user)])

"""
According to the business rules, months will be created in accordance with transactions creation or update, and the user should not be able to delete manually his months. So the only operations that the user can do with his months is update in moment. The rest of code works, but is commented because it is not necessary in moment and this project had not tests for this routes.
"""



""" 
@month_router_admin.get("/ops")
async def get_months():

    months: list[Month] = Month.all()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"months": [month.formatedMonthToClient().to_dict() for month in months]}
    )

@month_router_auth.post("/ops/{user_id}")
async def create_month(user_id: int, month_input: MonthCRUDInput):

    month: Month = Month.create(
        user_id = user_id,
        **month_input.to_dict()
    )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Month criado", "month": month.formatedMonthToClient().to_dict()}
    ) 
"""

@month_router_auth.get("/from-user/{user_id}")
async def get_months_by_user_id(user_id: int):

    months: list[Month] = Month.get_months_by_user_id(user_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"months": [month.formatedMonthToClient().to_dict() for month in months]}
    )

@month_router_auth_by_month.put("/ops/{month_id}")
async def update_month(month_id: int, month_input: MonthCRUDInput):
    month: Month = Month.from_id(month_id)  

    if month is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Month nao encontrada"
        )
    
    month.update(
        **month_input.to_dict()
    )

    updated_month: Month = Month.from_id(month_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Month atualizado", "month": updated_month.formatedMonthToClient().to_dict()}
    )

@month_router_auth.post("/require-balances")
async def request_real_balances_by_time(request_balances_input: RequestBalancesInput, current_user: User = Depends(User.get_current_user)):
    balances = {}

    for balance_requested_timestamp in request_balances_input.timestamps:

        if request_balances_input.type == "years":

            year_end_timestamp = get_start_and_end_of_year_by_date(balance_requested_timestamp)[1] - 1

            try:
                """pega o ultimo mês até a data de referência, para calcular o saldo do mês
                se não existir, pega o ultimo mês do ano anterior e assim subsequentemente, o objetivo é pegar o saldo do mês até a data de referência, não a evolução do saldo do ano"""
                month_reference: Month = Month.get_last_month_until_date(year_end_timestamp, current_user.id)
            except Exception:
                """significa que nao existe nenhum mês até a data de referência"""
                month_reference = None

        else: 
            try:
                month_reference: Month = Month.get_month_by_timestamp_date_and_user(balance_requested_timestamp, current_user.id)
            except Exception:
                month_reference = None


        if month_reference is None:
            balances[balance_requested_timestamp] = {
                "income": 0,
                "expense": 0,
                "balance": 0
            }
        else:
            transactions_in_time_range: list[Transaction] = Transaction.get_by_timestamps_range(
                user_id = current_user.id,
                start_timestamp = month_reference.date,
                end_timestamp = get_start_and_end_of_month_by_date(month_reference.date)[1] - 1
            )

            # Filter to ensure only current user's transactions are included
            """ transactions_in_time_range = [
                t for t in transactions_in_time_range if t.user_id == current_user.id
            ] """

            print("Transactions in time range:", [t.to_dict() for t in transactions_in_time_range])

            transactions_in_month_sum_expense = Transaction.sum_transactions_expense_amount(transactions_in_time_range)
            transactions_in_month_sum_income = Transaction.sum_transactions_income_amount(transactions_in_time_range)
            transactions_in_month_sum = transactions_in_month_sum_income - transactions_in_month_sum_expense
            print("Sum expense:", transactions_in_month_sum_expense)

            balances[balance_requested_timestamp] = {
                "income": transactions_in_month_sum_income,
                "expense": transactions_in_month_sum_expense,
                "balance": month_reference.balance_diff + transactions_in_month_sum
            }
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = balances
    )

""" 
@month_router_auth_by_month.delete("/ops/{month_id}")
async def delete_month(month_id: int):
    month: Month = Month.from_id(month_id)

    if month is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Month nao encontrada"
        )
    
    month.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Month deletado"}
    )
"""

month_router.include_router(month_router_auth)
month_router.include_router(month_router_auth_by_month)
month_router.include_router(month_router_admin)