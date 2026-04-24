# tests/test_camera.py
# Purpose: Test Arducam camera using picamera2
# Run: python3 tests/test_camera.py

from picamera2 import Picamera2
import cv2
import time
import numpy as np

print("=" * 45)
print("  SignBridge — Camera Test")
print("=" * 45)

# ── Open camera ───────────────────────────────────
print("\n[1] Opening camera...")
try:
    cam = Picamera2()
    config = cam.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    cam.configure(config)
    cam.start()
    time.sleep(1)
    print("OK - Camera opened successfully")
except Exception as e:
    print(f"FAIL - {e}")
    exit()

# ── Capture frame ─────────────────────────────────
print("\n[2] Capturing frame...")
try:
    frame = cam.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    print(f"OK - Frame captured")
    print(f"OK - Resolution : {frame.shape[1]}x{frame.shape[0]}")
    print(f"OK - Channels   : {frame.shape[2]}")
except Exception as e:
    print(f"FAIL - {e}")
    cam.stop()
    exit()

# ── FPS test ──────────────────────────────────────
print("\n[3] Testing FPS for 3 seconds...")
frames = 0
start  = time.time()

while time.time() - start < 3:
    frame = cam.capture_array()
    if frame is not None:
        frames += 1

fps = frames / 3
print(f"OK - FPS: {fps:.1f}")

# ── Save test image ───────────────────────────────
print("\n[4] Saving test image...")
try:
    frame = cam.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    cv2.imwrite("tests/camera_test_output.jpg", frame)
    print("OK - Saved: tests/camera_test_output.jpg")
except Exception as e:
    print(f"FAIL - {e}")

# ── Result ────────────────────────────────────────
print("\n" + "=" * 45)
print("  RESULTS")
print("=" * 45)
print(f"  Camera     : Arducam Autofocus")
print(f"  Resolution : {frame.shape[1]}x{frame.shape[0]}")
print(f"  FPS        : {fps:.1f}")

if fps >= 20:
    print("  Status     : EXCELLENT")
elif fps >= 15:
    print("  Status     : GOOD")
elif fps >= 10:
    print("  Status     : OK")
else:
    print("  Status     : SLOW")

cam.stop()
print("=" * 45)
