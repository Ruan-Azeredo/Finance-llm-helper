from services import dataProcessingService
from pTypes import Transaction
from services import categorizeTransactionService

transactions: list[Transaction] = dataProcessingService('../extratos-csv')

for transaction in transactions:

    categoryzed_transaction = categorizeTransactionService(transaction)

    print(transaction, '|', categoryzed_transaction)