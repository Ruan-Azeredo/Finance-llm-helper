from langchain_openai import ChatOpenAI
from  langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

from typing import Callable

async def llmInterface(
    prompt: str,
    llmAnswerCheck: Callable[[str], bool],
    callLLM: Callable[[str], str],
    limit: int = 5
) -> str:
    _  = load_dotenv(find_dotenv())

    answer = await callLLM(prompt)

    answer_checked = llmAnswerCheck(answer)

    if answer_checked:
        return answer
    elif limit > 0:
        print('LLM try, limit: ', limit)
        await llmInterface(prompt, llmAnswerCheck, callLLM, limit - 1)
    else:
        raise Exception(f"Erro na interface com a LLM, muitas tentativas sem sucesso")
        

async def callLLM(prompt: str) -> str:
    try:
        chat = ChatGroq(model="llama-3.1-8b-instant")
        answer = chat.invoke(prompt).content
        return answer
    except Exception as error:
        raise Exception(f"Erro ao comunicar-se com a LLM: {error}")
