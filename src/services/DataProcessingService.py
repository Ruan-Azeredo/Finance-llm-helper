from interface import loadDataFromOfxFile, loadDataFromCsvFile, loadDir, openCsvFile
from useCases import parsedDataToTransaction, formatDescriptionTransaction
from services import defineCsvHeadersService
from pTypes import FileTransaction

def dataProcessingService(path: str):

    if path is None:
        Exception("Nenhum caminho informado para a pasta de arquivos")

    processed_transaction_list = []

    files: list = loadDir(path)
    for file in files:
        if file.endswith('.ofx'):
            data_from_ofx: list[FileTransaction] = loadDataFromOfxFile(path, file)
        elif file.endswith('.csv'):
            file_data = openCsvFile(path, file)
            headers = defineCsvHeadersService(file_data)
            data_from_ofx: list[FileTransaction] = loadDataFromCsvFile(path, file, headers)
        else:
            raise Exception("Formato de arquivo inválido, use .ofx ou .csv")
        
        for transaction in data_from_ofx:
            processed_transaction = formatDescriptionTransaction(transaction)
            processed_transaction_list.append(processed_transaction)

    return processed_transaction_list
