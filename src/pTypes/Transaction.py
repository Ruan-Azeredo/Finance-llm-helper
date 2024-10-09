from dataclasses import dataclass

@dataclass
class Transaction:
    id: str
    Data: str
    Valor: float
    Descrição: str