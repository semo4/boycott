from fastapi import FastAPI, File, UploadFile, HTTPException
import cv2
import numpy as np
from src.utils.helpers import response, extract_barcode, read_barcode, identify_barcode_type, detect_crop_barcode


app = FastAPI()


@app.post("/read-barcode", description="Get Barcode Image and return The Barcode and it's Type")
async def read_barcode_api(file: UploadFile = File(...)):
    try:
        # Read the image from the file
        content = await file.read()
        # convert data to image using cv2
        image = cv2.imdecode(np.frombuffer(
            content, np.uint8), cv2.IMREAD_COLOR)

        # Call the read_barcode function
        barcode_results = read_barcode(image)

        # Return the results as JSON
        return response(True, barcode_results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/extract-barcode", description="Extract Barcode from Image and return The Barcode and it's Type")
async def extract_barcode_api(file: UploadFile = File(...)):
    try:
        barcode_results = []
        # Read the image from the file
        content = await file.read()
        # convert data to image using cv2
        image = cv2.imdecode(np.frombuffer(
            content, np.uint8), cv2.IMREAD_COLOR)
        barcode_results = extract_barcode(image)
        return response(True, barcode_results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/barcode", description="Get Barcode and return it's Type")
async def barcode_api(barcode: str):
    try:
        barcode_results = []
        barcode_type = identify_barcode_type(barcode)
        # Return the results as JSON
        barcode_results.append({"data": barcode, "type": barcode_type})
        return response(True, barcode_results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback", description="Send Feedback about Product or Company")
async def feedback(description: str, boycott: bool, file: UploadFile = File(...)):
    try:
        barcode_results = []
        content = await file.read()
        # convert data to image using cv2
        image = cv2.imdecode(np.frombuffer(
            content, np.uint8), cv2.IMREAD_COLOR)
        barcode = read_barcode(image)
        barcode_results.append(
            {"description": description, "barcode": barcode, "boycott": boycott})
        return barcode_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/detect-crop", description="Detect Barcode from image and crop it")
async def detect_crop(file: UploadFile = File(...)):
    try:
        barcode_results = []
        content = await file.read()
        # convert data to image using cv2
        image = cv2.imdecode(np.frombuffer(
            content, np.uint8), cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cropped_image = detect_crop_barcode(image, gray)
        barcode = read_barcode(cropped_image)
        barcode_results.append(
            {"description": "image cropped", "barcode": barcode})
        return barcode_results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
