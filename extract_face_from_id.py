
from ultralytics import YOLO
from PIL import Image

model = YOLO("best.pt")

def extract_face_from_id(image_path, conf=0.5):
    results = model.predict(image_path, conf=conf, verbose=False)
    boxes = results[0].boxes
    names = results[0].names

    best_conf = -1
    face_box = None
    for box in boxes:
        cls_id = int(box.cls[0])
        if names[cls_id] == "Face":
            conf_val = float(box.conf[0])
            if conf_val > best_conf:
                best_conf = conf_val
                face_box = box.xyxy[0].tolist()

    if face_box is None:
        return None

    img = Image.open(image_path)
    x1, y1, x2, y2 = map(int, face_box)
    return img.crop((x1, y1, x2, y2))
