import pyaudio
import numpy as np
import wave
import sys


FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 16000
CHUNK = 4096 
OUTPUT_FILENAME = "output.wav"


class Microphone:
    def __init__(self):
        self.audio = pyaudio.PyAudio()

    def start(self):
        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
    )

        print("Listening... (Ctrl+C to stop)")

    def read_chunk(self):
        data = self.stream.read(CHUNK, exception_on_overflow=False)
        audio_data = np.frombuffer(data, dtype=np.int16)
        return audio_data
    
    def record(self, duration=5):
        print(f"Recording for {duration} seconds...")
        self.frames = []
        for _ in range(0, int(RATE / CHUNK * duration)):
            self.frames.append(self.read_chunk())
        print("Recording finished.")
        return np.concatenate(self.frames)
    
    def stop(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

    def output(self):
        if self.frames:
            try:
                wf = wave.open(OUTPUT_FILENAME, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(self.frames))
                wf.close()
                print(f"Saved recording to '{OUTPUT_FILENAME}'")
            except Exception as e:
                print(f"Failed to save file: {e}", file=sys.stderr)

    


if __name__ == "__main__":
    mic = Microphone()
    mic.start()
    audio = mic.record(5)
    print(audio.shape)
    mic.stop()
    mic.output()

    