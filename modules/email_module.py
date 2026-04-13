import os
import smtplib
from email.mime.text import MIMEText
from modules.speech import speak
from dotenv import load_dotenv

load_dotenv()
#contacts = json.loads(os.getenv("CONTACTS", "{}"))
contacts = {}
for key, value in os.environ.items():
    if key.startswith("CONTACT_"):
        name = key.replace("CONTACT_", "").lower()
        contacts[name] = value

email = os.getenv("EMAIL")
password = os.getenv("PASS")
import os
import smtplib
from email.mime.text import MIMEText
from modules.speech import speak
from dotenv import load_dotenv

load_dotenv()
#contacts = json.loads(os.getenv("CONTACTS", "{}"))
contacts = {}
for key, value in os.environ.items():
    if key.startswith("CONTACT_"):
        name = key.replace("CONTACT_", "").lower()
        contacts[name] = value

email = os.getenv("EMAIL")
password = os.getenv("PASS")
import os
import smtplib
from email.mime.text import MIMEText
from modules.speech import speak
from dotenv import load_dotenv

load_dotenv()
#contacts = json.loads(os.getenv("CONTACTS", "{}"))
contacts = {}
for key, value in os.environ.items():
    if key.startswith("CONTACT_"):
        name = key.replace("CONTACT_", "").lower()
        contacts[name] = value

email = os.getenv("EMAIL")
password = os.getenv("PASS")
def send_email(receiver, message):
    try:
        msg = MIMEText(message)              # ✅ user ka message
        msg["Subject"] = "Message from NOVA"
        msg["From"] = email
        msg["To"] = receiver

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, receiver, msg.as_string())  # ✅ msg.as_string()
        server.quit()
        speak("Email sent successfully")
    except Exception as e:
        print("Email error:", e)
        speak("Sorry, I couldn't send the email")