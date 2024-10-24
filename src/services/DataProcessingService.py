from interface import loadDataFromOfxFile, loadDataFromCsvFile, loadDir, openCsvFile
from useCases import parsedDataToTransaction, formatDescriptionTransaction
from services import defineCsvHeadersService
from pTypes import FileTransaction

from fastapi import File, UploadFile

def _handleUtilsData(data: FileTransaction) -> FileTransaction:
    return {
        "id": data["id"],
        "date": data["date"],
        "amount": data["amount"],
        "memo": data["memo"]
    }

async def dataProcessingService(file: UploadFile = File(...)):

    processed_transaction_list = []

    if file.filename.endswith('.ofx'):
        content = await file.read()
        data_from_file_raw: list[FileTransaction] = loadDataFromOfxFile(content)
        data_from_file = []
        for raw_transaction in data_from_file_raw:
            formated_transaction = _handleUtilsData(raw_transaction)
            data_from_file.append(formated_transaction)
    elif file.filename.endswith('.csv'):
        content = await file.read()
        headers = await defineCsvHeadersService(content)
        data_from_file: list[FileTransaction] = await loadDataFromCsvFile(content, headers)
    else:
        raise Exception("Formato de arquivo inválido, use .ofx ou .csv")
    
    for transaction in data_from_file:
        processed_transaction = formatDescriptionTransaction(transaction)
        processed_transaction_list.append(processed_transaction)

    return {
        "processed_transaction_list": processed_transaction_list,
        "transactions_params_list": data_from_file
    }
