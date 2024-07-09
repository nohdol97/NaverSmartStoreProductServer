from flask import Flask, request, jsonify
from productManager import get_requested_products
from proxy import get_shuffled_proxies
from scheduler import start_scheduler
import excelManager
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_product', methods=['GET'])
def serve_product():
    try:
        response = get_requested_products()
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_ip', methods=['GET'])
def get_ip():
    try:
        proxies = get_shuffled_proxies()
        return jsonify({"proxies": proxies})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/updateExcel', methods=['POST'])
def update_excel():
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No file part'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'No selected file'}), 400

        if file and file.filename.endswith('.xlsx'):
            existing_file_path = 'data.xlsx'
            new_file_path = 'uploaded_data.xlsx'

            excelManager.download_excel_from_firebase(existing_file_path)
            
            try:
                file.save(new_file_path)
                # 파일 유효성 검사
                excelManager.load_workbook(new_file_path)
            except Exception as e:
                if os.path.exists(new_file_path):
                    os.remove(new_file_path)
                return jsonify({'message': f'Invalid Excel file: {e}'}), 400

            success, message = excelManager.process_and_update_excel(existing_file_path, new_file_path)

            if not success:
                os.remove(new_file_path)
                os.remove(existing_file_path)
                return jsonify({'message': message}), 400

            excelManager.upload_excel_to_firebase(existing_file_path)

            # Cleanup
            os.remove(new_file_path)
            os.remove(existing_file_path)

            return jsonify({'message': message}), 200

        return jsonify({'message': 'Invalid file format'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    start_scheduler()
    app.run(host='0.0.0.0', port=5000)
