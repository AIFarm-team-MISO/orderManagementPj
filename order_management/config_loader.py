import os
import configparser
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob
import platform

def load_config():
    config = configparser.ConfigParser()

    # 운영체제 판별 및 출력
    system_platform = platform.system()
    print(f"현재 플랫폼: {system_platform}")

    # 운영체제에 따라 로컬(Windows) 또는 서버(Ubuntu)의 config 파일을 선택
    if system_platform == 'Windows':
        config_filename = 'config.ini'  # 로컬 설정 파일
    else:
        config_filename = 'config_server.ini'  # 서버 설정 파일

    # 설정 파일의 경로를 설정
    config_path = os.path.join(os.path.dirname(__file__), '..', config_filename)
    
    # 설정 파일을 읽어옴
    config.read(config_path, encoding='utf-8')  # 인코딩을 명시적으로 설정

    # 시스템에 따라 타임아웃 값을 설정 파일에서 가져옴
    timeout = int(config['selenium'].get('timeout', 10))  # 설정 파일에서 timeout 값 불러오고, 기본값은 30초

    print(f"현재 타임아웃 값 : {timeout}")


    return config, timeout


def switch_to_iframe(driver, iframe_selector, timeout=10):
    """
    iframe으로 전환하는 함수. 전환에 실패하면 기본 프레임에서 진행.
    
    :param driver: Selenium WebDriver
    :param iframe_selector: iframe을 찾기 위한 CSS Selector 또는 XPath
    :param timeout: iframe을 찾기 위한 최대 대기 시간
    """
    try:

        print('아이프레임변경 timeout : ', timeout)


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

def get_latest_file(directory):
    """
    주어진 디렉토리에서 가장 최근에 수정된 파일의 경로를 반환합니다.
    
    Args:
        directory (str): 파일을 검색할 디렉토리 경로.
        
    Returns:
        str: 가장 최근에 수정된 파일의 경로.
    """
    list_of_files = glob.glob(os.path.join(directory, '*'))  # 모든 파일 가져오기
    if not list_of_files:
        return None  # 디렉토리가 비어있으면 None 반환
    latest_file = max(list_of_files, key=os.path.getctime)  # 가장 최근 파일 선택
    return latest_file