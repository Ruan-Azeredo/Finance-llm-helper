from interface import llmInterface, callLLM
from useCases.DefineCsvHeadersLogic import llmAnswerCheck, personalizedPrompt
from utils import default_categories as categories

import json

def defineCsvHeadersService(csv_data: str) -> str:

    prompt = personalizedPrompt(csv_data)

    headers_str = llmInterface(prompt, llmAnswerCheck, callLLM)

    return json.loads(headers_str)