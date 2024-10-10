import pytest

from useCases import parsedData
from pTypes import Transaction

def test_data_parser_return_transaction_type():

    data = parsedData({
        'id': '1',
        'date': '2022-01-01',
        'amount': 100,
        'memo': 'teste'
    })
    
    assert type(data) == Transaction

def test_data_parser_return_error_if_file_is_incomplete():

    with pytest.raises(Exception) as error:
        parsedData({
            'id': '1',
            'amount': 100
        })
    
    assert str(error.value) == "Transação com dados incompletos"
