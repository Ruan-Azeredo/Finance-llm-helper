import pytest

from interface import llmInterface

def test_llmInterface_returns_valid_answer():

    def fakeLlmAnswerCheck(answer: str) -> bool:
        return True
    
    def fakeCallLLM(prompt: str) -> str:
        return 'answer'

    answer = llmInterface('prompt', fakeLlmAnswerCheck, fakeCallLLM)

    assert answer == 'answer'

def test_llmInterface_when_pass_recursion_limit():

    def fakellmAnswerCheck(answer: str):
        return False
    
    def fakeCallLLM(prompt: str) -> str:
        return 'answer'

    with pytest.raises(Exception) as error:
        llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = fakellmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 0
        )

    assert str(error.value) == 'Erro na interface com a LLM, muitas tentativas sem sucesso'

def test_llmInterface_recursion():

    def fakellmAnswerCheck(answer: str):
        return False
    

    call_count = 0
    def fakeCallLLM(prompt: str) -> str:
        nonlocal call_count
        call_count += 1
        return 'answer'


    with pytest.raises(Exception) as error:
        llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = fakellmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 5
        )

    assert str(error.value) == 'Erro na interface com a LLM, muitas tentativas sem sucesso'
    assert call_count == 6

def test_llmInterface_when_callLLM_raise_error():

    def fakellmAnswerCheck(answer: str):
        return True
    
    def fakeCallLLM(prompt: str) -> str:
        raise Exception(f"Erro ao comunicar-se com a LLM:")

    with pytest.raises(Exception) as error:
        llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = fakellmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 5
        )

    assert str(error.value) == 'Erro ao comunicar-se com a LLM:'