import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pyttsx3
import docs.config as config

engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("volume", config.VOICE_VOLUME)
engine.setProperty("rate", config.VOICE_RATE)


def speak(query):
    engine.say(query)
    engine.runAndWait()

# speak("Hello, this is velix speaking")