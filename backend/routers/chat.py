from fastapi import APIRouter
from ai_services.chat_service import generate_bot_reply

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message")
async def send_message(payload: dict):
    user_message = payload.get("message", "")
    bot_reply = generate_bot_reply(user_message)
    return {"reply": bot_reply}
