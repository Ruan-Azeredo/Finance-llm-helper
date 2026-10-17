from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

import os
import openai
from typing import Callable

async def llmInterface(
    prompt: str,
    llmAnswerCheck: Callable[[str], bool],
    callLLM: Callable[[str], str],
    user_categories: list[str] = None,
    limit: int = 5
) -> str:
    _  = load_dotenv(find_dotenv())

    answer = await callLLM(prompt)

    is_answer_checked = llmAnswerCheck(answer, user_categories)

    if is_answer_checked:
        return answer
    elif limit > 0:
        print('LLM try, limit: ', limit)
        return await llmInterface(prompt, llmAnswerCheck, callLLM, user_categories, limit - 1)
    else:
        raise Exception(f"Erro na interface com a LLM, muitas tentativas sem sucesso")
        

class LLMApiKeyError(Exception):
    pass

def isApiKeyError(error: Exception) -> bool:
    if isinstance(error, (openai.AuthenticationError, openai.PermissionDeniedError)):
        return True
    # Gemini responde 400 "API key expired" em vez de 401
    return isinstance(error, openai.BadRequestError) and 'api key' in str(error).lower()

# Gemini (grátis) primeiro; se falhar (cota esgotada, fora do ar), cai para o OpenRouter.
PROVIDERS = [
    ("https://generativelanguage.googleapis.com/v1beta/openai/", "GEMINI_API_KEY", "GEMINI_MODEL", "gemini-flash-lite-latest"),
    ("https://openrouter.ai/api/v1", "OPENROUTER_API_KEY", "OPENROUTER_MODEL", "nvidia/nemotron-3.5-lightning:free"),
]

async def callLLM(prompt: str) -> str:
    errors = []
    expired_keys = []
    for base_url, key_env, model_env, default_model in PROVIDERS:
        if not os.getenv(key_env):
            continue
        try:
            chat = ChatOpenAI(
                base_url=base_url,
                api_key=os.getenv(key_env),
                model=os.getenv(model_env, default_model),
                max_retries=1,
            )
            response = await chat.ainvoke(prompt)
            return response.content.strip()
        except Exception as error:
            print(f'LLM {base_url} falhou: {error}')
            errors.append(str(error))
            if isApiKeyError(error):
                expired_keys.append(key_env)
    if expired_keys:
        raise LLMApiKeyError(f"Chave de API da LLM expirada ou inválida: {', '.join(expired_keys)}. Atualize a chave no .env do servidor.")
    raise Exception(f"Erro ao comunicar-se com a LLM: {errors}")
