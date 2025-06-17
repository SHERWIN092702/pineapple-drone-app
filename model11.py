import cv2
import numpy as np
from mss import mss
from ultralytics import YOLO

# === Load YOLO Model ===
# Make sure this path matches your actual model location
model = YOLO('/home/rpi5/Desktop/yolo_object/best.pt')  # <- or best_ncnn_model if you're using NCNN export

# === Screen Region to Capture (adjust as needed for uxplay window) ===
bounding_box = {'top': 50, 'left': 0, 'width': 1920, 'height': 850}
sct = mss()

print("[INFO] Starting detection... Press 'q' to stop.")

while True:
    # Capture screen
    sct_img = sct.grab(bounding_box)
    frame = np.array(sct_img)[:, :, :3]  # drop alpha channel

    # Run YOLO detection
    results = model(frame)
    annotated_frame = results[0].plot()

    # Show annotated result
    cv2.imshow("Pineapple Maturity Detection", annotated_frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Detection stopped.")
        break

cv2.destroyAllWindows()
