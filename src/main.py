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

UPLOAD_DIR = "imported-extratos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/categorizetransaction")
async def root(file: UploadFile = File(...)):
    try:
        allowed_extensions = ['ofx', 'csv']
        filename = file.filename
        file_extension = filename.split('.')[-1].lower()

        if file_extension not in allowed_extensions:
            print(file_extension)
            raise HTTPException(status_code=400, detail="Arquivo inválido, arquivo deve ser do formato .ofx ou .csv")

        file_path = os.path.join(UPLOAD_DIR, filename)

        try:
            content = await file.read()
            with open(file_path, "wb") as uploaded_file:
                uploaded_file.write(content)
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar o arquivo: {error}")

        return JSONResponse(content={
            "filename": filename, "message": "File uploaded successfully"
        })

    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {error}")

""" transactions: list[Transaction] = dataProcessingService('../extratos-csv')

for transaction in transactions:

    categoryzed_transaction = categorizeTransactionService(transaction)

    print(transaction, '|', categoryzed_transaction) """