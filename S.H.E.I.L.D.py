from gettext import ngettext
from re import search
import sys
import cv2
import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import wikipedia
import requests
import subprocess
import ctypes
import os
import json
import os.path
import spacy
import pywhatkit
import openai
import random
import pygame
import numpy as np
from bs4 import BeautifulSoup
import io
from google.cloud import speech
from google.cloud import translate_v2 as translate
from playsound import playsound
from translate import Translator


# Initialize the speech recognition object
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Load the English language model
nlp = spacy.load('en_core_web_sm')

engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')


# Set up OpenAI API
openai.api_key = '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'
model = "gpt-3.5-turbo"


# Global variables
user_info_file = "user_info.json"
user_info = {}

# Specify the path to your sound file
sound_file = r'C:\Users\er\Downloads\Avengers BGM.mp3'



# Text-to-speech setup
engine = pyttsx3.init()

# Define global variables for context and user preferences
context = []
user_preferences = {}

# Function to detect faces in an image
def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Function to speak the provided text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define the AI voice assistant function
def voice_assistant():
    # Initialize the video capture
    cap = cv2.VideoCapture(0)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Perform face detection
        faces = detect_faces(frame)

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('', frame)

        # Check if a face is detected
        if len(faces) > 0:
            greet_user()  # Greet the user
            break

        # Check if the user wants to terminate
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

    
    while True:

        with sr.Microphone() as source:
            print("Listening...")

            # Adjust microphone levels if needed
            r.adjust_for_ambient_noise(source)

            # Listen to the user's command
            audio = r.listen(source)
            
            
            try:
                # Convert speech to text
                command = r.recognize_google(audio)
                print("You said:", command)

                
                # Use spaCy for language understanding
                doc = nlp(command)


                # Check if the user wants to terminate
                if "deactivate yourself" in command.lower():
                    speak("Deactivating myself! Goodbye!..........")
                    break

                # Perform tasks based on the command
                if "hello" in command:
                    greet_user()
                elif "how are you" in command:
                    speak("I'm fine!")
                elif "I love you" in command:
                    speak("I love you 3000. But ,my only pain is that i can't feeled your love")
                elif "what is your name" in command:
                    speak("My name is Sheild. What's yours?")
                elif "my name is" in command:
                    speak("Oooo. Hi! Nice to meet you")
                elif "who created you" in command:
                    speak("I'm beutifully crafeted by Sumit Chakroborty")
                elif "what is the meaning of life" in command:
                    speak("Meaning of life is connected to a higher power, or divine purpose. It may involve concepts, such as, fulfilling God's will, attaining enlightenment, or seeking spiritual growth.")
                elif "open Google" in command:
                    open_google()
                elif "open YouTube" in command:
                    open_youtube()
                elif "search youtube for" in command.lower():
                   search_query = command.lower().replace("search youtube for", "").strip()
                   search_youtube(search_query)

                elif "play youtube video" in command.lower():
                    video_query = command.lower().replace("play youtube video", "").strip()
                    play_youtube_video(video_query)

                elif "open Facebook" in command:
                    open_facebook()
                elif "open Instagram" in command:
                    open_instagram()
                elif "browse the internet for" in command:
                    browse_internet(command)
                elif "search Google Chrome for" in command:
                    search_google_chrome(command)
                elif "find location" in command:
                     find_location(command)
                elif "view Gmail" in command:
                    view_gmail()
                elif "compose mail" in command:
                    compose_mail()
                elif "identify number" in command:
                    identify_number(command)
                elif "store information" in command:
                    store_information()
                elif "give me information" in command:
                      get_information()
                elif "create spreadsheet" in command:
                    create_spreadsheet()
                elif "open MS Word" in command:
                    create_word_document()
                elif "weather report for" in command:
                    get_weather_report(command)
                elif "tell me the time" in command:
                    tell_time()
                elif "search Wikipedia for" in command:
                    search_wikipedia(command)
                elif "play music" in command:
                    play_music()
                elif "increase brightness" in command:
                    increase_brightness()
                elif "decrease brightness" in command:
                    decrease_brightness()
                elif "increase volume" in command:
                    increase_volume()
                elif "decrease volume" in command:
                    decrease_volume()
                elif "turn on airplane mode" in command:
                    turn_on_airplane_mode()
                elif "turn off airplane mode" in command:
                    turn_off_airplane_mode()
                elif "turn on Wi-Fi" in command:
                    turn_on_wifi()
                elif "turn off Wi-Fi" in command:
                    turn_off_wifi()
                elif "tell me a joke" in command:
                    tell_joke()
                elif "translate language" in command:
                    translate_text = command.replace("translate", "").strip()
                    translation = translate(translate_text)
                    speak(f"The translation is: {translation}")

                else:
                     response = process_command(command)
                     speak(response)

                ask_for_another_task()

            except sr.UnknownValueError:
                speak("Sorry Sir! I didn't understand. Please try again.")
            except sr.RequestError as e:
                speak("Sorry Sir! I'm unable to process your request. Please try again later.")
                
                save_user_info()


                
# Function to greet the user
def greet_user():

    # Implement greeting logic based on time of day, user preferences, etc.
    # Example:
    speak("Welcome home sir!........")

    # Call the function to play the sound
    play_sound(sound_file)
    
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        speak("Good Morning!")
    elif 12 <= current_hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
        
    speak("Now me to introduce myself! I am Sheild! the virtual Artificial Intelligence. I'm here to assist you in variety of task as best i can! 24 hours a days ,7 days a week. Importing all preferences from home interface. Now system are fully operational!")
    speak("How can I help you today?")

def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def translate(text):
    translator = Translator(to_lang="bn")
    translation = translator.translate(text)
    speak(translation)
    return translation

# Function to browse the internet
def browse_internet(command):
    search_query = command.replace("browse the internet for", "")
    search_query = search_query.strip()
    webbrowser.open(f'https://www.google.com/search?q={search_query}')
    speak("Sir! Here is your result...")
    
def store_information():
    speak("What information would you like to store?")
    data = get_user_input()

    speak("Under what name would you like to store this information?")
    name = get_user_input()

    user_info[name] = data
    speak("Information stored successfully.")

def get_information():
    speak("What information would you like to retrieve?")
    query = get_user_input()

    if query in user_info:
        speak(f"Here is the information for {query}: {user_info[query]}")
    else:
        speak("Sorry, I couldn't find any information for that query.")

def get_user_input():
    with sr.Microphone() as source:
        audio = r.listen(source)
        return r.recognize_google(audio)


# Load user information from the file
def load_user_info():
    global user_info
    if os.path.isfile(user_info_file):
        with open(user_info_file, "r") as file:
            user_info = json.load(file)

# Save user information to the file
def save_user_info():
    with open(user_info_file, "w") as file:
        json.dump(user_info, file)

# Start the voice assistant
def start_voice_assistant():
    load_user_info()
    voice_assistant()
    save_user_info()
    
# Function to increase screen brightness
def increase_brightness():
    if sys.platform == "win32":
        brightness = ctypes.c_ulong()
        ctypes.windll.user32.GetMonitorBrightness(ctypes.c_void_p(), ctypes.byref(brightness))
        current_brightness = brightness.value / 1000.0
        new_brightness = min(current_brightness + 0.1, 1.0)
        ctypes.windll.user32.SetMonitorBrightness(ctypes.c_void_p(), int(new_brightness * 1000))
        speak("Brightness increased.")
        speak("Sir! your task is completed...")
    else:
      speak("Sorry, Sir! I'm unable to adjust the brightness on this operating system.")

# Function to decrease screen brightness
def decrease_brightness():
    if sys.platform == "win32":
        brightness = ctypes.c_ulong()
        ctypes.windll.user32.GetMonitorBrightness(ctypes.c_void_p(), ctypes.byref(brightness))
        current_brightness = brightness.value / 1000.0
        new_brightness = max(current_brightness - 0.1, 0.0)
        ctypes.windll.user32.SetMonitorBrightness(ctypes.c_void_p(), int(new_brightness * 1000))
        speak("Brightness decreased.")
        speak("Sir! your task is completed...")
    else:
     speak("Sorry, Sir! I'm unable to adjust the brightness on this operating system.")

# Function to increase system volume
def increase_volume():
    if sys.platform == "win32":
        subprocess.Popen(["nircmd.exe", "changesysvolume", "2000"])
        speak("Volume increased.")
        speak("Sir! your task is completed........")
    else:
        speak("Sorry, Sir! I'm unable to adjust the volume on this operating system.")

# Function to decrease system volume
def decrease_volume():
    if sys.platform == "win32":
        subprocess.Popen(["nircmd.exe", "changesysvolume", "-2000"])
        speak("Volume decreased.")
        speak("Sir! your task is completed........")
    else:
        speak("Sorry, Sir! I'm unable to adjust the volume on this operating system.")

# Function to turn on airplane mode
def turn_on_airplane_mode():
    if sys.platform == "win32":
        subprocess.Popen(["nircmd.exe", "setairport", "mode", "1"])
        speak("Airplane mode turned on.")
        speak("Sir! your task is completed.......")
    else:
        speak("Sorry, Sir! I'm unable to turn on airplane mode on this operating system.")

# Function to turn off airplane mode
def turn_off_airplane_mode():
    if sys.platform == "win32":
        subprocess.Popen(["nircmd.exe", "setairport", "mode", "0"])
        speak("Airplane mode turned off.")
        speak("Sir! your task is completed.......")
    else:
        speak("Sorry, Sir! I'm unable to turn off airplane mode on this operating system.")

# Function to turn on Wi-Fi
def turn_on_wifi():
    if sys.platform == "win32":
        subprocess.Popen(["nircmd.exe", "setsubunitvolumedb", "10"])
        speak("Wi-Fi turned on.")
        speak("Sir! your task is completed......")
    else:
        speak("Sorry, Sir! I'm unable to turn on Wi-Fi on this operating system.")

# Function to turn off Wi-Fi
def turn_off_wifi():
    if sys.platform == "win32":
        subprocess.Popen(["nircmd.exe", "setsubunitvolumedb", "-10"])
        speak("Wi-Fi turned off.")
        speak("Sir! your task is completed.......")
    else:
        speak("Sorry, Sir! I'm unable to turn off Wi-Fi on this operating system.")

# Function to open Control panel
def open_control_panel():
    
    if sys.platform == "win32":
        speak("Opening Control panel...")
        subprocess.Popen("control", shell=True)
        speak("Sir! your task is completed.......")
    else:
        speak("Sorry, Sir! I'm unable to open the Control Panel on this operating system.")

# Function to open the web browser
def open_google():
    speak("Opening Google...")
    webbrowser.open('https://www.google.com')
    speak("Welcome to Google! the gateway to a world of knowledge and limitless possibilities. As you type your search query, remember that within this digital realm lies a wealth of information waiting to be discovered....")

# Function to open YouTube
def open_youtube():
    speak("Opening YouTube...")
    webbrowser.open('https://www.youtube.com')
    speak("Welcome to YouTube! where inspiration and knowledge await at every click. As you venture into this vast sea of videos, remember that you have the power to transform your screen into a gateway of endless possibilities....")

    # Function to search YouTube for a specific query
def search_youtube(query):
    search_query = query.replace("search youtube for", "").strip()
    speak("Searching YouTube for " + search_query + "...")
    webbrowser.open("https://www.youtube.com/results?search_query=" + search_query)

    

# Function to play a YouTube video
def play_youtube_video(query):
    try:
        pywhatkit.playonyt(query)
        speak("Playing YouTube video for: " + query)
    except Exception as e:
        print("An error occurred:", str(e))
        speak("Sorry, I couldn't play the YouTube video.")


# Function to open Facebook
def open_facebook():
    speak("Opening Facebook...")
    webbrowser.open('https://www.facebook.com')
    speak("Embrace this moment! as an opportunity to connect, inspire, and uplift. As you scroll through Facebook, remember that you have the power to make a positive impact on someone's day. Share your joy, spread kindness, and support others in their endeavors ......................")

# Function to open Instagram
def open_instagram():
    speak("Opening Instagram...")
    webbrowser.open('https://www.instagram.com')
    speak("Sir! your task is completed...")

    # Function to search Google Chrome for a specific URL
def search_google_chrome(command):
    url = command.replace("search Google Chrome for", "")
    speak(f"Searching Google Chrome for {url}...")
    webbrowser.get('google-chrome').open(url)
    speak("Sir! Here is your result...")

# Function to find a location using Google Maps
def find_location(command):
    location = command.replace("find location", "")
    speak(f"Searching Google Maps for {location}...")
    webbrowser.get('google-chrome').open(f"https://www.google.com/maps/search/{location}")
    speak("Sir! Here is that location...")

# Function to view Gmail
def view_gmail():
    speak("Opening Gmail...")
    webbrowser.open('https://mail.google.com')
    speak("...")

# Function to compose a mail in Gmail
def compose_mail():
    speak("Opening Gmail to compose a mail...")
    webbrowser.open('https://mail.google.com/mail/?view=cm&fs=1&tf=1')
    speak("Sir! you can compose your mail now...")

# Function to identify a number using Truecaller
def identify_number(command):
    number = command.replace("identify number", "")
    speak(f"Searching Truecaller for {number}...")
    webbrowser.open(f"https://www.truecaller.com/search/in/{number}")
    speak("Sir! Here is the result...")

# Function to create a spreadsheet using MS Excel
def create_spreadsheet():
    speak("Creating a spreadsheet using MS Excel...")
    os.startfile("excel.exe")
    speak("Sir! your task is completed...")

    # Function to create a word document using MS Word
def create_word_document():
    speak("Opening MS Word...")
    os.startfile("winword.exe")
    speak("Sir! your task is completed...")


# Function to get the weather report
def get_weather_report(command):
    location = command.replace("weather report for", "")
    speak(f"Searching weather report for {location}...")
    weather_api_key = "YOUR_WEATHER_API_KEY"
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}"
    response = requests.get(weather_url)
    weather_data = response.json()
    if weather_data["cod"] == "404":
        speak(f"Sorry, I couldn't find the weather report for {location}.")
    else:
        temperature = weather_data["main"]["temp"]
        temperature_celsius = temperature - 273.15
        description = weather_data["weather"][0]["description"]
        speak(f"The current temperature in {location} is {temperature_celsius:.1f} degrees Celsius with {description}.")
        speak("Sir! your task is completed...")

# Function to tell the current time
def tell_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {current_time}.")
    speak("Sir! your task is completed...")

    # Function to tell a random joke
def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who’s afraid of negative numbers? He’ll stop at nothing to avoid them!",
        "How do you organize a space party? You planet!",
        "I was gonna tell you a chemistry joke, but all the good ones are argon.",
        "Why do we never tell secrets on a farm? Because the potatoes have eyes and the corn has ears!"
    ]
    return random.choice(jokes)


# Function to search Wikipedia
def search_wikipedia(command):
    search_query = command.replace("search Wikipedia for", "")
    speak(f"Searching Wikipedia for {search_query}...")
    try:
        summary = wikipedia.summary(search_query, sentences=2)
        speak(summary)
    except wikipedia.DisambiguationError as e:
        options = e.options[:2]
        speak(f"Multiple options found for {search_query}. Here are a few: {', '.join(options)}")
    except wikipedia.PageError:
        speak(f"Sorry, Sir! I couldn't find any results for {search_query}")
        speak("Sir! your task is completed...")


def process_command(command):
    if 'hello sheild' in command:
        return "Hello! How can I assist you today?"

    # Generate a response using the ChatGPT 3.5 turbo model
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=command,
        max_tokens=50
    )
    return response.choices[0].text.strip()
        
        
# Function to play music
def play_music():
    # Add your music streaming API code here
    speak("Sorry, I can't play music at the moment.") 


# Function to ask for another task
def ask_for_another_task():
    speak("Is there anything else I can help you with?")

# Start the voice assistant
voice_assistant()                                                                      
