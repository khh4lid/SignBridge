# src/hand_detector.py
import mediapipe as mp
import cv2
from src.config import (
    MP_COMPLEXITY, MP_MAX_HANDS,
    MP_DETECTION, MP_TRACKING
)

mp_hands = mp.solutions.hands
mp_draw  = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    model_complexity=MP_COMPLEXITY,
    max_num_hands=2,               # ← 2 hands للـ delete feature
    min_detection_confidence=MP_DETECTION,
    min_tracking_confidence=MP_TRACKING
)

def detect(frame):
    """Returns (hand_landmarks, num_hands, annotated_frame_bgr)"""
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    results   = hands.process(frame)

    num_hands = 0
    hand_lm   = None

    if results.multi_hand_landmarks:
        num_hands = len(results.multi_hand_landmarks)
        hand_lm   = results.multi_hand_landmarks[0]

        for lm in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame_bgr, lm,
                mp_hands.HAND_CONNECTIONS
            )

    return hand_lm, num_hands, frame_bgr
