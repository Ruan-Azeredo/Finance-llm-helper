import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)

@pytest.mark.llm
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_categorize_transaction_e2e_csv():
    file_path = "tests/extratos-csv/Extrato-01-09-2024-a-01-10-2024 (1).csv"

    with open(file_path, 'rb') as file:
        response = client.post('/categorize-transaction', files={'file': file})

    assert response.status_code == 200
    assert response.json()['message'] == "Transações categorizadas com sucesso"
    assert len(response.json()['transactions']) > 0
    assert len(response.json()['transactions'][0]['category']) > 0
    assert len(response.json()['transactions'][0]['memo']) > 0
    assert len(response.json()['transactions'][0]['amount']) > 0
    assert len(response.json()['transactions'][0]['date']) > 0

@pytest.mark.llm
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_categorize_transaction_e2e_ofx():
    file_path = "tests/extratos/Extrato-01-09-2024-a-01-10-2024 (1).ofx"

    with open(file_path, 'rb') as file:
        response = client.post('/categorize-transaction', files={'file': file})

    assert response.status_code == 200
    assert response.json()['message'] == "Transações categorizadas com sucesso"
    assert len(response.json()['transactions']) > 0
    assert len(response.json()['transactions'][0]['category']) > 0
    assert len(response.json()['transactions'][0]['memo']) > 0
    assert len(response.json()['transactions'][0]['amount']) > 0
    assert len(response.json()['transactions'][0]['date']) > 0
    