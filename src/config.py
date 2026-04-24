# src/config.py

# ── Camera ────────────────────────────────────────
CAMERA_WIDTH    = 1920
CAMERA_HEIGHT   = 1080
CAMERA_FPS      = 60
CAMERA_FORMAT   = "RGB888"
CAMERA_AF_MODE  = 2
CAMERA_AF_SPEED = 1

# ── MediaPipe ─────────────────────────────────────
MP_COMPLEXITY   = 0
MP_MAX_HANDS    = 1
MP_DETECTION    = 0.75
MP_TRACKING     = 0.5
FRAME_SKIP      = 2

# ── Model ─────────────────────────────────────────
MODEL_PATH      = "model/sign_model.pkl"       # ← الاسم الصح
ENCODER_PATH    = "model/label_encoder.pkl"
MIN_CONFIDENCE  = 0.75

# ── Word Builder ──────────────────────────────────
HOLD_TIME       = 1.2
SPACE_TIME      = 3.0

# ── TTS ───────────────────────────────────────────
TTS_LANGUAGE    = "ar"
