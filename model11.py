import cv2
import sys
from ultralytics import YOLO

# Load your trained model
model = YOLO("best.pt")  # Make sure best.pt is in the same folder as this script

# Check input mode
source_mode = sys.argv[1] if len(sys.argv) > 1 else "live"

# Choose video source
if source_mode == "test":
    video_path = "test_video.mp4"  # Replace with your video filename if needed
    cap = cv2.VideoCapture(video_path)
else:
    cap = cv2.VideoCapture(0)  # Live camera input (UX Play or webcam)

# Check if source opened correctly
if not cap.isOpened():
    print("[ERROR] Could not open video source.")
    sys.exit()

print(f"[INFO] Running detection on {'test video' if source_mode == 'test' else 'live feed'}...")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video or feed failed

    # Run YOLO detection
    results = model(frame)
    annotated = results[0].plot()  # Draw results

    # Display result
    cv2.imshow("Pineapple Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Press 'q' to quit

# Cleanup
cap.release()
cv2.destroyAllWindows()
