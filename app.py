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
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and file.filename.endswith('.xlsx'):
        existing_file_path = 'data.xlsx'
        new_file_path = 'uploaded_data.xlsx'

        # Download existing file from Firebase
        excelManager.download_excel_from_firebase(existing_file_path)
        
        # Save uploaded file
        file.save(new_file_path)

        # Process and update the Excel file
        success, message = excelManager.process_and_update_excel(existing_file_path, new_file_path)

        if not success:
            os.remove(new_file_path)
            os.remove(existing_file_path)
            return jsonify({'message': message}), 400

        # Upload updated file back to Firebase
        excelManager.upload_excel_to_firebase(existing_file_path)

        # Cleanup
        os.remove(new_file_path)
        os.remove(existing_file_path)

        return jsonify({'message': message}), 200

    return jsonify({'message': 'Invalid file format'}), 400

if __name__ == '__main__':
    start_scheduler()
    app.run(host='0.0.0.0', port=5000)
