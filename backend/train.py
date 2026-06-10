from ultralytics import YOLO
import torch


def main():

    # Check GPU
    print("CUDA available:", torch.cuda.is_available())

    if torch.cuda.is_available():
        print("GPU:", torch.cuda.get_device_name(0))
    else:
        print("Training will run on CPU")

    # Load pretrained YOLOv8 segmentation model
    model = YOLO("yolov8s.pt")

    # Train
    results = model.train(
        data="data.yaml",         
        epochs=60,               
        imgsz=640,                
        batch=4,                    
        device=0,                  
        workers=0,
        patience=30,
        pretrained=True,
        cache=False,
        amp=True,

        # augmentation
        degrees=20,
        fliplr=0.5,
        flipud=0.2,
        scale=0.3,
        hsv_h=0.015,
        hsv_s=0.7,
        hsv_v=0.4,

        # output
        project="runs/segment",
        name="bearing_housing_shaft_seg",
        save=True,
        plots=True,
        verbose=True
    )

    print("Training complete")
    print("Best model saved at:")
    print("runs/segment/bearing_housing_shaft_seg/weights/best.pt")


if __name__ == "__main__":
    main()