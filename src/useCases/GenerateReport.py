from pTypes import FileTransaction
from utils import formatDate, formatAmountToString, formatDirectionByAmount

def generateReport(raw_transaction: FileTransaction, category: str) -> dict:
    
    print(raw_transaction)
    report = {}

    report["id"] = raw_transaction["id"]
    report["date"] = formatDate(raw_transaction["date"])
    report["amount"] = formatAmountToString(raw_transaction["amount"])
    report["direction"] = formatDirectionByAmount(raw_transaction["amount"])
    report["memo"] = raw_transaction["memo"]
    report["category"] = category

    return report
