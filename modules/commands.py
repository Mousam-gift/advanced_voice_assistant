import os
import time
import datetime
import schedule
from modules.speech import speak, listen
from modules.intent import detect_intent
from modules.email_module import send_email, contacts
from modules.features import get_weather, google_search, set_reminder, open_app, close_app, play_music, save_memory, get_memory, ask_ollama, music_control, take_screenshot, shutdown_mac, restart_mac, set_timer


conversation_history = []

def active_mode():
    
    while True:
        schedule.run_pending()
        command = listen()
        time.sleep(0.3)
        if command == "":
            continue
        #save name
        if "my name is" in command:
            name = command.replace("my name is ", "").strip()
            save_memory("name", name)
            speak(f"Nice to meet you {name}")
            continue
        #recall name
        if "what is my name" in command:
            name = get_memory("name")
            if name:
                speak(f"Your name is {name}")
            else:
                speak("I don't know your name yet.")
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
        elif intent == "greeting":
            speak("Hello! How can I help you?")

        elif intent == "open_app":
            open_app(command)

        elif intent == "close_app":
            close_app(command)

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

        elif intent == "music_control":
            music_control(command)

        elif intent == "screenshot":
            take_screenshot()

        elif intent == "shutdown":
            speak("are you sure you want to shut down the system?")
            if "yes" in listen():
                shutdown_mac()
            else:
                speak("shutdown cancelled")
        
        elif intent == "timer":
            set_timer(command)

        elif intent == "restart":
            speak("are you sure you want to restart the system?")
            if "yes" in listen():
                restart_mac()
            else:
                speak("restart cancelled")

        elif intent == "exit":
            conversation_history.clear()
            speak("Shutting down the session. goodbye!")
            os._exit(0)

        else:
            speak("let me think...")
            try:
                response = ask_ollama(command, conversation_history)
                conversation_history.append({"user": command, "assistant":response})
                if len(conversation_history)>10:
                    conversation_history.pop(0)
                speak(response)
            except Exception :
                speak("Sorry, I couldn't connect to A I.")