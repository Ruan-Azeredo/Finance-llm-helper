import pytest
import inspect

from pTypes import FileTransaction
from interface import loadDataFromOfxFile, loadDir

def test_loadDir_returns_list_with_files():
    files = loadDir(path='src/tests/extratos')

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
        path='src/tests/extratos',
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


def test_loadDataFromOfxFile_when_file_not_exit():

    file_name = 'abacaxi.ofx'
    path = 'src/tests/extratos'

    with pytest.raises(Exception) as error:
        loadDataFromOfxFile(
            path=path,
            file_name=file_name
        )

    assert str(error.value) == f"Arquivo {file_name} não encontrado no caminho {path}"