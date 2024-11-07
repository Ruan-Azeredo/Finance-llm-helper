from services import dataProcessingService
from pTypes import FileTransaction
from services import categorizeTransactionService
from useCases import generateReport
from controllers import user_router, auth_router

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/user")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {'message': 'Hello World'}

@app.post("/categorize-transaction")
async def categorize_transaction(file: UploadFile = File(...)) -> None:
    print('Recebido arquivo: ', file.filename, ' Iniciando processamento para definição da categoria...')

    try:
        data: dict = await dataProcessingService(file = file)
        transactions = data["processed_transaction_list"]
        raw_transactions = data["transactions_params_list"]

        categorized_transactions: list = []
        for i, transaction in enumerate(transactions):

            categoryzed_transaction = await categorizeTransactionService(transaction)

            categorized_transactions.append(generateReport(raw_transactions[i], categoryzed_transaction))

        return JSONResponse(content={
            "transactions": categorized_transactions, 
            "message": "Transações categorizadas com sucesso"
        })
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))