import speech_recognition as sr


r = sr.Recognizer()

def listener():
    try:
        with sr.Microphone() as source:
            r.energy_threshold = 300
            r.dynamic_energy_threshold = True
            print("listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            audio = r.recognize_google(audio, language="en-IN")
            print(f"User: \n {audio}")
    except sr.WaitTimeoutError as e:
        print("Sorry, I didn't get you repeat please")
        return "None"

