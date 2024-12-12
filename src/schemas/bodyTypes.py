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

class LoginInput(BaseModel):
    email: str
    password: str
