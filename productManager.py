import pandas as pd
from datetime import datetime, timedelta
import os, random

def get_product(file_name):
    # 현재 작업 디렉토리 경로 가져오기
    current_directory = os.getcwd()
    
    # 파일 경로 설정
    file_path = os.path.join(current_directory, 'data.xlsx')
    output_file = os.path.join(current_directory, file_name)

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

    # 필터링된 데이터를 지정된 형식으로 product.txt 파일에 작성
    with open(output_file, 'w', encoding='utf-8') as file:
        for index, row in filtered_df.iterrows():
            if pd.notna(row['원부 MID값']):
                line = f"{int(row['MID값'])},{int(row['원부 MID값'])},{row['메인 키워드']},{int(row['유입수'])}\n"
            else:
                line = f"{int(row['MID값'])},{row['메인 키워드']},{int(row['유입수'])}\n"
            file.write(line)

    print(f"File created at: {output_file}")

def get_requested_products(requested_amount, unit):
    output_file = 'product.txt'
    # Debugging: 파일 읽기 확인
    print(f"Reading from {output_file}")

    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        random.shuffle(lines)

        product_dict = {}

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 3:
                mid, keyword, count = parts
                key = (mid, None)
                if key not in product_dict:
                    product_dict[key] = [mid, keyword, int(count)]
                else:
                    product_dict[key][-1] += int(count)
            elif len(parts) == 4:
                mid, sub_mid, keyword, count = parts
                key = (mid, sub_mid)
                if key not in product_dict:
                    product_dict[key] = [mid, sub_mid, keyword, int(count)]
                else:
                    product_dict[key][-1] += int(count)

        result = []
        total_count = 0

        while total_count < requested_amount and product_dict:
            for key in list(product_dict.keys()):
                if total_count >= requested_amount:
                    break
                product = product_dict[key]
                if product[-1] > 0:
                    take_amount = min(unit, product[-1], requested_amount - total_count)

                    added = False
                    for res in result:
                        if res[0] == product[0] and (len(res) == 3 or (len(res) == 4 and res[1] == product[1])):
                            res[-1] += take_amount
                            added = True
                            break

                    if not added:
                        if len(product) == 4:
                            result.append([product[0], product[1], product[2], take_amount])
                        else:
                            result.append([product[0], product[1], take_amount])

                    product[-1] -= take_amount
                    total_count += take_amount

                    if product[-1] == 0:
                        del product_dict[key]

        # product.txt 업데이트
        with open(output_file, 'w', encoding='utf-8') as file:
            for key, product in product_dict.items():
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
    
def get_products_for_id():
    output_file = 'product_for_id.txt'

    # Debugging: 파일 읽기 확인
    print(f"Reading from {output_file}")

    try:
        result = []
        with open(output_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        random.shuffle(lines)

        for line in lines:
            parts = line.strip().split(',')
            if len(parts) == 4:
                result.append([parts[0], parts[1], parts[2]])
            else:
                result.append([parts[0], parts[1]])

        # Debugging: 결과 확인
        print(f"Result: {result}")

        if not result:
            return {"data": []}
        else:
            return {"data": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"data": []}

if __name__ == "__main__":
    get_product()