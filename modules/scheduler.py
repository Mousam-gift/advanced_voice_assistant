import schedule
import time

#schedular tasks
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)