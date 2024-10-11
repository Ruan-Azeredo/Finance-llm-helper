from datetime import datetime

from src.services import dataProcessingService
from src.interface import loadDataFromOfxFile, loadDir
from src.useCases import parsedDataToTransaction
from src.pTypes import Transaction

def test_data_processing_service_function():
    processed_transaction_list = dataProcessingService('extratos')
    
    assert processed_transaction_list != None
    assert isinstance(processed_transaction_list, list)

    for transaction in processed_transaction_list:

        transaction_description = transaction.split(' | ')
        print(transaction_description)
        assert isinstance(datetime.strptime(transaction_description[0], '%d/%m/%Y'), datetime)
        assert isinstance(transaction_description[1], str)
        assert 'R$' in transaction_description[2]

def test_file_manager_to_data_parser_integration():
    processed_transaction_list = []

    files = loadDir(path='src/tests/extratos')

    for file in files:
        data_from_ofx= loadDataFromOfxFile(path='src/tests/extratos', file_name=file)
        for transaction in data_from_ofx:
            processed_transaction = parsedDataToTransaction(transaction)
            processed_transaction_list.append(processed_transaction)

    assert processed_transaction_list != None
    assert isinstance(processed_transaction_list, list)

    for transaction in processed_transaction_list:
        assert isinstance(transaction, Transaction)