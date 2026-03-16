#import pyttsx3
import speech_recognition as sr
import requests
import smtplib
import schedule
import datetime
import wikipedia
import webbrowser
import time
import os
import pywhatkit
import json
import threading
from dotenv import load_dotenv

load_dotenv()

WAKE_WORD = "nova"

#text to speech
#engine = pyttsx3.init('nsss')
def speak(text):
    print("Assistant:",text)
    #engine.runAndWait()
    os.system(f'say "{text}"')

#speech recognition
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening....")
        r.adjust_for_ambient_noise(source,duration=0.5)
        audio = r.listen(source, timeout=20, phrase_time_limit=60)
    try:
        command = r.recognize_google(audio)
        print("user:",command)
        return command.lower()
    except sr.UnknownValueError:
        return ""

#wake func
def wait_for_wake_word():
    while True:
       command = listen()
       if command == "":
           continue
       print("Heard:",command)
       if WAKE_WORD in command:
        speak("Yes mousam, how can i help you?")
        return

#active mode
def active_mode():
    schedule.run_pending()
    while True:
        command = listen()
        if command == "":
            continue

        if "sleep" in command:
            speak("going back to sleep")
            return
        
        intent = detect_intent(command)

        if intent == "weather":
            speak("which city?")
            city = listen()
            if city == "":
                speak("I did not hear the city name.")
            else:
                get_weather(city)

        elif intent == "email":
            speak("Who should I send the email to?")
            name = listen()
            if name in contacts:
                receiver = contacts[name]
            else:
                speak("i don't have the contact.")
                continue
            speak("What should I say?")
            message = listen()
            send_email(receiver,message)

        elif intent == "knowledge":
            answer_question(command)

        elif intent == "greeting":
            speak("Hello Mousam! How can I help you?")

        elif intent == "open_app":
            open_app(command)

        elif intent == "time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {now}")

        elif intent == "reminder":
            speak("what should i remind you?")
            reminder = listen()
            set_reminder(reminder)
            
        elif intent == "google_search":
            speak("what should i search on google")
            query = listen()
            if query != "":
                google_search(query)

        elif intent == "thank_you":
            speak("Welcome. it's my pleasure")

        elif intent == "play_music":
            song = command.replace("play", "")
            play_music(song)

        elif intent == "exit":
            speak("Shutting down the session. goodbye!")
            os._exit(0)

        else:
            speak("i don't understand")
#natural language processing
def detect_intent(command):
    if any(word in command for word in["weather", "temperature", "forecast"]):
        return "weather"
    elif "hello" in command or "hi" in command:
        return "greeting"
    elif "send email" in command or "email" in command:
        return "email"
    elif "reminder" in command:
        return "reminder"
    elif "who is" in command or "what is" in command  or "tell me about" in command:
        return "knowledge"
    elif "open" in command:
        return "open_app"
    elif "time" in command:
        return "time"
    elif "google" in command or "search" in command:
        return "google_search"
    elif "exit" in command or "stop" in command:
        return "exit"
    elif "play" in command:
        return "play_music"
    elif "thanks" or "thank" in command:
        return "thank_you"
    else:
        return "unknown"
    
#weather api integration
API_KEY = os.getenv("API_KEY")
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    #print("API RESPONSE:", data)   

    if str(data["cod"]) != "200":
        speak("city not found")
        return
    
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    speak(f"The temperature in {city} is {temp} degree Celsius with {desc}")
    
#sending emails
contacts = json.loads(os.getenv("CONTACTS"))

email = os.getenv("EMAIL")
password = os.getenv("PASS")
def send_email(receiver, message):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, receiver, message)
    server.quit()
    speak("Email sent successfully")

#google search function
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here are the search results")

#reminder section 
def set_reminder(message):
    speak("reminder set")
    schedule.every(1).minutes.do(lambda: speak(message))

#schedular tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

#open app
def open_app(app_name):
    if "brave" in app_name:
        os.system("open -a 'Brave Browser'")
        speak("Opening brave")
    elif "safari" in app_name:
        os.system("open -a Safari")
        speak("Opening safari")
    elif "finder" in app_name:
        os.system("open -a Finder")
        speak("Opening finder")
    elif "calculator" in app_name:
        os.system("open -a Calculator")
        speak("Opening calculator")
    elif "phone" in app_name:
        os.system("open -a Phone")
        speak("Opening phone")
    elif "vscode" in app_name or "code" in app_name or "playground" in app_name:
        os.system("open -a 'Visual Studio Code'")
        speak(f"Opening {app_name}")
    elif "youtube" in app_name:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    else:
        speak("I don't know that application")

#play music,vedio
def play_music(query):
    speak(f"Playing {query} on Youtube")
    pywhatkit.playonyt(query)

#general knowledge
def answer_question(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        speak(result)
    except:
        speak("sorry, i could not find anything")

#smart home control
#def turn_on_lights():
    #requests.get("https://192.168.1.50/light/on")
    #speak("light turned on")

#main assistant loop
def assistant():

    while True:
        wait_for_wake_word()
        active_mode()

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    assistant()