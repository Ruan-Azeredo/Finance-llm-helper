from services import dataProcessingService
from pTypes import Transaction
from services import llmService

transactions: list[Transaction] = dataProcessingService('../extratos-csv')

for transaction in transactions:

    categoryzed_transaction = llmService(transaction)

    print(transaction, '|', categoryzed_transaction)