from src.services import dataProcessingService
from src.pTypes import Transaction
from src.services import llmService

transactions: list[Transaction] = dataProcessingService('extratos-csv')

for transaction in transactions:

    categoryzed_transaction = llmService(transaction)

    print(transaction, '|', categoryzed_transaction)