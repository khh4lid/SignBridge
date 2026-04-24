# src/hand_detector.py
# MediaPipe hand landmark detection

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
    max_num_hands=MP_MAX_HANDS,
    min_detection_confidence=MP_DETECTION,
    min_tracking_confidence=MP_TRACKING
)

def detect_landmarks(frame):
    results = hands.process(frame)
    if not results.multi_hand_landmarks:
        return None
    landmarks = []
    for lm in results.multi_hand_landmarks[0].landmark:
        landmarks.extend([lm.x, lm.y, lm.z])
    return landmarks

def draw_landmarks(frame_bgr, frame_rgb):
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame_bgr, hand,
                mp_hands.HAND_CONNECTIONS
            )
    return frame_bgr, results.multi_hand_landmarks is not None
