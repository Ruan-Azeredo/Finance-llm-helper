from pTypes import Transaction, FileTransaction
from utils import formatDate, formatAmountToString

def parsedDataToTransaction(file_transaction: FileTransaction) -> Transaction:

    try:
        transaction = Transaction(
            id = file_transaction["id"],
            Data = file_transaction["date"],
            Valor = file_transaction["amount"],
            Descrição = file_transaction["memo"],
        )

    except:
        raise Exception(f"Transação com dados incompletos")

    return transaction

def formatDescriptionTransaction(file_transaction: FileTransaction) -> str:

    return formatDate(file_transaction["date"]) + ' | ' + file_transaction["memo"] + ' | R$ ' + formatAmountToString(file_transaction["amount"])