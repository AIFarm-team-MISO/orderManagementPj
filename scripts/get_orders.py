import requests
from get_access_token import get_access_token  # 액세스 토큰을 가져오는 함수 임포트

# API 정보 설정
API_URL = "https://api.smartstore.com/v1/orders"  # 실제 API 엔드포인트로 변경

def get_orders(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(API_URL, headers=headers)
        
        if response.status_code == 200:
            orders = response.json()
            print("주문 목록:", orders)
            return orders
        else:
            print("오류 발생:", response.status_code, response.text)
            return None
    except Exception as e:
        print("예외 발생:", str(e))
        return None

if __name__ == "__main__":
    access_token = get_access_token()  # 액세스 토큰을 발급받음
    if access_token:
        get_orders(access_token)  # 주문 목록 조회