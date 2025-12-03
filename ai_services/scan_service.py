from ultralytics import YOLO
import tempfile, os, sys

# Определяем путь к модели в зависимости от EXE или dev-режима
def get_model_path():
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, "best.pt")
    return "best.pt"

model = YOLO(get_model_path())  # правильно подхватываем best.pt


def analyze_plant_image(file_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    results = model.predict(tmp_path, imgsz=320)
    os.remove(tmp_path)

    r = results[0]
    if len(r.boxes) == 0:
        return None, None, None

    box = r.boxes[0]
    cls_id = int(box.cls[0])
    confidence = float(box.conf[0])
    label = model.names[cls_id]

    return label, confidence, box
