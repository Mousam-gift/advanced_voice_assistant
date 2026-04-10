from modules.wake_word import wait_for_wake_word
from modules.commands import active_mode
from modules.scheduler import run_scheduler
import threading

def main():
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.daemon = True
    scheduler_thread.start()

    while True:
        wait_for_wake_word()
        active_mode()

if __name__ == "__main__":
    main()