from picamera2 import Picamera2
import time
from src.config import CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS, CAMERA_FORMAT

def get_camera():
    cam = Picamera2()
    config = cam.create_video_configuration(
        main={
            "size":   (CAMERA_WIDTH, CAMERA_HEIGHT),
            "format": CAMERA_FORMAT
        },
        controls={"FrameRate": CAMERA_FPS}
    )
    cam.configure(config)
    cam.start()
    time.sleep(0.5)
    print(f"OK - Camera: {CAMERA_WIDTH}x{CAMERA_HEIGHT} @ {CAMERA_FPS}fps")
    return cam

def get_frame(cam):
    return cam.capture_array()

def release_camera(cam):
    cam.stop()
