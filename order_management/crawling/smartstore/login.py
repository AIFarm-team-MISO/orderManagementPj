import time
from selenium.webdriver.common.by import By

def login_to_smartstore(driver, base_url, naver_id, naver_pw):
    # 스마트스토어 로그인 페이지 열기
    driver.get(base_url)

    # 페이지 로딩 대기
    time.sleep(1)

    # ID와 비밀번호 입력 필드 선택
    naver_id_input = driver.find_element(By.CSS_SELECTOR, "input[type='text'][placeholder='아이디 또는 이메일 주소']")
    naver_pw_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'][placeholder='비밀번호']")

    # 로그인 폼 채우기
    naver_id_input.send_keys(naver_id)
    naver_pw_input.send_keys(naver_pw)

    time.sleep(1)

    # 로그인 버튼 클릭
    login_button = driver.find_element(By.CSS_SELECTOR, "button.Button_btn__enzXE.Button_btn_plain__1j7dG")
    login_button.click()

    # 로그인 후 페이지 로딩 대기
    time.sleep(10)
