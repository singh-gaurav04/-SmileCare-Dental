from fastapi import APIRouter, HTTPException
from src.llm.llm import get_llm
from src.llm.PROMPT import PROMPT
import json
import asyncio
import re
from src.schemas.chatSchema import ChatRequest, ChatResponse
from src.core.logger import get_logger

logger = get_logger(__name__)

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
    logger.info("Chat request received: message=%r", request.messages)
    llm = get_llm()
    prompt = f"{PROMPT}\n\n## User Message\n\n{request.messages}"
    try:
        llm_response = await asyncio.to_thread(llm.invoke, prompt)
        parsed = parse_llm_json(llm_response.content)
    except json.JSONDecodeError as exc:
        logger.error("Failed to parse LLM response as JSON: %s", exc)
        raise HTTPException(status_code=502, detail="Invalid response from language model") from exc
    except Exception as exc:
        logger.exception("LLM invocation failed")
        raise HTTPException(status_code=502, detail="Language model request failed") from exc
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
        logger.info("Booking follow-up triggered for service=%r", service)
    logger.info("Chat response: intent=%r entities=%r", intent, entities)
    return ChatResponse(
        intent=intent,
        entities=entities,
        response=response_text,
    )
