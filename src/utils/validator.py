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

def is_valid_date_format(date: str) -> bool:
    return bool(re.match(r'^\d{1,2}/\d{1,2}/\d{4}$', date))

def validate_transaction_input(transaction: dict):
    if 'direction' in transaction and transaction['direction'] != None and is_valid_direction_format(transaction['direction']) is False:
        raise Exception(f'Formato de direction está incorreto, direction deve ser "expense" ou "income". O direction recebido foi: {transaction["direction"]}')
    
    if 'amount' in transaction and transaction['amount'] != None and is_valid_amount_input_format(transaction['amount']) is False:
        raise Exception(f'Formato de amount está incorreto, o formato correto é "9999,99". O formato recebido foi: {transaction["amount"]}')
    
    if 'date' in transaction and transaction['date'] != None and is_valid_date_format(transaction['date']) is False:
        raise Exception(f'Formato de data inválido. Use dd/mm/aaaa. O formato recebido foi: {transaction["date"]}')
    
def is_valid_role_format(role: str) -> bool:
    return role in ['free', 'admin']

def validate_user_input(user: dict):
    if 'role' in user and user['role'] != None and is_valid_role_format(user['role']) is False:
        raise Exception(f'Formato de role está incorreto, role deve ser "free" ou "admin". O role recebido foi: {user["role"]}')

def is_valid_color_format(color: int) -> bool:
    # Caso mude a quantidade de cores disponiveis para as tags no front, mudar o range
    return color in range(0, 10)

def is_valid_tag_name(name: str) -> bool:
    if name == '':
        return False

def validate_tag_input(tag: dict):
    if 'color' in tag and tag['color'] != None and is_valid_color_format(tag['color']) is False:
        raise Exception(f'Formato de color está incorreto, color deve ser um número de 0 a 9. O color recebido foi: {tag["color"]}')

    if 'name' in tag and tag['name'] != None and is_valid_tag_name(tag['name']) is False:
        raise Exception(f'Formato de name está incorreto, name não pode ser vazio')