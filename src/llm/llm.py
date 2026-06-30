from langchain_mistralai.chat_models import ChatMistralAI
import os
from dotenv import load_dotenv
from src.core.logger import get_logger

load_dotenv()

logger = get_logger(__name__)

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    max_tokens=1000,
    api_key=os.getenv("MISTRAL_API_KEY"),
)

if os.getenv("MISTRAL_API_KEY"):
    logger.info("Mistral LLM client initialized")
else:
    logger.warning("MISTRAL_API_KEY is not set")


def get_llm():
    return llm
