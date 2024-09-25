import os
import time
from dotenv import load_dotenv
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 크롬 옵션 설정
chrome_options = Options()
#chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행, 현재 테스트 중이므로 주석처리함

# config.ini 파일 로드
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

# config.ini 파일에서 설정 값 불러오기
driver_path = config['selenium']['driver_path']
base_url = config['selenium']['base_url']

service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service, options=chrome_options)

# 스마트스토어 로그인 페이지 열기
driver.get(base_url)

# 페이지 로딩 대기 (필요에 따라 조정)
time.sleep(1)


# ID 입력 필드 선택
naver_id_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder='아이디 또는 이메일 주소']")
# 비밀번호 입력 필드 선택
naver_pw_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='비밀번호']")

# .env 파일 로드
load_dotenv()

# 환경 변수 불러오기
naver_id = os.getenv('NAVER_ID')
naver_pw = os.getenv('NAVER_PW')

# 로그인 폼 채우기
naver_id_input.send_keys(naver_id)  # 여기에 네이버 ID 입력
naver_pw_input.send_keys(naver_pw)  # 여기에 네이버 비밀번호 입력

time.sleep(1)

# 로그인 버튼 클릭
login_button = driver.find_element(By.CSS_SELECTOR, "button.Button_btn__enzXE.Button_btn_plain__1j7dG")
login_button.click()


# 로그인 후 페이지 로딩 대기
time.sleep(5)


# 작업이 끝나면 드라이버 종료
# driver.quit()
