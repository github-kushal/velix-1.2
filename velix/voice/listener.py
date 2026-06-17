import speech_recognition as sr
import pyttsx3

class Listener:
    def speak(text):
        """Convert text to speech using pyttsx3."""
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()

    def listen():
        """Listen to microphone input and return recognized text."""
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... ")
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("Recognizing speech...")
                text = recognizer.recognize_google(audio)
                return text
            except sr.WaitTimeoutError:
                return "No speech detected."
            except sr.UnknownValueError:
                return "Sorry, I could not understand the audio."
            except sr.RequestError:
                return "Speech recognition service is unavailable."

if __name__ == "__main__":
    recognized_text = Listener.listen()
    print(f"You said: {recognized_text}")
    Listener.speak(f"You said: {recognized_text}")
