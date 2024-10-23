import pytest
import json

from useCases.DefineCsvHeadersLogic import personalizedPrompt, llmAnswerCheck
from interface import llmInterface
from utils import formatHaderKey

csv = """
Data Lançamento;Histórico;Descrição;Valor;Saldo
01/10/2024;Crédito Evento B3;* Prov * Dividendos 3                  Vulc3;0,37
01/10/2024;Crédito Evento B3;* Prov * Juros S/capital 3                  Itsa4;0,06
"""

def test_personalizePrompt_returns_string():
    template = personalizedPrompt(csv)
    assert isinstance(template, str)

def test_llmAnswerCheck_success():

    llm_answer_fake = """
    {
        "amount": ["Valor"],
        "description": ["Descrição", "Histórico"],
        "date": ["Data Lançamento"]
    }
    """

    answer = llmAnswerCheck(llm_answer_fake)

    assert answer == True

def test_llmAnswerCheck_failure():
    llm_answer_fake = """
    Para fazer seu codig, bla bla bla ....

    ```python
    {
        "amount": ["Valor"],
        "description": ["Descrição", "Histórico"],
        "date": ["Data Lançamento"]
    }
    ```
    """

    answer = llmAnswerCheck(llm_answer_fake)

    assert answer == False

@pytest.mark.asyncio
async def test_DefineCsvHeaders_integration():

    async def fakeCallLLM(prompt: str) -> str:
        llm_answer_fake = """
    {
        "amount": ["Valor"],
        "description": ["Descrição", "Histórico"],
        "date": ["Data Lançamento"]
    }
    """
        return llm_answer_fake

    prompt = personalizedPrompt(csv = csv)

    headers = await llmInterface(prompt, llmAnswerCheck, fakeCallLLM)

    expected_headers = {
        "amount": ["Valor"],
        "description": ["Descrição", "Histórico"],
        "date": ["Data Lançamento"]
    }

    assert formatHaderKey(json.loads(headers)) == expected_headers