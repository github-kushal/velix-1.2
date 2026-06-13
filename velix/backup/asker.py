import speech_recognition as sr
import pyttsx3
import os
import sys
import shutil

# stderr = sys.stderr
# sys.stderr = open(os.devnull, 'w')
# sys.stderr = stderr

engine = pyttsx3.init()
voices = engine.getProperty('voices')
if voices:
    preferred_voice = next((voice for voice in voices if "english" in voice.name.lower()), voices[0])
    engine.setProperty('voice', preferred_voice.id)
engine.setProperty('rate', 180)
# engine.say("Initializing VELIX")


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    print(audio)

    
def takeCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"user said: {query}")

        except Exception as e:
            print("say that again please...")
            return "none"
        return query
    

def clear():
    clear_command = shutil.which("clear")
    if clear_command:
        os.system(clear_command)
    else:
        print("\033c", end="")


speak("Asker module loaded successfully")
