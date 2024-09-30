import time
from selenium.webdriver.common.by import By

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def login_to_smartstore(driver, base_url, naver_id, naver_pw, timeout):
    # 스마트스토어 로그인 페이지 열기
    driver.get(base_url)

    # 페이지 로딩 대기 (특정 요소가 나타날 때까지 기다림)
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text'][placeholder='아이디 또는 이메일 주소']"))
        )
        print("로그인 페이지 로딩 완료")
    except TimeoutException:
        print(f"{timeout}초 내에 로그인 페이지를 로드하지 못했습니다.")
        return

    # ID와 비밀번호 입력 필드 선택
    naver_id_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder='아이디 또는 이메일 주소']")
    naver_pw_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='비밀번호']")

    # 로그인 폼 채우기
    naver_id_input.send_keys(naver_id)
    naver_pw_input.send_keys(naver_pw)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.CSS_SELECTOR, "button.Button_btn__enzXE.Button_btn_plain__1j7dG")
    login_button.click()

    # 로그인 후 특정 요소가 나타날 때까지 대기 (예: 로그인 후 나타나는 특정 페이지 요소)
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "로그인 후 나타나는 특정 요소의 CSS 선택자"))
        )
        print("로그인 후 페이지 로딩 완료")
    except TimeoutException:
        print(f"{timeout}초 내에 로그인 후 페이지를 로드하지 못했습니다.")
        return

    # 로그인 후 페이지 타이틀 출력
    print(f"로그인 후 페이지 타이틀: {driver.title}")
