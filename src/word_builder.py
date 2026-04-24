# src/word_builder.py
# Builds words from confirmed letters

import time
from src.config import HOLD_TIME, SPACE_TIME

last_letter  = ""
last_time    = time.time()
current_word = ""

def update(letter):
    global last_letter, last_time, current_word

    now = time.time()

    if letter:
        if letter == last_letter:
            if now - last_time >= HOLD_TIME:
                if not current_word.endswith(letter):
                    current_word += letter
                    print(f"Letter confirmed: {letter} | Word: {current_word}")
        else:
            last_letter = letter
            last_time   = now
        return current_word, None

    else:
        if now - last_time >= SPACE_TIME and current_word:
            completed    = current_word
            current_word = ""
            last_letter  = ""
            print(f"Word complete: {completed}")
            return "", completed

    return current_word, None

def reset():
    global last_letter, last_time, current_word
    last_letter  = ""
    last_time    = time.time()
    current_word = ""
