# src/text_to_speech.py
# Arabic TTS — Piper offline (primary) + gTTS online (if internet) + espeak (last resort)

import os
import subprocess
import pygame

from src.config import TTS_LANGUAGE

pygame.mixer.init()

_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PIPER_BINARY = os.environ.get(
    "PIPER_BIN",
    os.path.join(_BASE, "piper", "piper.exe")
    if os.name == "nt"
    else "/usr/local/bin/piper"
)

PIPER_MODEL = os.environ.get(
    "PIPER_MODEL",
    os.path.join(_BASE, "models", "ar_JO-kareem-medium.onnx")
)

PIPER_OUTPUT = os.path.join(os.environ.get("TEMP", "/tmp"), "piper_output.wav")


def speak(text):
    if not text or not text.strip():
        return
    print(f"Speaking: {text}")
    try:
        import requests
        requests.get("https://google.com", timeout=2)
        _speak_online(text)
    except Exception:
        _speak_offline(text)


def _speak_online(text):
    """Online: gTTS — higher quality, needs internet"""
    from gtts import gTTS
    tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
    tts.save("/tmp/output.mp3")
    pygame.mixer.music.load("/tmp/output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    print("OK - gTTS played")


def _speak_offline(text):
    """Offline: Piper — great quality, no internet needed"""
    try:
        cmd = [
            PIPER_BINARY,
            "--model", PIPER_MODEL,
            "--output_file", PIPER_OUTPUT,
        ]
        proc = subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=10,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"Piper error: {proc.stderr.decode()}")

        pygame.mixer.music.load(PIPER_OUTPUT)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        print("OK - Piper played")

    except Exception as e:
        print(f"Piper failed ({e}), falling back to espeak")
        os.system(f'espeak -v ar+f3 -s 130 "{text}"')
        print("OK - espeak played")