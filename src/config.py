# src/config.py
# Camera: Arducam Autofocus IMX519
# Mode 1: 1920x1080 @ 60fps — best balance

# ── Camera ────────────────────────────────────────
CAMERA_WIDTH    = 1920
CAMERA_HEIGHT   = 1080
CAMERA_FPS      = 60
CAMERA_FORMAT   = "RGB888"
CAMERA_AF_MODE  = 2        # Continuous autofocus
CAMERA_AF_SPEED = 1        # Fast

# ── MediaPipe ─────────────────────────────────────
MP_COMPLEXITY   = 0        # 0=fast 1=accurate
MP_MAX_HANDS    = 1
MP_DETECTION    = 0.7
MP_TRACKING     = 0.5
FRAME_SKIP      = 2        # process every 2nd frame

# ── Model ─────────────────────────────────────────
MODEL_PATH      = "model/sign_model.pkl"
ENCODER_PATH    = "model/label_encoder.pkl"
MIN_CONFIDENCE  = 0.75

# ── Word builder ──────────────────────────────────
HOLD_TIME       = 1.2
SPACE_TIME      = 3.0

# ── TTS ───────────────────────────────────────────
TTS_LANGUAGE    = "ar"
