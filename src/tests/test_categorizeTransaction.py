from useCases.CategorizeTransactionLogic import personalizedPrompt, llmAnswerCheck
from utils import default_categories as categories
from interface import llmInterface

def test_personalizePrompt_returns_string():
    template = personalizedPrompt("Teste", ["Teste"])
    assert isinstance(template, str)


def test_llmAnswerCheck_success():

    categories = ["cat", "dog"]
    category = "dog"

    answer = llmAnswerCheck(category, categories)

    assert category == answer
    assert category in categories


def test_llmAnswerCheck_when_category_is_not_in_categories():

    categories = ["cat", "dog"]
    category = "fish"

    answer = llmAnswerCheck(category, categories)

    assert answer == False
    assert category not in categories

def test_CategoryTransaction_integration():

    def fakeCallLLM(prompt: str) -> str:
        return 'Investimento'

    prompt = personalizedPrompt('Crédito Evento B3 Prov Juros S/capital 1 Itub4', ['Investimento', 'Lazer'])

    category = llmInterface(prompt, llmAnswerCheck, fakeCallLLM)

    assert category == 'Investimento'