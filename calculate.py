import pandas as pd
from datetime import datetime, timedelta
import os

def get_filtered_data():
    # 현재 작업 디렉토리 경로 가져오기
    current_directory = os.getcwd()
    
    # 파일 경로 설정
    file_path = os.path.join(current_directory, 'data.xlsx')

    # Excel 파일 읽기
    df = pd.read_excel(file_path)

    # 컬럼명을 이해하기 쉽게 영어로 변경
    df.columns = ['Store Name', 'Main Keyword', 'Product URL', 'MID', 'Source URL', 'Source MID', 'Start Date', 'End Date', 'Inbound Count', 'Note']

    # 오늘 날짜와 내일 날짜 계산
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    # 내일 날짜가 시작일보다 크고 종료일보다 작거나 같은 경우 필터링
    filtered_df = df[(df['Start Date'] < tomorrow) & (df['End Date'] >= tomorrow)]

    return filtered_df

def calculate_requests(df):
    requests_count = 0
    
    while df['Inbound Count'].sum() > 0:
        if df[df['Inbound Count'] >= 1000].shape[0] > 0:
            for index, row in df.iterrows():
                if row['Inbound Count'] >= 1000:
                    df.at[index, 'Inbound Count'] -= 1000
                    requests_count += 1
                    break
        else:
            count = 0
            for index, row in df.iterrows():
                if row['Inbound Count'] > 0:
                    take_amount = min(250, row['Inbound Count'])
                    df.at[index, 'Inbound Count'] -= take_amount
                    count += 1
                    if count == 3:
                        requests_count += 1
                        break

    return requests_count

def calculate():
    filtered_df = get_filtered_data()
    total_requests = calculate_requests(filtered_df)
    print(f"필요한 서버 수: {total_requests}")

if __name__ == "__main__":
    calculate()