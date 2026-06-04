# Tool Detection System Dashboard

A modern, web-based real-time detection system for mechanical components (Bearings, Housings, and Shafts) powered by **YOLOv8**, **FastAPI**, and **React**.

## Features
- **Real-time Streaming:** Low-latency live detection via Server-Sent Events (SSE).
- **Image Upload:** Process static images to see detailed detections and object counts.
- **Modern UI:** Responsive dashboard built with Vite, React, and Tailwind CSS.
- **Async Processing:** Decoupled backend captures to ensure smooth performance.

---

## 🛠️ Setup & Installation

### 1. Backend Setup (Python)
Ensure you have Python 3.10+ installed.

```bash
# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 2. Frontend Setup (Node.js)
Ensure you have Node.js 18+ installed.

```bash
cd frontend
npm install
```

---

## 🚀 Running the Application

To run the full system, you need to start both the backend and the frontend.

### 1. Start the Backend API
From the root directory (ensure venv is active):
```bash
python backend/main.py
```
*The API will run on `http://localhost:8000`.*

### 2. Start the Frontend Dashboard
Open a new terminal, navigate to the `frontend` folder, and run:
```bash
npm run dev
```
*The dashboard will be available at `http://localhost:5173` (or similar).*

---

## 📂 Project Structure
- `backend/`: FastAPI application, YOLOv8 weights (`best.pt`), and training scripts.
- `frontend/`: Vite + React source code and dashboard UI.
- `PROJECT_ANALYSIS.md`: Detailed architectural breakdown and data flow.

---

## 📝 License
This project is powered by the Ultralytics YOLOv8 framework.
