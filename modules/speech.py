#import os
import time
import subprocess
import speech_recognition as sr

def speak(text):
    print("Assistant:",text)
    #engine.runAndWait()
    process = subprocess.Popen(['say',text])
    process.wait()
    time.sleep(0.5)

#speech recognition
def listen():
    r = sr.Recognizer()
    r.energy_threshold = 300
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("listening....")
        r.adjust_for_ambient_noise(source,duration=0.3)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=20)
        except sr.WaitTimeoutError:
            return ""
    try:
        command = r.recognize_google(audio)
        print("user:",command)
        return command.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""
