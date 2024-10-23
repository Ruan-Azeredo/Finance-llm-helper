from services import dataProcessingService
from pTypes import Transaction
from services import categorizeTransactionService

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou especifique ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {'message': 'Hello World'}

UPLOAD_DIR = "imported-extratos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/categorize-transaction")
async def categorize_transaction(file: UploadFile = File(...)):

    data: dict = await dataProcessingService(file = file)
    transactions = data["processed_transaction_list"]
    raw_transactions = data["transactions_params_list"]

    categorized_transactions: list = []
    for i, transaction in enumerate(transactions):
        print('transaction: ', transaction)

        categoryzed_transaction = await categorizeTransactionService(transaction)

        categorized_transactions.append({"transaction": raw_transactions[i], "category": categoryzed_transaction})
        print(transaction, '|', categoryzed_transaction)
        raw_transactions[i]["date"] = raw_transactions[i]["date"].__str__()
        raw_transactions[i]["amount"] = raw_transactions[i]["amount"].__str__()
        print(type(raw_transactions[i]["date"]))

    return JSONResponse(content={
        "transactions": categorized_transactions, 
        "message": "File uploaded successfully"
    })