from src.utils import category_validator


def llmAnswerCheck(categories: list[str], answer: str):
    if category_validator(categories, answer):
        return answer
    else:
        return False