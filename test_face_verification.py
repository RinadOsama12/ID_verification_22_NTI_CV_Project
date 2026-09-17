import cv2

from app.model import predict_id
from app.face_verification import verify_faces



# 1. Read ID image

with open("Rinad_Front_Id.jpeg", "rb") as f:
    id_bytes = f.read()


# -----------------------------
# 2. YOLO detects the ID card
# -----------------------------
id_result = predict_id(id_bytes)

print("YOLO result:")
print({
    "detected": id_result["detected"],
    "confidence": id_result.get("confidence"),
    "bbox": id_result.get("bbox")
})


if not id_result["detected"]:
    print("❌ No ID card detected")
    exit()


# Get the cropped ID image
id_crop = id_result["id_crop"]
cv2.imwrite("debug_face_crop.jpg", id_crop)


# -----------------------------
# 3. Read selfie
# -----------------------------
selfie_image = cv2.imread("dad.jpeg")

if selfie_image is None:
    raise FileNotFoundError("Could not load selfie.jpg")


result_color = verify_faces(
    id_crop,
    selfie_image
)

print("\nColor/normal result:")
print(result_color)


# Convert both to grayscale
id_gray = cv2.cvtColor(id_crop, cv2.COLOR_BGR2GRAY)
selfie_gray = cv2.cvtColor(selfie_image, cv2.COLOR_BGR2GRAY)

result_gray = verify_faces(
    id_gray,
    selfie_gray
)

print("\nGrayscale result:")
print(result_gray)

