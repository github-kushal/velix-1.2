# import speech_recognition as sr #pip install speechRecognition
import speech_recognition as sr
import datetime
import wikipedia #pip install wikipedia
import webbrowser
import os
import operator
import subprocess
import sys
from requests import get
import time
import smtplib
from asker import *
import geocoder
import requests
from bs4 import BeautifulSoup
import pygame
import time
import threading
from pywikihow import search_wikihow
from haversine import haversine
import pyautogui
import serial
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
import json
import numpy as np
from PIL import Image
import pyttsx3

pyautogui.FAILSAFE = False
        
# Global variables
user_name = "User"  # Default user name

def read_password():
    if os.path.exists("password.py"):
        with open("password.py", "r") as file:
            password = file.read().strip()
        return password
    else:
        return None


def write_password(password):
    with open("password.py", "w") as file:
        file.write(password)


def verify_password(user_password, stored_password):
    if user_password == stored_password:
        return True
    else:
        return False

def Face_Recognition():
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()  # Local Binary Patterns Histograms
    except AttributeError:
        speak("cv2.face.LBPHFaceRecognizer_create is not available. Please install opencv-contrib-python.")
        return False
    try:
        recognizer.read('trainer\\trainer.yml')  # Load trained model
    except Exception as e:
        speak("Face recognition model not found. Please run the face enrollment process first.")
        return False
        
    cascadePath = "face Recognizer\\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)  # Initializing haar cascade for object detection

    font = cv2.FONT_HERSHEY_SIMPLEX  # Denotes the font type
    names = ['Kushal', 'Kunal']  # Names, leave first empty because counter starts from 0

    cam = cv2.VideoCapture(0)  # cv2.CAP_DSHOW to remove warning
    cam.set(3, 640)  # Set video Frame Width
    cam.set(4, 480)  # Set video Frame Height

    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    speak("Looking for your face. Please look at the camera.")
    
    face_recognized = False
    user_cancelled = False
    start_time = time.time()
    timeout = 30  # 30 seconds timeout
    
    while time.time() - start_time < timeout:
        ret, img = cam.read()  # Read the frames using the above created object
        if not ret:
            speak("Camera error. Please check your camera connection.")
            speak("Restarting the system")
            restart_program()
            
        converted_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale

        faces = faceCascade.detectMultiScale(
            converted_image,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(int(minW), int(minH)),
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle around face

            id, accuracy = recognizer.predict(converted_image[y:y + h, x:x + w])  # Predict

            if accuracy < 70:  # Increased threshold for better accuracy
                id = names[id]
                accuracy = "  {0}%".format(round(100 - accuracy))
                face_recognized = True
                break
            else:
                id = "unknown"
                accuracy = "  {0}%".format(round(100 - accuracy))

            cv2.putText(img, str(id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, str(accuracy), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # Add text instructions on the image
        cv2.putText(img, "Press ESC to cancel", (10, 30), font, 0.7, (0, 0, 255), 2)

        cv2.imshow('Face Authentication', img)

        k = cv2.waitKey(10) & 0xff  # Check for key presses
        if k == 27:  # ESC key
            user_cancelled = True
            break
            
        if face_recognized:
            break

    cam.release()
    cv2.destroyAllWindows()
    
    if user_cancelled and not face_recognized:
        speak("Face authentication was cancelled by user.")
        return False
    
    return face_recognized

def enroll_face():
    """Function to enroll a new face for authentication"""
    speak("Starting face enrollment process. I'll take multiple photos of your face.")
    speak("Please look at the camera and move your head slightly to capture different angles.")
    
    # Create samples directory if it doesn't exist
    samples_dir = 'samples'
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
    
    # Initialize camera
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)  # Set video Frame Width
    cam.set(4, 480)  # Set video Frame Height
    
    # Load face detector
    detector = cv2.CascadeClassifier("face Recognizer\\haarcascade_frontalface_default.xml")
    
    # Get user ID
    speak("What is your name?")
    user_name = takeCommand().lower()
    face_id = 1  # Default to ID 1
    
    # Update names list in a file
    try:
        with open('face_names.txt', 'w') as f:
            f.write(f"1,{user_name}")
    except:
        speak("Could not save user name. Continuing with enrollment.")
    
    # Take samples
    speak("Taking samples, please look at the camera...")
    count = 0
    sample_count = 50
    
    while True:
        ret, img = cam.read()
        if not ret:
            speak("Camera error. Please check your camera connection.")
            break
            
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply histogram equalization to improve contrast
        gray_image = cv2.equalizeHist(gray_image)
        
        # Detect faces
        faces = detector.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            
            # Save the captured face
            face_img = gray_image[y:y + h, x:x + w]
            file_path = os.path.join(samples_dir, f"face.{face_id}.{count}.jpg")
            cv2.imwrite(file_path, face_img)
            
            cv2.imshow('Face Enrollment', img)
            
            # Provide feedback on progress
            if count % 10 == 0:
                speak(f"{count} samples taken. {sample_count - count} more to go.")
        
        k = cv2.waitKey(100) & 0xff
        if k == 27:  # ESC key
            break
        elif count >= sample_count:
            break
    
    cam.release()
    cv2.destroyAllWindows()
    
    speak("Face samples collected. Now training the model...")
    
    # Train the model
    train_face_model()
    
    speak("Face enrollment completed successfully.")
    return True

def train_face_model():
    """Function to train the face recognition model"""
    path = 'samples'  # Path for samples
    
    if not os.path.exists(path):
        speak("No samples found. Please enroll your face first.")
        return False
    
    # Create trainer directory if it doesn't exist
    trainer_dir = 'trainer'
    if not os.path.exists(trainer_dir):
        os.makedirs(trainer_dir)
    
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except AttributeError:
        speak("cv2.face.LBPHFaceRecognizer_create is not available. Please install opencv-contrib-python.")
        return False
    
    detector = cv2.CascadeClassifier("face Recognizer\\haarcascade_frontalface_default.xml")
    
    # Function to get images and labels
    def get_images_and_labels(path):
        image_paths = [os.path.join(path, f) for f in os.listdir(path)]
        face_samples = []
        ids = []
        
        for image_path in image_paths:
            try:
                gray_img = Image.open(image_path).convert('L')  # Convert to grayscale
                img_arr = np.array(gray_img, 'uint8')
                
                id = int(os.path.split(image_path)[-1].split(".")[1])
                faces = detector.detectMultiScale(img_arr)
                
                for (x, y, w, h) in faces:
                    face_samples.append(img_arr[y:y+h, x:x+w])
                    ids.append(id)
            except Exception as e:
                continue
                
        return face_samples, ids
    
    faces, ids = get_images_and_labels(path)
    
    if len(faces) == 0:
        speak("No faces detected in the samples. Please try again.")
        return False
    
    recognizer.train(faces, np.array(ids))
    recognizer.write('trainer\\trainer.yml')
    
    return True

# Authentication function that combines face and password
def authenticate():
    """Combined authentication using face recognition and password"""
    auth_method = "both"  # Options: "face", "password", "both"
    
    if auth_method == "face" or auth_method == "both":
        speak("Starting face authentication")
        face_authenticated = Face_Recognition()
        
        if not face_authenticated and auth_method == "face":
            speak("Face authentication failed. Access denied.")
            return False
        elif face_authenticated and auth_method == "face":
            speak("Face authenticated successfully.")
            return True
        elif not face_authenticated and auth_method == "both":
            speak("Face authentication failed. Proceeding to password authentication.")
    
    if auth_method == "password" or auth_method == "both":
        speak("Please say the password")
        user_password = takeCommand().lower()
        
        passwd = read_password()
        if passwd is None:
            speak("No password set. Setting up new password.")
            passwd = user_password
            write_password(passwd)
            speak("Password set successfully.")
            return True
        else:
            if not verify_password(user_password, passwd):
                speak("Incorrect password. Access denied.")
                return False
            else:
                speak("Password authenticated successfully.")
                return True
    
    return False

# Function to change password
def c_passwd():
    speak("Please say your current password")
    current_password = takeCommand().lower()
    
    stored_password = read_password()
    if stored_password is None:
        speak("No password is currently set. Setting up a new password.")
    elif not verify_password(current_password, stored_password):
        speak("Incorrect password. Password change aborted.")
        return False
    
    speak("Please say your new password")
    new_password = takeCommand().lower()
    
    speak("Please confirm your new password")
    confirm_password = takeCommand().lower()
    
    if new_password == confirm_password:
        write_password(new_password)
        speak("Password changed successfully.")
        return True
    else:
        speak("Passwords do not match. Password change aborted.")
        return False

def wishMe():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I %M %p")

    if hour >= 0 and hour < 12:
        speak(f"Good Morning {user_name}, It's {tt}")

    elif hour >= 12 and hour < 18:
        speak(f"Good Afternoon {user_name}, It's {tt}")

    else:
        speak(f"Good Evening {user_name}, It's {tt}")

    speak(f"I am your Assistant, jarvis")

def mail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # server.login('sender's mail Id', 'senders password')
    server.login('kushalgangurde6@gmail.com', 'nrpoabcgwmgniqwa')
    server.sendmail('kushalgangurde6@gmail.com', to, content)
    server.close()

def hibernation():
    while True:
            per = takeCommand().lower()
            if "wake" in per:
                execute()
            elif "goodbye" in per or "good bye" in per:
                sys.exit()

def get_current_temperature():
    search = "temperature near me"
    url = f"https://www.google.com/search?q={search}"
    try:
        r = requests.get(url)
        data = BeautifulSoup(r.text, "html.parser")
        temp_div = data.find("div", class_="BNeawe")
        if temp_div:
            temp = temp_div.text
            speak(f"The current temperature at your location is {temp}.")
            return temp
        else:
            speak("Sorry, I couldn't find the temperature information.")
            return None
    except Exception as e:
        speak(f"Sorry, I couldn't get the temperature. Error: {e}")
        return None


def calculate(query):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("what do you want to calculate")
        print("Listening...")
        audio = r.listen(source, phrase_time_limit=3)
    try:
        user_input = input("input : ")  # r.recognize_google(audio, language="en-in")
        print(f"You said:  {user_input}")
        my_string = user_input
        def get_operator_fn(op):
            return {
                '+': operator.add,
                '-': operator.sub,
                'x': operator.mul,
                'divide': operator.__truediv__,
            }[op]
        def eval_binary_expr(op1, oper, op2):
            op1, op2 = int(op1), int(op2)
            return get_operator_fn(oper)(op1, op2)
        speak("your result is")
        speak(eval_binary_expr(*(my_string.split())))
        return eval_binary_expr(*(my_string.split()))
    except sr.UnknownValueError:
        return "Sorry, I didn't catch that."
    except Exception as e:
        speak(f"Error in calculation: {e}")
        return None

def location():
    try:
        g = geocoder.ip('me')
        latitude = g.latlng[0]
        longitude = g.latlng[1]
        country = g.country
        city = g.city
        
        speak(f"Your current latitude is {latitude:.6f}")
        speak(f"Your current longitude is {longitude:.6f}")
        speak(f"Your current country is {country}")
        speak(f"Your current city is {city}")
        
        print(f"Your current latitude: {latitude:.6f}")
        print(f"Your current longitude: {longitude:.6f}")
    except Exception as e:
        speak(f"Sorry {user_name} I am not able to find your current location {e}")

def work():
    from pywikihow import search_wikihow
    speak(f"Ok {user_name}, Tell me which work you want to search")
    how = takeCommand().lower()
    max_result = 1
    how_to_func = search_wikihow(how, max_result)
    assert len(how_to_func) == 1
    how_to_func[0].print()
    speak(how_to_func[0].summary)

def shutdown_pc():
    """Shuts down the computer after a confirmation prompt."""
    speak("Please confirm once again.")
    confirmation = input("please confirm yes/no: ").lower()
    if confirmation == "yes" or confirmation == "y":
        print("Shutting down...")
        os.system('shutdown /s /t 10')
        os.system('killall5 -9')
    else:
        speak("Shutdown canceled.")

def restart_pc():
    """Restarts the computer after a confirmation prompt."""
    speak("Please confirm once again.")
    confirmation = takeCommand().lower()
    if confirmation.lower() == "yes":
        print("Restarting...")
        os.system("shutdown /r /t 10")  # Initiates restart with a 30-second delay
    else:
        speak("Restart canceled.")

take_cmd = True
def  sleep_pc():
    global take_cmd
    speak("Going to sleep now.")
    os.system("")
    take_cmd = False  # Disable speech recognition before sleeping

# Function to re-enable speech recognition after waking up
def wake_pc():
    global take_cmd
    take_cmd = True
    time.sleep(10)  # Wait for everything to stabilize
    takeCommand()

def restart_program():
    """Restarts the current program, with file objects and descriptors"""
    try:
        p = subprocess.run([sys.executable] + sys.argv)
    except AttributeError:
        p = subprocess.Popen([sys.executable] + sys.argv)
    sys.exit(p.returncode) 



alarm_playing = True

def play_alarm(sound_file):
    global alarm_playing
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    while alarm_playing:
        pygame.mixer.music.play(-1)  # Play the music indefinitely
        # Wait for the music to finish or for the alarm to be paused
        while pygame.mixer.music.get_busy() and alarm_playing:
            time.sleep(1)  # Check every second
        pygame.mixer.music.stop()
        if not alarm_playing:
            # If alarm is paused, break out of the loop
            break

def set_alarm(sound_file):
    global alarm_playing
    alarm_time = input("Please enter the alarm time (HH:MM): ")

    # Validate the input format
    try:
        datetime.datetime.strptime(alarm_time, "%H:%M")
    except ValueError:
        print("Invalid time format. Please use HH:MM.")
        return

    alarm_minute = datetime.datetime.strptime(alarm_time, "%H:%M").minute
    speak(f"Alarm set for {alarm_time}. Waiting...")
    while True:
        now = datetime.datetime.now()
        current_minute = now.minute
        if now.strftime("%H:%M") == alarm_time:
            print("Alarm ringing. Wake Up!")
            # Start the alarm in a separate thread
            alarm_thread = threading.Thread(target=play_alarm, args=(sound_file,))
            alarm_thread.start()
            # Listen for user input to pause or resume the alarm
            while current_minute == alarm_minute:
                user_input = input("Press 'p' to pause/restart the alarm or 's' to stop it: ").strip().lower()
                if user_input == 'p':
                    # Toggle the alarm state
                    alarm_playing = not alarm_playing
                elif user_input == 's':
                    # Stop the alarm
                    alarm_playing = False
                    break
                time.sleep(1)  # Sleep for a second and check again
                current_minute = datetime.datetime.now().minute
            pygame.mixer.music.stop()  # Stop the alarm when the minute changes or when user stops it
            break
        time.sleep(1)  # Sleep for a second and check again

def tell_me_about(topic):
    """Function to get information about a topic from Wikipedia."""
    try:
        speak(f"Searching Wikipedia for {topic}")
        summary = wikipedia.summary(topic, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple options for this topic. Can you be more specific?")
    except wikipedia.exceptions.PageError as e:
        speak("Sorry, I couldn't find any information about this topic.")

def search_google(topic):
    """Function to search for a topic on Google."""
    try:
        url = f"https://www.bing.com/search?q={topic}"
        speak("Opening Google...")
        webbrowser.open(url)
    except Exception as e:
        speak("Sorry, I couldn't perform this task.")

def find_information(topic):
    """Function to find information about a topic."""
    try:
        url = f"https://www.google.com/search?q={topic}"
        speak(f"Searching for information about {topic}...")
        webbrowser.open(url)
    except Exception as e:
        speak("Sorry, I couldn't perform this task.")

def take_note():
    """Function to take a note."""
    try:
        speak("What would you like to write down?")
        note = takeCommand().lower()
        with open("notes.txt", "a") as file:
            file.write(note + "\n")
        speak("Note saved successfully.")
    except Exception as e:
        speak("Sorry, I couldn't save the note.")

def play_music(song):
    """Function to play a song."""
    try:
        music_dir = "D:\\Documents\\songs"
        songs = os.listdir(music_dir)
        for s in songs:
            if song.lower() in s.lower():
                os.startfile(os.path.join(music_dir, s))
                break
        else:
            speak("Sorry, I couldn't find the requested song.")
    except Exception as e:
        speak("Sorry, I couldn't play the song.")

def get_weather(city):
    """Function to get the weather information."""
    try:
        api_key = "aa6e598da8317f856e9f5e79d41a01a3"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather_desc = data['weather'][0]['description']
            temperature = data['main']['temp']
            speak(f"The weather in {city} is {weather_desc} with a temperature of {temperature} degrees Celsius.")
        else:
            speak("Sorry, I couldn't get the weather information.")
    except Exception as e:
        speak("Sorry, I couldn't get the weather information.")


from pywikihow import search_wikihow
import pywikihow
def how_to(task):
    try:
        max_results = 1  # Number of results to retrieve
        results = search_wikihow(task, max_results)
        if results:
            how_to = results[0]  # Get the first result
            title = how_to.title
            summary = how_to.summary
            steps = how_to.steps
            
            speak(f"Here are the instructions on how to {task}:")
            speak(f"Title: {title}")
            print(f"Summary: \n{summary}")
            # speak("Steps:")
            # for step_num, step in enumerate(steps, start=1):
            #     speak(f"Step {step_num}: {step}")
        else:
            speak("Sorry, I couldn't find instructions for this task.")
    except Exception as e:
        speak(f"An error occurred: {e}")

def translate(phrase, language):
    """Function to translate a phrase to a specified language."""
    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={language}&dt=t&q={phrase}"
        response = requests.get(url)
        translated_text = response.json()[0][0][0]
        speak(f"The translation of '{phrase}' to {language} is: {translated_text}")
    except Exception as e:
        speak("Sorry, I couldn't translate the phrase.")

def open_file(locate):
    """Function to open a file."""
    try:
        os.startfile(locate)
    except Exception as e:
        speak("Sorry, I couldn't open the file.")

def get_current_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        coordinates = data['loc'].split(',')
        return float(coordinates[0]), float(coordinates[1])
    except Exception as e:
        print(f"Error getting current location: {e}")
        return None

def get_distance(location):
    try:
        # Get current location
        current_location = get_current_location()
        if current_location:
            print("Current Location:", current_location)
            # Use geocoding API to get coordinates of the specified location
            headers = {'User-Agent': 'Your_User_Agent'}
            location_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
            response = requests.get(location_url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
            print("Geocoding Response:", data)
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                destination = (lat, lon)
                print("Destination:", destination)

                # Use haversine formula to calculate distance
                distance = haversine(current_location, destination)
                print("Distance:", distance)
                speak(f"The distance from your current location to {location} is {distance} kilometers.")
            else:
                speak("Sorry, I couldn't find the specified location.")
        else:
            speak("Sorry, I couldn't get your current location.")
    except Exception as e:
        speak("Sorry, I couldn't get the distance.")
        print(f"Error: {e}")

    time.sleep(1)

def set_volume(level):
    """Sets the system volume to the specified level."""
    try:
        CLSCTX_ALL = 0x0000FFFF
        volume = int(level)
        if 0 <= volume <= 100:
            # Get the default audio endpoint
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume_control = cast(interface, POINTER(IAudioEndpointVolume))

            # Set the volume
            if hasattr(volume_control, 'SetMasterVolumeLevelScalar'):
                volume_control.SetMasterVolumeLevelScalar(volume / 100.0, None)  # type: ignore
                speak(f"Volume set to {volume} percent.")
            else:
                speak("SetMasterVolumeLevelScalar is not available on this system.")
        else:
            speak("Volume level must be between 0 and 100.")
    except Exception as e:
        speak("Sorry, I couldn't set the volume.")
        print(f"Error: {e}")

def get_crypto_price(crypto):
    """Fetches the current price of a specified cryptocurrency."""
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto}&vs_currencies=usd"
        response = requests.get(url)
        price = response.json()[crypto]['usd']
        speak(f"The current price of {crypto} is ${price}.")
    except Exception as e:
        speak("Sorry, I couldn't fetch the cryptocurrency price.")
    
def tell_joke():
    try:
        url = "https://official-joke-api.appspot.com/jokes/random"
        response = requests.get(url)
        joke_data = response.json()
        speak(f"Here's a joke: {joke_data['setup']} ... {joke_data['punchline']}")
    except Exception as e:
        speak(f"An error occurred: {e}")

arduino_port = '/dev/ttyUSB0'  # or /dev/ttyACM0
baud_rate = 9600
def send_command(command):
    try:
        with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
            time.sleep(2)  # Wait for the Arduino to reset after opening the serial port
            ser.write((command + '\n').encode('utf-8'))  # Send command with newline character
            response = ser.readline().decode('utf-8').strip()  # Read the response from Arduino
            print(f"Arduino response: {response}")
    except serial.SerialException as e:
        print(f"Error communicating with Arduino: {e}")

import random

def tell_hindi_joke():
    jokes = [
        "टीचर: तुम स्कूल क्यों नहीं आए? \nछात्र: सर, मेरे पापा ने कहा था, जो अच्छा करेगा, उसे मैं स्कूल भेजूंगा!",
        "पत्नी: क्या तुम मुझे चाँद से भी ज्यादा प्यार करते हो? \nपति: हां, पर चाँद तो बहुत दूर है!",
        "पप्पू: डॉक्टर साहब, मुझे भूलने की बीमारी हो गई है! \nडॉक्टर: ये बीमारी तुम्हें कब से है? \nपप्पू: कौन सी बीमारी?",
        "बच्चा: मम्मी, स्कूल में सब बच्चे मुझसे डरते हैं! \nमम्मी: क्यों बेटा? \nबच्चा: क्योंकि मैं हमेशा सबसे पहले बर्थडे केक खाने चला जाता हूँ!",
        "संता: यार, मुझे एक ऐसा जूता चाहिए जो मुझे दौड़ने में मदद करे। \nबंता: तो फिर क्यों नहीं खरीदता? \nसंता: अरे, मैं तो हमेशा गिर जाता हूँ!"
    ]
    
    joke = random.choice(jokes)
    return joke


STATE_FILE = "jarvis_state.json"

def save_conversation(conversation):
    with open(STATE_FILE, 'w') as f:
        json.dump(conversation, f)
    print("Conversation saved.")

def load_conversation():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            conversation = json.load(f)
        print("Conversation loaded.")
        return conversation
    else:
        print("No saved conversation found.")
        return []
    
def disable_history():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        speak("History disabled")
    else:
        speak("No history to disable")


def execute():
    try:
        
        # Authenticate user
        if not authenticate():
            speak("Authentication failed. Access denied.")
            return
            
        speak("Access Granted. Welcome.")
        
        global user_name
        speak("What should I call you?")
        name_input = takeCommand()
        if name_input.lower() != "none":
            user_name = name_input
        
        clear()

        conversation = load_conversation()  # Load previous conversation
        if conversation:
            for line in conversation:
                print(line) 

        wishMe()
        
        # Dictionary of commands for better organization and easier maintenance
        commands = {
            "google": lambda: webbrowser.open(""),
            "bye": lambda: (save_conversation(conversation), speak("goodbye!"), exit()),
            "buy": lambda: (save_conversation(conversation), speak("goodbye!"), exit()),
            "open youtube": lambda: webbrowser.open("https://www.youtube.com"),
            "find video": lambda: (speak("what do you want to search on youtube?"), 
                                      webbrowser.open(f"https://www.youtube.com/results?search_query={takeCommand()}")),
            "time": lambda: speak(f"the current time is {datetime.datetime.now().strftime('%H:%M:%S')}"),
            "joke": lambda: speak(tell_hindi_joke()),
            "thank you": lambda: speak(f"{user_name} that's my pleasure."),
            "thakyou": lambda: speak(f"{user_name} that's my pleasure."),
            "shutdown": lambda: shutdown_pc(),
            "restart": lambda: restart_pc(),
            "sleep": lambda: sleep_pc(),
            "wake up": lambda: wake_pc(),
            "hibernate": lambda: hibernation(),
            "change password": lambda: c_passwd(),
            "enroll face": lambda: enroll_face(),
            "enroll new faces": lambda: enroll_face(),
            "train face model": lambda: train_face_model(),
            "erase chat": lambda: (os.remove("jarvis_state.json") if os.path.exists("jarvis_state.json") else None, speak("chat erased")),
            "disable history": lambda: disable_history(),
            "malfunction": lambda: (speak("Re-executing myself..."), execute()),
            "resolve": lambda: (speak("Re-executing myself..."), execute()),
            "turn on": lambda: (speak("turning on"), send_command("on")),
            "turn off": lambda: (speak("turning off"), send_command("off")),
            "take screenshot": lambda: take_screenshot(),
            "summarize text": lambda: summarize_text(),
            "create timer": lambda: create_timer(),
            "set timer": lambda: create_timer(),
            "random fact": lambda: get_random_fact(),
            "tell me a fact": lambda: get_random_fact(),
            "quote": lambda: get_quote(),
            "tell me a quote": lambda: get_quote(),
            "clear screen": lambda: os.system('cls'),
            "clean screen": lambda: os.system('cls'),
        }

        while True:
            query = takeCommand().lower()
            if query == "none":
                continue
                
            conversation.append(query)
            
            # Check for exact command matches first
            command_executed = False
            for cmd, action in commands.items():
                if cmd in query:
                    action()
                    command_executed = True
                    break
                    
            if command_executed:
                continue
                
            # Handle more complex commands that need parameter extraction
            if "crypto price" in query:
                crypto = query.replace("crypto price ", "")
                get_crypto_price(crypto)

            elif "calculate" in query:
                calculate(query)
                
            elif "wikipedia" in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                
            elif "search" in query:
                search_term = query.replace("search ", "")
                search_google(search_term)
                
            elif "tell me about" in query:
                topic = query.replace("tell me about ", "")
                tell_me_about(topic)
                
            elif "how to" in query:
                task = query.replace("how to ", "")
                how_to(task)
                
            elif "translate" in query:
                # Extract the phrase and language
                try:
                    # Format: "translate [phrase] to [language]"
                    parts = query.replace("translate ", "").split(" to ")
                    if len(parts) == 2:
                        phrase = parts[0]
                        language = parts[1]
                        translate(phrase, language)
                    else:
                        speak("Please specify the phrase and language. For example, 'translate hello to Spanish'")
                except Exception as e:
                    speak(f"Error in translation: {e}")
                    
            elif "weather" in query:
                if "in" in query:
                    # Format: "weather in [city]"
                    city = query.split("in ")[1]
                    get_weather(city)
                else:
                    # Get weather for current location
                    location = get_current_location()
                    if location:
                        get_weather(location)
                    else:
                        speak("Could not determine your current location.")
                        
            elif "temperature" in query:
                temp = get_current_temperature()
                if temp:
                    speak(f"The current temperature is {temp} degrees Celsius.")
                else:
                    speak("Sorry, I couldn't get the temperature.")
                
            elif "set alarm" in query:
                speak("Setting an alarm. What time would you like to set it for?")
                alarm_time = takeCommand()
                set_alarm("alarm.mp3")
                
            elif "take note" in query or "make a note" in query:
                take_note()
                
            elif "play music" in query:
                speak("What song would you like to play?")
                song = takeCommand()
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}+song")
                
            elif "open file" in query or "open folder" in query:
                location = query.replace("open file ", "").replace("open folder ", "")
                open_file(location)
                
            elif "where am i" in query or "my location" in query:
                location = get_current_location()
                if location:
                    speak(f"You are currently in {location}")
                else:
                    speak("Could not determine your current location.")
                    
            elif "how far is" in query:
                location = query.replace("how far is ", "")
                get_distance(location)
                
            elif "set volume to" in query:
                level = query.replace("set volume to ", "").replace("%", "")
                set_volume(level)
                
            elif "send email" in query or "send mail" in query:
                try:
                    speak("Who should I send the email to?")
                    to = takeCommand()
                    speak("What should the email say?")
                    content = takeCommand()
                    mail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    speak(f"Sorry, I couldn't send the email. Error: {e}")
                    
            elif "system info" in query or "system information" in query:
                system_info()
                
            elif "battery status" in query:
                check_battery()
                
            elif "network status" in query:
                check_network()
                
            elif "memory usage" in query:
                check_memory_usage()
                
            elif "cpu usage" in query:
                check_cpu_usage()
                
            elif "disk space" in query:
                check_disk_space()
                
            elif "news" in query:
                get_latest_news()
                
            elif "reminder" in query:
                set_reminder()
                
            elif "todo" in query or "to do" in query:
                manage_todo()
                
            elif "stock price" in query or "stock value" in query:
                # Format: "stock price of [symbol]"
                symbol = query.replace("stock price of ", "").replace("stock value of ", "")
                get_stock_price(symbol)
                
            elif "exchange rate" in query:
                try:
                    # Format: "exchange rate from [currency] to [currency]"
                    parts = query.replace("exchange rate from ", "").split(" to ")
                    if len(parts) == 2:
                        from_currency = parts[0]
                        to_currency = parts[1]
                        get_exchange_rate(from_currency, to_currency)
                    else:
                        speak("Please specify the currencies. For example, 'exchange rate from USD to EUR'")
                except Exception as e:
                    speak(f"Error getting exchange rate: {e}")
                    
            elif "define" in query:
                # Format: "define [word]"
                word = query.replace("define ", "")
                get_word_definition(word)
                
            elif "covid" in query or "covid-19" in query:
                if "in" in query:
                    # Format: "covid stats in [country]"
                    country = query.split("in ")[1]
                    get_covid_stats(country)
                else:
                    get_covid_stats()
                    
            elif "movie info" in query or "about movie" in query:
                # Format: "movie info [movie name]" or "tell me about movie [movie name]"
                movie_name = query.replace("movie info ", "").replace("about movie ", "")
                get_movie_info(movie_name)
                
            elif "select all" in query:
                pyautogui.hotkey('ctrl', 'a')
                
            elif "copy" in query:
                pyautogui.hotkey('ctrl', 'c')
                
            elif "paste" in query:
                pyautogui.hotkey('ctrl', 'v')
                
            elif "undo" in query:
                pyautogui.hotkey('ctrl', 'z')
                
            elif "delete" in query:
                pyautogui.hotkey('del')
                
            elif "close tab" in query or "close this tab" in query:
                speak("closing tab")
                pyautogui.hotkey('ctrl', 'w')
                
            elif "change tab" in query:
                speak("Changing tab..")
                pyautogui.hotkey('alt', 'tab')

            else:
                speak(f"I'm not sure how to help with '{query}'. Can you try a different command?")

    except Exception as e:
        speak(f"Sorry {user_name}, an error occurred. Because {e}")
        execute()

# New functions to enhance the assistant's capabilities

def system_info():
    """Display system information"""
    import platform
    
    system = platform.system()
    processor = platform.processor()
    architecture = platform.architecture()
    node = platform.node()
    release = platform.release()
    version = platform.version()
    
    speak(f"System: {system}")
    speak(f"Processor: {processor}")
    speak(f"Architecture: {architecture[0]}")
    speak(f"Node: {node}")
    speak(f"Release: {release}")
    speak(f"Version: {version}")

def check_battery():
    """Check battery status"""
    try:
        import psutil
        
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            power_plugged = battery.power_plugged
            
            status = "plugged in" if power_plugged else "not plugged in"
            speak(f"Battery is at {percent}% and is {status}")
        else:
            speak("No battery detected. You might be using a desktop computer.")
    except Exception as e:
        speak(f"Could not check battery status: {e}")

def check_network():
    """Check network status"""
    try:
        import socket
        import psutil
        
        # Check if connected to internet
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            speak("Internet connection is active")
        except OSError:
            speak("No internet connection")
            
        # Get network interfaces
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent / (1024 * 1024)  # Convert to MB
        bytes_recv = net_io.bytes_recv / (1024 * 1024)  # Convert to MB
        
        speak(f"Network usage: {bytes_sent:.2f} MB sent, {bytes_recv:.2f} MB received")
    except Exception as e:
        speak(f"Could not check network status: {e}")

def check_memory_usage():
    """Check memory usage"""
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        total = memory.total / (1024 * 1024 * 1024)  # Convert to GB
        available = memory.available / (1024 * 1024 * 1024)  # Convert to GB
        used = memory.used / (1024 * 1024 * 1024)  # Convert to GB
        percent = memory.percent
        
        speak(f"Total memory: {total:.2f} GB")
        speak(f"Available memory: {available:.2f} GB")
        speak(f"Used memory: {used:.2f} GB")
        speak(f"Memory usage: {percent}%")
    except Exception as e:
        speak(f"Could not check memory usage: {e}")

def check_cpu_usage():
    """Check CPU usage"""
    try:
        import psutil
        
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        speak(f"CPU usage: {cpu_percent}%")
        speak(f"Number of CPU cores: {cpu_count}")
        if cpu_freq:
            speak(f"CPU frequency: {cpu_freq.current:.2f} MHz")
    except Exception as e:
        speak(f"Could not check CPU usage: {e}")

def check_disk_space():
    """Check disk space"""
    try:
        import psutil
        
        disk = psutil.disk_usage('/')
        total = disk.total / (1024 * 1024 * 1024)  # Convert to GB
        used = disk.used / (1024 * 1024 * 1024)  # Convert to GB
        free = disk.free / (1024 * 1024 * 1024)  # Convert to GB
        percent = disk.percent
        
        speak(f"Total disk space: {total:.2f} GB")
        speak(f"Used disk space: {used:.2f} GB")
        speak(f"Free disk space: {free:.2f} GB")
        speak(f"Disk usage: {percent}%")
    except Exception as e:
        speak(f"Could not check disk space: {e}")

def get_latest_news(category="general"):
    """Get latest news headlines"""
    try:
        import requests
        
        # You would need to get an API key from newsapi.org
        # For now, we'll use a mock response
        speak("Here are the latest headlines:")
        
        # In a real implementation, you would use:
        # url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey=YOUR_API_KEY"
        # response = requests.get(url)
        # news = response.json()
        
        # Mock headlines
        headlines = [
            "Global tech companies announce new AI initiatives",
            "Scientists discover potential breakthrough in renewable energy",
            "Major sports event concludes with unexpected results",
            "New health guidelines released for pandemic prevention",
            "Economic forecast predicts growth in coming quarter"
        ]
        
        for i, headline in enumerate(headlines, 1):
            if i > 5:  # Limit to 5 headlines
                break
            speak(f"{i}. {headline}")
    except Exception as e:
        speak(f"Could not fetch news: {e}")

def set_reminder():
    """Set a reminder"""
    speak("What would you like me to remind you about?")
    reminder_text = takeCommand()
    
    speak("When should I remind you? Please specify the time.")
    reminder_time = takeCommand()
    
    # Parse the time (this is a simplified version)
    import datetime
    import threading
    
    try:
        # Very basic time parsing - would need to be more sophisticated in a real app
        if ":" in reminder_time:
            hour, minute = map(int, reminder_time.split(":"))
        else:
            hour = int(reminder_time)
            minute = 0
            
        current_time = datetime.datetime.now()
        reminder_datetime = current_time.replace(hour=hour, minute=minute, second=0)
        
        # If the time has already passed today, set it for tomorrow
        if reminder_datetime < current_time:
            reminder_datetime += datetime.timedelta(days=1)
            
        # Calculate seconds until the reminder
        seconds_until_reminder = (reminder_datetime - current_time).total_seconds()
        
        speak(f"I'll remind you to {reminder_text} at {hour}:{minute:02d}")
        
        # Set up the reminder in a separate thread
        def reminder_thread():
            time.sleep(seconds_until_reminder)
            speak(f"Reminder: {reminder_text}")
            
        threading.Thread(target=reminder_thread, daemon=True).start()
    except Exception as e:
        speak(f"Sorry, I couldn't set the reminder: {e}")

def manage_todo():
    """Manage to-do list"""
    todo_file = "todo.json"
    
    # Load existing to-do list
    try:
        if os.path.exists(todo_file):
            with open(todo_file, "r") as f:
                todos = json.load(f)
        else:
            todos = []
    except Exception:
        todos = []
        
    speak("What would you like to do with your to-do list? Add an item, list items, mark as done, or clear the list?")
    action = takeCommand().lower()
    
    if "add" in action:
        speak("What would you like to add to your to-do list?")
        item = takeCommand()
        todos.append({"task": item, "done": False, "date_added": str(datetime.datetime.now())})
        speak(f"Added '{item}' to your to-do list.")
        
    elif "list" in action:
        if not todos:
            speak("Your to-do list is empty.")
        else:
            speak("Here's your to-do list:")
            for i, todo in enumerate(todos, 1):
                status = "Done" if todo["done"] else "Not done"
                speak(f"{i}. {todo['task']} - {status}")
                
    elif "mark" in action and "done" in action:
        if not todos:
            speak("Your to-do list is empty.")
        else:
            speak("Which item would you like to mark as done? Please say the number.")
            try:
                item_num = int(takeCommand())
                if 1 <= item_num <= len(todos):
                    todos[item_num-1]["done"] = True
                    speak(f"Marked '{todos[item_num-1]['task']}' as done.")
                else:
                    speak("Invalid item number.")
            except ValueError:
                speak("Sorry, I didn't understand the number.")
                
    elif "clear" in action:
        speak("Are you sure you want to clear your to-do list?")
        confirmation = takeCommand().lower()
        if "yes" in confirmation or "yeah" in confirmation:
            todos = []
            speak("To-do list cleared.")
        else:
            speak("Operation cancelled.")
            
    # Save the to-do list
    try:
        with open(todo_file, "w") as f:
            json.dump(todos, f)
    except Exception as e:
        speak(f"Could not save to-do list: {e}")

def take_screenshot():
    """Take a screenshot and save it"""
    try:
        import pyautogui
        from datetime import datetime
        
        # Create screenshots directory if it doesn't exist
        screenshots_dir = "screenshots"
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{screenshots_dir}/screenshot_{timestamp}.png"
        
        # Take screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        
        speak(f"Screenshot taken and saved as {filename}")
        return filename
    except Exception as e:
        speak(f"Could not take screenshot: {e}")
        return None

def summarize_text():
    """Summarize text from clipboard or user input"""
    try:
        import pyperclip
        
        speak("Would you like to summarize text from clipboard or would you like to speak it?")
        choice = takeCommand().lower()
        
        if "clipboard" in choice:
            text = pyperclip.paste()
            if not text:
                speak("Clipboard is empty. Please copy some text first.")
                return
        else:
            speak("Please speak the text you want to summarize.")
            text = takeCommand()
            
        # Simple summarization by extracting key sentences
        # In a real implementation, you would use a more sophisticated algorithm or API
        sentences = text.split('.')
        if len(sentences) <= 3:
            speak("Text is already concise. Here it is:")
            speak(text)
            return
            
        # Extract first, middle and last sentence as a simple summary
        summary = f"{sentences[0]}. {sentences[len(sentences)//2]}. {sentences[-2]}."
        
        speak("Here's a summary of the text:")
        speak(summary)
    except Exception as e:
        speak(f"Could not summarize text: {e}")

def create_timer():
    """Create a countdown timer"""
    speak("How many minutes would you like to set the timer for?")
    try:
        minutes = int(takeCommand())
        seconds = minutes * 60
        
        speak(f"Timer set for {minutes} minutes. Starting now.")
        
        # Create a separate thread for the timer
        def timer_thread():
            time.sleep(seconds)
            # Play a sound when timer is done
            speak("Timer is done!")
            try:
                pygame.mixer.init()
                pygame.mixer.music.load("alarm.mp3")
                pygame.mixer.music.play()
                time.sleep(3)  # Play for 3 seconds
                pygame.mixer.music.stop()
            except:
                pass
                
        threading.Thread(target=timer_thread, daemon=True).start()
    except ValueError:
        speak("Sorry, I couldn't understand the time. Please try again with a number.")

def get_stock_price(symbol):
    """Get the current stock price for a given symbol"""
    try:
        import requests
        from bs4 import BeautifulSoup
        
        # This is a simplified version - in a real app, you would use a proper API
        url = f"https://finance.yahoo.com/quote/{symbol}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # This is a simplified approach and might break if Yahoo Finance changes their layout
        price_element = soup.find('fin-streamer', {'data-field': 'regularMarketPrice'})
        
        if price_element:
            price = price_element.text
            speak(f"The current price of {symbol} is {price}")
        else:
            speak(f"Could not find the price for {symbol}")
    except Exception as e:
        speak(f"Could not get stock price: {e}")

def get_exchange_rate(from_currency, to_currency):
    """Get the exchange rate between two currencies"""
    try:
        import requests
        
        # This is a simplified version - in a real app, you would use a proper API
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        
        response = requests.get(url)
        data = response.json()
        
        if 'rates' in data and to_currency.upper() in data['rates']:
            rate = data['rates'][to_currency.upper()]
            speak(f"The exchange rate from {from_currency.upper()} to {to_currency.upper()} is {rate}")
        else:
            speak(f"Could not find the exchange rate between {from_currency} and {to_currency}")
    except Exception as e:
        speak(f"Could not get exchange rate: {e}")

def get_random_fact():
    """Get a random fact"""
    try:
        import requests
        
        url = "https://uselessfacts.jsph.pl/random.json?language=en"
        
        response = requests.get(url)
        data = response.json()
        
        if 'text' in data:
            fact = data['text']
            speak(f"Here's a random fact: {fact}")
        else:
            speak("Could not get a random fact")
    except Exception as e:
        speak(f"Could not get a random fact: {e}")

def get_word_definition(word):
    """Get the definition of a word"""
    try:
        import requests
        
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        response = requests.get(url)
        data = response.json()
        
        if isinstance(data, list) and len(data) > 0:
            meanings = data[0].get('meanings', [])
            if meanings:
                definition = meanings[0].get('definitions', [{}])[0].get('definition', '')
                speak(f"The definition of {word} is: {definition}")
            else:
                speak(f"Could not find the definition of {word}")
        else:
            speak(f"Could not find the definition of {word}")
    except Exception as e:
        speak(f"Could not get the definition: {e}")

def get_quote():
    """Get a random quote"""
    try:
        import requests
        
        url = "https://api.quotable.io/random"
        
        response = requests.get(url)
        data = response.json()
        
        if 'content' in data and 'author' in data:
            quote = data['content']
            author = data['author']
            speak(f"Here's a quote: {quote} - {author}")
        else:
            speak("Could not get a quote")
    except Exception as e:
        speak(f"Could not get a quote: {e}")

def get_covid_stats(country="global"):
    """Get COVID-19 statistics for a country or globally"""
    try:
        import requests
        
        if country.lower() == "global":
            url = "https://disease.sh/v3/covid-19/all"
        else:
            url = f"https://disease.sh/v3/covid-19/countries/{country}"
        
        response = requests.get(url)
        data = response.json()
        
        if 'cases' in data and 'deaths' in data and 'recovered' in data:
            cases = data['cases']
            deaths = data['deaths']
            recovered = data['recovered']
            
            location = "globally" if country.lower() == "global" else f"in {country}"
            speak(f"COVID-19 statistics {location}: {cases} cases, {deaths} deaths, and {recovered} recovered")
        else:
            speak(f"Could not find COVID-19 statistics for {country}")
    except Exception as e:
        speak(f"Could not get COVID-19 statistics: {e}")

def get_movie_info(movie_name):
    """Get information about a movie"""
    try:
        import requests
        
        # You would need to get an API key from OMDb API
        # For now, we'll use a mock response
        speak(f"Here's some information about {movie_name}:")
        
        # Mock movie information
        speak(f"{movie_name} is a popular movie released in 2023. It received positive reviews from critics and audiences alike.")
    except Exception as e:
        speak(f"Could not get movie information: {e}")

def takeCommand():
    """Takes microphone input from the user and returns string output"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300  # Adjust based on your environment
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            if hasattr(r, 'recognize_google'):
                query = r.recognize_google(audio, language='en-in')
                print(f"User said: {query}\n")
                return query
            else:
                print("recognize_google is not available in this version of speech_recognition.")
                return "None"
        except sr.UnknownValueError:
            # User didn't say anything or speech wasn't recognized
            print("No input detected.")
            return "None"
        except sr.RequestError:
            print("Sorry, my speech service is down. Please check your internet connection.")
            return "None"
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return "None"
    return "None"

def speak(audio):
    """Convert text to speech"""
    try:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  # 0 for male voice, 1 for female voice
        engine.setProperty('rate', 180)  # Speed of speech
        print(f"Assistant: {audio}")
        engine.say(audio)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech synthesis: {e}")
        print(f"Assistant: {audio}")

def clear():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    speak("Hello, Jarvis on this side.")
    speak("Starting up...")
    
    # Check if this is the first run
    if not os.path.exists("password.py") and not os.path.exists("trainer/trainer.yml"):
        speak("It seems this is your first time running the assistant.")
        speak("Would you like to set up face recognition, password authentication, or both?")
        auth_choice = takeCommand().lower()
        
        if "face" in auth_choice:
            speak("Setting up face recognition.")
            enroll_face()
            
        if "password" in auth_choice or "both" in auth_choice:
            speak("Setting up password authentication.")
            speak("Please say your password")
            password = takeCommand().lower()
            write_password(password)
            speak("Password set successfully.")
            
        speak("Setup complete. Now starting the assistant.")
    
    # Start the assistant
    execute()
    
    # Listen for wake word after execution ends
    speak("Assistant is now in sleep mode. Say 'wake' to activate.")
    while True:
        per = takeCommand().lower()
        if "wake" in per:
            speak("Waking up...")
            execute()
        elif "goodbye" in per or "good bye" in per:
            speak("Goodbye! Have a great day.")
            sys.exit()