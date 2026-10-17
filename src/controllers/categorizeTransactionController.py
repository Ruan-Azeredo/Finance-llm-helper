import asyncio
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse

from services import dataProcessingService
from services import categorizeTransactionService
from useCases import generateReport
from interface import LLMApiKeyError
from .utilsController import *

catTransact_router = APIRouter()

catTransact_router_auth = APIRouter(dependencies = [Depends(verify_only_self_access_user)])

@catTransact_router_auth.post("/by-file")
async def categorize_transactions_by_file(file: UploadFile = File(...), current_user: User = Depends(User.get_current_user)) -> None:
    print('Recebido arquivo: ', file.filename, ' Iniciando processamento para definição da categoria...')

    try:
        transactions, raw_transactions = await dataProcessingService(file = file)
        user_categories: list[Category] = Category.get_categories_by_user_id(current_user.id)
        category_names = [category.name for category in user_categories]

        semaphore = asyncio.Semaphore(10)

        async def categorize_single(transaction, raw_transaction):
            async with semaphore:
                categoryzed_transaction = await categorizeTransactionService(transaction, category_names)
                return generateReport(raw_transaction, categoryzed_transaction)

        categorized_transactions = await asyncio.gather(
            *(categorize_single(t, raw_t) for t, raw_t in zip(transactions, raw_transactions))
        )

        return JSONResponse(content={
            "transactions": categorized_transactions, 
            "message": "Transações categorizadas com sucesso"
        })
    
    except LLMApiKeyError as error:
        raise HTTPException(status_code=503, detail=str(error))
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

catTransact_router.include_router(catTransact_router_auth)