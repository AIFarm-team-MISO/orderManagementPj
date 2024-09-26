# 스마스스토어 api 정보
# 애플리케이션 ID : sIltmNvg6INzkAQw73puj
# 애플리케이션 시크릿 : $2a$04$MzPZ74rNjFxERQ34UplQ3.

import requests

# API 정보 설정
API_URL = "https://api.smartstore.com/v1/orders"  # 실제 API 엔드포인트로 변경
ACCESS_TOKEN = "your_access_token"  # 발급받은 액세스 토큰으로 변경

def get_orders():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
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
    orders = get_orders()
    # 추가적인 로직이 필요하다면 여기에서 처리