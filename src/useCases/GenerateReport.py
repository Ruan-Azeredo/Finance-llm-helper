from pTypes import FileTransaction
from utils import formatDate, formatAmount

def generateReport(raw_transaction: FileTransaction, category: str) -> dict:
    
    report = {}

    report["id"] = raw_transaction["id"]
    report["date"] = formatDate(raw_transaction["date"])
    report["amount"] = formatAmount(raw_transaction["amount"])
    report["memo"] = raw_transaction["memo"]
    report["category"] = category

    return report
