from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#import pyautogui  # 비밀번호 입력 자동화를 위해 사용
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from ...config_loader import switch_to_iframe, switch_to_default_content

def wait_for_download_to_complete(download_path, timeout=30):
    """
    파일 다운로드 완료 여부를 확인하는 함수
    """
    print('엑셀다운로드완료 timeout : ', timeout)

    start_time = time.time()
    while True:
        # 다운로드 경로에서 .crdownload 확장자가 없는 파일이 나타나면 완료로 간주
        files = os.listdir(download_path)
        if any(file.endswith('.xlsx') for file in files) and not any(file.endswith('.crdownload') for file in files):
            return True
        elif time.time() - start_time > timeout:
            return False
        time.sleep(1)

def download_excel_with_password(driver, password, download_path, timeout=30):
    try:

        print('엑셀다운로드 timeout : ', timeout)
        
        # iframe 으로의 전환
        # 현재 주문예정 페이지에서는 페이지 및 팝업 모두 하나의 ifram으로 감싸져 있는것 같으므로 
        # 모든 작업을 iframe으로 전환후 실행하고 이페이지를 벗어날때 iframe을 해제하자 
        switch_to_iframe(driver, 'iframe', timeout)


        # 엑셀다운 버튼 클릭
        excel_download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='엑셀다운']/ancestor::button"))
        )
        excel_download_button.click()
        print("엑셀다운 버튼 클릭 완료")

        
        print("첫 번째 비밀번호 입력 필드 대기")
        # 첫 번째 비밀번호 입력 필드 대기 및 입력
        password_input_1 = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='비밀번호']/following-sibling::input[@type='password']"))
        )
        password_input_1.send_keys(password)
        print("첫 번째 비밀번호 입력 완료")

        # 두 번째 비밀번호 입력 필드 대기 및 입력 (비밀번호 재확인)
        password_input_2 = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='재확인']/following-sibling::input[@type='password']"))
        )
        password_input_2.send_keys(password)
        print("비밀번호 재확인 입력 완료")

        # 다운로드 버튼 클릭
        download_button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button._rydLWC3ccz._Ue9WKGXozM"))
        )
        download_button.click()
        print("다운로드 버튼 클릭 완료")


        # 기본 프레임으로 전환
        switch_to_default_content(driver)

        # 다운로드 완료 여부 확인
        if not wait_for_download_to_complete(download_path, timeout):
            raise Exception("파일 다운로드가 완료되지 않았습니다.")
        print("엑셀 파일 다운로드 완료")


    except Exception as e:
        print(f"엑셀다운 버튼 실행 중 오류 발생: {e}")