import time
import requests
import json
import hashlib

# 애플리케이션 정보
CLIENT_ID = "sIltmNvg6INzkAQw73puj"
CLIENT_SECRET = "$2a$04$MzPZ74rNjFxERQ34UplQ3."
#TOKEN_URL = "https://openapi.naver.com/v1/oauth2/token"
TOKEN_URL = "https://openapi.naver.com/v1/nid/me/oauth2/token"

access_token = None
token_expiry = 0  # 토큰 만료 시간(타임스탬프)

def generate_client_secret_sign(timestamp):
    # 예시: 전자서명 생성 방법에 따라 이 부분을 수정하세요.
    message = f"{CLIENT_ID}{timestamp}"
    signature = hashlib.sha256((message + CLIENT_SECRET).encode('utf-8')).hexdigest()
    return signature

def get_access_token():
    global access_token, token_expiry
    timestamp = int(time.time() * 1000)  # 밀리초 단위로 변환
    client_secret_sign = generate_client_secret_sign(timestamp)

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret_sign": client_secret_sign,
        "timestamp": timestamp,
        "type": "SELLER SELF"  # 또는 "SELF" 필요에 따라 변경
        # "account_id": "판매자 ID"  # 필요시 추가
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get("access_token")
        expires_in = token_info.get("expires_in")  # 토큰 만료 시간(초)
        token_expiry = time.time() + expires_in  # 현재 시간 + 만료 시간
        print("새 액세스 토큰 발급:", access_token)
    else:
        print("토큰 발급 오류:", response.status_code, response.text)

def is_token_expired():
    return time.time() >= token_expiry

if __name__ == "__main__":
    get_access_token()