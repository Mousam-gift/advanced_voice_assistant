import os
import speech_recognition as sr

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
