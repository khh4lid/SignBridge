# src/interface.py
import cv2
import mediapipe as mp
import numpy as np
import joblib
import sys
import time
from collections import deque
from PIL import ImageFont, ImageDraw, Image
import arabic_reshaper
from bidi.algorithm import get_display
from picamera2 import Picamera2

sys.path.insert(0, '/home/khaled/sign_project')

# ── Load model ────────────────────────────────────
model = joblib.load("model/sign_model.pkl")
le    = joblib.load("model/label_encoder.pkl")
print(f"OK - Model loaded | Letters: {len(le.classes_)}")

# ── Arabic letter mapping ─────────────────────────
ARABIC_MAP = {
    "Ain":"ع", "Al":"ال", "Alef":"أ", "Beh":"ب",
    "Dad":"ض", "Dal":"د", "Feh":"ف", "Ghain":"غ",
    "Hah":"ح", "Heh":"ه", "Jeem":"ج", "Kaf":"ك",
    "Khah":"خ", "Laa":"لا", "Lam":"ل", "Meem":"م",
    "Noon":"ن", "Qaf":"ق", "Reh":"ر", "Sad":"ص",
    "Seen":"س", "Sheen":"ش", "Tah":"ط", "Teh":"ت",
    "Teh_Marbuta":"ة", "Thal":"ذ", "Theh":"ث",
    "Waw":"و", "Yeh":"ي", "Zah":"ظ", "Zain":"ز"
}

# ── Angle features ────────────────────────────────
def compute_angles(landmarks):
    finger_joints = [
        [0,1,2],[1,2,3],[2,3,4],
        [0,5,6],[5,6,7],[6,7,8],
        [0,9,10],[9,10,11],[10,11,12],
        [0,13,14],[13,14,15],[14,15,16],
        [0,17,18],[17,18,19],[18,19,20]
    ]
    angles = []
    for a, b, c in finger_joints:
        v1 = np.array([landmarks[a].x - landmarks[b].x,
                       landmarks[a].y - landmarks[b].y])
        v2 = np.array([landmarks[c].x - landmarks[b].x,
                       landmarks[c].y - landmarks[b].y])
        cosine = np.dot(v1, v2) / (
            np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-6
        )
        angles.append(np.arccos(np.clip(cosine, -1, 1)))
    return angles

# ── Arabic text drawing ───────────────────────────
def draw_text(img, text, pos, size=0.7, color=(255,255,255), bold=False):
    cv2.putText(img, text, pos, cv2.FONT_HERSHEY_SIMPLEX,
                size, color, 2 if bold else 1)

def get_font(size):
    for path in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    return ImageFont.load_default()

def draw_arabic(img, text, pos, font_size=38, color=(255,255,255)):
    if not text:
        return
    reshaped  = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    img_pil   = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw      = ImageDraw.Draw(img_pil)
    font      = get_font(font_size)
    draw.text(pos, bidi_text, font=font,
              fill=(color[2], color[1], color[0]))
    img[:] = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)[:]

def get_arabic_render_width(text, font_size=38):
    reshaped  = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    font      = get_font(font_size)
    dummy     = Image.new("RGB", (1, 1))
    d         = ImageDraw.Draw(dummy)
    bbox      = d.textbbox((0, 0), bidi_text, font=font)
    return bbox[2] - bbox[0]

def draw_arabic_fit(img, text, box_x, box_y, box_w,
                    font_size=38, color=(255,255,255)):
    if not text:
        draw_text(img, "---", (box_x+10, box_y+55), 0.8, (150,150,150))
        return
    display_text = text
    while get_arabic_render_width(display_text, font_size) > box_w - 20:
        display_text = display_text[1:]
    draw_arabic(img, display_text, (box_x+10, box_y+40),
                font_size=font_size, color=color)

# ── TTS ───────────────────────────────────────────
from src.text_to_speech import speak
# ── Camera (picamera2) ────────────────────────────
print("Starting camera...")
cam = Picamera2()
cam.configure(cam.create_video_configuration(
    main={"size": (1280, 720), "format": "RGB888"},
    controls={"FrameRate": 60}
))
cam.start()
time.sleep(1)
try:
    cam.set_controls({"AfMode": 2, "AfSpeed": 1})
    time.sleep(2)
    print("OK - Autofocus enabled")
except:
    pass
print("OK - Camera ready")

# ── MediaPipe ─────────────────────────────────────
mpHands = mp.solutions.hands
hands   = mpHands.Hands(
    model_complexity=0,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils

# ── State ─────────────────────────────────────────
buffer           = deque(maxlen=15)
arabic_word      = ""
arabic_output    = ""
last_added_sign  = ""
last_added_time  = 0
last_output_time = time.time()

HOLD_TIME        = 1.0
CONFIDENCE_MIN   = 0.30
SPACE_SIGN       = "Laa"
OUTPUT_CLEAR_SEC = 5
PANEL_W          = 580

# ── Panel section ─────────────────────────────────
def draw_section(panel, title, content, y, accent, font_size=40):
    bx = 20
    bw = PANEL_W - 40
    bh = 155
    cv2.rectangle(panel, (bx, y),     (bx+bw, y+bh), (30,30,48), -1)
    cv2.rectangle(panel, (bx, y),     (bx+bw, y+bh), accent,      2)
    cv2.rectangle(panel, (bx, y),     (bx+bw, y+35), accent,     -1)
    draw_text(panel, title, (bx+10, y+25), 0.65, (10,10,20), bold=True)
    draw_arabic_fit(panel, content, bx, y, bw, font_size=font_size)

print("\nSignBridge ready! Show your hand | ESC to quit\n")

# ── Main loop ─────────────────────────────────────
while True:
    frame  = cam.capture_array()
    img    = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    img    = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cam_h, cam_w = img.shape[:2]

    # Auto clear output
    if arabic_output and (time.time() - last_output_time) > OUTPUT_CLEAR_SEC:
        arabic_output = ""

    # Panel
    panel    = np.zeros((cam_h, PANEL_W, 3), dtype=np.uint8)
    panel[:] = (18, 18, 28)
    cv2.rectangle(panel, (0,0), (PANEL_W, 75), (40,40,65), -1)
    draw_text(panel, "SIGN BRIDGE", (20,52), 1.4, (100,220,255), bold=True)

    resulte       = hands.process(imgRGB)
    display_sign  = "No hand detected"
    display_color = (80, 80, 80)
    display_ar    = ""
    progress      = 0

    if resulte.multi_hand_landmarks:
        num_hands = len(resulte.multi_hand_landmarks)

        # TWO HANDS = DELETE
        if num_hands == 2:
            display_sign  = "DELETE WORD  (2 hands)"
            display_color = (0, 80, 255)
            for handLm in resulte.multi_hand_landmarks:
                mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)
            now = time.time()
            if last_added_sign != "DELETE":
                last_added_sign = "DELETE"
                last_added_time = now
            elapsed  = now - last_added_time
            progress = min(int((elapsed / HOLD_TIME) * 100), 100)
            if elapsed >= HOLD_TIME:
                arabic_word     = ""
                last_added_sign = ""
                last_added_time = now

        # ONE HAND = predict
        else:
            last_added_sign = "" if last_added_sign == "DELETE" else last_added_sign
            handLm = resulte.multi_hand_landmarks[0]
            mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)

            wrist    = handLm.landmark[0]
            features = []
            for lm in handLm.landmark:
                features.extend([lm.x - wrist.x,
                                  lm.y - wrist.y,
                                  lm.z - wrist.z])
            features.extend(compute_angles(handLm.landmark))
            features = np.array(features).reshape(1, -1)

            pred_enc   = model.predict(features)[0]
            confidence = model.predict_proba(features).max()
            sign       = le.inverse_transform([pred_enc])[0]

            if confidence >= CONFIDENCE_MIN:
                buffer.append(sign)
                smoothed      = max(set(buffer), key=buffer.count)
                display_ar    = ARABIC_MAP.get(smoothed, smoothed)
                display_sign  = f"{smoothed} ({confidence:.0%})"
                display_color = (0, 220, 100)

                now = time.time()
                if smoothed != last_added_sign:
                    last_added_sign = smoothed
                    last_added_time = now

                elapsed  = now - last_added_time
                progress = min(int((elapsed / HOLD_TIME) * 100), 100)

                if elapsed >= HOLD_TIME:
                    if smoothed == SPACE_SIGN:
                        if arabic_word:
                            arabic_output   += arabic_word + " "
                            arabic_word      = ""
                            last_output_time = time.time()
                            speak(arabic_output.strip())
                    else:
                        arabic_word += ARABIC_MAP.get(smoothed, smoothed)
                    last_added_sign = ""
                    last_added_time = now
            else:
                display_sign  = "not recognized ?"
                display_color = (0, 100, 220)
                buffer.clear()

    # Camera overlay
    cv2.rectangle(img, (0,0), (cam_w, 70), (0,0,0), -1)
    draw_text(img, display_sign, (15,48), 1.0, display_color, bold=True)

    if display_ar:
        draw_arabic(img, display_ar,
                    (15, cam_h-110), font_size=90, color=(0,255,150))

    if progress > 0:
        cv2.rectangle(img, (0, cam_h-28), (cam_w, cam_h), (25,25,25), -1)
        fill = (0,200,80) if progress < 100 else (0,255,150)
        cv2.rectangle(img, (0, cam_h-28),
                      (int(cam_w * progress / 100), cam_h), fill, -1)
        label_txt = "Deleting..." if display_sign.startswith("DELETE") else "Holding..."
        draw_text(img, label_txt, (15, cam_h-8), 0.6, (255,255,255))

    # Panel sections
    draw_section(panel, "CURRENT SIGN",  display_sign,  80,  (255,200,80),  font_size=32)
    draw_section(panel, "WORD (Arabic)", arabic_word,   220, (120,255,160), font_size=40)
    draw_section(panel, "OUTPUT (Arabic)", arabic_output, 360, (100,160,255), font_size=34)

    # Controls
    cy = 615
    cv2.rectangle(panel, (20,cy), (PANEL_W-20, cy+95), (28,28,42), -1)
    cv2.rectangle(panel, (20,cy), (PANEL_W-20, cy+95), (60,60,80),  1)
    draw_text(panel, "CONTROLS",                       (30, cy+22), 0.6,  (150,150,150), bold=True)
    draw_text(panel, "Laa (hold 1s) = move to output", (30, cy+46), 0.52, (180,180,180))
    draw_text(panel, "2 Hands (1s) = delete word",     (30, cy+66), 0.52, (180,180,180))
    draw_text(panel, "C = clear  |  ESC = quit",       (30, cy+88), 0.52, (180,180,180))

    combined = np.hstack([img, panel])
    cv2.imshow("Sign Bridge", combined)

    key = cv2.waitKey(5) & 0xff
    if key == 27:
        break
    if key == ord('c') or key == ord('C'):
        arabic_word      = ""
        arabic_output    = ""
        last_output_time = time.time()
        buffer.clear()

cam.stop()
cv2.destroyAllWindows()
print("SignBridge stopped")
