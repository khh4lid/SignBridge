# src/camera.py
from picamera2 import Picamera2
import time
from src.config import (
    CAMERA_WIDTH, CAMERA_HEIGHT,
    CAMERA_FPS, CAMERA_FORMAT,
    CAMERA_AF_MODE, CAMERA_AF_SPEED
)

def get_camera():
    cam = Picamera2()
    cam.configure(cam.create_video_configuration(
        main={
            "size":   (CAMERA_WIDTH, CAMERA_HEIGHT),
            "format": CAMERA_FORMAT
        },
        controls={"FrameRate": CAMERA_FPS}
    ))
    cam.start()
    time.sleep(1)

    # Autofocus
    try:
        cam.set_controls({
            "AfMode":  CAMERA_AF_MODE,
            "AfSpeed": CAMERA_AF_SPEED
        })
        time.sleep(2)
        print("OK - Autofocus enabled")
    except:
        print("AF not available")

    print(f"OK - {CAMERA_WIDTH}x{CAMERA_HEIGHT} @ {CAMERA_FPS}fps")
    return cam

def get_frame(cam):
    return cam.capture_array()

def release_camera(cam):
    cam.stop()
    print("Camera stopped")
