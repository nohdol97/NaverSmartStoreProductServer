import schedule
import time
from threading import Thread
from manageProduct import get_product

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    schedule.every().day.at("23:40").do(get_product)
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()