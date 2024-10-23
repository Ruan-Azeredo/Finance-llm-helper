from interface import loadDataFromOfxFile, loadDataFromCsvFile, loadDir, openCsvFile
from useCases import parsedDataToTransaction, formatDescriptionTransaction
from services import defineCsvHeadersService
from pTypes import FileTransaction

from fastapi import File, UploadFile

async def dataProcessingService(file: UploadFile = File(...)):

    processed_transaction_list = []

    if file.filename.endswith('.ofx'):
        content = await file.read()
        print('content: ',content)
        data_from_ofx: list[FileTransaction] = loadDataFromOfxFile(content)
    elif file.filename.endswith('.csv'):
        content = await file.read()
        print('content: ',content)
        headers = await defineCsvHeadersService(content)
        data_from_ofx: list[FileTransaction] = await loadDataFromCsvFile(content, headers)
    else:
        raise Exception("Formato de arquivo inválido, use .ofx ou .csv")
    
    for transaction in data_from_ofx:
        processed_transaction = formatDescriptionTransaction(transaction)
        processed_transaction_list.append(processed_transaction)

    return {
        "processed_transaction_list": processed_transaction_list,
        "transactions_params_list": data_from_ofx
    }
