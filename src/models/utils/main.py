from typing import Callable, Any
from peewee import IntegrityError, DoesNotExist

def handle_database_error(method: Callable[..., Any]) -> Callable[..., Any] | None:
    def wrapper(*args, **kwargs):

        unique_fields = ['id', 'email']

        try:
            return method(*args, **kwargs)
        except IntegrityError as error:
            if 'UNIQUE constraint failed' in str(error):
                for field in unique_fields:
                    if field in str(error):
                        raise Exception(f"Chave duplicada: {field} já existente")
            elif 'NOT NULL constraint failed' in str(error):
                missing_field = str(error).split("NOT NULL constraint failed: ")[1]
                raise Exception(f"Erro: O campo obrigatório '{missing_field}' está ausente ou é nulo.")
            else:
                raise Exception(f"Erro interno de integridade: {error}")
        except DoesNotExist as error:
            raise Exception(f"Registro não encontrado: {error}")
        except Exception as error:
            raise Exception(f"Erro interno: {error}")
    return wrapper

def handle_values(kwargs):
    values = {}
    for key, value in kwargs.items():
        if value is not None:
            values[key] = value
    return values