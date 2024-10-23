from interface import llmInterface, callLLM
from useCases.CategorizeTransactionLogic import llmAnswerCheck, personalizedPrompt
from utils import default_categories as categories

async def categorizeTransactionService(transaction_description: str) -> str:

    prompt = personalizedPrompt(transaction_description)

    category = await llmInterface(prompt, llmAnswerCheck, callLLM)

    return category