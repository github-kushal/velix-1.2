# ==========================
# VELIX Configuration File
# ==========================

import os
from dotenv import load_dotenv

load_dotenv()

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "VELIX")

WAKE_WORD = os.getenv("WAKE_WORD", "velix")

USER_NAME = os.getenv("USER_NAME", "")

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen3:8b"
)

VOICE_RATE = int(os.getenv("VOICE_RATE", 170))

VOICE_VOLUME = float(os.getenv("VOICE_VOLUME", 1.0))

DEBUG = os.getenv("DEBUG", "True") == "False"

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

EMAIL = os.getenv("EMAIL")

EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")