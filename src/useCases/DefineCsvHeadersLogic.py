from utils import category_validator, formatHaderKey
import json

def llmAnswerCheck(answer: dict):
    answer_json = json.loads(answer)
    answer_json_formated = formatHaderKey(answer_json)
    if type(answer_json_formated['amount']) == list and type(answer_json_formated['description']) == list and type(answer_json_formated['date']) == list:
        return answer_json_formated
    else:
        return False
    
    
def personalizedPrompt(csv: str) -> str:
    template = f"""
    Você é um profissional de analise de dados, trabalhando em um projeto de dados.
    Seu trabalho é ler um arquivo csv e definir as chaves de cada coluna.
    Você deve retornar um dicionario com as seguintes chaves: amout, description, date.
    Que indiquem os campos deste csv que contenham as respectivas informações.
    No campo description quero que adicione o maximo de informações possíveis, já que será utilizado para ajudar a catalogar a transação.
    Ids não são necessarios.

    exemplo:

    {{
        "amount": ["Valor"]
        "description": ["Descrição", "Histórico"]
        "date": ["Data Lançamento"]
    }}


    csv:

    {csv}

    Responda apenas com o dicionario.

    """

    return template