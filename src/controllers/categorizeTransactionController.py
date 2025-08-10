from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from services import dataProcessingService
from services import categorizeTransactionService
from useCases import generateReport
from .utilsController import *

catTransact_router = APIRouter()

catTransact_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])

@catTransact_router_auth.post("/by-file")
async def categorize_transactions_by_file(file: UploadFile = File(...), current_user: User = Depends(User.get_current_user)) -> None:
    print('Recebido arquivo: ', file.filename, ' Iniciando processamento para definição da categoria...')

    try:
        transactions, raw_transactions = await dataProcessingService(file = file)
        user_categories: list[Category] = Category.get_categories_by_user_id(current_user.id)

        categorized_transactions: list = []
        for i, transaction in enumerate(transactions):

            categoryzed_transaction = await categorizeTransactionService(transaction, [category.name for category in user_categories])

            categorized_transactions.append(generateReport(raw_transactions[i], categoryzed_transaction))

        return JSONResponse(content={
            "transactions": categorized_transactions, 
            "message": "Transações categorizadas com sucesso"
        })
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

catTransact_router.include_router(catTransact_router_auth)