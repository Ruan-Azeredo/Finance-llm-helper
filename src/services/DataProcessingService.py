from pTypes import Transaction, FileTransaction

def processedData(file_transaction: FileTransaction) -> Transaction:

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
        