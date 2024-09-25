import os
import configparser
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_config():

    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
    config.read(config_path, encoding='utf-8')  # 인코딩을 명시적으로 설정

    return config

def load_env():
    load_dotenv()
    naver_id = os.getenv('NAVER_ID')
    naver_pw = os.getenv('NAVER_PW')
    excel_pw = os.getenv('EXCEL_PASSWORD')
    excel_download_url = os.getenv('EXCEL_DOWNLOD_URL')

    return naver_id, naver_pw, excel_pw, excel_download_url


def switch_to_iframe(driver, iframe_selector, timeout=10):
    """
    iframe으로 전환하는 함수. 전환에 실패하면 기본 프레임에서 진행.
    
    :param driver: Selenium WebDriver
    :param iframe_selector: iframe을 찾기 위한 CSS Selector 또는 XPath
    :param timeout: iframe을 찾기 위한 최대 대기 시간
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, iframe_selector))
        )
        print(f"iframe({iframe_selector})으로 전환 완료")
    except Exception as e:
        print(f"iframe 전환 중 오류 발생: {e}. 기본 프레임에서 작업을 계속합니다.")

def switch_to_default_content(driver):
    """
    기본 프레임으로 돌아오는 함수.
    
    :param driver: Selenium WebDriver
    """
    try:
        driver.switch_to.default_content()
        print("기본 프레임으로 돌아옴")
    except Exception as e:
        print(f"기본 프레임으로 돌아오는 중 오류 발생: {e}")
