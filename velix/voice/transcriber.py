from faster_whisper import WhisperModel



class Transcriber:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.model = WhisperModel(self.model_size, device=self.device, compute_type=self.compute_type)

    def transcribe(self, audio):
        self.segments, self.info = self.model.transcribe(audio, beam_size=1, vad_filter=True)

        self.transcription = " ".join(self.segment.text for self.segment in self.segments)

        # print(f"Detected language: {self.info.language} (probability: {self.info.language_probability:.2f})")

        return self.transcription