def category_validator(tags: list, category: str) -> bool:
    if category in tags and category is not None:
        return True
    else:
        return False