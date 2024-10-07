from utils.validator import category_validator
from utils.constants import default_categories as categories

class LLMAnswerCheck:
    def execute(self, answer: str):
        if category_validator(categories, answer):
            return answer
        else:
            return False