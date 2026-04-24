# src/predictor.py
# Predicts Arabic letter from hand landmarks

import joblib
import numpy as np
from src.config import MODEL_PATH, ENCODER_PATH, MIN_CONFIDENCE

print("Loading AI model...")
model   = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
print(f"OK - Model loaded | Letters: {len(encoder.classes_)}")

def predict_letter(landmarks):
    if not landmarks or len(landmarks) != 63:
        return None, 0.0

    proba      = model.predict_proba([landmarks])[0]
    confidence = float(np.max(proba))

    if confidence < MIN_CONFIDENCE:
        return None, confidence

    number = int(np.argmax(proba))
    letter = encoder.inverse_transform([number])[0]
    return letter, confidence
