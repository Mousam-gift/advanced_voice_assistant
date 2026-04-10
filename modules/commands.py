import os
import time
import datetime
import schedule
from modules.speech import speak, listen
from modules.intent import detect_intent
from modules.email_module import send_email, contacts
from modules.features import get_weather, google_search, set_reminder, open_app, play_music
from modules.features import answer_question


def active_mode():
    
    while True:
        schedule.run_pending()
        command = listen()
        time.sleep(0.3)
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