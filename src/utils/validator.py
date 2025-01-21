import re

def category_validator(tags: list, category: str) -> bool:
    if category in tags and category is not None:
        return True
    else:
        return False
    
def is_valid_amount_format(amount_string: str) -> bool:
    regex = r"^\d+,\d{2}$"
    return bool(re.match(regex, amount_string))

def is_valid_type_format(type_string: str) -> bool:
    return type_string in ['expense', 'income']