from fastapi import FastAPI, UploadFile, File
from deepface.modules.exceptions import FaceNotDetected

from app.model import predict_id
from app.face_verification import verify_faces

import cv2
import numpy as np

from app.ocr import extract_id_information
app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "ID Verification API is running"
    }


@app.post("/verify-face")
async def verify_face(
    id_image: UploadFile = File(...),
    selfie: UploadFile = File(...)
):

    try:

        
        # 1. Read ID
        # -------------------------

        id_bytes = await id_image.read()

        if not id_bytes:
            return {
                "verified": False,
                "id_detected": False,
                "message": "ID image is empty"
            }

        
        # 2. YOLO
        # -------------------------

        yolo_result = predict_id(id_bytes)

        if not yolo_result["detected"]:
            return {
                "verified": False,
                "id_detected": False,
                "message": yolo_result["message"]
            }

        
        # 3. Read selfie
        # -------------------------

        selfie_bytes = await selfie.read()

        if not selfie_bytes:
            return {
                "verified": False,
                "id_detected": True,
                "message": "Selfie image is empty"
            }

        selfie_array = np.frombuffer(
            selfie_bytes,
            np.uint8
        )

        selfie_image = cv2.imdecode(
            selfie_array,
            cv2.IMREAD_COLOR
        )

        if selfie_image is None:
            return {
                "verified": False,
                "id_detected": True,
                "message": "Could not decode selfie image"
            }

        
        # 4. Face verification
        # -------------------------

        result = verify_faces(
            yolo_result["id_crop"],
            selfie_image
        )
        ocr_result = extract_id_information(
    yolo_result["name_crops"],
    yolo_result["address_crops"],
    yolo_result["number_crops"]
)
        
        # 5. Response
        # -------------------------

        return {
    "verified": result["verified"],
    "id_detected": True,

    "face_distance": result["distance"],
    "threshold": result["threshold"],

    "yolo_confidence": yolo_result["confidence"],

    "name": ocr_result["name"],
    "address": ocr_result["address"],
    "id_number": ocr_result["id_number"]
}
    except FaceNotDetected:

        return {
            "verified": False,
            "id_detected": True,
            "message": "Could not detect a face in the ID or selfie"
        }

    except Exception as e:

        print("ERROR:", repr(e))

        return {
            "verified": False,
            "id_detected": False,
            "message": f"Verification failed: {str(e)}"
        }