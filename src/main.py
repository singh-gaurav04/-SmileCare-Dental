from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.logger import get_logger, setup_logging
from src.routes.chat_route import chat_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger.info("SmileCare Dental API starting")
    yield
    logger.info("SmileCare Dental API shutting down")


app = FastAPI(
    title="Smile-care Dental API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Dental API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

app.include_router(chat_router)
