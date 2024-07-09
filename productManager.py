import pandas as pd
from datetime import datetime, timedelta
import os, random

def get_product():
    # 현재 작업 디렉토리 경로 가져오기
    current_directory = os.getcwd()
    
    # 파일 경로 설정
    file_path = os.path.join(current_directory, 'data.xlsx')
    output_file = os.path.join(current_directory, 'product.txt')

    # Excel 파일 읽기
    df = pd.read_excel(file_path)

    # 컬럼명을 이미지에 맞게 변경
    df.columns = [
        '식별번호', '총판', '대행사', '셀러', '메인 키워드', '서브 키워드', 
        '상품 URL', 'MID값', '원부 URL', '원부 MID값', '시작일', '종료일', '유입수'
    ]

    # 오늘 날짜와 내일 날짜 계산
    today = datetime.now()
    tomorrow = today + timedelta(days=1)

    # 내일 날짜가 시작일보다 크고 종료일보다 작거나 같은 경우 필터링
    filtered_df = df[(df['시작일'] < tomorrow) & (df['종료일'] >= tomorrow)]

    # 필터링된 데이터를 지정된 형식으로 product.txt 파일에 작성
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, row in filtered_df.iterrows():
            if pd.notna(row['원부 MID값']):
                line = f"{int(row['MID값'])},{int(row['원부 MID값'])},{row['메인 키워드']},{int(row['유입수'])}\n"
            else:
                line = f"{int(row['MID값'])},{row['메인 키워드']},{int(row['유입수'])}\n"
            file.write(line)

    print(f"File created at: {output_file}")

def get_requested_products():
    output_file = 'product.txt'
    products = []

    # Debugging: 파일 읽기 확인
    print(f"Reading from {output_file}")

    try:
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
        
        high_priority = [p for p in products if p[-1] >= 250]
        
        result = []

        if len(high_priority) >= 3:
            selected_products = random.sample(high_priority, 3)
            for product in selected_products:
                result.append(product[:-1] + [250])
                product[-1] -= 250
        else:
            total_sum = sum(p[-1] for p in high_priority)
            if total_sum >= 750:
                count = 0
                for product in high_priority:
                    if count < 750:
                        take_amount = min(750 - count, product[-1])
                        result.append(product[:-1] + [take_amount])
                        product[-1] -= take_amount
                        count += take_amount
            else:
                for product in high_priority:
                    result.append(product[:-1] + [product[-1]])
                    product[-1] = 0

        # product.txt 업데이트
        with open(output_file, 'w', encoding='utf-8') as file:
            for product in products:
                if len(product) == 4:
                    file.write(f"{product[0]},{product[1]},{product[2]},{product[3]}\n")
                else:
                    file.write(f"{product[0]},{product[1]},{product[2]}\n")

        # Debugging: 결과 확인
        print(f"Result: {result}")

        if not result:
            return {"data": []}
        else:
            return {"data": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"data": []}
    
get_product()