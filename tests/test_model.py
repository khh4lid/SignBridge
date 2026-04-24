# tests/test_model.py
# Tests the AI model against real hand sign images
# Run: python3 tests/test_model.py

import sys
sys.path.insert(0, '/home/khaled/sign_project')

import os
import time
import joblib
import numpy as np
import mediapipe as mp
import cv2

print("=" * 50)
print("  SignBridge — Model Test")
print("=" * 50)

# ── Load model ────────────────────────────────────
print("\n[1] Loading model...")
try:
    model   = joblib.load("model/sign_model.pkl")
    encoder = joblib.load("model/label_encoder.pkl")
    print(f"OK - Model loaded")
    print(f"OK - Letters: {len(encoder.classes_)}")
    print(f"OK - Classes: {list(encoder.classes_)}")
except Exception as e:
    print(f"FAIL - {e}")
    exit()

# ── Speed test ────────────────────────────────────
print("\n[2] Speed test...")
dummy = [0.5] * 63
start = time.time()
for _ in range(100):
    model.predict([dummy])
ms = (time.time() - start) / 100 * 1000
print(f"OK - Prediction speed: {ms:.2f}ms per frame")

if ms < 50:
    print("OK - Speed: EXCELLENT")
elif ms < 100:
    print("OK - Speed: GOOD")
else:
    print("SLOW - Speed: needs optimization")

# ── Confidence test ───────────────────────────────
print("\n[3] Confidence test...")
proba = model.predict_proba([dummy])[0]
print(f"OK - Confidence output works")
print(f"OK - Max confidence: {np.max(proba):.2f}")

# ── Image test ────────────────────────────────────
print("\n[4] Testing with real images...")

mp_hands = mp.solutions.hands
hands    = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.7
)

images_dir = "tests/images"
if not os.path.exists(images_dir):
    print("No images folder found — skipping image test")
else:
    image_files = [f for f in os.listdir(images_dir)
                   if f.endswith('.jpg') or f.endswith('.png')]

    if not image_files:
        print("No images found in tests/images/")
    else:
        passed = 0
        failed = 0
        no_hand = 0

        for img_file in image_files:
            img_path = os.path.join(images_dir, img_file)
            expected = os.path.splitext(img_file)[0]

            img     = cv2.imread(img_path)
            rgb     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if not results.multi_hand_landmarks:
                print(f"  NO HAND  - {img_file}")
                no_hand += 1
                continue

            landmarks = []
            for lm in results.multi_hand_landmarks[0].landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            proba      = model.predict_proba([landmarks])[0]
            confidence = np.max(proba)
            predicted  = encoder.inverse_transform([np.argmax(proba)])[0]

            if predicted == expected:
                print(f"  PASS  {img_file} -> {predicted} ({confidence:.0%})")
                passed += 1
            else:
                print(f"  FAIL  {img_file} -> got {predicted} expected {expected} ({confidence:.0%})")
                failed += 1

        print(f"\n  Passed  : {passed}")
        print(f"  Failed  : {failed}")
        print(f"  No hand : {no_hand}")
        if passed + failed > 0:
            rate = passed / (passed + failed) * 100
            print(f"  Accuracy: {rate:.1f}%")

print("\n" + "=" * 50)
print("  Model Test Complete")
print("=" * 50)
