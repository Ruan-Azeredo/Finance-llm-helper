from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

from models import Transaction, Month
from schemas import TransactionCRUDInput
from .utilsController import *
from utils import formatDateStrToTimestamp

transaction_router = APIRouter()

transaction_router_auth = APIRouter(
    dependencies = [Depends(verify_only_self_access_user)]
)
transaction_router_auth_by_transaction = APIRouter(
    dependencies = [Depends(verify_only_self_access_transaction)]
)
transaction_router_admin = APIRouter(
    dependencies = [Depends(verify_admin_access_user)]
)

@transaction_router_admin.get("/ops")
async def get_all_transactions():

    transactions: list[Transaction] = Transaction.all()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"transactions": [transaction.formatedTransactionToClient().to_dict() for transaction in transactions]}
    )

@transaction_router_auth.get("/from-user/{user_id}")
async def get_transactions_by_user_id(user_id: int, start_date: int = None, end_date: int = None):

    transactions: list[Transaction] = Transaction.get_transactions_by_user_id(user_id, start_date, end_date)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"transactions": [transaction.formatedTransactionToClient().to_dict() for transaction in transactions]}
    )

@transaction_router_auth.post("/ops/{user_id}")
async def create_transaction(user_id: int, transaction_input: TransactionCRUDInput):

    transaction: Transaction = Transaction.create(
        user_id = user_id,
        **transaction_input.to_dict()
    )

    print(transaction.formatedTransactionToClient().to_dict())

    Month.verify_and_create(transaction.date, user_id)

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Transação criada", "transaction": transaction.formatedTransactionToClient().to_dict()}
    )

@transaction_router_auth.post("/create-many-transactions/{user_id}")
async def create_many_transactions(user_id: int, transactions_input: list[TransactionCRUDInput]):

    month_already_have_transactions: list[str] = []
    for transaction_input in transactions_input:
        Transaction.create(
            user_id = user_id,
            **transaction_input.to_dict()
        )

        transaction_month_number = datetime.fromtimestamp(formatDateStrToTimestamp(transaction_input.date)).month
        transaction_month_year = datetime.fromtimestamp(formatDateStrToTimestamp(transaction_input.date)).year

        if (str(transaction_month_number) + '/' + str(transaction_month_year)) not in month_already_have_transactions:
            month_already_have_transactions.append(str(transaction_month_number) + '/' + str(transaction_month_year))
            Month.verify_and_create(formatDateStrToTimestamp(transaction_input.date), user_id)

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": "Transações criadas"}
    )

@transaction_router_auth_by_transaction.put("/ops/{transaction_id}")
async def update_transaction(transaction_id: str, transaction_input: TransactionCRUDInput):

    transaction: Transaction = Transaction.from_id(transaction_id)

    print('transaction in put: ', transaction)

    if not transaction:
        raise HTTPException(status_code = 404, detail = "Transação nao encontrada")
    
    transaction.update(
        **transaction_input.to_dict()
    )

    updated_transaction: Transaction = Transaction.from_id(transaction_id)

    if updated_transaction.date != transaction.date:
        Month.verify_and_create(updated_transaction.date, transaction.user_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Transação atualizada", "transaction": updated_transaction.formatedTransactionToClient().to_dict()}
    )

@transaction_router_auth_by_transaction.delete("/ops/{transaction_id}")
async def delete_transaction(*, transaction_id: str):

    transaction: Transaction = Transaction.from_id(transaction_id)

    print(transaction)

    if not transaction:
        raise HTTPException(status_code = 404, detail = "Transação nao encontrada")
    
    transaction.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {"message": "Transação deletada"}
    )

transaction_router.include_router(transaction_router_auth)
transaction_router.include_router(transaction_router_auth_by_transaction)
transaction_router.include_router(transaction_router_admin)