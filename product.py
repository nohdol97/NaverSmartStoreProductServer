import pandas as pd
from datetime import datetime, timedelta
import os

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

    print(f"File created at: {output_file}")

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