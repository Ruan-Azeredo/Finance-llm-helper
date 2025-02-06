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
    
def is_valid_tags_format(tags: list) -> bool | str:
    # tags = [{'name': 'Alimentação', 'color': 0}, {'name': 'Receitas', 'color': 1}]

    print(tags)

    if tags is None:
        return False
    
    if len(tags) == 0:
        return 'empty'
    
    tag_names = []
    for tag in tags:

        if 'name' not in tag or 'color' not in tag:
            return False
        
        if type(tag['name']) is not str or type(tag['color']) is not int:
            return False
        
        if tag['name'] == '':
            return False
        
        if tag['name'] in tag_names:
            # should not have repeated tags
            return 'duplicate'

        tag_names.append(tag['name'])

    return True

def validate_user_input(user: dict):

    if 'tags' in user and user['tags'] != None and is_valid_tags_format(user['tags']) is not True:
        if is_valid_tags_format(user['tags']) == 'duplicate':
            raise Exception('Formato de tags está incorreto, tags não pode ter tags duplicadas.')
        elif is_valid_tags_format(user['tags']) == 'empty':
            raise Exception('Formato de tags está incorreto, tags não pode ser vazio.')
        
        raise Exception("Formato de tags está incorreto, tags devem ser do formato [{'name': 'str', 'color': int}]. "
                        f"O tags recebido foi: {user['tags']}")