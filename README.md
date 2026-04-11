
# 🎙️ Advanced AI Voice Assistant (NOVA)

An intelligent voice-controlled assistant built using Python with local AI (Mistral via Ollama), wake word detection, and system automation.

---

## 🚀 Features

- 🎤 Wake word detection ("Nova")
- 🔊 Text-to-speech response
- 🧠 AI responses via Mistral (Ollama - runs locally)
- 🌐 Google search & web browsing
- 🖥️ Open & close any app by voice
- 📧 Send emails by voice
- ⏰ Reminders & scheduler
- 🎵 Play music on YouTube
- 🌤️ Weather updates
- 💾 Memory (remembers your name)

---

## 🧠 Tech Stack

- Python 3.x
- SpeechRecognition + PyAudio
- pyttsx3
- Ollama (Mistral LLM - local)
- OpenWeatherMap API
- pywhatkit, wikipedia, requests

---

## ⚙️ How It Works

1. Say **"Nova"** to wake the assistant
2. Give a voice command
3. NOVA processes it and responds
4. Say **"sleep"** to put it back to sleep

---

## ▶️ Run Locally

### Prerequisites (macOS)
```bash
brew install portaudio
brew install ollama
ollama pull mistral
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
advanced_voice_assistant/
│── modules/
│   ├── commands.py
│   ├── features.py
│   ├── intent.py
│   ├── speech.py
│   ├── wake_word.py
│   ├── scheduler.py
│   └── email_module.py
│── data/
│── config.py
│── main.py
│── requirements.txt
│── README.md

---

## 🧪 Example Commands

- "Open Safari" / "Close Safari"
- "Search Python tutorials"
- "What is the weather in Delhi"
- "Play lo-fi music"
- "Set a reminder"
- "What is machine learning"
- "Send email"

---

## ⚠️ Limitations

- Works best in quiet environments
- Ollama must be running locally
- macOS optimized (open/close app commands)

---

## 📌 Author

**Mousam Das** — AI/ML Developer  
[GitHub](https://github.com/Mousam-gift)

---

## ⭐ Show your support

If you like this project, give it a ⭐ on GitHub!
