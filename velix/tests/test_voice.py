from velix.voice.microphone import listener
from voice.speaker import speak # or with aliases like you have

query = listener().lower()
speak(query)

