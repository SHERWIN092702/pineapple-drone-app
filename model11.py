import sys
import cv2
from ultralytics import YOLO

# === Load YOLO model ===
model = YOLO("best.pt")  # Make sure 'best.pt' is in the same folder or provide full path

# === Get mode from command-line argument ===
mode = "live"  # Default
if len(sys.argv) > 1:
    mode = sys.argv[1].lower()

# === Video source setup ===
if mode == "test":
    cap = cv2.VideoCapture("test_video.mp4")  # Replace with actual test video path if needed
else:
    cap = cv2.VideoCapture(0)  # Webcam or UXPlay screen mirroring

# === Check if capture opened successfully ===
if not cap.isOpened():
    print("[ERROR] Could not open video source.")
    sys.exit(1)

# === Main loop ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("[INFO] End of stream or failed to read frame.")
        break

    # Run YOLO model on the frame
    results = model(frame)

    # Draw predictions
    annotated_frame = results[0].plot()

    # Display
    cv2.imshow("Pineapple Detection", annotated_frame)

    # Quit with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === Cleanup ===
cap.release()
cv2.destroyAllWindows()
