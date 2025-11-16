from fastapi import APIRouter, UploadFile, File
from ai_services.scan_service import analyze_plant_image
from ai_services.chat_service import generate_bot_reply
import json # Import json to load DATA for parse_yolo_label
from typing import Tuple # Import Tuple

router = APIRouter(prefix="/scan", tags=["scan"])

# Load your knowledge base for the parsing function (do this once)
with open("knowledge_base.json", "r") as f:
    CHAT_DATA_FOR_PARSING = json.load(f)

def parse_yolo_label(yolo_label: str) -> Tuple[str, str]:
    """
    Parses a YOLO output label string into a (crop, disease) tuple
    that matches the structure of the knowledge_base.json.
    This function is copied/adapted from our previous discussion to be used here.
    """
    yolo_label_lower = yolo_label.lower()

    for item in CHAT_DATA_FOR_PARSING: # Use the loaded data here
        kb_crop_lower = item['crop'].lower()
        kb_disease_lower = item['disease'].lower()

        if yolo_label_lower == kb_disease_lower:
            return item['crop'], item['disease']

        if yolo_label_lower.startswith(kb_crop_lower) and kb_disease_lower == yolo_label_lower:
            return item['crop'], item['disease']

        # Specific known mismatches
        if yolo_label_lower.startswith("cherry") and "cherry (including sour)" == kb_crop_lower and yolo_label_lower.endswith(kb_disease_lower.replace(kb_crop_lower, "").strip()):
            return "Cherry (including sour)", item['disease']

        if yolo_label_lower.startswith("corn") and "corn (maize)" == kb_crop_lower and yolo_label_lower.endswith(kb_disease_lower.replace(kb_crop_lower, "").strip()):
            return "Corn (maize)", item['disease']

        if yolo_label_lower.startswith("bell_pepper"):
            if yolo_label_lower == "bell_pepper leaf":
                return "Pepper, bell", "Bell_pepper leaf"
            if yolo_label_lower == "bell_pepper leaf spot":
                return "Pepper, bell", "Bell_pepper leaf spot"

        if yolo_label_lower.startswith("soyabean") and "soybean" == kb_crop_lower and yolo_label_lower.endswith(kb_disease_lower.replace(kb_crop_lower, "").strip()):
            return "Soybean", item['disease']

    # Fallback
    print(f"Warning: No perfect match found for YOLO label: '{yolo_label}'. Attempting generic split.")
    parts = yolo_label.split(' ')
    if len(parts) > 1:
        fallback_crop = parts[0]
        fallback_disease = ' '.join(parts[1:])
    else:
        fallback_crop = "Unknown"
        fallback_disease = yolo_label

    return fallback_crop, fallback_disease


@router.post("/analyze")
async def scan_plant(file: UploadFile = File(...)):
    file_bytes = await file.read()
    label, confidence, box = analyze_plant_image(file_bytes)

    if label is None:
        return {"status": "error", "result": "Не удалось обнаружить растение на фото"}

    healthy_labels = ["healthy", "здоровое", "normal"] # Make sure your YOLO model outputs one of these for healthy plants
    if label.lower() in healthy_labels:
        return {
            "status": "ok",
            "result": "Healthy plant 🌱",
            "confidence": confidence,
            "label": label
        }

    # --- THIS IS THE CRUCIAL CHANGE ---
    # Parse the YOLO label into separate crop and disease components
    # that match the knowledge base structure.
    parsed_crop, parsed_disease = parse_yolo_label(label)

    # Now call generate_bot_reply with the correctly parsed crop and disease
    treatment_advice = generate_bot_reply("", disease=parsed_disease)

    return {
        "status": "ok",
        "result": f"Desease detected: {label}",
        "confidence": confidence,
        "label": label,
        "treatment_advice": treatment_advice
    }