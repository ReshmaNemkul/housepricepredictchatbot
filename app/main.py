from fastapi import FastAPI
from app.api.chatbot import router as chatbot_router

app = FastAPI()

app.include_router(chatbot_router, prefix="/chatbot", tags=["chatbot"])
