from modules.wake_word import wait_for_wake_word
from modules.commands import active_mode
from modules.scheduler import run_scheduler
from modules.features import ask_ollama
from modules.intent import detect_intent
import threading
import time
import requests
import subprocess


def ensure_ollama_running():
        try:
            requests.get("http://localhost:11434", timeout=2)
            print("Ollama server is running.")
        except requests.exceptions.ConnectionError:
            print("Starting Ollama server...")
            subprocess.Popen(["ollama", "serve"])
            time.sleep(3)
            print("Ollama server started.")

def main():
    ensure_ollama_running()
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    while True:
        wait_for_wake_word()
        active_mode()

if __name__ == "__main__":
    main()