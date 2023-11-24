from pyzbar.pyzbar import decode
import cv2
from typing import List
import easyocr


def identify_barcode_type(barcode_data):
    if len(barcode_data) == 12:
        return "UPC-A"
    elif len(barcode_data) == 13:
        return "EAN-13"
    elif len(barcode_data) >= 8 and len(barcode_data) <= 12:
        return "Code 39"
    else:
        return "Unknown"


def detect_crop_barcode(image, gray_image):
    bar_codes = decode(gray_image)

    if bar_codes:
        bar_code = bar_codes[0]
        x, y, w, h = bar_code.rect

        margin = 120

        cropped_bar_code = image[y - margin: y +
                                 h + margin, x - margin: x + w + margin]

        # cv2.imwrite("cropped_image.png", cropped_bar_code)
        return cropped_bar_code
    else:
        return None


def response(success: bool, barCodes: List):
    result = dict()
    result = {"success": success, "barCodes": barCodes}
    return result


def extract_barcode(image):
    results = []
    reader = easyocr.Reader(['en'])
    # Read the image and extract text
    result = reader.readtext(image)

    # Extract only numeric characters from the OCR result
    extracted_numbers = ""
    for res in result:
        extracted_numbers += ''.join(filter(str.isdigit, res[1]))

    # print(f"Extracted Numbers: {extracted_numbers}")
    # Call the read_barcode function
    barcode_type = identify_barcode_type(extracted_numbers)

    results.append({"data": extracted_numbers, "type": barcode_type})
    return results


def read_barcode(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use the pyzbar library to decode barCodes
    bar_codes = decode(gray)

    results = []

    if not bar_codes:
        # if can't detect Barcode we will extract it
        results = extract_barcode(gray)
    else:
        # Loop through the detected barCodes and collect the data
        for barcode in bar_codes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type

            results.append({"data": barcode_data, "type": barcode_type})

    return results
