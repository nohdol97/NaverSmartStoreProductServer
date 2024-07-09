import schedule
import time
from threading import Thread
from productManager import get_product
from firebaseManager import download_file_from_firebase

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    # 23시 35분에 data.xlsx 파일 다운로드
    schedule.every().day.at("23:35").do(download_file_from_firebase, 'data.xlsx')
    
    # 23시 40분에 get_product 실행
    schedule.every().day.at("23:40").do(get_product)
    
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

if __name__ == "__main__":
    start_scheduler()