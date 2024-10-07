from langchain_openai import ChatOpenAI
from  langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from useCases.PersonalizePrompt import PersonalizePrompt
from utils.validator import category_validator
from useCases.LLMAnswerCheck import LLMAnswerCheck

class LLMService:

    def execute(self, prompt_content: str, limit: int = 5) -> str:
        _  = load_dotenv(find_dotenv())

        prompt = PersonalizePrompt().execute(prompt_content)

        try:
            chat = ChatGroq(model="llama-3.1-8b-instant")
            answer = chat.invoke(prompt).content

            is_answer_checked = LLMAnswerCheck().execute(answer)
            if is_answer_checked:
                return answer
            elif limit > 0:
                self.execute(prompt_content, limit - 1)
            else:
                return "Erro ao checkar resposta da LLM"
            

        except Exception as e:
            print(e)
            return "Erro ao comunicar-se com a LLM"