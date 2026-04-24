# src/main.py
# SignBridge — Main Controller
# Run: python3 src/main.py

import cv2
import time
import sys
import os
sys.path.insert(0, '/home/khaled/sign_project')

from src.camera          import get_camera, get_frame, release_camera
from src.hand_detector   import detect_landmarks, draw_landmarks
from src.predictor       import predict_letter
from src.word_builder    import update, reset
from src.text_to_speech  import speak
from src.config          import FRAME_SKIP

print("=" * 45)
print("  SignBridge — Starting")
print("=" * 45)

# ── Init ──────────────────────────────────────────
cam         = get_camera()
fps_start   = time.time()
fps_count   = 0
fps_display = 0
skip        = 0
letter      = None
confidence  = 0.0
word        = ""

print("\nReady — show your hand | Press Q to quit\n")

while True:
    frame     = get_frame(cam)
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    skip += 1
    if skip % FRAME_SKIP == 0:
        landmarks        = detect_landmarks(frame)
        letter, confidence = predict_letter(landmarks)
        frame_bgr, hand_found = draw_landmarks(frame_bgr, frame)

    # Word builder
    word, completed = update(letter)
    if completed:
        speak(completed)
        reset()

    # ── FPS ───────────────────────────────────────
    fps_count += 1
    if time.time() - fps_start >= 1.0:
        fps_display = fps_count
        fps_count   = 0
        fps_start   = time.time()

    # ── UI ────────────────────────────────────────
    cv2.putText(frame_bgr, f"FPS: {fps_display}",
        (30, 45), cv2.FONT_HERSHEY_SIMPLEX,
        1.2, (255, 255, 0), 2)

    if letter:
        cv2.putText(frame_bgr, f"Letter: {letter}",
            (30, 105), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 255, 0), 3)
        cv2.putText(frame_bgr, f"Conf: {confidence:.0%}",
            (30, 155), cv2.FONT_HERSHEY_SIMPLEX,
            1.0, (0, 255, 0), 2)
    else:
        cv2.putText(frame_bgr, "NO HAND",
            (30, 105), cv2.FONT_HERSHEY_SIMPLEX,
            2.0, (0, 0, 255), 3)

    cv2.putText(frame_bgr, f"Word: {word}",
        (30, 220), cv2.FONT_HERSHEY_SIMPLEX,
        1.5, (255, 255, 255), 2)

    cv2.imshow("SignBridge", frame_bgr)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

release_camera(cam)
cv2.destroyAllWindows()
print("SignBridge stopped")
