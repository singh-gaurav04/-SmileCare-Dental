from fastapi import APIRouter
from src.llm.llm import get_llm
from src.llm.PROMPT import PROMPT
import json
import asyncio
import re
from src.schemas.chatSchema import ChatRequest, ChatResponse

chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


def parse_llm_json(content: str) -> dict:
    text = content.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    return json.loads(text)

@chat_router.post("/")
async def chat(request: ChatRequest):
    llm = get_llm()
    prompt = f"{PROMPT}\n\n## User Message\n\n{request.messages}"
    llm_response = await asyncio.to_thread(llm.invoke, prompt)
    parsed = parse_llm_json(llm_response.content)
    entities = parsed.get("entities", {})
    intent = parsed["intent"]
    response_text = parsed["response"]
    if intent == "book_appointment" and (
        entities.get("date") is None and entities.get("time") is None
    ):
        service = entities.get("service", "dental")
        response_text = (
            f"I'd be happy to help. Which date and time would you prefer "
            f"for your {service} appointment?"
        )
    
    return ChatResponse(
        intent=intent,
        entities=entities,
        response=response_text,
    )
