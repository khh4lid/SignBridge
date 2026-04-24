# tests/test_model.py
import sys
sys.path.insert(0, '/home/khaled/sign_project')

import os, time, joblib, numpy as np
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
    print(f"OK - Letters : {len(encoder.classes_)}")
    print(f"OK - Features: {model.n_features_in_}")
except Exception as e:
    print(f"FAIL - {e}")
    exit()

# ── Speed test ────────────────────────────────────
print("\n[2] Speed test...")
dummy = [0.5] * 78
start = time.time()
for _ in range(100):
    model.predict([dummy])
ms = (time.time() - start) / 100 * 1000
print(f"OK - Speed: {ms:.2f}ms per frame")
print(f"OK - Status: {'EXCELLENT' if ms < 50 else 'GOOD'}")

# ── Confidence test ───────────────────────────────
print("\n[3] Confidence test...")
proba = model.predict_proba([dummy])[0]
print(f"OK - Confidence works: {np.max(proba):.2f}")

# ── Image test ────────────────────────────────────
print("\n[4] Testing with images...")

mp_hands = mp.solutions.hands
hands    = mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5
)

images_dir = "tests/images"
image_files = [
    f for f in os.listdir(images_dir)
    if f.endswith('.jpg') or f.endswith('.png')
]

if not image_files:
    print("No images found")
else:
    print(f"Found {len(image_files)} images\n")
    detected    = 0
    no_hand     = 0

    for img_file in image_files:
        img_path = os.path.join(images_dir, img_file)
        img      = cv2.imread(img_path)

        if img is None:
            print(f"  SKIP  - cannot read {img_file}")
            continue

        rgb     = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if not results.multi_hand_landmarks:
            print(f"  NO HAND - {img_file}")
            no_hand += 1
            continue

        # Extract features
        from src.predictor import extract_features
        hand_lm  = results.multi_hand_landmarks[0]

        # Wrap landmarks for extract_features
        class FakeLandmarks:
            def __init__(self, lms):
                self.landmark = lms
        fake     = FakeLandmarks(hand_lm.landmark)
        features = extract_features(fake)
        features = np.array(features).reshape(1, -1)

        proba      = model.predict_proba(features)[0]
        confidence = np.max(proba)
        pred_enc   = model.predict(features)[0]
        predicted  = encoder.inverse_transform([pred_enc])[0]

        print(f"  DETECTED - {img_file}")
        print(f"           -> {predicted} ({confidence:.0%})")
        detected += 1

    print(f"\n  Images tested : {len(image_files)}")
    print(f"  Hand detected : {detected}")
    print(f"  No hand       : {no_hand}")

print("\n" + "=" * 50)
print("  Model Test Complete")
print("=" * 50)
