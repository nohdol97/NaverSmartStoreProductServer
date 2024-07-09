import schedule
import time
from threading import Thread, Event
from datetime import datetime
from productManager import get_product
from firebaseManager import download_file_from_firebase

def run_scheduler(stop_event):
    while not stop_event.is_set():
        now = datetime.now()
        # 22:00:00에 data.xlsx 파일 다운로드
        if now.hour == 22 and now.minute == 0 and now.second == 0:
            try:
                download_file_from_firebase('data.xlsx')
            except Exception as e:
                print(f"Exception in download_file_from_firebase: {e}")
            time.sleep(1)  # 1초 대기하여 중복 실행 방지
        
        # 23:00:00에 get_product 실행
        if now.hour == 23 and now.minute == 0 and now.second == 0:
            try:
                get_product()
            except Exception as e:
                print(f"Exception in get_product: {e}")
            time.sleep(1)  # 1초 대기하여 중복 실행 방지

        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    stop_event = Event()
    scheduler_thread = Thread(target=run_scheduler, args=(stop_event,))
    scheduler_thread.start()
    return stop_event, scheduler_thread