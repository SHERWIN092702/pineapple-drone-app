import cv2 as cv
import numpy as np
from mss import mss
from ultralytics import YOLO
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import time
import json
from pathlib import Path
import argparse

# === Argument Parsing ===
parser = argparse.ArgumentParser()
parser.add_argument("--source", type=str, default="screen", help="screen or rtmp or youtube")
parser.add_argument("--url", type=str, default="", help="RTMP or YouTube video URL")
args = parser.parse_args()

# Load YOLO model
model = YOLO('C:/DAR/best_ncnn_model')

# === Detection Counters ===
counts_file = Path("C:/DAR/detection_counts.json")
counts = {"ripe": 0, "unripe": 0, "overripe": 0}
with open(counts_file, "w") as f:
    json.dump(counts, f)

# Fuzzy logic setup for hue to ripeness classification
hue = ctrl.Antecedent(np.arange(0, 181, 1), 'hue')
ripeness = ctrl.Consequent(np.arange(0, 3, 1), 'ripeness')

hue['green'] = fuzz.trimf(hue.universe, [30, 55, 80])
hue['yellow'] = fuzz.trimf(hue.universe, [70, 100, 130])
hue['brown'] = fuzz.trimf(hue.universe, [0, 15, 30])

ripeness['unripe'] = fuzz.trimf(ripeness.universe, [0, 0, 1])
ripeness['ripe'] = fuzz.trimf(ripeness.universe, [0, 1, 2])
ripeness['overripe'] = fuzz.trimf(ripeness.universe, [1, 2, 2])

ripeness_ctrl = ctrl.ControlSystem([
    ctrl.Rule(hue['green'], ripeness['unripe']),
    ctrl.Rule(hue['yellow'], ripeness['ripe']),
    ctrl.Rule(hue['brown'], ripeness['overripe'])
])
ripeness_sim = ctrl.ControlSystemSimulation(ripeness_ctrl)

# === Video Source Setup ===
cap = None

if args.source == "rtmp":
    cap = cv.VideoCapture(args.url)

elif args.source == "youtube":
    from pytube import YouTube
    yt = YouTube(args.url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
    cap = cv.VideoCapture(stream.url)

else:
    sct = mss()
    bounding_box = {'top': 180, 'left': 300, 'width': 1280, 'height': 720}

# === Main Detection Loop ===
while True:
    if args.source in ["rtmp", "youtube"]:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Failed to read from stream.")
            break
        scr_img = frame
    else:
        sct_img = sct.grab(bounding_box)
        scr_img = np.array(sct_img)[:, :, :3]

    # Enhance saturation
    hsv_img = cv.cvtColor(scr_img, cv.COLOR_BGR2HSV).astype(np.float32)
    hsv_img[:, :, 1] *= 1.3
    hsv_img[:, :, 1][hsv_img[:, :, 2] > 220] *= 0.9
    hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1], 0, 255)
    scr_img = cv.cvtColor(hsv_img.astype(np.uint8), cv.COLOR_HSV2BGR)

    resized_img = cv.resize(scr_img, (640, 360))
    results = model(resized_img)
    annotated_frame = resized_img.copy()

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cropped = resized_img[y1:y2, x1:x2]
        if cropped.size == 0:
            continue

        crop_small = cv.resize(cropped, (64, 64))
        hsv_crop = cv.cvtColor(crop_small, cv.COLOR_BGR2HSV)
        avg_hue = np.mean(hsv_crop[:, :, 0])

        ripeness_sim.input['hue'] = avg_hue
        ripeness_sim.compute()
        ripeness_level = ripeness_sim.output['ripeness']

        if ripeness_level < 0.5:
            label = "Unripe"
            counts["unripe"] += 1
        elif ripeness_level < 1.5:
            label = "Ripe"
            counts["ripe"] += 1
        else:
            label = "Overripe"
            counts["overripe"] += 1

        cv.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv.putText(annotated_frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        print(f"Pineapple at ({x1},{y1}) avg hue: {avg_hue:.1f} => {label}")

    with open(counts_file, "w") as f:
        json.dump(counts, f)

    cv.imshow('Optimized Detection', annotated_frame)
    time.sleep(0.2)

    if (cv.waitKey(1) & 0xFF) == ord('q'):
        break

cv.destroyAllWindows()
