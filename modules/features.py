import requests
import webbrowser
import schedule
import os
import pywhatkit
import json
import threading
import subprocess
import re
import time
import datetime
from modules.speech import speak

APP_ALIASES = {
    "vscode": "Visual Studio Code",
    "code": "Visual Studio Code",
    "brave": "Brave Browser",
    "yt": "YouTube",
    "powerpoint": "Microsoft PowerPoint",
    "word": "Microsoft Word",
    "words": "Microsoft Word",
    "excel": "Microsoft Excel",
    "colab": "Google Colab",
    "whatsapp": "WhatsApp",
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEMORY_FILE = os.path.join(BASE_DIR, "data", "memory.json")

API_KEY = os.getenv("OPENWEATHER_API_KEY")
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.RequestException:
        speak("Sorry, I couldn't connect to the internet.")
        return
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
    def remind():
        speak(message)
        return schedule.CancelJob
    schedule.every(1).minutes.do(remind)

def _resolved_app_name(raw: str, strip_words: list[str]) -> str | None:
    pattern = r'\b(?:' + '|'.join(strip_words) + r')\b'
    cleaned = re.sub(pattern, '', raw, flags=re.IGNORECASE).strip()
    return APP_ALIASES.get(cleaned.lower(), cleaned if cleaned else None)

#open app
def open_app(app_name: str):
    resolved = _resolved_app_name(app_name, ["open", "launch", "start"])
    if not resolved:
        speak("Sorry, I couldn't determine which app to open.")
        return
    result = os.system(f"open -a '{resolved}'")
    speak(f"Opening {resolved}" if result == 0 else f"Sorry, I couldn't open {resolved}")

def close_app(app_name: str):
    resolved = _resolved_app_name(app_name, ["close", "quit", "exit"])
    if not resolved:
        speak("Sorry, I couldn't determine which app to close.")
        return
    result = os.system(f"osascript -e 'quit app \"{resolved}\"'")
    speak(f"Closing {resolved}" if result == 0 else f"Sorry, I couldn't close {resolved}")


#play music,vedio
def play_music(query):
    speak(f"Playing {query} on Youtube")
    pywhatkit.playonyt(query)

#general knowledge
# def answer_question(query):
#     try:
#         result = wikipedia.summary(query, sentences=2)
#         speak(result)
#     except:
#         speak("sorry, i could not find anything")

def ask_ollama(prompt, history=None):
    if history is None:
        history = []
    try:
        history_text = "\n".join([f"User: {h['user']}\nNova: {h['assistant']}"for h in history])

        full_prompt = f"""You are NOVA, a smart AI voice assistant.
Reply in 1-2 short sentences only.
Be clear, helpful, and conversational.
Previous conversation:
{history_text}

User: {prompt}"""
        response = requests.post("http://localhost:11434/api/generate", json={"model": "mistral", "prompt":full_prompt,"stream": False,"keep_alive": -1}, timeout=30)
        data = response.json()
        return data["response"].strip()
    except Exception as e:
        print("Error connecting to Ollama:", e)
        return "Sorry, I couldn't connect to AI."
    
def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_memory(key, value):
    data = load_memory()
    data[key] = value
    with open(MEMORY_FILE, "w") as f:
        json.dump(data,f)

def get_memory(key):
    data = load_memory()
    return data.get(key)

#music control
def music_control(command):
    if "youtube" in command:
        if "pause" in command or "resume" in command:
            os.system("osascript -e 'tell application \"System Events\" to key code 49'") #spacebar
            speak("Done")
        elif "next" in command:
            os.system("osascript -e 'tell application \"System Events\" to key code 124'")
            speak("next song") #right arrow
        elif "previous" in command or "back" in command:
            os.system("osascript -e 'tell application \"System Events\" to key code 123'")
            speak("previous song") #left arrow
        elif "volume up" in command or "louder" in command or "up" in command:
            os.system("osascript -e 'set volume output volume (output volume of (get volume settings) + 30)'")
            speak("volume up") #up arrow
        elif "volume down" in command or "low" in command or "down" in command:
            os.system("osascript -e 'set volume output volume (output volume of (get volume settings) - 30)'") #down arrow
            speak("volume down")
        elif "unmute" in command:
            os.system("osascript -e 'set volume output muted false'")
            speak("unmuted")
        elif "mute" in command:
            os.system("osascript -e 'set volume output muted true'")
            speak("muted")
        
    else:
        if "pause" in command:
            os.system("osascript -e 'tell application \"Music\" to pause'")
            speak("music paused")
        elif "resume" in command:
            os.system("osascript -e 'tell application \"Music\" to play'")
            speak("music playing")
        elif "next" in command:
            os.system("osascript -e 'tell application \"Music\" to next track'")
            speak("next song")
        elif "previous" in command or "back" in command:
            os.system("osascript -e 'tell application \"Music\" to previous track'")
            speak("previous song")
        elif "volume up" in command or "louder" in command or "up" in command:
            os.system("osascript -e 'tell application \"Music\" to set sound volume to (sound volume of application \"Music\") +30'")
            speak("volume up")
        elif "volume down" in command or "low" in command or "down" in command:
            os.system("osascript -e 'tell application \"Music\" to set sound volume to (sound volume of application \"Music\") -30'")
            speak("volume down")
        elif "mute" in command:
            os.system("osascript -e 'tell application \"Music\" to set sound volume to 0'")
            speak("muted")

def take_screenshot():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.expanduser(f"~/Desktop/screenshot_{timestamp}.png")
    result = os.system(f"screencapture -x '{filename}'")
    if result == 0:
        speak(f"Screenshot saved on Desktop as {timestamp}")
    else:
        speak("Sorry, failed to take screenshot")

def shutdown_mac():
    os.system("osascript -e 'tell app \"System Events\" to shut down'")

def restart_mac():
    os.system("osascript -e 'tell app \"System Events\" to restart'")

def set_timer(command: str):
    match = re.search(r'(\d+)\s*(seconds?|minutes?|hours?)', command, re.IGNORECASE)
    if not match:
        speak("Sorry, I couldn't understand the timer duration.")
        return
    
    amount = int(match.group(1))
    unit = match.group(2).lower().rstrip('s')  # Normalize to singular
    if "second" in unit:
        seconds = amount
    elif "minute" in unit:
        seconds = amount * 60
    elif "hour" in unit:
        seconds = amount * 3600

    label = f"{amount} {unit}{'s' if amount > 1 else ''}"

    speak(f"Timer set for {label}")

    def _run():
        threading.Event().wait(seconds)
        subprocess.run(["osascript", "-e",f'display notification \"Your {label} timer is done!\" with title \"NOVA Timer\" sound name "Glass"'])
        time.sleep(1)
        speak(f"Time's up! Timer for {label} is done!")
    threading.Thread(target=_run, daemon=True).start()