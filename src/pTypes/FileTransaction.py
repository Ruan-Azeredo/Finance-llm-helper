from dataclasses import dataclass

@dataclass
class FileTransaction:
    id: str
    date: str
    amount: float
    memo: str