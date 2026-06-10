def load_environment():

    from dotenv import load_dotenv
    import os

    load_dotenv(dotenv_path="docs\.env")

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

    DEBUG = os.getenv("DEBUG", "True") == "True"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    print(ASSISTANT_NAME, WAKE_WORD, USER_NAME, OLLAMA_HOST, OLLAMA_MODEL, VOICE_RATE, VOICE_VOLUME, DEBUG, LOG_LEVEL)

load_environment()