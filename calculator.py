import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def get_filtered_data():
    # 현재 작업 디렉토리 경로 가져오기
    current_directory = os.getcwd()
    
    # 파일 경로 설정
    file_path = os.path.join(current_directory, 'data.xlsx')

    # Excel 파일 읽기
    df = pd.read_excel(file_path)

    # 컬럼명을 이미지에 맞게 변경
    df.columns = [
        '총판', '대행사', '셀러', '메인 키워드', '서브 키워드', '상품 URL',
        'MID값', '원부 URL', '원부 MID값', '시작일', '종료일', '유입수'
    ]

    # 오늘 날짜와 내일 날짜 계산
    today = datetime.now()
    tomorrow = today + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')

    # 내일 날짜가 시작일보다 크고 종료일보다 작거나 같은 경우 필터링
    filtered_df = df[(df['시작일'] <= tomorrow_str) & (df['종료일'] >= tomorrow_str)]

    return filtered_df

def calculate_requests(df):
    total_inbound_count = df['유입수'].sum()
    return total_inbound_count

def calculate():
    filtered_df = get_filtered_data()
    total_requests = calculate_requests(filtered_df)
    print(f"총 필요 유입수: {total_requests}")
    print(f"총 필요 서버수(8100 기준): {total_requests/8100}")

if __name__ == "__main__":
    calculate()