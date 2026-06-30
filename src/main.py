from fastapi import FastAPI
from src.routes.chat_route import chat_router
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app = FastAPI(
    title = "Smile-care Dental API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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
