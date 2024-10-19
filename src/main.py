from services import dataProcessingService
from pTypes import Transaction
from services import categorizeTransactionService

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import os


app = FastAPI()

@app.get("/")
async def root():
    return {'message': 'Hello World'}

UPLOD_DIR = "imported-extratos"

@app.post("categorize-transaction")
async def categorize_transaction(file: UploadFile = File(...)):
    allowed_extensions = ['.ofx', '.csv']
    filename = file.filename
    file_extension = filename.split('.')[-1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Arquivo inválido, arquivo deve ser do formato .ofx ou .csv")

    file_path = os.path.join(UPLOD_DIR, filename)

    try:
        with open(file_path, "wb") as file:
            content = await file.read()
            file.write(content)
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {error}")

    return JSONResponse(content={
        "filename": filename, "message": "File uploaded successfully"
    })

""" transactions: list[Transaction] = dataProcessingService('../extratos-csv')

for transaction in transactions:

    categoryzed_transaction = categorizeTransactionService(transaction)

    print(transaction, '|', categoryzed_transaction) """