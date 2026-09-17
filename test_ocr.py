import cv2

from app.model import predict_id
from app.ocr import extract_id_information


# --------------------------------------------------
# Read ID image
# --------------------------------------------------

with open("Rinad_Front_Id.jpeg", "rb") as f:
    image_bytes = f.read()


# --------------------------------------------------
# Run YOLO
# --------------------------------------------------

result = predict_id(image_bytes)


if not result["detected"]:

    print("❌ No face detected on ID")
    print(result["message"])

    exit()


print("✅ YOLO detected the ID face")
print(
    f"Face confidence: {result['confidence']:.4f}"
)


# --------------------------------------------------
# Check detected OCR crops
# --------------------------------------------------

print(
    f"Name crops: {len(result['name_crops'])}"
)

print(
    f"Address crops: {len(result['address_crops'])}"
)

print(
    f"Number crops: {len(result['number_crops'])}"
)


# --------------------------------------------------
# Run OCR
# --------------------------------------------------

ocr_result = extract_id_information(

    result["name_crops"],

    result["address_crops"],

    result["number_crops"]
)


# --------------------------------------------------
# Display OCR result
# --------------------------------------------------

print("\n========== OCR RESULT ==========")

print(
    "Name:",
    ocr_result["name"]
)

print(
    "Address:",
    ocr_result["address"]
)

print(
    "ID Number:",
    ocr_result["id_number"]
)

print("================================")
