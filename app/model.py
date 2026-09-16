from ultralytics import YOLO
import cv2 
import numpy as np
# Load your trained YOLOv8 model
from pathlib import Path
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "best.pt"
model = YOLO(str(MODEL_PATH))


def predict_id(image_bytes):

    # Convert uploaded bytes → NumPy array
    image_array = np.frombuffer(image_bytes, np.uint8)

    # Convert NumPy array → OpenCV image
    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return {
            "detected": False,
            "message": "Invalid image"
        }

    # YOLOv8 prediction
    results = model(image)

    result = results[0]

    if len(result.boxes) == 0:
        return {
            "detected": False,
            "message": "No ID detected"
        }

    # First detected bounding box
    box = result.boxes[0]

    coordinates = box.xyxy[0].tolist()

    x1, y1, x2, y2 = map(int, coordinates)

    confidence = float(box.conf[0])

    # Crop the detected ID
    id_crop = image[y1:y2, x1:x2]

    return {
        "detected": True,
        "confidence": confidence,
        "bbox": [x1, y1, x2, y2],
        "id_crop": id_crop
    }