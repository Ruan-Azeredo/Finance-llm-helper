from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from peewee import DoesNotExist

from models import Month, User, Transaction 
from schemas import MonthCRUDInput, MonthsBalanceInput
from .utilsController import *
from utils import get_start_and_end_of_month_by_date

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

@month_router_auth.get("/from-user/{user_id}")
async def get_months_by_user_id(user_id: int):

    months: list[Month] = Month.get_months_by_user_id(user_id)

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

@month_router_auth.post("/months-balance")
async def get_months_with_transactions_sum_by_time(MonthsBalanceInput: MonthsBalanceInput, current_user: User = Depends(User.get_current_user)):

    months_balance = {}

    for month_timestamp in MonthsBalanceInput.timestamps:

        transactions_in_time_range: list[Transaction] = Transaction.get_by_timestamps_range(user_id = current_user.id, start_timestamp = month_timestamp, end_timestamp = get_start_and_end_of_month_by_date(month_timestamp)[1])

        transactions_in_month_sum = Transaction.sum_transactions_amount(transactions_in_time_range)

        try:
            month: Month = Month.get_month_by_timestamp_date_and_user(month_timestamp, current_user.id)
        except Exception:
            month = None

        if month is None:
            months_balance[month_timestamp] = transactions_in_month_sum
        else:
            months_balance[month_timestamp] = month.balance_diff + transactions_in_month_sum
    
    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"months_balance": months_balance}
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