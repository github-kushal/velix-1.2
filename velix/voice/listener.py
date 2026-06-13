# import speech_recognition as sr

# r = sr.Recognizer()

# def listener():
#     try:
#         with sr.Microphone() as source:
#             r.energy_threshold = 300
#             r.dynamic_energy_threshold = True
#             print("listening...")
#             r.adjust_for_ambient_noise(source)
#             audio = r.listen(source, timeout=5, phrase_time_limit=5)
#             audio = r.recognize_google(audio, language="en-IN")
#             print(f"User: \n {audio}")
#             return audio
#     except sr.WaitTimeoutError as e:
#         print("Sorry, I didn't get you repeat please")
#         return "None"
#     except sr.UnknownValueError as ve:
#         print("Sorry, I didn't get that")
#         return None

# # query = listener()

# # print(query)


import pyaudio
import numpy as np

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024


def on_stream():
    audio = pyaudio.PyAudio()

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Listening... (Ctrl+C to stop)")

    try:
       frames = []

       while stream.is_active():
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

            audio_bytes = b"".join(frames)
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16)

    except KeyboardInterrupt:
            print("\nStopped.")

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


if __name__ == "__main__":
    on_stream()