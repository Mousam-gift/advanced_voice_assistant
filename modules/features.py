import requests
import webbrowser
import schedule
import wikipedia
import os
import pywhatkit
from modules.speech import speak



API_KEY = os.getenv("OPENWEATHER_API_KEY")
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

#google search function
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak("Here are the search results")

#reminder section 
def set_reminder(message):
    speak("reminder set")
    schedule.every(1).minutes.do(lambda: speak(message))

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
        speak("Opening Visual Studio Code")
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