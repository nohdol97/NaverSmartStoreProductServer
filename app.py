from flask import Flask, request, jsonify
from productManager import get_requested_products
from proxy import get_shuffled_proxies
from scheduler import start_scheduler
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

if __name__ == '__main__':
    stop_event, scheduler_thread = start_scheduler()
    app.run(host='0.0.0.0', port=5000)

    # 스케줄러를 안전하게 종료할 수 있도록 보장
    stop_event.set()
    scheduler_thread.join()