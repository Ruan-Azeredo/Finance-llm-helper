from src.pInterface import loadDataFromOfxFile, loadDir
from src.useCases import parsedData
from src.pTypes import Transaction

def dataProcessingService(path: str):

    if path is None:
        Exception("Nenhum caminho informado para a pasta de arquivos")

    processed_transaction_list = []

    files: list = loadDir(path)
    for file in files:
        data_from_ofx: list = loadDataFromOfxFile(path, file)
        for transaction in data_from_ofx:
            processed_transaction: Transaction = parsedData(transaction)
            processed_transaction_list.append(processed_transaction)

    return processed_transaction_list
