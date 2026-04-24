# tests/test_pipeline.py
# Tests full pipeline end-to-end with timing
# Run: python3 tests/test_pipeline.py

import sys
sys.path.insert(0, '/home/khaled/sign_project')

import time
import cv2
import numpy as np

print("=" * 50)
print("  SignBridge — Full Pipeline Test")
print("=" * 50)

results_log = []

def check(label, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {label} {detail}")
    results_log.append((label, passed))

# ── Step 1: Config ────────────────────────────────
print("\n[1] Config...")
try:
    from src.config import (
        CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS,
        MODEL_PATH, ENCODER_PATH, MIN_CONFIDENCE,
        HOLD_TIME, SPACE_TIME, TTS_LANGUAGE
    )
    check("Config loads", True,
          f"| {CAMERA_WIDTH}x{CAMERA_HEIGHT} @ {CAMERA_FPS}fps")
    check("Model path set", MODEL_PATH != "",
          f"| {MODEL_PATH}")
    check("Confidence valid", 0 < MIN_CONFIDENCE < 1,
          f"| {MIN_CONFIDENCE}")
except Exception as e:
    check("Config loads", False, str(e))
    exit()

# ── Step 2: Model ─────────────────────────────────
print("\n[2] Model...")
try:
    import joblib
    t      = time.time()
    model  = joblib.load(MODEL_PATH)
    enc    = joblib.load(ENCODER_PATH)
    load_t = (time.time() - t) * 1000
    check("Model loads", True, f"| {load_t:.0f}ms")
    check("Encoder loads", True, f"| {len(enc.classes_)} letters")
    check("Letters count", len(enc.classes_) >= 20,
          f"| {list(enc.classes_)}")
except Exception as e:
    check("Model loads", False, str(e))
    exit()

# ── Step 3: Prediction speed ──────────────────────
print("\n[3] Prediction speed...")
dummy = [0.5] * 63
t = time.time()
for _ in range(100):
    model.predict([dummy])
ms = (time.time() - t) / 100 * 1000
check("Prediction < 50ms",  ms < 50,   f"| {ms:.1f}ms")
check("Prediction < 100ms", ms < 100,  f"| {ms:.1f}ms")

# ── Step 4: MediaPipe ─────────────────────────────
print("\n[4] MediaPipe...")
try:
    import mediapipe as mp
    hands = mp.solutions.hands.Hands(
        model_complexity=0,
        max_num_hands=1
    )
    check("MediaPipe loads", True)
except Exception as e:
    check("MediaPipe loads", False, str(e))

# ── Step 5: Camera ────────────────────────────────
print("\n[5] Camera...")
try:
    from picamera2 import Picamera2
    cam = Picamera2()
    cam.configure(cam.create_video_configuration(
        main={"size": (CAMERA_WIDTH, CAMERA_HEIGHT),
              "format": "RGB888"},
        controls={"FrameRate": CAMERA_FPS}
    ))
    cam.start()
    time.sleep(1)

    t     = time.time()
    frame = cam.capture_array()
    cap_t = (time.time() - t) * 1000

    check("Camera opens",   True)
    check("Frame captured", frame is not None,
          f"| {frame.shape}")
    check("Capture < 50ms", cap_t < 50,
          f"| {cap_t:.1f}ms")

    # FPS test
    frames = 0
    start  = time.time()
    while time.time() - start < 2:
        cam.capture_array()
        frames += 1
    fps = frames / 2
    check("FPS >= 30", fps >= 30, f"| {fps:.0f}fps")

except Exception as e:
    check("Camera opens", False, str(e))
    cam = None

# ── Step 6: Full pipeline timing ──────────────────
print("\n[6] Full pipeline timing...")
if cam:
    try:
        frame = cam.capture_array()

        t       = time.time()
        rgb     = frame
        results = hands.process(rgb)
        detect_t = (time.time() - t) * 1000

        landmarks = []
        if results.multi_hand_landmarks:
            for lm in results.multi_hand_landmarks[0].landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            t         = time.time()
            pred      = model.predict([landmarks])[0]
            letter    = enc.inverse_transform([pred])[0]
            predict_t = (time.time() - t) * 1000
        else:
            landmarks = dummy
            predict_t = ms

        total_t = cap_t + detect_t + predict_t

        check("Detection < 100ms",  detect_t < 100,
              f"| {detect_t:.1f}ms")
        check("Prediction < 50ms",  predict_t < 50,
              f"| {predict_t:.1f}ms")
        check("Total < 1000ms",     total_t < 1000,
              f"| {total_t:.0f}ms")

        print(f"\n  Timing breakdown:")
        print(f"  Camera capture : {cap_t:.1f}ms")
        print(f"  MediaPipe      : {detect_t:.1f}ms")
        print(f"  Model predict  : {predict_t:.1f}ms")
        print(f"  Total          : {total_t:.0f}ms")

        cam.stop()

    except Exception as e:
        check("Pipeline timing", False, str(e))

# ── Step 7: Word builder ──────────────────────────
print("\n[7] Word builder...")
try:
    from src.word_builder import update, reset
    reset()
    word, completed = update("أ")
    check("WordBuilder works", True)
    reset()
except Exception as e:
    check("WordBuilder works", False, str(e))

# ── Step 8: TTS ───────────────────────────────────
print("\n[8] TTS...")
try:
    import subprocess
    result = subprocess.run(
        ["which", "espeak"],
        capture_output=True
    )
    check("espeak available",
          result.returncode == 0)
except Exception as e:
    check("espeak available", False, str(e))

# ── Summary ───────────────────────────────────────
passed = sum(1 for _, p in results_log if p)
total  = len(results_log)

print("\n" + "=" * 50)
print(f"  Results: {passed}/{total} passed")

if passed == total:
    print("  STATUS: ALL TESTS PASSED")
    print("  SignBridge is ready to run!")
elif passed >= total * 0.8:
    print("  STATUS: MOSTLY PASSING")
    print("  Minor issues — check failed tests")
else:
    print("  STATUS: NEEDS ATTENTION")
    print("  Fix failed tests before running")

print("=" * 50)
