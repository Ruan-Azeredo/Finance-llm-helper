def category_validator(tags: list, category: str) -> bool:
    if category in tags:
        return True
    else:
        return False