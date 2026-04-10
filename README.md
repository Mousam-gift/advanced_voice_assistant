# 🎙️ Advanced AI Voice Assistant

An intelligent voice-controlled assistant built using Python that can understand user commands and perform tasks like opening applications, searching the web, and automating daily activities.

---

## 🚀 Features

- 🎤 Voice recognition (speech-to-text)
- 🔊 Text-to-speech response system
- 🌐 Open websites and perform Google searches
- 🖥️ System automation (open apps, files, etc.)
- 🧠 Basic command understanding (NLP logic)
- ⚡ Real-time interaction with wake word detection
- ⏰ Background task scheduler

---

## 🧠 Tech Stack

- Python 3.x
- SpeechRecognition
- pyttsx3
- pyaudio
- openai
- wikipedia
- python-dotenv
- requests

---

## ⚙️ How It Works

1. Assistant listens for a **wake word**
2. Converts speech into text using SpeechRecognition
3. Processes the command using predefined logic
4. Executes the task (open app, search, etc.)
5. Responds using text-to-speech

---

## ▶️ Run Locally

### Prerequisites (macOS)
```bash
brew install portaudio
```

### Setup
```bash
git clone https://github.com/Mousam-gift/advanced_voice_assistant.git
cd advanced_voice_assistant
pip install -r requirements.txt
python main.py
```

---

## 📁 Project Structure
