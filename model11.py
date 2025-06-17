import cv2
from ultralytics import YOLO

# === Load your trained model ===
model = YOLO("best.pt")  # Ensure best.pt is in the same folder

# === Load the test video ===
video_path = "test_video.mp4"  # Replace with your actual filename if different
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("[ERROR] Could not open video file.")
    exit()

print("[INFO] Running detection on test video...")

while True:
    ret, frame = cap.read()
    if not ret:
        break  # End of video

    # Run detection
    results = model(frame)
    annotated = results[0].plot()

    # Show result
    cv2.imshow("Pineapple Detection (Test Video)", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
