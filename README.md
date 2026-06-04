# Tool Detection System

A YOLOv8-based real-time detection system for mechanical components (Bearings, Housings, and Shafts).

## Quick Start

### 1. Setup Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run Inference
To start real-time detection using your webcam:
```bash
python inference.py
```

### 3. Training
To train the model on your dataset (configured in `data.yaml`):
```bash
python train.py
```

## Features
- **Smooth Real-time Detection:** Multi-threaded architecture for fluid video preview (19-24+ FPS).
- **Asynchronous Inference:** Detection runs in the background to prevent UI lag.
- **Dimension Tracking:** Displays width and height of detected parts in pixels.
- **FPS Counter:** Integrated on-screen frame rate monitoring.
- **Pre-trained Weights:** Includes `best.pt` for immediate use.

For a detailed breakdown of the architecture and configuration, see [PROJECT_ANALYSIS.md](./PROJECT_ANALYSIS.md).
