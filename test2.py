from ultralytics import YOLO

model = YOLO("best.pt")
for cls_id, name in model.names.items():
    print(cls_id, name)