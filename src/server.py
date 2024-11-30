from services import dataProcessingService
from pTypes import FileTransaction
from services import categorizeTransactionService
from useCases import generateReport
from controllers import user_router, auth_router

import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import traceback

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except HTTPException as http_error:
        return JSONResponse(
            status_code=http_error.status_code,
            content={"detail": http_error.detail},
        )
    except Exception as error:

        tb_lines = traceback.format_exception(type(error), error, error.__traceback__)
        organized_traceback = "".join(tb_lines)

        return JSONResponse(
            status_code=500,
            content={
                "detail": str(error),
                "traceback": organized_traceback
            },
        )

app.include_router(user_router, prefix="/user")
app.include_router(auth_router, prefix="/auth")

@app.get("/")
async def root():
    return {'message': 'Hello World'}

@app.post("/categorize-transactions-by-file")
async def categorize_transactions_by_file(file: UploadFile = File(...)) -> None:
    print('Recebido arquivo: ', file.filename, ' Iniciando processamento para definição da categoria...')

    try:
        transactions, raw_transactions = await dataProcessingService(file = file)

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