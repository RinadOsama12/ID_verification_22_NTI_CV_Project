from ultralytics import YOLO
import cv2
import numpy as np
from pathlib import Path


MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "best.pt"

model = YOLO(str(MODEL_PATH))


# YOLO class IDs
FACE_CLASSES = [2]

NAME_CLASSES = [3, 4, 5]

ADDRESS_CLASSES = [0, 1]

NUMBER_CLASSES = [6, 7]


def predict_id(image_bytes):

    # Convert bytes → OpenCV image
    image_array = np.frombuffer(image_bytes, np.uint8)

    image = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if image is None:
        return {
            "detected": False,
            "message": "Invalid image"
        }


    # Run YOLO
    results = model.predict(
        source=image,
        verbose=False
    )

    result = results[0]


    # --------------------------------------------------
    # Store detected crops
    # --------------------------------------------------

    face_crops = []
    name_crops = []
    address_crops = []
    number_crops = []


    # --------------------------------------------------
    # Process YOLO boxes
    # --------------------------------------------------

    for box in result.boxes:

        class_id = int(box.cls[0])

        confidence = float(box.conf[0])

        x1, y1, x2, y2 = map(
            int,
            box.xyxy[0].tolist()
        )


        # Make sure coordinates are inside image
        x1 = max(0, x1)
        y1 = max(0, y1)

        x2 = min(image.shape[1], x2)
        y2 = min(image.shape[0], y2)


        crop = image[y1:y2, x1:x2]


        if crop.size == 0:
            continue


        # ----------------------------------------------
        # Face
        # ----------------------------------------------

        if class_id in FACE_CLASSES:

            face_crops.append(
                (confidence, crop)
            )


        # ----------------------------------------------
        # Name
        # ----------------------------------------------

        elif class_id in NAME_CLASSES:

            name_crops.append(
                (class_id, confidence, crop)
            )


        # ----------------------------------------------
        # Address
        # ----------------------------------------------

        elif class_id in ADDRESS_CLASSES:

            address_crops.append(
                (class_id, confidence, crop)
            )


        # ----------------------------------------------
        # ID Number
        # ----------------------------------------------

        elif class_id in NUMBER_CLASSES:

            number_crops.append(
                (class_id, confidence, crop)
            )


    # --------------------------------------------------
    # No face
    # --------------------------------------------------

    if not face_crops:

        return {
            "detected": False,
            "message": "No face detected on ID"
        }


    # Select highest-confidence face
    face_confidence, face_crop = max(
        face_crops,
        key=lambda x: x[0]
    )


    # --------------------------------------------------
    # Sort text crops
    #
    # Sort by vertical position would be even better,
    # but for now confidence/class ordering is enough.
    # --------------------------------------------------

    name_crops.sort(
        key=lambda x: x[0]
    )

    address_crops.sort(
        key=lambda x: x[0]
    )

    number_crops.sort(
        key=lambda x: x[0]
    )


    return {

        "detected": True,

        "class": "Face",

        "confidence": face_confidence,

        "bbox": [
            0,
            0,
            face_crop.shape[1],
            face_crop.shape[0]
        ],

        # Face → DeepFace
        "id_crop": face_crop,

        # Text → OCR
        "name_crops": [
            crop for _, _, crop in name_crops
        ],

        "address_crops": [
            crop for _, _, crop in address_crops
        ],

        "number_crops": [
            crop for _, _, crop in number_crops
        ]
    }