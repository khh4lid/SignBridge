import cv2

print("Testing camera backends...")

# جرّب كل backend
backends = [
    (cv2.CAP_V4L2,  "V4L2"),
    (cv2.CAP_GSTREAMER, "GStreamer"),
    (0, "Default"),
]

for backend, name in backends:
    cap = cv2.VideoCapture(0, backend)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"SUCCESS with {name}!")
            print(f"Resolution: {frame.shape[1]}x{frame.shape[0]}")
            cap.release()
            break
        else:
            print(f"FAIL read with {name}")
        cap.release()
    else:
        print(f"FAIL open with {name}")
