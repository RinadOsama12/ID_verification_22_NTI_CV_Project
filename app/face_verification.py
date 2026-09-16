from deepface import DeepFace
import cv2
import tempfile
import os


def verify_faces(id_image, selfie_image):

    # Save cropped ID image
    with tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    ) as id_file:

        id_path = id_file.name

        cv2.imwrite(
            id_path,
            id_image
        )

    # Save selfie image
    with tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    ) as selfie_file:

        selfie_path = selfie_file.name

        cv2.imwrite(
            selfie_path,
            selfie_image
        )

    try:

        result = DeepFace.verify(
            img1_path=id_path,
            img2_path=selfie_path,
            model_name="Facenet512",
            detector_backend="opencv"
        )

        return {
            "verified": bool(result["verified"]),
            "distance": float(result["distance"])
        }

    finally:

        # Delete temporary files
        if os.path.exists(id_path):
            os.remove(id_path)

        if os.path.exists(selfie_path):
            os.remove(selfie_path)