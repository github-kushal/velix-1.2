import datetime
import math
import time
import geocoder
import requests
from haversine import haversine


class Utilities:
    """A collection of utility helper functions for the assistant."""

    user_name = "User"

    @staticmethod
    def take_note():
        """Function to take a note."""
        try:
            print("What would you like to write down?")
            note = input("Enter your note: ")
            with open("notes.txt", "a") as file:
                file.write(note + "\n")
            print("Note saved successfully.")
        except Exception as e:
            print("Sorry, I couldn't save the note.")

    @staticmethod
    def add(a, b):
        """Adds two numbers and prints the result."""
        print(f"Answer is : {a + b}")

    @staticmethod
    def subtract(a, b):
        """Subtracts b from a and prints the result."""
        print(f"Answer is {a - b}")

    @staticmethod
    def multiply(a, b):
        """Multiplies two numbers and prints the result."""
        print(f"Answer is : {a * b}")

    @staticmethod
    def divide(a, b):
        """Divides a by b and prints the result."""
        print(f"{a / b}")

    @staticmethod
    def exponent(a: float, b: float):
        """Calculates a raised to the power of b."""
        c = math.pow(a, b)
        print(f"The exponent is {c}")

    @staticmethod
    def sq_root(a):
        """Calculates the square root of a."""
        print(f"The square-root of {a} is {math.sqrt(a):.2f}")

    @staticmethod
    def translate(phrase, language):
        """Function to translate a phrase to a specified language."""
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={language}&dt=t&q={phrase}"
            response = requests.get(url)
            translated_text = response.json()[0][0][0]
            print(f"The translation of '{phrase}' to {language} is: {translated_text}")
        except Exception as e:
            print("Sorry, I couldn't translate the phrase.")

    @classmethod
    def wishMe(cls):
        """Greets the user based on the current time of day."""
        print("What should I call you ?")

        name = takeCommand()

        if name is None or name.lower() == "none" or name.strip() == "":
            cls.user_name = "User"
        else:
            cls.user_name = name
            
        clear()
        
        hour = int(datetime.datetime.now().hour)
        tt = time.strftime("%I %M %p")

        if 0 <= hour < 12:
            print(f"Good Morning {cls.user_name}, It's {tt}")
        elif 12 <= hour < 18:
            print(f"Good Afternoon {cls.user_name}, It's {tt}")
        else:
            print(f"Good Evening {cls.user_name}, It's {tt}")

        print("I am your Assistant, jarvis")

    @classmethod
    def location(cls):
        """Fetches and announces the user's current location details."""
        try:
            g = geocoder.ip('me')
            latitude = g.latlng[0]
            longitude = g.latlng[1]
            country = g.country
            city = g.city
            
            print(f"Your current latitude is {latitude:.6f}")
            print(f"Your current longitude is {longitude:.6f}")
            print(f"Your current country is {country}")
            print(f"Your current city is {city}")
            
            print(f"Your current latitude: {latitude:.6f}")
            print(f"Your current longitude: {longitude:.6f}")
        except Exception as e:
            print(f"Sorry {cls.user_name} I am not able to find your current location {e}")

    @staticmethod
    def get_current_location():
        """Fetches current location coordinates using ipinfo.io."""
        try:
            response = requests.get("https://ipinfo.io/json")
            response.raise_for_status()
            data = response.json()
            coordinates = data['loc'].split(',')
            return float(coordinates[0]), float(coordinates[1])
        except Exception as e:
            print(f"Error getting current location: {e}")
            return None

    @classmethod
    def get_distance(cls, location):
        """Calculates distance between the user's current location and a destination."""
        try:
            current_location = cls.get_current_location()
            if current_location:
                print("Current Location:", current_location)
                headers = {'User-Agent': 'Your_User_Agent'}
                location_url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
                response = requests.get(location_url, headers=headers)
                response.raise_for_status()
                data = response.json()
                print("Geocoding Response:", data)
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    destination = (lat, lon)
                    print("Destination:", destination)

                    distance = haversine(current_location, destination)
                    print("Distance:", distance)
                    print(f"The distance from your current location to {location} is {distance} kilometers.")
                else:
                    print("Sorry, I couldn't find the specified location.")
            else:
                print("Sorry, I couldn't get your current location.")
        except Exception as e:
            print("Sorry, I couldn't get the distance.")
            print(f"Error: {e}")

        time.sleep(1)

    @staticmethod
    def get_quote():
        """Fetches and prints a random quote."""
        try:
            url = "https://api.quotable.io/random"
            response = requests.get(url)
            data = response.json()
            
            if 'content' in data and 'author' in data:
                quote = data['content']
                author = data['author']
                print(f"Here's a quote: {quote} - {author}")
            else:
                print("Could not get a quote")
        except Exception as e:
            print(f"Could not get a quote: {e}")


        