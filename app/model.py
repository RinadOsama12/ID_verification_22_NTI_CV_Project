from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "best.pt"

model = YOLO(str(MODEL_PATH))

FACE_CLASS_ID = 2


def predict_id(image_bytes):

    # Bytes → NumPy
    image_array = np.frombuffer(image_bytes, np.uint8)

    # NumPy → OpenCV image
    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return {
            "detected": False,
            "message": "Invalid image"
        }

    # Run YOLO on THIS image
    results = model.predict(
        source=image,
        verbose=False
    )

    result = results[0]

    # Find Face detection
    face_boxes = []

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        if class_id == FACE_CLASS_ID:
            face_boxes.append((confidence, box))

    if not face_boxes:
        return {
            "detected": False,
            "message": "No face detected on ID"
        }

    # Select highest-confidence face
    confidence, box = max(
        face_boxes,
        key=lambda x: x[0]
    )

    x1, y1, x2, y2 = map(
        int,
        box.xyxy[0].tolist()
    )

    # Crop face
    face_crop = image[y1:y2, x1:x2]

    return {
        "detected": True,
        "class": "Face",
        "confidence": confidence,
        "bbox": [x1, y1, x2, y2],
        "id_crop": face_crop
    }