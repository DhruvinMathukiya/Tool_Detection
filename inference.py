from ultralytics import YOLO
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Load YOLO model
model = YOLO("best.pt")

image_path = None
output_image = None


# ---------------- Upload Image ----------------
def upload_image():
    global image_path

    image_path = filedialog.askopenfilename(
        title="Select Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.bmp")
        ]
    )

    if not image_path:
        return

    img = Image.open(image_path)

    # Larger preview size
    img = img.resize((600, 500))

    photo = ImageTk.PhotoImage(img)

    original_label.config(image=photo)
    original_label.image = photo

    status_label.config(text="Image Loaded Successfully")


# ---------------- Run Detection ----------------
def detect_objects():
    global output_image

    if image_path is None:
        messagebox.showwarning(
            "Warning",
            "Please upload an image first."
        )
        return

    image = cv2.imread(image_path)

    results = model(image)

    count = 0

    for result in results:
        for box in result.boxes:

            count += 1

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            confidence = float(box.conf[0])

            width = x2 - x1
            height = y2 - y1

            # Draw box
            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )

            label = (
                f"Conf:{confidence:.2f} "
                f"W:{width}px "
                f"H:{height}px"
            )

            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 0),
                2
            )

    output_image = image.copy()

    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    img = Image.fromarray(image_rgb)

    # Larger preview size
    img = img.resize((600, 500))

    photo = ImageTk.PhotoImage(img)

    result_label.config(image=photo)
    result_label.image = photo

    info_label.config(
        text=f"Detected Objects: {count}"
    )

    status_label.config(
        text="Detection Completed"
    )


# ---------------- Save Output ----------------
def save_output():

    if output_image is None:
        messagebox.showwarning(
            "Warning",
            "No output image available."
        )
        return

    save_path = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("JPEG", "*.jpg")]
    )

    if save_path:
        cv2.imwrite(save_path, output_image)

        messagebox.showinfo(
            "Success",
            "Output Image Saved Successfully"
        )


# ---------------- View Full Image ----------------
def view_full_image():

    if output_image is None:
        messagebox.showwarning(
            "Warning",
            "Run detection first."
        )
        return

    cv2.imshow(
        "Full Resolution Detection Result",
        output_image
    )
    cv2.waitKey(0)


# ---------------- GUI ----------------
root = tk.Tk()
root.title("YOLO Object Detection System")

# Bigger Window
root.geometry("1400x900")

# Title
title = tk.Label(
    root,
    text="YOLO Object Detection",
    font=("Arial", 24, "bold")
)
title.pack(pady=15)

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

upload_btn = tk.Button(
    button_frame,
    text="Upload Image",
    command=upload_image,
    width=20,
    height=2,
    bg="lightblue"
)
upload_btn.grid(row=0, column=0, padx=10)

detect_btn = tk.Button(
    button_frame,
    text="Run Detection",
    command=detect_objects,
    width=20,
    height=2,
    bg="lightgreen"
)
detect_btn.grid(row=0, column=1, padx=10)

save_btn = tk.Button(
    button_frame,
    text="Save Output",
    command=save_output,
    width=20,
    height=2,
    bg="orange"
)
save_btn.grid(row=0, column=2, padx=10)



# Image Area
image_frame = tk.Frame(root)
image_frame.pack(pady=20)

original_label = tk.Label(
    image_frame,
    text="Original Image",
    relief="solid",
    bd=2
)
original_label.grid(
    row=0,
    column=0,
    padx=20
)

result_label = tk.Label(
    image_frame,
    text="Detection Result",
    relief="solid",
    bd=2
)
result_label.grid(
    row=0,
    column=1,
    padx=20
)

# Info
info_label = tk.Label(
    root,
    text="Detected Objects: 0",
    font=("Arial", 14)
)
info_label.pack(pady=10)

status_label = tk.Label(
    root,
    text="Ready",
    fg="blue",
    font=("Arial", 12)
)
status_label.pack()

root.mainloop()