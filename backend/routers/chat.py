from fastapi import APIRouter
from ai_services.chat_service import generate_bot_reply
from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def send_message(payload: ChatMessage):
    bot_reply = generate_bot_reply(payload.message)
    return {"reply": bot_reply}
