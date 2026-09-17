import easyocr

# Arabic + English
reader = easyocr.Reader(
    ['ar', 'en'],
    gpu=False
)


def extract_text(image):
    if image is None or image.size == 0:
        return ""

    results = reader.readtext(image)

    texts = []

    for result in results:
        text = result[1]
        confidence = result[2]

        if confidence >= 0.30:
            texts.append(text)

    return " ".join(texts)


def extract_multiple_crops(crops):
    all_text = []

    for crop in crops:
        text = extract_text(crop)

        if text:
            all_text.append(text)

    return " ".join(all_text)


def extract_id_information(
    name_crops,
    address_crops,
    number_crops
):
    name = extract_multiple_crops(name_crops)
    address = extract_multiple_crops(address_crops)
    id_number = extract_multiple_crops(number_crops)

    return {
        "name": name,
        "address": address,
        "id_number": id_number
    }