import pyttsx3
from docs import config

engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
print(f"voices are: {voices}")
engine.setProperty("voice", voices[1].id)
engine.setProperty("volume", config.VOICE_VOLUME)
engine.setProperty("rate", config.VOICE_RATE)


def speak(query):
    engine.say(query)
    engine.runAndWait()

# speak("Hello, this is velix speaking")