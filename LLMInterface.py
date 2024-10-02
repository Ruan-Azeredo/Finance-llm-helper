from langchain_openai import ChatOpenAI
from  langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from utils.Validator import category_validator

categories = [
    "Alimentação", "Receitas", "Saúde", "Transporte", "Mercado", 
    "Educação", "Compras", "Investimento", "Transferencia para terceiros", 
    "Telefone", "Moradia"
]

def generate_prompt(text, categories):
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

def get_category(description: str, limit: int = 5) -> str:
    _  = load_dotenv(find_dotenv())

    prompt = generate_prompt(description, categories)

    try:
        chat = ChatGroq(model="llama-3.1-8b-instant")
        category = chat.invoke(prompt).content
        if category_validator(categories, category):
            return category
        elif limit > 0:
            get_category(description, limit - 1)
        else:
            return f"Categoria inválida ({category})"

    except Exception as e:
        print(e)
        return "Erro ao gerar categoria"