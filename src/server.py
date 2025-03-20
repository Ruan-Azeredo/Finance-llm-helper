from services import dataProcessingService
from pTypes import FileTransaction
from services import categorizeTransactionService
from useCases import generateReport
from controllers import user_router, auth_router, transaction_router, catTransact_router, category_router, month_router, category_router

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

        response = JSONResponse(
            status_code=500,
            content={"detail": str(error), "traceback": organized_traceback},
        )

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

app.include_router(user_router, prefix="/user")
app.include_router(transaction_router, prefix="/transaction")
app.include_router(auth_router, prefix="/auth")
app.include_router(catTransact_router, prefix="/categorize-transaction")
app.include_router(category_router, prefix="/category")
app.include_router(month_router, prefix="/month")


@app.get("/")
async def root():
    return {'message': 'Hello World'}