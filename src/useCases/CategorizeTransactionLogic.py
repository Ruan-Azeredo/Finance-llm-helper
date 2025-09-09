from utils import category_validator, default_categories

def llmAnswerCheck(answer: str, categories: str = default_categories):
    if category_validator(categories, answer):
        return True
    else:
        return False
    
    
def personalizedPrompt(text: str, categories: str = default_categories) -> str:
    template = f"""
    Você é um analista de dados, trabalhando em um projeto de dados.
    Seu trabalho é escolher uma categoria adequada para cada transação financeira que vou lhe enviar.
    Todas são transações financeiras de uma pessoa física.

    Escolha uma dentre as seguintes categorias:
    {', '.join(categories)}

    Escolha a categoria deste item:
    {text}

    Responda apenas com a categoria.
    """
    return template