import cv2
import numpy as np
import base64
import json
import asyncio
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from ultralytics import YOLO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
model = YOLO("best.pt")

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
            
            detections.append({
                "box": [x1, y1, x2, y2],
                "confidence": conf,
                "class": name
            })
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, f"{name} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    _, buffer = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return {
        "detections": detections,
        "image": f"data:image/jpeg;base64,{img_base64}",
        "count": len(detections)
    }

async def frame_generator(request: Request):
    cap = cv2.VideoCapture(0)
    try:
        while True:
            # Check if client disconnected
            if await request.is_disconnected():
                break

            success, frame = cap.read()
            if not success:
                break

            results = model(frame)
            count = 0
            for result in results:
                for box in result.boxes:
                    count += 1
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    name = model.names[int(box.cls[0])]
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            img_base64 = base64.b64encode(buffer).decode('utf-8')

            data = {
                "image": f"data:image/jpeg;base64,{img_base64}",
                "count": count
            }
            
            # SSE format: "data: <payload>\n\n"
            yield f"data: {json.dumps(data)}\n\n"
            
            # Small sleep to control FPS and prevent CPU hogging
            await asyncio.sleep(0.05)
            
    finally:
        cap.release()

@app.get("/stream")
async def stream_detections(request: Request):
    return StreamingResponse(frame_generator(request), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)