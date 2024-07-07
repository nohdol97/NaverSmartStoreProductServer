import schedule
import time
from threading import Thread
from manageProduct import get_product

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    schedule.every().day.at("02:00").do(get_product)  # 한국 시간으로 11시 (UTC 시간으로는 02시)
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()