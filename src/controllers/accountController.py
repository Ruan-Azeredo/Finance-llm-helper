from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from models import Account
from schemas import AccountCRUDInput
from .utilsController import *

account_router = APIRouter()

account_router_auth = APIRouter(dependencies=[Depends(verify_only_self_access_user)])
account_router_auth_by_account = APIRouter(dependencies = [Depends(verify_only_self_access_account)])
account_router_admin = APIRouter(dependencies = [Depends(verify_admin_access_user)])

@account_router_admin.get("/ops")
async def get_accounts():

    accounts: list[Account] = Account.all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "accounts": [account.formatedAccountToClient().to_dict() for account in accounts]
        }
    )

@account_router_auth.get("/from-user/{user_id}")
async def get_accounts_from_user(user_id: int):

    accounts: list[Account] = Account.get_accounts_by_user_id(user_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "accounts": [account.formatedAccountToClient().to_dict() for account in accounts]
        }
    )

@account_router_auth.post("/ops/{user_id}")
async def create_account(user_id: int, account_input: AccountCRUDInput):

    account: Account = Account.create(
        user_id = user_id,
        **account_input.to_dict()
    )

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {
            "message": "Conta criada", "account": account.formatedAccountToClient().to_dict()
        }
    )

@account_router_auth_by_account.put("/ops/{account_id}")
async def update_account(account_id: int, account_input: AccountCRUDInput):

    account: Account = Account.from_id(account_id)

    print("account in update:", account, account_id)

    if not account:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Conta não encontrada"
        )

    account.update(
        **account_input.to_dict()
    )

    update_account: Account = Account.from_id(account_id)

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "message": "Conta atualizada", "account": update_account.formatedAccountToClient().to_dict()
        }
    )

@account_router_auth_by_account.delete("/ops/{account_id}")
async def delete_account(account_id: int):

    account: Account = Account.from_id(account_id)

    if not account:
        raise HTTPException(
            status_code = 404,
            detail = "Conta não encontrada"
        )

    account.delete()

    return JSONResponse(
        status_code = status.HTTP_200_OK,
        content = {
            "message": "Conta deletada"
        }
    )

account_router.include_router(account_router_auth)
account_router.include_router(account_router_auth_by_account)
account_router.include_router(account_router_admin)