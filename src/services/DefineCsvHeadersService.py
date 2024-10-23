from interface import llmInterface, callLLM
from useCases.DefineCsvHeadersLogic import llmAnswerCheck, personalizedPrompt
from utils import formatHaderKey

import json

async def defineCsvHeadersService(csv_data: str) -> str:

    prompt = personalizedPrompt(csv_data)

    headers_str = await llmInterface(prompt, llmAnswerCheck, callLLM)

    return formatHaderKey(json.loads(headers_str))