from langchain_mistralai.chat_models import ChatMistralAI
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    max_tokens=1000,
    api_key=os.getenv("MISTRAL_API_KEY")
)
def get_llm():
    return llm