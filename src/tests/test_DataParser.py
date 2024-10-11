import pytest

from src.useCases import parsedDataToTransaction, formatDescriptionTransaction
from src.pTypes import Transaction

def test_data_parser_return_transaction_type():

    data = parsedDataToTransaction({
        'id': '1',
        'date': '01-01-2022',
        'amount': 100,
        'memo': 'teste'
    })
    
    assert type(data) == Transaction

def test_data_parser_return_error_if_file_is_incomplete():

    with pytest.raises(Exception) as error:
        parsedDataToTransaction({
            'id': '1',
            'amount': 100
        })
    
    assert str(error.value) == "Transação com dados incompletos"

def test_formatDescritptionTransaction():
    formated_data = formatDescriptionTransaction({
        'id': '1',
        'date': '01-01-2022',
        'amount': 100,
        'memo': 'teste'
    })

    assert formated_data == '01/01/2022 | teste | R$ 100,00'

def test_formatDate_when_date_is_none():

    formated_data = formatDescriptionTransaction({
        'id': '1',
        'date': None,
        'amount': 100,
        'memo': 'teste'
    })

    assert formated_data == ' | teste | R$ 100,00'