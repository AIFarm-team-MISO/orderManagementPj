# 업체코드 : A00256672
# Access Key : 64278013-5673-47cc-9f22-5108a79590fa	
# Secret Key : 1f5d518e620d5536fa70d599c1c64465ecf85855
# 일단 코드는 완성되었으나 업체가 1군데만 사용가능해서 접송이 안됨. 현재 이셀러스로 사용중이어서 더이상 추가가 안되니 쿠팡은 일단 보류 

import requests
import time
import hmac
import hashlib
from datetime import datetime, timezone
import urllib.parse


# 쿠팡 API 설정
ACCESS_KEY = '64278013-5673-47cc-9f22-5108a79590fa'  # 여기에 쿠팡 API Access Key를 입력하세요
SECRET_KEY = '1f5d518e620d5536fa70d599c1c64465ecf85855'  # 여기에 쿠팡 API Secret Key를 입력하세요
VENDOR_ID = 'A00256672'    # 여기에 Vendor ID를 입력하세요

# 엔드포인트 설정
path = f'/v2/providers/openapi/apis/api/v4/vendors/{VENDOR_ID}/ordersheets'
query_params = {
    "createdAtFrom": "2024-09-01",
    "createdAtTo": "2024-09-23",
    "status": "UC"
}
query = urllib.parse.urlencode(query_params)

# 메시지 생성
timestamp = datetime.now(timezone.utc).strftime('%y%m%dT%H%M%SZ')
message = f'{timestamp}GET{path}{query}'

# 서명 생성
signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()

# Authorization 헤더 생성
authorization = f'CEA algorithm=HmacSHA256, access-key={ACCESS_KEY}, signed-date={timestamp}, signature={signature}'

# 요청 URL
url = f'https://api-gateway.coupang.com{path}?{query}'

# 요청 보내기
headers = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Authorization': authorization
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")