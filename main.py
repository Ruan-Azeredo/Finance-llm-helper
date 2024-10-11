from src.services import dataProcessingService

transactions = dataProcessingService('extratos')

for transaction in transactions:
    print(transaction)