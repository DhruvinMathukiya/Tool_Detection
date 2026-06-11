from unicodedata import name
from unittest import result

import cv2
import numpy as np
import base64
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ultralytics import YOLO

from paddleocr import PaddleOCR



app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:3000"],  # Adjust this to your frontend URL
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
model = YOLO("best.pt")

# Load PaddleOCR
ocr = PaddleOCR(
    use_textline_orientation=True,
    lang="en"
)

@app.get("/")
async def root():
    return {"message": "Tool Detection API is running"}

@app.post("/detect")        
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()

    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(img)

    detections = []

    for result in results:
        for box in result.boxes:

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            conf = float(box.conf[0])

            cls = int(box.cls[0])

            name = model.names[cls]

            # -----------------------
            # Crop bearing
            # -----------------------

            crop = img[y1:y2, x1:x2]

            detected_text = ""

            if crop.size > 0:

                # Convert to gray
                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

                gray = cv2.resize(
                    gray,
                    None,
                    fx=4,
                    fy=4,
                    interpolation=cv2.INTER_CUBIC
                )

                gray = cv2.equalizeHist(gray)

                # Convert back to 3-channel image
                gray = cv2.cvtColor(
                    gray,
                    cv2.COLOR_GRAY2BGR
                )

                ocr_result = ocr.predict(gray)

                # Sharpen
                kernel = np.array([
                    [-1,-1,-1],
                    [-1, 9,-1],
                    [-1,-1,-1]
                ])

                gray = cv2.filter2D(gray, -1, kernel)

                # OCR
                ocr_result = ocr.predict(gray)

                print(ocr_result)

                try:

                    if (
                        len(ocr_result) > 0 and
                        "rec_texts" in ocr_result[0] and
                        len(ocr_result[0]["rec_texts"]) > 0
                    ):

                        detected_text = " ".join(
                            ocr_result[0]["rec_texts"]
                        )

                except Exception as e:
                    print(e)

            detections.append({
                "class": name,
                "confidence": round(conf, 2),
                "serial_number": detected_text
            })

            # -----------------------
            # Draw bounding box
            # -----------------------

            cv2.rectangle(
                img,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Detection label

            label = f"{name} | {conf:.2f}"

            cv2.putText(
                img,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

            # OCR text

            if detected_text != "":

                cv2.putText(
                    img,
                    detected_text,
                    (x1, y2 + 20),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 0, 0),
                    2
                )

    _, buffer = cv2.imencode(".jpg", img)

    img_base64 = base64.b64encode(
        buffer
    ).decode("utf-8")

    return {
        "detections": detections,
        "image": f"data:image/jpeg;base64,{img_base64}",
        "count": len(detections)
    }
@app.get("/stream")
async def stream_detections(request: Request):
    return StreamingResponse(frame_generator(request), media_type="text/event-stream")
    if crop.size > 0:
        ocr_result = ocr.predict(crop)

    print("\n====================")
    print("OCR RESULT:")
    print(ocr_result)
    print("====================\n")

    print("\nOCR RESULT:")
    print(ocr_result)

    detected_text = str(ocr_result)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)