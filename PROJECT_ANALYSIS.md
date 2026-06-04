# Tool Detection System (Bearings, Housing, Shaft)

This project implements a modern web-based computer vision system using the YOLOv8 framework to detect mechanical components: **Bearings**, **Housings**, and **Shafts**.

## Directory Structure

```
Tool_Detection/
├── backend/
│   ├── main.py             # FastAPI server with SSE streaming
│   ├── best.pt             # Trained YOLOv8 model weights
│   ├── data.yaml           # Dataset configuration
│   ├── train.py            # Script for training the model
│   └── requirements.txt    # Python dependencies (FastAPI, Ultralytics, etc.)
├── frontend/               # Vite + React Dashboard
│   ├── src/
│   │   ├── App.jsx         # Main dashboard logic and UI
│   │   └── index.css       # Tailwind CSS styles
│   ├── vite.config.js      # Vite configuration with Tailwind plugin
│   └── package.json        # Frontend dependencies
├── PROJECT_ANALYSIS.md     # Project overview (this file)
├── README.md               # Quick start guide
└── venv/                   # Python virtual environment
```

## Core Components

### 1. Model Configuration (`backend/data.yaml`)
Defines the dataset structure and classes:
- **Classes:** `0: bearing`, `1: housing`, `2: shaft`.
- **Target:** Detection and potentially segmentation of industrial parts.

### 2. Backend API (`backend/main.py`)
A FastAPI application that serves as the bridge between the YOLO model and the web frontend.
- **Image Detection (`/detect`):** Accepts an image upload, runs inference, and returns the annotated image (base64) and object counts.
- **Real-time Streaming (`/stream`):** Uses **Server-Sent Events (SSE)** to push live detection frames from the local webcam to the dashboard.
- **CORS Enabled:** Configured to allow communication with the React frontend.

### 3. Frontend Dashboard (`frontend/src/App.jsx`)
A responsive dashboard built with **Vite**, **React**, and **Tailwind CSS**.
- **Tabbed Interface:** Seamlessly switch between "Upload" and "Real-time" modes.
- **SSE Integration:** Handles persistent connections for low-latency live streaming.
- **Responsive Design:** Optimized for various screen sizes with modern UI elements from Lucide-React.

## Data Flow Architecture

### Real-time Mode (SSE)
1. **Frontend** initiates a `new EventSource('/stream')`.
2. **Backend** captures frames from the webcam via OpenCV.
3. **YOLOv8** processes each frame and draws detections.
4. **Backend** encodes the result as Base64 and pushes it as an SSE message.
5. **Frontend** receives the payload and updates the UI state to render the live feed.

### Upload Mode (HTTP)
1. **Frontend** sends an image via `multipart/form-data` to `/detect`.
2. **Backend** runs inference and returns a JSON response.
3. **Frontend** displays the processed result alongside the object count.

## Usage Summary
- **Backend:** Run with `uvicorn backend.main:app` or `python backend/main.py`.
- **Frontend:** Run with `npm run dev` inside the `frontend` folder.
