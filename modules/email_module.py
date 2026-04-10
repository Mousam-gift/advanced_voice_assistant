import os
import json
import smtplib
from modules.speech import speak
from dotenv import load_dotenv

load_dotenv()
contacts = json.loads(os.getenv("CONTACTS", "{}"))

email = os.getenv("EMAIL")
password = os.getenv("PASS")
def send_email(receiver, message):
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, receiver, message)
    server.quit()
    speak("Email sent successfully")