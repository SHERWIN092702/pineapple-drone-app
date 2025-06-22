import cv2 as cv
import numpy as np
from mss import mss
from ultralytics import YOLO
import skfuzzy as fuzz
import skfuzzy.control as ctrl
import time
import json
from pathlib import Path

# Load YOLO model
model = YOLO('/home/rpi5/Desktop/yolo_object/best_ncnn_model')

# Optimized bounding box - capture only the video feed area (adjust as needed)
bounding_box = {'top': 180, 'left': 300, 'width': 1280, 'height': 720}

sct = mss()

# Fuzzy logic setup for color hue (example: unripe-green, ripe-yellow, overripe-brown)
hue = ctrl.Antecedent(np.arange(0, 181, 1), 'hue')
ripeness = ctrl.Consequent(np.arange(0, 3, 1), 'ripeness')

# Define membership functions for hue
hue['green'] = fuzz.trimf(hue.universe, [30, 55, 80])
hue['yellow'] = fuzz.trimf(hue.universe, [70, 100, 130])
hue['brown'] = fuzz.trimf(hue.universe, [0, 15, 30])

# Ripeness labels
ripeness['unripe'] = fuzz.trimf(ripeness.universe, [0, 0, 1])
ripeness['ripe'] = fuzz.trimf(ripeness.universe, [0, 1, 2])
ripeness['overripe'] = fuzz.trimf(ripeness.universe, [1, 2, 2])

# Rules
rule1 = ctrl.Rule(hue['green'], ripeness['unripe'])
rule2 = ctrl.Rule(hue['yellow'], ripeness['ripe'])
rule3 = ctrl.Rule(hue['brown'], ripeness['overripe'])

# Create fuzzy control system
ripeness_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
ripeness_sim = ctrl.ControlSystemSimulation(ripeness_ctrl)

# === Detection Counters ===
counts_file = Path("/home/rpi5/Desktop/yolo_object/detection_counts.json")
counts = {"ripe": 0, "unripe": 0, "overripe": 0}
with open(counts_file, "w") as f:
    json.dump(counts, f)

while True:
    sct_img = sct.grab(bounding_box)
    scr_img = np.array(sct_img)[:, :, :3]

    # -------- Fine-Tuned Saturation Enhancement Block --------
    hsv_img = cv.cvtColor(scr_img, cv.COLOR_BGR2HSV)
    hsv_float = hsv_img.astype(np.float32)
    saturation_multiplier = 1.3
    hsv_float[:, :, 1] *= saturation_multiplier
    brightness_limit = 220
    hsv_float[:, :, 1][hsv_float[:, :, 2] > brightness_limit] *= 0.9
    hsv_float[:, :, 1] = np.clip(hsv_float[:, :, 1], 0, 255)
    hsv_img = hsv_float.astype(np.uint8)
    scr_img = cv.cvtColor(hsv_img, cv.COLOR_HSV2BGR)
    # ---------------------------------------------------------

    # Resize frame to speed up detection
    resized_img = cv.resize(scr_img, (640, 360))

    # Run YOLO detection on resized image
    results = model(resized_img)
    annotated_frame = resized_img.copy()

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        cropped_pineapple = resized_img[y1:y2, x1:x2]
        if cropped_pineapple.size == 0:
            continue

        crop_small = cv.resize(cropped_pineapple, (64, 64))
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
        cv.putText(annotated_frame, label, (x1, y1 - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        print(f"Pineapple at ({x1},{y1}) avg hue: {avg_hue:.1f} => {label}")

    # Save updated counts to file
    with open(counts_file, "w") as f:
        json.dump(counts, f)

    # Show the result
    cv.imshow('Optimized Detection', annotated_frame)

    # Limit FPS for smoother performance
    time.sleep(0.2)

    if (cv.waitKey(1) & 0xFF) == ord('q'):
        cv.destroyAllWindows()
        break
