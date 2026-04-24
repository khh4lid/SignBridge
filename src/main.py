# src/main.py
import cv2
import time
import sys
sys.path.insert(0, '/home/khaled/sign_project')

from picamera2             import Picamera2
from src.camera            import get_camera, get_frame, release_camera
from src.hand_detector     import detect
from src.predictor         import predict_raw
from src.word_builder      import update, reset
from src.text_to_speech    import speak
from src.config            import FRAME_SKIP, CAMERA_WIDTH, CAMERA_HEIGHT

print("=" * 45)
print("  SignBridge — Starting")
print("=" * 45)

cam         = get_camera()
fps_start   = time.time()
fps_count   = 0
fps_display = 0
skip        = 0
label       = None
arabic      = None
confidence  = 0.0
word        = ""

print("Ready — show your hand | Press Q to quit\n")

while True:
    frame     = get_frame(cam)
    hand_lm, num_hands, frame_bgr = detect(frame)

    skip += 1
    if skip % FRAME_SKIP == 0:

        # DELETE — رفع يدين
        if num_hands == 2:
            label      = "DELETE"
            arabic     = "حذف"
            confidence = 1.0

        elif num_hands == 1:
            label, arabic, confidence = predict_raw(hand_lm)

        else:
            label      = None
            arabic     = None
            confidence = 0.0

    # Word builder
    word, completed = update(arabic if arabic != "حذف" else None)
    if completed:
        speak(completed)
        reset()

    # FPS
    fps_count += 1
    if time.time() - fps_start >= 1.0:
        fps_display = fps_count
        fps_count   = 0
        fps_start   = time.time()

    # ── UI ────────────────────────────────────────
    cv2.putText(frame_bgr, f"FPS: {fps_display}",
        (30, 45), cv2.FONT_HERSHEY_SIMPLEX,
        1.2, (255, 255, 0), 2)

    if label:
        cv2.putText(frame_bgr, f"{label} ({confidence:.0%})",
            (30, 105), cv2.FONT_HERSHEY_SIMPLEX,
            1.8, (0, 255, 0), 3)
    else:
        cv2.putText(frame_bgr, "NO HAND",
            (30, 105), cv2.FONT_HERSHEY_SIMPLEX,
            1.8, (0, 0, 255), 3)

    if arabic:
        cv2.putText(frame_bgr, f"Arabic: {arabic}",
            (30, 165), cv2.FONT_HERSHEY_SIMPLEX,
            1.5, (0, 255, 150), 2)

    cv2.putText(frame_bgr, f"Word: {word}",
        (30, 230), cv2.FONT_HERSHEY_SIMPLEX,
        1.5, (255, 255, 255), 2)

    cv2.imshow("SignBridge", frame_bgr)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break
    if key == ord('c'):
        reset()
        word = ""

release_camera(cam)
cv2.destroyAllWindows()
print("SignBridge stopped")
