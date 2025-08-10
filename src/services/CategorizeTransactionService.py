from interface import llmInterface, callLLM
from useCases.CategorizeTransactionLogic import llmAnswerCheck, personalizedPrompt
#from utils import default_categories
from  models import Category

async def categorizeTransactionService(transaction_description: str, categories: list[str]) -> str:

    prompt = personalizedPrompt(transaction_description, categories)

    category = await llmInterface(prompt, llmAnswerCheck, callLLM, categories)

    return category