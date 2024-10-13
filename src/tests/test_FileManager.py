import pytest
import inspect
from unittest.mock import mock_open, patch

from pTypes import FileTransaction
from interface import loadDataFromOfxFile, loadDataFromCsvFile, loadDir

def test_loadDir_returns_list_with_files():
    files = loadDir(path='tests/extratos')

    assert isinstance(files, list)

    for file in files:
        assert isinstance(file, str)
        assert file.endswith('.ofx')


def test_loadDir_when_no_files():

    with pytest.raises(Exception) as error:
        loadDir(path='/ext')

    assert str(error.value) == "Nenhum arquivo encontrado"


def test_loadDataFromOfxFile_returns_file_transactions_data():
    transactions_data = loadDataFromOfxFile(
        path='tests/extratos',
        file_name='Extrato-01-09-2024-a-01-10-2024 (1).ofx'
    )

    assert isinstance(transactions_data, list)

    # Get Props existents in FileTransaction
    allowed_keys = {
        param.name 
        for param in inspect.signature(FileTransaction.__init__).parameters.values()
        if param.name != 'self'
    }
    
    for transaction in transactions_data:

        # Just get Props existents in FileTransaction
        filtered_transaction = {key: value for key, value in transaction.items() if key in allowed_keys}

        transactionClass = FileTransaction(**filtered_transaction)
        assert isinstance(transactionClass, FileTransaction)


def test_loadDataFromOfxFile_when_file_is_not_ofx():

    with pytest.raises(Exception) as error:
        loadDataFromOfxFile(
            path='src/tests/extratos',
            file_name='Extrato.pdf'
        )

    assert str(error.value) == "Arquivo inválido, arquivo deve ser do formato .ofx"


def test_loadDataFromOfxFile_when_file_not_found():

    file_name = 'abacaxi.ofx'
    path = 'src/tests/extratos'

    with pytest.raises(Exception) as error:
        loadDataFromOfxFile(
            path=path,
            file_name=file_name
        )

    assert str(error.value) == f"Arquivo {file_name} não encontrado no caminho {path}"


def test_loadDataFromCsvFile_returns_file_transactions_data():
    mock_csv_data = "Data Lançamento;Valor;Histórico;Descrição\n01/01/2023;100,00;Payment;Salary\n02/01/2023;200,50;Refund;Product"
    
    with patch('builtins.open', mock_open(read_data=mock_csv_data)):
        
        transactions_data = loadDataFromCsvFile('extratos', 'extrato.csv')
        assert isinstance(transactions_data, list)

        # Get Props existents in FileTransaction
        allowed_keys = {
            param.name 
            for param in inspect.signature(FileTransaction.__init__).parameters.values()
            if param.name != 'self'
        }
        
        for transaction in transactions_data:

            # Just get Props existents in FileTransaction
            filtered_transaction = {key: value for key, value in transaction.items() if key in allowed_keys}

            transactionClass = FileTransaction(**filtered_transaction)
            assert isinstance(transactionClass, FileTransaction)


def test_loadDataFromCsvFile_when_file_is_not_csv():

    with pytest.raises(Exception) as error:
        loadDataFromCsvFile('extratos', 'extrato.pdf')

    assert str(error.value) == "Arquivo inválido, arquivo deve ser do formato .csv"


def test_loadDataFromCsvFile_when_file_not_found():

    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(Exception) as error:
            loadDataFromCsvFile('extratos', 'extrato.csv')

        assert str(error.value) == "Arquivo extrato.csv não encontrado no caminho extratos"


def test_loadDataFromCsvFile_when_data_is_empty():

    empty_csv_data = "Data Lançamento;Valor;Histórico;Descrição\n"
    
    with patch('builtins.open', mock_open(read_data=empty_csv_data)):
        with pytest.raises(Exception) as error:
            loadDataFromCsvFile('extratos', 'extrato.csv')

        assert str(error.value) == "O arquivo CSV parece estar vazio"