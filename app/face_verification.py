from deepface import DeepFace
import cv2
import tempfile
import os


def verify_faces(id_image, selfie_image):

    # Save images temporarily
    with tempfile.NamedTemporaryFile(
        suffix=".jpg", delete=False
    ) as id_file:
        id_path = id_file.name
        cv2.imwrite(id_path, id_image)

    with tempfile.NamedTemporaryFile(
        suffix=".jpg", delete=False
    ) as selfie_file:
        selfie_path = selfie_file.name
        cv2.imwrite(selfie_path, selfie_image)

    try:
        # Extract face from ID
        id_faces = DeepFace.extract_faces(
            img_path=id_path,
            detector_backend="opencv",
            enforce_detection=True,
            align=True
        )

        # Extract face from selfie
        selfie_faces = DeepFace.extract_faces(
            img_path=selfie_path,
            detector_backend="opencv",
            enforce_detection=True,
            align=True
        )

        print("ID faces detected:", len(id_faces))
        print("Selfie faces detected:", len(selfie_faces))

        # Save detected/aligned faces for inspection
        id_face = id_faces[0]["face"]
        selfie_face = selfie_faces[0]["face"]

        cv2.imwrite(
            "debug_id_face.jpg",
            (id_face * 255).astype("uint8")
        )

        cv2.imwrite(
            "debug_selfie_face.jpg",
            (selfie_face * 255).astype("uint8")
        )

        # Compare
        result = DeepFace.verify(
            img1_path=id_path,
            img2_path=selfie_path,
            model_name="Facenet512",
            detector_backend="opencv",
            distance_metric="cosine",
            threshold=0.39
        )

        return {
            "verified": bool(result["verified"]),
            "distance": float(result["distance"]),
            "threshold": float(result["threshold"])
        }

    finally:
        if os.path.exists(id_path):
            os.remove(id_path)

        if os.path.exists(selfie_path):
            os.remove(selfie_path)