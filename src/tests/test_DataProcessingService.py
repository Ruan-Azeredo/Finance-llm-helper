import pytest
from services.DataProcessingService import processedData
from pTypes import Transaction

def test_data_processing_service_return_transaction_type():

    data = processedData({
        'id': '1',
        'date': '2022-01-01',
        'amount': 100,
        'memo': 'teste'
    })
    
    assert type(data) == Transaction

def test_data_processing_service_return_error_if_file_is_incomplete():

    with pytest.raises(Exception) as error:
        processedData({
            'id': '1',
            'amount': 100
        })
    
    assert str(error.value) == "Transação com dados incompletos"
