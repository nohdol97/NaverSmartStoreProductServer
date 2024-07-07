import pandas as pd
from datetime import datetime, timedelta
from flask import Flask, jsonify
import os
import schedule
import time
from threading import Thread
import random

app = Flask(__name__)

def get_product():
    # 현재 작업 디렉토리 경로 가져오기
    current_directory = os.getcwd()
    
    # 파일 경로 설정
    file_path = os.path.join(current_directory, 'data.xlsx')
    output_file = os.path.join(current_directory, 'product.txt')

    # Excel 파일 읽기
    df = pd.read_excel(file_path)

    # 컬럼명을 이해하기 쉽게 영어로 변경
    df.columns = ['Store Name', 'Main Keyword', 'Product URL', 'MID', 'Source URL', 'Source MID', 'Start Date', 'End Date', 'Inbound Count', 'Note']

    # 한국 시간으로 오늘 날짜와 내일 날짜 계산
    today_korea = datetime.now() + timedelta(hours=9)
    tomorrow_korea = today_korea + timedelta(days=1)

    # 내일 날짜가 시작일보다 크고 종료일보다 작거나 같은 경우 필터링
    filtered_df = df[(df['Start Date'] < tomorrow_korea) & (df['End Date'] >= tomorrow_korea)]

    # 필터링된 데이터를 지정된 형식으로 product.txt 파일에 작성
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, row in filtered_df.iterrows():
            if pd.notna(row['Source MID']):
                line = f"{int(row['MID'])},{int(row['Source MID'])},{row['Main Keyword']},{int(row['Inbound Count'])}\n"
            else:
                line = f"{int(row['MID'])},{row['Main Keyword']},{int(row['Inbound Count'])}\n"
            file.write(line)

    # 생성된 파일 경로 출력
    print(f"File created at: {output_file}")

# 일정한 시간에 get_product 함수를 실행하기 위해 스케줄 설정
schedule.every().day.at("02:00").do(get_product)  # 한국 시간으로 11시 (UTC 시간으로는 02시)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# 스케줄러를 별도의 스레드로 실행
scheduler_thread = Thread(target=run_scheduler)
scheduler_thread.start()

@app.route('/get_product', methods=['GET'])
def serve_product():
    try:
        response = get_requested_products()
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_requested_products():
    output_file = 'product.txt'
    products = []
    
    with open(output_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split(',')
        if len(parts) == 3:
            mid, keyword, count = parts
            products.append([mid, keyword, int(count)])
        elif len(parts) == 4:
            mid, sub_mid, keyword, count = parts
            products.append([mid, sub_mid, keyword, int(count)])
    
    high_priority = [p for p in products if p[-1] >= 1000]
    low_priority = [p for p in products if p[-1] < 1000]

    result = []

    # 1000 이상인 항목 처리
    for product in high_priority:
        if product[-1] >= 1000:
            result.append(product[:-1] + [1000])
            product[-1] -= 1000
            break

    # 1000 이하인 항목 처리
    if not result:
        low_priority = sorted(low_priority, key=lambda x: x[-1], reverse=True)
        count = 0
        for product in low_priority:
            if count < 3 and product[-1] > 0:
                take_amount = min(250, product[-1])
                result.append(product[:-1] + [take_amount])
                product[-1] -= take_amount
                count += 1
            if count >= 3:
                break

    # product.txt 업데이트
    with open(output_file, 'w', encoding='utf-8') as file:
        for product in products:
            if len(product) == 4:
                file.write(f"{product[0]},{product[1]},{product[2]},{product[3]}\n")
            else:
                file.write(f"{product[0]},{product[1]},{product[2]}\n")

    if not result:
        return {"data": "No products available"}
    else:
        return {"data": result}

@app.route('/get_ip', methods=['GET'])
def get_ip():
    try:
        # proxyIp.txt 파일 읽기
        with open('proxyIp.txt', 'r', encoding='utf-8') as file:
            proxies = file.readlines()
        
        # 공백 제거
        proxies = [proxy.strip() for proxy in proxies]
        
        # 리스트 셔플
        random.shuffle(proxies)
        
        return jsonify({"proxies": proxies})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)