# src/text_to_speech.py
# Arabic TTS — gTTS online + espeak offline fallback

import os
import pygame
from src.config import TTS_LANGUAGE

pygame.mixer.init()

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
    from gtts import gTTS
    tts = gTTS(text=text, lang=TTS_LANGUAGE, slow=False)
    tts.save("/tmp/output.mp3")
    pygame.mixer.music.load("/tmp/output.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    print("OK - gTTS played")

def _speak_offline(text):
    os.system(f'espeak -v ar+f3 -s 130 "{text}"')
    print("OK - espeak played")
