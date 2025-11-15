from fastapi import APIRouter, UploadFile, File
from ai_services.scan_service import analyze_plant_image
from ai_services.chat_service import generate_bot_reply

router = APIRouter(prefix="/scan", tags=["scan"])

@router.post("/analyze")
async def scan_plant(file: UploadFile = File(...)):
    file_bytes = await file.read()
    label, confidence, box = analyze_plant_image(file_bytes)

    if label is None:
        return {"status": "error", "result": "Не удалось обнаружить растение на фото"}

    healthy_labels = ["healthy", "здоровое", "normal"]
    if label.lower() in healthy_labels:
        return {
            "status": "ok",
            "result": "Растение здоровое 🌱",
            "confidence": confidence,
            "label": label
        }

    # Передаём болезнь в чат для рекомендаций
    treatment_advice = generate_bot_reply(crop=None, disease=label)

    return {
        "status": "ok",
        "result": f"Обнаружена болезнь: {label}",
        "confidence": confidence,
        "label": label,
        "treatment_advice": treatment_advice
    }
