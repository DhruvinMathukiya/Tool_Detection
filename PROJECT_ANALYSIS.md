# Tool Detection (Bearings, Housing, Shaft)

This project implements a computer vision system using the YOLOv8 framework to detect and potentially segment mechanical components: **Bearings**, **Housings**, and **Shafts**.

## Directory Structure

```
Tool_Detection/
├── best.pt             # Trained YOLOv8 model weights
├── data.yaml           # Dataset configuration (classes and paths)
├── train.py            # Script for training the YOLOv8 model
├── inference.py        # Script for real-time inference using a webcam
├── requirements.txt    # Python dependencies
└── venv/               # Virtual environment (ignored by git)
```

## Core Components

### 1. Model Configuration (`data.yaml`)
Defines the dataset structure and classes:
- **Classes (nc: 3):**
  - `0: bearing`
  - `1: housing`
  - `2: shaft`
- **Paths:** Expects a dataset at `./dataset` with `images/train` and `images/val` subdirectories.

### 2. Training (`train.py`)
Uses the `ultralytics` YOLOv8 implementation.
- **Base Model:** `yolov8s.pt` (Small YOLOv8 model).
- **Configuration:**
  - Epochs: 30
  - Image Size: 640x640
  - Batch Size: 16
  - Device: GPU (0) if available, otherwise CPU.
  - Augmentations: Degrees, flip (LR/UD), scale, and HSV adjustments.
- **Output:** Saves results to `runs/segment/bearing_housing_shaft_seg`.

### 3. Inference (`inference.py`)
A high-performance real-time detection script optimized for smooth preview.
- **Multi-threaded Architecture:** 
  - **Main Thread:** Handles camera capture, UI rendering, and result overlay at high FPS.
  - **Inference Thread:** Runs YOLOv8 detection in the background, updating results asynchronously.
- **Input:** Webcam stream (`cv2.VideoCapture(0)`).
- **Performance Features:**
  - **Smooth Preview:** Decoupled inference ensures the video feed remains fluid (targeting 19-24+ FPS).
  - **Real-time FPS Display:** Shows the actual rendering frame rate on-screen.
- **Functionality:**
  - Draws bounding boxes and displays object dimensions (width/height in pixels).
- **Control:** Press 'q' to exit.

### 4. Weights (`best.pt`)
The project includes a `best.pt` file, which is the result of a previous training session and can be used immediately for inference.

## Dependencies
The project relies on:
- `ultralytics`: For YOLOv8 model architecture and training.
- `torch`: For deep learning operations and GPU acceleration.
- `opencv-python` (`cv2`): For image processing and webcam handling.
- `PyYAML`: For parsing the configuration file.

## Usage

### Training
To train the model with your own dataset (configured in `data.yaml`):
```bash
python train.py
```

### Inference
To run real-time detection using the webcam:
```bash
python inference.py
```