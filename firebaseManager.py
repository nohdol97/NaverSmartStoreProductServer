import firebase_admin
from firebase_admin import credentials, storage
import os

# 현재 작업 디렉토리 경로 가져오기
current_directory = os.getcwd()

# 서비스 계정 키 파일 경로
service_account_key_path = os.path.join(current_directory, "serviceAccountKey.json")
cred = credentials.Certificate(service_account_key_path)

firebase_admin.initialize_app(cred, {
    'storageBucket': 'navertrafficweb-fed26.appspot.com'
})

def download_file_from_firebase(file_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(file_name)
        output_file = os.path.join(current_directory, file_name)

        if not blob.exists():
            print(f"File {file_name} does not exist in Firebase Storage.")
            return

        blob.download_to_filename(output_file)
        print(f"File downloaded to {output_file}")
    except Exception as e:
        print(f"Exception in download_file_from_firebase: {e}")