import speech_recognition as sr
from modules.speech import speak, listen
from config import WAKE_WORD

def wait_for_wake_word():
    while True:
       command = listen()
       if command == "":
           continue
       print("Heard:",command)
       if WAKE_WORD in command:
        speak("Yes mousam, how can i help you?")
        return
