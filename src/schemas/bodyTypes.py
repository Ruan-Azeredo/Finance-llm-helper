from pydantic import BaseModel
from typing import Optional

class UserCRUDInput(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None

    def to_dict(obj) -> dict:
        """
        Converte um objeto em dicionário, verificando se ele é uma instância de Pydantic ou uma classe genérica.
        """
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):  # Verifica se tem o método `dict()`
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):  # Classes Python normais
            return vars(obj)
        else:
            raise ValueError("O objeto não pode ser convertido em um dicionário.")
        
class TransactionCRUDInput(BaseModel):
    memo: Optional[str] = None
    amount: Optional[str] = None
    date: Optional[str] = None
    category: Optional[str] = None
    direction: Optional[str] = None

    def to_dict(obj) -> dict:
        """
        Converte um objeto em dicionário, verificando se ele é uma instância de Pydantic ou uma classe genérica.
        """
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):  # Verifica se tem o método `dict()`
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):  # Classes Python normais
            return vars(obj)
        else:
            raise ValueError("O objeto não pode ser convertido em um dicionário.")

class CategoryCRUDInput(BaseModel):
    name: Optional[str] = None
    color: Optional[int] = None

    def to_dict(obj) -> dict:
        """
        Converte um objeto em dicionário, verificando se ele é uma instância de Pydantic ou uma classe genérica.
        """
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):  # Verifica se tem o método `dict()`
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):  # Classes Python normais
            return vars(obj)
        else:
            raise ValueError("O objeto não pode ser convertido em um dicionário.")

class LoginInput(BaseModel):
    email: str
    password: str

class MonthCRUDInput(BaseModel):
    date: Optional[str] = None
    balance_diff: Optional[str] = None
    income: Optional[float] = None
    expense: Optional[float] = None

    def to_dict(obj) -> dict:
        """
        Converte um objeto em dicionário, verificando se ele é uma instância de Pydantic ou uma classe genérica.
        """
        if hasattr(obj, 'dict') and callable(getattr(obj, 'dict')):  # Verifica se tem o método `dict()`
            return obj.model_dump()
        elif hasattr(obj, '__dict__'):  # Classes Python normais
            return vars(obj)
        else:
            raise ValueError("O objeto não pode ser convertido em um dicionário.")