from datetime import datetime
import pytest
from io import BytesIO
from fastapi import UploadFile

from services import dataProcessingService
from interface import loadDataFromOfxFile, loadDir
from useCases import parsedDataToTransaction
from pTypes import Transaction, FileTransaction

@pytest.mark.asyncio
async def test_data_processing_service_function():
    with open('tests/extratos/Extrato-01-09-2024-a-01-10-2024 (1).ofx', 'rb') as file:
        file_bytes = file.read()
        upload_file = UploadFile(filename="Extrato-01-09-2024.ofx", file=BytesIO(file_bytes))

        processed_transaction_list, transactions_params_list = await dataProcessingService(file = upload_file)
        
        assert processed_transaction_list != None
        assert transactions_params_list != None

        assert isinstance(processed_transaction_list, list)
        assert isinstance(transactions_params_list, list)

        for transaction in processed_transaction_list:

            transaction_description = transaction.split(' | ')
            assert isinstance(datetime.strptime(transaction_description[0], '%d/%m/%Y'), datetime)
            assert isinstance(transaction_description[1], str)
            assert 'R$' in transaction_description[2]

@pytest.mark.asyncio
async def test_file_manager_to_data_parser_integration():
    processed_transaction_list = []

    files = loadDir(path='tests/extratos')

    for file in files:
        with open(f'tests/extratos/{file}', 'rb') as file:
            file_bytes = file.read()
            data_from_ofx = loadDataFromOfxFile(content = file_bytes)
            for transaction in data_from_ofx:
                processed_transaction = parsedDataToTransaction(transaction)
                processed_transaction_list.append(processed_transaction)

    assert processed_transaction_list != None
    assert isinstance(processed_transaction_list, list)

    for transaction in processed_transaction_list:
        assert isinstance(transaction, Transaction)

@pytest.mark.asyncio
async def test_data_processing_service_function_when_file_is_not_ofx_or_csv():

    invalid_file_content = "Arquivo de teste com formato inválido".encode('utf-8')
    upload_file = UploadFile(filename="extrato_invalido.txt", file=BytesIO(invalid_file_content))

    with pytest.raises(Exception) as error:
        await dataProcessingService(file = upload_file)

    assert str(error.value) == "Formato de arquivo inválido, use .ofx ou .csv"
