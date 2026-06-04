import argparse
import threading
import time
import cv2
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description="YOLOv8 Real-time Inference")
    parser.add_argument("--model", type=str, default="best.pt", help="Path to model weights")
    parser.add_argument("--source", type=int, default=0, help="Camera index or video path")
    parser.add_argument("--headless", action="store_true", help="Run without showing GUI window")
    return parser.parse_args()

# Shared variables
frame_lock = threading.Lock()
latest_frame = None
latest_results = None
new_frame_evt = threading.Event()
running = True

def inference_worker(model_path):
    """Background thread for model inference."""
    global latest_results, running
    
    # Load model inside thread to keep main thread responsive during init
    print(f"[Info] Loading model: {model_path}...")
    model = YOLO(model_path)
    print("[Info] Model loaded.")

    while running:
        # Wait for a new frame to process
        if new_frame_evt.wait(timeout=0.1):
            new_frame_evt.clear()
            
            with frame_lock:
                if latest_frame is None:
                    continue
                img = latest_frame.copy()
            
            # Run inference
            results = model(img, verbose=False)
            
            with frame_lock:
                latest_results = results
        else:
            # Idle sleep to prevent high CPU usage when no frames are coming
            time.sleep(0.001)

def main():
    global latest_frame, latest_results, running
    args = parse_args()
    
    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"[Error] Could not open video source {args.source}")
        return

    # Start inference worker
    infer_thread = threading.Thread(
        target=inference_worker, 
        args=(args.model,), 
        daemon=True
    )
    infer_thread.start()

    prev_time = time.time()
    print("[Info] Starting inference. Press 'q' in GUI or Ctrl+C in CLI to stop.")

    try:
        while running:
            ret, frame = cap.read()
            if not ret:
                print("[Warning] Failed to grab frame.")
                break

            # Update latest frame and signal worker
            with frame_lock:
                latest_frame = frame
                current_results = latest_results
            new_frame_evt.set()

            # Processing for display or logging
            if current_results:
                for result in current_results:
                    for box in result.boxes:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        width, height = x2 - x1, y2 - y1
                        
                        if not args.headless:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            label = f"W:{width}px H:{height}px"
                            cv2.putText(frame, label, (x1, y1 - 10), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        else:
                            # In headless mode, we can log to console periodically
                            pass 

            # Calculate FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time

            if not args.headless:
                cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow("Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                # Print status to CLI periodically
                if int(curr_time) % 5 == 0 and int(prev_time) % 5 != 0:
                    print(f"[Status] Running... FPS: {fps:.2f}")

    except KeyboardInterrupt:
        print("\n[Info] Interrupted by user.")
    finally:
        running = False
        cap.release()
        cv2.destroyAllWindows()
        print("[Info] Cleanup complete.")

if __name__ == "__main__":
    main()