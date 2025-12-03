from ultralytics import YOLO
import tempfile, os
from logging_config import setup_logging
import logging

logger = setup_logging()


# Загружаем модель один раз
model = YOLO("best.pt")  # используем извлечённый .pt

def analyze_plant_image(file_bytes: bytes):
    logger.info("User image received")
    # сохраняем во временный файл
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    results = model.predict(tmp_path, imgsz=320)  # уменьшенное для CPU
    os.remove(tmp_path)

    r = results[0]
    if len(r.boxes) == 0:
        logger.info("Scan reply: Plant is not recognized")
        return None, None, None

    box = r.boxes[0]
    cls_id = int(box.cls[0])
    confidence = float(box.conf[0])
    label = model.names[cls_id]
    logger.info(f"Scan reply: '{label}' ")
    return label, confidence, box
