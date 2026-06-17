from .microphone import Microphone
from .transcriber import Transcriber
import time

def listen():
    mic = Microphone()
    whisper = Transcriber()

    mic.start()

    # start = time.perf_counter()
    audio = mic.record(duration=5)
    # print(f"recording: {time.perf_counter() - start}")

    # start = time.perf_counter()
    text = whisper.transcribe(audio)
    # print(f"transcription: {time.perf_counter() - start}")

    print(f"User:{text}")

    mic.stop()

listen()