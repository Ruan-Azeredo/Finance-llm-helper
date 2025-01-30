import re

def category_validator(tags: list, category: str) -> bool:
    if category in tags and category is not None:
        return True
    else:
        return False
    
def is_valid_amount_db_format(amount: float) -> bool:
    if amount < 0:
        return False
    return True

def is_valid_direction_format(direction_string: str) -> bool:
    return direction_string in ['expense', 'income']

def is_valid_amount_input_format(amount: str) -> bool:
    return bool(re.match(r'^\d{1,9},\d{2}$', amount))

def validate_transaction_input(transaction: dict):
    if 'direction' in transaction and is_valid_direction_format(transaction['direction']) is False:
            raise Exception(f'Formato de direction está incorreto, direction deve ser "expense" ou "income". O direction recebido foi: {transaction["direction"]}')
    
    if 'amount' in transaction and is_valid_amount_input_format(transaction['amount']) is False:
            raise Exception(f'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: {transaction["amount"]}')