from flask import Flask, request, jsonify
from openpyxl import load_workbook
import firebase_admin
from firebase_admin import credentials, storage
import os

def download_excel_from_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob('data.xlsx')
    blob.download_to_filename(file_path)

def upload_excel_to_firebase(file_path):
    bucket = storage.bucket()
    blob = bucket.blob('data.xlsx')
    blob.upload_from_filename(file_path)

def copy_cell_styles(source_cell, target_cell):
    if source_cell.has_style:
        target_cell.font = source_cell.font
        target_cell.border = source_cell.border
        target_cell.fill = source_cell.fill
        target_cell.number_format = source_cell.number_format
        target_cell.protection = source_cell.protection
        target_cell.alignment = source_cell.alignment

def process_and_update_excel(existing_file_path, new_file_path):
    # Load existing and new workbooks
    existing_wb = load_workbook(existing_file_path)
    new_wb = load_workbook(new_file_path)
    
    existing_ws = existing_wb.active
    new_ws = new_wb.active

    # 검증된 헤더 목록
    expected_headers = ['총판', '대행사', '셀러', '메인 키워드', '서브 키워드', '상품 URL', 'MID값', '원부 URL', '원부 MID값', '시작일', '종료일', '유입수']
    
    # 헤더 검증
    headers = [cell.value for cell in new_ws[1]]
    if headers != expected_headers:
        return False, "올바른 형식의 파일이 아닙니다."

    # Get current max identifier
    current_max_identifier = existing_ws.max_row

    # Copy new data to existing sheet
    for row in new_ws.iter_rows(min_row=2, values_only=False):
        if row[0].value == 'Example':
            continue
        current_max_identifier += 1
        new_row = [current_max_identifier] + [cell.value for cell in row]
        
        for col_index, cell in enumerate(new_row, start=1):
            new_cell = existing_ws.cell(row=current_max_identifier, column=col_index)
            new_cell.value = cell
            copy_cell_styles(row[col_index - 1], new_cell)

    existing_wb.save(existing_file_path)
    return True, "파일이 성공적으로 업로드되었습니다."