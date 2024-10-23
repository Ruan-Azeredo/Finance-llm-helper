import pytest

from interface import llmInterface
from useCases.DefineCsvHeadersLogic import llmAnswerCheck
from utils import default_categories as categories

@pytest.mark.asyncio
async def test_llmInterface_returns_valid_answer():

    def fakeLlmAnswerCheck(answer: str) -> bool:
        return True
    
    async def fakeCallLLM(prompt: str) -> str:
        return 'answer'

    answer = await llmInterface('prompt', fakeLlmAnswerCheck, fakeCallLLM)

    assert answer == 'answer'

@pytest.mark.asyncio
async def test_llmInterface_when_pass_recursion_limit():

    def fakellmAnswerCheck(answer: str):
        return False
    
    async def fakeCallLLM(prompt: str) -> str:
        return 'answer'

    with pytest.raises(Exception) as error:
        await llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = fakellmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 0
        )

    assert str(error.value) == 'Erro na interface com a LLM, muitas tentativas sem sucesso'

@pytest.mark.asyncio
async def test_llmInterface_recursion():

    def fakellmAnswerCheck(answer: str):
        return False
    

    call_count = 0
    async def fakeCallLLM(prompt: str) -> str:
        nonlocal call_count
        call_count += 1
        return 'answer'


    with pytest.raises(Exception) as error:
        await llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = fakellmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 5
        )

    assert str(error.value) == 'Erro na interface com a LLM, muitas tentativas sem sucesso'
    assert call_count == 6

@pytest.mark.asyncio
async def test_llmInterface_when_callLLM_raise_error():

    def fakellmAnswerCheck(answer: str):
        return True
    
    async def fakeCallLLM(prompt: str) -> str:
        raise Exception(f"Erro ao comunicar-se com a LLM:")

    with pytest.raises(Exception) as error:
        await llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = fakellmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 5
        )

    assert str(error.value) == 'Erro ao comunicar-se com a LLM:'

@pytest.mark.asyncio
async def test_llmInterface_when_receive_invalid_answer_from_callLLM():
    
    async def fakeCallLLM(prompt: str) -> str:
        return """
        ```python
            import csv
            import io

            csv_data = b" Extrato Conta Corrente \nConta ;55844227\nPer\xc3\xadodo ;24/05/2024 a 24/06/2024\n\nData Lan\xc3\xa7amento;Hist\xc3\xb3rico;Descri\xc3\xa7\xc3\xa3o;Valor;Saldo\n23/06/2024;Pix enviado ;Alipayaliexpress  Pix;-185,99\n22/06/2024;Pix recebido;Maria Vit\xc3\xb3ria Favero;21,00\n21/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Juros S/capital 4                  Bbas3;1,00\n21/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Dividendos 4                  Bbas3;0,65\n20/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Dividendos 3                  Petr4;2,54\n20/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Dividendos 3                  Petr4;1,65\n20/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Rendimento 3                  Petr4;0,07\n20/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Rendimento 3                  Petr4;0,10\n12/06/2024;Pagamento efetuado;Fatura cart\xc3\xa3o Inter;-178,80\n11/06/2024;Pix recebido;Nicolas Cremasco Campos Resende Do Carmo;14,35\n08/06/2024;Pix recebido;Maria Vit\xc3\xb3ria Favero;31,00\n05/06/2024;Pix recebido;Maria Vitoria Favero;8,00\n03/06/2024;Cr\xc3\xa9dito Evento B3;* Prov * Juros S/capital 1                  Itub4;0,01\n01/06/2024;Pix recebido;Maria Vit\xc3\xb3ria Favero;83,00\n30/05/2024;Pix recebido;Maria Vit\xc3\xb3ria Favero;8,00\n29/05/2024;Cr\xc3\xa9dito Evento B3;* Prov * Dividendos 3                  Vulc3;0,45\n28/05/2024;Pix recebido;Sara Azeredo Dos Santos Gomes;80,00\n26/05/2024;Pix enviado ;Augusto Cesar De Souza Costa;-25,00\n"

            reader = csv.reader(io.BytesIO(csv_data).readlines()[3:], delimiter=";")

            chaves = {
                "amount": [],
                "description": [],
                "date": []
            }

            for row in reader:
                chaves["amount"].append(row[4])
                chaves["description"].append(f"{row[1]} {row[2]}")
                chaves["date"].append(row[0])

            print({
                "amount": list(set(chaves["amount"])),
                "description": list(set(chaves["description"])),
                "date": list(set(chaves["date"]))
            })
            ```

            O código lê o arquivo CSV como uma lista de linhas, excluindo as primeiras linhas com cabeçalho. Em seguida, ele itera sobre as linhas restantes e atribui os valores da coluna "Valor" para a chave "amount", os valores da coluna "Histórico" e "Descrição" para a chave "description" e os valores da coluna "Data Lançamento" para a chave "date". O resultado é um dicionário com as chaves "amount", "description" e "date" e seus respectivos valores. Além disso, o código remove as linhas duplicadas de cada lista de valores, garantindo que cada valor seja único.

            O resultado do código é o seguinte dicionário:

            ```python
            {
                "amount": ["-185,99", "21,00", "1,00", "0,65", "2,54", "1,65", "0,07", "0,10", "-178,80", "14,35", "31,00", "8,00", "0,01", "83,00", "8,00", "0,45", "80,00", "-25,00"],
                "description": ["Pix enviado Alipayaliexpress Pix", "Pix recebido Maria Vitória Favero", "Crédito Evento B3 * Prov * Juros S/capital 4 Bbas3", "Crédito Evento B3 * Prov * Dividendos 4 Bbas3", "Crédito Evento B3 * Prov * Dividendos 3 Petr4", "Crédito Evento B3 * Prov * Dividendos 3 Petr4", "Crédito Evento B3 * Prov * Rendimento 3 Petr4", "Crédito Evento B3 * Prov * Rendimento 3 Petr4", "Pagamento efetuado Fatura cartão Inter", "Pix recebido Nicolas Cremasco Campos Resende Do Carmo", "Pix recebido Maria Vitória Favero", "Pix recebido Maria Vitoria Favero", "Crédito Evento B3 * Prov * Juros S/capital 1 Itub4", "Pix recebido Maria Vitória Favero", "Pix recebido Maria Vitória Favero", "Crédito Evento B3 * Prov * Dividendos 3 Vulc3", "Pix recebido Sara Azeredo Dos Santos Gomes", "Pix enviado Augusto Cesar De Souza Costa"],
                "date": ["23/06/2024", "22/06/2024", "21/06/2024", "21/06/2024", "20/06/2024", "20/06/2024", "20/06/2024", "20/06/2024", "12/06/2024", "11/06/2024", "08/06/2024", "05/06/2024", "03/06/2024", "01/06/2024", "30/05/2024", "29/05/2024", "28/05/2024", "26/05/2024"]
            }
            ```
        """

    with pytest.raises(Exception) as error:
        await llmInterface(
            prompt = 'prompt',
            llmAnswerCheck = llmAnswerCheck,
            callLLM = fakeCallLLM,
            limit = 5
        )

    assert str(error.value) == 'Erro na interface com a LLM, muitas tentativas sem sucesso'