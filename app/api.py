from fastapi import FastAPI, UploadFile, File, HTTPException

import numpy as np
import cv2

from app.model import predict_id
from app.face_verification import verify_faces


app = FastAPI(
    title="ID Verification API",
    description="Computer Vision API for ID verification",
    version="1.0"
)


@app.get("/")
def home():

    return {
        "message": "ID verification API is running"
    }

from fastapi.concurrency import run_in_threadpool

@app.post("/verify-face")
async def verify_face(id_image: UploadFile = File(...), selfie: UploadFile = File(...)):
    id_bytes = await id_image.read()
    id_result = await run_in_threadpool(predict_id, id_bytes)

    if not id_result["detected"]:
        return {"verified": False, "id_detected": False, "message": "No ID detected"}

    id_crop = id_result["id_crop"]
    if id_crop is None or id_crop.size == 0:
        return {"verified": False, "id_detected": False, "message": "ID crop was empty"}

    selfie_bytes = await selfie.read()
    selfie_array = np.frombuffer(selfie_bytes, np.uint8)
    selfie_image = cv2.imdecode(selfie_array, cv2.IMREAD_COLOR)

    if selfie_image is None:
        raise HTTPException(status_code=400, detail="Invalid selfie image")

    face_result = await run_in_threadpool(verify_faces, id_crop, selfie_image)

    return {
        "verified": face_result["verified"],
        "id_detected": True,
        "id_confidence": id_result["confidence"],
        "bbox": id_result["bbox"],
        "face_distance": face_result["distance"],
    }