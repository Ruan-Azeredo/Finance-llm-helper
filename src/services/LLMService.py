from langchain_openai import ChatOpenAI
from  langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from useCases.PersonalizePrompt import personalizePrompt
from useCases import llmAnswerCheck
from utils import default_categories as categories

def llmService(prompt_content: str, limit: int = 5) -> str:
    _  = load_dotenv(find_dotenv())

    prompt = personalizePrompt(prompt_content, categories)

    try:
        chat = ChatGroq(model="llama-3.1-8b-instant")
        answer = chat.invoke(prompt).content

        is_answer_checked = llmAnswerCheck(categories, answer)
        if is_answer_checked:
            return answer
        elif limit > 0:
            llmService(prompt_content, limit - 1)
        else:
            return "Erro ao checkar resposta da LLM"
        

    except Exception as e:
        print(e)
        return "Erro ao comunicar-se com a LLM"