# src/config.py
# Camera settings based on IMX519 sensor modes

# ── Best for real-time AI processing ──
CAMERA_WIDTH    = 1280
CAMERA_HEIGHT   = 720
CAMERA_FPS      = 80        # Mode 0 — fastest
CAMERA_FORMAT   = "RGB888"

# ── Alternative — higher quality ──
# CAMERA_WIDTH  = 1920
# CAMERA_HEIGHT = 1080
# CAMERA_FPS    = 60        # Mode 1

# ── Model settings ──
MODEL_PATH      = "model/sign_model.pkl"
ENCODER_PATH    = "model/label_encoder.pkl"
MIN_CONFIDENCE  = 0.75

# ── Word builder ──
HOLD_TIME       = 1.2
SPACE_TIME      = 3.0

# ── TTS ──
TTS_LANGUAGE    = "ar"
