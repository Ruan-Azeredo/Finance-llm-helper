from src.services import dataProcessingService
from src.interface import loadDataFromOfxFile, loadDir
from src.useCases import parsedData
from src.pTypes import Transaction

def test_data_processing_service_function():
    processed_transaction_list = dataProcessingService('extratos')
    
    assert processed_transaction_list != None
    assert isinstance(processed_transaction_list, list)

    for transaction in processed_transaction_list:
        assert isinstance(transaction, Transaction)

def test_file_manager_to_data_parser_integration():
    processed_transaction_list = []

    files = loadDir(path='src/tests/extratos')

    for file in files:
        data_from_ofx= loadDataFromOfxFile(path='src/tests/extratos', file_name=file)
        for transaction in data_from_ofx:
            processed_transaction = parsedData(transaction)
            processed_transaction_list.append(processed_transaction)

    assert processed_transaction_list != None
    assert isinstance(processed_transaction_list, list)

    for transaction in processed_transaction_list:
        assert isinstance(transaction, Transaction)