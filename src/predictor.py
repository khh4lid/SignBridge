# src/predictor.py
import joblib
import numpy as np
from src.config import MODEL_PATH, ENCODER_PATH, MIN_CONFIDENCE

print("Loading AI model...")
model   = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
print(f"OK - Model loaded | Letters: {len(encoder.classes_)}")
print(f"OK - Features expected: {model.n_features_in_}")

# Arabic letter mapping
ARABIC_MAP = {
    "Ain":         "ع",  "Al":          "ال", "Alef":       "أ",
    "Beh":         "ب",  "Dad":         "ض",  "Dal":        "د",
    "Feh":         "ف",  "Ghain":       "غ",  "Hah":        "ح",
    "Heh":         "ه",  "Jeem":        "ج",  "Kaf":        "ك",
    "Khah":        "خ",  "Laa":         "لا", "Lam":        "ل",
    "Meem":        "م",  "Noon":        "ن",  "Qaf":        "ق",
    "Reh":         "ر",  "Sad":         "ص",  "Seen":       "س",
    "Sheen":       "ش",  "Tah":         "ط",  "Teh":        "ت",
    "Teh_Marbuta": "ة",  "Thal":        "ذ",  "Theh":       "ث",
    "Waw":         "و",  "Yeh":         "ي",  "Zah":        "ظ",
    "Zain":        "ز"
}

def compute_angles(landmarks_obj):
    """Compute 15 joint angles — same as training"""
    finger_joints = [
        [0,  1,  2], [1,  2,  3], [2,  3,  4],
        [0,  5,  6], [5,  6,  7], [6,  7,  8],
        [0,  9, 10], [9, 10, 11], [10, 11, 12],
        [0, 13, 14], [13, 14, 15], [14, 15, 16],
        [0, 17, 18], [17, 18, 19], [18, 19, 20]
    ]
    angles = []
    for a, b, c in finger_joints:
        v1 = np.array([landmarks_obj[a].x - landmarks_obj[b].x,
                       landmarks_obj[a].y - landmarks_obj[b].y])
        v2 = np.array([landmarks_obj[c].x - landmarks_obj[b].x,
                       landmarks_obj[c].y - landmarks_obj[b].y])
        cosine = np.dot(v1, v2) / (
            np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6
        )
        angles.append(np.arccos(np.clip(cosine, -1, 1)))
    return angles

def extract_features(hand_landmarks):
    """Extract 78 features — 63 positions + 15 angles"""
    wrist    = hand_landmarks.landmark[0]
    features = []

    # 63 — normalized positions relative to wrist
    for lm in hand_landmarks.landmark:
        features.extend([
            lm.x - wrist.x,
            lm.y - wrist.y,
            lm.z - wrist.z
        ])

    # 15 — joint angles
    features.extend(compute_angles(hand_landmarks.landmark))

    return features  # total: 78

def predict_letter(hand_landmarks):
    """Takes MediaPipe hand_landmarks object — returns letter, confidence"""
    if hand_landmarks is None:
        return None, 0.0

    features   = extract_features(hand_landmarks)
    features   = np.array(features).reshape(1, -1)
    confidence = float(model.predict_proba(features).max())

    if confidence < MIN_CONFIDENCE:
        return None, confidence

    pred_enc = model.predict(features)[0]
    label    = encoder.inverse_transform([pred_enc])[0]
    letter   = ARABIC_MAP.get(label, label)
    return letter, confidence

def predict_raw(hand_landmarks):
    """Returns English label + Arabic letter + confidence"""
    if hand_landmarks is None:
        return None, None, 0.0

    features   = extract_features(hand_landmarks)
    features   = np.array(features).reshape(1, -1)
    confidence = float(model.predict_proba(features).max())
    pred_enc   = model.predict(features)[0]
    label      = encoder.inverse_transform([pred_enc])[0]
    arabic     = ARABIC_MAP.get(label, label)
    return label, arabic, confidence
